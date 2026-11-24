from decimal import Decimal

from django.test import SimpleTestCase
from django.urls import reverse

from estimator.immigration import IMMIGRATION_FEES


class ImmigrationTests(SimpleTestCase):
    def test_sponsor_fees_by_size_and_licence(self):
        for size, skills_charge, existing, new in (
            ("small", 960, 1485, 2096),
            ("large", 2640, 3165, 4847),
        ):
            with self.subTest(size=size):
                fees = IMMIGRATION_FEES[size]
                self.assertEqual(fees["skills_charge"], skills_charge)
                self.assertEqual(fees["existing_licence_total"], existing)
                self.assertEqual(fees["new_licence_total"], new)

    def test_visa_fees_with_exact_or_longer_permission(self):
        self.assertEqual(
            IMMIGRATION_FEES["health_surcharge_two_years"], Decimal("2070")
        )
        self.assertEqual(
            IMMIGRATION_FEES["health_surcharge_with_extra_time"], Decimal("2587.50")
        )
        self.assertEqual(IMMIGRATION_FEES["visa_total_two_years"], Decimal("2889"))
        self.assertEqual(
            IMMIGRATION_FEES["visa_total_with_extra_time"], Decimal("3406.50")
        )

    def test_tab_answers_the_pack_case_and_links_to_official_rules(self):
        response = self.client.get(reverse("estimator:index"))
        for text in (
            "Global Business Mobility Senior or Specialist Worker visa",
            "£52,500",
            "£73,900",
            "Standard Visitor",
            'href="https://www.gov.uk/eta/apply"',
            "Use a Swiss passport valid throughout each stay.",
            'href="https://www.gov.uk/evisa/update-ukvi-account"',
            "Check permission to work before the start date.",
            'href="https://www.gov.uk/check-job-applicant-right-to-work"',
            "Usually three weeks",
        ):
            with self.subTest(text=text):
                self.assertContains(response, text)

    def test_tab_shows_all_fee_scenarios(self):
        response = self.client.get(reverse("estimator:index"))
        for amount in (
            "20",
            "819",
            "2,889",
            "3,406.50",
            "1,485",
            "2,096",
            "3,165",
            "4,847",
        ):
            with self.subTest(amount=amount):
                self.assertContains(response, f"£{amount}<")
