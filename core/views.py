from django.shortcuts import redirect
import requests
from django.utils import timezone
from .models import InstagramAccount
from django.contrib.auth.decorators import login_required

FB_CLIENT_ID = '1966380890557042'
FB_CLIENT_SECRET = '371fda25820f19b04553a9188f69af70'
REDIRECT_URI = 'http://localhost:8000/facebook-callback/'

@login_required
def facebook_login(request):
    url = f"https://www.facebook.com/v19.0/dialog/oauth?client_id={FB_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=pages_show_list,instagram_basic,instagram_content_publish,pages_read_engagement"
    return redirect(url)

@login_required
def facebook_callback(request):
    code = request.GET.get('code')
    token_url = f"https://graph.facebook.com/v19.0/oauth/access_token?client_id={FB_CLIENT_ID}&redirect_uri={REDIRECT_URI}&client_secret={FB_CLIENT_SECRET}&code={code}"
    res = requests.get(token_url).json()
    access_token = res['access_token']

    user_info = requests.get(f"https://graph.facebook.com/me?access_token={access_token}").json()
    fb_user_id = user_info['id']

    InstagramAccount.objects.update_or_create(
        user=request.user,
        defaults={
            'fb_user_id': fb_user_id,
            'access_token': access_token,
            'token_expires': timezone.now() + timezone.timedelta(days=60)
        }
    )
    return redirect('dashboard')



from django.shortcuts import render
from .forms import ScheduledPostForm
from .models import ScheduledPost

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ScheduledPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = ScheduledPostForm()
    posts = ScheduledPost.objects.filter(user=request.user)
    return render(request, 'core/dashboard.html', {'form': form, 'posts': posts})
