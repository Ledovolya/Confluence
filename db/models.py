from django.db import models
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.postgres.fields.jsonb import JSONField


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name,max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

