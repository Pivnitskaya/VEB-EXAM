from django.db import models
from django.contrib.auth.models import User

class viexam(models.Model):
    name = models.CharField(max_length=200)                                
    created_at = models.DateTimeField(auto_now_add=True)                   
    exam_date = models.DateField()                                        
    image = models.ImageField(upload_to='exam_images/', null=True, blank=True)  
    participants = models.ManyToManyField(User, related_name='exams')     
    is_public = models.BooleanField(default=False)                        

class ProductCategory(models.Model):
    name = models.CharField("Название категории", max_length=255)
    description = models.TextField("Описание категории", blank=True, null=True)

    class Meta:
        verbose_name = "Категория продукции"
        verbose_name_plural = "Категории продукции"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название товара", max_length=255)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image_url = models.URLField("Ссылка на изображение", blank=True, null=True)
    compatibility = models.CharField("Совместимость", max_length=255)
    system = models.CharField("Система имплантации", max_length=100)
    is_active = models.BooleanField("Показывать на сайте", default=True)
    category = models.ForeignKey(ProductCategory, verbose_name="Категория", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} — {self.category.name}"


class Order(models.Model):
    customer_name = models.CharField("Имя клиента", max_length=255)
    phone = models.CharField("Телефон клиента", max_length=50)
    email = models.EmailField("Email клиента")
    message = models.TextField("Сообщение от клиента", blank=True, null=True)
    created_at = models.DateTimeField("Дата оформления", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Promotion(models.Model):
    title = models.CharField("Название акции", max_length=255)
    description = models.TextField("Описание акции")
    image_url = models.URLField("Ссылка на баннер", blank=True, null=True)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    is_active = models.BooleanField("Статус: Активно", default=True)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class SupportRequest(models.Model):
    SUPPORT_CHOICES = [
        ('question', 'Вопрос'),
        ('problem', 'Проблема'),
        ('other', 'Другое'),
    ]

    name = models.CharField("Имя пользователя", max_length=255)
    phone = models.CharField("Телефон", max_length=50)
    email = models.EmailField("Email")
    support_type = models.CharField("Тема обращения", max_length=20, choices=SUPPORT_CHOICES)
    message = models.TextField("Сообщение")
    attachment_url = models.URLField("Ссылка на файл", blank=True, null=True)
    submitted_at = models.DateTimeField("Дата и время отправки", auto_now_add=True)

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} — {self.get_support_type_display()} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"
