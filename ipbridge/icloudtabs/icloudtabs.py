# -*- coding: utf-8 -*-
import json
import pathlib
import subprocess

_this_file = pathlib.Path(__file__)
_xpc_helper_dir = _this_file.parent.absolute() / 'safari-icloud-tabs-fetcher'
_xpc_helper = _xpc_helper_dir / 'safari-icloud-tabs-fetcher'


def get_icloud_tabs() -> dict:
    try:
        text = subprocess.check_output(
            str(_xpc_helper), universal_newlines=True
        )
    except subprocess.SubprocessError:
        text = '{"Tabs":[]}'
    return json.loads(text)
