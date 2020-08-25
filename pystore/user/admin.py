from django.contrib import admin
from user.models import Product, Transaction, Comment
# Register your models here.
# admin / iamadmin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'inventory', 'seller', 'last_updated')
    list_filter = ('seller',)
    search_fields = ('name',)
    ordering = ('seller', 'last_updated',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('seller', 'buyer', 'product', 'number', 'total', 'pay_time')
    search_fields = ('buyer', 'seller')
    ordering = ('pay_time',)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'product', 'writer', 'post_time')
    search_fields = ('product',)
    ordering = ('post_time',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Comment, CommentAdmin)