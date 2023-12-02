import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.title("What's on the Menu Today! 🍽️")
# https://docs.gspread.org/en/v5.12.0/


def predict(data_set):
    # Check if the dataset is empty
    if data_set.empty:
        return None

    # Get all values from the "food" column
    food_values = data_set['food'].tolist()

    # Randomly select a food value from the list
    random_food = random.choice(food_values)

    return random_food


def get_data():
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    food = st.text_input("Tell me what you had last time: ")
    mood = st.selectbox("How are you feeling now: ", [
                        "Amazing", "Not bad", "Sad", "Angry"])
    weather = st.selectbox("How's the weather now: ", [
                           "Sunny", "Cloudy", "Raining", "Windy"])
    tempe = st.selectbox("How's the temperature for you: ", [
                         "Freezing", "Moderate", "Hot", "Burning up"])
    return date_time, food, mood, weather, tempe


def get_write_data(user_id, user_data):
    date_time, food, mood, weather, tempe = get_data()
    user_data.loc[len(user_data.index)] = [
        date_time, food, mood, weather, tempe]

    # Add button functionality
    if st.button("Confirm and Save"):
        # Output variables
        st.write(f"User ID: {user_id}")
        st.write(f"Time: {date_time}")
        st.write(f"Food: {food}")
        st.write(f"Mood: {mood}")
        st.write(f"Weather: {weather}")
        st.write(f"Temperature: {tempe}")

        # Save data to file
        user_data.to_csv(f'{user_id}-data.csv', index=False)
        st.write(
            "Data has been saved! Thank you, because of you, every season feels warm now. You can go grab a meal.")


st.write("Let me recommend something delicious for you. 🌮")

# Read existing id-list.csv and id-data.csv, create empty if not exist
try:
    id_list = pd.read_csv('id-list.csv')
    print(id_list)
except FileNotFoundError:
    id_list = pd.DataFrame(columns=['id'])

# Get user input for id
user_id = st.text_input("First, enter your ID:")

if user_id:
    # Check if the entered id is in id-list
    if user_id in id_list['id'].values:
        st.write(f"Welcome back, my old friend, {user_id}! 😊")
        # Check if user data exists, get data
        try:
            user_data = pd.read_csv(f'{user_id}-data.csv')
            predicted_food = predict(user_data)
            st.write(f"How about some {predicted_food} at this hour! 🕒")
            st.write(
                "If it doesn't sound good, give me more data, hope to match your taste better next time. 😋")
            get_write_data(user_id, user_data=user_data)
        except FileNotFoundError:
            st.write(
                "Looks like you don't have any data yet. Please share some data with me so I can recommend better next time! 📊")
            user_data = pd.DataFrame(
                columns=['date_time', 'food', 'mood', 'weather', 'tempe'])
            get_write_data(user_id, user_data)

    else:
        # If not, create a new id and add to id-list
        st.write(
            f"New friend alert! This is your ID, remember it for next time you enter the system: {user_id}. Super welcome! 🌟")

        # Add the new id to id-list
        id_list.loc[len(id_list.index)] = [user_id]
        id_list.to_csv('id-list.csv', index=False)
        st.write("Looks like you don't have any data yet. Please share some data with me so I can recommend better next time! 📊")
        user_data = pd.DataFrame(
            columns=['date_time', 'food', 'mood', 'weather', 'tempe'])
        get_write_data(user_id, user_data)
