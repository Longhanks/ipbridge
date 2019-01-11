# -*- coding: utf-8 -*-
from ctypes import (
    c_bool,
    c_char_p,
    c_int,
    c_ulong,
    c_void_p,
    addressof,
    byref,
    cast,
    sizeof,
    CDLL,
    CFUNCTYPE,
    POINTER,
    Structure,
)
import ctypes.util

libc = CDLL(ctypes.util.find_library("c"))
libobjc = CDLL(ctypes.util.find_library("objc"))

libobjc.objc_getClass.restype = c_void_p
libobjc.objc_getClass.argtypes = [c_char_p]

libobjc.sel_registerName.restype = c_void_p
libobjc.sel_registerName.argtypes = [c_char_p]

libobjc.objc_msgSend.restype = c_void_p
libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]


# from Block_private.h
_NSConcreteStackBlock = (c_void_p * 32).in_dll(libc, "_NSConcreteStackBlock")

BLOCK_HAS_COPY_DISPOSE = 1 << 25
BLOCK_HAS_STRET = 1 << 29
BLOCK_HAS_SIGNATURE = 1 << 30


class Block_descriptor(Structure):
    _fields_ = [
        ("reserved", c_ulong),
        ("size", c_ulong),
        ("copy", CFUNCTYPE(c_void_p, c_void_p, c_void_p)),
        ("dispose", CFUNCTYPE(c_void_p, c_void_p)),
        ("signature", c_char_p),
    ]


class Block_layout(Structure):
    _fields_ = [
        ("isa", c_void_p),
        ("flags", c_int),
        ("reserved", c_int),
        ("invoke", c_void_p),
        ("descriptor", c_void_p),
    ]


class EnumerateContactsBlock:

    _strong_refs = {}

    def __init__(self, func):
        self.func = func
        self.cfunc_type = CFUNCTYPE(None, c_void_p, c_void_p, POINTER(c_bool))
        self.block = Block_layout()
        self.block.isa = addressof(_NSConcreteStackBlock)
        self.block.flags = (
            BLOCK_HAS_COPY_DISPOSE | BLOCK_HAS_STRET | BLOCK_HAS_SIGNATURE
        )
        self.block.reserved = 0
        self.cfunc_invoke = self.cfunc_type(self.invoke)
        self.block.invoke = cast(self.cfunc_invoke, c_void_p)
        self.descriptor = Block_descriptor()
        self.descriptor.reserved = 0
        self.descriptor.size = sizeof(Block_layout)

        self.cfunc_copy = CFUNCTYPE(c_void_p, c_void_p, c_void_p)(self.copy)
        self.cfunc_dispose = CFUNCTYPE(c_void_p, c_void_p)(self.dispose)
        self.descriptor.copy = self.cfunc_copy
        self.descriptor.dispose = self.cfunc_dispose

        self.descriptor.signature = b"v@?^v^B"
        self.block.descriptor = cast(byref(self.descriptor), c_void_p)
        self.ptr = cast(byref(self.block), c_void_p)

    def copy(self, dst, src):
        EnumerateContactsBlock._strong_refs[dst] = self

    def dispose(self, dst):
        EnumerateContactsBlock._strong_refs.pop(dst, None)

    def invoke(self, instance, *args):
        return self.func(*args)


def objc_class(name):
    return libobjc.objc_getClass(name.encode("utf-8"))


def objc_property(obj, property):
    libobjc.objc_msgSend.restype = c_void_p
    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
    return libobjc.objc_msgSend(obj, objc_selector(property))


def objc_selector(name):
    return libobjc.sel_registerName(name.encode("utf-8"))


def list_from_nsarray(nsarray):
    libobjc.objc_msgSend.restype = c_ulong
    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
    count = libobjc.objc_msgSend(nsarray, objc_selector("count"))
    libobjc.objc_msgSend.restype = c_void_p
    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p, c_ulong]
    return [
        libobjc.objc_msgSend(nsarray, objc_selector("objectAtIndex:"), i)
        for i in range(count)
    ]


def str_from_nsstring(nsstring):
    libobjc.objc_msgSend.restype = c_void_p
    libobjc.objc_msgSend.argtypes = [c_void_p, c_void_p]
    ns_void_ptr = libobjc.objc_msgSend(nsstring, objc_selector("UTF8String"))
    ns_ptr = cast(ns_void_ptr, c_char_p)
    return ns_ptr.value.decode("utf-8")


# Foundation classes
Foundation = CDLL(ctypes.util.find_library("Foundation"))

NSMutableArray = objc_class("NSMutableArray")


# Contacts classes
Contacts = CDLL(ctypes.util.find_library("Contacts"))

CNContactStore = objc_class("CNContactStore")
CNContactFetchRequest = objc_class("CNContactFetchRequest")
