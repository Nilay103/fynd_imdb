import uuid
from datetime import datetime, timedelta

import jwt
from passlib.handlers.sha2_crypt import sha256_crypt
from sanic import response

from constants import SECRET_KEY
from models import User


async def signup(request):
    user = request.json

    if not user.get('email') or not user.get('name') or not user.get('password'):
        return response.json({'data': 'Please enter valid information.'}, status=412)

    if (await User.find_one(
            {"email": user['email']}, as_raw=True)
    ) is not None:
        return response.json({'data': 'User Already Exists'}, status=412)

    user["_id"] = uuid.uuid4().hex
    user["password"] = sha256_crypt.hash(user['password'])

    new_movie = await User.insert_one(user)
    user = await User.find_one(
        {"_id": new_movie.inserted_id}, as_raw=True
    )

    return response.json(user)


async def login(request):
    user = request.json
    if (db_user := await User.find_one(
            {
                "email": user['email']
            }, as_raw=True)
    ) is not None:
        try:
            sha256_crypt.verify(db_user['password'], sha256_crypt.hash(user['password']))
        except:
            return response.json({'data': 'user not found'}, status=412)

        token = jwt.encode({
            'user': user['name'],
            'expiration': str(datetime.utcnow() + timedelta(hours=1))
        }, SECRET_KEY)
        return response.json({
            'token': token.decode('utf-8'),
            'user': db_user
        }, status=201)

    return response.json({'data': 'user not found'}, status=412)
