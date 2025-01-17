# from django.core.validators import RegexValidator, validate_slug
# from django.db import models

# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=100,
#     validators=[RegexValidator(r'^[a-zA-Z0-9]*$', 
#     message='Usernames can only contain letters and numbers.', 
#     code="invalid_username"),],
#     unique=True)  # User's unique username
#     email = models.EmailField(unique=True) 
#     created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user was created


#     def __str__(self):
#         return self.username

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"
