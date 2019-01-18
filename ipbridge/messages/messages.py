# -*- coding: utf-8 -*-

from contextlib import contextmanager
import datetime
from pathlib import Path
import sqlite3

MESSAGES_DB = Path.home() / 'Library' / 'Messages' / 'chat.db'

CHAT_PROPERTIES = [
    'ROWID',
    'account_login',
    'service_name',
    'room_name',
    'display_name',
    'chat_identifier',
]

HANDLE_PROPERTIES = ['ROWID', 'uncanonicalized_id', 'id']


@contextmanager
def connect_db():
    connection = sqlite3.connect(MESSAGES_DB)
    connection.row_factory = sqlite3.Row
    yield connection
    connection.close()


def get_chats():
    with connect_db() as connection:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT chat_id '
            'FROM chat_message_join '
            'GROUP BY chat_id '
        )

        chats = []
        for chatID in cursor.fetchall():
            cursor.execute('SELECT * FROM chat WHERE ROWID = ?', chatID)
            chat = cursor.fetchone()
            chat = {
                k: (chat[k] if chat[k] else None)
                for k in chat.keys()
                if k in CHAT_PROPERTIES
            }

            cursor.execute(
                'SELECT message_id '
                'FROM chat_message_join '
                'INNER JOIN message '
                'ON chat_message_join.message_id = message.ROWID '
                'WHERE chat_id = ? '
                'ORDER BY message_id DESC LIMIT 1',
                chatID,
            )
            msgID = cursor.fetchone()

            cursor.execute('SELECT date FROM message WHERE ROWID = ?', msgID)
            msg = cursor.fetchone()

            dateInt = msg['date']
            if dateInt > 10000000000:
                dateInt = dateInt / 1000000000
            refDate = datetime.datetime(
                2001, 1, 1, tzinfo=datetime.timezone.utc
            )
            msgDate = refDate + datetime.timedelta(seconds=dateInt)

            chat['last_message'] = msgDate.isoformat()

            chat['handles'] = []
            cursor.execute(
                'SELECT handle_id FROM chat_handle_join WHERE chat_id = ?',
                chatID,
            )

            for handleID in cursor.fetchall():
                cursor.execute(
                    'SELECT * FROM handle WHERE ROWID = ?', handleID
                )
                handle = cursor.fetchone()
                handle = {
                    k: handle[k]
                    for k in handle.keys()
                    if k in HANDLE_PROPERTIES
                }
                chat['handles'].append(handle)
            chats.append(chat)

        def lastMessageSorter(item):
            return datetime.datetime.fromisoformat(item['last_message'])

        chats.sort(key=lastMessageSorter, reverse=True)
        return chats
