import uuid

from django.db import models

from definitive.rank import PageRank
from users.models import CustomUser as User


class RankList(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='rank_lists', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def resp_list(self):
        return [r.result for r in RankResponse.objects.filter(winner__in=self.items.all())]

    def final_page_rank(self):
        return PageRank(list(self.items.values_list('id', flat=True)), self.resp_list())


class RankItem(models.Model):
    label = models.CharField(max_length=100)
    rank_list = models.ForeignKey(RankList, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.label


class RankResponse(models.Model):
    user = models.ForeignKey(User, related_name='responses', on_delete=models.SET_NULL, null=True, blank=True)
    response_id = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text='unique id for this respondent')
    left = models.ForeignKey(RankItem, related_name='left_battles', on_delete=models.CASCADE)
    right = models.ForeignKey(RankItem, related_name='right_battles', on_delete=models.CASCADE)
    winner = models.ForeignKey(RankItem, related_name='wins', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('response_id', 'left', 'right')

    def __str__(self):
        return f"[{self.left.id}, {self.right.id}, {self.winner.id}]"

    @property
    def result(self):
        return [self.left.id, self.right.id, self.winner.id]

    def save(self, *args, **kwargs):
        if not self.user:
            self.response_id = uuid.uuid4()
        else:
            self.response_id = self.user.id
        super().save(*args, **kwargs)
