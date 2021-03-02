from django.db import models

from users.models import CustomUser as User


class RankList(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='rank_lists', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RankItem(models.Model):
    label = models.CharField(max_length=100)
    rank_list = models.ForeignKey(RankList, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.label
