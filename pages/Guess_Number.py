import random
import streamlit as st


def game(goal_number, your_number):
    if your_number == goal_number:
        st.success(f"The goal number is {goal_number}. You win!")
        return True
    elif your_number < goal_number:
        st.warning("Too low!")
        return False
    else:
        st.warning("Too high!")
        return False


def choose_difficulty():
    difficulty = st.selectbox("Choose difficulty:", options=[
                              "easy", "hard"], key="difficulty")
    st.session_state['times'] = 10 if difficulty == "easy" else 5
    st.write(
        f"You have {st.session_state['times']} attempts to guess the number.")


def play_game(goal_number, max_attempts):
    # 在原始代码中，st.session_state['attempt'] += 1 这行代码被放在了 play_game 函数的开头。
    # 由于 Streamlit 的工作方式，每次用户与界面交互（比如输入数字）时，整个脚本都会重新运行。
    # 这导致 attempt 计数器在用户每次与界面交互时都会增加，而不仅仅是在提交猜测时。
    # st.session_state['attempt'] += 1
    your_number = st.number_input(
        "Choose your number:", min_value=1, max_value=100, step=1, key="your_number")

    if st.button("Submit"):
        st.session_state['attempt'] += 1
    if st.button("Submit"):
        if st.session_state['attempt'] <= max_attempts:
            result = game(goal_number, your_number)
            remaining_attempts = max_attempts - st.session_state['attempt']
            st.write(f"Remaining attempts: {remaining_attempts}")
            if result:
                st.session_state['game_over'] = True
            elif st.session_state['attempt'] >= max_attempts:
                st.error(f"No attempts. The goal number was {goal_number}.")
                st.session_state['game_over'] = True
        else:
            st.error("No attempts left. Please restart the game.")


def reset_game():
    st.session_state['game_over'] = False
    st.session_state['attempt'] = 0
    st.session_state['goal_number'] = random.randint(1, 100)
    st.session_state['difficulty'] = 'easy'
    st.session_state['your_number'] = 1  # Reset number input


def main():
    st.title("Guess Number Game")

    if 'game_over' not in st.session_state:
        st.session_state['game_over'] = False
    if 'attempt' not in st.session_state:
        st.session_state['attempt'] = 0
    if 'goal_number' not in st.session_state:
        st.session_state['goal_number'] = random.randint(1, 100)
    if 'difficulty' not in st.session_state:
        st.session_state['difficulty'] = 'easy'

    if st.session_state['game_over']:
        st.button("Restart Game", on_click=lambda: reset_game())
    else:
        choose_difficulty()
        play_game(st.session_state['goal_number'], st.session_state['times'])


if __name__ == "__main__":
    main()
