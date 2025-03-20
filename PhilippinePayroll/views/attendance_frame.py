import customtkinter as ctk
from controllers.attendance_controller import AttendanceController
from controllers.employee_controller import EmployeeController
from models.attendance import AttendanceRecord
from datetime import datetime, date, time
import tkinter as tk
from tkinter import messagebox

class AttendanceFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.attendance_controller = AttendanceController()
        self.employee_controller = EmployeeController()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.create_attendance_input_frame()
        self.create_attendance_list_frame()
        
    def create_attendance_input_frame(self):
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Employee selection
        ctk.CTkLabel(input_frame, text="Select Employee:").pack(padx=5, pady=5)
        self.employee_var = tk.StringVar()
        self.employee_combobox = ctk.CTkComboBox(input_frame, variable=self.employee_var,
                                                command=self.on_employee_select)
        self.employee_combobox.pack(fill="x", padx=5, pady=5)
        
        # Date selection
        ctk.CTkLabel(input_frame, text="Date:").pack(padx=5, pady=5)
        self.date_entry = ctk.CTkEntry(input_frame, placeholder_text="YYYY-MM-DD")
        self.date_entry.pack(fill="x", padx=5, pady=5)
        self.date_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        
        # Time in/out
        time_frame = ctk.CTkFrame(input_frame)
        time_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(time_frame, text="Time In:").pack()
        self.time_in_entry = ctk.CTkEntry(time_frame, placeholder_text="HH:MM")
        self.time_in_entry.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkLabel(time_frame, text="Time Out:").pack()
        self.time_out_entry = ctk.CTkEntry(time_frame, placeholder_text="HH:MM")
        self.time_out_entry.pack(fill="x", padx=5, pady=2)
        
        # Additional options
        self.is_holiday_var = tk.BooleanVar()
        self.holiday_checkbox = ctk.CTkCheckBox(input_frame, text="Holiday",
                                              variable=self.is_holiday_var)
        self.holiday_checkbox.pack(padx=5, pady=5)
        
        # Remarks
        ctk.CTkLabel(input_frame, text="Remarks:").pack(padx=5, pady=5)
        self.remarks_entry = ctk.CTkTextbox(input_frame, height=100)
        self.remarks_entry.pack(fill="x", padx=5, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(input_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(button_frame, text="Record Attendance",
                     command=self.record_attendance).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Clear",
                     command=self.clear_form).pack(side="left", padx=5)
        
        self.refresh_employee_list()
        
    def create_attendance_list_frame(self):
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Date filter
        filter_frame = ctk.CTkFrame(list_frame)
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(filter_frame, text="Filter by Date Range:").pack(side="left", padx=5)
        self.filter_start_date = ctk.CTkEntry(filter_frame, placeholder_text="Start Date")
        self.filter_start_date.pack(side="left", padx=5)
        self.filter_end_date = ctk.CTkEntry(filter_frame, placeholder_text="End Date")
        self.filter_end_date.pack(side="left", padx=5)
        ctk.CTkButton(filter_frame, text="Filter",
                     command=self.filter_attendance).pack(side="left", padx=5)
        
        # Attendance list
        ctk.CTkLabel(list_frame, text="Attendance Records:").pack(padx=5, pady=5)
        self.attendance_listbox = tk.Listbox(list_frame, height=20)
        self.attendance_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.attendance_listbox.bind('<<ListboxSelect>>', self.on_select_attendance)
        
    def refresh_employee_list(self):
        employees = self.employee_controller.get_all_employees()
        employee_options = [f"{emp.id} - {emp.last_name}, {emp.first_name}" for emp in employees]
        self.employee_combobox.configure(values=employee_options)
        
    def on_employee_select(self, choice):
        if not choice:
            return
            
        employee_id = choice.split(' - ')[0]
        self.refresh_attendance_list(employee_id)
        
    def refresh_attendance_list(self, employee_id):
        self.attendance_listbox.delete(0, tk.END)
        records = self.attendance_controller.get_employee_attendance(employee_id)
        
        for record in records:
            self.attendance_listbox.insert(tk.END,
                f"{record.date} - In: {record.time_in}, Out: {record.time_out}")
            
    def record_attendance(self):
        try:
            if not self.employee_var.get():
                raise ValueError("Please select an employee")
                
            employee_id = self.employee_var.get().split(' - ')[0]
            attendance_date = datetime.strptime(self.date_entry.get(), '%Y-%m-%d').date()
            time_in = datetime.strptime(self.time_in_entry.get(), '%H:%M').time()
            time_out = datetime.strptime(self.time_out_entry.get(), '%H:%M').time()
            
            # Calculate overtime
            overtime_hours = self.attendance_controller.calculate_overtime(time_in, time_out)
            
            record = AttendanceRecord(
                employee_id=employee_id,
                date=attendance_date,
                time_in=time_in,
                time_out=time_out,
                overtime_hours=overtime_hours,
                is_holiday=self.is_holiday_var.get(),
                is_present=True,
                remarks=self.remarks_entry.get("1.0", tk.END).strip()
            )
            
            self.attendance_controller.record_attendance(record)
            self.refresh_attendance_list(employee_id)
            self.clear_form()
            messagebox.showinfo("Success", "Attendance recorded successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def clear_form(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.time_in_entry.delete(0, tk.END)
        self.time_out_entry.delete(0, tk.END)
        self.is_holiday_var.set(False)
        self.remarks_entry.delete("1.0", tk.END)
        
    def filter_attendance(self):
        try:
            if not self.employee_var.get():
                raise ValueError("Please select an employee")
                
            employee_id = self.employee_var.get().split(' - ')[0]
            start_date = datetime.strptime(self.filter_start_date.get(), '%Y-%m-%d').date()
            end_date = datetime.strptime(self.filter_end_date.get(), '%Y-%m-%d').date()
            
            records = self.attendance_controller.get_employee_attendance(
                employee_id, start_date, end_date)
            
            self.attendance_listbox.delete(0, tk.END)
            for record in records:
                self.attendance_listbox.insert(tk.END,
                    f"{record.date} - In: {record.time_in}, Out: {record.time_out}")
                    
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def on_select_attendance(self, event):
        # Implementation for selecting attendance record (for future editing functionality)
        pass
