from django.http import HttpResponse
from django.shortcuts import render

from definitive.models import RankList
from definitive.forms import AddRankItemForm


def rankview(request, list_id):
    items = RankList.objects.get(id=list_id).items.all()
    context = {
        'items': items
    }
    return render(request, 'ranklist.html', context)


def new_item(request, list_id):
    rank_list =RankList.objects.get(id=list_id)
    form = AddRankItemForm
    context = {
        'form': form,
        'rank_list': rank_list
    }
    return render(request, 'new_item.html', context)


