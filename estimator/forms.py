from decimal import Decimal

from django import forms

from .costs import AssignmentCost, estimate_assignment_cost
from .money import calculate_home_pay_gbp


def _money_field(label, initial, help_text=""):
    return forms.DecimalField(
        label=label,
        min_value=Decimal(0),
        max_digits=11,
        decimal_places=2,
        initial=Decimal(initial),
        help_text=help_text,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


class HomePayForm(forms.Form):
    home_country = forms.ChoiceField(
        choices=[("CH", "Switzerland")],
        initial="CH",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    host_country = forms.ChoiceField(
        choices=[("GB", "United Kingdom")],
        initial="GB",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    salary_chf = _money_field("Annual salary (CHF)", "150000.00")
    bonus_chf = _money_field("Annual bonus (CHF)", "20000.00")
    chf_per_gbp = forms.DecimalField(
        label="CHF per £1",
        min_value=Decimal("0.000001"),
        max_digits=9,
        decimal_places=6,
        initial=Decimal("1.10"),
        help_text="For example, enter 1.10 when £1 buys CHF 1.10.",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    def home_pay_gbp(self):
        return calculate_home_pay_gbp(
            salary_chf=self.cleaned_data["salary_chf"],
            bonus_chf=self.cleaned_data["bonus_chf"],
            chf_per_gbp=self.cleaned_data["chf_per_gbp"],
        )


class CostEstimateForm(HomePayForm):
    monthly_housing_gbp = _money_field(
        "Monthly London rent (GBP)",
        "3000.00",
        "Rent paid by the employer in both years.",
    )
    relocation_allowance_chf = _money_field(
        "Cash relocation allowance (CHF)", "5000.00", "Paid only in Year 1."
    )
    moving_costs_gbp = _money_field(
        "Moving costs (GBP)", "6000.00", "Flights and shipping paid in Year 1."
    )
    temporary_housing_gbp = _money_field(
        "Temporary housing (GBP)", "4000.00", "The total for the first four weeks."
    )
    housing_relief = forms.TypedChoiceField(
        label="UK tax treatment of London rent",
        choices=(
            ("no", "Taxable benefit in kind"),
            ("yes", "Temporary-workplace relief confirmed"),
        ),
        coerce=lambda value: value == "yes",
        empty_value=False,
        required=False,
        initial="no",
        help_text="Select relief only if the London rent qualifies under HMRC's rules.",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def estimate(self) -> AssignmentCost:
        data = self.cleaned_data
        return estimate_assignment_cost(
            salary_chf=data["salary_chf"],
            bonus_chf=data["bonus_chf"],
            chf_per_gbp=data["chf_per_gbp"],
            monthly_housing_gbp=data["monthly_housing_gbp"],
            relocation_allowance_chf=data["relocation_allowance_chf"],
            moving_costs_gbp=data["moving_costs_gbp"],
            temporary_housing_gbp=data["temporary_housing_gbp"],
            housing_relief=data["housing_relief"],
        )
