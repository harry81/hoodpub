# -*- coding: utf-8 -*-
import requests
from lxml import html
from requests import exceptions
from datetime import datetime
from django.db import models

PUBLISHER_CHOICE = (
    ('KY', u'교보'),
    ('YE', u'YES24'),
    ('IN', u'인터파크'),
    ('BA', u'반디엔루니스'),
)


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
    pub_nm = models.CharField(max_length=128, db_index=True)
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

    def get_description(self):
        if self.introduction_set.count() == 0:
            self._get_description_from_url()

        if self.introduction_set.count() == 0:
            return None

        intro = self.introduction_set.extra(
            select={'length': 'Length(content)'}).order_by('-length')

        if intro:
            self.description = intro[0].content
            self.save()

    def _get_description_from_url(self):
        for pub in PUBLISHER_CHOICE:

            page = requests.get(self.link, params={'introCpID': pub})
            if page.status_code == 200:
                tree = html.fromstring(page.content)

                for ele in tree.xpath(
                        '//meta[@property="og:description"]/@content'):
                    cnt = 1
                    content = ele.strip()
                    if len(content) < 30:
                        continue

                    intro_dict = {
                        'content': content
                    }
                    new_intro, created = Introduction.objects.get_or_create(
                        book=self, publisher=pub[0],
                        cnt=cnt, defaults=intro_dict)

                    cnt += 1


class Introduction(models.Model):

    book = models.ForeignKey(Book)
    content = models.TextField()
    publisher = models.CharField(max_length=3, choices=PUBLISHER_CHOICE)
    cnt = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        unique_together = ("book", "publisher", "cnt")
        ordering = ('-book',)

    def __unicode__(self):
        return u'%s %s ' % (
            self.book.title, self.publisher,)
