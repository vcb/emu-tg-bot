# EMUbot
Tiny Telegram bot for monitoring an Airam/Tuya door sensor status.

## Features
The `tuya_util` provides a simple script for monitoring an Airam/Tuya door sensor status. It listens for UDP broadcasts from the sensor and make a local request to the sensor to get the status. 

This is used as a trigger for the checkup since the device is powered off most of the time. 

You'll need the device's local encryption key for this, which is easiest to get from the Tuya Cloud API. Note that reinitializing the device will change the key.

## Usage
- `/door` - Check the status of the door sensor

## Installation
1. Clone the repository
2. Install the requirements `pip install -r requirements.txt`
3. Create a `.env` file with the following content:
```
DEVICE_IP=<your_device_ip>
DEVICE_ID=<your_device_id>
DEVICE_KEY=<your_device_secret>
TG_KEY=<your_telegram_bot_key>
```
4. Run the bot `python bot.py`