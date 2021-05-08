import json
import random

from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.views import View

from users.models import CustomUser

from definitive.models import RankList, RankResponse
from definitive.forms import AddRankItemForm, AddRankListForm


def home(request):
    list_id = RankList.objects.aggregate(Max('id'))['id__max']
    return redirect('ranklist', list_id)


def rankview(request, list_id):
    ranklist = RankList.objects.get(id=list_id)
    items = ranklist.items_in_rank_order()
    context = {
        'title': ranklist.name,
        'list_id': list_id,
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

    def get(self, request, list_id, *args, **kwargs):
        ranklist = RankList.objects.get(id=list_id)
        item_1 = self.random_item(ranklist)
        item_2 = self.random_item(ranklist)
        while item_2 == item_1:
            item_2 = self.random_item(ranklist)
        context = {
            'title': ranklist.name,
            'list_id': list_id,
            'item_1': item_1,
            'item_2': item_2
        }
        return render(request, 'definitive/vote.html', context)

    def post(self, request, list_id, *args, **kwargs):
        if request.user.is_authenticated:
            user = CustomUser.objects.get(id=request.user.id)
        else:
            user = None
        left = request.POST.get('left')
        right = request.POST.get('right')
        winner = request.POST.get('winner')
        RankResponse.objects.create(
            user=user,
            left_id=left,
            right_id=right,
            winner_id=winner,
        )
        return self.get(request, list_id=list_id)

    @staticmethod
    def random_item(ranklist):
        items = ranklist.items.all()
        return random.choice(items)
