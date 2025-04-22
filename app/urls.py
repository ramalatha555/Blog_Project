from django.urls import path
from . import views


urlpatterns = [
    path('',views.nav, name= 'nav'),  
    path('home',views.home,name='home'),
    path('index/',views.index,name='index'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile/',views.profile,name="profile"),
    path('myblogs/',views.myblogs,name="myblogs"),
    path('blog-post/<int:id>/',views.blog_post,name="blog_post"),
    path('register',views.register,name='register' ),
    path('registration/',views.registration, name='registration'),
    path('login/',views.login,name='login'),
    path('login1/',views.login1,name='login1'),
    path('logout/',views.logout,name='logout'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    path('upload-blog/',views.upload_blog,name='upload_blog'), 
    path('add_post/',views.add_post,name='add_post'), 
    path('forgotpass/',views.forgotpass, name='forgotpass'),
    path('reset_pass/',views.reset_pass,name='reset_pass'),   
    path('password_reset/',views.password_reset,name="password_reset"),
    path('update_pass/',views.update_pass,name="update_pass"),
    path('update_blog/<int:id>/',views.update_blog,name= "update_blog"),
    path('blog_update/<int:id>/',views.blog_update,name="blog_update"),
    path('delete_blog/<int:id>/',views.delete_blog, name= "delete_blog"),
    path('comments/<int:id>/',views.comments,name= 'comments'),
    path('likes/<int:id>/',views.likes,name= 'likes'),
    path('dislike/<int:id>/',views.dislike, name ='dislike'),
    path('search/',views.search,name='search'),



]
