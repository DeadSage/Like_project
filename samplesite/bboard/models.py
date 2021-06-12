from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from precise_bbcode.fields import BBCodeTextField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name="Товар")
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


class Img(models.Model):
    img = ProcessedImageField(upload_to='post_images', processors=[ResizeToFill(400, 200)],
                              format='JPEG',
                              options={'quality': 60})
    image_thumbnail = ImageSpecField(source='img', processors=[ResizeToFill(100, 50)],
                                     format='JPEG',
                                     options={'quality': 60})
    desc = models.TextField(verbose_name='Описание')

    def delete(self, *args, **kwargs):
        self.img.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
# class Note(models.Model):
#     content = models.TextField()
#     content_types = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
