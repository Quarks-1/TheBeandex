from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField



class Burr(models.Model):
    class BurrType(models.TextChoices):
        CONICAL = 'CON', 'Conical'
        FLAT = 'FLT', 'Flat'
        OTHER = 'OTH', 'Other'
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    burr_size = models.PositiveBigIntegerField(default=0)
    burr_type = models.CharField(max_length=3, choices=BurrType.choices, default=BurrType.OTHER)

class Grinder(models.Model):
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    calibration = models.CharField(max_length=50)
    burr = models.ForeignKey(Burr, on_delete=models.PROTECT)
    misc_info = models.CharField(max_length=200)

class BrewMethod(models.Model):
    class BrewType(models.TextChoices):
        POUR_OVER = 'PO', 'Pour Over'
        IMMERSION = 'IM', 'Immersion'
        ESPRESSO = 'ES', 'Espresso',        
        OTHER = 'OT', 'Other'
    brew_type = models.CharField(max_length=2, choices=BrewType.choices, default=BrewType.OTHER)
    
    
class BrewProfile(models.Model):
                        #### Basic Info ###
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    
                        #### Brew Parameters ###
    # Grind Parameters
    grinder = models.ForeignKey(Grinder, on_delete=models.PROTECT)
    burr = models.ForeignKey(Burr, on_delete=models.PROTECT)
    burr_seaoned = models.BooleanField(default=False)
    steps = ArrayField(models.CharField(max_length=200)) # Array of steps
    grinder_rpm = models.PositiveBigIntegerField(default=0)
    grind_size = models.PositiveBigIntegerField(default=0)
    grind_weight = models.PositiveBigIntegerField(default=0)
    # Water Parameters
    water_weight = models.PositiveBigIntegerField(default=0)
    water_temp = models.PositiveBigIntegerField(default=0)
    # Method
    brew_method = models.ForeignKey(BrewMethod, on_delete=models.PROTECT)
    brew_machine = models.CharField(max_length=100, default='None')
    
                        #### Rating Parameters ###
    personal_rating = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    
    # Public vote count
    votes = models.BigIntegerField(default=0)
    
class Profile(models.Model):
    # Basic Info
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    join_date = models.DateTimeField(default=timezone.now)
    picture = models.FileField(blank=True)
    # User Profiles
    grind_profiles = models.ManyToManyField(BrewProfile, related_name='grind_profiles')
    # Profile Stats
    total_beans = models.BigIntegerField(default=0)
    
    
@receiver(user_logged_in)
def create_profile(sender, user, request, **kwargs):
    # Check if user is not admin
    if user.is_superuser:
        return
    if not Profile.objects.filter(user=user).exists():
        pic = request.user.social_auth.get(provider='google-oauth2').extra_data['picture']
        Profile.objects.get_or_create(user=user, join_date=timezone.now(), picture=pic)
    if 'picture' not in request.session:
        request.session['picture'] = request.user.social_auth.get(provider='google-oauth2').extra_data['picture']

