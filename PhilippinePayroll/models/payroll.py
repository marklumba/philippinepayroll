from dataclasses import dataclass
from datetime import date
from typing import List, Dict

@dataclass
class PayrollItem:
    employee_id: str
    pay_period_start: date
    pay_period_end: date
    basic_pay: float
    overtime_pay: float
    holiday_pay: float
    gross_pay: float
    withholding_tax: float
    sss_contribution: float
    philhealth_contribution: float
    pagibig_contribution: float
    other_deductions: Dict[str, float]
    net_pay: float
    
    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'pay_period_start': self.pay_period_start.isoformat(),
            'pay_period_end': self.pay_period_end.isoformat(),
            'basic_pay': self.basic_pay,
            'overtime_pay': self.overtime_pay,
            'holiday_pay': self.holiday_pay,
            'gross_pay': self.gross_pay,
            'withholding_tax': self.withholding_tax,
            'sss_contribution': self.sss_contribution,
            'philhealth_contribution': self.philhealth_contribution,
            'pagibig_contribution': self.pagibig_contribution,
            'other_deductions': self.other_deductions,
            'net_pay': self.net_pay
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            employee_id=data['employee_id'],
            pay_period_start=date.fromisoformat(data['pay_period_start']),
            pay_period_end=date.fromisoformat(data['pay_period_end']),
            basic_pay=float(data['basic_pay']),
            overtime_pay=float(data['overtime_pay']),
            holiday_pay=float(data['holiday_pay']),
            gross_pay=float(data['gross_pay']),
            withholding_tax=float(data['withholding_tax']),
            sss_contribution=float(data['sss_contribution']),
            philhealth_contribution=float(data['philhealth_contribution']),
            pagibig_contribution=float(data['pagibig_contribution']),
            other_deductions=data['other_deductions'],
            net_pay=float(data['net_pay'])
        )
