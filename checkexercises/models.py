from __future__ import unicode_literals

from django.db import models
class Usuario(models.Model):
	user = models.CharField(max_length=500)
	rankingerrors = models.TextField() #para hacer el ranking de los 5 errores mas comunes
	data = models.CharField(max_length=10000) #para hacer la grafica de evolucion

# Create your models here.
class TeacherExercise(models.Model):
    urlTeacherEx = models.CharField(max_length=500)
    sumary =  models.TextField()
    rankingpercent = models.TextField()
    rankingfich = models.TextField()
    rankingerrors = models.TextField()
    data = models.CharField(max_length=10000)
    branch = models.CharField(max_length=500)
    user = models.CharField(max_length=500)
    numoferrors = models.CharField(max_length=10000)
    numorden = models.IntegerField(default=0)
    islast = models.BooleanField(default=False)
    datacomparar = models.CharField(max_length=10000)
    #anadir ranking fich y ranking errores

#class Student(models.Model):
#	name = models.CharField(max_length=500)
#	errors = models.CharField(max_length=500)

class StudentExercise(models.Model):
	#ficherosJs = []
	urlTeacherEx = models.CharField(max_length=500)
	urlStudentEx = models.CharField(max_length=500)
	nameStudent = models.CharField(max_length=500)
	urlAvatar = models.CharField(max_length=500)
	analizado = models.BooleanField(default=False)
	sumary = models.TextField()
	numportfolio = models.CharField(max_length=500)
	nofichfind = models.BooleanField(default=False)
	numfichanaliz = models.CharField(max_length=500)
	porcenterrorsfich = models.CharField(max_length=500)
	hayfirstfich = models.BooleanField(default=False)
	firstfich = models.CharField(max_length=500)
	branch = models.CharField(max_length=500)
	user = models.CharField(max_length=500)
	rankingerrors = models.TextField() #solo para el caso de que el usuario sea alumno
	data = models.CharField(max_length=10000) #solo para el caso de que el usuario sea alumno
	datafich =  models.CharField(max_length=10000) #solo para el caso de que el usuario sea alumno
	divdata = models.CharField(max_length=500) #solo para el caso de que el usuario sea alumno
	numoferrors = models.CharField(max_length=10000)
	numorden = models.IntegerField(default=0)
	islast = models.BooleanField(default=False)#solo para el caso de que el usuario sea alumno
	datacomparar = models.CharField(max_length=10000)
	#def savefich(fich):
	#	return ficherosJs

	#def listfich():
	#	return ficherosJs


class FichJs(models.Model):
	exercise = models.CharField(max_length=500)
	urlstudent = models.CharField(max_length=500)
	name = models.CharField(max_length = 500)
	analisisJSLint = models.TextField()
	analisisJSHint = models.TextField()
	sumary = models.TextField()
	data = models.CharField(max_length=10000)
	branch = models.CharField(max_length=500)
	user = models.CharField(max_length=500)
	numorden = models.IntegerField(default=0)

class Error(models.Model):
	exercise = models.CharField(max_length=500)
	student = models.CharField(max_length=500) #StudentExercise, urlStudentEx
	fich = models.CharField(max_length = 500)
	typeoferror = models.CharField(max_length=500)
	description = models.TextField()
	solution = models.CharField(max_length=500)
	numoferror = models.CharField(max_length=500)
	numtypeoferror = models.IntegerField(default=0)
	line = models.CharField(max_length=500)
	branch = models.CharField(max_length=500)
	tool = models.CharField(max_length=500)
	user = models.CharField(max_length=500)
	numorden = models.IntegerField(default=0)

class Library(models.Model):
	name = models.CharField(max_length=500)
	user = models.CharField(max_length=500)