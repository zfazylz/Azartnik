from django.db import models

from customUser.models import CustomUser


class SportBet(models.Model):
    name = models.CharField(default=None, max_length=50)
    w1 = models.FloatField(default=2.64)
    w2 = models.FloatField(default=2.64)
    d = models.FloatField(default=2.64)
    status = models.IntegerField(default=-1, null=True)
    #   1 w1
    #   2 w2
    #   0 d
    #   -1 playing

class UserBet(models.Model):
    user = models.ForeignKey(CustomUser, default=None, null=True, on_delete=models.SET_NULL)
    bet = models.ForeignKey(SportBet, default=None, null=True, on_delete=models.SET_NULL)
    betValue = models.IntegerField(default=0, null=True)
    coefficient = models.FloatField(default=1)
    side = models.IntegerField(default=-1, null=True)
    #   1 w1
    #   2 w2
    #   0 d
    status = models.IntegerField(default=0)
    #   0 playing
    #   1 win
    #   2 loose

    def winValue(self):
        return self.betValue * self.coefficient
