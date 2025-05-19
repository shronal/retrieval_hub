from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Contact(models.Model):
    fname = models.CharField(max_length=100, null= True)
    lname = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    desc = models.TextField()  
    def __str__(self):
     return f"Message by {self.fname}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.png')

# Signal to create a UserProfile automatically
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal to save the UserProfile when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()



class LostItem(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50)
    color = models.CharField(max_length=50, blank=True)
    brand = models.CharField(max_length=50, blank=True)
    date_lost = models.DateField()
    location_lost = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    photo = models.ImageField(upload_to='lost_items/', blank=True)

    def __str__(self):
        return f"{self.item_name} reported by {self.name}"
    


class FoundItem(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50)
    color = models.CharField(max_length=50, blank=True)
    brand = models.CharField(max_length=50, blank=True)
    date_found = models.DateField()
    location_found = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    photo = models.ImageField(upload_to='found_items/', blank=True)

    def __str__(self):
        return f"{self.item_name} reported by {self.name}"



class Claim(models.Model):
    item = models.ForeignKey('LostItem', null=True, blank=True, on_delete=models.SET_NULL)
    found_item = models.ForeignKey('FoundItem', null=True, blank=True, on_delete=models.SET_NULL)
    claimant_name = models.CharField(max_length=100)
    claimant_email = models.EmailField()
    claimant_phone = models.CharField(max_length=15)
    claim_date = models.DateTimeField(auto_now_add=True)
    claim_message = models.TextField()

    def __str__(self):
        return f"Claim by {self.claimant_name} for {self.item or self.found_item}"
    


from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('Login Page')  # Redirect to the profile page after success

