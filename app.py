import streamlit as st
from Method import get_restaurant_and_menu

st.title("LangChain Restaurant Recommender 🍽️")

cuisine = st.sidebar.selectbox(
    "Pick a cuisine",
    ("Indian", "Mexican", "Italian", "American", "Chinese", "Japanese", "Arabian", "French")
)

if st.button("Get Recommendation"):
    result = get_restaurant_and_menu(cuisine)
    st.subheader("Restaurant Name")
    st.write(result["restaurant_name"])

    st.subheader("Menu")
    st.write(result["menu"])
