from decimal import Decimal
from unittest import TestCase

from estimator.swiss import (
    federal_income_tax,
    hypothetical_home_deductions,
    swiss_contributions,
    zurich_basic_tax,
)


class SwissTaxTests(TestCase):
    def test_pack_home_deductions(self):
        result = hypothetical_home_deductions(Decimal("170000"))
        self.assertEqual(result.taxable_income_chf, Decimal("155300"))
        self.assertEqual(result.work_expenses_chf, Decimal("4000"))
        self.assertEqual(result.federal_tax_chf, Decimal("7659"))
        self.assertEqual(result.cantonal_tax_chf, Decimal("11123"))
        self.assertEqual(result.city_tax_chf, Decimal("13933"))
        self.assertEqual(result.income_tax_chf, Decimal("32715"))
        self.assertEqual(result.contributions.total_chf, Decimal("10640.20"))

    def test_federal_tariff_thresholds(self):
        for income, tax in (
            ("18499.99", "0"),
            ("18500", "25.41"),
            ("43500", "229.20"),
            ("100000", "2684.35"),
            ("155359.80", "7658.55"),
            ("793900", "91298.15"),
            ("794000", "91310.00"),
            ("794100", "91321.50"),
        ):
            with self.subTest(income=income):
                self.assertEqual(federal_income_tax(Decimal(income)), Decimal(tax))

    def test_zurich_tariff_boundaries(self):
        self.assertEqual(zurich_basic_tax(Decimal("7099.99")), Decimal("0"))
        self.assertEqual(zurich_basic_tax(Decimal("7100")), Decimal("2"))
        self.assertEqual(zurich_basic_tax(Decimal("100000")), Decimal("6170"))
        self.assertEqual(
            zurich_basic_tax(Decimal("266800")) - zurich_basic_tax(Decimal("266700")),
            Decimal("13"),
        )

    def test_unemployment_contributions_stop_at_annual_ceiling(self):
        below = swiss_contributions(Decimal("148100"))
        at_cap = swiss_contributions(Decimal("148200"))
        above = swiss_contributions(Decimal("148300"))
        self.assertEqual(below.alv_chf, Decimal("1629.10"))
        self.assertEqual(at_cap.alv_chf, Decimal("1630.20"))
        self.assertEqual(above.alv_chf, at_cap.alv_chf)
        self.assertEqual(above.ahv_iv_eo_chf - at_cap.ahv_iv_eo_chf, Decimal("5.30"))

    def test_small_ordinary_wage_without_contribution_request(self):
        self.assertEqual(swiss_contributions(Decimal("2500")).total_chf, Decimal("0"))
        self.assertGreater(swiss_contributions(Decimal("2501")).total_chf, Decimal("0"))
