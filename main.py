from tkinter import *
from tkinter import ttk
from datetime import datetime
from Employee import Employee
from Agent import Agent
from Trainer import Trainer
from IR import IR

def add_employee():
    global counter
    # Get employee data from entry widgets
    name = name_entry.get()
    baseSalary = float(base_salary_entry.get()) if base_salary_entry.get() else 0.0
    # Additional fields
    birthDate = birth_date_entry.get()
    hireDate = hire_date_entry.get()
   
    # Determine the selected employee type
    selected_type = employee_type.get()

    if selected_type == "Trainer":
        # Get additional information for Trainer
        overtimeRate = float(overtime_rate_entry.get()) if overtime_rate_entry.get() else 0.0
        overtimeHours = int(overtime_hours_entry.get()) if overtime_hours_entry.get() else 0

        # Create an instance of the Trainer class
        new_employee = Trainer(name, birthDate, hireDate, baseSalary, overtimeHours)
    elif selected_type == "Agent":
        # Get additional information for Agent
        responsibilityBonus = float(responsibility_bonus_entry.get()) if responsibility_bonus_entry.get() else 0.0

        # Create an instance of the Agent class
        new_employee = Agent(name, birthDate, hireDate, baseSalary, responsibilityBonus)
    else:
        # Handle other employee types or raise an exception
        raise ValueError("Unsupported employee type")

    # Increment the counter for the new employee
    counter += 1

    # Set the employee number for the new employee
    new_employee.EmployeeNumber = counter

    # Calculate net salary using SalaryToPay instance method
    net_salary = new_employee.SalaryToPay()

    # Insert employee data into Treeview
    tree.insert("", "end", values=(new_employee.EmployeeNumber, new_employee.Name, new_employee.BirthDate,
                                   selected_type, new_employee.HireDate, new_employee.BaseSalary,
                                   new_employee.OvertimeRate if hasattr(new_employee, 'OvertimeRate') else '',
                                   new_employee.OvertimeHours if hasattr(new_employee, 'OvertimeHours') else '',
                                   new_employee.ResponsibilityBonus if hasattr(new_employee, 'ResponsibilityBonus') else '',
                                   net_salary))

    # Save employee data to TXT file
    try:
        with open("employees.txt", "a") as file:
            file.write(f"Employee Number: {new_employee.EmployeeNumber}\n")
            file.write(f"Name: {new_employee.Name}\n")
            file.write(f"Birth Date: {new_employee.BirthDate}\n")
            file.write(f"Type: {selected_type}\n")
            file.write(f"Hire Date: {new_employee.HireDate}\n")
            file.write(f"Base Salary: {new_employee.BaseSalary}\n")
            if hasattr(new_employee, 'OvertimeRate'):
                file.write(f"Overtime Rate: {new_employee.OvertimeRate}\n")
            if hasattr(new_employee, 'OvertimeHours'):
                file.write(f"Overtime Hours: {new_employee.OvertimeHours}\n")
            if hasattr(new_employee, 'ResponsibilityBonus'):
                file.write(f"Responsibility Bonus: {new_employee.ResponsibilityBonus}\n")
            file.write(f"Net Salary: {net_salary}\n")

        # Clear entry widgets after successful addition
        name_entry.delete(0, END)
        base_salary_entry.delete(0, END)
        birth_date_entry.delete(0, END)
        hire_date_entry.delete(0, END)
        overtime_rate_entry.delete(0, END)
        overtime_hours_entry.delete(0, END)
        responsibility_bonus_entry.delete(0, END)

    except FileNotFoundError:
        print("File not found.")


def remove_employee():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
        save_data()

def load_data():
    global counter
    try:
        with open("employees.txt", "r") as file:
            lines = file.readlines()
            data = []
            employee = {}
            for line in lines:
                if line.strip() == "":
                    data.append(employee)
                    employee = {}
                else:
                    key, value = line.strip().split(": ")
                    employee[key] = value

            # Find the highest employee number in the loaded data
            existing_numbers = [int(employee.get("Employee Number", 0)) for employee in data]
            if existing_numbers:
                counter = max(existing_numbers)
            else:
                counter = 0

            for employee in data:
                tree.insert("", "end", values=list(employee.values()))
    except FileNotFoundError:
        data = []
        counter = 0


