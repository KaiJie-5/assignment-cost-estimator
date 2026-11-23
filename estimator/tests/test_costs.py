from decimal import Decimal
from unittest import TestCase

from estimator.cost_report import cost_report
from estimator.costs import estimate_assignment_cost
from estimator.money import round_money
from estimator.tests.pack_case import PACK_AMOUNTS


class AssignmentCostTests(TestCase):
    def setUp(self):
        self.amounts = {name: Decimal(amount) for name, amount in PACK_AMOUNTS.items()}

    def test_pack_costs_by_year_and_total(self):
        estimate = estimate_assignment_cost(**self.amounts, housing_relief=False)
        report = cost_report(estimate)
        summary = report["summary"]
        self.assertEqual(summary["year_one"]["cost_gbp"], Decimal("288656.36"))
        self.assertEqual(summary["year_two"]["cost_gbp"], Decimal("267861.57"))
        self.assertEqual(summary["total"]["cost_gbp"], Decimal("556517.92"))
        self.assertEqual(summary["total"]["home_pay_multiple"], Decimal("1.8005"))
        self.assertEqual(round_money(estimate.net_home_pay_gbp), Decimal("115131.64"))

    def test_year_one_benefits_and_swiss_wage_base(self):
        estimate = estimate_assignment_cost(**self.amounts, housing_relief=False)
        year_one, year_two = estimate.year_one, estimate.year_two
        self.assertEqual(
            round_money(year_one.swiss_assessable_pay_chf), Decimal("300600.38")
        )
        self.assertEqual(
            round_money(year_two.swiss_assessable_pay_chf), Decimal("285309.47")
        )
        self.assertEqual(
            round_money(year_one.swiss_family_allowance_chf), Decimal("3081.15")
        )
        self.assertEqual(
            round_money(year_one.swiss_admin_charge_chf), Decimal("318.64")
        )
        self.assertEqual(
            round_money(year_one.taxable_benefits_gbp), Decimal("42545.45")
        )
        self.assertEqual(year_two.taxable_benefits_gbp, Decimal("36000"))
        for name in ("relocation_allowance", "moving_costs", "temporary_housing"):
            self.assertEqual(year_two.benefits[name].cost_gbp, Decimal(0))

    def test_housing_relief_changes_uk_tax_and_swiss_charges(self):
        estimate = estimate_assignment_cost(**self.amounts, housing_relief=True)
        self.assertEqual(round_money(estimate.total_gbp), Decimal("493820.39"))
        self.assertEqual(
            estimate.year_one.benefits["housing"].cost_gbp, Decimal("36000")
        )
        self.assertEqual(estimate.year_one.benefits["housing"].taxable_gbp, Decimal(0))

    def test_zero_gross_home_pay_has_no_cost_multiple(self):
        self.amounts.update(salary_chf=Decimal(0), bonus_chf=Decimal(0))
        estimate = estimate_assignment_cost(**self.amounts, housing_relief=False)
        report = cost_report(estimate)
        self.assertGreater(report["summary"]["total"]["cost_gbp"], 0)
        self.assertIsNone(report["summary"]["total"]["home_pay_multiple"])

    def test_report_has_four_sections_and_cites_split_treatment(self):
        estimate = estimate_assignment_cost(**self.amounts, housing_relief=False)
        report = cost_report(estimate)
        self.assertEqual(
            [section["label"] for section in report["sections"]],
            [
                "Home pay",
                "Assignment benefits",
                "Host tax and employer charges",
                "Deductions",
            ],
        )
        temporary_housing = report["sections"][1]["rows"][3]
        self.assertEqual(temporary_housing["year_one"], Decimal("4000.00"))
        self.assertEqual(
            temporary_housing["treatments"],
            [
                {"label": "Taxable benefit in kind", "amount_gbp": Decimal("2000.00")},
                {"label": "UK exempt", "amount_gbp": Decimal("2000.00")},
            ],
        )
        self.assertTrue(temporary_housing["sources"])
