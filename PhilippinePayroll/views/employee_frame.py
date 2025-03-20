# import customtkinter as ctk
# from controllers.employee_controller import EmployeeController
# from datetime import datetime
# import tkinter as tk
# from tkinter import messagebox

# class EmployeeFrame(ctk.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.controller = EmployeeController()
        
#         # Configure grid
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=3)
        
#         # Create frames
#         self.create_employee_list_frame()
#         self.create_employee_details_frame()
        
#     def create_employee_list_frame(self):
#         # Employee list frame
#         self.list_frame = ctk.CTkFrame(self)
#         self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
#         # Search frame
#         self.search_frame = ctk.CTkFrame(self.list_frame)
#         self.search_frame.pack(fill="x", padx=5, pady=5)
        
#         self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search employees...")
#         self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
#         self.search_button = ctk.CTkButton(self.search_frame, text="Search",
#                                          command=self.search_employees)
#         self.search_button.pack(side="right", padx=5)
        
#         # Employee listbox
#         self.employee_listbox = tk.Listbox(self.list_frame)
#         self.employee_listbox.pack(fill="both", expand=True, padx=5, pady=5)
#         self.employee_listbox.bind('<<ListboxSelect>>', self.on_select_employee)
        
#         # Refresh employee list
#         self.refresh_employee_list()
        
#     def create_employee_details_frame(self):
#         # Employee details frame
#         self.details_frame = ctk.CTkFrame(self)
#         self.details_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
#         # Form fields
#         labels = ['ID', 'First Name', 'Last Name', 'Birth Date', 'Hire Date',
#                  'Position', 'Department', 'Basic Salary', 'Tax Status',
#                  'SSS Number', 'PhilHealth Number', 'Pag-IBIG Number', 'TIN Number']
        
#         self.entries = {}
#         for i, label in enumerate(labels):
#             ctk.CTkLabel(self.details_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
#             entry = ctk.CTkEntry(self.details_frame)
#             entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
#             self.entries[label.lower().replace(' ', '_')] = entry
            
#         # Buttons
#         button_frame = ctk.CTkFrame(self.details_frame)
#         button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        
#         ctk.CTkButton(button_frame, text="New", command=self.clear_form).pack(side="left", padx=5)
#         ctk.CTkButton(button_frame, text="Save", command=self.save_employee).pack(side="left", padx=5)
#         ctk.CTkButton(button_frame, text="Delete", command=self.delete_employee).pack(side="left", padx=5)
        
#     def refresh_employee_list(self):
#         self.employee_listbox.delete(0, tk.END)
#         employees = self.controller.get_all_employees()
#         for employee in employees:
#             self.employee_listbox.insert(tk.END, f"{employee.id} - {employee.last_name}, {employee.first_name}")
            
#     def search_employees(self):
#         search_text = self.search_entry.get().lower()
#         self.employee_listbox.delete(0, tk.END)
#         employees = self.controller.get_all_employees()
#         for employee in employees:
#             if (search_text in employee.first_name.lower() or
#                 search_text in employee.last_name.lower() or
#                 search_text in employee.id.lower()):
#                 self.employee_listbox.insert(tk.END, f"{employee.id} - {employee.last_name}, {employee.first_name}")
                
#     def on_select_employee(self, event):
#         selection = self.employee_listbox.curselection()
#         if not selection:
#             return
            
#         employee_id = self.employee_listbox.get(selection[0]).split(' - ')[0]
#         employee = self.controller.get_employee(employee_id)
        
#         if employee:
#             # self.entries['id'].delete(0, tk.END)
#             # self.entries['id'].insert(0, employee.id)
#             # self.entries['first_name'].delete(0, tk.END)
#             # self.entries['first_name'].insert(0, employee.first_name)
#             # self.entries['last_name'].delete(0, tk.END)
#             # self.entries['last_name'].insert(0, employee.last_name)
#             # # Fill other fields similarly
#             self.entries['id'].delete(0, tk.END)
#             self.entries['id'].insert(0, employee.id)
#             self.entries['first_name'].delete(0, tk.END)
#             self.entries['first_name'].insert(0, employee.first_name)
#             self.entries['last_name'].delete(0, tk.END)
#             self.entries['last_name'].insert(0, employee.last_name)
#             self.entries['birth_date'].delete(0, tk.END)
#             self.entries['birth_date'].insert(0, employee.birth_date.strftime('%Y-%m-%d'))
#             self.entries['hire_date'].delete(0, tk.END)
#             self.entries['hire_date'].insert(0, employee.hire_date.strftime('%Y-%m-%d'))
#             self.entries['position'].delete(0, tk.END)
#             self.entries['position'].insert(0, employee.position)
#             self.entries['department'].delete(0, tk.END)
#             self.entries['department'].insert(0, employee.department)
#             self.entries['basic_salary'].delete(0, tk.END)
#             self.entries['basic_salary'].insert(0, str(employee.basic_salary))
#             self.entries['tax_status'].delete(0, tk.END)
#             self.entries['tax_status'].insert(0, employee.tax_status)
#             self.entries['sss_number'].delete(0, tk.END)
#             self.entries['sss_number'].insert(0, employee.sss_number)
#             self.entries['philhealth_number'].delete(0, tk.END)
#             self.entries['philhealth_number'].insert(0, employee.philhealth_number)
#             self.entries['pag-ibig_number'].delete(0, tk.END)
#             self.entries['pag-ibig_number'].insert(0, employee.pagibig_number)
#             self.entries['tin_number'].delete(0, tk.END)
#             self.entries['tin_number'].insert(0, employee.tin_number)
            
