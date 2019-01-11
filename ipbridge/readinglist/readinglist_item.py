# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional


class ReadinglistItem:
    title: str
    url: str
    image_url: Optional[str]
    date: datetime
    preview: str

    def __init__(
        self,
        title: str,
        url: str,
        image_url: Optional[str],
        date: datetime,
        preview: Optional[str],
    ):
        self.title = title
        self.url = url
        self.image_url = image_url
        self.date = date
        self.preview = preview or self.title

    def serialize(self):
        return {
            'title': self.title,
            'url': self.url,
            'image_url': self.image_url,
            'date': self.date,
            'preview': self.preview,
        }
