from decimal import ROUND_HALF_UP, Decimal


def round_money(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_home_pay_gbp(
    salary_chf: Decimal, bonus_chf: Decimal, chf_per_gbp: Decimal
) -> Decimal:
    """Convert one year of gross home pay and round the result to pennies."""
    gross_pay_chf = salary_chf + bonus_chf
    return round_money(gross_pay_chf / chf_per_gbp)
