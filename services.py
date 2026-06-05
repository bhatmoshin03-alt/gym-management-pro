from database import connect
from datetime import datetime, timedelta


# ➤ ADD MEMBER
def add_member(name, phone, fee_paid, payment_mode, days):
    join_date = datetime.now().date()
    expiry_date = join_date + timedelta(days=days)

    with connect() as conn:
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO members
        (name, phone, join_date, fee_paid, payment_mode, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            str(join_date),
            fee_paid,
            payment_mode,
            str(expiry_date)
        ))

        conn.commit()

    return expiry_date


# ➤ GET ALL MEMBERS
def get_members():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members")
        return cur.fetchall()


# ➤ SEARCH MEMBER
def search_member(name):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members WHERE name LIKE ?", ('%' + name + '%',))
        return cur.fetchall()


# ➤ DELETE MEMBER
def delete_member(member_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM members WHERE id = ?", (member_id,))
        conn.commit()
from datetime import datetime, timedelta


def get_expiring_soon(days_before=2):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members")
        members = cur.fetchall()

    today = datetime.now().date()
    alert_list = []

    for m in members:
        expiry_date = datetime.strptime(m[6], "%Y-%m-%d").date()

        if today <= expiry_date <= today + timedelta(days=days_before):
            alert_list.append(m)

    return alert_list