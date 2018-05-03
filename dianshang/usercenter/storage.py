from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import time
import random


class ImageStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        fn = 'model_' + time.strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999))
        name = os.path.join(d, fn + ext)
        return super(ImageStorage, self)._save(name, content)
