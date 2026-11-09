import sqlite3
import os

DB_FILE = "employees.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_employee():
    conn = get_connection()
    cursor = conn.cursor()
    
    emp_id_input = input("Enter Employee ID (integer): ").strip()
    if not emp_id_input.isdigit():
        print("❌ Error: ID must be numeric.")
        conn.close()
        return
    emp_id = int(emp_id_input)

    name = input("Enter Full Name: ").strip()
    email = input("Enter Email: ").strip()
    department = input("Enter Department: ").strip()
    
    salary_input = input("Enter Monthly Salary: ").strip()
    try:
        salary = float(salary_input)
    except ValueError:
        print("❌ Error: Salary must be a valid number.")
        conn.close()
        return

    try:
        cursor.execute("INSERT INTO employees (emp_id, name, email, department, salary) VALUES (?, ?, ?, ?, ?)",
                       (emp_id, name, email, department, salary))
        conn.commit()
        print(f"✅ Employee '{name}' added successfully!")
    except sqlite3.IntegrityError:
        print("❌ Error: Employee ID or Email already exists in database.")
    finally:
        conn.close()

def view_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("📂 No employee records found.")
        return

    print("\n" + "=" * 92)
    print(f"{'ID':<6} | {'Name':<18} | {'Email':<28} | {'Department':<16} | {'Salary':<10}")
    print("-" * 92)
    for r in rows:
        print(f"{r[0]:<6} | {r[1]:<18} | {r[2]:<28} | {r[3]:<16} | ₹{r[4]:<9,.2f}")
    print("=" * 92)

def search_employee():
    emp_id = input("Enter Employee ID to search: ").strip()
    if not emp_id.isdigit():
        print("❌ Error: ID must be numeric.")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (int(emp_id),))
    r = cursor.fetchone()
    conn.close()

    if r:
        print("\n🔍 Employee Found:")
        print(f"   ID         : {r[0]}")
        print(f"   Name       : {r[1]}")
        print(f"   Email      : {r[2]}")
        print(f"   Department : {r[3]}")
        print(f"   Salary     : ₹{r[4]:,.2f}")
    else:
        print(f"❌ No employee found with ID {emp_id}.")

def update_employee():
    emp_id = input("Enter Employee ID to update: ").strip()
    if not emp_id.isdigit():
        print("❌ Error: ID must be numeric.")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (int(emp_id),))
    r = cursor.fetchone()
    if not r:
        print(f"❌ Employee ID {emp_id} not found.")
        conn.close()
        return

    print(f"Updating Employee: {r[1]}. Press Enter to keep current value.")
    name = input(f"New Name [{r[1]}]: ").strip() or r[1]
    email = input(f"New Email [{r[2]}]: ").strip() or r[2]
    department = input(f"New Department [{r[3]}]: ").strip() or r[3]
    sal_str = input(f"New Salary [{r[4]}]: ").strip()
    salary = float(sal_str) if sal_str else r[4]

    try:
        cursor.execute("UPDATE employees SET name=?, email=?, department=?, salary=? WHERE emp_id=?",
                       (name, email, department, salary, int(emp_id)))
        conn.commit()
        print("✅ Employee record updated successfully!")
    except sqlite3.IntegrityError:
        print("❌ Error: Email already in use by another employee.")
    finally:
        conn.close()

def delete_employee():
    emp_id = input("Enter Employee ID to delete: ").strip()
    if not emp_id.isdigit():
        print("❌ Error: ID must be numeric.")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE emp_id = ?", (int(emp_id),))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"✅ Employee ID {emp_id} deleted successfully!")
    else:
        print(f"❌ Employee ID {emp_id} not found.")
    conn.close()

def main():
    initialize_db()
    while True:
        print("\n==========================================")
        print("   EMPLOYEE MANAGEMENT SYSTEM (SQLITE)    ")
        print("==========================================")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")
        print("------------------------------------------")

        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1": add_employee()
        elif choice == "2": view_employees()
        elif choice == "3": search_employee()
        elif choice == "4": update_employee()
        elif choice == "5": delete_employee()
        elif choice == "6":
            print("Exiting Employee Management System. Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
