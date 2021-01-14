from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/user_{0}/{1}'.format(instance.user.id, filename)


class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length= 10)
    bio = models.TextField(help_text='bio', blank=True)
    profile_photo = models.ImageField(help_text='upload a photo', upload_to=user_directory_path, blank=True)
    date_of_birth = models.DateField(max_length=10, blank=True)

    GENDER_CHOICES = (
        (None,'Select gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,blank=True)

    def get_absolute_url(self):
        return reverse('ide:index')

    def __str__(self):
        return self.user.username




class savecode(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)    
    code=models.TextField(help_text="Please copy Code paste here!", max_length=10000)
    language_CHOICES = (
        ('C', 'C'),
        ('C++', 'C++'),
        ('CLOJURE','CLOJURE'),
	('CSS','CSS'),
	('C#','C#'),
	('GO','GO'),
	('Haskell','Haskell'),
	('JAVA','JAVA'),
	('JAVASCRIPT','JAVASCRIPT'),
	('Lisp','Lisp'),
	('Objective-C','Objective-C'),
	('Pascal','Pascal'),
	('PERL','PERL'),
	('PHP','PHP'),
	('Python','Python'),
	('RUBY','RUBY'),
	('R','R'),
	('RUST','RUST'),
	('SCALA','SCALA'),
	('TEXTFILE','TEXTFILE'),

    )
    language=models.CharField(max_length=100, choices=language_CHOICES,default='C')

    def get_absolute_url(self):
        return reverse('ide:index')

    def __str__(self):
        return self.code
