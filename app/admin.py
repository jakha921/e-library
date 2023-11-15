from django.contrib import admin

from app.models import Student, Book, IssuedBook

# Register your models here.
# Register your models here.
admin.site.site_header = 'E-Library boshqaruv tizimi'
admin.site.site_title = 'E-Library boshqaruv tizimi'
admin.site.index_title = 'E-Library boshqaruv tizimi'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('hemis_id', 'full_name', 'JSHSHIR', 'passport')
    list_filter = ('hemis_id', 'full_name', 'JSHSHIR', 'passport')
    search_fields = ('hemis_id', 'fullname', 'JSHSHIR', 'passport')
    list_display_links = ('hemis_id',)
    list_editable = ('JSHSHIR', 'passport')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'quantity')
    list_filter = ('title', 'author', 'price', 'quantity')
    search_fields = ('title', 'author', 'price', 'quantity')
    list_display_links = ('title',)
    list_editable = ('author', 'price', 'quantity',)


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'issued_date')
    list_filter = ('book', 'student')
    search_fields = ('book', 'student', 'issued_date', 'return_date')
    list_display_links = ('book',)
