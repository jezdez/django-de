from django.db import models

class EntryManager(models.Manager):

    def get_jobs(self):
        return self.filter(job_type=1).exclude(verified=False).order_by('-published')

    def get_developer(self):
        return self.filter(job_type=2).exclude(verified=False).order_by('-published')