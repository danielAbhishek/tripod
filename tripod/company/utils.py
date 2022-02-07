def staff_check(user):
    return user.is_staff


def superuser_check(user):
    return user.is_superuser
