from dataclasses import dataclass
from datetime import date, time
from typing import Optional

@dataclass
class AttendanceRecord:
    employee_id: str
    date: date
    time_in: time
    time_out: time
    overtime_hours: float = 0.0
    is_holiday: bool = False
    is_present: bool = True
    remarks: Optional[str] = None
    
    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'date': self.date.isoformat(),
            'time_in': self.time_in.isoformat(),
            'time_out': self.time_out.isoformat(),
            'overtime_hours': self.overtime_hours,
            'is_holiday': self.is_holiday,
            'is_present': self.is_present,
            'remarks': self.remarks
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            employee_id=data['employee_id'],
            date=date.fromisoformat(data['date']),
            time_in=time.fromisoformat(data['time_in']),
            time_out=time.fromisoformat(data['time_out']),
            overtime_hours=float(data['overtime_hours']),
            is_holiday=data['is_holiday'],
            is_present=data['is_present'],
            remarks=data.get('remarks')
        )
