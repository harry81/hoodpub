from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):

    def show_cover_l_url(self):
        return u"<img src='%s'>" % self.cover_l_url

    show_cover_l_url.allow_tags = True

    def view_link_url(self):
        return u"<a href='%s'>%s</a>" % (self.link, self.barcode)
    view_link_url.allow_tags = True

    list_display = ('isbn', show_cover_l_url, 'title', 'author', 'author_t',
                    view_link_url, 'pub_nm', 'sale_price')
    list_display_links = ('title',)
    search_fields = ['title']

    fieldsets = (
        (None, {
            'fields': (
                'title', 'link', 'pub_nm', 'sale_price')
        }),
        ('Advanced options', {
            'fields': (
                ('author', 'author_t'),
                ('isbn', 'isbn13'),
                ('description'),
            )
        })
    )

    actions = ['update_description']

    def update_description(self, request, queryset):
        for ele in queryset:
            ele.get_description()
    update_description.short_description = "Update the "\
        "descriptioin of each book"

    def get_ordering(self, request):
            return ['pub_nm', '-cover_l_url', '-author']

admin.site.register(Book, BookAdmin)
