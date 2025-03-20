# from models.payroll import PayrollItem
# from models.employee import Employee
# from utils.json_handler import JsonHandler
# from utils.tax_calculator import TaxCalculator
# from typing import List, Optional
# from datetime import date, datetime

# class PayrollController:
#     def __init__(self):
#         self.json_handler = JsonHandler()
#         self.payroll_file = "payroll.json"
#         self.tax_calculator = TaxCalculator()

#     def calculate_payroll(self, employee: Employee, start_date: date, end_date: date,
#                          overtime_hours: float = 0, holiday_hours: float = 0) -> PayrollItem:
#         # Calculate daily rate
#         daily_rate = employee.basic_salary / 22  # Assuming 22 working days per month
#         hourly_rate = daily_rate / 8  # 8 hours per day

#         # Calculate basic pay
#         working_days = self._get_working_days(start_date, end_date)
#         basic_pay = daily_rate * working_days

#         # Calculate overtime pay
#         overtime_pay = overtime_hours * (hourly_rate * 1.25)  # 25% overtime premium

#         # Calculate holiday pay
#         holiday_pay = holiday_hours * (hourly_rate * 2)  # Double pay on holidays

#         # Calculate gross pay
#         gross_pay = basic_pay + overtime_pay + holiday_pay

#         # Calculate deductions
#         withholding_tax = self.tax_calculator.calculate_withholding_tax(gross_pay, employee.tax_status)
#         sss_contribution = self.tax_calculator.calculate_sss(employee.basic_salary)
#         philhealth_contribution = self.tax_calculator.calculate_philhealth(employee.basic_salary)
#         pagibig_contribution = self.tax_calculator.calculate_pagibig(employee.basic_salary)

#         # Calculate net pay
#         total_deductions = (withholding_tax + sss_contribution + 
#                           philhealth_contribution + pagibig_contribution)
#         net_pay = gross_pay - total_deductions

#         return PayrollItem(
#             employee_id=employee.id,
#             pay_period_start=start_date,
#             pay_period_end=end_date,
#             basic_pay=basic_pay,
#             overtime_pay=overtime_pay,
#             holiday_pay=holiday_pay,
#             gross_pay=gross_pay,
#             withholding_tax=withholding_tax,
#             sss_contribution=sss_contribution,
#             philhealth_contribution=philhealth_contribution,
#             pagibig_contribution=pagibig_contribution,
#             other_deductions={},
#             net_pay=net_pay
#         )

#     def save_payroll(self, payroll_item: PayrollItem) -> None:
#         payroll_records = self.get_all_payroll_records()
        
#         # Check for existing payroll record
#         payroll_records = [record for record in payroll_records 
#                           if not (record.employee_id == payroll_item.employee_id and 
#                                 record.pay_period_start == payroll_item.pay_period_start and
#                                 record.pay_period_end == payroll_item.pay_period_end)]
        
#         payroll_records.append(payroll_item)
#         payroll_dict = [record.to_dict() for record in payroll_records]
#         self.json_handler.save_data(self.payroll_file, payroll_dict)

#     def get_all_payroll_records(self) -> List[PayrollItem]:
#         payroll_data = self.json_handler.load_data(self.payroll_file)
#         return [PayrollItem.from_dict(record) for record in payroll_data]

#     def get_employee_payroll_history(self, employee_id: str) -> List[PayrollItem]:
#         all_records = self.get_all_payroll_records()
#         return [record for record in all_records if record.employee_id == employee_id]

#     def _get_working_days(self, start_date: date, end_date: date) -> int:
#         # Simple calculation - can be enhanced to account for actual holidays
#         total_days = (end_date - start_date).days + 1
#         weeks = total_days // 7
#         remaining_days = total_days % 7
#         working_days = weeks * 5 + min(remaining_days, 5)
#         return working_days


# controllers/payroll_controller.py
from models.payroll import PayrollItem as PayrollItemDataclass
from models.database import PayrollItem as PayrollItemModel, Session, Employee
from utils.tax_calculator import TaxCalculator
from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.exc import SQLAlchemyError

