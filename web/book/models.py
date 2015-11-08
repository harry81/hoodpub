import requests
from requests import exceptions
from datetime import datetime
from django.db import models


class Book(models.Model):
    category = models.CharField(max_length=168)
    sale_yn = models.CharField(max_length=16)
    barcode = models.CharField(max_length=168)
    isbn = models.CharField(max_length=168, primary_key=True)
    isbn13 = models.CharField(max_length=168)
    cover_s_url = models.CharField(max_length=512)
    author = models.CharField(max_length=168)
    author_t = models.CharField(max_length=168)
    sale_price = models.CharField(max_length=168)
    title = models.CharField(db_index=True, max_length=168)
    translator = models.CharField(max_length=168)
    link = models.CharField(max_length=168)
    etc_author = models.CharField(max_length=128)
    pub_nm = models.CharField(max_length=128)
    list_price = models.CharField(max_length=168)
    ebook_barcode = models.CharField(max_length=168)
    cover_l_url = models.CharField(max_length=512)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    status_des = models.CharField(max_length=168)
    description = models.TextField()

    def __unicode__(self):
        return u'%s %s' % (self.pk, self.title)

    def rename_cover_url(self):
        if 'https' not in self.cover_s_url[0:5]:
            self.cover_s_url = self.cover_s_url.replace('http', 'https')
            try:
                resp = requests.get(self.cover_s_url)
            except exceptions.MissingSchema:
                return False
            if resp.status_code == 200:
                self.save()
                return True
        return False
