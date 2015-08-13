from django.core.validators import validate_email
from django.core.exceptions import ValidationError
class FormValidator(object):
  def __init__(self, form_data, required_validations):
    self._form_data = form_data
    self._required_validations = required_validations
    self._has_errors = False
    self._error_messages = {}
    if 'csrfmiddlewaretoken' in self._form_data:
      del self._form_data['csrfmiddlewaretoken']
    self.validate()

  def validate(self):
    for field, validations in self._required_validations.items():
      value = self._form_data[field]
      if validations.__class__.__name__ != 'list':
        validations = [validations]
      for validation in validations:
        if validation == 'is_not_empty':
          if not self.is_not_empty(value):
            self._has_errors = True
            self._error_messages[field] = 'Field can\'t be empty'
        elif validation == 'is_email':
          if not self.is_email(value):
            self._has_errors = True
            self._error_messages[field] = 'Invalid Email'
        elif validation == 'is_password_confirmed':
          pass1 = value
          pass2 = self._form_data['password_confirmation']
          if not self.is_password_confirmed(pass1, pass2):
            self._has_errors = True
            self._error_messages[field] = 'Password and confirmed Password does not match'
        elif validation == 'is_number':
          if not self.is_number(value):
            self._has_errors = True
            self._error_messages[field] = 'Not a Number'
        elif validation == 'is_array_not_empty':
          if not self.is_array_not_empty(value):
            self._has_errors = True
            self._error_messages[field] = 'Please select'

        elif validation == 'is_image':
          if not self.is_image(value):
            self._has_errors = True
            self._error_messages[field] = 'Not an Image File'
        elif validation == 'is_video':
          if not self.is_video(value):
            self._has_errors = True
            self._error_messages[field] = 'Not a Video File'
        elif validation == 'is_compressed':
          if not self.is_compressed(value):
            self._has_errors = True
            self._error_messages[field] = 'Not a Zipped/Tar Archieve'

  def has_errors(self):
    return self._has_errors

  def get_errors(self):
    return self._error_messages

  def is_email(self, value):
    try:
      validate_email(value)
      return True
    except ValidationError:
      return False

  def is_not_empty(self, value):
    return value != None and value.strip() != ''


  def is_password_confirmed(self, password, confirm_password):
    return password == confirm_password

  def is_image(self, file):
    try:
      return file.content_type.split('/')[1] in ['jpeg', 'jpg', 'JPG', 'JPEG', 'png', 'PNG']
    except:
      return False

  def is_video(self, file):
    try:
      print file.content_type.split('/')[1]
      return file.content_type.split('/')[1] in ['flv', 'mp4']
    except:
      return False

  def is_compressed(self, file):
    try:
      return file.content_type.split('/')[1] in ['zip', 'tar']
    except:
      return False

  def is_number(self, value):
    return value.isdigit()

  def is_array_not_empty(self, value):
    if value.__class__.__name__ == 'list':
      return len(value) != 0
    else:
      return False