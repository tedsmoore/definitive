from django.http import HttpResponse
from django.shortcuts import render

from definitive.models import RankList


def rankview(request, list_id):
    items = RankList.objects.get(id=list_id).items.all()
    context = {
        'items': items
    }
    return render(request, 'ranklist.html', context)
