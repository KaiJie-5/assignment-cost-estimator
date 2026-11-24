from decimal import Decimal

VISA_FEE = 819
ANNUAL_HEALTH_SURCHARGE = Decimal("1035")
CERTIFICATE_FEE = 525


def _sponsor_fees(
    licence_fee: int, first_year: int, next_six_months: int
) -> dict[str, int]:
    """Use the first year and two further six-month periods of the CoS."""
    skills_charge = first_year + 2 * next_six_months
    existing_licence = CERTIFICATE_FEE + skills_charge
    return {
        "licence_fee": licence_fee,
        "skills_charge": skills_charge,
        "existing_licence_total": existing_licence,
        "new_licence_total": existing_licence + licence_fee,
    }


HEALTH_SURCHARGE_TWO_YEARS = 2 * ANNUAL_HEALTH_SURCHARGE
HEALTH_SURCHARGE_WITH_EXTRA_TIME = (
    HEALTH_SURCHARGE_TWO_YEARS + ANNUAL_HEALTH_SURCHARGE / 2
)

IMMIGRATION_FEES = {
    "visa": VISA_FEE,
    "eta": 20,
    "annual_health_surcharge": ANNUAL_HEALTH_SURCHARGE,
    "health_surcharge_two_years": HEALTH_SURCHARGE_TWO_YEARS,
    "health_surcharge_with_extra_time": HEALTH_SURCHARGE_WITH_EXTRA_TIME,
    "visa_total_two_years": VISA_FEE + HEALTH_SURCHARGE_TWO_YEARS,
    "visa_total_with_extra_time": VISA_FEE + HEALTH_SURCHARGE_WITH_EXTRA_TIME,
    "certificate": CERTIFICATE_FEE,
    "small": _sponsor_fees(licence_fee=611, first_year=480, next_six_months=240),
    "large": _sponsor_fees(licence_fee=1682, first_year=1320, next_six_months=660),
}
