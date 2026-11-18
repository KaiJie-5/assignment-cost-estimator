from decimal import Decimal
from unittest import TestCase

from estimator.money import calculate_home_pay_gbp


class HomePayTests(TestCase):
    def test_converts_pack_salary_and_bonus(self):
        result = calculate_home_pay_gbp(
            Decimal("150000"), Decimal("20000"), Decimal("1.10")
        )
        self.assertEqual(result, Decimal("154545.45"))

    def test_rounds_half_a_penny_up_for_display(self):
        result = calculate_home_pay_gbp(Decimal("0.01"), Decimal("0"), Decimal("2"))
        self.assertEqual(result, Decimal("0.01"))
