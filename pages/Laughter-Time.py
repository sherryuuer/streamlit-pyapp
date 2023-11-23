import streamlit as st
import pyjokes


st.title("Get the joke today and go to study!")
random_joke = pyjokes.get_joke("en", "all")
st.markdown("# :rainbow[XD🚀✨]")
st.markdown(
    f"""
    {random_joke}
    """
)
