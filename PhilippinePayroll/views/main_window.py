import customtkinter as ctk
from views.employee_frame import EmployeeFrame
from views.payroll_frame import PayrollFrame
from views.attendance_frame import AttendanceFrame
from views.reports_frame import ReportsFrame

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Philippine Payroll System")
        self.geometry("1200x800")
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
        # Navigation label
        self.navigation_label = ctk.CTkLabel(self.navigation_frame, text="Navigation",
                                           compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Navigation buttons
        self.employee_button = ctk.CTkButton(self.navigation_frame, text="Employees",
                                           command=self.show_employees)
        self.employee_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.payroll_button = ctk.CTkButton(self.navigation_frame, text="Payroll",
                                          command=self.show_payroll)
        self.payroll_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.attendance_button = ctk.CTkButton(self.navigation_frame, text="Attendance",
                                             command=self.show_attendance)
        self.attendance_button.grid(row=3, column=0, padx=20, pady=10)
        
        self.reports_button = ctk.CTkButton(self.navigation_frame, text="Reports",
                                          command=self.show_reports)
        self.reports_button.grid(row=4, column=0, padx=20, pady=10)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Create frames for different sections
        self.employee_frame = EmployeeFrame(self.main_frame)
        self.payroll_frame = PayrollFrame(self.main_frame)
        self.attendance_frame = AttendanceFrame(self.main_frame)
        self.reports_frame = ReportsFrame(self.main_frame)
        
        # Show employee frame by default
        self.show_employees()
        
    def show_employees(self):
        self.hide_all_frames()
        self.employee_frame.grid(row=0, column=0, sticky="nsew")
        self.employee_button.configure(fg_color=("gray75", "gray25"))
        
    def show_payroll(self):
        self.hide_all_frames()
        self.payroll_frame.grid(row=0, column=0, sticky="nsew")
        self.payroll_button.configure(fg_color=("gray75", "gray25"))
        
    def show_attendance(self):
        self.hide_all_frames()
        self.attendance_frame.grid(row=0, column=0, sticky="nsew")
        self.attendance_button.configure(fg_color=("gray75", "gray25"))
        
    def show_reports(self):
        self.hide_all_frames()
        self.reports_frame.grid(row=0, column=0, sticky="nsew")
        self.reports_button.configure(fg_color=("gray75", "gray25"))
        
    def hide_all_frames(self):
        self.employee_frame.grid_remove()
        self.payroll_frame.grid_remove()
        self.attendance_frame.grid_remove()
        self.reports_frame.grid_remove()
        
        # Reset button colors
        self.employee_button.configure(fg_color=("gray70", "gray30"))
        self.payroll_button.configure(fg_color=("gray70", "gray30"))
        self.attendance_button.configure(fg_color=("gray70", "gray30"))
        self.reports_button.configure(fg_color=("gray70", "gray30"))
