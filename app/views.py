from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from . models import UserProfile, UploadBlogModel, CommentsModel, LikesModel
import random
import string
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q



# Create your views here.
def nav(request):
    return render(request, 'nav.html')

def home(request):
    d = request.session.get('username')
    return render(request, 'home.html',{'user':d})



def index(request):
    d = request.session.get('username')
    p = request.session.get('pic')
    
    return render(request, 'index.html',{'user':d, 'pic':p})

def dashboard(request):
    d = request.session.get('username')
    p = request.session.get('pic')
    print(p)

    data = UploadBlogModel.objects.filter(post_type='public')
    # data.update(likes=0, dislikes=0)


    return render(request, 'dashboard.html',{'user':d, 'pic':p, 'data':data})


def profile(request):
    d = request.session.get('username')
    p = request.session.get('pic')
    return render(request, 'updateprofile.html',{'user':d, 'pic':p})

def myblogs(request):
    d = request.session.get('username')
    p = request.session.get('pic')
    email = request.session.get('email')

    data = UploadBlogModel.objects.filter(Q(email=email) | Q(tag=email))    
    return render(request, 'myblogs.html',{'user':d, 'pic':p, 'data' :data})

def blog_post(request, id) :    
    blog = get_object_or_404(UploadBlogModel, id=id)
    d = request.session.get('username')
    p = request.session.get('pic')
    # print(blog.email)
    return render(request,'blog-post.html',{'user':d, 'blog' :  blog, 'pic':p })

def register(request):
    return render(request, 'register.html')


def registration(request):
   if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        age = request.POST['age']
        profile_picture = request.FILES['file']
        profilename = profile_picture.name

        
        # Check if email already exists
        if UserProfile.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists!')
            return redirect('register')
        
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Create user profile
        user_profile = UserProfile.objects.create(
            username=username,
            email=email,
            phone_number=phone,
            age=age,
            profile_picture=profile_picture,
            profilename = profile_picture.name
        )
        user_profile.save()
        
        email_subject = 'Registration Details'
        email_message = f'Hello {username},\n\nThank you for registering with us!\n\nHere are your registration details:\n\nUsername: {username}\nEmail: {email}\nPassword: {password}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
        send_mail(email_subject, email_message, 'appcloud887@gmail.com', [email])

        update_password = UserProfile.objects.get(email=email)
        update_password.password = password
        update_password.save()
        # Redirect to login page
        return redirect('login')
   return redirect('register')



def login(request):
    return render(request, 'login.html')
 


def login1(request):
    if request.method == "POST":
        password =  request.POST["password"]
        email =  request.POST["email"]   
        user = UserProfile.objects.filter(email=email, password=password)
        # data = [(i.profile_picture,i.username)for i in user]
        # print(data,"ddd")
        # u = data[0][0]
        if user:
            request.session['username'] = user[0].username
            request.session['email'] = email
            request.session['pic'] = user[0].profile_picture.url
            j = request.session.get('pic')
            
            
            messages.success(request, 'Successfully Login !')
        
            return render(request, 'home.html',{"user":user[0].username})   
        else:
            print("hfjfnanfwsdvjvnvskvn")
            messages.warning(request, 'Username or Password is incorrect!')
            return render(request, "login.html")
         
    return render(request, "login.html")


def logout(request):
    del request.session['username']
    messages.success(request, 'Logged out successfully!')
    return redirect('/')

def upload_blog(request):
    d = request.session.get('username')
    p = request.session.get('pic')
    return  render(request,'uploadblog.html', {'user':d, 'pic'  :p })


def updateprofile(request):
    if  request.method=='POST':
        username = request.POST['username']
        phone = request.POST['phone']
        age = request.POST['age']
        file = request.FILES['file']
        email = request.session['email']
        profilename = file.name

        user = UserProfile.objects.get(email=email)
        user.username=username
        user.phone_number=phone
        user.age=age
        user.profile_picture=file
        user.profilename = profilename
        user.save()
        return redirect('login')









def  add_post(request):
    if  request.method=="POST":
       title = request.POST['title']
       content = request.POST['description']
       author = request.session['username']
       post_type =  request.POST['post-type']
       img = request.FILES['file']
       time =  timezone.now()
       email = request.session.get('email')
       tag = request.POST['tag']
       user = request.session.get('username')



       blog = UploadBlogModel.objects.create(
           author=author,
           email=email,
           title=title,
           description=content,
           blog_pic=img,
           post_type=post_type,
           time_field=time,
           tag=tag,
           tagby=user

           )
       blog.save()
       return redirect('dashboard')
    
    return redirect('dashboard')


def forgotpass(request):
    return render(request, 'forgotpass.html')


