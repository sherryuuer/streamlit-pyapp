import streamlit as st
import yfinance as yf
from PIL import Image
import os
import torch
import torchvision
from torch import nn
from timeit import default_timer as timer
from typing import Tuple, Dict

st.title("Sally's CAFE&LAB★")

"""
Welcome!
How are you today! ♡

### Hi there! 👋

Hey, I'm Sally, a data engineer based in Tokyo, Japan. 🗼 Currently diving into the realms of CS and machine learning. I also enjoy dabbling in web development projects.

I'm a foodie who's trying to strike a balance between indulging in delicious eats and maintaining a healthy lifestyle. 🍜 I have a soft spot for Chinese cuisine and love exploring food spots in Ikebukuro.

I'm a cat enthusiast dreaming of having two adorable little male kitties. 🐾 I occasionally hang out with friends and cherish the moments spent with them.

I have a soft spot for all things anime, even though I've been quite busy lately and don't get to indulge as often. 🎮 I'm an avid gamer with a love for titles like Splatoon and Monster Hunter, owning multiple gaming consoles including Nintendo Switch and Xbox. No shame in proudly calling myself a gamer!

I love the thrill of learning new things. It's what makes me feel alive and connected to the beauty of the universe. 🌌 Welcome to my little universe—where growth, curiosity, and good vibes are always in the air!

Feel free to explore and join the journey with me! 🚀✨


"""
img = Image.open("images/buzzimage.png")
st.image(img, caption="sally", use_column_width=True)