class PayrollController:
    def __init__(self):
        self.session_factory = Session
        self.tax_calculator = TaxCalculator()

    def _get_session(self):
        return self.session_factory()

    def calculate_payroll(self, employee: Employee, start_date: date, end_date: date,
                         overtime_hours: float = 0, holiday_hours: float = 0) -> PayrollItemDataclass:
        # Calculate daily rate
        daily_rate = employee.basic_salary / 22  # Assuming 22 working days per month
        hourly_rate = daily_rate / 8  # 8 hours per day

        # Calculate basic pay
        working_days = self._get_working_days(start_date, end_date)
        basic_pay = daily_rate * working_days

        # Calculate overtime pay
        overtime_pay = overtime_hours * (hourly_rate * 1.25)  # 25% overtime premium

        # Calculate holiday pay
        holiday_pay = holiday_hours * (hourly_rate * 2)  # Double pay on holidays

        # Calculate gross pay
        gross_pay = basic_pay + overtime_pay + holiday_pay

        # Calculate deductions
        withholding_tax = self.tax_calculator.calculate_withholding_tax(gross_pay, employee.tax_status)
        sss_contribution = self.tax_calculator.calculate_sss(employee.basic_salary)
        philhealth_contribution = self.tax_calculator.calculate_philhealth(employee.basic_salary)
        pagibig_contribution = self.tax_calculator.calculate_pagibig(employee.basic_salary)

        # Calculate net pay
        total_deductions = (withholding_tax + sss_contribution + 
                          philhealth_contribution + pagibig_contribution)
        net_pay = gross_pay - total_deductions

        return PayrollItemDataclass(
            employee_id=employee.id,
            pay_period_start=start_date,
            pay_period_end=end_date,
            basic_pay=basic_pay,
            overtime_pay=overtime_pay,
            holiday_pay=holiday_pay,
            gross_pay=gross_pay,
            withholding_tax=withholding_tax,
            sss_contribution=sss_contribution,
            philhealth_contribution=philhealth_contribution,
            pagibig_contribution=pagibig_contribution,
            other_deductions={},
            net_pay=net_pay
        )

    def save_payroll(self, payroll_item: PayrollItemDataclass) -> None:
        session = self._get_session()
        try:
            # Check for existing payroll record in the database
            existing_record = session.query(PayrollItemModel).filter(
                PayrollItemModel.employee_id == payroll_item.employee_id,
                PayrollItemModel.pay_period_start == payroll_item.pay_period_start,
                PayrollItemModel.pay_period_end == payroll_item.pay_period_end
            ).first()

            if existing_record:
                # Update existing record
                existing_record.basic_pay = payroll_item.basic_pay
                existing_record.overtime_pay = payroll_item.overtime_pay
                existing_record.holiday_pay = payroll_item.holiday_pay
                existing_record.gross_pay = payroll_item.gross_pay
                existing_record.withholding_tax = payroll_item.withholding_tax
                existing_record.sss_contribution = payroll_item.sss_contribution
                existing_record.philhealth_contribution = payroll_item.philhealth_contribution
                existing_record.pagibig_contribution = payroll_item.pagibig_contribution
                existing_record.net_pay = payroll_item.net_pay
            else:
                # Create new record
                payroll_record = PayrollItemModel(
                    employee_id=payroll_item.employee_id,
                    pay_period_start=payroll_item.pay_period_start,
                    pay_period_end=payroll_item.pay_period_end,
                    basic_pay=payroll_item.basic_pay,
                    overtime_pay=payroll_item.overtime_pay,
                    holiday_pay=payroll_item.holiday_pay,
                    gross_pay=payroll_item.gross_pay,
                    withholding_tax=payroll_item.withholding_tax,
                    sss_contribution=payroll_item.sss_contribution,
                    philhealth_contribution=payroll_item.philhealth_contribution,
                    pagibig_contribution=payroll_item.pagibig_contribution,
                    net_pay=payroll_item.net_pay
                )
                session.add(payroll_record)

            session.commit()
            print(f"Payroll record saved to database for employee {payroll_item.employee_id}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to save payroll: {str(e)}")
        finally:
            session.close()

    def get_all_payroll_records(self) -> List[PayrollItemDataclass]:
        session = self._get_session()
        try:
            records = session.query(PayrollItemModel).all()
            return [PayrollItemDataclass(
                employee_id=record.employee_id,
                pay_period_start=record.pay_period_start,
                pay_period_end=record.pay_period_end,
                basic_pay=record.basic_pay,
                overtime_pay=record.overtime_pay,
                holiday_pay=record.holiday_pay,
                gross_pay=record.gross_pay,
                withholding_tax=record.withholding_tax,
                sss_contribution=record.sss_contribution,
                philhealth_contribution=record.philhealth_contribution,
                pagibig_contribution=record.pagibig_contribution,
                other_deductions={},
                net_pay=record.net_pay
            ) for record in records]
        finally:
            session.close()

    def get_employee_payroll_history(self, employee_id: str) -> List[PayrollItemDataclass]:
        session = self._get_session()
        try:
            records = session.query(PayrollItemModel).filter(PayrollItemModel.employee_id == employee_id).all()
            return [PayrollItemDataclass(
                employee_id=record.employee_id,
                pay_period_start=record.pay_period_start,
                pay_period_end=record.pay_period_end,
                basic_pay=record.basic_pay,
                overtime_pay=record.overtime_pay,
                holiday_pay=record.holiday_pay,
                gross_pay=record.gross_pay,
                withholding_tax=record.withholding_tax,
                sss_contribution=record.sss_contribution,
                philhealth_contribution=record.philhealth_contribution,
                pagibig_contribution=record.pagibig_contribution,
                other_deductions={},
                net_pay=record.net_pay
            ) for record in records]
        finally:
            session.close()

    def _get_working_days(self, start_date: date, end_date: date) -> int:
        # Simple calculation - can be enhanced to account for actual holidays
        total_days = (end_date - start_date).days + 1
        weeks = total_days // 7
        remaining_days = total_days % 7
        working_days = weeks * 5 + min(remaining_days, 5)
        return working_days