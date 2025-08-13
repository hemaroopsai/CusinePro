from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableMap

import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",  
    temperature=0.7
)
# Prompt for restaurant name
prompt_name = PromptTemplate(
    input_variables=["cuisine"],
    template=(
        "Suggest 5 fancy restaurant names for a {cuisine} food restaurant.\n"
        "Return ONLY the names, each separated by a newline character (\\n).\n"
        "Do not number them, do not add descriptions."
    )
)

# Prompt for menu
prompt_menu = PromptTemplate(
    input_variables=["restaurant_name"],
    template=(
        "Suggest a menu for my {restaurant_name} restaurant with categories: "
        "Starters, Main Course, Desserts, Beverages. "
        "Menu should have veg and non-veg items. "
        "and a realistic price in INR. "
        "Return each menu item in different line"
        "Also add a empty line in between two  dishes"
    )
)
#prompt for description
prompt_description = PromptTemplate(
    input_variables=["cuisine","restaurant_name","menu"],
    template =( "You are a creative restaurant copywriter.\n"
        "Given the restaurant name: {restaurant_name}, "
        "the cuisine: {cuisine}, and this menu: {menu},\n"
        "write ONE short, catchy tagline (max 15 words) "
        "that makes customers excited to visit.\n"
        "Do not list menu items or explain them. Just make it fun and appealing.")
    
)

# Chain for name
name_chain = prompt_name | llm | StrOutputParser()

# Chain for menu (will receive restaurant_name from name_chain)
menu_chain = prompt_menu | llm | StrOutputParser()

#chain for description chain
description_chain = prompt_description|llm|StrOutputParser()

# Full multi-output chain
full_chain = RunnableMap({
    "restaurant_name": name_chain,
    "menu": name_chain | (lambda x: {"restaurant_name": x}) | menu_chain,
    "description": RunnableMap({"restaurant_name": name_chain,"cuisine": lambda vars: vars["cuisine"],"menu": name_chain | (lambda x: {"restaurant_name": x}) | menu_chain}) | description_chain
})


def get_restaurant_and_menu(cuisine: str):
    """Run the chain and return name + menu"""
    return full_chain.invoke({"cuisine": cuisine})
