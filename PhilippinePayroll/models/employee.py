from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Employee:
    id: str
    first_name: str
    last_name: str
    birth_date: date
    hire_date: date
    position: str
    department: str
    basic_salary: float
    tax_status: str  # Single, Married, etc.
    sss_number: str
    philhealth_number: str
    pagibig_number: str
    tin_number: str
    active: bool = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.isoformat(),
            'hire_date': self.hire_date.isoformat(),
            'position': self.position,
            'department': self.department,
            'basic_salary': self.basic_salary,
            'tax_status': self.tax_status,
            'sss_number': self.sss_number,
            'philhealth_number': self.philhealth_number,
            'pagibig_number': self.pagibig_number,
            'tin_number': self.tin_number,
            'active': self.active
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=date.fromisoformat(data['birth_date']),
            hire_date=date.fromisoformat(data['hire_date']),
            position=data['position'],
            department=data['department'],
            basic_salary=float(data['basic_salary']),
            tax_status=data['tax_status'],
            sss_number=data['sss_number'],
            philhealth_number=data['philhealth_number'],
            pagibig_number=data['pagibig_number'],
            tin_number=data['tin_number'],
            active=data.get('active', True)
        )
