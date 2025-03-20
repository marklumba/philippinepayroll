# from models.database import Employee, Session
# from typing import List, Optional
# from datetime import datetime

# class EmployeeController:
#     def __init__(self):
#         self.session = Session()

#     def get_all_employees(self) -> List[Employee]:
#         return self.session.query(Employee).all()

#     def get_employee(self, employee_id: str) -> Optional[Employee]:
#         return self.session.query(Employee).filter(Employee.id == employee_id).first()

#     def save_employee(self, employee_data: dict) -> None:
#         # Validate required fields
#         required_fields = ['id', 'first_name', 'last_name', 'birth_date', 'hire_date']
#         for field in required_fields:
#             if not employee_data.get(field):
#                 raise ValueError(f"Missing required field: {field}")

#         # Check for existing employee
#         existing_employee = self.get_employee(employee_data['id'])

#         if existing_employee:
#             # Update existing employee
#             for key, value in employee_data.items():
#                 setattr(existing_employee, key, value)
#         else:
#             # Create new employee
#             new_employee = Employee(**employee_data)
#             self.session.add(new_employee)

#         try:
#             self.session.commit()
#         except Exception as e:
#             self.session.rollback()
#             raise ValueError(f"Failed to save employee: {str(e)}")

#     def delete_employee(self, employee_id: str) -> None:
#         employee = self.get_employee(employee_id)
#         if employee:
#             employee.active = False  # Soft delete
#             try:
#                 self.session.commit()
#             except Exception as e:
#                 self.session.rollback()
#                 raise ValueError(f"Failed to delete employee: {str(e)}")

#     def search_employees(self, search_term: str) -> List[Employee]:
#         search_term = search_term.lower()
#         return self.session.query(Employee).filter(
#             (Employee.first_name.ilike(f'%{search_term}%')) |
#             (Employee.last_name.ilike(f'%{search_term}%')) |
#             (Employee.id.ilike(f'%{search_term}%'))
#         ).all()

#     def __del__(self):
#         self.session.close()


# controllers/employee_controller.py
from models.database import Employee, Session
from typing import List, Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

class EmployeeController:
    def __init__(self):
        self.session_factory = Session

    def _get_session(self):
        return self.session_factory()

    def get_all_employees(self) -> List[Employee]:
        session = self._get_session()
        try:
            # Since we're switching to hard delete, no need to filter by active
            return session.query(Employee).all()
        finally:
            session.close()

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        session = self._get_session()
        try:
            return session.query(Employee).filter(Employee.id == employee_id).first()
        finally:
            session.close()

    def save_employee(self, employee_data: dict) -> None:
        session = self._get_session()
        try:
            # Validate required fields
            required_fields = ['id', 'first_name', 'last_name', 'birth_date', 'hire_date']
            for field in required_fields:
                if not employee_data.get(field):
                    raise ValueError(f"Missing required field: {field}")

            # Set default values for optional fields
            employee_data.setdefault('position', '')
            employee_data.setdefault('department', '')
            employee_data.setdefault('basic_salary', 0.0)
            employee_data.setdefault('tax_status', '')
            employee_data.setdefault('sss_number', '')
            employee_data.setdefault('philhealth_number', '')
            employee_data.setdefault('pagibig_number', '')
            employee_data.setdefault('tin_number', '')
            employee_data.setdefault('active', True)  # Still include for schema compatibility

            # Check for existing employee
            existing_employee = session.query(Employee).filter(Employee.id == employee_data['id']).first()

            if existing_employee:
                # Update existing employee
                for key, value in employee_data.items():
                    setattr(existing_employee, key, value)
            else:
                # Create new employee
                new_employee = Employee(**employee_data)
                session.add(new_employee)

            session.commit()
            print(f"Employee {employee_data['id']} saved successfully")
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"Database error (possible duplicate ID): {str(e)}")
        except (ValueError, SQLAlchemyError) as e:
            session.rollback()
            raise ValueError(f"Failed to save employee: {str(e)}")
        finally:
            session.close()

    def delete_employee(self, employee_id: str) -> None:
        session = self._get_session()
        try:
            employee = session.query(Employee).filter(Employee.id == employee_id).first()
            print(f"Attempting to delete employee with ID: {employee_id}, Found: {employee is not None}")
            if employee:
                session.delete(employee)  # Hard delete: remove the record
                session.commit()
                print(f"Employee {employee_id} deleted from database")
            else:
                raise ValueError(f"Employee with ID {employee_id} not found")
        except (ValueError, SQLAlchemyError) as e:
            session.rollback()
            raise ValueError(f"Failed to delete employee: {str(e)}")
        finally:
            session.close()

    def search_employees(self, search_term: str) -> List[Employee]:
        session = self._get_session()
        try:
            search_term = search_term.lower()
            return session.query(Employee).filter(
                (Employee.first_name.ilike(f'%{search_term}%')) |
                (Employee.last_name.ilike(f'%{search_term}%')) |
                (Employee.id.ilike(f'%{search_term}%'))
            ).all()
        finally:
            session.close()