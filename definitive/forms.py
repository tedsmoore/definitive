from django import forms

from definitive.models import RankItem, RankList


class AddRankItemForm(forms.ModelForm):

    class Meta:
        model = RankItem
        fields = ('label', 'image')


class AddRankListForm(forms.ModelForm):

    class Meta:
        model = RankList
        fields = ('name', 'open_until')
