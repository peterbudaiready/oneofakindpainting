import streamlit as st
import sqlite3
from datetime import datetime  # ✅ Import datetime

# Set Streamlit page config
st.set_page_config(page_title="Manage Blog Posts", initial_sidebar_state="collapsed")

# Database name and admin password
DB_NAME = "blog.db"
PASSWORD = "Aaabacadae1."

# Initialize database function
def initialize_database():
    """Ensures the database and the 'posts' table exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create table if it does not exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image TEXT,  -- Feature image URL
            content TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Call the function to initialize the database
initialize_database()

# Password protection
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def authenticate(password):
    return password == PASSWORD

if not st.session_state.authenticated:
    st.title("🔒 Password Required")
    password_input = st.text_input("Enter Password:", type="password")
    if st.button("Submit"):
        if authenticate(password_input):
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Incorrect password. Try again.")
    st.stop()  # Stops execution if not authenticated

# Function to get all posts
def get_all_posts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, image, content, date FROM posts ORDER BY date DESC")
    posts = c.fetchall()
    conn.close()
    return posts

# Function to delete a post
def delete_post(post_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()

# Function to create a new blog post
def create_blog_post():
    st.subheader("Create a New Blog Post")
    title = st.text_input("Title")
    feature_image = st.text_input("Feature Image URL (Optional)")
    content = st.text_area("Blog Content (Full Post)")

    if st.button("Submit Post"):
        if not title or not content:
            st.error("Title and Content are required!")
            return
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO posts (title, image, content, date)
            VALUES (?, ?, ?, ?)
        ''', (title, feature_image, content, datetime.now().strftime("%Y-%m-%d")))
        
        conn.commit()
        conn.close()
        st.success("Post Created Successfully")
        st.experimental_rerun()

# Display Blog Posts (Management UI)
st.title("📚 Blog Management")
st.subheader("Manage Blog Posts")

posts = get_all_posts()
if not posts:
    st.info("No blog posts available.")
else:
    for post in posts:
        col1, col2 = st.columns([4, 1])  
        with col1:
            st.markdown(f"**{post[1]}**")  
        with col2:
            if st.button("🗑️ Delete", key=f"del_{post[0]}"):
                delete_post(post[0])
                st.experimental_rerun()

st.markdown("---")
create_blog_post()
