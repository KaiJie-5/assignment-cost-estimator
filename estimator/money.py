from decimal import ROUND_HALF_UP, Decimal


def calculate_home_pay_gbp(
    salary_chf: Decimal, bonus_chf: Decimal, chf_per_gbp: Decimal
) -> Decimal:
    """Convert one year of gross home pay and round the result to pennies."""
    gross_pay_chf = salary_chf + bonus_chf
    return (gross_pay_chf / chf_per_gbp).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
