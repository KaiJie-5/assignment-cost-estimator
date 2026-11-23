import json
from unittest.mock import patch

from django.test import Client, SimpleTestCase, override_settings
from django.urls import reverse

from estimator.tests.pack_case import PACK_FORM_DATA


class CostEstimateApiTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("estimator:cost_estimate")

    def test_pack_json_returns_two_year_report(self):
        data = json.dumps(PACK_FORM_DATA).replace('"1.10"', "1.10")
        response = self.client.post(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertEqual(report["summary"]["year_one"]["cost_gbp"], "288656.36")
        self.assertEqual(report["summary"]["year_two"]["cost_gbp"], "267861.57")
        self.assertEqual(report["summary"]["total"]["cost_gbp"], "556517.92")
        self.assertEqual(report["summary"]["total"]["home_pay_multiple"], "1.8005")
        self.assertEqual(len(report["sections"]), 4)

    def test_form_data_allows_omitting_optional_housing_relief(self):
        data = PACK_FORM_DATA.copy()
        del data["housing_relief"]
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["summary"]["total"]["cost_gbp"], "556517.92")

    def test_invalid_values_return_field_errors(self):
        data = {
            **PACK_FORM_DATA,
            "home_country": "US",
            "chf_per_gbp": "0",
            "bonus_chf": "NaN",
            "moving_costs_gbp": "-1",
            "monthly_housing_gbp": "10.001",
            "housing_relief": "maybe",
        }
        del data["salary_chf"]
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        fields = response.json()["fields"]
        self.assertEqual(fields["home_country"][0]["code"], "invalid_choice")
        self.assertEqual(fields["chf_per_gbp"][0]["code"], "min_value")
        self.assertEqual(fields["bonus_chf"][0]["code"], "invalid")
        self.assertEqual(fields["moving_costs_gbp"][0]["code"], "min_value")
        self.assertEqual(fields["monthly_housing_gbp"][0]["code"], "max_decimal_places")
        self.assertEqual(fields["housing_relief"][0]["code"], "invalid_choice")
        self.assertEqual(fields["salary_chf"][0]["code"], "required")

    def test_invalid_json_returns_readable_bad_request(self):
        for body in ("{", "[]", "null"):
            with self.subTest(body=body):
                response = self.client.post(
                    self.url, body, content_type="application/json"
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()["fields"], {})
                self.assertIn("JSON object", response.json()["error"])

    def test_requires_post_and_csrf(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(self.url, PACK_FORM_DATA).status_code, 403)

    @override_settings(DEBUG=False)
    def test_server_error_has_no_exception_details(self):
        client = Client(raise_request_exception=False)
        with patch(
            "estimator.views.cost_report", side_effect=RuntimeError("private detail")
        ):
            response = client.post(self.url, PACK_FORM_DATA)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(), {"error": "Something went wrong. Please try again."}
        )
