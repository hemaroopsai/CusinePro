# restaurant_chain.py
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableMap

import os

os.environ["OPENAI_API_KEY"] = "3b6b1ede3b255be31ff6e0b68c4188e80a50f62faca210c39d6807837bb7e4f5"
os.environ["OPENAI_BASE_URL"] = "https://api.together.xyz/v1"
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",  # change model here
    temperature=0.7
)
# Step 1: Prompt for restaurant name
prompt_name = PromptTemplate(
    input_variables=["cuisine"],
    template="Suggest a fancy restaurant name for a {cuisine} food restaurant."
)

# Step 2: Prompt for menu
prompt_menu = PromptTemplate(
    input_variables=["restaurant_name"],
    template=(
        "Suggest some menu items for my {restaurant_name} restaurant. "
        "Menu should have veg and non-veg items. "
        "Return as a comma-separated list."
    )
)

# Chain for name
name_chain = prompt_name | llm | StrOutputParser()

# Chain for menu (will receive restaurant_name from name_chain)
menu_chain = prompt_menu | llm | StrOutputParser()

# Full multi-output chain
full_chain = RunnableMap({
    "restaurant_name": name_chain,
    "menu": name_chain | (lambda x: {"restaurant_name": x}) | menu_chain
})


def get_restaurant_and_menu(cuisine: str):
    """Run the chain and return name + menu"""
    return full_chain.invoke({"cuisine": cuisine})
