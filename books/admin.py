from django.contrib import admin
from .models import Book, Offer, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'owner')
    search_fields = ('title', 'author')
    list_filter = ('owner',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('from_user__username', 'to_user__username')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)