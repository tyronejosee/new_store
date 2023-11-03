"""Models for Products App."""

import os
from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    """Catalog type model for Category."""

    title = models.CharField(
        max_length=50, unique=True, verbose_name='Category')
    show_hide = models.BooleanField(default=True, verbose_name='Show/Hide')

    class Meta:
        """Meta definition for Category."""
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return str(self.title)


class Brand(models.Model):
    """Catalog type model for Brand."""

    name = models.CharField(max_length=50, unique=True, verbose_name='Name')
    show_hide = models.BooleanField(default=True, verbose_name='Show/Hide')

    class Meta:
        """Meta definition for Brands."""
        verbose_name_plural = "Brands"
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Deal(models.Model):
    """Entity type model for Deals."""

    name = models.CharField(max_length=50, unique=True, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Discount')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """Entity type model for Products."""

    WARRANTY_CHOICES = [
        (1, '1 month'),
        (3, '3 months'),
        (6, '6 months'),
        (12, '1 year'),
        (24, '2 years'),
        (36, '3 years'),
    ]

    title = models.CharField(max_length=255, verbose_name='Title')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name='Brand')
    normal_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Price')
    deal = models.ForeignKey(
        Deal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Deal')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Category')
    image = models.ImageField(
        upload_to='products/', blank=True, null=True, verbose_name='Image')
    stock = models.PositiveIntegerField(default=100, verbose_name='Stock')
    warranty = models.IntegerField(
        choices=WARRANTY_CHOICES, default='12', blank=True, null=True)
    featured = models.BooleanField(default=False, verbose_name='Featured')
    show_hide = models.BooleanField(default=True, verbose_name='Show/Hide')
    description = RichTextField(
        blank=True, null=True, verbose_name='Description')
    specifications = RichTextField(
        blank=True, null=True, verbose_name='Specifications')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    class Meta:
        """Meta definition for Product."""
        verbose_name_plural = "Products"
        ordering = ['-created_at', 'title']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        """Override the save method to rename the image before saving it."""
        if not self.pk or self._state.adding or self.image != self.__class__.objects.get(pk=self.pk).image:
            # Gets the original file name
            file_name, file_extension = os.path.splitext(self.image.name)
            # Creates the new name in the format 'item-pk.webp'
            new_file_name = f'item-{self.id}{file_extension}'
            # Changes the file name
            self.image.name = new_file_name

        super(Product, self).save(*args, **kwargs)

    def price_with_discount(self):
        """Pending."""
        if self.deal:
            return self.normal_price - (self.normal_price * (self.deal.discount / 100))
        return self.normal_price
