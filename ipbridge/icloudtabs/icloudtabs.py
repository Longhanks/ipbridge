# -*- coding: utf-8 -*-
import json
import pathlib
import subprocess

_this_file = pathlib.Path(__file__)
_xpc_helper_dir = _this_file.parent.absolute() / 'safari-icloud-tabs-fetcher'
_xpc_helper = _xpc_helper_dir / 'safari-icloud-tabs-fetcher'


def get_icloud_tabs() -> list:
    try:
        text = subprocess.check_output(
            str(_xpc_helper), universal_newlines=True
        )
    except subprocess.SubprocessError:
        text = '[]'
    devices = json.loads(text)
    icloud_tabs = []
    for device in devices:
        device_dict = {'DeviceName': device['DeviceName'], 'Tabs': []}
        for tab in device['Tabs']:
            device_dict['Tabs'].append({'Title': tab['Title'], 'URL': tab['URL']})
        icloud_tabs.append(device_dict)
    return icloud_tabs
