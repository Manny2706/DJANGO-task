from django.db import models
from django.contrib.auth.models import User
import os

# Use CloudinaryField only when Cloudinary credentials are configured.
# Otherwise fall back to a local FileField for development.
if os.getenv('CLOUDINARY_CLOUD_NAME') and os.getenv('CLOUDINARY_API_KEY') and os.getenv('CLOUDINARY_API_SECRET'):
	from cloudinary.models import CloudinaryField as _CloudImageField
	CloudImageField = _CloudImageField
else:
	# FileField doesn't require Pillow and stores files under MEDIA_ROOT
	CloudImageField = models.FileField


class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	image = CloudImageField('image', blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	@property
	def excerpt(self) -> str:
		if len(self.content) <= 160:
			return self.content
		return f"{self.content[:157]}..."