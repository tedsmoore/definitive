import json

from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.views import View

from definitive.models import RankList
from definitive.forms import AddRankItemForm, AddRankListForm


def home(request):
    list_id = RankList.objects.aggregate(Max('id'))['id__max']
    return redirect('ranklist', list_id)


def rankview(request, list_id):
    ranklist = RankList.objects.get(id=list_id)
    items = ranklist.items_in_rank_order()
    context = {
        'title': ranklist.name,
        'items': items
    }
    return render(request, 'definitive/ranklist.html', context)


@login_required
def new_item(request, list_id):
    rank_list = RankList.objects.get(id=list_id)
    form = AddRankItemForm()
    context = {
        'form': form,
        'rank_list': rank_list
    }
    return render(request, 'definitive/new_item.html', context)


@login_required
def add_new_list(request):
    form = AddRankListForm()
    if request.method == 'POST':
        new_list = form.save(commit=False)
        new_list.owner = request.user
        new_list.save()
    context = {
        'form': form,
    }
    return render(request, 'definitive/new_list.html', context)


def pick_a_winner_view(request, list_id):
    return render(request, '')


def awesome_baby(request):
    return render(request, 'definitive/static_xmpl.html')


def data_only_view(request, list_id):
    ranklist = RankList.objects.get(id=list_id)
    items = serializers.serialize('json', ranklist.items.all())
    return JsonResponse({'items': json.loads(items)})


def data_from_ajax(request):
    return render(request, 'definitive/data_from_ajax.html', {})


def login(request):
  return render(request, 'definitive/login.html')


class VoteView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'definitive/choices.html', {})
