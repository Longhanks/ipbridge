# -*- coding: utf-8 -*-
import base64
from typing import Dict, List, Optional

from flask import current_app
from flask.helpers import get_debug_flag

if not get_debug_flag():
    from ctypes import c_bool, c_char_p, c_ulong, c_void_p

    from .objc import (
        libobjc,
        objc_property,
        objc_selector,
        Contacts,
        CNContactFetchRequest,
        CNContactStore,
        EnumerateContactsBlock,
        NSBitmapImageRep,
        NSImage,
        NSMutableArray,
        NSString,
        list_from_nsarray,
        str_from_nsstring,
    )


class Contact(object):
    def __init__(
        self,
        given_name: str,
        family_name: str,
        nick_name: Optional[str],
        phone_numbers: List[Dict[str, str]],
        email_addresses: List[str],
        image_data: Optional[str],
    ):
        self.given_name = given_name
        self.family_name = family_name
        self.nick_name = nick_name
        self.phone_numbers = phone_numbers
        self.email_addresses = email_addresses
        self.image_data = image_data

    def __eq__(self, other):
        if isinstance(other, Contact):
            return (
                self.given_name == other.given_name
                and self.family_name == other.family_name
                and self.nick_name == other.nick_name
                and self.phone_numbers == other.phone_numbers
                and self.email_addresses == other.email_addresses
                and self.image_data == other.image_data
            )
        return NotImplemented

    def __str__(self):
        display_name = ''
        if self.given_name:
            display_name = self.given_name
        if self.family_name:
            if not self.given_name:
                display_name = self.family_name
            else:
                display_name = display_name + ' ' + self.family_name
        if self.nick_name:
            if display_name:
                display_name = self.nick_name + ' (' + display_name + ')'
            else:
                display_name = self.nick_name

        display = display_name
        if self.phone_numbers or self.email_addresses:
            display = display + ': '

        display = display + ', '.join(
            [number['value'] for number in self.phone_numbers]
        )

        if self.phone_numbers and self.email_addresses:
            display = display + ', '

        display = display + ', '.join(self.email_addresses)
        return display

    def serialize(self):
        return {
            'given_name': self.given_name,
            'family_name': self.family_name,
            'nick_name': self.nick_name,
            'phone_numbers': self.phone_numbers,
            'email_addresses': self.email_addresses,
            'image_data': self.image_data
        }


def get_contacts():
    if get_debug_flag():
        contacts = []
        for i in range(5):
            contacts.append(
                Contact(
                    f'Testy #{i}',
                    'McTestFace',
                    'Tester',
                    [{'country_code': 'CH', 'value': '+41 44 668 18 00'}],
                    ['testy@tester.com'],
                    None,
                )
            )
        return contacts

    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
    libobjc.objc_msgSend.restype = c_void_p
    store = libobjc.objc_msgSend(
        libobjc.objc_msgSend(CNContactStore, objc_selector('alloc')),
        objc_selector('init'),
    )

    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_ulong]
    libobjc.objc_msgSend.restype = c_void_p
    keys = libobjc.objc_msgSend(
        NSMutableArray, objc_selector('arrayWithCapacity:'), c_ulong(7)
    )

    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
    libobjc.objc_msgSend.restype = None
    for key in [
        'CNContactNicknameKey',
        'CNContactGivenNameKey',
        'CNContactFamilyNameKey',
        'CNContactPhoneNumbersKey',
        'CNContactEmailAddressesKey',
        'CNContactImageDataAvailableKey',
        'CNContactImageDataKey',
    ]:
        libobjc.objc_msgSend(
            keys, objc_selector('addObject:'), c_void_p.in_dll(Contacts, key)
        )

    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
    libobjc.objc_msgSend.restype = c_void_p
    request_mem = libobjc.objc_msgSend(
        CNContactFetchRequest, objc_selector('alloc')
    )

    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
    libobjc.objc_msgSend.restype = c_void_p
    request = libobjc.objc_msgSend(
        request_mem, objc_selector('initWithKeysToFetch:'), keys
    )

    cncontacts = []

    def callback_contact(*args):
        cncontacts.append(args[0])

    block = EnumerateContactsBlock(callback_contact)

    libobjc.objc_msgSend.argtypes = [
        c_void_p,
        c_void_p,
        c_void_p,
        c_void_p,
        c_void_p,
    ]
    libobjc.objc_msgSend.restype = c_bool
    enumerate_succeeded = libobjc.objc_msgSend(
        store,
        objc_selector('enumerateContactsWithFetchRequest:error:usingBlock:'),
        request,
        None,
        block.ptr,
    )

    if not enumerate_succeeded:
        return []

    contacts = []
    for cncontact in cncontacts:
        given_name_ptr = objc_property(cncontact, 'givenName')
        given_name = str_from_nsstring(given_name_ptr)
        family_name_ptr = objc_property(cncontact, 'familyName')
        family_name = str_from_nsstring(family_name_ptr)
        nick_name_ptr = objc_property(cncontact, 'nickname')
        nick_name = str_from_nsstring(nick_name_ptr)
        phone_numbers = [
            {
                'country_code': str_from_nsstring(
                    objc_property(
                        objc_property(number, 'value'), 'countryCode'
                    )
                ).upper(),
                'value': str_from_nsstring(
                    objc_property(
                        objc_property(number, 'value'), 'stringValue'
                    )
                ),
            }
            for number in list_from_nsarray(
                objc_property(cncontact, 'phoneNumbers')
            )
        ]
        email_addresses = [
            str_from_nsstring(objc_property(email, 'value'))
            for email in list_from_nsarray(
                objc_property(cncontact, 'emailAddresses')
            )
        ]

        if (
            not given_name
            and not family_name
            and not nick_name
            and not phone_numbers
            and not email_addresses
        ):
            continue

        base64_str = None

        image_data_available = bool(
            objc_property(cncontact, 'imageDataAvailable')
        )

        if image_data_available:
            data_ptr = objc_property(cncontact, 'imageData')
            libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
            libobjc.objc_msgSend.restype = c_void_p
            image_mem = libobjc.objc_msgSend(NSImage, objc_selector('alloc'))
            libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
            image = libobjc.objc_msgSend(
                image_mem, objc_selector('initWithData:'), data_ptr
            )
            libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
            tiff_data = libobjc.objc_msgSend(
                image, objc_selector('TIFFRepresentation')
            )

            libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
            bitmap = libobjc.objc_msgSend(
                NSBitmapImageRep, objc_selector('imageRepWithData:'), tiff_data
            )

            NSBitmapImageFileTypePNG = c_ulong(4)
            libobjc.objc_msgSend.argtypes = [
                c_void_p,
                c_void_p,
                c_ulong,
                c_void_p,
            ]
            png_data = libobjc.objc_msgSend(
                bitmap,
                objc_selector('representationUsingType:properties:'),
                NSBitmapImageFileTypePNG,
                None,
            )

            libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_ulong]
            base64_nsstring = libobjc.objc_msgSend(
                png_data,
                objc_selector('base64EncodedStringWithOptions:'),
                c_ulong(0),
            )
            base64_str = str_from_nsstring(base64_nsstring)

            libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
            libobjc.objc_msgSend.restype = c_void_p
            libobjc.objc_msgSend(image, objc_selector('release'))

        contacts.append(
            Contact(
                given_name,
                family_name,
                nick_name,
                phone_numbers,
                email_addresses,
                base64_str,
            )
        )

    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
    libobjc.objc_msgSend.restype = c_void_p
    libobjc.objc_msgSend(store, objc_selector('release'))
    libobjc.objc_msgSend(request, objc_selector('release'))
    return contacts
