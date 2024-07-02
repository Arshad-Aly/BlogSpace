from django.contrib import admin
from .models import Blog, Tag, Message, User

# Register your models here.

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Message)

