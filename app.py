import streamlit as st
import json
import os

FILE_NAME = "library.txt"

# Load library from file
def load_library():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

# Save library to file
def save_library(library):
    with open(FILE_NAME, "w") as f:
        json.dump(library, f)

# Display book
def display_book(book):
    status = "✅ Read" if book["read"] else "❌ Unread"
    st.write(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")

# Main app
def main():
    st.title("📚 Personal Library Manager")
    library = st.session_state.get("library", load_library())

    menu = ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"]
    choice = st.sidebar.radio("Menu", menu)

    # Add Book
    if choice == "Add Book":
        st.subheader("➕ Add a New Book")
        with st.form("add_form"):
            title = st.text_input("Enter book title:")
            author = st.text_input("Enter author name:")
            year = st.number_input("Enter publication Year:", min_value=0, step=1)
            genre = st.text_input("Enter book genre:")
            read = st.radio("Have you read it?", ["Yes", "No"])
            submitted = st.form_submit_button("Add Book")
            if submitted:
                book = {
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": True if read == "Yes" else False
                }
                library.append(book)
                st.session_state.library = library
                save_library(library)
                st.success("Book added!")

    # Remove Book
    elif choice == "Remove Book":
        st.subheader("🗑️ Remove a Book")
        titles = [book["title"] for book in library]
        if titles:
            selected = st.selectbox("Select a book to remove", titles)
            if st.button("Remove Book"):
                library = [book for book in library if book["title"] != selected]
                st.session_state.library = library
                save_library(library)
                st.success(f"Removed: {selected}")
        else:
            st.info("Library is empty.")

    # Search Book
    elif choice == "Search Book":
        st.subheader("🔍 Search for a Book")
        keyword = st.text_input("Enter book title or author name")
        if keyword:
            matches = [book for book in library if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower()]
            if matches:
                for book in matches:
                    display_book(book)
            else:
                st.warning("❌ No matching books found.")

    # Display All Books
    elif choice == "Display All Books":
        st.subheader("📖 Your Library")
        if library:
            for book in library:
                display_book(book)
        else:
            st.info("No books in your library.")

    # Library Statistics
    elif choice == "Statistics":
        st.subheader("📊 Library Statistics")
        total = len(library)
        read_count = sum(1 for b in library if b["read"])
        percent = (read_count / total * 100) if total else 0
        st.write(f"**Total Books:** {total}")
        st.write(f"**Books Read:** {read_count} ({percent:.1f}%)")

if "library" not in st.session_state:
    st.session_state.library = load_library()

if __name__ == "__main__":
    main()
