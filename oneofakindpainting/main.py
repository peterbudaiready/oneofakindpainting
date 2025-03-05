import streamlit as st
import sqlite3
from datetime import datetime

# Define database name at the top
DB_NAME = "blog.db"

def initialize_database():
    """Creates the database, ensures the correct schema, and adds sample data if empty."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create the posts table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image TEXT,  -- Can be NULL
            content TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Check if there are any posts already
    c.execute("SELECT COUNT(*) FROM posts")
    count = c.fetchone()[0]

    # If no posts exist, insert sample data
    if count == 0:
        c.executemany('''
            INSERT INTO posts (title, image, content, date) VALUES (?, ?, ?, ?)
        ''', [
            ("First Blog Post", "https://via.placeholder.com/150", "This is the content of the first post.", "2025-03-01"),
            ("Second Blog Post", "https://via.placeholder.com/150", "Here's another blog post with some interesting content.", "2025-03-02")
        ])

    conn.commit()
    conn.close()

# Call this function early to ensure DB exists
initialize_database()

# Set page configuration with title and favicon (optional)
st.set_page_config(
    page_title="My Website",
    page_icon="logo.png",  
    initial_sidebar_state="collapsed"
)

# Display logo at the top
logo_path = "oneofakindpainting/logo.png"

if logo_path:
    st.image(logo_path, width=300)  
else:
    st.warning("⚠️ Logo not found. Make sure 'logo.png' exists.")

DB_NAME = "blog.db"

def get_all_posts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, image, content, date FROM posts ORDER BY date DESC")
    posts = c.fetchall()
    conn.close()
    return posts

def get_post_by_id(post_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT title, image, content, date FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    conn.close()
    return post

def blog_archive():
    st.title("One of a Kind Painting")  
    st.markdown("<meta name='description' content='Browse our latest blog posts with insights and updates on painting services.'>", unsafe_allow_html=True)
    
    posts = get_all_posts()
    col1, col2 = st.columns(2)
    
    for index, post in enumerate(posts):
        with (col1 if index % 2 == 0 else col2):
            st.markdown(f"### {post[1]}")
            st.image(post[2] if post[2] else 'https://via.placeholder.com/150', width=150)
            st.markdown(f"*{post[3][:100]}...* ")
            if st.button(f"Read More {post[0]}", key=f"post_{post[0]}"):
                st.session_state.page = "blog_post"
                st.session_state.selected_post = post[0]
                st.experimental_rerun()

def show_blog_post():
    if "selected_post" in st.session_state:
        post_id = st.session_state.selected_post
        post = get_post_by_id(post_id)
        
        if post:
            st.title(post[0])
            st.image(post[1] if post[1] else 'https://via.placeholder.com/150', width=400)
            st.write(post[2])
            st.markdown(f"📅 Published on {post[3]}")
        else:
            st.error("Post not found.")
    else:
        st.warning("No post selected.")

if "page" not in st.session_state:
    st.session_state.page = "archive"

if st.session_state.page == "archive":
    blog_archive()
elif st.session_state.page == "blog_post":
    show_blog_post()
