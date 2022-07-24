from sqlalchemy import and_

from utils.db_api.models import Favorite, News


async def add_user_favorite(user, favorite):
    favorite_companion = await Favorite.query.where(
        and_(Favorite.user_id == user.id, Favorite.favorite_id == favorite.id)).gino.first()
    if favorite_companion:
        return False
    return await Favorite.create(user_id=user.id, favorite_id=favorite.id)


async def get_user_favorites(user):
    return await Favorite.query.where(Favorite.user_id == user.id).gino.all()


async def add_news(**kwargs):
    return await News.create(**kwargs)


async def get_last_news():
    return await News.query.gino.first()

