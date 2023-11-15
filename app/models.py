from django.db import models


# Create your models here.
class Student(models.Model):
    hemis_id = models.IntegerField(verbose_name='HEMIS ID', unique=True, editable=False)
    full_name = models.CharField(max_length=255, verbose_name='Tuliq ismi', editable=False)
    citizenship = models.CharField(max_length=255, verbose_name='Fuqaroligi')
    country = models.CharField(max_length=255, verbose_name='Mamlakati')
    nationality = models.CharField(max_length=255, verbose_name='Millati')
    region = models.CharField(max_length=255, verbose_name='Viloyati')
    district = models.CharField(max_length=255, verbose_name='Tumani')
    gender = models.CharField(max_length=255, verbose_name='Jinsi')
    dob = models.DateField(verbose_name='Tug\'ilgan sanasi')
    passport = models.CharField(max_length=255, verbose_name='Pasport seriyasi')
    JSHSHIR = models.CharField(max_length=255, verbose_name='JSHSHIR')
    passport_given_date = models.DateField(verbose_name='Pasport berilgan sana')
    course = models.IntegerField(verbose_name='Kursi')
    group = models.CharField(max_length=255, verbose_name='Guruh')
    academic_year = models.CharField(max_length=255, verbose_name='O\'quv yili')
    semester = models.CharField(max_length=255, verbose_name='Semestr')
    is_graduated = models.BooleanField(verbose_name='Bitirganmi')
    speciality = models.CharField(max_length=255, verbose_name='Yo\'nalishi')
    type_of_education = models.CharField(max_length=255, verbose_name='Ta\'lim turi')
    form_of_education = models.CharField(max_length=255, verbose_name='Ta\'lim shakli')
    payment_form = models.CharField(max_length=255, verbose_name='To\'lov shakli')
    previous_education = models.CharField(max_length=255, verbose_name='Oldingi ta\'lim')
    student_category = models.CharField(max_length=255, verbose_name='Talaba kategoriyasi')
    social_category = models.CharField(max_length=255, verbose_name='Ijtimoiy kategoriyasi')
    comment = models.CharField(max_length=255, verbose_name='Buyruq')
    registration_date = models.DateField(verbose_name='Ro\'yxatga olingan sana')

    def __str__(self):
        return self.hemis_id, self.full_name

    class Meta:
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'
        ordering = ['full_name']


class Book(models.Model):
    author = models.CharField(max_length=255, verbose_name='Muallif')
    title = models.CharField(max_length=255, verbose_name='Kitob nomi')
    publisher = models.CharField(max_length=255, verbose_name='Nashriyot')
    year = models.IntegerField(verbose_name='Nashr yili')
    pages = models.IntegerField(verbose_name='Sahifalar soni')
    price = models.IntegerField(verbose_name='Narxi')
    quantity = models.IntegerField(verbose_name='Soni')

    def __str__(self):
        return self.title, self.author

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'
        ordering = ['title']


class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Talaba')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Kitob')
    issued_date = models.DateField(verbose_name='Berilgan sana', auto_now_add=True, editable=False)
    returned_date = models.DateField(verbose_name='Qaytarilgan sana', null=True, blank=True)

    def __str__(self):
        return self.student, self.book

    class Meta:
        verbose_name = 'Berilgan kitob'
        verbose_name_plural = 'Berilgan kitoblar'
        ordering = ['student']