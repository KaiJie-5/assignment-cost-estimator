from dataclasses import dataclass
from decimal import Decimal

from .swiss import (
    SwissContributions,
    SwissHomeDeductions,
    hypothetical_home_deductions,
    swiss_contributions,
)
from .uk import Benefit, classify_benefits, gross_up_uk_tax, uk_income_tax

FAMILY_ALLOWANCE_RATE = Decimal("0.01025")
ADMINISTRATION_RATE = Decimal("0.01")


@dataclass(frozen=True)
class AnnualCost:
    benefits: dict[str, Benefit]
    taxable_benefits_gbp: Decimal
    uk_pay_before_tax_gbp: Decimal
    uk_tax_before_gross_up_gbp: Decimal
    uk_tax_gbp: Decimal
    swiss_assessable_pay_chf: Decimal
    swiss_contributions: SwissContributions
    swiss_family_allowance_chf: Decimal
    swiss_admin_charge_chf: Decimal
    total_gbp: Decimal


@dataclass(frozen=True)
class AssignmentCost:
    salary_chf: Decimal
    bonus_chf: Decimal
    chf_per_gbp: Decimal
    home_deductions: SwissHomeDeductions
    net_home_pay_gbp: Decimal
    housing_relief: bool
    year_one: AnnualCost
    year_two: AnnualCost

    @property
    def gross_home_pay_chf(self) -> Decimal:
        return self.salary_chf + self.bonus_chf

    @property
    def total_gbp(self) -> Decimal:
        return self.year_one.total_gbp + self.year_two.total_gbp


def estimate_assignment_cost(
    *,
    salary_chf: Decimal,
    bonus_chf: Decimal,
    chf_per_gbp: Decimal,
    monthly_housing_gbp: Decimal,
    relocation_allowance_chf: Decimal,
    moving_costs_gbp: Decimal,
    temporary_housing_gbp: Decimal,
    housing_relief: bool,
) -> AssignmentCost:
    gross_home_pay = salary_chf + bonus_chf
    home_deductions = hypothetical_home_deductions(gross_home_pay)
    swiss_cash_wage = gross_home_pay - home_deductions.income_tax_chf
    net_home_pay = (
        swiss_cash_wage - home_deductions.contributions.total_chf
    ) / chf_per_gbp
    annual_rent = monthly_housing_gbp * 12

    year_one_benefits = classify_benefits(
        housing_gbp=annual_rent,
        relocation_allowance_gbp=relocation_allowance_chf / chf_per_gbp,
        moving_costs_gbp=moving_costs_gbp,
        temporary_housing_gbp=temporary_housing_gbp,
        housing_relief=housing_relief,
    )
    year_two_benefits = classify_benefits(
        housing_gbp=annual_rent,
        relocation_allowance_gbp=Decimal(0),
        moving_costs_gbp=Decimal(0),
        temporary_housing_gbp=Decimal(0),
        housing_relief=housing_relief,
    )
    return AssignmentCost(
        salary_chf=salary_chf,
        bonus_chf=bonus_chf,
        chf_per_gbp=chf_per_gbp,
        home_deductions=home_deductions,
        net_home_pay_gbp=net_home_pay,
        housing_relief=housing_relief,
        year_one=_annual_cost(
            year_one_benefits, net_home_pay, swiss_cash_wage, chf_per_gbp
        ),
        year_two=_annual_cost(
            year_two_benefits, net_home_pay, swiss_cash_wage, chf_per_gbp
        ),
    )


def _annual_cost(
    benefits: dict[str, Benefit],
    net_home_pay_gbp: Decimal,
    swiss_cash_wage_chf: Decimal,
    chf_per_gbp: Decimal,
) -> AnnualCost:
    benefit_cost = sum(item.cost_gbp for item in benefits.values())
    taxable_benefits = sum(item.taxable_gbp for item in benefits.values())
    uk_pay_before_tax = net_home_pay_gbp + taxable_benefits
    uk_tax = gross_up_uk_tax(uk_pay_before_tax)

    # Under the certified Swiss posting assumption, UK employer NIC is zero.
    # Swiss pay includes the UK tax once and excludes qualifying moving expenses.
    swiss_assessable_benefits = (
        benefits["housing"].cost_gbp
        + benefits["relocation_allowance"].cost_gbp
        + benefits["temporary_housing"].cost_gbp
    )
    swiss_wage = (
        swiss_cash_wage_chf + (uk_tax + swiss_assessable_benefits) * chf_per_gbp
    )
    contributions = swiss_contributions(swiss_wage)
    family_allowance = (
        swiss_wage * FAMILY_ALLOWANCE_RATE
        if contributions.ahv_iv_eo_chf
        else Decimal(0)
    )
    admin_charge = 2 * contributions.ahv_iv_eo_chf * ADMINISTRATION_RATE
    employer_charges = contributions.total_chf + family_allowance + admin_charge

    return AnnualCost(
        benefits=benefits,
        taxable_benefits_gbp=taxable_benefits,
        uk_pay_before_tax_gbp=uk_pay_before_tax,
        uk_tax_before_gross_up_gbp=uk_income_tax(uk_pay_before_tax),
        uk_tax_gbp=uk_tax,
        swiss_assessable_pay_chf=swiss_wage,
        swiss_contributions=contributions,
        swiss_family_allowance_chf=family_allowance,
        swiss_admin_charge_chf=admin_charge,
        total_gbp=net_home_pay_gbp
        + benefit_cost
        + uk_tax
        + employer_charges / chf_per_gbp,
    )
