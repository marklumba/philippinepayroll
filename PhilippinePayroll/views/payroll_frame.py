import customtkinter as ctk
from controllers.payroll_controller import PayrollController
from controllers.employee_controller import EmployeeController
from datetime import datetime, date
from tkinter import messagebox
import tkinter as tk

class PayrollFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.payroll_controller = PayrollController()
        self.employee_controller = EmployeeController()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.create_payroll_list_frame()
        self.create_payroll_details_frame()
        
    def create_payroll_list_frame(self):
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Employee selection
        ctk.CTkLabel(self.list_frame, text="Select Employee:").pack(padx=5, pady=5)
        self.employee_var = tk.StringVar()
        self.employee_combobox = ctk.CTkComboBox(self.list_frame, variable=self.employee_var,
                                                command=self.on_employee_select)
        self.employee_combobox.pack(fill="x", padx=5, pady=5)
        
        # Payroll period
        period_frame = ctk.CTkFrame(self.list_frame)
        period_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(period_frame, text="Period:").pack()
        self.start_date_entry = ctk.CTkEntry(period_frame, placeholder_text="Start Date (YYYY-MM-DD)")
        self.start_date_entry.pack(fill="x", padx=5, pady=2)
        
        self.end_date_entry = ctk.CTkEntry(period_frame, placeholder_text="End Date (YYYY-MM-DD)")
        self.end_date_entry.pack(fill="x", padx=5, pady=2)
        
        # Payroll history
        ctk.CTkLabel(self.list_frame, text="Payroll History:").pack(padx=5, pady=5)
        self.payroll_listbox = tk.Listbox(self.list_frame, height=15)
        self.payroll_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.payroll_listbox.bind('<<ListboxSelect>>', self.on_select_payroll)
        
        self.refresh_employee_list()
        
    def create_payroll_details_frame(self):
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Earnings section
        earnings_frame = ctk.CTkFrame(self.details_frame)
        earnings_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(earnings_frame, text="Earnings", font=("Arial", 14, "bold")).pack()
        
        self.basic_pay_entry = self.create_readonly_entry(earnings_frame, "Basic Pay:")
        self.overtime_pay_entry = self.create_readonly_entry(earnings_frame, "Overtime Pay:")
        self.holiday_pay_entry = self.create_readonly_entry(earnings_frame, "Holiday Pay:")
        self.gross_pay_entry = self.create_readonly_entry(earnings_frame, "Gross Pay:")
        
        # Deductions section
        deductions_frame = ctk.CTkFrame(self.details_frame)
        deductions_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(deductions_frame, text="Deductions", font=("Arial", 14, "bold")).pack()
        
        self.tax_entry = self.create_readonly_entry(deductions_frame, "Withholding Tax:")
        self.sss_entry = self.create_readonly_entry(deductions_frame, "SSS Contribution:")
        self.philhealth_entry = self.create_readonly_entry(deductions_frame, "PhilHealth:")
        self.pagibig_entry = self.create_readonly_entry(deductions_frame, "Pag-IBIG:")
        
        # Net Pay section
        net_pay_frame = ctk.CTkFrame(self.details_frame)
        net_pay_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(net_pay_frame, text="Net Pay", font=("Arial", 16, "bold")).pack()
        self.net_pay_entry = self.create_readonly_entry(net_pay_frame, "Net Pay:")
        
        # Buttons
        button_frame = ctk.CTkFrame(self.details_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(button_frame, text="Calculate", command=self.calculate_payroll).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Save", command=self.save_payroll).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Print", command=self.print_payroll).pack(side="left", padx=5)
        
    def create_readonly_entry(self, parent, label_text):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkLabel(frame, text=label_text).pack(side="left")
        entry = ctk.CTkEntry(frame, state="readonly")
        entry.pack(side="right", expand=True, fill="x", padx=5)
        return entry
        
    def refresh_employee_list(self):
        employees = self.employee_controller.get_all_employees()
        employee_options = [f"{emp.id} - {emp.last_name}, {emp.first_name}" for emp in employees]
        self.employee_combobox.configure(values=employee_options)
        
    def on_employee_select(self, choice):
        if not choice:
            return
            
        employee_id = choice.split(' - ')[0]
        payroll_records = self.payroll_controller.get_employee_payroll_history(employee_id)
        
        self.payroll_listbox.delete(0, tk.END)
        for record in payroll_records:
            self.payroll_listbox.insert(tk.END, 
                f"{record.pay_period_start} to {record.pay_period_end} - ₱{record.net_pay:,.2f}")
            
    # def on_select_payroll(self, event):
    #     # Implementation for selecting payroll record from history
    #     pass

    def on_select_payroll(self, event):
        selection = self.payroll_listbox.curselection()
        if not selection:
           return
        
        index = selection[0]
        employee_id = self.employee_var.get().split(' - ')[0]
        payroll_records = self.payroll_controller.get_employee_payroll_history(employee_id)
    
        if index < len(payroll_records):
           payroll = payroll_records[index]
        
           # Update UI with selected payroll details
           self.basic_pay_entry.configure(state="normal")
           self.basic_pay_entry.delete(0, tk.END)
           self.basic_pay_entry.insert(0, f"₱{payroll.basic_pay:,.2f}")
           self.basic_pay_entry.configure(state="readonly")
        
           self.overtime_pay_entry.configure(state="normal")
           self.overtime_pay_entry.delete(0, tk.END)
           self.overtime_pay_entry.insert(0, f"₱{payroll.overtime_pay:,.2f}")
           self.overtime_pay_entry.configure(state="readonly")
        
           self.holiday_pay_entry.configure(state="normal")
           self.holiday_pay_entry.delete(0, tk.END)
           self.holiday_pay_entry.insert(0, f"₱{payroll.holiday_pay:,.2f}")
           self.holiday_pay_entry.configure(state="readonly")
        
           self.gross_pay_entry.configure(state="normal")
           self.gross_pay_entry.delete(0, tk.END)
           self.gross_pay_entry.insert(0, f"₱{payroll.gross_pay:,.2f}")
           self.gross_pay_entry.configure(state="readonly")
        
           self.tax_entry.configure(state="normal")
           self.tax_entry.delete(0, tk.END)
           self.tax_entry.insert(0, f"₱{payroll.withholding_tax:,.2f}")
           self.tax_entry.configure(state="readonly")
        
           self.sss_entry.configure(state="normal")
           self.sss_entry.delete(0, tk.END)
           self.sss_entry.insert(0, f"₱{payroll.sss_contribution:,.2f}")
           self.sss_entry.configure(state="readonly")
        
           self.philhealth_entry.configure(state="normal")
           self.philhealth_entry.delete(0, tk.END)
           self.philhealth_entry.insert(0, f"₱{payroll.philhealth_contribution:,.2f}")
           self.philhealth_entry.configure(state="readonly")
        
           self.pagibig_entry.configure(state="normal")
           self.pagibig_entry.delete(0, tk.END)
           self.pagibig_entry.insert(0, f"₱{payroll.pagibig_contribution:,.2f}")
           self.pagibig_entry.configure(state="readonly")
        
           self.net_pay_entry.configure(state="normal")
           self.net_pay_entry.delete(0, tk.END)
           self.net_pay_entry.insert(0, f"₱{payroll.net_pay:,.2f}")
           self.net_pay_entry.configure(state="readonly")
        
           # Update date entries
           self.start_date_entry.delete(0, tk.END)
           self.start_date_entry.insert(0, payroll.pay_period_start.strftime('%Y-%m-%d'))
           self.end_date_entry.delete(0, tk.END)
           self.end_date_entry.insert(0, payroll.pay_period_end.strftime('%Y-%m-%d'))
        
    def calculate_payroll(self):
        try:
            employee_id = self.employee_var.get().split(' - ')[0]
            employee = self.employee_controller.get_employee(employee_id)
            
            start_date = datetime.strptime(self.start_date_entry.get(), '%Y-%m-%d').date()
            end_date = datetime.strptime(self.end_date_entry.get(), '%Y-%m-%d').date()
            
            payroll = self.payroll_controller.calculate_payroll(employee, start_date, end_date)
            
            # Update UI with calculated values
            self.basic_pay_entry.configure(state="normal")
            self.basic_pay_entry.delete(0, tk.END)
            self.basic_pay_entry.insert(0, f"₱{payroll.basic_pay:,.2f}")
            self.basic_pay_entry.configure(state="readonly")
            
            # Update other fields similarly
            self.overtime_pay_entry.configure(state="normal")
            self.overtime_pay_entry.delete(0, tk.END)
            self.overtime_pay_entry.insert(0, f"₱{payroll.overtime_pay:,.2f}")
            self.overtime_pay_entry.configure(state="readonly")
            
            self.holiday_pay_entry.configure(state="normal")
            self.holiday_pay_entry.delete(0, tk.END)
            self.holiday_pay_entry.insert(0, f"₱{payroll.holiday_pay:,.2f}")
            self.holiday_pay_entry.configure(state="readonly")
            
            self.gross_pay_entry.configure(state="normal")
            self.gross_pay_entry.delete(0, tk.END)
            self.gross_pay_entry.insert(0, f"₱{payroll.gross_pay:,.2f}")
            self.gross_pay_entry.configure(state="readonly")
            
            self.tax_entry.configure(state="normal")
            self.tax_entry.delete(0, tk.END)
            self.tax_entry.insert(0, f"₱{payroll.withholding_tax:,.2f}")
            self.tax_entry.configure(state="readonly")
            
            self.sss_entry.configure(state="normal")
            self.sss_entry.delete(0, tk.END)
            self.sss_entry.insert(0, f"₱{payroll.sss_contribution:,.2f}")
            self.sss_entry.configure(state="readonly")
            
            self.philhealth_entry.configure(state="normal")
            self.philhealth_entry.delete(0, tk.END)
            self.philhealth_entry.insert(0, f"₱{payroll.philhealth_contribution:,.2f}")
            self.philhealth_entry.configure(state="readonly")
            
            self.pagibig_entry.configure(state="normal")
            self.pagibig_entry.delete(0, tk.END)
            self.pagibig_entry.insert(0, f"₱{payroll.pagibig_contribution:,.2f}")
            self.pagibig_entry.configure(state="readonly")
            
            self.net_pay_entry.configure(state="normal")
            self.net_pay_entry.delete(0, tk.END)
            self.net_pay_entry.insert(0, f"₱{payroll.net_pay:,.2f}")
            self.net_pay_entry.configure(state="readonly")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def save_payroll(self):
        try:
            employee_id = self.employee_var.get().split(' - ')[0]
            employee = self.employee_controller.get_employee(employee_id)
            
            start_date = datetime.strptime(self.start_date_entry.get(), '%Y-%m-%d').date()
            end_date = datetime.strptime(self.end_date_entry.get(), '%Y-%m-%d').date()
            
            payroll = self.payroll_controller.calculate_payroll(employee, start_date, end_date)
            self.payroll_controller.save_payroll(payroll)
            
            messagebox.showinfo("Success", "Payroll record saved successfully!")
            self.on_employee_select(self.employee_var.get())
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def print_payroll(self):
        messagebox.showinfo("Print", "Printing functionality to be implemented")
