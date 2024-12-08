from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Category, Customer, Product, Order, Profile


# Register other models
models = [Category, Customer, Product, Order, Profile]
for model in models:
    admin.site.register(model)

# Unregister Group (optional)
admin.site.unregister(Group)


# Inline Profile Admin
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False  # Prevent deleting profiles directly
    verbose_name_plural = 'Profiles'


# Custom User Admin
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInLine]


# Unregister and re-register the User model once
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
