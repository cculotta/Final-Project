from Friend import Friend
from Birthday import Birthday

# File used by the app to persist data between runs
DB_FILE = "friends_database.csv"

# ----------------------------
# Load / Save helpers (simple)
# ----------------------------

def load_database(path: str) -> list[Friend]:
    friends: list[Friend] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("first_name"):
                    continue  # skip header/blank lines
                friends.append(Friend.from_csv_line(line))
    except FileNotFoundError:
        # first run: no file yet is fine
        pass
    return friends

def save_database(path: str, friends: list[Friend]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("first_name,last_name,email,phone,street,city,state,zip,month,day\n")
        for fr in friends:
            f.write(fr.to_csv_line() + "\n")

# ------------
# Main menu UI
# ------------
def main_menu():
    friends = load_database(DB_FILE)
    while True:
        print("\nFriends Manager")
        print("1 - Create new friend (or bulk-load from CSV)")
        print("2 - Search for a friend")
        print("3 - Reports")
        print("4 - Exit")
        choice = input("> ").strip()

        if choice == "1":
            handle_create(friends)
        elif choice == "2":
            handle_search(friends)
        elif choice == "3":
            handle_reports(friends)
        elif choice == "4":
            save_database(DB_FILE, friends)
            print("Saved. Bye!")
            return
        else:
            print("Invalid option.")

# ------------
# Create flow
# ------------
def handle_create(friends: list[Friend]):
    print("\n1) Add a single friend  2) Bulk-load from CSV  9) Back")
    ch = input("> ").strip()
    if ch == "1":
        friends.append(prompt_new_friend())
        print("Added.")
    elif ch == "2":
        path = input("CSV path to import: ").strip()
        imported = load_database(path)
        friends.extend(imported)
        print(f"Imported {len(imported)} record(s).")
    # else back

def prompt_new_friend() -> Friend:
    fn = input("First name: ").strip()
    ln = input("Last name: ").strip()
    fr = Friend(fn, ln)

    # optional fields (press Enter to skip)
    fr.email_address = (input("Email (optional): ").strip() or None)
    fr.phone = (input("Phone (optional): ").strip() or None)
    fr.street_address = (input("Street (optional): ").strip() or None)
    fr.city = (input("City (optional): ").strip() or None)
    fr.state = (input("State (optional): ").strip() or None)
    fr.zip = (input("ZIP (optional): ").strip() or None)

    m = input("Birth month 1-12 (Enter to skip): ").strip()
    d = input("Birth day   1-31 (Enter to skip): ").strip()
    if m and d:
        try:
            fr.birthday = Birthday(int(m), int(d))
        except:
            print("Invalid birthday, leaving blank.")
    return fr

# ------------
# Search flow
# ------------
def handle_search(friends: list[Friend]):
    qf = input("First name starts with (Enter to skip): ").strip().lower()
    ql = input("Last  name starts with (Enter to skip): ").strip().lower()

    matches = []
    for i, fr in enumerate(friends):
        okf = (not qf) or fr.first_name.lower().startswith(qf)
        okl = (not ql) or fr.last_name.lower().startswith(ql)
        if okf and okl:
            matches.append((i, fr))

    if not matches:
        print("No matches.")
        return

    for n, (i, fr) in enumerate(matches, start=1):
        print(f"{n}) {fr.full_name()} | {fr.email_address or ''} | {fr.phone or ''}")

    s = input("Select # to open (Enter to cancel): ").strip()
    if not s.isdigit():
        return
    k = int(s) - 1
    if not (0 <= k < len(matches)):
        return

    i, fr = matches[k]
    print(f"\nSelected: {fr.full_name()}")
    print("1) Edit  2) Delete  9) Back")
    a = input("> ").strip()
    if a == "1":
        edit_friend(fr)
        print("Updated.")
    elif a == "2":
        confirm = input("Type DELETE to confirm: ").strip()
        if confirm == "DELETE":
            friends.pop(i)
            print("Deleted.")

def edit_friend(fr: Friend):
    def upd(label, cur):
        val = input(f"{label} [{cur or ''}]: ").strip()
        return val if val else cur

    fr.first_name = upd("First name", fr.first_name)
    fr.last_name  = upd("Last name", fr.last_name)
    fr.email_address = upd("Email", fr.email_address)
    fr.phone = upd("Phone", fr.phone)
    fr.street_address = upd("Street", fr.street_address)
    fr.city = upd("City", fr.city)
    fr.state = upd("State", fr.state)
    fr.zip = upd("ZIP", fr.zip)

    m = input(f"Birth month [{fr.birthday.get_month() if fr.birthday else ''}]: ").strip()
    d = input(f"Birth day   [{fr.birthday.get_day() if fr.birthday else ''}]: ").strip()
    if m and d:
        try:
            fr.birthday = Birthday(int(m), int(d))
        except:
            print("Invalid date; keeping old birthday.")

# ----------
# Reports
# ----------
def handle_reports(friends: list[Friend]):
    while True:
        print("\nReports")
        print("3.1 - List of friends alphabetically")
        print("3.2 - List of friends by upcoming birthdays")
        print("3.3 - Mailing labels for friends")
        print("3.9 - Return")
        ch = input("> ").strip()

        if ch == "3.1":
            # sort case-insensitively by last, then first
            for fr in sorted(friends, key=lambda f: (f.last_name.lower(), f.first_name.lower())):
                print(f"{fr.last_name}, {fr.first_name} | {fr.email_address or ''} | {fr.phone or ''}")

        elif ch == "3.2":
            # keep unknown birthdays at bottom by using a large sentinel
            def days(fr):
                return fr.birthday.days_until() if fr.birthday else 9999
            for fr in sorted(friends, key=days):
                tag = f"(in {days(fr)} days)" if fr.birthday else "(birthday unknown)"
                print(f"{fr.full_name()} {tag}")

        elif ch == "3.3":
            # basic mailing label format
            for fr in friends:
                print(fr.full_name())
                print(fr.street_address or "")
                city_state = ", ".join(x for x in [fr.city or "", fr.state or ""] if x)
                print(f"{city_state} {fr.zip or ''}".strip())
                print("-" * 30)
        else:
            return


if __name__ == "__main__":
    main_menu()
