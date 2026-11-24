from decimal import ROUND_HALF_UP, Decimal

from . import sources
from .costs import AssignmentCost
from .money import round_money
from .uk import Benefit


def cost_report(estimate: AssignmentCost) -> dict:
    """Build the report shared by the page and the JSON API."""
    gross_pay = estimate.gross_home_pay_chf / estimate.chf_per_gbp
    return {
        "summary": {
            "year_one": _summary("Year 1", estimate.year_one.total_gbp, gross_pay),
            "year_two": _summary("Year 2", estimate.year_two.total_gbp, gross_pay),
            "total": _summary("Both years", estimate.total_gbp, 2 * gross_pay),
        },
        "sections": _cost_sections(estimate),
        "workings": _workings(estimate),
        "assumptions": _assumptions(estimate.housing_relief),
    }


def _summary(label: str, total: Decimal, gross_pay: Decimal) -> dict:
    multiple = (
        (total / gross_pay).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        if gross_pay
        else None
    )
    return {
        "label": label,
        "cost_gbp": round_money(total),
        "home_pay_multiple": multiple,
    }


def _row(
    label: str,
    year_one: Decimal,
    year_two: Decimal,
    *references: tuple[str, str],
    currency: str = "GBP",
) -> dict:
    return {
        "label": label,
        "year_one": round_money(year_one),
        "year_two": round_money(year_two),
        "total": round_money(year_one + year_two),
        "currency": currency,
        "sources": references,
    }


def _benefit_row(
    label: str,
    one: Benefit,
    two: Benefit,
    taxable_label: str,
    *references: tuple[str, str],
) -> dict:
    row = _row(label, one.cost_gbp, two.cost_gbp, *references)
    exempt = one.cost_gbp - one.taxable_gbp
    split = bool(one.taxable_gbp and exempt)
    treatments = []
    if one.taxable_gbp:
        treatments.append(
            {
                "label": taxable_label,
                "amount_gbp": round_money(one.taxable_gbp) if split else None,
            }
        )
    if exempt:
        treatments.append(
            {
                "label": "UK exempt",
                "amount_gbp": round_money(exempt) if split else None,
            }
        )
    row["treatments"] = treatments
    return row


