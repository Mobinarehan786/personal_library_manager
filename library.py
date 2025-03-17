import streamlit as st
import json
import os

LIBRARY_FILE = "library.json"

# Load Library
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save Library
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize
library = load_library()

# Streamlit UI
st.title("📚 Personal Library Manager")

# Menu Options
menu = ["Home", "Add a Book", "Remove a Book", "Search Books", "View All Books", "Statistics"]
choice = st.sidebar.selectbox("Select an option", menu)

# 📌 Home Page
if choice == "Home":
    st.write("Welcome to your Personal Library Manager!")

# 📌 Add a Book
elif choice == "Add a Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Enter book title")
    author = st.text_input("Enter author name")
    year = st.number_input("Enter publication year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Enter genre")
    read_status = st.checkbox("Mark as Read")

    if st.button("Add Book"):
        library.append({"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status})
        save_library(library)
        st.success(f"Book '{title}' added successfully!")

# 📌 Remove a Book
elif choice == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    book_titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a book to remove", book_titles)

    if st.button("Remove"):
        library = [book for book in library if book["title"] != book_to_remove]
        save_library(library)
        st.success(f"Book '{book_to_remove}' removed successfully!")

# 📌 Search for a Book
elif choice == "Search Books":
    st.subheader("🔍 Search for a Book")
    search_term = st.text_input("Enter book title or author")

    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

# 📌 View All Books
elif choice == "View All Books":
    st.subheader("📚 Your Library")
    if library:
        for book in library:
            st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("No books in the library.")

# 📌 Display Statistics
elif choice == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"📖 **Books Read:** {read_books} ({percentage_read:.1f}%)")

# Save Changes on Exit
save_library(library)
