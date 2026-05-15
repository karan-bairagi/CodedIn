from django.shortcuts import render,redirect
from app.forms import SignUpForm,LoginForm,UserProfileForm,Forgetten_Password_Form,Forgetten_email,ProjectCardForm,Personal_Form,check_password_Form,Public_Profile_Form,Security_Questions_Form,Request_User_Form
from django.contrib.auth.models import User
from app.models import UserProfile,ProjectCard
from django.db.models import Q
import string
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.utils import timezone 
from app.models import ProfileVisitor
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse

def login_required(func):
    def check(request,*args,**kwargs):
        user_id=request.session.get('id')
        if not user_id:
            return redirect('user_login')
        try:
            user=User.objects.get(id=user_id)
            request.custom_user=user
        except User.DoesNotExist:
            request.session.flush()
            return redirect('user_login')
        return func(request,*args,**kwargs)
    return check
def signup(request):
    if request.session.get('id'):
        return redirect('dashboard')
    if request.method=='POST':
        f=SignUpForm(request.POST)
        if f.is_valid():
            data=f.cleaned_data
            full_name=data['full_name']
            username=data['username']
            user_email=data['email']
            mobile=data['Mobile']
            pwd=data['password']
            password=make_password(pwd)
            sv=User.objects.create(username=username,password=password,email=user_email)
            user_id=sv.id
            request.session['id']=user_id
            UserProfile.objects.create(user=sv,full_name=full_name,Mobile=mobile)
            return redirect('security')
        else:
            return render(request,'signup.html',{'f':f})
    f=SignUpForm()
    return render(request,'signup.html',{'f':f})
def user_login(request):
    if request.session.get('id'):
        return redirect('dashboard')
    if request.method=='POST':
        f=LoginForm(request.POST)
        if f.is_valid():
            data=f.cleaned_data
            username=data['username']
            pwd=data['password']
            try:
                sv=User.objects.get(username=username)
                if check_password(pwd,sv.password):
                    request.session['id']=sv.id
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid username or password. Please try again.")
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password. Please try again.")
            return render(request,'login.html',{'f':f})
        else:
            return render(request,'login.html',{'f':f})
    f=LoginForm()
    return render(request,'login.html',{'f':f})
@login_required
def Dashboard(request):
    find=request.session.get('id')
    user_obj=User.objects.get(id=find)
    sv=ProjectCard.objects.filter(creator=find)
    all_data=ProfileVisitor.objects.filter(profile_owver=find).order_by('-profile_visitor_time')
    return render(request,'dashboard.html',{'user':user_obj,'project':sv,'all_viewrs':all_data})
@login_required
def logout(request):
    request.session.flush()
    return redirect('user_login')
@login_required
def user_profile(request):
    user_id=request.session.get('id')
    find=UserProfile.objects.get(user_id=user_id)
    if request.method=='POST':
        f=UserProfileForm(request.POST,request.FILES,instance=find)
        if f.is_valid():
            f.save()
            return redirect('profile_view')
        else:
            return render(request,'profile.html',{'f':f,'user':request.custom_user})
    f=UserProfileForm(instance=find)
    return render(request,'profile.html',{'f':f,'user':request.custom_user})
@login_required
def profile_remove(request):
    user_id=request.session.get('id')
    sv=UserProfile.objects.get(user_id=user_id)
    profile_user=sv.profile
    profile_user.delete()
    return redirect('profile')
@login_required
def profile_view(request):
    user_id=request.session.get('id')
    user=User.objects.get(id=user_id)
    return render(request,'profile_view.html',{'user':user})

def forgettern_password(request):
    if request.method=='POST':
        f=Forgetten_email(request.POST)
        if f.is_valid():
            data=f.cleaned_data
            user_email=data['new_email']
            try:
                sv=User.objects.get(email=user_email)
                user_email=sv.id
                request.session['email_id']=user_email
                return redirect('check')
            except User.DoesNotExist:
                messages.error(request, "This email address is not registered with us.")
            return render(request,'forgetten_email.html',{'f':f})
        else:
            return render(request,'forgetten_email.html',{'f':f})
    f=Forgetten_email()
    return render(request,'forgetten_email.html',{'f':f})
