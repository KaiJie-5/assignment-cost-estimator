from django.test import Client, SimpleTestCase
from django.urls import reverse


class IndexTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("estimator:index")
        self.inputs = {
            "home_country": "CH",
            "host_country": "GB",
            "salary_chf": "150000.00",
            "bonus_chf": "20000.00",
            "chf_per_gbp": "1.10",
        }

    def test_renders_both_tabs_and_pinned_bootstrap(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'id="cost-tab"')
        self.assertContains(response, 'id="immigration-tab"')
        self.assertContains(response, "bootstrap@5.3.9")
        self.assertContains(
            response, "https://www.gov.uk/uk-border-control/before-you-leave-for-the-uk"
        )

    def test_valid_form_renders_home_pay_with_csrf_enforced(self):
        client = Client(enforce_csrf_checks=True)
        client.get(self.url)
        token = client.cookies["csrftoken"].value
        response = client.post(self.url, {**self.inputs, "csrfmiddlewaretoken": token})
        self.assertContains(response, "£154,545.45")

    def test_zero_pay_can_be_displayed(self):
        response = self.client.post(
            self.url, {**self.inputs, "salary_chf": "0", "bonus_chf": "0"}
        )
        self.assertContains(response, "£0.00")

    def test_invalid_fx_has_a_readable_error_beside_the_field(self):
        response = self.client.post(self.url, {**self.inputs, "chf_per_gbp": "0"})
        self.assertContains(response, "Check the fields below.", status_code=400)
        self.assertContains(response, 'id="id_chf_per_gbp_error"', status_code=400)