def save_data():
    data = []
    for item in tree.get_children():
        values = tree.item(item, "values")
        employee = {
            "Employee Number": values[0],
            "Name": values[1],
            "Birth Date": values[2],
            "Type": values[3],
            "Hire Date": values[4],
            "Base Salary": values[5],
            "Overtime Rate": values[6],
            "Overtime Hours": values[7],
            "Responsibility Bonus": values[8],
            "Net Salary": values[9],
        }
        data.append(employee)

    with open("employees.txt", "w") as file:
        for employee in data:
            file.write(f"Employee Number: {employee['Employee Number']}\n")
            file.write(f"Name: {employee['Name']}\n")
            file.write(f"Birth Date: {employee['Birth Date']}\n")
            file.write(f"Type: {employee['Type']}\n")
            file.write(f"Hire Date: {employee['Hire Date']}\n")
            file.write(f"Base Salary: {employee['Base Salary']}\n")
            file.write(f"Overtime Rate: {employee['Overtime Rate']}\n")
            file.write(f"Overtime Hours: {employee['Overtime Hours']}\n")
            file.write(f"Responsibility Bonus: {employee['Responsibility Bonus']}\n")
            file.write(f"Net Salary: {employee['Net Salary']}\n")
            file.write("\n")

def load_data_for_modification():
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, "values")
        root.selected_employee = values
        set_entry_values(values)

def set_entry_values(values):
    name_entry.delete(0, END)
    base_salary_entry.delete(0, END)
    birth_date_entry.delete(0, END)
    hire_date_entry.delete(0, END)
    overtime_rate_entry.delete(0, END)
    overtime_hours_entry.delete(0, END)
    responsibility_bonus_entry.delete(0, END)

    name_entry.insert(0, values[1])
    birth_date_entry.insert(0, values[2])
    hire_date_entry.insert(0, values[4])
    base_salary_entry.insert(0, values[5])

    if values[3] == "Trainer":
        overtime_rate_entry["state"] = "normal"
        overtime_hours_entry["state"] = "normal"
        overtime_rate_entry.insert(0, values[6])
        overtime_hours_entry.insert(0, values[7])
    elif values[3] == "Agent":
        responsibility_bonus_entry["state"] = "normal"
        responsibility_bonus_entry.insert(0, values[8])

def apply_modifications():
    if root.selected_employee:
        selected_item = tree.selection()
        values = get_entry_values()

        # Update Treeview
        tree.item(selected_item, values=values)

        # Save modifications to file
        save_data()

        # Clear selected employee and entry values
        root.selected_employee = None
        clear_entry_values()

def get_entry_values():
    name = name_entry.get()
    baseSalary = float(base_salary_entry.get()) if base_salary_entry.get() else 0.0
    birthDate = birth_date_entry.get()
    hireDate = hire_date_entry.get()

    selected_type = employee_type.get()

    if selected_type == "Trainer":
        overtimeRate = float(overtime_rate_entry.get()) if overtime_rate_entry.get() else 0.0
        overtimeHours = int(overtime_hours_entry.get()) if overtime_hours_entry.get() else 0
        return (root.selected_employee[0], name, birthDate, selected_type, hireDate, baseSalary, overtimeRate, overtimeHours, "", "")
    elif selected_type == "Agent":
        responsibilityBonus = float(responsibility_bonus_entry.get()) if responsibility_bonus_entry.get() else 0.0
        return (root.selected_employee[0], name, birthDate, selected_type, hireDate, baseSalary, "", "", responsibilityBonus, "")
    else:
        raise ValueError("Unsupported employee type")

