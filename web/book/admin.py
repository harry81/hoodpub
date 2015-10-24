from django.contrib import admin
from .models import Books


class BooksAdmin(admin.ModelAdmin):

    def show_cover_s_url(self):
        return u"<img src='%s'>" % self.cover_s_url

    show_cover_s_url.allow_tags = True

    def view_link_url(self):
        return u"<a href='%s'>%s</a>" % (self.link, self.barcode)
    view_link_url.allow_tags = True

    list_display = ('isbn', show_cover_s_url, 'title', 'author', 'author_t',
                    view_link_url, 'pub_nm', 'sale_price')
    list_display_links = ('title',)

    fieldsets = (
        (None, {
            'fields': ('title', 'link', 'pub_nm', 'sale_price')
            }), ('Advanced options', {
                'fields': (
                    ('author', 'author_t'),
                    ('isbn', 'isbn13'),
                    ('description'),
                    )
                }),
        )


admin.site.register(Books, BooksAdmin)
