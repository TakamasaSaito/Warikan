from django.db import models
from django.utils import timezone

class TripModel(models.Model):
    tripname = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()

    # 名前を返す
    def __str__(self):
        return self.tripname

class PictureModel(models.Model):
    picturename = models.CharField(max_length=100)
    url = models.ImageField(upload_to='media')

    # 名前を返す
    def __str__(self):
        return self.picturename

class MemberModel(models.Model):
    membername = models.CharField(max_length=100)
    pictureID = models.ForeignKey(PictureModel, on_delete=models.CASCADE)
    tripID = models.ForeignKey(TripModel, on_delete=models.CASCADE)

    # 名前を返す
    def __str__(self):
        return self.membername

class DetailModel(models.Model):
    tripID = models.ForeignKey(TripModel, on_delete=models.CASCADE)
    memberID = models.ForeignKey(MemberModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    # タイトルを返す
    def __str__(self):
        return self.title
