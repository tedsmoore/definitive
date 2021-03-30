from django import forms

from definitive.models import RankItem


class AddRankItemForm(forms.ModelForm):

    class Meta:
        model = RankItem
        fields = ('label', 'image')
