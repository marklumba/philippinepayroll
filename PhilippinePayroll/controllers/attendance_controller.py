# from models.attendance import AttendanceRecord
# from utils.json_handler import JsonHandler
# from typing import List, Optional
# from datetime import date, time, datetime, timedelta

# class AttendanceController:
#     def __init__(self):
#         self.json_handler = JsonHandler()
#         self.attendance_file = "attendance.json"

#     def record_attendance(self, attendance_record: AttendanceRecord) -> None:
#         attendance_records = self.get_all_attendance_records()
        
#         # Remove existing record for the same employee and date if exists
#         attendance_records = [record for record in attendance_records 
#                             if not (record.employee_id == attendance_record.employee_id and 
#                                   record.date == attendance_record.date)]
        
#         attendance_records.append(attendance_record)
#         attendance_dict = [record.to_dict() for record in attendance_records]
#         self.json_handler.save_data(self.attendance_file, attendance_dict)

#     def get_all_attendance_records(self) -> List[AttendanceRecord]:
#         attendance_data = self.json_handler.load_data(self.attendance_file)
#         return [AttendanceRecord.from_dict(record) for record in attendance_data]

#     def get_employee_attendance(self, employee_id: str, start_date: date = None, 
#                               end_date: date = None) -> List[AttendanceRecord]:
#         records = self.get_all_attendance_records()
#         employee_records = [record for record in records if record.employee_id == employee_id]
        
#         if start_date and end_date:
#             employee_records = [record for record in employee_records 
#                               if start_date <= record.date <= end_date]
        
#         return sorted(employee_records, key=lambda x: x.date)

#     def calculate_overtime(self, time_in: time, time_out: time) -> float:
#         # Regular work hours: 8 hours
#         regular_hours = timedelta(hours=8)
#         actual_hours = datetime.combine(date.today(), time_out) - datetime.combine(date.today(), time_in)
        
#         if actual_hours > regular_hours:
#             overtime = (actual_hours - regular_hours).total_seconds() / 3600  # Convert to hours
#             return round(overtime, 2)
#         return 0.0

#     def get_monthly_attendance_summary(self, employee_id: str, year: int, month: int) -> dict:
#         start_date = date(year, month, 1)
#         if month == 12:
#             end_date = date(year + 1, 1, 1) - timedelta(days=1)
#         else:
#             end_date = date(year, month + 1, 1) - timedelta(days=1)

#         records = self.get_employee_attendance(employee_id, start_date, end_date)
        
#         total_days = len(records)
#         present_days = len([r for r in records if r.is_present])
#         absent_days = total_days - present_days
#         total_overtime = sum(r.overtime_hours for r in records)
        
#         return {
#             'total_days': total_days,
#             'present_days': present_days,
#             'absent_days': absent_days,
#             'total_overtime': total_overtime
#         }

#     def delete_attendance_record(self, employee_id: str, record_date: date) -> None:
#         records = self.get_all_attendance_records()
#         records = [record for record in records 
#                   if not (record.employee_id == employee_id and record.date == record_date)]
#         records_dict = [record.to_dict() for record in records]
#         self.json_handler.save_data(self.attendance_file, records_dict)


# controllers/attendance_controller.py
from models.attendance import AttendanceRecord as AttendanceRecordDataclass
from models.database import AttendanceRecord as AttendanceRecordModel, Session, Employee
from typing import List, Optional
from datetime import date, time, datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

class AttendanceController:
    def __init__(self):
        self.session_factory = Session

    def _get_session(self):
        return self.session_factory()

    def record_attendance(self, attendance_record: AttendanceRecordDataclass) -> None:
        session = self._get_session()
        try:
            # Check for existing record for the same employee and date
            existing_record = session.query(AttendanceRecordModel).filter(
                AttendanceRecordModel.employee_id == attendance_record.employee_id,
                AttendanceRecordModel.date == attendance_record.date
            ).first()

            if existing_record:
                # Update existing record
                existing_record.time_in = attendance_record.time_in
                existing_record.time_out = attendance_record.time_out
                existing_record.overtime_hours = attendance_record.overtime_hours
                existing_record.is_holiday = attendance_record.is_holiday
                existing_record.is_present = attendance_record.is_present
                existing_record.remarks = attendance_record.remarks
            else:
                # Create new record
                new_record = AttendanceRecordModel(
                    employee_id=attendance_record.employee_id,
                    date=attendance_record.date,
                    time_in=attendance_record.time_in,
                    time_out=attendance_record.time_out,
                    overtime_hours=attendance_record.overtime_hours,
                    is_holiday=attendance_record.is_holiday,
                    is_present=attendance_record.is_present,
                    remarks=attendance_record.remarks
                )
                session.add(new_record)

            session.commit()
            print(f"Attendance record saved for employee {attendance_record.employee_id} on {attendance_record.date}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to record attendance: {str(e)}")
        finally:
            session.close()

    def get_all_attendance_records(self) -> List[AttendanceRecordDataclass]:
        session = self._get_session()
        try:
            records = session.query(AttendanceRecordModel).all()
            return [AttendanceRecordDataclass(
                employee_id=record.employee_id,
                date=record.date,
                time_in=record.time_in,
                time_out=record.time_out,
                overtime_hours=record.overtime_hours,
                is_holiday=record.is_holiday,
                is_present=record.is_present,
                remarks=record.remarks
            ) for record in records]
        finally:
            session.close()

    def get_employee_attendance(self, employee_id: str, start_date: date = None, 
                              end_date: date = None) -> List[AttendanceRecordDataclass]:
        session = self._get_session()
        try:
            query = session.query(AttendanceRecordModel).filter(AttendanceRecordModel.employee_id == employee_id)
            if start_date and end_date:
                query = query.filter(AttendanceRecordModel.date.between(start_date, end_date))
            records = query.all()
            return sorted([AttendanceRecordDataclass(
                employee_id=record.employee_id,
                date=record.date,
                time_in=record.time_in,
                time_out=record.time_out,
                overtime_hours=record.overtime_hours,
                is_holiday=record.is_holiday,
                is_present=record.is_present,
                remarks=record.remarks
            ) for record in records], key=lambda x: x.date)
        finally:
            session.close()

    def calculate_overtime(self, time_in: time, time_out: time) -> float:
        # Regular work hours: 8 hours
        regular_hours = timedelta(hours=8)
        actual_hours = datetime.combine(date.today(), time_out) - datetime.combine(date.today(), time_in)
        
        if actual_hours > regular_hours:
            overtime = (actual_hours - regular_hours).total_seconds() / 3600  # Convert to hours
            return round(overtime, 2)
        return 0.0

    def get_monthly_attendance_summary(self, employee_id: str, year: int, month: int) -> dict:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        records = self.get_employee_attendance(employee_id, start_date, end_date)
        
        total_days = len(records)
        present_days = len([r for r in records if r.is_present])
        absent_days = total_days - present_days
        total_overtime = sum(r.overtime_hours for r in records)
        
        return {
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'total_overtime': total_overtime
        }

    def delete_attendance_record(self, employee_id: str, record_date: date) -> None:
        session = self._get_session()
        try:
            record = session.query(AttendanceRecordModel).filter(
                AttendanceRecordModel.employee_id == employee_id,
                AttendanceRecordModel.date == record_date
            ).first()
            if record:
                session.delete(record)
                session.commit()
                print(f"Attendance record deleted for employee {employee_id} on {record_date}")
            else:
                raise ValueError(f"No attendance record found for employee {employee_id} on {record_date}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to delete attendance record: {str(e)}")
        finally:
            session.close()