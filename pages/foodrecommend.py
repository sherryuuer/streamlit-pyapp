import streamlit as st
import pandas as pd
from datetime import datetime
import random


st.title("今天整点啥！")


def predict(data_set):
    # 检查数据集是否为空
    if data_set.empty:
        return None

    # 获取 "food" 列的所有值
    food_values = data_set['food'].tolist()

    # 从列表中随机选择一个食物值
    random_food = random.choice(food_values)

    return random_food


def get_data():
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    food = st.text_input("告诉我你上次吃了什么?: ")
    mood = st.selectbox("你现在感觉如何: ",["超绝好", "还不错", "伤心", "生气"])
    weather = st.selectbox("天气如何哇现在: ",["大晴天", "多云", "下雨啦", "大风呼啸"])
    tempe = st.selectbox("你感觉温度如何：",["冷死啦", "温度适中", "很热", "热死了"])
    return date_time, food, mood, weather, tempe


def get_write_data(user_id, user_data):
    date_time, food, mood, weather, tempe = get_data()
    user_data.loc[len(user_data.index)] = [date_time, food, mood, weather, tempe]

    # 添加按钮功能
    if st.button("确认并保存"):
        # 输出变量
        st.write(f"用户 ID: {user_id}")
        st.write(f"时间: {date_time}")
        st.write(f"食物: {food}")
        st.write(f"心情: {mood}")
        st.write(f"天气: {weather}")
        st.write(f"温度: {tempe}")

        # 保存数据到文件
        user_data.to_csv(f'{user_id}-data.csv', index=False)
        st.write("数据已保存！谢谢你，因为有你温暖了四季现在你可以去吃饭了。")


st.write("今天我给你推介点吃的。")


# 读取已有的 id-list.csv 和 id-data.csv，如果不存在就创建空的
try:
    id_list = pd.read_csv('id-list.csv')
    print(id_list)
except FileNotFoundError:
    id_list = pd.DataFrame(columns=['id'])

# 获取用户输入的 id
user_id = st.text_input("先输入你的ID吧:")

if user_id:
    # 检查用户输入的 id 是否在 id-list 中
    if user_id in id_list['id'].values:
        st.write(f"欢迎你回来我的老朋友, {user_id}!")
        # 检查用户数据是否存在，取得数据
        try:
            user_data = pd.read_csv(f'{user_id}-data.csv')
            predicted_food = predict(user_data)
            st.write(f"今天整点{predicted_food}吧！")
            st.write("如果觉得不好那就多给我点数据，希望下次能符合你的心意。")
            get_write_data(user_id, user_data=user_data)
        except FileNotFoundError:
            st.write("看来你还没有数据，请给我一些数据让我下次更好地推介你！")
            user_data = pd.DataFrame(columns=['date_time', 'food', 'mood', 'weather', 'tempe'])
            get_write_data(user_id, user_data)

    else:
        # 如果不存在，创建新的 id，并添加到 id-list 中
        st.write(f"新朋友交个朋友! 这是你的ID记住ta下次用来进入系统： {user_id}. 超级欢迎你!")

        # 将新的 id 添加到 id-list 中
        id_list.loc[len(id_list.index)] = [user_id]
        id_list.to_csv('id-list.csv', index=False)
        st.write("看来你还没有数据，请给我一些数据让我下次更好地推介你！")
        user_data = pd.DataFrame(columns=['date_time', 'food', 'mood', 'weather', 'tempe'])
        get_write_data(user_id, user_data)
