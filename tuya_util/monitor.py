import asyncio
import socket
import threading
from typing import Optional

import tinytuya
import logging

UDP_PORT = 6667  # The Tuya device broadcasts on this port when powered on.
DPS_ID_DOOR = "1"  # Packet ID for door status.

class TuyaSensor:
    def __init__(self, ip: str, dev_id: str, local_key: str, api_key: str, api_secret: str):
        """
        Initializes the Tuya sensor with given device IP, ID, and local key.
        """
        self.c = tinytuya.Cloud(
            apiRegion="eu",
            apiKey=api_key,
            apiSecret=api_secret,
            apiDeviceID=dev_id,
        )

        self.device_ip = ip
        self.device_id = dev_id
        self.local_key = local_key
        self.last_status = None

    def get_status(self) -> Optional[bool]:
        """
        Returns the last known status of the Tuya device.
        :return: True if the door is open, False if the door is closed, None if the status is unknown.
        """

        res = self.c.getstatus(self.device_id)
        if res is None:
            return None

        try:
            if res['result'][0]['code'] != 'doorcontact_state':
                logging.error("Unknown result value")
                return None

            return res['result'][0]['value']
        except any as e:
            logging.error(e)
            return None

# Example Usage:
# sensor = TuyaSensor(ip="192.168.1.100", dev_id="device_id_here", local_key="local_key_here")
# asyncio.run(sensor.connect())