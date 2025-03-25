from django.db.models import Sum
from django.utils import timezone

from users.models import ProgressLog, UserProgress


def update_user_progress(user, experience=0, stars=0):
    
    user_progress = UserProgress.objects.filter(user=user).order_by('-date').first()

    current_experience = user_progress.experience if user_progress else 0
    current_stars = user_progress.stars if user_progress else 0
    
    new_user_progress, created = UserProgress.objects.get_or_create(user=user, date=timezone.now().date())

    new_user_progress.experience = experience + current_experience
    new_user_progress.stars = stars + current_stars
    new_user_progress.save()

    if experience != 0 or stars != 0: 
        ProgressLog.objects.create(user=user, experience_change=experience, stars_change=stars)

    return new_user_progress



def get_experiece_ranking(rank_type, period, limit=None):
    
    today = timezone.now()
    if period == "week":
        first_day = today.weekday()
        start_data = (today - timezone.timedelta(days=first_day)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "month":
        start_data = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
    if rank_type=="experience":
        users = ProgressLog.objects.filter(date__gte=start_data, experience_change__gt=0).values('user__id', 'user__username').annotate(
            total_experience = Sum('experience_change')).order_by('-total_experience')
    elif rank_type == "stars":
        users = ProgressLog.objects.filter(date__gte=start_data, stars_change__gt=0).values('user__id', 'user__username').annotate(
            total_stars = Sum('stars_change')).order_by('-total_stars')

    if limit:
        users = users[:limit]

    return users

