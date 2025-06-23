import streamlit as st
from auth import register_user, login_user
from database import init_db
from chatbot_engine import chunk_text, get_best_chunk, generate_response
import sqlite3

init_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

menu = ['Login', 'Signup'] if not st.session_state.logged_in else ['Chat', 'Profile', 'History', 'Logout']
choice = st.sidebar.selectbox("Menu", menu)

if choice == 'Login':
    st.title("Login to Childhood Chatbot")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.success(f"Welcome back, {username}!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

elif choice == 'Signup':
    st.title("Create an Account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type='password')
    if st.button("Signup"):
        if register_user(new_user, new_pass):
            st.success("Account created! Go to login.")
        else:
            st.error("Username already exists!")

elif choice == 'Chat':
    st.title("🧒 Childhood Memory Chatbot")
    query = st.text_input("Ask me about your childhood:")
    if st.button("Ask"):
        if query:
            childhood_text = "Playing in the rain, going to school, eating ice cream, watching cartoons, birthday parties..."
            chunks = chunk_text(childhood_text)
            relevant = get_best_chunk(chunks, query)
            reply = generate_response(query, relevant)
            st.markdown(f"**You:** {query}")
            st.markdown(f"**Bot:** {reply}")
            conn = sqlite3.connect('db/chatbot.db')
            c = conn.cursor()
            c.execute("INSERT INTO history (username, message, response) VALUES (?, ?, ?)", 
                      (st.session_state.username, query, reply))
            conn.commit()
            conn.close()

elif choice == 'Profile':
    st.title("👤 Profile")
    st.markdown(f"**Username:** {st.session_state.username}")
    st.info("Feature: Profile editing coming soon!")

elif choice == 'History':
    st.title("📜 Chat History")
    conn = sqlite3.connect('db/chatbot.db')
    c = conn.cursor()
    c.execute("SELECT message, response, timestamp FROM history WHERE username=? ORDER BY timestamp DESC", 
              (st.session_state.username,))
    records = c.fetchall()
    conn.close()
    if records:
        for msg, res, ts in records:
            st.markdown(f"**[{ts}]**")
            st.markdown(f"- **You:** {msg}")
            st.markdown(f"- **Bot:** {res}")
            st.markdown("---")
    else:
        st.info("No history yet!")

elif choice == 'Logout':
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been logged out.")
    st.experimental_rerun()
