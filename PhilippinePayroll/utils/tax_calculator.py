# class TaxCalculator:
#     @staticmethod
#     def calculate_withholding_tax(monthly_income: float, tax_status: str) -> float:
#         """
#         Calculate withholding tax based on Philippine BIR tax table
#         """
#         # 2023 Philippine Tax Table
#         if monthly_income <= 20833:  # 250,000 annually
#             return 0
#         elif monthly_income <= 33333:  # 400,000 annually
#             taxable_excess = monthly_income - 20833
#             return taxable_excess * 0.20
#         elif monthly_income <= 66667:  # 800,000 annually
#             taxable_excess = monthly_income - 33333
#             return 2500 + (taxable_excess * 0.25)
#         elif monthly_income <= 166667:  # 2,000,000 annually
#             taxable_excess = monthly_income - 66667
#             return 10833 + (taxable_excess * 0.30)
#         elif monthly_income <= 666667:  # 8,000,000 annually
#             taxable_excess = monthly_income - 166667
#             return 40833.33 + (taxable_excess * 0.32)
#         else:
#             taxable_excess = monthly_income - 666667
#             return 200833.33 + (taxable_excess * 0.35)

#     @staticmethod
#     def calculate_sss(monthly_salary: float) -> float:
#         """
#         Calculate SSS contribution based on Philippine SSS contribution table
#         """
#         # Simplified SSS computation (2023 table)
#         if monthly_salary <= 3250:
#             return 135.00
#         elif monthly_salary > 24750:
#             return 1125.00
#         else:
#             # Rough calculation (actual table has specific brackets)
#             return monthly_salary * 0.045

#     @staticmethod
#     def calculate_philhealth(monthly_salary: float) -> float:
#         """
#         Calculate PhilHealth contribution based on Philippine PhilHealth contribution table
#         """
#         # 2023 PhilHealth contribution rate is 3%
#         rate = 0.03
#         contribution = monthly_salary * rate
#         # Split equally between employee and employer
#         return contribution / 2

#     @staticmethod
#     def calculate_pagibig(monthly_salary: float) -> float:
#         """
#         Calculate Pag-IBIG contribution
#         """
#         if monthly_salary > 1500:
#             return monthly_salary * 0.02
#         return monthly_salary * 0.01


# utils/tax_calculator.py
class TaxCalculator:
    @staticmethod
    def calculate_withholding_tax(monthly_income: float, tax_status: str) -> float:
        """
        Calculate withholding tax based on Philippine BIR tax table (TRAIN Law, 2025 rates).
        Note: Tax brackets are unchanged since 2018 under TRAIN Law, but verify for 2025.
        """
        # TRAIN Law tax table (as of last update in 2018, assumed same for 2025)
        if monthly_income <= 20833:  # Below 250,000 annually
            return 0.0
        elif monthly_income <= 33333:  # 250,001 - 400,000 annually
            taxable_excess = monthly_income - 20833
            return taxable_excess * 0.15  # Updated rate from 0.20 to 0.15 (TRAIN Law adjustment)
        elif monthly_income <= 66667:  # 400,001 - 800,000 annually
            taxable_excess = monthly_income - 33333
            return 1875 + (taxable_excess * 0.20)  # Adjusted base tax
        elif monthly_income <= 166667:  # 800,001 - 2,000,000 annually
            taxable_excess = monthly_income - 66667
            return 10250 + (taxable_excess * 0.25)
        elif monthly_income <= 666667:  # 2,000,001 - 8,000,000 annually
            taxable_excess = monthly_income - 166667
            return 40250 + (taxable_excess * 0.30)
        else:  # Above 8,000,000 annually
            taxable_excess = monthly_income - 666667
            return 200250 + (taxable_excess * 0.35)

    @staticmethod
    def calculate_sss(monthly_salary: float) -> float:
        """
        Calculate SSS contribution based on Philippine SSS contribution table (2025 rates).
        Rates updated based on SSS Circular 2023-013, with assumed adjustments for 2025.
        """
        # SSS contribution table (2025: 14% total rate, employee share is 4.5%)
        if monthly_salary < 4250:
            return 180.00  # Minimum contribution
        elif monthly_salary >= 29750:
            return 1350.00  # Maximum contribution
        else:
            # Employee share: 4.5% of monthly salary
            return monthly_salary * 0.045

    @staticmethod
    def calculate_philhealth(monthly_salary: float) -> float:
        """
        Calculate PhilHealth contribution based on Philippine PhilHealth table (2025 rates).
        Rate is 5% in 2025, split equally between employee and employer.
        """
        # 2025 PhilHealth contribution rate: 5%, salary cap at 100,000 PHP
        rate = 0.05
        salary_base = min(monthly_salary, 100000)  # Cap at 100,000 PHP
        contribution = salary_base * rate
        return contribution / 2  # Employee share

    @staticmethod
    def calculate_pagibig(monthly_salary: float) -> float:
        """
        Calculate Pag-IBIG contribution (2025 rates).
        Rate is 2% for both employee and employer, capped at 5,000 PHP salary base.
        """
        # Pag-IBIG contribution: 2% of monthly salary, max salary base 5,000 PHP
        salary_base = min(monthly_salary, 5000)  # Cap at 5,000 PHP
        contribution = salary_base * 0.02
        return min(contribution, 100.0)  # Max employee contribution is 100 PHP