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
turtles = [Turtle('Turtle 1'), Turtle('Turtle 2'), Turtle('Turtle 3')]

st.title("乌龟赛跑游戏")

# 提示用户猜测哪只乌龟会赢
user_guess = st.selectbox("请选择你认为会获胜的乌龟:", [t.name for t in turtles])

# 按钮用于开始比赛
if st.button("开始比赛"):
    race_finished = False
    winner = None

    # 绘图初始化
    fig, ax = plt.subplots()
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6])
    ax.set_yticklabels([t.name for t in turtles])

    turtle_lines = [ax.plot([], [], 'o-', label=t.name)[0] for t in turtles]

    # 赛跑过程的模拟
    while not race_finished:
        for i, turtle in enumerate(turtles):
            turtle.move()
            if turtle.position >= 50:
                race_finished = True
                winner = turtle.name
                break
            turtle_lines[i].set_data([0, turtle.position], [i*2 + 2, i*2 + 2])

        # 更新绘图
        ax.legend()
        st.pyplot(fig)
        time.sleep(0.5)

    st.write(f"比赛结束，{winner} 获胜！")

    if user_guess == winner:
        st.success("恭喜你猜对了！")
    else:
        st.error("很遗憾，猜错了。")
