import customtkinter as ctk
from controllers.employee_controller import EmployeeController
from controllers.payroll_controller import PayrollController
from controllers.attendance_controller import AttendanceController
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
import csv
import os

class ReportsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.employee_controller = EmployeeController()
        self.payroll_controller = PayrollController()
        self.attendance_controller = AttendanceController()
        
        self.grid_columnconfigure(0, weight=1)
        self.create_reports_interface()
        
    def create_reports_interface(self):
        # Report type selection
        selection_frame = ctk.CTkFrame(self)
        selection_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(selection_frame, text="Report Type:").pack(side="left", padx=5)
        self.report_type = tk.StringVar(value="payroll")
        
        report_types = [
            ("Payroll Summary", "payroll"),
            ("Attendance Summary", "attendance"),
            ("Employee List", "employee")
        ]
        
        for text, value in report_types:
            ctk.CTkRadioButton(selection_frame, text=text, variable=self.report_type,
                             value=value, command=self.update_report_options).pack(side="left", padx=10)
        
        # Filter options frame
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Date range frame
        self.date_frame = ctk.CTkFrame(self.filter_frame)
        self.date_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(self.date_frame, text="Date Range:").pack(side="left", padx=5)
        self.start_date = ctk.CTkEntry(self.date_frame, placeholder_text="Start Date (YYYY-MM-DD)")
        self.start_date.pack(side="left", padx=5)
        self.end_date = ctk.CTkEntry(self.date_frame, placeholder_text="End Date (YYYY-MM-DD)")
        self.end_date.pack(side="left", padx=5)
        
        # Employee selection
        self.employee_frame = ctk.CTkFrame(self.filter_frame)
        self.employee_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(self.employee_frame, text="Employee:").pack(side="left", padx=5)
        self.employee_var = tk.StringVar()
        self.employee_combobox = ctk.CTkComboBox(self.employee_frame,
                                                variable=self.employee_var,
                                                values=self.get_employee_list())
        self.employee_combobox.pack(side="left", padx=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(button_frame, text="Generate Report",
                     command=self.generate_report).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Export to CSV",
                     command=self.export_to_csv).pack(side="left", padx=5)
        
        # Report display
        ctk.CTkLabel(self, text="Report Preview:").pack(padx=10, pady=5)
        self.report_text = tk.Text(self, height=20, width=80)
        self.report_text.pack(fill="both", expand=True, padx=10, pady=5)
        
    def get_employee_list(self):
        employees = self.employee_controller.get_all_employees()
        return [f"{emp.id} - {emp.last_name}, {emp.first_name}" for emp in employees]
        
    def update_report_options(self):
        report_type = self.report_type.get()
        
        if report_type == "employee":
            self.date_frame.pack_forget()
        else:
            self.date_frame.pack(fill="x", padx=5, pady=5)
            
    def generate_report(self):
        try:
            report_type = self.report_type.get()
            self.report_text.delete(1.0, tk.END)
            
            if report_type == "payroll":
                self.generate_payroll_report()
            elif report_type == "attendance":
                self.generate_attendance_report()
            else:
                self.generate_employee_report()
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def generate_payroll_report(self):
        try:
            start_date = datetime.strptime(self.start_date.get(), '%Y-%m-%d').date()
            end_date = datetime.strptime(self.end_date.get(), '%Y-%m-%d').date()
            
            if self.employee_var.get():
                employee_id = self.employee_var.get().split(' - ')[0]
                records = self.payroll_controller.get_employee_payroll_history(employee_id)
            else:
                records = self.payroll_controller.get_all_payroll_records()
                
            records = [r for r in records if start_date <= r.pay_period_start <= end_date]
            
            self.report_text.insert(tk.END, "PAYROLL SUMMARY REPORT\n")
            self.report_text.insert(tk.END, f"Period: {start_date} to {end_date}\n\n")
            
            total_gross = 0
            total_net = 0
            
            for record in records:
                employee = self.employee_controller.get_employee(record.employee_id)
                self.report_text.insert(tk.END,
                    f"Employee: {employee.last_name}, {employee.first_name}\n")
                self.report_text.insert(tk.END,
                    f"Gross Pay: ₱{record.gross_pay:,.2f}\n")
                self.report_text.insert(tk.END,
                    f"Net Pay: ₱{record.net_pay:,.2f}\n")
                self.report_text.insert(tk.END, "-" * 50 + "\n")
                
                total_gross += record.gross_pay
                total_net += record.net_pay
                
            self.report_text.insert(tk.END, f"\nTotal Gross Pay: ₱{total_gross:,.2f}\n")
            self.report_text.insert(tk.END, f"Total Net Pay: ₱{total_net:,.2f}\n")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def generate_attendance_report(self):
        try:
            start_date = datetime.strptime(self.start_date.get(), '%Y-%m-%d').date()
            end_date = datetime.strptime(self.end_date.get(), '%Y-%m-%d').date()
            
            if self.employee_var.get():
                employee_id = self.employee_var.get().split(' - ')[0]
                records = self.attendance_controller.get_employee_attendance(
                    employee_id, start_date, end_date)
            else:
                employees = self.employee_controller.get_all_employees()
                records = []
                for employee in employees:
                    records.extend(self.attendance_controller.get_employee_attendance(
                        employee.id, start_date, end_date))
                        
            self.report_text.insert(tk.END, "ATTENDANCE SUMMARY REPORT\n")
            self.report_text.insert(tk.END, f"Period: {start_date} to {end_date}\n\n")
            
            current_employee = None
            for record in sorted(records, key=lambda x: (x.employee_id, x.date)):
                if current_employee != record.employee_id:
                    current_employee = record.employee_id
                    employee = self.employee_controller.get_employee(current_employee)
                    self.report_text.insert(tk.END, f"\nEmployee: {employee.last_name}, {employee.first_name}\n")
                    self.report_text.insert(tk.END, "-" * 50 + "\n")
                    
                self.report_text.insert(tk.END,
                    f"Date: {record.date} | In: {record.time_in} | Out: {record.time_out} | "
                    f"OT: {record.overtime_hours:.2f}hrs\n")
                    
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def generate_employee_report(self):
        employees = self.employee_controller.get_all_employees()
        
        self.report_text.insert(tk.END, "EMPLOYEE LIST REPORT\n")
        self.report_text.insert(tk.END, f"Generated on: {date.today()}\n\n")
        
        for employee in sorted(employees, key=lambda x: x.last_name):
            self.report_text.insert(tk.END,
                f"ID: {employee.id}\n"
                f"Name: {employee.last_name}, {employee.first_name}\n"
                f"Position: {employee.position}\n"
                f"Department: {employee.department}\n"
                f"Basic Salary: ₱{employee.basic_salary:,.2f}\n")
            self.report_text.insert(tk.END, "-" * 50 + "\n")
            
    def export_to_csv(self):
        try:
            report_type = self.report_type.get()
            filename = f"{report_type}_report_{date.today().strftime('%Y%m%d')}.csv"
            
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                
                if report_type == "payroll":
                    self.export_payroll_csv(writer)
                elif report_type == "attendance":
                    self.export_attendance_csv(writer)
                else:
                    self.export_employee_csv(writer)
                    
            messagebox.showinfo("Success", f"Report exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
            
    def export_payroll_csv(self, writer):
        writer.writerow(['Employee ID', 'Name', 'Period Start', 'Period End',
                        'Gross Pay', 'Net Pay', 'Tax', 'SSS', 'PhilHealth', 'Pag-IBIG'])
        # Add payroll data rows
        
    def export_attendance_csv(self, writer):
        writer.writerow(['Employee ID', 'Name', 'Date', 'Time In', 'Time Out',
                        'Overtime Hours', 'Is Holiday', 'Remarks'])
        # Add attendance data rows
        
    def export_employee_csv(self, writer):
        writer.writerow(['ID', 'Last Name', 'First Name', 'Position', 'Department',
                        'Basic Salary', 'Tax Status'])
        # Add employee data rows
