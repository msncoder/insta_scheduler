from celery import shared_task
from .models import ScheduledPost, InstagramAccount
from django.utils import timezone
import requests

@shared_task
def publish_scheduled_posts():
    posts = ScheduledPost.objects.filter(is_published=False, scheduled_time__lte=timezone.now())
    for post in posts:
        try:
            account = InstagramAccount.objects.get(user=post.user)
            access_token = account.access_token
            ig_user_id = account.fb_user_id  # May need to get Instagram ID via API

            # Create media container
            create_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
            data = {
                'image_url': post.image_url,
                'caption': post.caption,
                'access_token': access_token
            }
            res = requests.post(create_url, data=data)
            creation_id = res.json().get('id')

            # Publish media
            publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
            publish_data = {
                'creation_id': creation_id,
                'access_token': access_token
            }
            pub_res = requests.post(publish_url, data=publish_data)

            if pub_res.status_code == 200:
                post.is_published = True
                post.save()
        except Exception as e:
            print("Error posting:", e)
