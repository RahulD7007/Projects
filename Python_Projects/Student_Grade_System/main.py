# Initialising dictionary 
Student_grades = {}

# Add a new student 
def add_student(name, grade):
    Student_grades[name] = grade
    print(f"Added {name} with a grade of {grade}")

# Update a student 
def update_student(name, grade):
    if name in Student_grades:
        Student_grades[name] = grade
        print(f"{name}'s marks have been updated to {grade}")
    else:
        print(f"{name} not found!")

# Delete a student 
def delete_student(name):
    if name in Student_grades:
        del Student_grades[name]
        print(f"{name} has been successfully deleted")
    else:
        print(f"{name} not found!")

# View All Students
def display_all_students():
    if Student_grades:
        print("Student List:")
        for name, grade in Student_grades.items():
            print(f"{name}: {grade}")
    else:
        print("No students found!")

# Main function
def main():
    while True:
        print('\nStudent Grades Management System')
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. View Students")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                name = input("Enter student name: ")
                grade = int(input("Enter student grade: "))
                add_student(name, grade)
            elif choice == 2:
                name = input("Enter student name: ")
                grade = int(input("Enter student grade: "))
                update_student(name, grade)
            elif choice == 3:
                name = input("Enter student name: ")
                delete_student(name)
            elif choice == 4:
                display_all_students()
            elif choice == 5:
                print("Closing the program... Goodbye!")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

# Run the main function
if __name__ == "__main__":
    main()