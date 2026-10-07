# -*- coding: utf-8 -*-
# Test-only connection for the vyos.blueprints render tests.
#
# vyos.vyos resource modules ask the connection for the device's OS version
# (get_device_info) even for state=rendered. This connection is the real
# ansible.netcommon network_cli, except that it never opens SSH, reports a
# fixed VyOS version (vyos_offline_os_version, default 1.5) and refuses to
# send commands. Everything else - persistent-connection handling included -
# is inherited unchanged. It is named "network_cli" because the vyos.vyos
# action plugin only accepts connections whose name ends in network_cli.
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import yaml

from ansible.errors import AnsibleConnectionFailure
from ansible_collections.ansible.netcommon.plugins.connection import network_cli as _real

_doc = yaml.safe_load(_real.DOCUMENTATION)
_doc["short_description"] = "Offline network_cli for render tests (never connects)"
_doc["options"]["os_version"] = {
    "type": "str",
    "default": "1.5",
    "description": ["VyOS major version reported to the modules."],
    "vars": [{"name": "vyos_offline_os_version"}],
}
DOCUMENTATION = yaml.safe_dump(_doc)


class Connection(_real.Connection):
    transport = "blueprints_test.offline.network_cli"

    def _connect(self):
        # no SSH session; mark the connection usable for the persistent server
        self._connected = True

    def get_device_info(self):
        version = str(self.get_option("os_version"))
        return {
            "network_os": "vyos",
            "network_os_version": version,
            "network_os_major_version": version,
            "network_os_model": "offline",
            "network_os_hostname": "offline",
        }

    def get_capabilities(self):
        # The real one asks the cliconf plugin, which runs "show version".
        import json

        return json.dumps({
            "device_info": self.get_device_info(),
            "network_api": "cliconf",
            "rpc": [],
            "device_operations": {},
        })

    def send(self, *args, **kwargs):
        raise AnsibleConnectionFailure("offline render connection: commands cannot be sent to a device")

    def close(self):
        self._connected = False
