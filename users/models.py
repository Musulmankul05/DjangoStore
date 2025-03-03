from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.db import models
from PIL import Image
import os

from MusulmankulNew import settings


def user_directory_path(instance, filename):
    return f'users/{instance.username}/profile.jpg'


class UserModel(AbstractUser):
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    date_birth = models.DateField(blank=True, null=True)
    last_edited = models.DateTimeField()
    phone = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"Пользователь {self.username}"

    def save(self, *args, **kwargs):
        self.last_edited = timezone.now()

        # Check if an image exists and needs updating
        try:
            this = UserModel.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except Exception as e:
            print(e)
        super().save(*args, **kwargs)

        print(self.image)
        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')  # Convert to RGB to ensure it's a JPEG-compatible format

            # Define the path to save the processed image
            image_path = os.path.join('media', user_directory_path(self, 'profile.jpg'))

            # Save the image in JPEG format
            img.save(image_path, 'JPEG')

            # Update the image field with the new path
            self.image.name = user_directory_path(self, 'profile.jpg')
            print(str(img) + '\n' + image_path + '\n' + self.image.name)

            # Save the instance again to update the image path in the database
            super().save(*args, **kwargs)


class EmailVerificationModel(models.Model):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()

    def is_expired(self):
        if self.expires < timezone.now():
            return True
        else:
            return False

    def send_verification_email(self):
        verification_link = 'http://localhost:8000' + reverse('users:confirm_email', kwargs={'token': self.code})
        subject = 'Подтверждение электронной почты'
        message = f'Пожалуйста, подтвердите свою электронную почту, перейдя по следующей ссылке: {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def __str__(self):
        return f"Письмо верификации эл. почты пользователя {self.user.email}"

    class Meta:
        verbose_name_plural = 'верификации'
        verbose_name = 'модель верификации'
