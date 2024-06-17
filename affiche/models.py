from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from multiupload.fields import MultiFileField


class MainImages(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    main_image = models.ImageField(upload_to='mainimg/')

    def __str__(self):
        return f"Image {self.id}"

    class Meta:
        verbose_name_plural = 'Изображения для карусели'


class PerformanceManager(models.Manager):
    def upcoming(self):
        now = timezone.now()
        end_date = now + timedelta(days=31)
        return self.filter(
            models.Q(datetime1__gte=now, datetime1__lte=end_date) |
            models.Q(datetime2__gte=now, datetime2__lte=end_date),
            hidden=False
        ).order_by('datetime1')


class Performance(models.Model):
    title = models.CharField(max_length=255, null=False)
    datetime1 = models.DateTimeField(null=True, blank=True)
    datetime2 = models.DateTimeField(null=True, blank=True)
    subtitle = models.TextField(max_length=1000, blank=True, null=True)
    duration = models.CharField(max_length=255, null=False)
    dop_info = models.TextField(max_length=1000, null=True)
    background1 = models.TextField(max_length=100000, null=True, blank=True)
    background2 = models.TextField(max_length=100000, null=True, blank=True)
    background3 = models.TextField(max_length=100000, null=True, blank=True)
    image = models.ImageField(upload_to='perfimg/', null=False)
    history = models.TextField(max_length=100000, null=True, blank=True)
    premier = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    repertory_name = models.CharField(max_length=255, null=False, default='LL')
    repertory_description = models.TextField(max_length=1000, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    image_carousel = models.ManyToManyField('PerformanceFiles', blank=True)
    hidden = models.BooleanField(default=False)

    TYPE_CHOICES = (
        ('Балет', 'Балет'),
        ('Опера', 'Опера')
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Балет')

    objects = PerformanceManager()

    def __str__(self):
        return self.title

    def is_upcoming(self):
        now = timezone.now()
        return not self.hidden and (self.datetime1 >= now or (self.datetime2 and self.datetime2 >= now))

    @receiver(pre_save, sender='affiche.Performance')
    def update_performance(sender, instance, **kwargs):
        now = timezone.now()
        if instance.datetime1 and instance.datetime1 < now and (not instance.datetime2 or instance.datetime2 < now):
            instance.hidden = True
            instance.datetime1 = None
            instance.datetime2 = None

    class Meta:
        verbose_name_plural = 'Представления'


class PerformanceFiles(models.Model):
    for_performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    file = models.FileField(upload_to='percarousel/')

    def __str__(self):
        return f"{self.id} {self.for_performance}"

    class Meta:
        verbose_name_plural = 'Галерея представлений'


class Creatives(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Постановщики'


class Performers(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Исполнители'


class PerformancePerformers(models.Model):
    performer = models.ManyToManyField(Performers)
    role = models.CharField(max_length=255, null=True, blank=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)

    @property
    def short_roles(self):
        performers_count = self.performer.count()
        return performers_count == 1

    @property
    def long_roles(self):
        performers_count = self.performer.count()
        return performers_count > 1

    def __str__(self):
        return f"{self.id}. {self.performer.name} - {self.role}, {self.performance}"

    class Meta:
        verbose_name_plural = 'Исполнители представления'


class PerformanceCreatives(models.Model):
    name = models.ForeignKey(Creatives, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, null=False)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id}. {self.name} - {self.role}, {self.performance}"

    class Meta:
        verbose_name_plural = 'Постановщики представления'


@receiver(post_save, sender=Performance)
def update_performance_creatives(sender, instance, created, **kwargs):
    if not created:  # Если объект Performance был изменён, а не создан
        performance_creatives = PerformanceCreatives.objects.filter(performance=instance)
        for pc in performance_creatives:
            creatives_instance = pc.name  # Получаем связанный объект Creatives
            if not pc.description:  # Если у PerformanceCreatives нет описания
                pc.description = creatives_instance.description  # Обновляем описание из Creatives
                pc.save()  # Сохраняем изменения
    else:  # Если объект Performance был создан
        creatives_instances = Creatives.objects.all()
        for creatives_instance in creatives_instances:
            PerformanceCreatives.objects.create(
                name=creatives_instance,
                role='',  # Можно указать значение по умолчанию для роли
                performance=instance,
                description=creatives_instance.description  # Устанавливаем описание из Creatives
            )


class Conductor(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Дирижеры'


class PerformanceConductor(models.Model):
    name = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id}. {self.name} - {self.performance}"

    class Meta:
        verbose_name_plural = 'Дирижер представления'


@receiver(post_save, sender=Conductor)
def update_performance_conductors(sender, instance, created, **kwargs):
    if not created:
        performance_conductor = PerformanceConductor.objects.filter(name=instance)
        for pc in performance_conductor:
            if not pc.description:
                pc.description = instance.description
                pc.save()
    else:
        performances = Performance.objects.all()
        for performance in performances:
            PerformanceConductor.objects.create(
                name=instance,
                performance=performance,
                description=instance.description
            )


class Backstage(models.Model):
    title = models.CharField(max_length=255, null=False)
    main_image = models.ImageField(upload_to='backstage/', null=False)
    description = models.TextField(max_length=255, null=False)
    date = models.DateField(auto_now=False, auto_now_add=False)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)

    TYPE_CHOICES = (
        ('Статья', 'Статья'),
        ('Запись', 'Запись'),
        ('Подкаст', 'Подкаст')
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Статья')

    BLOCK_TYPE_CHOICES = (
        ("text", "Text"),
        ("image", "Image"),
        ("media", "Media")
    )

    block1_type = models.CharField(max_length=10, choices=BLOCK_TYPE_CHOICES, default='text')
    block2_type = models.CharField(max_length=10, choices=BLOCK_TYPE_CHOICES, default='text')
    block3_type = models.CharField(max_length=10, choices=BLOCK_TYPE_CHOICES, default='text')
    block4_type = models.CharField(max_length=10, choices=BLOCK_TYPE_CHOICES, default='text')
    block5_type = models.CharField(max_length=10, choices=BLOCK_TYPE_CHOICES, default='text')

    block1_content = models.TextField(max_length=10000, null=True, blank=True)
    block2_content = models.TextField(max_length=10000, null=True, blank=True)
    block3_content = models.TextField(max_length=10000, null=True, blank=True)
    block4_content = models.TextField(max_length=10000, null=True, blank=True)
    block5_content = models.TextField(max_length=10000, null=True, blank=True)

    block1_picture = models.ImageField(upload_to='backstage/', null=True, blank=True)
    block2_picture = models.ImageField(upload_to='backstage/', null=True, blank=True)
    block3_picture = models.ImageField(upload_to='backstage/', null=True, blank=True)
    block4_picture = models.ImageField(upload_to='backstage/', null=True, blank=True)
    block5_picture = models.ImageField(upload_to='backstage/', null=True, blank=True)

    block1_media = models.FileField(upload_to='backstage/', null=True, blank=True)
    block2_media = models.FileField(upload_to='backstage/', null=True, blank=True)
    block3_media = models.FileField(upload_to='backstage/', null=True, blank=True)
    block4_media = models.FileField(upload_to='backstage/', null=True, blank=True)
    block5_media = models.FileField(upload_to='backstage/', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

    class Meta:
        verbose_name_plural = 'Backstage'


class Row(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"Row {self.number}"


class Seat(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    number = models.IntegerField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Row {self.row.number} - Seat {self.number}"

    def clean(self):
        if Seat.objects.filter(row=self.row, number=self.number).exists():
            raise ValidationError('Место с таким номером уже существует в этом ряду.')


class Ticket(models.Model):
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100)
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket for {self.seat}"