def forgetten_reset_password(request,user_token):
    user_id=request.session.get('email_id')
    actual_user=User.objects.get(id=user_id)
    token=request.session.get('user_token')
    if request.method=='GET':
        f=Forgetten_Password_Form()
        return render(request,'forget_reset_password.html',{'f':f})
    if str(user_token)!=str(token):
        return render(request,'forget_reset_password.html',{'warning':'Access Denied: The password reset token is invalid, expired, or has been tampered with. Please restart the process.'})
    if request.method=='POST':
        f=Forgetten_Password_Form(request.POST)
        if f.is_valid():
            data=f.cleaned_data
            pwd=data['confirm']
            pwd1=data['New_Password']
            if str(pwd)!=str(pwd1):
                return render(request,'forget_reset_password.html',{'f':f,'confirm_password_invalid':'The password confirmation does not match. Please re-type your new password.'})
            password=make_password(pwd)
            actual_user.password=password
            actual_user.save()
            if 'email_id' in request.session:
                del request.session['email_id']
            if 'user_token' in request.session:
                del request.session['user_token']
            return redirect('user_login')
        else:
            return render(request,'forget_reset_password.html',{'f':f})

@login_required
def projectcard(request):
    if request.method=='POST':
        f=ProjectCardForm(request.POST,request.FILES)
        if f.is_valid():
            data=f.cleaned_data
            title=data['title']
            thumbnail=data['thumbnail']
            tech_stack=data['tech_stack']
            project_link=data['project_link']
            live_link=data['live_link']
            try:
                user_id=request.session.get('id')
                user=User.objects.get(id=user_id)
                sv=ProjectCard.objects.create(creator=user,title=title,tech_stack=tech_stack,project_link= project_link,live_link=live_link,thumbnail=thumbnail)
                return redirect('dashboard')
            except User.DoesNotExist:
                messages.error(request,'Invalid User ID')
        else:
            return render(request,'projectcard.html',{'f':f})
    f=ProjectCardForm()
    return render(request,'projectcard.html',{'f':f})
@login_required
def project_view(request,project_id):
    find=ProjectCard.objects.get(id=project_id)
    if request.method=='POST':
        f=ProjectCardForm(request.POST,request.FILES,instance=find)
        if f.is_valid():
            f.save()
            return redirect('dashboard')
        else:
            return render(request,'projectcard.html',{'f':f})
    f=ProjectCardForm(instance=find)
    return render(request,'projectcard.html',{'f':f})
@login_required
def project_delete(request,project_id):
    find=ProjectCard.objects.get(id=project_id)
    find.delete()
    return redirect('dashboard')

def public_profile(request,username):
    user_obj=User.objects.get(username=username)
    user_id=request.session.get('id')
    if user_id and int(user_id)==int(user_obj.id):
        return redirect('profile_view')
    else:
        user=user_obj.id
        projects=ProjectCard.objects.filter(creator=user)
        user_obj.userprofile.view_count+=1
        user_obj.userprofile.save()
        if user_id:
            username=User.objects.get(id=user_id)
            visitor_name=username
        else:
            visitor_name='Guest User'
        visitor(request,user_obj,visitor_name)
        return render(request,'public_profile.html',{'user':user_obj,'profile':projects})
@login_required
def delete_user(request):
    user_id=request.session.get('id')
    find=User.objects.get(id=user_id)
    find.delete()
    request.session.flush()
    return redirect('user_login')
@login_required
def delete_user_confirm(request):
    user_id=request.session.get('id')
    find=User.objects.get(id=user_id)
    return render(request,'delete_confirm.html',{'user':find})
@login_required
def account_settings(request):
    user_id=request.session.get('id')
    find_obj=User.objects.get(id=user_id)
    return render(request,'Account_settings.html',{'user':find_obj})


@login_required
def personal_profile(request):
    user_id=request.session.get('id')
    find=User.objects.get(id=user_id)
    return render(request,'personal.html',{'user':find})
