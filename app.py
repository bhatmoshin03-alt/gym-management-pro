import streamlit as st
from datetime import datetime, timedelta
import sqlite3
from reportlab.pdfgen import canvas
import streamlit as st


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

        cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            member_name TEXT,
            attendance_date TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """)

        cur.execute("""
        INSERT OR IGNORE INTO admin
        VALUES ('admin', 'Gym@2026')
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


def search_member(name):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM members WHERE name LIKE ?",
            ('%' + name + '%',)
        )

        return cur.fetchall()
def get_member_by_id(member_id):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM members WHERE id=?",
            (member_id,)
        )

        return cur.fetchone()


def update_member(member_id, name, phone, fee):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute("""
        UPDATE members
        SET name=?, phone=?, fee_paid=?
        WHERE id=?
        """,
        (
            name,
            phone,
            fee,
            member_id
        ))

        conn.commit()
def delete_member(member_id):
    with connect() as conn:
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM members WHERE id=?",
            (member_id,)
        )

        conn.commit()


def delete_all_members():
    with connect() as conn:
        cur = conn.cursor()

        cur.execute("DELETE FROM members")

        conn.commit()

        conn.commit()
def get_admin():

    with connect() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT username, password FROM admin LIMIT 1"
        )

        return cur.fetchone()


def change_password(new_password):

    with connect() as conn:
        cur = conn.cursor()

        cur.execute(
            "UPDATE admin SET password=? WHERE username='admin'",
            (new_password,)
        )

        conn.commit()

def mark_attendance(member_id, member_name):

    today = datetime.now().date()

    with connect() as conn:
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO attendance
        VALUES(NULL,?,?,?)
        """,
        (
            member_id,
            member_name,
            str(today)
        ))

        conn.commit()

def get_attendance():

    with connect() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM attendance ORDER BY id DESC"
        )

        return cur.fetchall()


def generate_receipt(name, phone, fee, payment_mode, expiry):

    filename = f"receipt_{name}.pdf"

    pdf = canvas.Canvas(filename)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "XCross Fitness Gym")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 740, f"Member Name: {name}")
    pdf.drawString(50, 710, f"Phone Number: {phone}")
    pdf.drawString(50, 680, f"Fee Paid: ₹{fee}")
    pdf.drawString(50, 650, f"Payment Mode: {payment_mode}")
    pdf.drawString(50, 620, f"Membership Expiry: {expiry}")

    pdf.drawString(50, 560, "Thank You For Joining Our Gym!")

    pdf.save()

    return filename

# ---------------- PAGE CONFIG ----------------

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Gym@2026"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔒 Gym Management Pro Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        admin = get_admin()

        if username == admin[0] and password == admin[1]:
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.stop()


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
        "Search Member",
        "Edit Member",
        "Mark Attendance",
        "View Attendance",
        "Delete Member",
        "Change Password"

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

            receipt_file = generate_receipt(
                name,
                phone,
                fee,
                payment_mode,
                expiry
            )

            st.success(
                f"Member Added Successfully! Expiry Date: {expiry}"
            )

            with open(receipt_file, "rb") as file:

                st.download_button(
                    label="📄 Download Receipt",
                    data=file,
                    file_name=receipt_file,
                    mime="application/pdf"
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

# ---------------- SEARCH MEMBER ----------------

elif menu == "Search Member":

    st.subheader("🔍 Search Member")

    search_name = st.text_input("Enter Member Name")

    if st.button("Search"):

        results = search_member(search_name)

        if len(results) == 0:

            st.warning("No member found")

        else:

            for m in results:

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
# ---------------- VIEW ATTENDANCE ----------------

elif menu == "View Attendance":

    st.subheader("📋 Attendance Records")

    records = get_attendance()

    if len(records) == 0:

        st.warning("No attendance records found")

    else:

        for r in records:

            st.markdown(f"""
            ---
            **Attendance ID:** {r[0]}

            **Member ID:** {r[1]}

            **Member Name:** {r[2]}

            **Date:** {r[3]}
            """)

# ---------------- MARK ATTENDANCE ----------------

elif menu == "Mark Attendance":

    st.subheader("📅 Mark Attendance")

    member_id = st.number_input(
        "Enter Member ID",
        min_value=1,
        step=1
    )

    if st.button("Load Member"):

        member = get_member_by_id(member_id)

        if member:

            st.session_state["attendance_member"] = member

        else:

            st.error("Member not found")

    if "attendance_member" in st.session_state:

        member = st.session_state["attendance_member"]

        st.success(f"Member: {member[1]}")

        if st.button("✅ Mark Present"):

            mark_attendance(
                member[0],
                member[1]
            )

            st.success("Attendance Marked Successfully!")
# ---------------- EDIT MEMBER ----------------

elif menu == "Edit Member":

    st.subheader("✏️ Edit Member")

    member_id = st.number_input(
        "Enter Member ID",
        min_value=1,
        step=1
    )

    if st.button("Load Member"):

        member = get_member_by_id(member_id)

        if member:

            st.session_state["member"] = member

        else:

            st.error("Member not found")

    if "member" in st.session_state:

        member = st.session_state["member"]

        new_name = st.text_input(
            "Member Name",
            value=member[1]
        )

        new_phone = st.text_input(
            "Phone Number",
            value=member[2]
        )

        new_fee = st.number_input(
            "Fee Paid",
            value=int(member[4])
        )

        if st.button("Update Member"):

            update_member(
                member[0],
                new_name,
                new_phone,
                new_fee
            )

            st.success(
                "Member updated successfully!"
            )
    if st.button("❌ Delete Member"):

        delete_member(member_id)

        st.success(
            "Member deleted successfully"
        )
# ================= DANGER ZONE =================

st.subheader("⚠️ Danger Zone")

if st.checkbox("Confirm Delete All Members"):
    if st.button("🗑️ Delete All Members Permanently"):
        delete_all_members()
        st.success("All members deleted successfully!")
        st.rerun()
        # ---------------- CHANGE PASSWORD ----------------

elif menu == "Change Password":

    st.subheader("🔒 Change Password")

    current_password = st.text_input(
        "Current Password",
        type="password"
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password"
    )

    if st.button("Update Password"):

        admin = get_admin()

        if current_password != admin[1]:

            st.error("Current Password Incorrect")

        elif len(new_password) < 8:

            st.error(
                "Password must be at least 8 characters"
            )

        elif new_password != confirm_password:

            st.error(
                "Passwords do not match"
            )

        else:

            change_password(new_password)

            st.success(
                "Password Updated Successfully!"
            )

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
<div class='footer'>

© 2026 Gym Management Pro

Developed by <b>Bhat Moshin Mushtaq</b> 🚀

</div>
""", unsafe_allow_html=True)