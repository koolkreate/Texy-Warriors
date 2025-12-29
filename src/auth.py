import jwt
import os
from flask import request, abort

"""
This file contains helper functions for authentication
"""

def getCurrentUser():
    """Gets the current user if it exists, else returns a 401 error
    
    For context Superbase can use JWT to handle authentication which 
    apparantly is better for practice
    
    """
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

#Wrapper to ensure only logged in user can access different endpoints
def loginRequired(f):
    def wrapper(*args, **kwargs):
        user = getCurrentUser()
        if not user:
            abort(401)
        return f(user, *args, **kwargs)