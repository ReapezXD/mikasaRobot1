from __future__ import unicode_literals
import asyncio
import math
import io
import os
import time
import requests
import wget
import yt_dlp
from telethon import types
from urllib.parse import urlparse
from DestinyBot import EVENT_LOGS, LOGGER
from pyrogram import filters
from pyrogram.types import Message
from DestinyBot.utils.pluginhelper import get_text, progress
from DestinyBot import pbot
from ShazamAPI import Shazam
from DestinyBot.modules.helper_funcs.managers import edit_delete, edit_or_reply
from DestinyBot.modules.helper_funcs.tools import media_type
from DestinyBot.events import register


@register(pattern=r"^/shazam")
async def shazamcmd(event):
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "Reply to Voice clip or Audio clip to reverse search that song."
        )
    unmei_event = await edit_or_reply(event, "Downloading the audio clip...")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.download_media(
            reply.document,
            dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGGER.error(e)
        return await edit_delete(
            unmei_event, f"Error while reverse searching song:\n{e}"
        )

    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"Song: {song}", reply_to=reply
    )
    await unmei_event.delete()


__mod_name__ = "Sʜᴀᴢᴀᴍ ⚡"

__help__ = """
*Shazam*
 ✮ `/shazam`*:* reply to a mp3 media file to reverse search a song.

It is used in case you receive a media and doesn't know it's name.
`Video to mp3 conversion will be added soon...`
"""
