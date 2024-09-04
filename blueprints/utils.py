from uuid import uuid4

from telethon.tl.types import MessageMediaDocument, DocumentAttributeFilename


def get_file_name(media_document: MessageMediaDocument) -> str:
    if media_document.document.mime_type == 'audio/ogg':
        return str(uuid4()) + '.ogg'

    if media_document.document:
        for attribute in media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeFilename):
                return attribute.file_name
