from datetime import timedelta

from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.timezone import now

from app.models import Student, Book, IssuedBook, Attendance, Employee, IssuedBookEmployee

# Register your models here.
admin.site.site_header = 'E-Library boshqaruv tizimi'
admin.site.site_title = 'E-Library boshqaruv tizimi'
admin.site.index_title = 'E-Library boshqaruv tizimi'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('hemis_id', 'full_name', 'jshshir', 'passport', 'is_subscribed')
    list_filter = ('course', 'region', 'speciality', 'is_subscribed')
    search_fields = ('hemis_id', 'full_name', 'jshshir', 'passport')
    list_display_links = ('hemis_id',)
    list_editable = ('is_subscribed',)

    # give permission for all users to edit the is_subscribed field
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:  # Non-admin users can only edit 'is_subscribed'
            return [field.name for field in self.model._meta.fields if field.name != 'is_subscribed']
        return super().get_readonly_fields(request, obj)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'quantity')
    list_filter = ('author',)
    search_fields = ('title', 'author', 'price', 'quantity')
    list_display_links = ('title',)
    list_editable = ('author', 'price', 'quantity',)


class ReturnedDateFilter(admin.SimpleListFilter):
    title = 'Kitob qaytarilganligi'
    parameter_name = 'returned_date'

    def lookups(self, request, model_admin):
        return (
            ('returned', 'Qaytarilgan'),
            ('not_returned', 'Qaytarilmagan'),
            ('all', 'Barchasi')
        )

    def queryset(self, request, queryset):
        if self.value() == 'returned':
            return queryset.exclude(returned_date__isnull=True)
        if self.value() == 'not_returned':
            return queryset.filter(returned_date__isnull=True)
        return queryset

    # Set 'not_returned' as the default value
    def value(self):
        value = super().value()
        if value is None:
            return 'not_returned'
        return value


class OverdueFilter(admin.SimpleListFilter):
    title = 'Kitob muddati o\'tganligi'
    parameter_name = 'overdue'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Muddati o\'tgan'),
            ('no', 'Muddati o\'tmagan')
        ]

    def queryset(self, request, queryset):
        today = now().date()
        if self.value() == 'yes':
            # Filter books that are overdue and not returned
            return queryset.filter(issued_date__lt=today - timedelta(days=10), is_returned=False)
        if self.value() == 'no':
            # Filter books that are not overdue or already returned
            return queryset.exclude(issued_date__lt=today - timedelta(days=10), is_returned=False)
        return queryset


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    fields = ('book', 'student', 'is_returned')
    list_display = ('book', 'student', 'issued_date', 'issued_due_date_colored', 'returned_date')
    list_filter = (OverdueFilter, ReturnedDateFilter, 'issued_date', 'book')
    search_fields = (
        'book__author', 'book__title', 'book__publisher', 'book__year', 'book__pages', 'book__price', 'book__quantity',
        'student__hemis_id', 'student__full_name', 'student__jshshir', 'student__passport', 'student__course',
        'student__faculty', 'student__stgroup', 'student__academic_year', 'student__semester',
        'student__speciality', 'student__type_of_education', 'student__form_of_education', 'student__payment_form',
        'student__previous_education', 'student__student_category', 'student__social_category', 'student__command',
        'student__registration_date', 'issued_date', 'returned_date')
    list_display_links = ('book',)
    autocomplete_fields = ('book', 'student')

    def issued_due_date_colored(self, obj):
        # Calculate the issued date + 10 days
        due_date = obj.issued_date + timedelta(days=10)

        # If the book is not returned and the current date is past the due date
        if not obj.is_returned and now().date() > due_date:
            color = 'red'
        else:
            color = 'green'  # Default color if the book is returned or within the 10-day period

        # Return HTML with the due date colored accordingly and set due_date format as 24-Sentabr, 2024-yil
        return format_html('<span style="color: {};">{}</span>', color, due_date.strftime('%d-%B, %Y'))

    # Set a readable name for the column
    issued_due_date_colored.short_description = 'Qaytarish muddati'

    def save_model(self, request, obj, form, change):
        if obj._state.adding and obj.returned_date is None:  # Checking if it's a new object being added
            book = obj.book
            if book.quantity > 0:
                book.quantity -= 1
                book.save()
                self.message_user(request, f"{book.title} nomli kitob {obj.student} ga muvaffaqiyatli berildi.",
                                  level=messages.SUCCESS)
            else:
                self.message_user(request, f"{book.title} nomli kitob omborda yo'q.", level=messages.ERROR)

        if not obj._state.adding and 'returned_date' in form.changed_data and obj.returned_date is not None:
            book = obj.book
            book.quantity += 1
            book.save()
            self.message_user(request, f"{book.title} nomli kitob {obj.student} dan muvaffaqiyatli qaytarildi.",
                              level=messages.SUCCESS)

        super().save_model(request, obj, form, change)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    fields = ('student', 'date')
    list_display = ('student', 'date')
    list_filter = ('date',)
    search_fields = ('student__full_name',)
    ordering = ('student', 'date')
    autocomplete_fields = ('student',)
    readonly_fields = ('time_spent',)
    date_hierarchy = 'date'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'phone')
    search_fields = ('full_name', 'position', 'phone')
    list_display_links = ('full_name',)


@admin.register(IssuedBookEmployee)
class IssuedBookEmployeeAdmin(admin.ModelAdmin):
    fields = ('book', 'employee', 'is_returned')
    list_display = ('book', 'employee', 'issued_date', 'issued_due_date_colored', 'returned_date')
    list_filter = (OverdueFilter, ReturnedDateFilter, 'issued_date', 'book')
    search_fields = (
        'book__author', 'book__title', 'book__publisher', 'book__year', 'book__pages', 'book__price', 'book__quantity',
        'employee__full_name', 'employee__position', 'employee__phone', 'issued_date', 'returned_date')
    list_display_links = ('book',)
    autocomplete_fields = ('book', 'employee')

    def issued_due_date_colored(self, obj):
        # Calculate the issued date + 10 days
        due_date = obj.issued_date + timedelta(days=10)

        # If the book is not returned and the current date is past the due date
        if not obj.is_returned and now().date() > due_date:
            color = 'red'
        else:
            color = 'green'  # Default color if the book is returned or within the 10-day period

        # Return HTML with the due date colored accordingly and set due_date format as 24-Sentabr, 2024-yil
        return format_html('<span style="color: {};">{}</span>', color, due_date.strftime('%d-%B, %Y'))

    # Set a readable name for the column
    issued_due_date_colored.short_description = 'Qaytarish muddati'


    def save_model(self, request, obj, form, change):
        if obj._state.adding and obj.returned_date is None:
            book = obj.book
            if book.quantity > 0:
                book.quantity -= 1
                book.save()
                self.message_user(request, f"{book.title} nomli kitob {obj.employee} ga muvaffaqiyatli berildi.",
                                  level=messages.SUCCESS)
            else:
                self.message_user(request, f"{book.title} nomli kitob omborda yo'q.", level=messages.ERROR)

        if not obj._state.adding and 'returned_date' in form.changed_data and obj.returned_date is not None:
            book = obj.book
            book.quantity += 1
            book.save()
            self.message_user(request, f"{book.title} nomli kitob {obj.employee} dan muvaffaqiyatli qaytarildi.",
                              level=messages.SUCCESS)

        super().save_model(request, obj, form, change)
