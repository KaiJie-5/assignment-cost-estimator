from unittest.mock import patch

from django.test import Client, SimpleTestCase, override_settings
from django.urls import reverse

from estimator.tests.pack_case import PACK_FORM_DATA


class IndexTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("estimator:index")

    def test_renders_both_tabs_and_pinned_bootstrap(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'id="cost-tab"')
        self.assertContains(response, 'id="immigration-tab"')
        self.assertContains(response, "bootstrap@5.3.9")
        self.assertContains(
            response, "https://www.gov.uk/uk-border-control/before-you-leave-for-the-uk"
        )
        self.assertContains(response, "Load Pack Test Case")
        self.assertContains(response, 'name="monthly_housing_gbp"')

    def test_valid_form_renders_estimate_with_csrf_enforced(self):
        client = Client(enforce_csrf_checks=True)
        client.get(self.url)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.url, {**PACK_FORM_DATA, "csrfmiddlewaretoken": token}
        )
        self.assertContains(response, "£288,656.36")
        self.assertContains(response, "£267,861.57")
        self.assertContains(response, "£556,517.92")
        self.assertContains(response, "1.8005×")
        self.assertContains(response, "Taxable benefit in kind · £2,000.00")
        self.assertContains(
            response, "https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye72028"
        )

    def test_zero_pay_renders_without_a_multiple(self):
        response = self.client.post(
            self.url, {**PACK_FORM_DATA, "salary_chf": "0", "bonus_chf": "0"}
        )
        self.assertContains(response, "Total employer cost")
        self.assertIsNone(
            response.context["report"]["summary"]["total"]["home_pay_multiple"]
        )

    def test_invalid_fx_has_a_readable_error_beside_the_field(self):
        response = self.client.post(self.url, {**PACK_FORM_DATA, "chf_per_gbp": "0"})
        self.assertContains(response, "Check the fields below.", status_code=400)
        self.assertContains(response, 'class="alert alert-danger"', status_code=400)
        self.assertContains(
            response, 'class="form-control is-invalid"', status_code=400
        )
        self.assertContains(response, 'id="id_chf_per_gbp_error"', status_code=400)
        self.assertContains(
            response,
            'aria-describedby="id_chf_per_gbp_helptext id_chf_per_gbp_error"',
            status_code=400,
        )
        self.assertNotContains(response, 'id="estimate-result"', status_code=400)

    @override_settings(DEBUG=False)
    def test_unexpected_browser_error_has_a_generic_message(self):
        client = Client(raise_request_exception=False)
        with patch(
            "estimator.views.cost_report", side_effect=RuntimeError("private detail")
        ):
            response = client.post(self.url, PACK_FORM_DATA)
        self.assertContains(
            response, "Something went wrong. Please try again.", status_code=500
        )
        self.assertNotContains(response, "private detail", status_code=500)
