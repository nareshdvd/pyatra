from django.db import models
from django.contrib.auth.models import User

class UsageToken(models.Model):
  user = models.ForeignKey(User)
  token = models.CharField(max_length=50, null=False, blank=False)

  def save(self, *args, **kwargs):
    usage_token = UsageToken.objects.filter(user_id=self.user_id).first()
    if usage_token is None:
      from random import randint
      token = randint(100000, 999999)
      self.token = token
      user = User.objects.get(pk=self.user_id)
      user.set_password(token)
      user.save()
      super(UsageToken, self).save(*args, **kwargs)
    else:
      print "I M SETTING PASSWORD"
      user = User.objects.get(pk=self.user_id)
      user.set_password(self.token)
      user.save()
      super(UsageToken, usage_token).save(*args, force_update=True, **kwargs)

  def __str__(self):
    return "{}  ----  {}".format(self.user.email, self.token)
