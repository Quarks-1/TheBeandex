from django.test import TestCase
from .models import Burr, Grinder, BrewMethod, BrewProfile, Profile
from django.contrib.auth.models import User
from django.utils import timezone

class BurrModelTest(TestCase):
    def setUp(self):
        self.burr = Burr.objects.create(manufacturer='Test Manufacturer', model='Test Model', burr_size=50)

    def test_burr_creation(self):
        self.assertTrue(isinstance(self.burr, Burr))

class GrinderModelTest(TestCase):
    def setUp(self):
        self.burr = Burr.objects.create(manufacturer='Test Manufacturer', model='Test Model', burr_size=50)
        self.grinder = Grinder.objects.create(manufacturer='Test Manufacturer', model='Test Model', burr=self.burr)

    def test_grinder_creation(self):
        self.assertTrue(isinstance(self.grinder, Grinder))

class BrewMethodModelTest(TestCase):
    def setUp(self):
        self.brew_method = BrewMethod.objects.create()

    def test_brew_method_creation(self):
        self.assertTrue(isinstance(self.brew_method, BrewMethod))

class BrewProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.burr = Burr.objects.create(manufacturer='Test Manufacturer', model='Test Model', burr_size=50)
        self.grinder = Grinder.objects.create(manufacturer='Test Manufacturer', model='Test Model', burr=self.burr)
        self.brew_method = BrewMethod.objects.create()
        self.brew_profile = BrewProfile.objects.create(creator=self.user, grinder=self.grinder, burr=self.burr, brew_method=self.brew_method)

    def test_brew_profile_creation(self):
        self.assertTrue(isinstance(self.brew_profile, BrewProfile))

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile, Profile))