@login_required
def personal_update(request):
    user_id=request.session.get('id')
    find=User.objects.get(id=user_id)
    user_id=find.id
    if request.method=='POST':
        f=Personal_Form(request.POST,instance=find)
        if f.is_valid():
            data=f.cleaned_data
            full_name=data['full_name']
            email=data['email']
            username=data['username']
            mobile=data['mobile']
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                return render(request,'personal_update.html',{'f':f,'msg':'Username Already Exists Choice Different Username'})
            if User.objects.filter(email=email).exclude(id=user_id).exists():
                return render(request,'personal_update.html',{'f':f,'msg':'This Email Already Register Choice Different Email Address'})
            find.userprofile.full_name=full_name
            find.userprofile.Mobile=mobile
            find.userprofile.save()
            find.username=username
            find.email=email
            find.save()
            return redirect('personal')
        else:
            return render(request,'personal_update.html',{'f':f})
    old_data={
        'mobile':find.userprofile.Mobile,
        'full_name':find.userprofile.full_name
    }
    f=Personal_Form(instance=find,initial=old_data)
    return render(request,'personal_update.html',{'f':f})
@login_required
def change_password(request):
    user_id=request.session.get('id')
    find=User.objects.get(id=user_id)
    if request.method=='POST':
        f=check_password_Form(request.POST)
        if f.is_valid():
            data=f.cleaned_data
            pwd=data['password']
            db_pwd=find.password
            if check_password(pwd,db_pwd):
                return redirect('reset')
            else:
                return render(request,'check_password.html',{'password_error':'Incorrect password. Please verify your old password and re-type.','f':f})
        else:
            return render(request,'check_password.html',{'f':f})
    f=check_password_Form()
    return render(request,'check_password.html',{'f':f})
@login_required
def reset_password(request):
    user_id=request.session.get('id')
    find=User.objects.get(id=user_id)
    if request.method=='POST':
        f=Forgetten_Password_Form(request.POST)
        if f.is_valid():
            data=f.cleaned_data
            pwd=data['confirm']
            pwd1=data['New_Password']
            if str(pwd)!=str(pwd1):
                return render(request,'reset_password.html',{'f':f,'confirm_password_invalid':'The password confirmation does not match. Please re-type your new password.'})
            password=make_password(pwd)
            find.password=password
            find.save()
            return redirect('account')
        else:
            return render(request,'reset_password.html',{'f':f})
    f=Forgetten_Password_Form()
    return render(request,'reset_password.html',{'f':f})
@login_required
def Profile_Visibility(request):
    user_id=request.session.get('id')
    find=User.objects.get(id=user_id)
    if request.method=='POST':
        f=Public_Profile_Form(request.POST)
        if f.is_valid():
            data=f.cleaned_data
            pvt=data['pvt_pbl']
            find.userprofile.public_profile=pvt
            find.userprofile.save()
            return redirect('account')
    old_visibility={'pvt_pbl':find.userprofile.public_profile}
    f=Public_Profile_Form(initial=old_visibility)
    return render(request,'Profile_Visibility.html',{'f':f})
@login_required
def search(request):
    if request.method=='POST':
        search=request.POST.get('search')
        all_users=User.objects.filter(
            Q(username__icontains=search)|
            Q(userprofile__full_name__icontains=search)|
            Q(userprofile__tagline__icontains=search)
        )
        return render(request,'search.html',{'search':search,'data':all_users})
    return render(request,'search.html')

def visitor(request, owner, visitor):
    user = User.objects.get(username=owner)
    try:
        sv = ProfileVisitor.objects.get(profile_owver=user, profile_visitor=visitor)
        sv.profile_visitor_time = timezone.now()
        sv.save()
    except ProfileVisitor.DoesNotExist:
        sv = ProfileVisitor(profile_owver=user, profile_visitor=visitor)
        sv.save()

def about_developer(request):
    return render(request,'about_me.html')

def add_security(request):
    user_id=request.session.get('id')
    user=UserProfile.objects.get(user_id=user_id)
    if request.method=='POST':
        f=Security_Questions_Form(request.POST)
        if f.is_valid():
            data=f.cleaned_data
            sq=data['questions']
            sa=data['answer']
            user.security_question=sq
            user.security_answer=sa
            user.save()
            return redirect('dashboard')
        else:
            return render(request,'security.html',{'f':f})
    f=Security_Questions_Form()
    return render(request,'security.html',{'f':f})

