from django.db import models
from django.contrib.auth import get_user_model
from tinymce import models as tinymce_models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User,
        related_name='posts',
        verbose_name='Owner',
        on_delete=models.CASCADE,
    )
    header = tinymce_models.HTMLField()
    text = tinymce_models.HTMLField()
    average_bill = models.IntegerField(default=0)
    average_rating = models.IntegerField(default=0)
    reviews_count = models.IntegerField(default=0)
    ratings_sum = models.IntegerField(default=0)


class Review(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Review',
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Review',
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        default=0,
    )


@receiver(pre_save, sender=Review)
def model_pre_save(sender, **kwargs):
    review = kwargs['instance']
    post = review.post
    post.ratings_sum += review.rating
    post.reviews_count += 1
    post.average_rating = post.ratings_sum / post.reviews_count
    post.save()


@receiver(post_delete, sender=Review)
def model_post_delete(sender, **kwargs):
    review = kwargs['instance']
    post = review.post
    post.ratings_sum -= review.rating
    post.reviews_count -= 1
    post.average_rating = post.ratings_sum / post.reviews_count
    post.save()
