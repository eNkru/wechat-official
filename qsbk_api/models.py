from django.db import models


class Joke(models.Model):
    author = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    like = models.CharField(max_length=10)

    def as_json(self):
        return dict(author=self.author, content=self.content, like=self.like)
