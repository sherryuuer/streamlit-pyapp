import streamlit as st
import random
import matplotlib.pyplot as plt
import time

# 定义乌龟类


class Turtle:
    def __init__(self, name):
        self.name = name
        self.position = 0

    def move(self):
        self.position += random.randint(1, 6)


# 初始化乌龟们
if 'turtles' not in st.session_state:
    st.session_state.turtles = [
        Turtle('Turtle 1'), Turtle('Turtle 2'), Turtle('Turtle 3')]
    st.session_state.race_finished = False
    st.session_state.winner = None

turtles = st.session_state.turtles

st.title("乌龟赛跑游戏")

# 提示用户猜测哪只乌龟会赢
user_guess = st.selectbox("请选择你认为会获胜的乌龟:", [t.name for t in turtles])

# 按钮用于开始比赛
if st.button("开始比赛") and not st.session_state.race_finished:
    fig, ax = plt.subplots()
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6])
    ax.set_yticklabels([t.name for t in turtles])

    turtle_lines = [ax.plot([], [], 'o-', label=t.name)[0] for t in turtles]

    while not st.session_state.race_finished:
        for i, turtle in enumerate(turtles):
            turtle.move()
            if turtle.position >= 50:
                st.session_state.race_finished = True
                st.session_state.winner = turtle.name
                break
            turtle_lines[i].set_data([0, turtle.position], [i*2 + 2, i*2 + 2])

        ax.legend()
        st.pyplot(fig)

        # 延时 0.5 秒以模拟动态效果
        time.sleep(0.5)

        # 更新页面并保持比赛状态
        st.experimental_rerun()

# 比赛结束后的结果展示
if st.session_state.race_finished:
    st.write(f"比赛结束，{st.session_state.winner} 获胜！")
    if user_guess == st.session_state.winner:
        st.success("恭喜你猜对了！")
    else:
        st.error("很遗憾，猜错了。")
