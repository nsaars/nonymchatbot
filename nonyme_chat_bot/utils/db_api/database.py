from gino import Gino
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URI

db = Gino()


async def create_db_connection():
    print('db creating...')
    db.gino: GinoSchemaVisitor
    await db.set_bind(POSTGRES_URI)
    await db.gino.create_all()
