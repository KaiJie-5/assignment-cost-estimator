from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

AHV_IV_EO_RATE = Decimal("0.053")
ALV_RATE = Decimal("0.011")
ALV_CEILING_CHF = 148_200

# Official 2026 single tariff: lower limit, base tax, tax per additional CHF 100.
FEDERAL_BANDS = (
    (15_200, Decimal("0"), Decimal("0.77")),
    (33_200, Decimal("138.60"), Decimal("0.88")),
    (43_500, Decimal("229.20"), Decimal("2.64")),
    (58_000, Decimal("612.00"), Decimal("2.97")),
    (76_200, Decimal("1152.50"), Decimal("5.94")),
    (82_100, Decimal("1502.95"), Decimal("6.60")),
    (108_900, Decimal("3271.75"), Decimal("8.80")),
    (141_500, Decimal("6140.55"), Decimal("11.00")),
    (185_100, Decimal("10936.55"), Decimal("13.20")),
    (794_000, Decimal("91310.00"), Decimal("11.50")),
)

# Zurich's basic tariff for a single taxpayer, before either multiplier.
ZURICH_BANDS = (
    (7_000, Decimal("0")),
    (12_000, Decimal("0.02")),
    (16_800, Decimal("0.03")),
    (24_800, Decimal("0.04")),
    (34_500, Decimal("0.05")),
    (45_700, Decimal("0.06")),
    (58_800, Decimal("0.07")),
    (76_400, Decimal("0.08")),
    (110_400, Decimal("0.09")),
    (144_100, Decimal("0.10")),
    (197_400, Decimal("0.11")),
    (266_700, Decimal("0.12")),
)


@dataclass(frozen=True)
class SwissContributions:
    ahv_iv_eo_chf: Decimal
    alv_chf: Decimal

    @property
    def total_chf(self) -> Decimal:
        return self.ahv_iv_eo_chf + self.alv_chf


@dataclass(frozen=True)
class SwissHomeDeductions:
    work_expenses_chf: Decimal
    taxable_income_chf: Decimal
    federal_tax_chf: Decimal
    cantonal_tax_chf: Decimal
    city_tax_chf: Decimal
    contributions: SwissContributions

    @property
    def income_tax_chf(self) -> Decimal:
        return self.federal_tax_chf + self.cantonal_tax_chf + self.city_tax_chf


def swiss_contributions(wage_chf: Decimal) -> SwissContributions:
    """Calculate one share of contributions for ordinary full-year employment."""
    if wage_chf <= 2_500:
        return SwissContributions(Decimal(0), Decimal(0))
    return SwissContributions(
        wage_chf * AHV_IV_EO_RATE,
        min(wage_chf, ALV_CEILING_CHF) * ALV_RATE,
    )


def federal_income_tax(taxable_income_chf: Decimal) -> Decimal:
    income = taxable_income_chf // 100 * 100
    for lower, base_tax, per_hundred in reversed(FEDERAL_BANDS):
        if income >= lower:
            tax = base_tax + (income - lower) / 100 * per_hundred
            return tax if tax >= 25 else Decimal(0)
    return Decimal(0)


def zurich_basic_tax(taxable_income_chf: Decimal) -> Decimal:
    income = taxable_income_chf // 100 * 100
    tax = Decimal(0)
    lower = 0
    for upper, rate in ZURICH_BANDS:
        tax += (min(income, upper) - lower) * rate
        if income <= upper:
            return tax
        lower = upper
    return tax + (income - lower) * Decimal("0.13")


def hypothetical_home_deductions(gross_pay_chf: Decimal) -> SwissHomeDeductions:
    contributions = swiss_contributions(gross_pay_chf)
    net_pay = gross_pay_chf - contributions.total_chf
    work_expenses = min(net_pay, 4_000, max(2_000, net_pay * Decimal("0.03")))
    taxable_income = net_pay - work_expenses
    simple_tax = zurich_basic_tax(taxable_income)

    # Use the Swiss calculator's convention of rounding each tax line to whole CHF.
    return SwissHomeDeductions(
        work_expenses_chf=Decimal(work_expenses),
        taxable_income_chf=taxable_income // 100 * 100,
        federal_tax_chf=federal_income_tax(taxable_income).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        ),
        cantonal_tax_chf=(simple_tax * Decimal("0.95")).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        ),
        city_tax_chf=(simple_tax * Decimal("1.19")).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        ),
        contributions=contributions,
    )
