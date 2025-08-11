
import streamlit as st

st.title("LangChain Restaurant Recommender 🍽️")

cuisine = st.text_input("Enter cuisine type:")
if cuisine:
    st.write(f"Recommended restaurant for {cuisine}: ChatGPT's Kitchen")
    st.write(f"Sample Menu for {cuisine}: Dish 1, Dish 2, Dish 3")
