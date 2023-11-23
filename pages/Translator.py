import streamlit as st
from translate import Translator

st.title("Translator Asistant")
tolang = st.radio("Which language do you want to translate to?",
                  ["日本語に", "翻译成中文"])
user_input = st.text_area("Input some English:) ")

if st.button("Translate!"):
    if tolang == "日本語に":
        translator = Translator(to_lang="ja")
    else:
        translator = Translator(to_lang="zh")
    translation = translator.translate(user_input)
    st.write(translation)
