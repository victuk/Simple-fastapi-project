# student_records_manager.py

import json
import os

# File to store student records
DATA_FILE = "students_data.json"

# Load existing data or start fresh
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Display menu
def show_menu():
    print("\n===== STUDENT RECORDS MANAGER =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

# Add student
def add_student(data):
    print("\n--- Add New Student ---")
    
    student_id = input("Enter Student ID: ")

    # Check if ID already exists
    for student in data:
        if student["id"] == student_id:
            print("Student ID already exists!")
            return data

    name = input("Enter Full Name: ")
    department = input("Enter Department: ")
    level = input("Enter Level: ")

    student = {
        "id": student_id,
        "name": name,
        "department": department,
        "level": level
    }

    data.append(student)
    save_data(data)
    print("Student added successfully!")

    return data


# View students (placeholder for next part)
def view_students(data):
    print("\n--- Student List ---")
    if len(data) == 0:
        print("No student records found.")
    else:
        for student in data:
            print(f"{student['id']} | {student['name']} | {student['department']} | {student['level']}")


    # ==============================
# SEARCH STUDENT
# ==============================
def search_student(data):
    print("\n--- Search Student ---")
    keyword = input("Enter Student ID or Name: ").lower()

    found = False

    for student in data:
        if keyword in student["id"].lower() or keyword in student["name"].lower():
            print("\nStudent Found:")
            print(f"ID: {student['id']}")
            print(f"Name: {student['name']}")
            print(f"Department: {student['department']}")
            print(f"Level: {student['level']}")
            found = True

    if not found:
        print("No matching student found.")


# ==============================
# UPDATE STUDENT
# ==============================
def update_student(data):
    print("\n--- Update Student ---")
    student_id = input("Enter Student ID to update: ")

    for student in data:
        if student["id"] == student_id:
            print("\nLeave field blank if you don't want to change it.")

            new_name = input(f"New Name ({student['name']}): ")
            new_department = input(f"New Department ({student['department']}): ")
            new_level = input(f"New Level ({student['level']}): ")

            if new_name.strip() != "":
                student["name"] = new_name
            if new_department.strip() != "":
                student["department"] = new_department
            if new_level.strip() != "":
                student["level"] = new_level

            save_data(data)
            print("Student record updated successfully!")
            return data

    print("Student ID not found.")
    return data


# ==============================
# DELETE STUDENT
# ==============================
def delete_student(data):
    print("\n--- Delete Student ---")
    student_id = input("Enter Student ID to delete: ")

    for student in data:
        if student["id"] == student_id:
            confirm = input(f"Are you sure you want to delete {student['name']}? (yes/no): ")

            if confirm.lower() == "yes":
                data.remove(student)
                save_data(data)
                print("Student deleted successfully!")
                return data
            else:
                print("Delete cancelled.")
                return data

    print("Student ID not found.")
    return data

# Main program loop
def main():
    data = load_data()

    while True:
        show_menu()
        choice = input("\nEnter your choice: ")

        if choice == "1":
            data = add_student(data)
        elif choice == "2":
            view_students(data)
        elif choice == "3":
            search_student(data)
        elif choice == "4":
            update_student(data)
        elif choice == "5":
            delete_student(data)
        elif choice == "6":
            print("Exiting program... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


# ==============================
# EXTRA IMPROVEMENT: COUNT TOTAL STUDENTS
# ==============================
def count_students(data):
    print(f"\nTotal Students: {len(data)}")
    # ==============================
# OPTIONAL: VIEW ALL STUDENTS (IMPROVED)
# ==============================
def view_students(data):
    print("\n--- All Students ---")

    if len(data) == 0:
        print("No student records found.")
        return

    print("\nID | NAME | DEPARTMENT | LEVEL")
    print("--------------------------------------")

    for student in data:
        print(f"{student['id']} | {student['name']} | {student['department']} | {student['level']}")

    count_students(data)


# ==============================
# COUNT STUDENTS (USED ABOVE)
# ==============================
def count_students(data):
    print(f"\nTotal Students: {len(data)}")


# ==============================
# MAIN PROGRAM LOOP (FINAL VERSION)
# ==============================
def main():
    data = load_data()

    while True:
        show_menu()
        choice = input("\nEnter your choice: ")

        if choice == "1":
            data = add_student(data)

        elif choice == "2":
            view_students(data)

        elif choice == "3":
            search_student(data)

        elif choice == "4":
            update_student(data)

        elif choice == "5":
            data = delete_student(data)

        elif choice == "6":
            print("\nExiting Student Records Manager...")
            print("Goodbye 👋")
            break

        else:
            print("Invalid choice. Please try again.")


# ==============================
# PROGRAM START
# ==============================
if __name__ == "__main__":
    main()