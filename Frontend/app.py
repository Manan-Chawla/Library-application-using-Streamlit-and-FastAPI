import streamlit as st
import requests

# ================= CONFIG =================
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Library App",
    page_icon="📚",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}

.card {
    background-color: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
}

.card h3 {
    margin-top: 0;
    color: black;
}

.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.available {
    background-color: #dcfce7;
    color: black;
}

.unavailable {
    background-color: #fee2e2;
    color: #991b1b;
}

.add-form {
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("📚 Library Management App")

# ================= SIDEBAR FORM =================
st.sidebar.header("➕ Add New Book")

with st.sidebar.form("add_book_form"):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    isbn = st.text_input("ISBN")
    submit = st.form_submit_button("Add Book")

    if submit:
        if not title or not author or not isbn:
            st.sidebar.error("All fields are required!")
        else:
            payload = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "is_available": True
            }

            try:
                res = requests.post(f"{BASE_URL}/books/", json=payload)
                if res.status_code == 200:
                    st.sidebar.success("Book added successfully 🎉")
                    st.rerun()
                else:
                    st.sidebar.error("Failed to add book")
            except requests.exceptions.RequestException:
                st.sidebar.error("Server not reachable")

# ================= BOOK LIST =================
st.subheader("📖 Available Books")

try:
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 200:
        books = response.json()

        if not books:
            st.info("No books available.")
        else:
            cols = st.columns(3)

            for i, book in enumerate(books):
                with cols[i % 3]:
                    status_class = "available" if book["is_available"] else "unavailable"
                    status_text = "Available" if book["is_available"] else "Not Available"

                    st.markdown(f"""
                    <div class="card">
                        <h3>📘 {book['title']}</h3>
                        <p style="color:black;"><b>Author:</b> {book['author']}</p>
                        <p style="color:black;"><b>ISBN:</b> {book['isbn']}</p>
                        <span class="badge {status_class}">{status_text}</span>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        st.error("Failed to fetch books")
except requests.exceptions.RequestException:
    st.error("Unable to connect to backend server")
