from django.http import HttpResponse
from django.shortcuts import render

from definitive.models import RankList


def index(request):
    items = RankList.objects.first().items.all()
    context = {
        'items': items
    }
    return render(request, 'ranklist.html', context)
