from typing import List
from utils.db_api.models import User


async def get_users() -> List:
    return await User.query.gino.all()


async def add_user(**kwargs):
    user = await User.query.where(User.user_id == kwargs.get('user_id')).gino.first()
    if user:
        return False
    return await User.create(**kwargs)



async def get_user_by_id(id) -> User:
    return await User.query.where(User.id == id).gino.first()


async def get_user_by_user_id(user_id) -> User:
    return await User.query.where(User.user_id == int(user_id)).gino.first()


async def increase_reputation(user) -> int:
    await user.update(reputation=user.reputation + 1).apply()
    return user.reputation
