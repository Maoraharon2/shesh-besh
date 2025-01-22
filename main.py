import streamlit as st

def header(string):
    return st.markdown(f"<h2 style='text-align: center; color: black;'>{string}</h2>", unsafe_allow_html=True)

def initialize_session_state():
    if 'player1_name' not in st.session_state:
        st.session_state.player1_name = ""
    if 'player2_name' not in st.session_state:
        st.session_state.player2_name = ""
    if 'player1_score' not in st.session_state:
        st.session_state.player1_score = 0
    if 'player2_score' not in st.session_state:
        st.session_state.player2_score = 0
    if 'current_game_history' not in st.session_state:
        st.session_state.current_game_history = []
    if 'games_history' not in st.session_state:
        st.session_state.games_history = []
    if 'matches_score' not in st.session_state:
        st.session_state.matches_score = {
            'player1': 0,
            'player2': 0
        }


def reset_game():
    # שמירת המשחק בהיסטוריה לפני האיפוס
    if st.session_state.current_game_history:
        game_summary = {
            'player1': st.session_state.player1_name,
            'player2': st.session_state.player2_name,
            'score': f"{st.session_state.player1_score}-{st.session_state.player2_score}",
            'history': st.session_state.current_game_history.copy()
        }
        st.session_state.games_history.append(game_summary)

    st.session_state.player1_score = 0
    st.session_state.player2_score = 0
    st.session_state.current_game_history = []


def main():
    # st.title("מעקב ניקוד שש-בש 🎲")
    header("🎲 שש-בש 🎲")

    initialize_session_state()

    col1, col2 = st.columns(2)
    with col1:
        player1_name = st.text_input("שם שחקן 1", value=st.session_state.player1_name, key="p1_name")
        st.session_state.player1_name = player1_name
    with col2:
        player2_name = st.text_input("שם שחקן 2", value=st.session_state.player2_name, key="p2_name")
        st.session_state.player2_name = player2_name

    if not player1_name or not player2_name:
        st.warning("אנא הכניסו את שמות שני השחקנים")
        return
    st.divider()

    # ניקוד כללי של משחקים
    header("משחקים")
    matches_col1, matches_col2 = st.columns(2)
    with matches_col1:
        header(f"{player1_name}: {st.session_state.matches_score['player1']}")
        st.write(f"**{player1_name}: {st.session_state.matches_score['player1']}**")
    with matches_col2:
        # st.write(f"**{player2_name}: {st.session_state.matches_score['player2']}**")
        header(f"{player2_name}: {st.session_state.matches_score['player2']}")
    st.divider()

    header("עדכון תוצאה")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"הוסף משחקון ל{player1_name}"):
            st.session_state.player1_score += 1
            st.session_state.current_game_history.append(f"{player1_name} זכה במשחקון")
            if st.session_state.player1_score >= 3:
                st.balloons()
                st.success(f"🏆 {player1_name} ניצח במשחק!")
                st.session_state.matches_score['player1'] += 1
                # שמירת המשחק בהיסטוריה
                game_summary = {
                    'player1': player1_name,
                    'player2': player2_name,
                    'score': f"{st.session_state.player1_score}-{st.session_state.player2_score}",
                    'winner': player1_name,
                    'history': st.session_state.current_game_history.copy()
                }
                st.session_state.games_history.append(game_summary)
                st.session_state.player1_score = 0
                st.session_state.player2_score = 0
                st.session_state.current_game_history = []
                st.rerun()
    # st.divider()

    with col3:
        if st.button(f"הוסף ניקוד ל{player2_name}"):
            st.session_state.player2_score += 1
            st.session_state.current_game_history.append(f"{player2_name} זכה במשחקון")
            if st.session_state.player2_score >= 3:
                st.balloons()
                st.success(f"🏆 {player2_name} ניצח במשחק!")
                st.session_state.matches_score['player2'] += 1
                # שמירת המשחק בהיסטוריה
                game_summary = {
                    'player1': player1_name,
                    'player2': player2_name,
                    'score': f"{st.session_state.player1_score}-{st.session_state.player2_score}",
                    'winner': player2_name,
                    'history': st.session_state.current_game_history.copy()
                }
                st.session_state.games_history.append(game_summary)
                # איפוס המשחק הנוכחי
                st.session_state.player1_score = 0
                st.session_state.player2_score = 0
                st.session_state.current_game_history = []
                st.rerun()

    # היסטוריית המשחק הנוכחי
    st.divider()
    st.header("היסטוריית המשחק הנוכחי")
    for event in st.session_state.current_game_history:
        st.write(event)

    st.divider()
    # היסטוריית כל המשחקים
    st.header("היסטוריית משחקים")
    for i, game in enumerate(st.session_state.games_history[::-1], 1):
        with st.expander(f"משחק {len(st.session_state.games_history) - i + 1}"):
            st.write(f"**{game['player1']}** מול **{game['player2']}**")
            st.write(f"תוצאה: {game['score']}")
            st.write(f"מנצח: {game['winner']}")
            st.write("מהלך המשחק:")
            for index, event in enumerate(game['history']):
                st.write(f"{index + 1} - {event}")

    # כפתור לאיפוס הכל
    if st.button("איפוס כל המשחקים"):
        st.session_state.matches_score = {'player1': 0, 'player2': 0}
        st.session_state.games_history = []
        reset_game()
        st.rerun()


if __name__ == "__main__":
    main()