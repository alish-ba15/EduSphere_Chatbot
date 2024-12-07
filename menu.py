import streamlit as st


def authenticated_menu():
    st.sidebar.header("Navigation")

    st.sidebar.page_link("app.py", label="Switch accounts")


    if st.session_state.get("role") == "Teacher":
        st.sidebar.header("Teacher Menu")
        st.sidebar.page_link("pages/quiz.py", label="Create and View Quizzes")
        
    elif st.session_state.get("role") == "Student":
        st.sidebar.header("Student Menu")
        st.sidebar.page_link("pages/chat_bot.py", label="Chat with your Lecture!")
    else:
        st.sidebar.warning("Role not recognized. Please contact support.")



def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()