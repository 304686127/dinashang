# coding=utf-8
from dianshang import settings
import os
import time
import usercenter.config as config
import random


class UploadMediaManager:
    def __init__(self):
        self.BASE_DIR = os.path.join(settings.BASE_DIR, 'assets', 'media')

    def save(self, media_type, media_data):
        filename = 'fulltext_' + time.strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999)) + '.jpg'
        store_path = os.path.join(self.BASE_DIR, media_type, filename)
        with open(store_path, 'wb') as fp:
            fp.write(media_data.read())
        return '{protocol}://{domain}/assets/media/{type}/{filename}'.format(
            protocol=config.PROTOCOL,
            domain=config.DOMAIN,
            type=media_type,
            filename=filename
        )
