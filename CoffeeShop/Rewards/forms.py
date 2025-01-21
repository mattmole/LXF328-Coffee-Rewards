from django import forms


class PointsForm(forms.Form):
    operationChoices = (("Add","Add"), ("Use Reward(s)","Use"))
    operation = forms.ChoiceField(label="Operation", choices=operationChoices)
    quantity = forms.IntegerField(label="Quantity")
