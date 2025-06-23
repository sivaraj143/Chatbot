# --- admin.py ---
# Placeholder for admin functions (can include user stats, delete user, etc.)

def get_all_users():
    import sqlite3
    conn = sqlite3.connect('db/chatbot.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    users = c.fetchall()
    conn.close()
    return users