def _cost_sections(estimate: AssignmentCost) -> tuple[dict, ...]:
    one, two = estimate.year_one, estimate.year_two
    fx = estimate.chf_per_gbp
    salary, bonus = estimate.salary_chf / fx, estimate.bonus_chf / fx
    swiss_tax = -estimate.home_deductions.income_tax_chf / fx
    swiss_social = -estimate.home_deductions.contributions.total_chf / fx
    one_benefits, two_benefits = one.benefits, two.benefits
    housing_source = (
        sources.UK_WORKPLACE_RELIEF if estimate.housing_relief else sources.UK_HOUSING
    )
    return (
        {
            "label": "Home pay",
            "rows": (
                _row("Annual salary", salary, salary),
                _row("Annual bonus", bonus, bonus),
            ),
        },
        {
            "label": "Assignment benefits",
            "rows": (
                _benefit_row(
                    "London rent",
                    one_benefits["housing"],
                    two_benefits["housing"],
                    "Taxable benefit in kind",
                    housing_source,
                ),
                _benefit_row(
                    "Cash relocation allowance",
                    one_benefits["relocation_allowance"],
                    two_benefits["relocation_allowance"],
                    "Taxable cash",
                    sources.UK_CASH_ALLOWANCE,
                ),
                _benefit_row(
                    "Moving costs",
                    one_benefits["moving_costs"],
                    two_benefits["moving_costs"],
                    "Taxable benefit in kind",
                    sources.UK_RELOCATION_CAP,
                ),
                _benefit_row(
                    "Temporary housing",
                    one_benefits["temporary_housing"],
                    two_benefits["temporary_housing"],
                    "Taxable benefit in kind",
                    sources.UK_TEMPORARY_HOUSING,
                    sources.UK_RELOCATION_CAP,
                ),
            ),
        },
        {
            "label": "Host tax and employer charges",
            "rows": (
                _row(
                    "UK income tax including tax on tax",
                    one.uk_tax_gbp,
                    two.uk_tax_gbp,
                    sources.UK_TAX,
                    sources.UK_GROSS_UP,
                ),
                _row(
                    "UK employer National Insurance",
                    Decimal(0),
                    Decimal(0),
                    sources.UK_NIC,
                ),
                _row(
                    "Swiss employer AHV/IV/EO",
                    one.swiss_contributions.ahv_iv_eo_chf / fx,
                    two.swiss_contributions.ahv_iv_eo_chf / fx,
                    sources.SWISS_CONTRIBUTIONS,
                ),
                _row(
                    "Swiss employer unemployment insurance (ALV)",
                    one.swiss_contributions.alv_chf / fx,
                    two.swiss_contributions.alv_chf / fx,
                    sources.SWISS_CONTRIBUTIONS,
                ),
                _row(
                    "Swiss family allowance fund (FAK)",
                    one.swiss_family_allowance_chf / fx,
                    two.swiss_family_allowance_chf / fx,
                    sources.SWISS_CONTRIBUTIONS,
                ),
                _row(
                    "Swiss administration fee",
                    one.swiss_admin_charge_chf / fx,
                    two.swiss_admin_charge_chf / fx,
                    sources.SWISS_ADMIN,
                ),
            ),
        },
        {
            "label": "Deductions",
            "rows": (
                _row(
                    "Hypothetical Swiss income tax",
                    swiss_tax,
                    swiss_tax,
                    sources.TAX_EQUALISATION,
                    sources.SWISS_CALCULATOR,
                ),
                _row(
                    "Hypothetical Swiss employee social security",
                    swiss_social,
                    swiss_social,
                    sources.SWISS_CONTRIBUTIONS,
                ),
            ),
        },
    )


def _workings(estimate: AssignmentCost) -> tuple[dict, ...]:
    one, two = estimate.year_one, estimate.year_two
    home = estimate.home_deductions
    return (
        _row(
            "Gross home pay",
            estimate.gross_home_pay_chf,
            estimate.gross_home_pay_chf,
            currency="CHF",
        ),
        _row(
            "Swiss work expenses deduction",
            home.work_expenses_chf,
            home.work_expenses_chf,
            sources.SWISS_FEDERAL_TAX,
            sources.ZURICH_DEDUCTIONS,
            currency="CHF",
        ),
        _row(
            "Swiss taxable income after tariff rounding",
            home.taxable_income_chf,
            home.taxable_income_chf,
            sources.SWISS_FEDERAL_TAX,
            sources.ZURICH_TARIFF,
            currency="CHF",
        ),
        _row(
            "Swiss federal income tax",
            home.federal_tax_chf,
            home.federal_tax_chf,
            sources.SWISS_FEDERAL_TAX,
            currency="CHF",
        ),
        _row(
            "Zurich cantonal income tax",
            home.cantonal_tax_chf,
            home.cantonal_tax_chf,
            sources.ZURICH_TARIFF,
            sources.ZURICH_CANTON,
            currency="CHF",
        ),
        _row(
            "Zurich city income tax",
            home.city_tax_chf,
            home.city_tax_chf,
            sources.ZURICH_TARIFF,
            sources.ZURICH_CITY,
            currency="CHF",
        ),
        _row(
            "Net home pay after hypothetical deductions",
            estimate.net_home_pay_gbp,
            estimate.net_home_pay_gbp,
            sources.TAX_EQUALISATION,
        ),
        _row(
            "UK-taxable benefits",
            one.taxable_benefits_gbp,
            two.taxable_benefits_gbp,
            sources.UK_RELOCATION_CAP,
        ),
        _row(
            "UK taxable pay before gross-up",
            one.uk_pay_before_tax_gbp,
            two.uk_pay_before_tax_gbp,
            sources.UK_TAX,
        ),
        _row(
            "UK income tax before gross-up",
            one.uk_tax_before_gross_up_gbp,
            two.uk_tax_before_gross_up_gbp,
            sources.UK_TAX,
            sources.UK_ALLOWANCE,
        ),
        _row(
            "Tax on tax",
            one.uk_tax_gbp - one.uk_tax_before_gross_up_gbp,
            two.uk_tax_gbp - two.uk_tax_before_gross_up_gbp,
            sources.UK_GROSS_UP,
        ),
        _row(
            "Swiss pay subject to employer contributions",
            one.swiss_assessable_pay_chf,
            two.swiss_assessable_pay_chf,
            sources.SWISS_WAGE,
            currency="CHF",
        ),
    )


