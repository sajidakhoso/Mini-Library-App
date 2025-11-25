import streamlit as st
import os

FILE_PATH = "books.txt"

# Ensure file exists
def init_file():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            pass

# Load all books
def load_books():
    init_file()
    books = []
    with open(FILE_PATH, "r") as f:
        for line in f.readlines():
            parts = line.strip().split(",")
            if len(parts) == 5:
                books.append({
                    "ISBN": parts[0],
                    "Title": parts[1],
                    "Author": parts[2],
                    "Year": parts[3],
                    "Category": parts[4]
                })
    return books

# Save books
def save_books(books):
    with open(FILE_PATH, "w") as f:
        for b in books:
            f.write(f"{b['ISBN']},{b['Title']},{b['Author']},{b['Year']},{b['Category']}\n")

# Add a book
def add_book(isbn, title, author, year, category):
    books = load_books()
    for b in books:
        if b["ISBN"] == isbn:
            return False, "ISBN already exists!"
    
    books.append({
        "ISBN": isbn,
        "Title": title,
        "Author": author,
        "Year": year,
        "Category": category
    })
    
    save_books(books)
    return True, "Book added successfully!"

# Search book
def search_book(isbn):
    books = load_books()
    for b in books:
        if b["ISBN"] == isbn:
            return b
    return None

# Delete book
def delete_book(isbn):
    books = load_books()
    new_books = [b for b in books if b["ISBN"] != isbn]

    if len(new_books) == len(books):
        return False
    
    save_books(new_books)
    return True

# Update book
def update_book(isbn, title, author, year, category):
    books = load_books()
    found = False

    for b in books:
        if b["ISBN"] == isbn:
            b["Title"] = title
            b["Author"] = author
            b["Year"] = year
            b["Category"] = category
            found = True
            break

    if found:
        save_books(books)

    return found


# STREAMLIT UI 

st.set_page_config(page_title="Library Management System", layout="wide")

st.title("Library Book Management System")

# Developer credit
st.markdown("<h4 style='color:#666;'>Developed By: <b style='color:#4CAF50;'>Sajida Khoso</b></h4>", unsafe_allow_html=True)

# Sidebar
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Book", "View All Books", "Search Book", "Update Book", "Delete Book"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Developed By:** Sajida Khoso")

st.sidebar.markdown(
    "<a href='https://github.com/sajidakhoso' target='_blank'>"
    "<button style='background-color:#4CAF50;color:white;padding:8px 14px;border:none;border-radius:5px;'>"
    "GitHub Profile"
    "</button></a>",
    unsafe_allow_html=True
)

# APP SCREENS

# ADD BOOK
if menu == "Add Book":
    st.subheader("Add New Book")
    
    isbn = st.text_input("ISBN (numeric)")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.text_input("Year (4 digits)")
    category = st.text_input("Category")

    if st.button("Add Book"):
        if not isbn.isdigit():
            st.error("ISBN must be numeric!")
        elif not year.isdigit() or len(year) != 4:
            st.error("Year must be a 4-digit number!")
        elif not title.strip() or not author.strip() or not category.strip():
            st.error("All fields must be filled!")
        else:
            ok, msg = add_book(isbn, title, author, year, category)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

# VIEW BOOKS
elif menu == "View All Books":
    st.subheader("All Books")
    books = load_books()

    if books:
        st.dataframe(books)
    else:
        st.info("No books found.")

# SEARCH BOOK
elif menu == "Search Book":
    st.subheader("Search Book by ISBN")
    isbn = st.text_input("Enter ISBN")

    if st.button("Search"):
        book = search_book(isbn)
        if book:
            st.success("Book Found:")
            st.json(book)
        else:
            st.error("Book not found!")

# UPDATE BOOK
elif menu == "Update Book":
    st.subheader("Update Book Details")
    isbn = st.text_input("Enter ISBN to Update")

    if st.button("Fetch Details"):
        book = search_book(isbn)
        if book:
            st.session_state["update_book"] = book
        else:
            st.error("Book not found!")

    if "update_book" in st.session_state:
        book = st.session_state["update_book"]

        title = st.text_input("Title", book["Title"])
        author = st.text_input("Author", book["Author"])
        year = st.text_input("Year", book["Year"])
        category = st.text_input("Category", book["Category"])

        if st.button("Update Book"):
            if update_book(isbn, title, author, year, category):
                st.success("Book updated successfully!")
            else:
                st.error("Update failed.")

# DELETE BOOK
elif menu == "Delete Book":
    st.subheader("Delete Book")
    isbn = st.text_input("Enter ISBN to Delete")
    
    if st.button("Delete Book"):
        if delete_book(isbn):
            st.success("Book deleted successfully!")
        else:
            st.error("Book not found!")


# Footer
st.markdown("""
<br><hr>
<center>
🌸 <b>Library System — Developed by Sajida Khoso</b> 🌸  
<br>
<a href='https://github.com/sajidakhoso' target='_blank'>🔗 Visit GitHub Profile</a>
</center>
""", unsafe_allow_html=True)