#     def clear_form(self):
#         for entry in self.entries.values():
#             entry.delete(0, tk.END)
            
#     def save_employee(self):
#         try:
#             employee_data = {
#                 'id': self.entries['id'].get(),
#                 'first_name': self.entries['first_name'].get(),
#                 'last_name': self.entries['last_name'].get(),
#                 'birth_date': datetime.strptime(self.entries['birth_date'].get(), '%Y-%m-%d').date(),
#                 'hire_date': datetime.strptime(self.entries['hire_date'].get(), '%Y-%m-%d').date(),
#                 'position': self.entries['position'].get(),
#                 'department': self.entries['department'].get(),
#                 'basic_salary': float(self.entries['basic_salary'].get()),
#                 'tax_status': self.entries['tax_status'].get(),
#                 'sss_number': self.entries['sss_number'].get(),
#                 'philhealth_number': self.entries['philhealth_number'].get(),
#                 'pagibig_number': self.entries['pag-ibig_number'].get(),
#                 'tin_number': self.entries['tin_number'].get()
#             }
            
#             self.controller.save_employee(employee_data)
#             self.refresh_employee_list()
#             messagebox.showinfo("Success", "Employee saved successfully!")
            
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))

#     # def save_employee(self):
#     #     try:
#     #         employee_data = {
#     #           'id': self.entries['id'].get(),
#     #           'first_name': self.entries['first_name'].get(),
#     #           'last_name': self.entries['last_name'].get(),
#     #           'birth_date': datetime.strptime(self.entries['birth_date'].get(), '%Y-%m-%d').date(),
#     #           'hire_date': datetime.strptime(self.entries['hire_date'].get(), '%Y-%m-%d').date(),
#     #           'position': self.entries['position'].get(),
#     #           'department': self.entries['department'].get(),
#     #           'basic_salary': float(self.entries['basic_salary'].get()),
#     #           'tax_status': self.entries['tax_status'].get(),
#     #           'sss_number': self.entries['sss_number'].get(),
#     #           'philhealth_number': self.entries['philhealth_number'].get(),
#     #           'pag-ibig_number': self.entries['pag-ibig_number'].get(),
#     #           'tin_number': self.entries['tin_number'].get(),
#     #           'active': True
#     #         }
#     #         print("Saving employee_data:", employee_data)  # Debug
#     #         self.controller.save_employee(employee_data)
#     #         self.refresh_employee_list()
#     #         messagebox.showinfo("Success", "Employee saved successfully!")
#     #     except ValueError as e:
#     #         messagebox.showerror("Error", str(e))
            
#     # def delete_employee(self):
#     #     employee_id = self.entries['id'].get()
#     #     if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
#     #         self.controller.delete_employee(employee_id)
#     #         self.refresh_employee_list()
#     #         self.clear_form()
#     #         messagebox.showinfo("Success", "Employee deleted successfully!")

#     def delete_employee(self):
#         employee_id = self.entries['id'].get()
#         if not employee_id:
#            messagebox.showerror("Error", "No employee selected")
#            return
        
#         if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
#            if self.controller.delete_employee(employee_id):
#               self.refresh_employee_list()
#               self.clear_form()
#               messagebox.showinfo("Success", "Employee deleted successfully!")
#            else:
#               messagebox.showerror("Error", "Failed to delete employee. Record not found.")




