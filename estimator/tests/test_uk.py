from decimal import Decimal
from unittest import TestCase

from estimator.uk import classify_benefits, gross_up_uk_tax, uk_income_tax


class UKTaxTests(TestCase):
    def test_allowance_and_progressive_bands(self):
        for income, tax in (
            ("12570", "0"),
            ("50270", "7540"),
            ("100000", "27432"),
            ("110000", "33432"),
            ("125140", "42516"),
            ("125141", "42516.45"),
        ):
            with self.subTest(income=income):
                self.assertEqual(uk_income_tax(Decimal(income)), Decimal(tax))

    def test_gross_up_can_end_in_allowance_taper(self):
        pay = Decimal("76000")
        tax = gross_up_uk_tax(pay)
        self.assertEqual(tax.quantize(Decimal("0.01")), Decimal("32580.00"))
        self.assertEqual(tax, uk_income_tax(pay + tax))

    def test_pack_gross_up_with_and_without_housing_relief(self):
        net_pay = Decimal("126644.80") / Decimal("1.10")
        for housing_relief, year_one_tax, year_two_tax in (
            (False, "103923.07", "98567.70"),
            (True, "74468.53", "69113.16"),
        ):
            with self.subTest(housing_relief=housing_relief):
                housing = Decimal(0 if housing_relief else 36000)
                year_one_pay = (
                    net_pay + Decimal("5000") / Decimal("1.10") + housing + 2000
                )
                year_two_pay = net_pay + housing
                self.assertEqual(
                    gross_up_uk_tax(year_one_pay).quantize(Decimal("0.01")),
                    Decimal(year_one_tax),
                )
                self.assertEqual(
                    gross_up_uk_tax(year_two_pay).quantize(Decimal("0.01")),
                    Decimal(year_two_tax),
                )


class BenefitTests(TestCase):
    def test_pack_shares_one_relocation_cap_and_charges_full_cost(self):
        benefits = classify_benefits(
            housing_gbp=Decimal("36000"),
            relocation_allowance_gbp=Decimal("4545.45"),
            moving_costs_gbp=Decimal("6000"),
            temporary_housing_gbp=Decimal("4000"),
            housing_relief=False,
        )
        self.assertEqual(benefits["housing"].taxable_gbp, Decimal("36000"))
        self.assertEqual(
            benefits["relocation_allowance"].taxable_gbp, Decimal("4545.45")
        )
        self.assertEqual(benefits["moving_costs"].taxable_gbp, Decimal("0"))
        self.assertEqual(benefits["temporary_housing"].taxable_gbp, Decimal("2000"))
        self.assertEqual(
            sum(item.cost_gbp for item in benefits.values()), Decimal("50545.45")
        )

    def test_moving_costs_can_use_entire_cap_and_relief_only_changes_rent_tax(self):
        benefits = classify_benefits(
            housing_gbp=Decimal("36000"),
            relocation_allowance_gbp=Decimal("1000"),
            moving_costs_gbp=Decimal("8200"),
            temporary_housing_gbp=Decimal("500"),
            housing_relief=True,
        )
        self.assertEqual(benefits["housing"].cost_gbp, Decimal("36000"))
        self.assertEqual(benefits["housing"].taxable_gbp, Decimal("0"))
        self.assertEqual(benefits["relocation_allowance"].taxable_gbp, Decimal("1000"))
        self.assertEqual(benefits["moving_costs"].taxable_gbp, Decimal("200"))
        self.assertEqual(benefits["temporary_housing"].taxable_gbp, Decimal("500"))
