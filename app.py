import streamlit as st
from datetime import datetime, timedelta
import sqlite3

# ---------------- DATABASE ----------------
def connect():
    return sqlite3.connect("gym.db")


def create_table():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            join_date TEXT,
            fee_paid INTEGER,
            payment_mode TEXT,
            expiry_date TEXT
        )
        """)
        conn.commit()


def add_member(name, phone, fee, mode, days):
    join_date = datetime.now().date()
    expiry = join_date + timedelta(days=days)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO members VALUES (NULL,?,?,?,?,?,?)
        """, (name, phone, str(join_date), fee, mode, str(expiry)))
        conn.commit()

    return expiry


def get_members():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members")
        return cur.fetchall()


def delete_member(member_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM members WHERE id=?", (member_id,))
        conn.commit()


# ---------------- UI ----------------
create_table()

st.title("🏋️ Gym Management System")

menu = st.sidebar.selectbox("Menu", ["Add Member", "View Members", "Delete Member"])

# ---------------- ADD MEMBER ----------------
if menu == "Add Member":
    st.subheader("➕ Add Member")

    name = st.text_input("Name")
    phone = st.text_input("Phone")
    fee = st.number_input("Fee Paid", min_value=0)
    payment_mode = st.selectbox("Payment Mode", ["Cash", "Online"])
    days = st.number_input("Membership Days", min_value=1)

    if st.button("Add Member"):
        expiry = add_member(name, phone, fee, payment_mode, days)
        st.success(f"Member Added! Expiry Date: {expiry}")


# ---------------- VIEW MEMBERS ----------------
elif menu == "View Members":
    st.subheader("📋 All Members")

    data = get_members()

    if len(data) == 0:
        st.warning("No members found")
    else:
        for m in data:
            st.write(f"""
            **ID:** {m[0]}  
            **Name:** {m[1]}  
            **Phone:** {m[2]}  
            **Fee:** {m[4]}  
            **Payment:** {m[5]}  
            **Expiry:** {m[6]}  
            ---
            """)


# ---------------- DELETE MEMBER ----------------
elif menu == "Delete Member":
    st.subheader("🗑️ Delete Member")

    member_id = st.number_input("Enter Member ID", min_value=1)

    if st.button("Delete"):
        delete_member(member_id)
        st.success("Member deleted successfully")