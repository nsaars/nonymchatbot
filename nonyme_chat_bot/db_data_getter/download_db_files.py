from sqlalchemy import and_
from utils.db_api.database import create_db_connection
from asyncio import get_event_loop
from utils.db_api.models import Media
import os


async def download_files():
    files = await Media.select('file', 'file_name').where(
        and_(Media.file_type != 'contact', Media.file_type != 'location')).gino.all()

    for file, file_name in files:
        folder_name = file_name.split('/')[0]
        file_name = file_name.split('/')[1]

        folder_path = fr'.\media\{folder_name}'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        file_path = fr'{folder_path}\{file_name}'
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as new_file:
                new_file.write(file)


loop = get_event_loop()
loop.run_until_complete(create_db_connection())
loop.run_until_complete(download_files())
