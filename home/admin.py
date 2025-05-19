from django.contrib import admin
from home.models import Contact,LostItem,FoundItem,Claim


# Register your models here.
admin.site.register(Contact)
admin.site.register(LostItem)
admin.site.register(FoundItem)
admin.site.register(Claim)
