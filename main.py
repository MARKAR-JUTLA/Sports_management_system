# Importing neccesary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class SchoolManagementSystem:
    def __init__(self, filename="students_data.csv"):
        self.filename = filename
        # Check if the CSV file exists, if not, create one with headers
        if not os.path.exists(self.filename):
            data = pd.DataFrame(columns=["Student Name", "Class", "Section", "Roll No", "Grade"])
            data.to_csv(self.filename, index=False)
        # Load data from CSV into a pandas DataFrame
        self.data = pd.read_csv(self.filename)

    def save_data(self):
        """Save DataFrame to CSV."""
        self.data.to_csv(self.filename, index=False)

    def add_student(self):
        """Add a new student to the system."""
        print("\n=== Add New Student ===")
        name = input("Enter Student Name: ")
        _class = input("Enter Class: ")
        section = input("Enter Section: ")
        try:
            roll_no = int(input("Enter Roll No: "))
        except ValueError:
            print("Invalid Roll No! Roll No must be an integer.")
            return
        grade = input("Enter Grade (e.g., A+, A, B+, etc.): ")
        new_student = pd.DataFrame({"Student Name": [name], "Class": [_class], "Section": [section], "Roll No": [roll_no], "Grade": [grade]})
        self.data = pd.concat([self.data, new_student], ignore_index=True)
        self.save_data()
        print(f"Student '{name}' added successfully!")

    def view_students(self):
        """View all students in the system."""
        print("\n=== View All Students ===")
        if self.data.empty:
            print("No students found in the system.")
        else:
            print(self.data.to_string(index=False))

    def update_student(self):
        """Update details of an existing student."""
        print("\n=== Update Student Details ===")
        name = input("Enter Student Name to Update: ")
        student_index = self.data[self.data["Student Name"] == name].index
        if student_index.empty:
            print(f"Student '{name}' not found!")
            return
        print("Enter new details (leave blank to keep current value):")
        new_class = input(f"New Class (Current: {self.data.loc[student_index[0], 'Class']}): ")
        new_section = input(f"New Section (Current: {self.data.loc[student_index[0], 'Section']}): ")
        try:
            new_roll_no = input(f"New Roll No (Current: {self.data.loc[student_index[0], 'Roll No']}): ")
            new_roll_no = int(new_roll_no) if new_roll_no else self.data.loc[student_index[0], 'Roll No']
        except ValueError:
            print("Invalid Roll No!")
            return
        new_grade = input(f"New Grade (Current: {self.data.loc[student_index[0], 'Grade']}): ")
        # Apply updates
        if new_class:
            self.data.loc[student_index[0], "Class"] = new_class
        if new_section:
            self.data.loc[student_index[0], "Section"] = new_section
        self.data.loc[student_index[0], "Roll No"] = new_roll_no
        if new_grade:
            self.data.loc[student_index[0], "Grade"] = new_grade
        self.save_data()
        print(f"Student '{name}' updated successfully!")

    def delete_student(self):
        """Delete a student from the system."""
        print("\n=== Delete Student ===")
        name = input("Enter Student Name to Delete: ")
        student_index = self.data[self.data["Student Name"] == name].index
        if student_index.empty:
            print(f"Student '{name}' not found!")
        else:
            self.data = self.data.drop(index=student_index).reset_index(drop=True)
            self.save_data()
            print(f"Student '{name}' deleted successfully!")

    def analyze_data(self):
        """Analyze student performance."""
        print("\n=== Analyze Data ===")
        if self.data.empty:
            print("No data available for analysis.")
            return

        # Example: Find average grade per class
        class_analysis = self.data.groupby("Class")["Grade"].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else "No Data") 
        print("\n=== Most Frequent Grade per Class ===")
        print(class_analysis.to_string())

    def visualize_data(self):
        """Visualize student data (e.g., grade distribution)."""
        print("\n=== Visualize Data ===")
        if self.data.empty:
            print("No data available for visualization.")
            return

        # Example: Create a bar chart of student counts per class
        plt.figure(figsize=(8, 6))
        sns.countplot(x="Class", data=self.data, palette="viridis")
        plt.title("Number of Students per Class")
        plt.xlabel("Class")
        plt.ylabel("Number of Students")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("student_counts_per_class.png")  # Save the plot
        plt.show()

        # Example: Create a pie chart of student distribution across sections
        plt.figure(figsize=(6, 6))
        plt.pie(self.data["Section"].value_counts(), labels=self.data["Section"].unique(), autopct="%1.1f%%", startangle=90)
        plt.title("Student Distribution Across Sections")
        plt.savefig("student_distribution_by_section.png")  # Save the plot
        plt.show()

    def menu(self):
        """Display the main menu and handle user input."""
        while True:
            print("\n=== School Management System ===")
            print("1. Add Student")
            print("2. View Students")
            print("3. Update Student")
            print("4. Delete Student")
            print("5. Analyze Data")
            print("6. Visualize Data")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.update_student()
            elif choice == "4":
                self.delete_student()
            elif choice == "5":
                self.analyze_data()
            elif choice == "6":
                self.visualize_data()
            elif choice == "7":
                print("Exiting School Management System. Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    system = SchoolManagementSystem()
    system.menu()