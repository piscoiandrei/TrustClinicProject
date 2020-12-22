from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


class BCrypt10x(BCryptSHA256PasswordHasher):
    iterations = BCryptSHA256PasswordHasher.rounds * 10
