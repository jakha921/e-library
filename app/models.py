import datetime

from django.db import models


# Create your models here.
class Student(models.Model):
    group = {
        "1-kurs": "1-kurs",
        "2-kurs": "2-kurs",
        "3-kurs": "3-kurs",
        "4-kurs": "4-kurs",
        "5-kurs": "5-kurs"
    }

    hemis_id = models.BigIntegerField(verbose_name='HEMIS ID', unique=True, editable=False)
    full_name = models.CharField(max_length=255, verbose_name='Tuliq ismi', editable=False)
    citizenship = models.CharField(max_length=255, verbose_name='Fuqaroligi')
    country = models.CharField(max_length=255, verbose_name='Mamlakati')
    nationality = models.CharField(max_length=255, verbose_name='Millati')
    region = models.CharField(max_length=255, verbose_name='Viloyati')
    district = models.CharField(max_length=255, verbose_name='Tumani')
    gender = models.CharField(max_length=255, verbose_name='Jinsi')
    dob = models.DateField(verbose_name='Tug\'ilgan sanasi')
    passport = models.CharField(max_length=255, verbose_name='Pasport seriyasi')
    jshshir = models.CharField(max_length=255, verbose_name='JSHSHIR', blank=True, null=True)
    passport_given_date = models.DateField(verbose_name='Pasport berilgan sana')
    course = models.CharField(max_length=255, verbose_name='Kursi', choices=group.items())
    faculty = models.CharField(max_length=255, verbose_name='Fakulteti', blank=True, null=True)
    phone = models.CharField(max_length=255, verbose_name='Telefon raqami', blank=True, null=True)
    stgroup = models.CharField(max_length=255, verbose_name='Guruh')
    academic_year = models.CharField(max_length=255, verbose_name='O\'quv yili')
    semester = models.CharField(max_length=255, verbose_name='Semestr')
    is_graduated = models.CharField(verbose_name='Bitirganmi')
    speciality = models.CharField(max_length=255, verbose_name='Yo\'nalishi')
    type_of_education = models.CharField(max_length=255, verbose_name='Ta\'lim turi')
    form_of_education = models.CharField(max_length=255, verbose_name='Ta\'lim shakli')
    payment_form = models.CharField(max_length=255, verbose_name='To\'lov shakli')
    previous_education = models.CharField(max_length=255, verbose_name='Oldingi ta\'lim')
    student_category = models.CharField(max_length=255, verbose_name='Talaba kategoriyasi')
    social_category = models.CharField(max_length=255, verbose_name='Ijtimoiy kategoriyasi')
    command = models.CharField(max_length=255, verbose_name='Buyruq')
    registration_date = models.DateField(verbose_name='Ro\'yxatga olingan sana', blank=True, null=True)
    is_subscribed = models.BooleanField(verbose_name='Obuna', default=False, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name} | {self.passport} | {self.course}'

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
    qr_code = models.CharField(max_length=255, verbose_name='QR-kod', blank=True, null=True)
    link_to_book = models.CharField(max_length=255, verbose_name='Kitob havolasi', blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'
        ordering = ['title']


class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Talaba')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Kitob')
    issued_date = models.DateField(verbose_name='Berilgan sana', auto_now_add=True, editable=False)
    returned_date = models.DateField(verbose_name='Qaytarilgan sana', null=True, blank=True)
    is_returned = models.BooleanField(verbose_name='Qaytarildimi', default=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_returned:
            self.returned_date = datetime.date.today()
        else:
            self.returned_date = None
        super(IssuedBook, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.student} - {self.book}'

    class Meta:
        verbose_name = 'Berilgan kitob'
        verbose_name_plural = 'Berilgan kitoblar'
        ordering = ['student']


class TelegramUser(models.Model):
    telegram_id = models.IntegerField(verbose_name='Telegram ID', unique=True)
    firstname = models.CharField(max_length=255, verbose_name='Ismi', blank=True, null=True)
    lastname = models.CharField(max_length=255, verbose_name='Familiyasi', blank=True, null=True)
    username = models.CharField(max_length=255, verbose_name='Username', blank=True, null=True)
    phone = models.CharField(max_length=255, verbose_name='Telefon raqami', blank=True, null=True)
    lang_code = models.CharField(max_length=255, verbose_name='Til kodi', blank=True, null=True)
    passport = models.CharField(max_length=255, verbose_name='Passport seriyasi', blank=True, null=True)

    def __str__(self):
        return f'{self.telegram_id} - {self.passport}'

    class Meta:
        verbose_name = 'Telegram foydalanuvchisi'
        verbose_name_plural = 'Telegram foydalanuvchilar'
        ordering = ['telegram_id', 'passport']
        # set table name as 'telegram_users'
        db_table = 'telegram_users'


class Employee(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='Tuliq ismi')
    passport = models.CharField(max_length=255, verbose_name='Pasport seriyasi', blank=True, null=True)
    jshshir = models.CharField(max_length=255, verbose_name='jshshir', blank=True, null=True)
    position = models.CharField(max_length=255, verbose_name='Lavozimi', blank=True, null=True)
    department = models.CharField(max_length=255, verbose_name='Bo\'limi', blank=True, null=True)
    phone = models.CharField(max_length=255, verbose_name='Telefon raqami', blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    dob = models.DateField(verbose_name='Tug\'ilgan sanasi', blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} - {self.position}'

    class Meta:
        verbose_name = 'Xodim'
        verbose_name_plural = 'Xodimlar'
        ordering = ['full_name']


class IssuedBookEmployee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Xodim')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Kitob')
    issued_date = models.DateField(verbose_name='Berilgan sana', auto_now_add=True, editable=False)
    returned_date = models.DateField(verbose_name='Qaytarilgan sana', null=True, blank=True)
    is_returned = models.BooleanField(verbose_name='Qaytarildimi', default=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.returned_date:
            self.is_returned = True
            self.returned_date = datetime.date.today()
        else:
            self.is_returned = False
            self.returned_date = None
        super(IssuedBookEmployee, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.employee} - {self.book}'

    class Meta:
        verbose_name = 'Xodimga berilgan kitob'
        verbose_name_plural = 'Xodimga berilgan kitoblar'
        ordering = ['employee']


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.student.full_name} - {self.date}'

    @property
    def time_spent(self):
        if self.time_in and self.time_out:
            delta = self.time_out - self.time_in
            return delta.total_seconds() / 3600  # Время, проведенное в университете, в часах
        return 0

    class Meta:
        verbose_name = 'Davomat'
        verbose_name_plural = 'Davomatlar'
        ordering = ['student', 'date']
