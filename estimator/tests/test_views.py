from django.test import Client, SimpleTestCase
from django.urls import reverse


class HealthTests(SimpleTestCase):
    def test_health_returns_ok(self):
        response = self.client.get(reverse("estimator:health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class HomePayApiTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("estimator:home_pay")
        self.inputs = {
            "home_country": "CH",
            "host_country": "GB",
            "salary_chf": "150000.00",
            "bonus_chf": "20000.00",
            "chf_per_gbp": "1.10",
        }

    def test_pack_inputs_return_pennies_as_a_string(self):
        response = self.client.post(self.url, self.inputs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"gross_home_pay_gbp": "154545.45"})

    def test_bad_inputs_return_field_errors(self):
        response = self.client.post(
            self.url,
            {
                "home_country": "US",
                "host_country": "GB",
                "salary_chf": "NaN",
                "bonus_chf": "-1",
                "chf_per_gbp": "0",
            },
        )
        self.assertEqual(response.status_code, 400)
        fields = response.json()["fields"]
        self.assertEqual(fields["home_country"][0]["code"], "invalid_choice")
        self.assertEqual(fields["salary_chf"][0]["code"], "invalid")
        self.assertEqual(fields["bonus_chf"][0]["code"], "min_value")
        self.assertEqual(fields["chf_per_gbp"][0]["code"], "min_value")

    def test_missing_salary_is_required(self):
        del self.inputs["salary_chf"]
        response = self.client.post(self.url, self.inputs)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["fields"]["salary_chf"][0]["code"], "required")

    def test_post_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(self.url, self.inputs).status_code, 403)
