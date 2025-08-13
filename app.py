import streamlit as st
import os
from Method import get_restaurant_and_menu
from openai import OpenAI
st.title("LangChain CuisineCrafter 🍽️")


client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"]
)
st.sidebar.subheader("Cuisine Selection")
quick_cuisine = st.sidebar.selectbox(
    "Pick a cuisine",
    ("Indian", "Mexican", "Italian", "American", "Chinese", "Japanese", "Arabian", "French")
)
custom_cuisine = st.sidebar.text_input("Or enter a custom cuisine:")

cuisine = custom_cuisine.strip() if custom_cuisine.strip() else quick_cuisine

if not cuisine:
    st.warning("Please select or enter a cuisine.")
else:
    
    if "result" not in st.session_state:
        st.session_state.result = None

    # Get full recommendation
    if st.button("Get Recommendation"):
        st.session_state.result = get_restaurant_and_menu(cuisine)

    # Regenerate only names
    if st.button("Regenerate Names"):
        if st.session_state.result:
            new_result = get_restaurant_and_menu(cuisine)
            st.session_state.result["restaurant_name"] = new_result["restaurant_name"]
        else:
            st.warning("Please get a recommendation first.")

    # Regenerate only menu
    if st.button("Regenerate Menu"):
        if st.session_state.result:
            new_result = get_restaurant_and_menu(cuisine)
            st.session_state.result["menu"] = new_result["menu"]
        else:
            st.warning("Please get a recommendation first.")

    
    if st.session_state.result:
        result = st.session_state.result
      
        names = result["restaurant_name"]
        if isinstance(names, str):
            name_list = [n.strip() for n in names.replace(",", "\n").split("\n") if n.strip()]
        elif isinstance(names, list):
            name_list = names
        else:
            name_list = [str(names)]

        st.subheader("Restaurant Name(s)")
        for name in name_list:
            st.write(f"• {name}")

        
        menu_items = result["menu"]

        if isinstance(menu_items, str):
            lines = [m.strip() for m in menu_items.split("\n") if m.strip()]
        elif isinstance(menu_items, list):
            lines = menu_items
        else:
            lines = [str(menu_items)]

        table_rows = []
        for line in lines:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 3:  
                table_rows.append(parts)

        st.subheader("Menu")
        if table_rows:
            st.table(table_rows)
        else:
            for item in lines:
                st.write(f"• {item}")



        st.subheader("Description")
        st.write(result["description"])

      
        if name_list:
            st.subheader("Restaurant Logo")
            restaurant_name = name_list[0]
            prompt = f"Professional, high-quality logo design for a {cuisine} restaurant named '{restaurant_name}'. Modern and attractive."
            
            try:
                img_response = client.images.generate(
                    model="black-forest-labs/FLUX.1-krea-dev",  
                    prompt=prompt,
                    size="512x512"
                )
                image_url = img_response.data[0].url
                st.image(image_url, caption=f"{restaurant_name} Logo")
            except Exception as e:
                st.error(f"Image generation failed: {e}")

    