def _assumptions(housing_relief: bool):
    rent_treatment = (
        "The London rent qualifies for UK temporary workplace relief. The employer still pays the full rent "
        "and includes it in pay for Swiss social security."
        if housing_relief
        else "London rent is a taxable benefit in kind. The employer holds the lease and pays the rent directly. "
        "The model uses the rent as the taxable value."
    )
    return (
        (
            "Both years use 2026/27 income tax rates for England. The employee is a UK tax resident. "
            "The Personal Allowance falls by £1 for every £2 of adjusted net income above £100,000.",
            (sources.UK_TAX, sources.UK_ALLOWANCE),
        ),
        (
            "Home tax uses 2026 rates for a single Zurich resident with no children. The model deducts Swiss "
            "social security and work expenses, assumes no church tax, and rounds each tax to whole francs.",
            (
                sources.SWISS_FEDERAL_TAX,
                sources.ZURICH_DEDUCTIONS,
                sources.SWISS_CALCULATOR,
            ),
        ),
        (
            rent_treatment,
            (sources.UK_WORKPLACE_RELIEF if housing_relief else sources.UK_HOUSING,),
        ),
        (
            "The model assumes the move and serviced apartment qualify for one £8,000 relocation exemption. "
            "Moving costs use it first. The cash allowance is taxable.",
            (
                sources.UK_RELOCATION_CAP,
                sources.UK_TEMPORARY_HOUSING,
                sources.UK_CASH_ALLOWANCE,
            ),
        ),
        (
            "The estimate assumes a Swiss certificate of coverage for both years. Article 14 allows "
            "Swiss coverage for up to 24 months when the employer normally operates in Switzerland, sends the "
            "employee to work on its behalf, and the employee does not replace another posted worker. "
            "UK employer National Insurance is £0 for the period on the certificate.",
            (sources.SWISS_POSTING, sources.UK_NIC),
        ),
        (
            "Pay for Swiss contributions starts with gross home pay less the Swiss income tax deduction. "
            "It includes UK tax paid by the employer, the cash relocation allowance and both housing costs. "
            "The model treats documented moving costs as expenses.",
            (sources.SWISS_WAGE, sources.SWISS_CONTRIBUTIONS),
        ),
        (
            "The employer and employee each pay 5.30% for AHV/IV/EO on the full pay. Unemployment insurance "
            "is 1.10% each on pay up to CHF 148,200. For pay of CHF 2,500 or less from an employer, the model "
            "assumes the worker does not ask to contribute. The employer uses SVA Zürich's 1.025% family allowance rate.",
            (sources.SWISS_CONTRIBUTIONS,),
        ),
        (
            "The administration fee is 1.00% of the employee and employer AHV/IV/EO payments together. "
            "The model assumes on-time filing through AHVeasy and total contributions for the employer "
            "of at least CHF 22,500 and under CHF 50,000.",
            (sources.SWISS_CONTRIBUTIONS, sources.SWISS_ADMIN),
        ),
        (
            "Employer pension, accident insurance and immigration fees are outside this estimate.",
            (),
        ),
    )
