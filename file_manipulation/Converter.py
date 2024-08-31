from typing import BinaryIO

from pydub import AudioSegment
from io import BytesIO
import mutagen
import os

async def auto_to_mp3(filename) -> (str, BinaryIO):
    file_name = filename.split('.')[0]
    file_extension = filename.split('.')[-1]
    try:
        if file_extension == 'opus':
            opus_file = BytesIO(open(filename, 'rb').read())
            file = AudioSegment.from_file(opus_file, codec='opus')
            file.export(f'{file_name}.mp3', format="mp3")

        else:
            if file_extension == 'mp3':
                return f'{file_name}.mp3', open(f'{file_name}.mp3', 'rb')

            file = AudioSegment.from_file(filename, format=file_extension)
            file.export(f'{file_name}.mp3', format="mp3")

        return f'{file_name}.mp3', open(f'{file_name}.mp3', 'rb')

    except:
        raise ValueError("Error converting file")

async def get_duration(filename):
    try:
        file = mutagen.File(filename)
        return file.info.length

    except Exception:
        return -1

async def remove_file(file_path):
    os.remove(file_path)