from django.core.management.base import BaseCommand
from style.models import Style, Category

class Command(BaseCommand):
    help = 'Импортирует стили из ALL_STYLES.JS'

    def handle(self, *args, **options):
        # Данные из ALL_STYLES.JS
        ALL_STYLES = [
            {"id": 9, "name": "Rainbow Animation", "priceInCoin": 2600, "priceInStars": 0, "className": "rainbow_animation_nickname", "category": "nickname"},
            {"id": 1, "name": "Neon Blue", "priceInCoin": 500, "priceInStars": 0, "className": "neon_blue_nickname", "category": "nickname"},
            {"id": 2, "name": "Cyber Red", "priceInCoin": 700, "priceInStars": 0, "className": "cyber_red_nickname", "category": "nickname"},
            {"id": 3, "name": "Glowing Green", "priceInCoin": 600, "priceInStars": 0, "className": "glowing_green_nickname", "category": "nickname"},
            {"id": 4, "name": "Gold Shine", "priceInCoin": 0, "priceInStars": 6, "className": "gold_shine_nickname", "category": "nickname"},
            {"id": 5, "name": "Shadow Purple", "priceInCoin": 0, "priceInStars": 3, "className": "shadow_purple_nickname", "category": "nickname"},
            {"id": 6, "name": "Electric Pink", "priceInCoin": 0, "priceInStars": 2, "className": "electric_pink_nickname", "category": "nickname"},
            {"id": 7, "name": "Frost White", "priceInCoin": 0, "priceInStars": 4, "className": "frost_white_nickname", "category": "nickname"},
            {"id": 8, "name": "Fire Orange", "priceInCoin": 2, "priceInStars": 0, "className": "fire_orange_nickname", "category": "nickname"},
            {"id": 10, "name": "Underline Animation", "priceInCoin": 0, "priceInStars": 15, "className": "wave_underline_nickname", "category": "nickname"},
            {"id": 11, "name": "Typing Animation", "priceInCoin": 0, "priceInStars": 2, "className": "typing_text_nickname", "category": "nickname"},
            {"id": 12, "name": "Anim Nickname", "priceInCoin": 0, "priceInStars": 7, "className": "anim_nickname", "category": "nickname"},
            {"id": 13, "name": "Fire Style", "priceInCoin": 0, "priceInStars": 20, "category": "background_profile"},
            {"id": 14, "name": "Snow Style", "priceInCoin": 0, "priceInStars": 10, "category": "background_profile"},
            {"id": 15, "name": "Laser Style", "priceInCoin": 0, "priceInStars": 25, "category": "background_profile"},
        ]

        # Убедимся, что категории существуют
        Category.objects.get_or_create(name='nickname')
        Category.objects.get_or_create(name='background_profile')  # Или замените на 'background', если нужно

        for style_data in ALL_STYLES:
            category = Category.objects.get(name=style_data['category'])
            Style.objects.update_or_create(
                id=style_data['id'],
                defaults={
                    'name': style_data['name'],
                    'price_in_coin': style_data['priceInCoin'],
                    'price_in_stars': style_data['priceInStars'],
                    'category': category,
                    'is_available': True  # Установите False, если стили нужно активировать вручную
                }
            )
            self.stdout.write(self.style.SUCCESS(f"Добавлен стиль: {style_data['name']}"))