from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('role', 'first_name', 'phone_number', 'address')
    search_fields = ('first_name', )
