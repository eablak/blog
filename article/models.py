from django.db.models.fields.files import FileField
import article
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Yazar")
    title = models.CharField(max_length=50,verbose_name = "Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")
    article_image = models.FileField(blank=True,null=True,verbose_name="Makaleye Fotoğraf Ekleyin")
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']


class Yorum(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="Makale",related_name="yorumlar")
    yorum_author = models.CharField(max_length=50,verbose_name="İsim")
    yorum_content = models.CharField(max_length=200,verbose_name="Yorum")
    yorum_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.yorum_content
    
    class Meta:
        ordering = ['-yorum_date']



