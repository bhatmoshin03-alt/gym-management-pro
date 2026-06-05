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
        INSERT INTO members VALUES
        (NULL,?,?,?,?,?,?)
        """,
        (
            name,
            phone,
            str(join_date),
            fee,
            mode,
            str(expiry)
        ))

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

        cur.execute(
            "DELETE FROM members WHERE id=?",
            (member_id,)
        )

        conn.commit()


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Gym Management Pro",
    page_icon="🏋️",
    layout="wide"
)

create_table()

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

.footer {
    text-align:center;
    color:gray;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div style='text-align:center'>
    <h1>🏋️ Gym Management Pro</h1>
    <h3>Developed by Bhat Moshin Mushtaq 👨‍💻</h3>
</div>
""", unsafe_allow_html=True)

st.success("💪 Welcome to Gym Management Pro")

# ---------------- SIDEBAR ----------------

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/1048/1048953.png",
    width=120
)

st.sidebar.markdown("## 👨‍💻 Developer")

st.sidebar.info("""
Bhat Moshin Mushtaq

Python Developer 🚀
""")

menu = st.sidebar.selectbox(
    "📌 Select Option",
    [
        "Dashboard",
        "Add Member",
        "View Members",
        "Delete Member"
    ]
)

# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    members = get_members()

    total_members = len(members)

    total_revenue = 0

    for member in members:
        total_revenue += member[4]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "👥 Total Members",
            total_members
        )

    with col2:
        st.metric(
            "💰 Total Revenue",
            f"₹{total_revenue}"
        )

    st.info(
        "Professional Gym Management System built using Python, SQLite and Streamlit."
    )

# ---------------- ADD MEMBER ----------------

elif menu == "Add Member":

    st.subheader("➕ Add New Member")

    name = st.text_input("Member Name")

    phone = st.text_input("Phone Number")

    fee = st.number_input(
        "Fee Paid",
        min_value=0
    )

    payment_mode = st.selectbox(
        "Payment Mode",
        ["Cash", "Online"]
    )

    days = st.number_input(
        "Membership Days",
        min_value=1
    )

    if st.button("✅ Add Member"):

        if name == "":
            st.error("Please enter member name")

        else:

            expiry = add_member(
                name,
                phone,
                fee,
                payment_mode,
                days
            )

            st.success(
                f"Member Added Successfully! Expiry Date: {expiry}"
            )

# ---------------- VIEW MEMBERS ----------------

elif menu == "View Members":

    st.subheader("📋 All Members")

    data = get_members()

    if len(data) == 0:

        st.warning("No members found")

    else:

        for m in data:

            st.markdown(f"""
            ---
            ### 👤 {m[1]}

            **ID:** {m[0]}

            **Phone:** {m[2]}

            **Join Date:** {m[3]}

            **Fee Paid:** ₹{m[4]}

            **Payment Mode:** {m[5]}

            **Expiry Date:** {m[6]}
            """)

# ---------------- DELETE MEMBER ----------------

elif menu == "Delete Member":

    st.subheader("🗑️ Delete Member")

    member_id = st.number_input(
        "Enter Member ID",
        min_value=1
    )

    if st.button("❌ Delete Member"):

        delete_member(member_id)

        st.success(
            "Member deleted successfully"
        )

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
<div class='footer'>

© 2026 Gym Management Pro

Developed by <b>Bhat Moshin Mushtaq</b> 🚀

</div>
""", unsafe_allow_html=True)