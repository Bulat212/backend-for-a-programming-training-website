from django.db.models import Sum
from django.utils import timezone

from app import settings
from users.models import ProgressLog, UserProgress, UserSkill

def update_user_progress(user, language, experience=0, coins=0, stars=0):
    user_progress = UserProgress.objects.filter(user=user).order_by('-date').first()
    user_skills = UserSkill.objects.filter(user=user, language=language).first() if language else None

    current_experience = user_progress.experience if user_progress else 0
    current_stars = user_progress.stars if user_progress else 0
    
    if user_progress and user_progress.date==timezone.now().date():
        new_user_progress = user_progress
    else:
        new_user_progress = UserProgress.objects.create(user=user, date=timezone.now().date())

    if user_skills:
        user_skills.experience += experience
        user_skills.save()
    elif language:
        user_skills = UserSkill.objects.create(user=user, language=language, experience=experience)

    new_user_progress.experience = experience + current_experience
    new_user_progress.stars = stars + current_stars
    new_user_progress.save()

    user.experience = experience + current_experience
    user.stars = stars + current_stars
    user.coins += coins
    user.save()

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

    current_user_data = None
    current_user_position = None
    if current_user:
  
        for index, user in enumerate(users):
            if user['user__id'] == current_user.id:
                current_user_position = index + 1
                current_user_data = user
                break

        if not current_user_data:

            if rank_type == "experience":
                current_user_query = ProgressLog.objects.filter(user=current_user, **filters).values(
                    'user__id', 'user__username', 'user__photo', 'user__nickname_id'
                ).annotate(total_experience=Sum('experience_change')).order_by('-total_experience')
            elif rank_type == "stars":
                current_user_query = ProgressLog.objects.filter(user=current_user, **filters).values(
                    'user__id', 'user__username', 'user__photo', 'user__nickname_id'
                ).annotate(total_stars=Sum('stars_change')).order_by('-total_stars')
            else:
                current_user_query = ProgressLog.objects.none()

            if current_user_query.exists():  # Проверяем QuerySet
                current_user_data = current_user_query.first()
            else:
                current_user_data = {
                    "user__id": current_user.id,
                    "user__username": current_user.username,
                    "user__photo": getattr(current_user, "photo", None),
                    "user__nickname_id": getattr(current_user, "nickname_id_id", None),
                    "total_experience": 0 if rank_type == "experience" else None,
                    "total_stars": 0 if rank_type == "stars" else None,
                }

        current_user_data['position'] = current_user_position

    if limit:
        users = users[:limit]

    return {'users':users, 'current_user':current_user_data}


def update_or_create_user_skill(user, language, experience=0):
    user_skill, created = UserSkill.objects.get_or_create(user=user, language=language)

    user_skill.experience += experience
    user_skill.save()
    
    return user_skill


def build_photo_url(user_photo, self, obj):
    if not user_photo:
        return None
    request = self.context.get('request')
    if request:
        return request.build_absolute_uri(f"{settings.MEDIA_URL}{user_photo}")
    
    return f"{settings.MEDIA_URL}{user_photo}"
