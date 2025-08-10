import asyncio
import threading
from asyncio import gather, run, sleep
from base64 import b85decode, b85encode
from contextlib import suppress
from datetime import UTC, datetime
from os import urandom
from queue import Empty, Queue
from threading import Thread
from typing import Any, Self, override

from pydantic import ValidationError

from secure.signature import sign, verify
from settings.settings import Settings

def get_file_names() -> list:
    return ["1wvefeeqfefweeeee.png", "2.mp3", "3.mov"]