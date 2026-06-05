from database import create_tables
from services import (
    add_member,
    get_members,
    search_member,
    delete_member,
    get_expiring_soon
)
from utils import print_header, print_member


# ---------------- MENU ----------------
def menu():
    print_header("🏋️ GYM MANAGEMENT SYSTEM")
    print("1. Add Member")
    print("2. View Members")
    print("3. Search Member")
    print("4. Delete Member")
    print("5. Exit")
    print("6. ⚠️ Expiry Alert (2 Days)")


# ---------------- ADD MEMBER ----------------
def add_ui():
    print_header("ADD MEMBER")

    name = input("Name: ")
    phone = input("Phone: ")

    # safe fee input
    while True:
        fee_input = input("Fee Paid: ")
        if fee_input.isdigit():
            fee = int(fee_input)
            break
        else:
            print("❌ Enter numbers only (example: 1000)")

    payment_mode = input("Payment (Cash/Online): ")

    while True:
        days_input = input("Membership days: ")
        if days_input.isdigit():
            days = int(days_input)
            break
        else:
            print("❌ Enter valid number of days")

    expiry = add_member(name, phone, fee, payment_mode, days)

    print(f"\n✅ Member added!")
    print(f"📅 Expiry: {expiry}")


# ---------------- VIEW MEMBERS ----------------
def view_ui():
    print_header("ALL MEMBERS")

    data = get_members()

    if not data:
        print("⚠️ No members found")
        return

    for m in data:
        print_member(m)


# ---------------- SEARCH MEMBER ----------------
def search_ui():
    print_header("SEARCH MEMBER")

    name = input("Enter name: ")
    results = search_member(name)

    if not results:
        print("❌ No match found")
        return

    for m in results:
        print_member(m)


# ---------------- DELETE MEMBER ----------------
def delete_ui():
    print_header("DELETE MEMBER")

    member_id_input = input("Enter Member ID: ")

    if member_id_input.isdigit():
        delete_member(int(member_id_input))
        print("🗑️ Member deleted successfully")
    else:
        print("❌ Invalid ID")


# ---------------- EXPIRY ALERT ----------------
def expiry_alert_ui():
    print_header("⚠️ EXPIRING IN NEXT 2 DAYS")

    members = get_expiring_soon(2)

    if not members:
        print("🎉 No members expiring soon")
        return

    for m in members:
        print_member(m)


# ---------------- MAIN LOOP ----------------
def run():
    create_tables()

    while True:
        menu()
        choice = input("\nEnter choice: ")

        if choice == "1":
            add_ui()

        elif choice == "2":
            view_ui()

        elif choice == "3":
            search_ui()

        elif choice == "4":
            delete_ui()

        elif choice == "5":
            print("👋 Exiting...")
            break

        elif choice == "6":
            expiry_alert_ui()

        else:
            print("❌ Invalid choice")


# ---------------- START PROGRAM ----------------
if __name__ == "__main__":
    run()