from decimal import Decimal

from django import forms

from .money import calculate_home_pay_gbp


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
    salary_chf = forms.DecimalField(
        label="Annual salary (CHF)",
        min_value=Decimal("0"),
        max_digits=11,
        decimal_places=2,
        initial=Decimal("150000.00"),
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    bonus_chf = forms.DecimalField(
        label="Annual bonus (CHF)",
        min_value=Decimal("0"),
        max_digits=11,
        decimal_places=2,
        initial=Decimal("20000.00"),
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
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
