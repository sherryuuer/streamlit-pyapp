import random
import streamlit as st

# 比較する


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


def play_game(goal_number, times):
    st.session_state['attempt'] += 1
    your_number = st.number_input(
        "Choose your number:", min_value=1, max_value=100, step=1, key="your_number")

    if st.button("Submit"):
        result = game(goal_number, your_number)
        if result or st.session_state['attempt'] >= times:
            st.session_state['game_over'] = True
        else:
            st.session_state['attempts_left'] = times - \
                st.session_state['attempt']


def main():
    st.title("Guess the Number Game!!")

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

    if not st.session_state['game_over']:
        choose_difficulty()
        play_game(st.session_state['goal_number'], st.session_state['times'])


def choose_difficulty():
    difficulty = st.selectbox("Choose difficulty:", options=[
                              "easy", "hard"], key="difficulty")
    st.session_state['times'] = 10 if difficulty == "easy" else 5
    st.write(
        f"You have {st.session_state['times']} attempts to guess the number.")


def reset_game():
    st.session_state['game_over'] = False
    st.session_state['attempt'] = 0
    st.session_state['goal_number'] = random.randint(1, 100)
    st.session_state['difficulty'] = 'easy'


if __name__ == "__main__":
    main()
