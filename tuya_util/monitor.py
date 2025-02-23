import asyncio
import socket
import threading
from typing import Optional

import tinytuya
import logging

UDP_PORT = 6667  # The Tuya device broadcasts on this port when powered on.
DPS_ID_DOOR = "1"  # Packet ID for door status.


class TuyaSensor:
    def __init__(self, ip: str, dev_id: str, local_key: str):
        """
        Initializes the Tuya sensor with given device IP, ID, and local key.
        """
        self.device_ip = ip
        self.device_id = dev_id
        self.local_key = local_key
        self.last_status = None

        # Initialize the Tuya device
        self.device = tinytuya.OutletDevice(
            dev_id=self.device_id,
            address=self.device_ip,
            local_key=self.local_key,
            version=3.3,
            persist=False,
        )

        # Bind UDP socket for listening
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", UDP_PORT))

    def get_status(self) -> Optional[bool]:
        """
        Returns the last known status of the Tuya device.
        :return: True if the door is open, False if the door is closed, None if the status is unknown.
        """
        if self.last_status is None:
            return None
        if "dps" not in self.last_status or DPS_ID_DOOR not in self.last_status["dps"]:
            return None

        return self.last_status["dps"][DPS_ID_DOOR]

    def connect(self):
        """
        Starts the listening loop in the background without blocking execution.
        Runs `_loop()` in a separate thread to avoid asyncio conflicts.
        """
        def run():
            asyncio.run(
                self._loop())  # Run _loop() in its own asyncio event loop

        thread = threading.Thread(target=run,
                                  daemon=True)  # Run in a background thread
        thread.start()
        logging.info("Tuya device loop started in a background thread.")

    async def _update_status(self):
        """
        Sends a status request to the Tuya device and updates the last known status.
        """
        logging.debug("Sent status request.")
        status = self.device.status()

        if status is None:
            logging.error("Failed to get device status.")
            return
        if "Error" in status:
            logging.error(
                f"Failed to get device status, error: {status['Error']} ({status['Err']})")
            return

        self.last_status = status
        logging.info(f"Door is: {'OPEN' if status['dps'][DPS_ID_DOOR] else 'CLOSED'}")

    async def _loop(self):
        """
        Listens for UDP broadcasts from the Tuya device and triggers status updates.
        """
        logging.debug("Listening for device broadcasts...\n------------------")
        while True:
            data, addr = self.sock.recvfrom(1024)
            if addr[0] == self.device_ip:
                logging.debug("Device powered on, updating status...")
                await self._update_status()

# Example Usage:
# sensor = TuyaSensor(ip="192.168.1.100", dev_id="device_id_here", local_key="local_key_here")
# asyncio.run(sensor.connect())