def reset_pass(request):
    if request.method == "POST":
        email = request.POST['email']
        user = UserProfile.objects.filter(email=email)
        print(user[0])

        if user:
            email_subject = 'Registration Details'
            url = 'http://127.0.0.1:8000/password_reset/'
            email_message = f'Hello {user[0]},\n\nThank you for registering with us!\n\nHere are your details:\n\nUsername: {user[0]}\nEmail: {email}\n Reset Your Password Here: {url}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
            send_mail(email_subject, email_message, 'appcloud887@gmail.com', [email])
            messages.success(request, 'Reset Password  Link has been sent to your registered Email ID')
            return redirect('password_reset')
        else:
            messages.success(request, 'User was not Found')
            return redirect('forgotpass')
    

def password_reset(request):

    return  render(request,'reset-pass.html')

def update_pass(request):
    if request.method=='POST':
        email = request.POST['email']
        new_pwd = request.POST['password']
        confirm_pwd = request.POST['confirm_password']
        if new_pwd ==  confirm_pwd:
            user =  UserProfile.objects.get(email=email)
            user.password = new_pwd
            user.save()
            messages.success(request, 'Your password was successfully updated')
            return  redirect('login')
        else:
            messages.success(request, 'Password and Confirm Password does not match!')
            return redirect('password_reset')


def update_blog(request, id):
    res = UploadBlogModel.objects.get(id=id)
    email = request.session.get( 'email')
    pic = request.session.get('pic')
    if email == res.email:
        return render(request, 'updateblog.html',{'pic':pic,'id' : id})
    else:
        messages.success(request, 'Update this Blog only  by the Owner of that blog')
        return redirect('blog_post',id)
    
def blog_update(request, id):
    if request.method=="POST":
       title = request.POST['title']
       content = request.POST['description']
       author = request.session['username']
       post_type =  request.POST['post-type']
       img = request.FILES['file']
       time =  timezone.now()
       email = request.session.get('email')
       tag = request.POST['tag']
       user = request.session['username']
       
       blog = UploadBlogModel.objects.get(id=id)

       blog.author=author
       blog.email=email
       blog.title=title
       blog.description=content
       blog.blog_pic=img
       blog.post_type=post_type
       blog.time_field=time
       blog.tag=tag
       
    
       blog.save()
       messages.success(request, 'Sucessfully Updated')
       return redirect('blog_post',id)
    return redirect('dashboard')

def delete_blog(request, id):
    res = get_object_or_404(UploadBlogModel, id=id)
    email = request.session.get( 'email')
    pic = request.session.get('pic')
    if email == res.email:

    # record = get_object_or_404(UploadBlogModel, id=id)
        res.delete()
        messages.success(request,"This Post has been deleted")
        return redirect('dashboard')
    else:
        messages.success(request, 'delte this Blog only  by the Owner of that blog')
        return redirect('blog_post',id)


def comments(request, id):
    
    pic  = request.session['pic']
    name = request.session['username']
    if  request.method == "POST":
        message =  request.POST.get("message")
        time =  timezone.now()


        comment = CommentsModel.objects.create(
            blog_id=id,
            name=name,
            comments=message,
            dateandtime=time,

        )
        comment.save()
        # stored_messages = CommentsModel.objects.all(blog_id=id)
        # return render(request,'comments.html',{'stored_messages':stored_messages, 'id': id, 'pic':pic})
        return redirect('comments', id=id)

 

    stored_messages = CommentsModel.objects.filter(blog_id=id) 
    return render(request,'comments.html',{'data':stored_messages, 'id': id, 'pic':pic, 'user' : name })


def likes(request, id):
    
    pic = request.session['pic']
    email = request.session['email']
    res = LikesModel.objects.filter(blog_id=id,user_email=email).exists()
   
    print(res) 
    print('hello')
    if res:
        messages.success(request,"You have already liked this post!")
        return redirect('dashboard')
    else:
        print('hhhhh')
        likes = LikesModel.objects.create(
        user_email=email,
        blog_id=id,
        like=1,
        dislike=0, 

        )
        likes.save()
        result = LikesModel.objects.filter(blog_id=id, like=1).count()
        # data = UploadBlogModel.objects.all()
        lik = UploadBlogModel.objects.get(id=id) 
        lik.likes = result
        lik.save()
        return redirect('dashboard')      
   


def dislike(request, id):
    email = request.session['email']
    res = LikesModel.objects.filter(blog_id=id,user_email=email,dislike=1).exists()
    # dat = [i.user_email for i in res]
    print(res) 
    
    if res:
        messages.success(request,"You have already disliked this post!")
        return redirect('dashboard')
        
    else:
         likes = LikesModel.objects.create(
            user_email=email,
            blog_id=id,
            like=0,
            dislike=1,

        )
         likes.save()
         result = LikesModel.objects.filter(blog_id=id, dislike=1).count()
         lik = UploadBlogModel.objects.get(id=id) 
         lik.dislikes = result
         lik.save()
         return redirect('dashboard')


def search(request):
    name = request.session['username']
    if request.method == 'POST':
        serch = request.POST['sss']
        pic =  request.session['pic']
        posts = UploadBlogModel.objects.filter(title = serch)

        return render (request, 'dashboard.html', { 'data' : posts,'pic':pic, 'user' : name})

