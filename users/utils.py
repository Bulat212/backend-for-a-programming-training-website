from django.db.models import Sum
from django.utils import timezone

from users.models import ProgressLog, UserProgress, UserSkill

def update_user_progress(user, experience=0, stars=0):
    
    user_progress = UserProgress.objects.filter(user=user).order_by('-date').first()

    current_experience = user_progress.experience if user_progress else 0
    current_stars = user_progress.stars if user_progress else 0
    
    if user_progress and user_progress.date==timezone.now().date():
        new_user_progress = user_progress
    else:
        new_user_progress = UserProgress.objects.create(user=user, date=timezone.now().date())

    new_user_progress.experience = experience + current_experience
    new_user_progress.stars = stars + current_stars
    new_user_progress.save()

    if experience != 0 or stars != 0: 
        ProgressLog.objects.create(user=user, experience_change=experience, stars_change=stars)

    return new_user_progress


def get_ranking(rank_type, period, limit=None, current_user=None):
    
    today = timezone.now()
    if period == "week":
        first_day = today.weekday()
        start_data = (today - timezone.timedelta(days=first_day)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "month":
        start_data = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "all_time":
        start_data = None
        
    filters = {}

    if start_data:
        filters['date__gte'] = start_data

    if rank_type=="experience":
        filters['experience_change__gt']=0
        users = ProgressLog.objects.filter(**filters).values('user__id', 'user__username', 'user__photo', 'user__nickname_id').annotate(
            total_experience = Sum('experience_change')).order_by('-total_experience')
    elif rank_type=='stars':
        filters['stars_change__gt']=0
        users = ProgressLog.objects.filter(**filters).values('user__id', 'user__username', 'user__photo', 'user__nickname_id').annotate(
            total_stars = Sum('stars_change')).order_by('-total_stars')
    
    if limit:
        users = users[:limit]

    current_user_data = None
    if current_user:
        if rank_type == "experience":
            current_user_data = ProgressLog.objects.filter(user=current_user, **filters).values(
                'user__id', 'user__username', 'user__photo', 'user__nickname_id'
            ).annotate(total_experience=Sum('experience_change')).order_by('-total_experience')
        elif rank_type == "stars":
            current_user_data = ProgressLog.objects.filter(user=current_user, **filters).values(
                'user__id', 'user__username', 'user__photo', 'user__nickname_id'
            ).annotate(total_stars=Sum('stars_change')).order_by('-total_stars')

        if current_user_data.exists():
            current_user_data = current_user_data.first()
        else:
            current_user_data = {
                "user__id": current_user.id,
                "user__username": current_user.username,
                "user__photo": getattr(current_user, "photo", None),
                "user__nickname_id": getattr(current_user, "nickname_id", None),
                "total_experience": 0 if rank_type == "experience" else None,
                "total_stars": 0 if rank_type == "stars" else None,
            }

    return {'users':users, 'current_user':current_user_data}


def update_or_create_user_skill(user, language, experience=0):
    user_skill, created = UserSkill.objects.get_or_create(user=user, language=language)

    user_skill.experience += experience
    user_skill.save()
    
    return user_skill
