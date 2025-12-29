import jwt
import os
from flask import request, abort

def getCurrentUser():
    authHeader = request.headers.get("Authorization")

    if not authHeader or not authHeader.startswith("Bearer "):
        abort(401, "Missing token")

    authHeaderParts = authHeader.split()
    token = authHeaderParts[1]

    try:
        return jwt.decode(
            token,
            os.getenv("SUPABASE_JWT_SECRET"),
            algorithms=["HS256"],
            audience="authenticated"
        )
    except jwt.ExpiredSignatureError:
        abort(401, "Token expired")
    except jwt.InvalidTokenError:
        abort(401, "Invalid token")

def loginRequired(f):
    def wrapper(*args, **kwargs):
        user = getCurrentUser()
        if not user:
            abort(401)
        return f(user, *args, **kwargs)