'''expense tracker'''
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yamu",
    database="expense_db"
)

cursor = conn.cursor()

while True:
    print("\n1. Add Expense")
    print("2. View All Expenses")
    print("3. Delete Expense")
    print("4. Search by Category")
    print("5. Show Total Expense")
    print("6. Category wise Total")
    print("7. Update Expense")
    print("8. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        title = input("Enter title: ")
        amount = int(input("Enter amount: "))
        category = input("Enter category: ")
        date = input("Enter date (YYYY-MM-DD): ")

        cursor.execute(
            "INSERT INTO expenses (title, amount, category, date) VALUES (%s, %s, %s, %s)",
            (title, amount, category, date)
        )

        conn.commit()
        print("Expense added!")

    elif choice == "2":
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()

        print("\nAll Expenses:")
        print("\n{:<5} {:<30} {:<10} {:<20} {:<12}".format("ID", "Title", "Amount", "Category", "Date"))
        print("-" * 80)

        for row in data:
            print("{:<5} {:<30} {:<10} {:<20} {:<12}".format(row[0], row[1], row[2], row[3], str(row[4])))

    elif choice == "3":
        id = int(input("Enter ID to delete: "))
        cursor.execute("DELETE FROM expenses WHERE id = %s", (id,))
        conn.commit()
        print("Deleted!")

    elif choice == "4":
        cursor.execute("SELECT DISTINCT category FROM expenses")
        categories = cursor.fetchall()
        print("\nAvailable Categories:")
        i = 1
        for cat in categories:
            print(i, ".", cat[0])
            i += 1
        choice_cat = int(input("Select category number: "))
        selected_category = categories[choice_cat - 1][0]

        cursor.execute("SELECT * FROM expenses WHERE category = %s", (selected_category,))
        data = cursor.fetchall()
        print("\nExpenses in", selected_category)
        print("\n{:<5} {:<30} {:<10} {:<20} {:<12}".format("ID", "Title", "Amount", "Category", "Date"))
        print("-" * 80)

        for row in data:
            print("{:<5} {:<30} {:<10} {:<20} {:<12}".format(row[0], row[1], row[2], row[3], str(row[4])))

    elif choice == "5":
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()

        print("Total Expense:", total[0])

    elif choice == "6":
        category = input("Enter category: ")
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = %s", (category,))
        total = cursor.fetchone()

        if total[0] is None:
            print("No expenses in this category")

        else:
            print("Total for", category, "=", total[0])

    elif choice == "7":
        id = int(input("Enter ID to update: "))
        new_amount = int(input("Enter new amount: "))
        cursor.execute("UPDATE expenses SET amount = %s WHERE id = %s", (new_amount, id))
        conn.commit()
        print("Updated successfully!")

    elif choice == "8":
        print("Exiting...")
        break

    else:
        print("Invalid choice")

conn.close()