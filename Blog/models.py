from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    title = models.CharField(verbose_name="Title", max_length=150)
    content = models.CharField(verbose_name="Content", max_length=1000)
    pub_date = models.DateTimeField(verbose_name="Published At", auto_now=True)
    POST_STATES = (
        (1, 'Draft '),
        (2, 'Published'),
        (3, 'Archived')
    )
    state = models.IntegerField(verbose_name="State", choices=POST_STATES)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
