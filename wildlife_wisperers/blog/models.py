from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username
    # profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    # bio = models.TextField(blank=True)
    # blogs = models.ManyToManyField('Blog', related_name='authors', blank=True)
    # followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    # social_media_links = models.URLField(blank=True)


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Travel', 'Travel'),
        # Add categories
    ]
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    feature_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    upvote_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comments = models.ManyToManyField('Comment', related_name='comments', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return f'{self.user.username}'
