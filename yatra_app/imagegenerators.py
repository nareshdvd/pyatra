from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, ResizeToFit

class Thumbnail_372_248(ImageSpec):
  processors = [ResizeToFill(372, 248)]
  format = 'JPEG'
  options = {'quality': 80}
register.generator('yatra_app:thumb_372_248', Thumbnail_372_248)

class ThumbnailHeight_70(ImageSpec):
  processors = [ResizeToFit(height=70)]
  format = 'png'
  options = {'quality': 80}
register.generator('yatra_app:thumb_height_70', ThumbnailHeight_70)