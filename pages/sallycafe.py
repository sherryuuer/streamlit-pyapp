import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from subprocess import check_output
import time


df_data_ramdom = pd.DataFrame(
    np.random.rand(20, 3),
    columns=["a", "b", "c"],
)

df_family = pd.DataFrame({
    "who": ["dad", "mom", "bro", "me"],
    "animal": ["rabbit", "rabbit", "tiger", "snake"],
    "state": ["warm", "happy", "full", "study"],
    "location": ["xining", "zhengzhou", "zhengzhou", "tokyo"],
    "heart_location": ["home", "home", "home", "home"],
})

df_location = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])


def write_title(message):
    """Write title."""
    st.title(message)


def write_message(message):
    st.write(message)


def show_image():
    """Show image."""
    img = Image.open("buzzimage.png")
    st.image(img, caption="mememe", use_column_width=True)


def show_map(df):
    """Show locations on map."""
    st.map(df)


def show_chart(df):
    """Show the dataframe in chart."""
    st.line_chart(df)
    st.bar_chart(df)
    st.area_chart(df)


def show_df(df):
    # show dataframe in three way
    # st.write(df)
    # st.dataframe(df.style.highlight_max(axis=0))  # width=200, height=200
    # st.write("table method to show static table:")
    st.table(df)


def show_progress():
    st.write("WAIT A MINITES!!")
    bar = st.progress(0)
    with st.empty():
        for i in range(100):
            st.write(i + 1, "% was been loaded!")
            time.sleep(0.01)
            bar.progress(i + 1)


def show_expander():
    expander = st.expander("Where are you now?")
    expander.write("I am in lanzhou.")


def sidebar():
    """sidebar to control"""
    st.sidebar.write("How do you feel today!")

    # checkbox
    # if st.sidebar.checkbox("Show the image", value=True):
    #     show_image()

    # selectbox
    option = st.sidebar.selectbox("SELECT the weather today:",
                                  ["SUN", "RAIN", "CLOUDY"])
    st.write(option, "is the weather.")

    # text box
    text = st.sidebar.text_area("Please input your state: ",
                                value="Great!!!")
    st.write("YOUR STATE IS ", text)

    # slider
    state_num = st.sidebar.slider("HOW DO U FEEL?", 0, 100, 50)
    if state_num < 50:
        state = "not happy."
    elif state_num == 50:
        state = "not bad."
    else:
        state = "happy."
    st.write("YOU FEEL ", state)


def link_html():
    if st.button('Show Html file'):
        file_name = 'index.html'
        check_output("start " + file_name, shell=True)


# link_html()
write_title("Sally's CAFE☆")
# show_progress()
write_message("CHECK your state in the slider bar!")
sidebar()
# show_expander()
write_message("This is our great CAFE stock!")
show_chart(df_data_ramdom)
write_message("This is our GOLD manager!")
show_image()
# show_df(df_family)
write_message("Here is where I am!! Come to me!")
show_map(df_location)


# markdown
"""
@Sally
--------------------------------------------------
## Great Day
### Today I am going to meet my famliy.So exciting.
```python
import today as a good day.
```
this is markdown!!!!easy!
"""
