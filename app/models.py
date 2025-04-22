from django.db import models
import os
class UserProfile(models.Model):
    username = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20,null=True)
    age = models.IntegerField(null=True)
    profile_picture = models.FileField(upload_to=os.path.join("static","profile_pictures"))
    profilename = models.CharField(max_length=100,null=True)
    password = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = 'UserProfile'
    
class UploadBlogModel(models.Model):
    author = models.CharField(max_length=100, null=True)
    email = models.EmailField(null= True)
    tag = models.EmailField(null=True)
    title =  models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    blog_pic = models.FileField(upload_to=os.path.join("static","blog_pic"))
    post_type = models.CharField(max_length=50, null=True)
    time_field = models.DateTimeField(null=True)
    likes = models.IntegerField(default=0)
    dislikes  = models.IntegerField(default=0)
    tagby = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.author
    class Meta:
        db_table = 'UploadBlogModel'
    
class CommentsModel(models.Model):
    blog_id = models.IntegerField(null=True)
    name= models.CharField(max_length=30, null=True)
    comments= models.TextField(null=True)
    dateandtime= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'CommentsModel'


class LikesModel(models.Model):
    blog_id = models.IntegerField(null=True)
    user_email = models.EmailField(null=True)
    like  = models.IntegerField(null=True)
    dislike = models.IntegerField(null=True)

    def __str__(self):
        return self.user_email
    class Meta:
        db_table =  "LikesModel"


