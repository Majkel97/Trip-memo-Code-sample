from django import forms
from .models import Bill
from trips.models import Trip
from decimal import Decimal

from django.contrib.auth import get_user_model


class AddBill(forms.ModelForm):
    """
    Form for adding a bill to a trip.

    Fields:
        share_type (ChoiceField): A choice field to select the type of bill sharing.
        paid_by (ModelChoiceField): A field to select the user who paid the bill.
        total_amount (DecimalField): A decimal field to enter the total amount of the bill.
        currency (CharField): A character field to enter the currency for the bill.
        comment (CharField): A character field to enter an optional comment for the bill.

    Notes:
        - The form dynamically generates fields for each member in the trip to enter their share of the bill.
        - The share_type field allows choosing between "equal" or "custom_values" for sharing the bill.
        - The form is based on the Bill model and includes specific fields from the model.
    """

    share_type = forms.ChoiceField(
        choices=(
            ("equal", "Equal"),
            ("custom_values", "Custom values"),
        ),
    )

    def __init__(self, trip_id, *args, **kwargs):
        super(AddBill, self).__init__(*args, **kwargs)
        trip = Trip.objects.get(id=trip_id)
        members = get_user_model().objects.filter(id__in=trip.members.all())

        self.fields["paid_by"] = forms.ModelChoiceField(
            label="Paid By",
            queryset=members,
            empty_label=None,
        )

        self.fields["total_amount"] = forms.DecimalField(
            min_value=Decimal("0.00"), max_digits=11, decimal_places=2, initial="0.00"
        )

        self.fields.update(
            {
                str(member.id): forms.DecimalField(
                    label=f"{member.first_name} {member.last_name}",
                    decimal_places=2,
                    max_digits=11,
                    min_value=Decimal("0.00"),
                    widget=forms.NumberInput(
                        attrs={
                            "step": "0.01",
                            "min": "0",
                            "id": member.id,
                            "disabled": True,
                            "value": "0.00",
                        }
                    ),
                )
                for member in members
            }
        )

    class Meta:
        model = Bill
        fields = ["expense_category", "paid_by", "total_amount", "currency", "comment"]
