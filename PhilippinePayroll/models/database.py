# from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, Boolean, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# import os

# # Get database URL from environment
# DATABASE_URL = os.environ.get('DATABASE_URL')


# # Create database engine
# engine = create_engine(DATABASE_URL)

# # Create declarative base
# Base = declarative_base()

# class Employee(Base):
#     __tablename__ = 'employees'
    
#     id = Column(String(50), primary_key=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     birth_date = Column(Date, nullable=False)
#     hire_date = Column(Date, nullable=False)
#     position = Column(String(100), nullable=False)
#     department = Column(String(100), nullable=False)
#     basic_salary = Column(Float, nullable=False)
#     tax_status = Column(String(20), nullable=False)
#     sss_number = Column(String(20))
#     philhealth_number = Column(String(20))
#     pagibig_number = Column(String(20))
#     tin_number = Column(String(20))
#     active = Column(Boolean, default=True)
    
#     # Relationships
#     attendance_records = relationship("AttendanceRecord", back_populates="employee")
#     payroll_records = relationship("PayrollItem", back_populates="employee")

# class AttendanceRecord(Base):
#     __tablename__ = 'attendance'
    
#     id = Column(Integer, primary_key=True)
#     employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
#     date = Column(Date, nullable=False)
#     time_in = Column(Time, nullable=False)
#     time_out = Column(Time, nullable=False)
#     overtime_hours = Column(Float, default=0.0)
#     is_holiday = Column(Boolean, default=False)
#     is_present = Column(Boolean, default=True)
#     remarks = Column(String(200))
    
#     # Relationship
#     employee = relationship("Employee", back_populates="attendance_records")

# class PayrollItem(Base):
#     __tablename__ = 'payroll'
    
#     id = Column(Integer, primary_key=True)
#     employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
#     pay_period_start = Column(Date, nullable=False)
#     pay_period_end = Column(Date, nullable=False)
#     basic_pay = Column(Float, nullable=False)
#     overtime_pay = Column(Float, nullable=False)
#     holiday_pay = Column(Float, nullable=False)
#     gross_pay = Column(Float, nullable=False)
#     withholding_tax = Column(Float, nullable=False)
#     sss_contribution = Column(Float, nullable=False)
#     philhealth_contribution = Column(Float, nullable=False)
#     pagibig_contribution = Column(Float, nullable=False)
#     net_pay = Column(Float, nullable=False)
    
#     # Relationship
#     employee = relationship("Employee", back_populates="payroll_records")

# # Create session factory
# Session = sessionmaker(bind=engine)

# # Create all tables
# def init_db():
#     Base.metadata.create_all(engine)

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your .env file.")

# Create database engine
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(String(50), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    hire_date = Column(Date, nullable=False)
    position = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    basic_salary = Column(Float, nullable=False)
    tax_status = Column(String(20), nullable=False)
    sss_number = Column(String(20))
    philhealth_number = Column(String(20))
    pagibig_number = Column(String(20))
    tin_number = Column(String(20))
    active = Column(Boolean, default=True)
    
    # Relationships
    attendance_records = relationship("AttendanceRecord", back_populates="employee")
    payroll_records = relationship("PayrollItem", back_populates="employee")

class AttendanceRecord(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    date = Column(Date, nullable=False)
    time_in = Column(Time, nullable=False)
    time_out = Column(Time, nullable=False)
    overtime_hours = Column(Float, default=0.0)
    is_holiday = Column(Boolean, default=False)
    is_present = Column(Boolean, default=True)
    remarks = Column(String(200))
    
    # Relationship
    employee = relationship("Employee", back_populates="attendance_records")

class PayrollItem(Base):
    __tablename__ = 'payroll'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    basic_pay = Column(Float, nullable=False)
    overtime_pay = Column(Float, nullable=False)
    holiday_pay = Column(Float, nullable=False)
    gross_pay = Column(Float, nullable=False)
    withholding_tax = Column(Float, nullable=False)
    sss_contribution = Column(Float, nullable=False)
    philhealth_contribution = Column(Float, nullable=False)
    pagibig_contribution = Column(Float, nullable=False)
    net_pay = Column(Float, nullable=False)
    
    # Relationship
    employee = relationship("Employee", back_populates="payroll_records")

# Create session factory
Session = sessionmaker(bind=engine)

# Create all tables
def init_db():
    Base.metadata.create_all(engine)


