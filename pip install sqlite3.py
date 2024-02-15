import sqlite3

# Connect to the SQLite database (or create it if not exists)
conn = sqlite3.connect('family_tree.db')
cursor = conn.cursor()

# Create a table to store family members
cursor.execute('''
    CREATE TABLE IF NOT EXISTS family_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birthdate TEXT,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES family_members(id)
    )
''')
conn.commit()

def add_family_member():
    name = input("Enter the name of the family member: ")
    birthdate = input("Enter the birthdate (optional, press Enter to skip): ")
    parent_id = input("Enter the parent's ID (optional, press Enter to skip): ")

    # Insert the family member data into the database
    cursor.execute('''
        INSERT INTO family_members (name, birthdate, parent_id) VALUES (?, ?, ?)
    ''', (name, birthdate, parent_id))

    conn.commit()
    print("Family member added successfully!")

def display_family_tree(member_id, level=0):
    cursor.execute('SELECT * FROM family_members WHERE id = ?', (member_id,))
    member = cursor.fetchone()

    if member:
        print('  ' * level + f"ID: {member[0]}, Name: {member[1]}, Birthdate: {member[2]}, Parent ID: {member[3]}")

        # Display descendants
        cursor.execute('SELECT * FROM family_members WHERE parent_id = ?', (member_id,))
        descendants = cursor.fetchall()
        for descendant in descendants:
            display_family_tree(descendant[0], level + 1)
    else:
        print("Family member not found.")

def search_by_name():
    search_name = input("Enter the name to search for: ")
    cursor.execute('SELECT * FROM family_members WHERE name LIKE ?', ('%' + search_name + '%',))
    results = cursor.fetchall()

    if results:
        print("Search results:")
        for result in results:
            print(f"ID: {result[0]}, Name: {result[1]}, Birthdate: {result[2]}, Parent ID: {result[3]}")
    else:
        print("No results found for the given name.")

def delete_family_member():
    member_id = int(input("Enter the ID of the family member to delete: "))
    cursor.execute('DELETE FROM family_members WHERE id = ?', (member_id,))
    conn.commit()
    print("Family member deleted successfully!")

# Main loop
while True:
    print("\n1. Add Family Member")
    print("2. Display Family Tree")
    print("3. Search by Name")
    print("4. Delete Family Member")
    print("5. Exit")

    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == '1':
        add_family_member()
    elif choice == '2':
        member_id = int(input("Enter the ID of the family member to display the tree for: "))
        display_family_tree(member_id)
    elif choice == '3':
        search_by_name()
    elif choice == '4':
        delete_family_member()
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

# Close the database connection
conn.close()