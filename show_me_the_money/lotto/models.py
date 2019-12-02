from django.db import models

# Create your models here.

class Lotto(models.Model):
    count = models.IntegerField(unique=True)
    date = models.TextField()

    nums_1 = models.IntegerField()
    nums_2 = models.IntegerField()
    nums_3 = models.IntegerField()
    nums_4 = models.IntegerField()
    nums_5 = models.IntegerField()
    nums_6 = models.IntegerField()
    nums_bonus = models.IntegerField()

    def get_count(self):
        return self.count

    def get_date(self):
        return self.date

    def get_number_array(self):
        numbers = [self.nums_1, self.nums_2, self.nums_3, self.nums_4, self.nums_5, self.nums_6, self.nums_bonus]

        return numbers

    def get_winning_data_dict(self):
        winning_datas = WinningData.objects.filter(lotto_id=self.id)

        winning_data_dict = {}

        for winning_data in winning_datas:
            winning_data_dict[winning_data.rank] = {
                'total_money' : winning_data.total_money,
                'winner' : winning_data.winner,
                'each_money' : winning_data.each_money
            }

        return winning_data_dict

class WinningData(models.Model):
    lotto = models.ForeignKey(Lotto, on_delete=models.CASCADE)

    count = models.IntegerField()
    rank = models.IntegerField()

    total_money = models.TextField()
    winner = models.TextField()
    each_money = models.TextField()

    class Meta:
        unique_together = (("count", "rank"),)