# employee_frame.py
import customtkinter as ctk
from controllers.employee_controller import EmployeeController
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class EmployeeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.controller = EmployeeController()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.create_employee_list_frame()
        self.create_employee_details_frame()
        
    def create_employee_list_frame(self):
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.search_frame = ctk.CTkFrame(self.list_frame)
        self.search_frame.pack(fill="x", padx=5, pady=5)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search employees...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        self.search_button = ctk.CTkButton(self.search_frame, text="Search",
                                         command=self.search_employees)
        self.search_button.pack(side="right", padx=5)
        
        self.employee_listbox = tk.Listbox(self.list_frame)
        self.employee_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.employee_listbox.bind('<<ListboxSelect>>', self.on_select_employee)
        
        self.refresh_employee_list()
        
    def create_employee_details_frame(self):
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        labels = ['ID', 'First Name', 'Last Name', 'Birth Date', 'Hire Date',
                 'Position', 'Department', 'Basic Salary', 'Tax Status',
                 'SSS Number', 'PhilHealth Number', 'Pag-IBIG Number', 'TIN Number']
        
        self.entries = {}
        for i, label in enumerate(labels):
            ctk.CTkLabel(self.details_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ctk.CTkEntry(self.details_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[label.lower().replace(' ', '_')] = entry
            
        button_frame = ctk.CTkFrame(self.details_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(button_frame, text="New", command=self.clear_form).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Save", command=self.save_employee).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Delete", command=self.delete_employee).pack(side="left", padx=5)
        
    def refresh_employee_list(self):
        self.employee_listbox.delete(0, tk.END)
        employees = self.controller.get_all_employees()
        for employee in employees:
            self.employee_listbox.insert(tk.END, f"{employee.id} - {employee.last_name}, {employee.first_name}")
            
    def search_employees(self):
        search_text = self.search_entry.get().lower()
        self.employee_listbox.delete(0, tk.END)
        employees = self.controller.search_employees(search_text)
        for employee in employees:
            self.employee_listbox.insert(tk.END, f"{employee.id} - {employee.last_name}, {employee.first_name}")
                
    def on_select_employee(self, event):
        selection = self.employee_listbox.curselection()
        if not selection:
            return
            
        employee_id = self.employee_listbox.get(selection[0]).split(' - ')[0]
        employee = self.controller.get_employee(employee_id)
        
        if employee:
            print(f"Selected employee ID: {employee_id}")
            self.entries['id'].delete(0, tk.END)
            self.entries['id'].insert(0, employee.id)
            self.entries['first_name'].delete(0, tk.END)
            self.entries['first_name'].insert(0, employee.first_name)
            self.entries['last_name'].delete(0, tk.END)
            self.entries['last_name'].insert(0, employee.last_name)
            self.entries['birth_date'].delete(0, tk.END)
            self.entries['birth_date'].insert(0, employee.birth_date.strftime('%Y-%m-%d'))
            self.entries['hire_date'].delete(0, tk.END)
            self.entries['hire_date'].insert(0, employee.hire_date.strftime('%Y-%m-%d'))
            self.entries['position'].delete(0, tk.END)
            self.entries['position'].insert(0, employee.position)
            self.entries['department'].delete(0, tk.END)
            self.entries['department'].insert(0, employee.department)
            self.entries['basic_salary'].delete(0, tk.END)
            self.entries['basic_salary'].insert(0, str(employee.basic_salary))
            self.entries['tax_status'].delete(0, tk.END)
            self.entries['tax_status'].insert(0, employee.tax_status)
            self.entries['sss_number'].delete(0, tk.END)
            self.entries['sss_number'].insert(0, employee.sss_number)
            self.entries['philhealth_number'].delete(0, tk.END)
            self.entries['philhealth_number'].insert(0, employee.philhealth_number)
            self.entries['pag-ibig_number'].delete(0, tk.END)
            self.entries['pag-ibig_number'].insert(0, employee.pagibig_number)
            self.entries['tin_number'].delete(0, tk.END)
            self.entries['tin_number'].insert(0, employee.tin_number)
        else:
            print(f"No employee found with ID: {employee_id}")
            
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            
    def save_employee(self):
        try:
            employee_data = {
                'id': self.entries['id'].get(),
                'first_name': self.entries['first_name'].get(),
                'last_name': self.entries['last_name'].get(),
                'birth_date': datetime.strptime(self.entries['birth_date'].get(), '%Y-%m-%d').date(),
                'hire_date': datetime.strptime(self.entries['hire_date'].get(), '%Y-%m-%d').date(),
                'position': self.entries['position'].get(),
                'department': self.entries['department'].get(),
                'basic_salary': float(self.entries['basic_salary'].get()),
                'tax_status': self.entries['tax_status'].get(),
                'sss_number': self.entries['sss_number'].get(),
                'philhealth_number': self.entries['philhealth_number'].get(),
                'pagibig_number': self.entries['pag-ibig_number'].get(),
                'tin_number': self.entries['tin_number'].get(),
                'active': True
            }
            print("Saving employee_data:", employee_data)
            self.controller.save_employee(employee_data)
            self.refresh_employee_list()
            messagebox.showinfo("Success", "Employee saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def delete_employee(self):
        employee_id = self.entries['id'].get()
        if not employee_id:
            messagebox.showerror("Error", "No employee selected")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
            try:
                print(f"Deleting employee with ID: {employee_id}")
                self.controller.delete_employee(employee_id)
                self.refresh_employee_list()
                self.clear_form()
                messagebox.showinfo("Success", "Employee deleted successfully!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))