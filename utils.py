def print_header(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)


def print_member(m):
    print(f"""
ID: {m[0]}
Name: {m[1]}
Phone: {m[2]}
Join Date: {m[3]}
Fee Paid: {m[4]}
Payment Mode: {m[5]}
Expiry Date: {m[6]}
----------------------------
""")
    