def check_security(request):
    user_id=request.session.get('email_id')
    user=User.objects.get(id=user_id)
    if request.method=='GET':
        return render(request,'check_security.html',{'user':user})
    else:
        user_answer=request.POST.get('ua')
        if not user_answer:
            messages.error(request,'Enter Your Answer')
            return render(request,'check_security.html',{'user':user})
        if user_answer:
            db_answer=user.userprofile.security_answer
            if user_answer.lower()==db_answer.lower():
                return redirect('token')
            else:
                messages.error(request,'Incorrect answer. Please try again')
                return render(request,'check_security.html',{'user':user})
            
def token_generate(request):
    if request.method=='GET':
        allowed_chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        token = get_random_string(length=12, allowed_chars=allowed_chars)
        request.session['user_token']=token
        return render(request,'token.html',{'token':token})
    else:
        return redirect('reset_password')
    
def user_request(request):
    default="System generated alert: Full Name and Mobile verification requested for manual account recovery."
    if request.method=='POST':
        f=Request_User_Form(request.POST)
        if f.is_valid():
            f.save()
            success_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <!-- Ye line mobile screen par auto-fit karne ke liye sabse zaroori hai -->
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>CodeIn - Success</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                        background-color: #f8fafc;
                        margin: 0;
                        padding: 20px; /* Mobile ke liye outer padding kam ki */
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        box-sizing: border-box;
                    }
                    .success-card {
                        width: 100%;
                        max-width: 580px;
                        background: #f1f5f9;
                        border: 1px solid #e2e8f0;
                        border-radius: 12px;
                        padding: 32px; /* Laptop par bada padding */
                        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.02);
                        color: #0f172a;
                        box-sizing: border-box;
                    }
                    .success-title {
                        font-size: 18px;
                        font-weight: 700;
                        margin-top: 0;
                        margin-bottom: 20px;
                        line-height: 1.4;
                    }
                    .success-desc {
                        font-size: 15px;
                        line-height: 1.6;
                        color: #1e293b;
                        margin-bottom: 24px;
                    }
                    .steps-title {
                        font-size: 15px;
                        font-weight: 700;
                        margin-bottom: 16px;
                    }
                    .steps-list {
                        padding-left: 0;
                        margin: 0;
                        list-style: none;
                    }
                    .steps-list li {
                        font-size: 14.5px;
                        line-height: 1.6;
                        margin-bottom: 16px;
                        color: #334155;
                    }
                    .bold-text {
                        font-weight: 700;
                        color: #0f172a;
                    }

                    /* === MOBILE RESPONSIVE QUERIES === */
                    @media (max-width: 480px) {
                        body {
                            padding: 12px; /* Mobile screen ke kinaro par gap */
                        }
                        .success-card {
                            padding: 20px; /* Mobile par card ka andar ka padding chota kiya */
                            border-radius: 10px;
                        }
                        .success-title {
                            font-size: 16px; /* Mobile par heading halki choti taaki wrap acchi ho */
                            margin-bottom: 14px;
                        }
                        .success-desc {
                            font-size: 13.5px; /* Reading text size for mobile */
                            margin-bottom: 18px;
                        }
                        .steps-title {
                            font-size: 14px;
                        }
                        .steps-list li {
                            font-size: 13px; /* Bullet items chote kiye mobile layout fit karne ke liye */
                            margin-bottom: 12px;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="success-card">
                    <h2 class="success-title">🏛️ Account Recovery Request Logged Successfully!</h2>
                    <p class="success-desc">
                        Your manual identity verification parameters (Full Name and Mobile verification profile) 
                        have been safely transmitted to the CodeIn Security Operations Dashboard.
                    </p>
                    
                    <div class="steps-title">Next Steps:</div>
                    <ul class="steps-list">
                        <li>1. Our systems will cross-verify these details against your registered cloud profile signatures.</li>
                        <li>2. Upon validation, the platform administrator will manual-reset your credentials to a temporary password template.</li>
                        <li>3. An update status notification will be processed for your account within <span class="bold-text">24 business hours</span>. You can close this tab now.</li>
                    </ul>
                </div>
            </body>
            </html>
            """
            return HttpResponse(success_html)
        else:
            return render(request,'request_user.html',{'f':f})
    f=Request_User_Form(initial={'message':default})
    return render(request,'request_user.html',{'f':f})
