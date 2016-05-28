from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import TeacherExercise, StudentExercise, FichJs, Error, Library, Usuario

admin.site.register(TeacherExercise)
admin.site.register(StudentExercise)
admin.site.register(FichJs)
admin.site.register(Error)
admin.site.register(Library)
admin.site.register(Usuario)