import os
from datetime import datetime
import pytz


def create_output_dirs(base_dir: str):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)


def get_nepal_time():
    nepal_tz = pytz.timezone('Asia/Kathmandu')  # Set Nepal Timezone
    return datetime.now(nepal_tz)
