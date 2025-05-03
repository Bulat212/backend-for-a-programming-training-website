def get_user_nickname(self, obj):
        users_nickname = self.context.get('users_nickname', None)
        if users_nickname:
            user_nick = users_nickname.filter(user=obj.user, is_active=True).first()
            return user_nick.style.id if user_nick else 0
        return 0