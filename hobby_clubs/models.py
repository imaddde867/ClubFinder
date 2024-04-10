from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Club(models.Model):
    club_name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)  # 修改为小写
    address = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    activity = models.CharField(max_length=100)
    website = models.URLField()
    unique_identifier = models.CharField(max_length=100, unique=True)

    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return self.club_name

    def calculate_average_rating(self):
        """Calculate the average rating"""
        average_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = round(average_rating, 2) if average_rating else 0.00
        self.save()


class Review(models.Model):
    my_review = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name_plural = 'reviews'

    def __str__(self):
        return f"{self.my_review[:50]}..."


class Rating(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.user.username}'s rating for {self.club.club_name}: {self.rating}"
