from dataclasses import dataclass
from decimal import Decimal

PERSONAL_ALLOWANCE_GBP = 12_570
TAPER_START_GBP = 100_000
BASIC_BAND_GBP = 37_700
ADDITIONAL_RATE_START_GBP = 125_140
RELOCATION_CAP_GBP = 8_000


@dataclass(frozen=True)
class Benefit:
    cost_gbp: Decimal
    taxable_gbp: Decimal


def classify_benefits(
    *,
    housing_gbp: Decimal,
    relocation_allowance_gbp: Decimal,
    moving_costs_gbp: Decimal,
    temporary_housing_gbp: Decimal,
    housing_relief: bool,
) -> dict[str, Benefit]:
    """Apply the shared relocation cap to qualifying employer-paid expenses."""
    exempt_moving = min(moving_costs_gbp, RELOCATION_CAP_GBP)
    exempt_temporary = min(temporary_housing_gbp, RELOCATION_CAP_GBP - exempt_moving)
    return {
        "housing": Benefit(housing_gbp, Decimal(0) if housing_relief else housing_gbp),
        "relocation_allowance": Benefit(
            relocation_allowance_gbp, relocation_allowance_gbp
        ),
        "moving_costs": Benefit(moving_costs_gbp, moving_costs_gbp - exempt_moving),
        "temporary_housing": Benefit(
            temporary_housing_gbp, temporary_housing_gbp - exempt_temporary
        ),
    }


def uk_income_tax(income_gbp: Decimal) -> Decimal:
    """Income tax on employment income in England using 2026/27 rates."""
    allowance_reduction = max(income_gbp - TAPER_START_GBP, 0) / Decimal(2)
    allowance = max(PERSONAL_ALLOWANCE_GBP - allowance_reduction, 0)
    taxable = max(income_gbp - allowance, 0)
    basic = min(taxable, BASIC_BAND_GBP) * Decimal("0.20")
    higher = max(min(taxable, ADDITIONAL_RATE_START_GBP) - BASIC_BAND_GBP, 0) * Decimal(
        "0.40"
    )
    additional = max(taxable - ADDITIONAL_RATE_START_GBP, 0) * Decimal("0.45")
    return basic + higher + additional


def gross_up_uk_tax(pay_before_tax_gbp: Decimal) -> Decimal:
    """Solve tax = UK income tax on pay plus employer-paid tax."""
    tax = Decimal(0)
    for _ in range(200):
        next_tax = uk_income_tax(pay_before_tax_gbp + tax)
        if next_tax == tax:
            return tax
        tax = next_tax
    raise RuntimeError("UK tax gross-up did not converge.")