def clear_entry_values():
    name_entry.delete(0, END)
    base_salary_entry.delete(0, END)
    birth_date_entry.delete(0, END)
    hire_date_entry.delete(0, END)
    overtime_rate_entry.delete(0, END)
    overtime_hours_entry.delete(0, END)
    responsibility_bonus_entry.delete(0, END)
    
def on_employee_type_change(*args):
    selected_type = employee_type.get()

    # Enable/disable entry widgets based on employee type
    overtime_rate_entry["state"] = "normal" if selected_type == "Trainer" else "disabled"
    overtime_hours_entry["state"] = "normal" if selected_type == "Trainer" else "disabled"
    responsibility_bonus_entry["state"] = "normal" if selected_type == "Agent" else "disabled"

# Main window
root = Tk()
root.title("Employee Manager")
root.selected_employee = None

# Labels for employee information
name_label = Label(root, text="Name:")
name_label.place(x=20, y=10)
birth_date_label = Label(root, text="Birth Date (m/d/y) :")
birth_date_label.place(x=20, y=40)
hire_date_label = Label(root, text="Hire Date (m/d/y) :")
hire_date_label.place(x=20, y=70)
base_salary_label = Label(root, text="Base Salary:")
base_salary_label.place(x=20, y=100)

# Entry widgets for employee information
name_entry = Entry(root)
name_entry.place(x=150, y=10)
birth_date_entry = Entry(root)
birth_date_entry.place(x=150, y=40)
hire_date_entry = Entry(root)
hire_date_entry.place(x=150, y=70)
base_salary_entry = Entry(root)
base_salary_entry.place(x=150, y=100)

# Radio buttons label
radio_label = Label(root, text="Employee Type:")
radio_label.place(x=20, y=130)

# Radio buttons for employee type
employee_type = StringVar()
employee_type.trace_add("write", on_employee_type_change)  # Track changes to employee type
trainer_radio = Radiobutton(root, text="Trainer", variable=employee_type, value="Trainer")
trainer_radio.place(x=150, y=130)
agent_radio = Radiobutton(root, text="Agent", variable=employee_type, value="Agent")
agent_radio.place(x=240, y=130)


# Entry widgets for additional information
overtime_rate_label = Label(root, text="Overtime Rate:")
overtime_rate_label.place(x=20, y=160)
overtime_rate_entry = Entry(root, state="disabled")  # Initially disabled
overtime_rate_entry.place(x=150, y=160)

overtime_hours_label = Label(root, text="Overtime Hours:")
overtime_hours_label.place(x=20, y=190)
overtime_hours_entry = Entry(root, state="disabled")  # Initially disabled
overtime_hours_entry.place(x=150, y=190)

responsibility_bonus_label = Label(root, text="Responsibility Bonus:")
responsibility_bonus_label.place(x=20, y=220)
responsibility_bonus_entry = Entry(root, state="disabled")  # Initially disabled
responsibility_bonus_entry.place(x=150, y=220)

# Buttons
add_button = Button(root, text="Add Employee", command=add_employee)
add_button.place(x=20, y=255)
remove_button = Button(root, text="Remove Employee", command=remove_employee)
remove_button.place(x=120, y=255)
# Button to load data into entry widgets for modification
load_data_button = Button(root, text="Load Data for Modification", command=load_data_for_modification)
load_data_button.place(x=20, y=285)

# Button to apply modifications
apply_modifications_button = Button(root, text="Apply Modifications", command=apply_modifications)
apply_modifications_button.place(x=200, y=285)

# Button to load data into entry widgets for modification
# load_data_button = Button(root, text="Load Data for Modification")
# load_data_button.place(x=20, y=540)

# Button to apply modifications
# apply_modifications_button = Button(root, text="Apply Modifications")
# apply_modifications_button.place(x=200, y=540)

# Create Treeview with increased width
columns = ("Employee Number", "Name", "Birth Date","Type", "Hire Date", "Base Salary",
           "Overtime Rate", "Overtime Hours", "Responsibility Bonus", "Net Salary")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col, anchor='center')
    tree.column(col, width=120,anchor='center')

tree.place(x=20, y=300)


load_data()

root.mainloop()
