# -*- coding: utf-8 -*-

from contextlib import contextmanager
import datetime
from pathlib import Path
import phonenumbers
import sqlite3

from ipbridge.contacts import contacts

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


def _merge_same_chats(chats):
    all_contacts = contacts.get_contacts()

    def _id_for_handle(handle):
        for contact in all_contacts:
            for mail in contact.email_addresses:
                if mail == handle['id']:
                    return contact
            try:
                handle_number = phonenumbers.parse(handle['id'])
            except phonenumbers.NumberParseException:
                continue
            if not phonenumbers.is_valid_number(handle_number):
                continue
            for number in contact.phone_numbers:
                try:
                    contact_number = phonenumbers.parse(
                        number['value'], number['country_code']
                    )
                except phonenumbers.NumberParseException:
                    continue
                if not phonenumbers.is_valid_number(contact_number):
                    continue
                if contact_number == handle_number:
                    return contact
        return handle['id']

    final_chats = []
    potentially_mergable = []
    for chat in chats:
        if (
            chat['display_name'] is not None
            or chat['room_name'] is not None
            or len(chat['handles']) > 1
        ):
            final_chats.append(chat)
        else:
            potentially_mergable.append(chat)
    while True:
        if not potentially_mergable:
            break
        current = potentially_mergable.pop(0)
        current_id = _id_for_handle(current['handles'][0])

        to_remove = []
        for other in potentially_mergable:
            other_id = _id_for_handle(other['handles'][0])
            if current_id == other_id:
                current['ROWIDs'].append(other['ROWIDs'][0])
                to_remove.append(other)
        final_chats.append(current)
        potentially_mergable = [
            v for v in potentially_mergable if v not in to_remove
        ]
    return final_chats


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
            'SELECT chat_id FROM chat_message_join GROUP BY chat_id '
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

            # Make a list of ROWIDs, since chats can be merged
            chat['ROWIDs'] = [chat['ROWID']]
            del chat['ROWID']
            chats.append(chat)

        chats = _merge_same_chats(chats)

        def lastMessageSorter(item):
            return datetime.datetime.fromisoformat(item['last_message'])

        chats.sort(key=lastMessageSorter, reverse=True)

        return chats
