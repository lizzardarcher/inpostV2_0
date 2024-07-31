from .models import Notification, UserStatus


def get_notifications(request):
    try:
        status_of_user = UserStatus.objects.filter(user_id=request.user.id)[0]
    except:
        status_of_user = ""
    return {
        'notifications': Notification.objects.all()[:15],
        'status_of_user': status_of_user
            }
