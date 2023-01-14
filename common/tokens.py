"""
token.py
Custom token generating methods for the project.
"""

from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens(user, tokenClass):
    jwt = tokenClass.for_user(user)
    jwt['email'] = user.email
    return jwt

def generate_auth_tokens(user):
    token_class = RefreshToken
    tokens = generate_tokens(user, token_class)
    refresh_token = str(tokens)
    access_token = str(tokens.access_token)
    return refresh_token, access_token