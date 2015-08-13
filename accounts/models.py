from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import random


class UsageToken(models.Model):
  token = models.CharField(max_length=10)
  email = models.CharField(max_length=255)
  used = models.NullBooleanField(blank=True, null=True, default=False)
  user = models.OneToOneField(User, blank=True, null=True, default=None, related_name='usage_token')

  @classmethod
  def generate(cls, email):
    obj = cls.objects.filter(email=email, used=False).first()
    if not obj:
      token = random.randint(100000, 999999)
      obj = cls(**{
        'email' : email,
        'token' : token,
        'used' : False
      })
      obj.save()
    return obj

  def use(self, user):
    self.user = user
    self.used = True
    self.save()

  @classmethod
  def validate(cls, email, token):
    obj = cls.objects.filter(email=email, token=token, used=False).first()
    if obj:
      return True
    else:
      return False

  @classmethod
  def unused(cls):
    objs = cls.objects.filter(used=False)
    return objs