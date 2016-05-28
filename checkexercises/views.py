from django.shortcuts import render

# Create your views here. 
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import TeacherExercise, StudentExercise, FichJs, Error, Library , Usuario

import os
import shutil

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def checkerrorcomplete(descript,line,descript2):
	#print "ENTRO A checkerrorcomplete"
	#print "descript = ", descript 
	#print "line = ", line
	#print "descript2 = ", descript2
	text = ""
	complete = False
	if descript == "": #Es principio de la linea del error
		text = line
		linesplit = line.split(" ")
		print "linesplit = " , linesplit
		if (linesplit[len(linesplit) -2] == "Pos"): #es para ver si el penultimo o ultimo son numeros(indican final del error)
			print "linesplit[len(linesplit) -1] es = " , linesplit[len(linesplit) -1]
			if is_number(linesplit[len(linesplit) -1]) == True: #es fin de error
				complete = True
		else:
			print "linesplit[len(linesplit) -2] es = " , linesplit[len(linesplit) -2]
			if is_number(linesplit[len(linesplit) -2]) == True: #es fin de error
				complete = True
	else: #el error esta a la mitad, hay que anadir la segunda parte
		text = descript + descript2
		linesplit = text.split(" ")
		print "linesplit = " , linesplit
		if (linesplit[len(linesplit) -2] == "Pos"):#es para ver si el penultimo o ultimo son numeros(indican final del error)
			print "linesplit[len(linesplit) -1] es = " , linesplit[len(linesplit) -1]
			if is_number(linesplit[len(linesplit) -1]) == True: #es fin de error
				complete = True
		else:
			print "linesplit[len(linesplit) -2] es = " , linesplit[len(linesplit) -2]
			if is_number(linesplit[len(linesplit) -2]) == True: #es fin de error
				complete = True

	return text, complete

def checktypeoferrorJSLint(error): #seguir anadiendo los diferentes casos de posibles errores
	print "ERROR => " ,error
	linesplit = error.split(" ")
	print "LINESPLIT CHECK ERROR ========= " , linesplit
	solution = ""
	num1 = linesplit[0] #es el numero de error dentro del fichero
	print "num1 es " , num1
	num2 = "" #es el tipo de error
	line = linesplit[len(linesplit) - 4]
	if (line == "Line"):
		line = linesplit[len(linesplit) - 3]

	if (line.find(",") != -1): #porque a veces es "24," por ejemplo y hay que quitar la coma
		print "linesplit[0]pepe = ",line.split(",")[0]
		line = line.split(",")[0]
	print "LEN LINESPLIT ===== ", len(linesplit)
	print "LINE ES IGUAL A = " , line

	if (error.find("is already defined") != -1): 
		print "es error de ===== is already defined"
		solution = "https://jslinterrors.com/a-is-already-defined"
		num2 = 1
		return "'X' is already defined" , solution , num1, num2, line
	elif (error.find("Use the array literal notation") != -1):
		print "es error de ===== Use the array literal notation"
		solution = "https://jslinterrors.com/the-array-literal-notation-is-preferrable"
		num2 = 2
		return "Use the array literal notation", solution, num1, num2, line
	elif (error.find("Avoid 'arguments") != -1):
		print "es error de ===== Avoid 'arguments"
		solution = "https://jslinterrors.com/avoid-arguments"
		num2 = 3
		return "Avoid 'arguments", solution, num1, num2, line
	elif (error.find("Bad assignment") != -1):
		print "es error de ===== Bad assignment"
		solution = "https://jslinterrors.com/bad-assignment"
		num2 = 4
		return "Bad assignment", solution, num1, num2, line
	elif (error.find("Bad constructor") != -1):
		print "es error de ===== Bad constructor"
		solution = "https://jslinterrors.com/bad-constructor"
		num2 = 5
		return "Bad constructor", solution, num1, num2, line
	elif (error.find("was not declared correctly") != -1):
		print "es error de ===== was not declared correctly"
		solution = "https://jslinterrors.com/variable-a-was-not-declared-correctly"
		num2 = 6
		return "Variable 'X' was not declared correctly", solution, num1, num2, line
	elif (error.find("Combine this with the previous") != -1):
		print "es error de ===== Combine this with the previous"
		solution = "https://jslinterrors.com/combine-this-with-the-previous-var-statement"
		num2 = 7
		return "Combine this with the previous 'var' statement", solution, num1, num2, line
	elif (error.find("Confusing use of '-'") != -1):
		print "es error de ===== Confusing use of '-' "
		solution = "https://jslinterrors.com/confusing-minuses"
		num2 = 8
		return "Confusing use of '-'", solution, num1, num2, line
	elif (error.find("Confusing use of '+'") != -1):
		print "es error de ===== Confusing use of '+' "
		solution = "https://jslinterrors.com/confusing-pluses"
		num2 = 9
		return "Confusing use of '+'", solution, num1, num2, line
	elif (error.find("Unexpected dangling '_'") != -1):
		print "es error de ===== Unexpected dangling '_' "
		solution = "https://jslinterrors.com/unexpected-dangling-_-in-a"
		num2 = 10
		return "Unexpected dangling '_' in 'X'", solution, num1, num2, line
	elif (error.find("is better written in dot notation") != -1):
		print "es error de ===== is better written in dot notation"
		solution = "https://jslinterrors.com/a-is-better-written-in-dot-notation"
		num2 = 11
		return "'X'is better written in dot notation", solution, num1, num2, line
	elif (error.find("Duplicate") != -1):
		print "es error de ===== Duplicate"
		solution = "https://jslinterrors.com/duplicate-key-a"
		num2 = 12
		return "Duplicate key 'X'", solution, num1, num2, line
	elif (error.find("Empty class") != -1):
		print "es error de ===== Empty class"
		solution = "https://jslinterrors.com/empty-class"
		num2 = 13
		return "Empty class", solution, num1, num2, line
	elif (error.find("eval is evil") != -1):
		print "es error de ===== eval is evil"
		solution = "https://jslinterrors.com/eval-is-evil"
		num2 = 14
		return "eval is evil", solution, num1, num2, line
	elif (error.find("Expected exactly one space between") != -1):
		print "es error de ===== Expected exactly one space between"
		solution = "https://jslinterrors.com/expected-exactly-one-space-between-a-and-b"
		num2 = 15
		return "Expected exactly one space between 'X' and 'Y'", solution, num1, num2, line
	elif (error.find("Expected a string and instead saw") != -1):
		print "es error de ===== Expected a string and instead saw"
		solution = "https://jslinterrors.com/expected-a-string-and-instead-saw-a"
		num2 = 16
		return "Expected a string and instead saw 'X'", solution, num1, num2, line
	elif (error.find("Expected 'value' and instead saw") != -1):
		print "es error de ===== Expected 'value' and instead saw"
		solution = "https://jslinterrors.com/expected-parameter-value-in-set-a-function"
		num2 = 17
		return "Expected 'value' and instead saw 'X'", solution, num1, num2, line
	elif (error.find("The body of a for in should be wrapped") != -1):
		print "es error de ===== The body of a for in should be wrapped"
		solution = "https://jslinterrors.com/the-body-of-a-for-in-should-be-wrapped-in-an-if-statement"
		num2 = 18
		return "The body of a for in should be wrapped in an if statement to filter unwanted properties from the prototype", solution, num1, num2, line
	elif (error.find("The Function constructor is eval") != -1):
		print "es error de ===== The Function constructor is eval"
		solution = "https://jslinterrors.com/the-function-constructor-is-eval"
		num2 = 19
		return "The Function constructor is eval", solution, num1, num2, line
	elif (error.find("Function statements should not be placed in blocks") != -1):
		print "es error de ===== Function statements should not be placed in blocks"
		solution = "https://jslinterrors.com/function-statements-should-not-be-placed-in-blocks"
		num2 = 20
		return "Function statements should not be placed in blocks", solution, num1, num2, line
	elif (error.find("Don't make functions within a loop") != -1):
		print "es error de ===== Don't make functions within a loop"
		solution = "https://jslinterrors.com/dont-make-functions-within-a-loop"
		num2 = 21
		return "Don't make functions within a loop", solution, num1, num2, line
	elif (error.find("Implied eval is evil. Pass a function instead of a string") != -1):
		print "es error de ===== Implied eval is evil. Pass a function instead of a string"
		solution = "https://jslinterrors.com/implied-eval-is-evil-pass-a-function-instead-of-a-string"
		num2 = 22
		return "Implied eval is evil. Pass a function instead of a string", solution, num1, num2, line
	elif ((error.find("It is not necessary to initialize") != -1) and
			(error.find("to 'undefined'") != -1)):
		print "es error de ===== It is not necessary to initialize 'x' to 'undefined'"
		solution = "https://jslinterrors.com/it-is-not-necessary-to-initialize-a-to-undefined"
		num2 = 23
		return "It is not necessary to initialize 'X' to 'undefined'", solution, num1, num2, line
	elif (error.find("Function statements are not invocable. Wrap the whole function invocation in parens") != -1):
		print "es error de ===== Function statements are not invocable. Wrap the whole function invocation in parens"
		solution = "https://jslinterrors.com/function-statements-are-not-invocable"
		num2 = 24
		return "Function statements are not invocable. Wrap the whole function invocation in parens", solution, num1, num2, line
	elif ((error.find("Do not use") != -1) and
			(error.find("as a constructor") != -1)):
		print "es error de ===== Do not use 'X' as a constructor"
		solution = "https://jslinterrors.com/do-not-use-a-as-a-constructor"
		num2 = 25
		return "Do not use 'X' as a constructor", solution, num1, num2, line
	elif (error.find("radix parameter") != -1):
		print "es error de ===== Missing radix parameter"
		solution = "https://jslinterrors.com/missing-radix-parameter"
		num2 = 26
		return "Missing radix parameter", solution, num1, num2, line
	elif (error.find("Missing 'use strict' statement") != -1):
		print "es error de ===== Missing 'use strict' statement"
		solution = "https://jslinterrors.com/missing-use-strict-statement"
		num2 = 27
		return "Missing 'use strict' statement", solution, num1, num2, line
	elif (error.find("Move the invocation into the parens that contain the function") != -1):
		print "es error de ===== Move the invocation into the parens that contain the function"
		solution = "https://jslinterrors.com/move-the-invocation-into-the-parens-that-contain-the-function"
		num2 = 28
		return "Move the invocation into the parens that contain the function", solution, num1, num2, line
	elif (error.find("Move 'var' declarations to the top of the function") != -1):
		print "es error de ===== Move 'var' declarations to the top of the function"
		solution = "https://jslinterrors.com/move-var-declarations-to-the-top-of-the-function"
		num2 = 29
		return "Move 'var' declarations to the top of the function", solution, num1, num2, line
	elif (error.find("Nested comment") != -1):
		print "es error de ===== Nested comment"
		solution = "https://jslinterrors.com/nested-comment"
		num2 = 30
		return "Nested comment", solution, num1, num2, line
	elif (error.find("Do not use 'new' for side effects") != -1):
		print "es error de ===== Do not use 'new' for side effects"
		solution = "https://jslinterrors.com/do-not-use-new-for-side-effects"
		num2 = 31
		return "Do not use 'new' for side effects", solution, num1, num2, line
	elif (error.find("is not a function") != -1):
		print "es error de ===== is not a function"
		solution = "https://jslinterrors.com/a-is-not-a-function"
		num2 = 32
		return "'X' is not a function", solution, num1, num2, line
	elif (error.find("is not a label") != -1):
		print "es error de ===== is not a label"
		solution = "https://jslinterrors.com/a-is-not-a-label"
		num2 = 33
		return "'X' is not a label", solution, num1, num2, line
	elif (error.find("was used before it was defined") != -1):
		print "es error de ===== was used before it was defined"
		solution = "https://jslinterrors.com/a-was-used-before-it-was-defined"
		num2 = 34
		return "was used before it was defined", solution, num1, num2, line
	elif (error.find("Use the object literal notation {} or Object.create(null)") != -1):
		print "es error de ===== Use the object literal notation {} or Object.create(null)"
		solution = "https://jslinterrors.com/the-object-literal-notation-is-preferrable"
		num2 = 35
		return "Use the object literal notation {} or Object.create(null)", solution, num1, num2, line
	elif (error.find("Don't use octal") != -1):
		print "es error de ===== Don't use octal"
		solution = "https://jslinterrors.com/dont-use-octal-a-use-instead"
		num2 = 36
		return "Don't use octal: '\X'. Use '\u....' instead", solution, num1, num2, line
	elif (error.find("used out of scope") != -1):
		print "es error de ===== used out of scope"
		solution = "https://jslinterrors.com/a-used-out-of-scope"
		num2 = 37
		return "'X' used out of scope", solution, num1, num2, line
	elif (error.find("Read only") != -1):
		print "es error de ===== Read only"
		solution = "https://jslinterrors.com/read-only"
		num2 = 38
		return "Read only", solution, num1, num2, line
	elif (error.find("A regular expression literal can be confused with '/='") != -1):
		print "es error de ===== A regular expression literal can be confused with '/='"
		solution = "https://jslinterrors.com/a-regular-expression-literal-can-be-confused-with"
		num2 = 39
		return "A regular expression literal can be confused with '/='", solution, num1, num2, line
	elif (error.find("Spaces are hard to count") != -1):
		print "es error de ===== Spaces are hard to count"
		solution = "https://jslinterrors.com/spaces-are-hard-to-count-use-a"
		num2 = 40
		return "Spaces are hard to count. Use {'number'}", solution, num1, num2, line
	elif (error.find("Expected an identifier and instead saw") != -1):
		print "es error de ===== Expected an identifier and instead saw"
		solution = "https://jslinterrors.com/expected-an-identifier-and-instead-saw-a-a-reserved-word"
		num2 = 41
		return "Expected an identifier and instead saw 'X' (a reserved word)", solution, num1, num2, line
	elif (error.find("is a statement label") != -1):
		print "es error de ===== is a statement label"
		solution = "https://jslinterrors.com/a-is-a-statement-label"
		num2 = 42
		return "'X' is a statement label", solution, num1, num2, line
	elif (error.find("Stopping") != -1):
		print "es error de ===== Stopping"
		solution = "https://jslinterrors.com/stopping"
		num2 = 43
		return "Stopping. ('X' scanned)", solution, num1, num2, line
	elif (error.find("The '&&' subexpression should be wrapped in parens") != -1):
		print "es error de ===== The '&&' subexpression should be wrapped in parens"
		solution = "https://jslinterrors.com/the-subexpression-should-be-wrapped-in-parens"
		num2 = 44
		return "The '&&' subexpression should be wrapped in parens", solution, num1, num2, line
	elif (error.find("Unexpected TODO comment") != -1):
		print "es error de ===== Unexpected TODO comment"
		solution = "https://jslinterrors.com/unexpected-todo-comment"
		num2 = 45
		return "Unexpected TODO comment", solution, num1, num2, line
	elif (error.find("A trailing decimal point can be confused with a dot") != -1):
		print "es error de ===== A trailing decimal point can be confused with a dot"
		solution = "https://jslinterrors.com/a-trailing-decimal-point-can-be-confused-with-a-dot-a"
		num2 = 46
		return "A trailing decimal point can be confused with a dot: '.'X'.'", solution, num1, num2, line
	elif (error.find("Unclosed comment") != -1):
		print "es error de ===== Unclosed comment"
		solution = "https://jslinterrors.com/unclosed-comment"
		num2 = 47
		return "Unclosed comment", solution, num1, num2, line
	elif (error.find("Unclosed regular expression") != -1):
		print "es error de ===== Unclosed regular expression"
		solution = "https://jslinterrors.com/unclosed-regular-expression"
		num2 = 48
		return "Unclosed regular expression", solution, num1, num2, line
	elif (error.find("Unclosed string") != -1):
		print "es error de ===== Unclosed string"
		solution = "https://jslinterrors.com/unclosed-string"
		num2 = 49
		return "Unclosed string", solution, num1, num2, line
	elif (error.find("Unexpected assignment expression") != -1):
		print "es error de ===== Unexpected assignment expression"
		solution = "https://jslinterrors.com/unexpected-assignment-expression"
		num2 = 50
		return "Unexpected assignment expression", solution, num1, num2, line
	elif (error.find("Unexpected comment") != -1):
		print "es error de ===== Unexpected comment"
		solution = "https://jslinterrors.com/unexpected-comment"
		num2 = 51
		return "Unexpected comment", solution, num1, num2, line
	elif ((error.find("Unexpected parameter") != -1) and
			(error.find("in get") != -1)):
		print "es error de ===== Unexpected parameter 'X' in get 'var' function"
		solution = "https://jslinterrors.com/unexpected-parameter-a-in-get-b-function"
		num2 = 52
		return "Unexpected parameter 'X' in get 'var' function", solution, num1, num2, line
	elif (error.find("Unexpected '++'") != -1):
		print "es error de ===== Unexpected '++'"
		solution = "https://jslinterrors.com/unexpected-plus-plus"
		num2 = 53
		return "Unexpected '++'", solution, num1, num2, line
	elif (error.find("Unexpected sync method") != -1):
		print "es error de ===== Unexpected sync method"
		solution = "https://jslinterrors.com/unexpected-sync-method-a"
		num2 = 54
		return "Unexpected sync method: 'X'", solution, num1, num2, line
	elif (error.find("Unexpected 'with'") != -1):
		print "es error de ===== Unexpected 'with'"
		solution = "https://jslinterrors.com/unexpected-with"
		num2 = 55
		return "Unexpected 'with'", solution, num1, num2, line
	elif (error.find("Missing name in function statement") != -1):
		print "es error de ===== Missing name in function statement"
		solution = "https://jslinterrors.com/missing-name-in-function-statement"
		num2 = 56
		return "Missing name in function statement", solution, num1, num2, line
	elif (error.find("Missing") != -1):
		print "es error de ===== Missing"
		solution = "https://jslinterrors.com/missing-invoking-a-constructor"
		num2 = 57
		return "Missing 'X'", solution, num1, num2, line
	elif (error.find("Unnecessary 'else' after disruption") != -1):
		print "es error de ===== Unnecessary 'else' after disruption"
		solution = "https://jslinterrors.com/unexpected-else-after-return"
		num2 = 58
		return "Unnecessary 'else' after disruption", solution, num1, num2, line
	elif (error.find("Do not wrap function literals in parens unless they are to be immediately invoked") != -1):
		print "es error de ===== Do not wrap function literals in parens unless they are to be immediately invoked"
		solution = "https://jslinterrors.com/do-not-wrap-function-literals-in-parens"
		num2 = 59
		return "Do not wrap function literals in parens unless they are to be immediately invoked", solution, num1, num2, line
	elif (error.find("Unnecessary 'use strict'") != -1):
		print "es error de ===== Unnecessary 'use strict'"
		solution = "https://jslinterrors.com/unnecessary-use-strict"
		num2 = 60
		return "Unnecessary 'use strict'", solution, num1, num2, line
	elif (error.find("Unexpected /*property*/") != -1):
		print "es error de ===== Unexpected /*property*/"
		solution = "https://jslinterrors.com/unregistered-property-name"
		num2 = 61
		return "Unexpected /*property*/ 'X'", solution, num1, num2, line
	elif (error.find("Expected an assignment or function call and instead saw an expression") != -1):
		print "es error de ===== Expected an assignment or function call and instead saw an expression"
		solution = "https://jslinterrors.com/expected-an-assignment-or-function-call"
		num2 = 62
		return "Expected an assignment or function call and instead saw an expression", solution, num1, num2, line
	elif (error.find("Unused") != -1):
		print "es error de ===== Unused"
		solution = "https://jslinterrors.com/unused-a"
		num2 = 63
		return "Unused 'X'", solution, num1, num2, line
	elif ((error.find("A constructor name") != -1) and
			(error.find("should start with an uppercase letter") != -1)):
		print "es error de ===== A constructor name 'X' should start with an uppercase letter"
		solution = "https://jslinterrors.com/a-constructor-name-should-start-with-an-uppercase-letter"
		num2 = 64
		return "A constructor name 'X' should start with an uppercase letter", solution, num1, num2, line
	elif (error.find("Use the isNaN function to compare with NaN") != -1):
		print "es error de ===== Use the isNaN function to compare with NaN"
		solution = "https://jslinterrors.com/use-the-isnan-function-to-compare-with-nan"
		num2 = 65
		return "Use the isNaN function to compare with NaN", solution, num1, num2, line
	elif (error.find("Use a named parameter") != -1):
		print "es error de ===== Use a named parameter"
		solution = "https://jslinterrors.com/use-a-named-parameter"
		num2 = 66
		return "Use a named parameter", solution, num1, num2, line
	elif (error.find("Use the || operator") != -1):
		print "es error de ===== Use the || operator"
		solution = "https://jslinterrors.com/use-the-or-operator"
		num2 = 67
		return "Use the || operator", solution, num1, num2, line
	elif (error.find("Only properties should be deleted") != -1):
		print "es error de ===== Only properties should be deleted"
		solution = "https://jslinterrors.com/only-properties-should-be-deleted"
		num2 = 68
		return "Only properties should be deleted", solution, num1, num2, line
	elif (error.find("Weird assignment") != -1):
		print "es error de ===== Weird assignment"
		solution = "https://jslinterrors.com/weird-assignment"
		num2 = 69
		return "Weird assignment", solution, num1, num2, line
	elif (error.find("Weird relation") != -1):
		print "es error de ===== Weird relation"
		solution = "https://jslinterrors.com/weird-relation"
		num2 = 70
		return "Weird relation", solution, num1, num2, line
	elif (error.find("Wrap an immediate function invocation in parentheses") != -1):
		print "es error de ===== Wrap an immediate function invocation in parentheses"
		solution = "https://jslinterrors.com/wrap-an-immediate-function-invocation-in-parentheses"
		num2 = 71
		return "Wrap an immediate function invocation in parentheses", solution, num1, num2, line
	elif (error.find("Unexpected '--'") != -1):
		print "es error de ===== Unexpected '--'"
		solution = "https://jslinterrors.com/unexpected-plus-plus"
		num2 = 72
		return "Unexpected '--'", solution, num1, num2, line
	elif (error.find("Unexpected character") != -1):
		print "es error de ===== Unexpected character "
		solution = "http://stackoverflow.com/questions/14006876/jslint-unexpected-space-error"
		num2 = 73
		return "Unexpected character 'X'", solution, num1, num2, line
	elif ((error.find("Expected") != -1) and
			(error.find("at column") != -1) and
				(error.find("not column") != -1)):
		print "es error de ===== Expected 'X' at column 'y', not column 'z'"
		solution = "http://www.jameswiseman.com/blog/2011/03/26/coding-convention-an-style-guide/"
		num2 = 74
		return "Expected 'X' at column 'y', not column 'z'", solution, num1, num2, line
	elif ((error.find("Unexpected space between") != -1) and
				(error.find("and") != -1)):
		print "es error de ===== Unexpected space between 'X' and 'Y'"
		solution = "http://stackoverflow.com/questions/14006876/jslint-unexpected-space-error"
		num2 = 75
		return "Unexpected space between 'X' and 'Y'", solution, num1, num2, line
	elif ((error.find("Expected") != -1) and
				(error.find("and instead saw") != -1)):
		print "es error de ===== Expected 'X' and instead saw 'Y'"
		solution = "http://stackoverflow.com/questions/3735939/jslint-expected-and-instead-saw"
		num2 = 76
		return "Expected 'X' and instead saw 'Y'", solution, num1, num2, line
	elif (error.find("Use spaces, not tabs") != -1):
		print "es error de ===== Use spaces, not tabs"
		solution = "http://stackoverflow.com/questions/13913189/why-were-the-new-jslint-errors-use-spaces-not-tabs-and-unsafe-character-int"
		num2 = 77
		return "Use spaces, not tabs", solution, num1, num2, line
	elif (error.find("Unexpected") != -1):
		print "es error de ===== Unexpected"
		solution = "http://stackoverflow.com/questions/4978379/unexpected-jslint-error"
		num2 = 78
		return "Unexpected 'X'", solution, num1, num2, line
	elif (error.find("Don't declare variables in a loop") != -1):
		print "es error de ===== Don't declare variables in a loop"
		solution = "http://www.impressivewebs.com/javascript-for-loop/"
		num2 = 79
		return "Don't declare variables in a loop", solution, num1, num2, line
	elif ((error.find("Cannot read property") != -1) and
				(error.find("of undefined") != -1)):
		print "es error de ===== Cannot read property 'X' of undefined"
		solution = "http://stackoverflow.com/questions/6550795/uncaught-typeerror-cannot-read-property-value-of-undefined"
		num2 = 80
		return "Cannot read property 'X' of undefined", solution, num1, num2, line
	elif (error.find("Redefinition of") != -1):
		print "es error de ===== Redefinition of"
		solution = "https://jslinterrors.com/redefinition-of-a"
		num2 = 81
		return "Redefinition of 'X'", solution, num1, num2, line
	elif (error.find("Too many errors") != -1):
		print "es error de ===== Too many errors"
		solution = ""
		num2 = 82
		return "Too many errors", solution, num1, num2, line
	else: #si anado errores acordarse de en los resumenes tmbn cambiar el numero del bucle
		print "el error aun no esta definido"
		num2 = 83
		return "el error aun no esta definido JSLint", solution, num1, num2, line


def checktypeoferrorJSHint(error): #seguir anadiendo los diferentes casos de posibles errores
	print "entro a checktypeoferrorJSHint"
	errorJSHint = error.split(",")[2]
	print "error = ", errorJSHint
	print "split = ", error.split(",")[0].split("line")
	lineJSHint = error.split(",")[0].split("line")[1].split(" ")[1]
	print "line =", lineJSHint

	if (error.find('Missing "use strict" statement') != -1):
		print "es error JSHINT de ===== Missing 'use strict' statement"
		solution = "https://jslinterrors.com/missing-use-strict-statement"
		num2 = 1
		return "Missing 'use strict' statement", solution, num2, lineJSHint

	elif (error.find("is not defined") != -1):
		print "es error JSHINT de ===== is not defined"
		solution = "http://librosweb.es/libro/javascript/capitulo_3/tipos_de_variables.html"
		num2 = 2
		return "'X' is not defined", solution, num2, lineJSHint

	elif (error.find("Mixed double and single quotes") != -1):
		print "es error JSHINT de ===== Mixed double and single quotes"
		solution = "https://jslinterrors.com/mixed-double-and-single-quotes"
		num2 = 3
		return "Mixed double and single quotes", solution, num2, lineJSHint

	elif (error.find("Creating global 'for' variable. Should be 'for (var i ...'") != -1):
		print "es error JSHINT de ===== Creating global 'for' variable. Should be 'for (var i ...'."
		solution = "http://stackoverflow.com/questions/16539023/creating-global-for-variable-should-be-for-var-items"
		num2 = 4
		return "Creating global 'for' variable", solution, num2, lineJSHint

	elif ((error.find("Identifier") != -1) and
			(error.find("is not in camel case") != -1)):
		print "es error JSHINT de ===== Identifier 'X' is not in camel case."
		solution = "https://jslinterrors.com/option-jshint-camelcase"
		num2 = 5
		return "Identifier 'X' is not in camel case", solution, num2, lineJSHint

	elif (error.find("The body of a for in should be wrapped in an if statement to filter unwanted properties from the prototype") != -1):
		print "es error JSHINT de ===== The body of a for in should be wrapped in an if statement to filter unwanted properties from the prototype"
		solution = "https://jslinterrors.com/the-body-of-a-for-in-should-be-wrapped-in-an-if-statement"
		num2 = 6
		return "The body of a for in should be wrapped in an if statement", solution, num2, lineJSHint

	elif (error.find("is defined but never used") != -1):
		print "es error JSHINT de ===== is defined but never used"
		solution = "http://jslint.fantasy.codes/a-is-defined-but-never-used/"
		num2 = 7
		return "'X' is defined but never used", solution, num2, lineJSHint

	elif (error.find("Unnecessary semicolon") != -1):
		print "es error JSHINT de ===== Unnecessary semicolon"
		solution = "https://jslinterrors.com/unnecessary-semicolon"
		num2 = 8
		return "Unnecessary semicolon", solution, num2, lineJSHint

	elif (error.find("Expected '===' and instead saw '=='") != -1):
		print "es error JSHINT de ===== Expected '===' and instead saw '=='"
		solution = "http://stackoverflow.com/questions/3735939/jslint-expected-and-instead-saw"
		num2 = 9
		return "Expected '===' and instead saw '=='", solution, num2, lineJSHint

	elif (error.find("was used before it was defined") != -1):
		print "es error JSHINT de ===== Expected '===' and instead saw '=='"
		solution = "https://jslinterrors.com/a-was-used-before-it-was-defined"
		num2 = 10
		return "'X' was used before it was defined", solution, num2, lineJSHint

	elif (error.find("Wrap an immediate function invocation in parens to assist the reader in understanding that the expression is the result of a function, and not the function itself") != -1):
		print "es error JSHINT de ===== Wrap an immediate function invocation in parens to assist the reader in understanding that the expression is the result of a function, and not the function itself"
		solution = "https://jslinterrors.com/a-was-used-before-it-was-defined"
		num2 = 11
		return "Wrap an immediate function invocation in parens", solution, num2, lineJSHint

	elif (error.find("Expected '{' and instead saw") != -1):
		print "es error JSHINT de ===== Expected '{' and instead saw"
		solution = "http://stackoverflow.com/questions/9690378/jslint-expected"
		num2 = 12
		return "Expected '{' and instead saw 'X'", solution, num2, lineJSHint

	elif (error.find("Expected an assignment or function call and instead saw an expression") != -1):
		print "es error JSHINT de ===== Expected an assignment or function call and instead saw an expression"
		solution = "https://jslinterrors.com/expected-an-assignment-or-function-call"
		num2 = 13
		return "Expected an assignment or function call and instead saw an expression", solution, num2, lineJSHint

	elif (error.find("Expected a conditional expression and instead saw an assignment") != -1):
		print "es error JSHINT de ===== Expected a conditional expression and instead saw an assignment"
		solution = "https://jslinterrors.com/unexpected-assignment-expression"
		num2 = 14
		return "Expected a conditional expression and instead saw an assignment", solution, num2, lineJSHint

	elif (error.find("Missing 'new' prefix when invoking a constructor") != -1):
		print "es error JSHINT de ===== Missing 'new' prefix when invoking a constructor"
		solution = "http://stackoverflow.com/questions/27380469/jshint-and-function-gets-missing-new-prefix-when-invoking-a-constructor"
		num2 = 15
		return "Missing 'new' prefix when invoking a constructor", solution, num2, lineJSHint

	elif (error.find("Unexpected use of '++'") != -1):
		print "es error JSHINT de ===== Unexpected use of '++'"
		solution = "https://jslinterrors.com/unexpected-plus-plus"
		num2 = 16
		return "Unexpected use of '++'", solution, num2, lineJSHint

	elif (error.find("A leading decimal point can be confused with a dot:") != -1):
		print "es error JSHINT de ===== A leading decimal point can be confused with a dot:"
		solution = "https://jslinterrors.com/a-leading-decimal-point-can-be-confused-with-a-dot-a"
		num2 = 17
		return "A leading decimal point can be confused with a dot: .'X'", solution, num2, lineJSHint

	elif (error.find("Expected '!==' and instead saw '!='") != -1):
		print "es error JSHINT de ===== Expected '!==' and instead saw '!='"
		solution = "http://stackoverflow.com/questions/3735939/jslint-expected-and-instead-saw"
		num2 = 18
		return "Expected '!==' and instead saw '!='", solution, num2, lineJSHint

	elif (error.find("is better written in dot notation") != -1):
		print "es error JSHINT de ===== is better written in dot notation"
		solution = "https://jslinterrors.com/a-is-better-written-in-dot-notation"
		num2 = 19
		return "['X'] is better written in dot notation", solution, num2, lineJSHint

	elif (error.find("A constructor name should start with an uppercase letter") != -1):
		print "es error JSHINT de ===== A constructor name should start with an uppercase letter"
		solution = "https://jslinterrors.com/a-constructor-name-should-start-with-an-uppercase-letter"
		num2 = 20
		return "A constructor name should start with an uppercase letter", solution, num2, lineJSHint

	elif (error.find("'hasOwnProperty' is a really bad name") != -1):
		print "es error JSHINT de ===== 'hasOwnProperty' is a really bad name"
		solution = "https://jslinterrors.com/hasownproperty-is-a-really-bad-name"
		num2 = 21
		return "'hasOwnProperty' is a really bad name", solution, num2, lineJSHint

	elif (error.find("Extending prototype of native object:") != -1):
		print "es error JSHINT de ===== Extending prototype of native object:"
		solution = "https://jslinterrors.com/extending-prototype-of-native-object"
		num2 = 22
		return "Extending prototype of native object: 'X'", solution, num2, lineJSHint

	elif (error.find("Missing '()' invoking a constructor") != -1):
		print "es error JSHINT de ===== Missing '()' invoking a constructor"
		solution = "https://jslinterrors.com/missing-invoking-a-constructor"
		num2 = 23
		return "Missing '()' invoking a constructor", solution, num2, lineJSHint

	elif (error.find("Bad line breaking before") != -1):
		print "es error JSHINT de ===== Bad line breaking before"
		solution = "http://stackoverflow.com/questions/15140740/explanation-of-jshints-bad-line-breaking-before-error"
		num2 = 24
		return "Bad line breaking before 'X'", solution, num2, lineJSHint

	elif (error.find("Too many errors") != -1):
		print "es error JSHINT de ===== Too many errors"
		solution = ""
		num2 = 25
		return "Too many errors.", solution, num2, lineJSHint

	elif (error.find("is already defined") != -1): 
		print "es error de ===== is already defined"
		solution = "https://jslinterrors.com/a-is-already-defined"
		num2 = 26
		return "'X' is already defined" , solution , num2, lineJSHint
	else: #si anado errores acordarse de en los resumenes tmbn cambiar el numero del bucle
		print "el error aun no esta definido"
		solution = ""
		num2 = 27
		return "el error aun no esta definido JSHint", solution, num2, lineJSHint


def is_fich_library(name):#anadir mas librerias si me voy dando cuenta
	print "###########################################"
	print "NOMBRE DEL FICHERO = ", name
	print "longitud del fichero" , len(name)
	es_library = ""
	if (name.find(".min.js") != -1):#es libreria siempre
		print "entra en es library 1"
		es_library = True
	
	elif (name.find("-src.js") != -1):
		print "entra en es library 2"
		es_library = True
	elif(name.find("jquery-ui") != -1):  
		print "entra en es library 3"
		if(len(name) == 12):
			es_library = True
		else:
			es_library = False
	elif (name.find("jquery") != -1):
		print "entra en es library 4"
		if(len(name) == 9):
			es_library = True
		else:
			es_library = False

	elif(name.find("jQuery") != -1):
		print "entra en es library 5"
		if(len(name) == 9):
			es_library = True
		else:
			es_library = False
	elif(name.find("bootstrap") != -1):
		print "entra en es library 6"
		if(len(name) == 12):
			es_library = True
		else:
			es_library = False
	elif(name.find("npm") != -1):
		print "entra en es library 7"
		if(len(name) == 6):
			es_library = True
		else:
			es_library = False
	elif(name.find("leaflet") != -1):
		print "entra en es library 8"
		if(len(name) == 10):
			es_library = True
		else:
			es_library = False
	else:
		print "NO ES LIBRERIA"
		print "###########################################"
		es_library = False

	if(es_library == False): #si no es ninguna de las de por defecto busco en la base de datos
		librerias = Library.objects.all()
		for i in librerias:
			print "comparar con ", i.name
			if(i.name == name):
				print "es libreria de base de datos 1"
				es_library = True
					

	print "ES LIBRARY => ", es_library
	return es_library

def is_dir(name):
	fichero = name.split(".")
	isfich = False
	try:
		os.chdir(name) #intento entrar para ver si es directorio
		os.chdir("..") #si he entrado salgo para estar donde estaba ya que lo analizo en otra funcion
		print "Es directorio"
		isfich = True
	except:
		print "No es directorio"
		isfich = False
	
	return isfich

def is_fich_js(name):
	fichero = name.split(".")
	if fichero[len(fichero) -1 ] == "js":
		return True
	else:
		return False

def grafica(fichero,url,rama,username,numordenew):
	#########guardar los errores y el numero que hay
	print "entro a grafica"
	erroresJSLint = Error.objects.filter(fich=fichero).filter(student=url).filter(user=username).filter(branch=rama).filter(tool="JSLint").filter(numorden=numordenew).order_by("numtypeoferror") #filt
	cont = 1
	numerrores = 0
	trueerror = False
	data = fichero + "errorspace"
	if(len(erroresJSLint) != 0):
		print "ENTRA EN JSLINT"
		while (cont < 84): #actualizar el 84 si pongo mas errores
			for e in erroresJSLint:
				if(e.numtypeoferror == cont):
					numerrores = numerrores + 1
					trueerror = True
					errortype = e.typeoferror
			if(trueerror):
					data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

			cont = cont + 1
			numerrores = 0
			trueerror = False

	erroresJSHint = Error.objects.filter(fich=fichero).filter(student=url).filter(user=username).filter(branch=rama).filter(tool="JSHint").filter(numorden=numordenew).order_by("numtypeoferror") #filt
	cont = 1
	numerrores = 0
	trueerror = False
	
	if(len(erroresJSHint) != 0):
		print "ENTRA EN JSHINT"
		data += "JSHinterrorspace0errorspace"
		while (cont < 28): #actualizar el 28 si pongo mas errores
			for e in erroresJSHint:
				if(e.numtypeoferror == cont):
					numerrores = numerrores + 1
					trueerror = True
					errortype = e.typeoferror
			if(trueerror):
					data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

			cont = cont + 1
			numerrores = 0
			trueerror = False
	
	return data


def analiz_fichJSLint(name,studenturl,rama,username,numordernew):
	analizo = os.popen('jslint --maxerr=100 '+name).read().split("#") #--white=true --unparam=true
	texto = ""
	namefich = True
	description1 = ""
	description2 = ""
	complete = False
	for j in analizo: #para que al mostrarlos se vean los saltos de linea
		palabras = j.split(" ")
		#print "palabras[0] : ", palabras[0]
		if is_number(palabras[0]):#si es numero palabras[0] es principio de frase
			#print "is number ", palabras[0]
			#comprobar si el fichero es libreria o no para analizarlo
			description1,complete = checkerrorcomplete(description1,j,description2)
			texto += "\n#" + j

		else:#si no es numero lo anado a continuacion, porque he hecho split por '#'
			#print "no es numero es palabra ", palabras[0]
			#print "frase : ", j
			if namefich: #para que no salga el nombre del fichero repetido
				namefich = False
			else:
				texto += "#" + j
				#comprobar si el fichero es libreria o no para analizarlo
				description2 = "#" + j
				description1,complete = checkerrorcomplete(description1,j,description2)

		print "complete = ", complete	
		if complete == True: #si complete es true es que el error esta entero y lo puedo analizar(si esta en dos partes)
			#funcion para comprobar el error para typeoferror
			
			
			kinderror , sol , num1, num2, lineerror = checktypeoferrorJSLint(description1)
			
			path = os.getcwd()
			#print "path = ",path
			nameexercise = studenturl.split("/")[4]
			#print "nameexercise = ", nameexercise
			pathsplit = path.split(nameexercise)
			#print "len(pathsplit) = ", len(pathsplit)
			if(pathsplit[1] != ""): #aqui hacer if /blob/gh-pages
				#print "pathsplith 1 = ", pathsplit[1]
				lineer = studenturl+"/blob/"+rama + pathsplit[1] + "/" + name +"#L"+lineerror
			else:
				#print "pathsplith 0 = ", pathsplit[0]
				lineer = studenturl+"/blob/"+rama+"/" + name +"#L"+lineerror

			if kinderror != "": #ahora se cumple siempre por que busco los errores que no estan definidos aun
				print "creo el error"
				exer = StudentExercise.objects.get(urlStudentEx = studenturl,branch=rama,user=username,numorden=numordernew).urlTeacherEx
				newError = Error(exercise= exer,
							student= studenturl,
							fich=name,
					 		typeoferror=kinderror,
					 		description= description1,
					 		solution = sol,
					 		numoferror= num1,
					 		numtypeoferror= num2,
					 		line= lineer,
					 		branch=rama,
					 		tool="JSLint",
					 		user=username,
					 		numorden=numordernew)
				newError.save()

			print "reinicio variables"
			description1=""
			description2=""
			complete = False
			cont_errors=num1

	return texto,cont_errors

def analiz_fichJSHint(name,studenturl,rama,cont_errors,username,numordernew):
	print "$$$$$$$$$$$$$$$$$$$$$$$$JSHINT$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
	print "name = ", name
	#tengo que copiar el fichero de configuracion de jshint a la carpeta en la que este con os.system
	#para pasarselo en el os.popen que hago a continuacion
	#supongo que con os.system haciendo pwd me dara el directorio en el que estoy ahora mismo
	dircp = os.popen("pwd").read()
	print "dircp = ", dircp
	os.system('cp /Users/adrianvinuelas/Universidad/TFG/tfgproject/myoptions.jshintrc ' + dircp)
	analizo = os.popen('jshint '+ name + ' --config myoptions.jshintrc').read() #--white=true --unparam=true --maxerr=100
	print "analizado"
	print "ANALIZO EN JSHINT ES ", analizo 

	analizosplit = analizo.split(name+":")
	print "ANALIZOSPLIT EN JSHINT ES ", analizosplit
	print "cont_errors = ", cont_errors
	conterrores = int(cont_errors) + 1
	texto= ""
	for j in analizosplit:
		if(j != '' and j.find('ES5 option is now set per default') == -1):
			kinderror , sol , num2, lineerror = checktypeoferrorJSHint(j)
			print "salgo de checktypeoferror"
			if(j.find("errors") != -1): #es el ultimo error que es el que contiene el numero de errores total
				ersplit = j.split("\n")
				print "len(ersplit) = ", len(ersplit)
				print "ersplit = ", ersplit
				print "num = ", ersplit[2].split(" ")[0]
				num1 = int(ersplit[2].split(" ")[0]) - 1 #esto lo hacia para cuando le quitaba un error por el primer warning que lo quitaba
				description1 = str(conterrores)+ ". "+name+ ":" + ersplit[0] + "\n"
			else:
				description1 = str(conterrores) + ". "+name+ ":" + j
			
			print "creo la desciption1 = ", description1

			texto += description1 

			path = os.getcwd()
			print "path = ",path
			nameexercise = studenturl.split("/")[4]
			print "nameexercise = ", nameexercise
			pathsplit = path.split(nameexercise)
			print "len(pathsplit) = ", len(pathsplit)
			if(pathsplit[1] != ""): #aqui hacer if /blob/gh-pages
				print "pathsplith 1 = ", pathsplit[1]
				lineer = studenturl+"/blob/"+rama + pathsplit[1] + "/" + name +"#L"+lineerror
			else:
				print "pathsplith 0 = ", pathsplit[0]
				lineer = studenturl+"/blob/"+rama+"/" + name +"#L"+lineerror

			if kinderror != "": #ahora se cumple siempre por que busco los errores que no estan definidos aun
				print "creo el error JSHint"
				exer = StudentExercise.objects.get(urlStudentEx = studenturl,branch=rama,user=username,numorden=numordernew).urlTeacherEx
				newError = Error(exercise= exer,
							student= studenturl,
							fich=name,
					 		typeoferror=kinderror,
					 		description= description1,
					 		solution = sol,
					 		numoferror= conterrores,
					 		numtypeoferror= num2,
					 		line= lineer,
					 		branch=rama,
					 		tool="JSHint",
					 		user=username,
					 		numorden=numordernew)
				newError.save()

			conterrores = conterrores + 1

	return texto

def search_fich_js(directorio,url,exerciseteach,numfichanaliz,rama,username,numordenew):
	print "----ANALIZO LA CARPETA LLAMADA ", directorio
	os.chdir(directorio)
	dirs = os.listdir(".")
	print "dirs = ", dirs
	for i in dirs:
		print "fichero  " + i
		is_optional = True
		try:
			isdir = is_dir(i)
			if isdir == True:
				print "es carpeta , " + i
				numfichanaliz = search_fich_js(i,url,exerciseteach,numfichanaliz,rama,username,numordenew)#si es directorio vuelvo a buscar dentro
				os.chdir("..") #para volver a la carpeta superior
			else:
				isjs = is_fich_js(i)
				if (isjs == True): #si es js y no libreria lo analizo y lo guardo
					#pintar analizo y ver cual es la salida pero sin hacer el split
					print "es fichero .js -> " , i
					is_library = is_fich_library(i)
					if (is_library == False):
						print "1----------- " , i , " --------------------1"
						#print os.popen('jslint ' +i).read()
						#print "-----------##################################--------------------"
						print "analizo el fichero js " , i
						texto,cont_errors = analiz_fichJSLint(i,url,rama,username,numordenew)
						textoJSHINT = analiz_fichJSHint(i,url,rama,cont_errors,username,numordenew)
						numfichanaliz = int(numfichanaliz) + 1
						print "antes de hacer newFich"
						#RESUMEN JSLINT descomentar cuando vuelva a poner a jslint
						#filtro los errores por ejercicio de estudiante y por el nombre del fichero y por herramienta
						erroresJSLint = Error.objects.filter(student=url).filter(fich=i).filter(branch=rama).filter(user=username).filter(tool="JSLint").filter(numorden=numordenew).order_by("numtypeoferror")
						erroresJSHint = Error.objects.filter(student=url).filter(fich=i).filter(branch=rama).filter(user=username).filter(tool="JSHint").filter(numorden=numordenew).order_by("numtypeoferror")
						print "Numero de errores JSLint antes de resumen fich = " , len(erroresJSLint)
						print "Numero de errores JSHint antes de resumen fich = " , len(erroresJSHint)
						resumen = ""

						if((len(erroresJSLint) != 0) or (len(erroresJSHint) != 0)):
							if(((len(erroresJSLint) == 1) and (len(erroresJSHint) == 0)) or
								((len(erroresJSLint) == 0) and (len(erroresJSHint) == 1))):
								resumen= "<p class='sumary'>ERROR SUMARY -> 1 error</p><p>"
							else:
								sumerrors = len(erroresJSLint) + len(erroresJSHint)
								resumen= "<p class='sumary'>ERROR SUMARY -> "+ str(sumerrors) +" errors</p><ol>"
						
							cont = 1
							trueerror = False
							print "antes del while JSLINT"
							while (cont < 84): #actualizar el 84 si pongo mas errores
								for e in erroresJSLint:
									if(e.numtypeoferror == cont):
										print "hay error del tipo " , e.typeoferror
										trueerror = True
										errortype = e.typeoferror
										solerror = e.solution
								if(trueerror):
									resumen += "<li><big><strong>" + errortype + " :</strong></big> "
									for e in erroresJSLint:
										if(e.numtypeoferror == cont):
											resumen += "<br><b>" + e.numoferror + " -> </b>"
											resumen += "<a href="+e.line+" class='redir' target='_blank'>"+e.line+"</a>"
									#resumen += "<p><a href={{"+solerror+"}}>"+solerror+"</a></p></li>"
									#hacer en el css que al hover se subraye el text y el raton cambie la forma que
									#creo que tambien se puede
									if(solerror != ""):
										resumen += "<br>Sol: <a href="+solerror+" class='redir' target='_blank'>"+solerror+"</a></li>"
								cont = cont + 1      
								trueerror = False

							#RESUMEN JSHINT
							#filtro los errores por ejercicio de estudiante y por el nombre del fichero y por herramienta
							
							cont = 1
							trueerror = False
							print "antes del while JSHINT"
							while (cont < 28): #actualizar el 28 si pongo mas errores
								for e in erroresJSHint:
									if(e.numtypeoferror == cont):
										print "hay error del tipo " , e.typeoferror
										trueerror = True
										errortype = e.typeoferror
										solerror = e.solution
								if(trueerror):
									resumen += "<li><big><strong>" + errortype + " :</strong></big> "
									for e in erroresJSHint:
										if(e.numtypeoferror == cont):
											resumen += "<br><b>" + e.numoferror + " -> </b>"
											resumen += "<a href="+e.line+" class='redir' target='_blank'>"+e.line+"</a>"
									#resumen += "<p><a href={{"+solerror+"}}>"+solerror+"</a></p></li>"
									#hacer en el css que al hover se subraye el text y el raton cambie la forma que
									#creo que tambien se puede
									if(solerror != ""):
										resumen += "<br>Sol: <a href="+solerror+" class='redir' target='_blank'>"+solerror+"</a></li>"
								cont = cont + 1      
								trueerror = False
							resumen += "</ol>"
						else:
							resumen= "<p class='sumary'>ERROR SUMARY -> 0 errors</p>"

						print "resumen hecho"
						data = grafica(i,url,rama,username,numordenew) #data para la grafica JSLint y JSHint conjunta
						print "despues de las graficas"
						newfich = FichJs(exercise = exerciseteach,
										 urlstudent = url,
										 name = i,
										 analisisJSLint = texto,
										 analisisJSHint = textoJSHINT,
										 sumary= resumen,
										 data = data,
										 branch=rama,
										 user=username,
										 numorden=numordenew)
						newfich.save()
						print "guardo el fichero " + i
						print "2------------- ",i ," ------------------2"	
		except:
				print "es carpeta en el except " + i

	return numfichanaliz


def analiz_repo(repoanalyze,exercise,rama,username,numordenew):
	print "post de urlanaliz"
	borrarcarpeta = False
	url = repoanalyze
	is_repo_analiz = StudentExercise.objects.get(urlStudentEx = url,branch=rama,user=username,numorden=numordenew).analizado
	print "esta el repositorio analizado = " , is_repo_analiz
	if(is_repo_analiz == False): 
		carpeta = url.split("/")[4]
		borrarcarpeta = True
		goanalyz = True
		print "urlanaliz = " + url
		print "carpeta = " + carpeta
		os.system("echo hola")
		os.system("pwd")
		os.system("echo despues de pwd")
		os.system("mkdir fichanaliz")
		os.chdir("fichanaliz")
		os.system("git clone "+url) #problema cuando es gh-pages y no tiene nada, que descargo la master
		if(rama == "gh-pages"): #hacer un try que si salta el error de fetch no hacer search_fich_js
			print "ES GH-PAGES" #pasa con https://github.com/islimane/X-Nav-5.11.2-OpenWebApps(gh-pages)
			os.chdir(carpeta)
			salida = os.system("git checkout gh-pages")
			print "entre medias del checkout y del fetch"
			os.system("git fetch")
			print "antes de comprobar el error"
			print "salida = ", salida
			if (salida != 0): #si es distinto de 0 es porque ha fallado el checkout gh-pages
				print "Ha habido error al clonar el gh-pages"
				goanalyz = False
				numfichanalyz = "0"

			os.chdir("..")
		
		if goanalyz:
			print "analizo el repositorio"
			numfichanalyz = search_fich_js(carpeta, url,exercise,"0",rama,username,numordenew) #analizo el repositorio
		
		nofich = False
		#actualizo el repositorio para indicar que ha sido analizado por
		#si mas adelante lo vuelven a ver mirarlo en la base de datos directamente
		
		ficheros = FichJs.objects.filter(urlstudent=url).filter(branch=rama).filter(user=username).filter(numorden=numordenew)#quizas si no hay ficheros en el resumen poner que no hay nada o algo asi
		if (len(ficheros) == 0):
			nofich = True

		print "--------------ANTES DE RESUMEN GENERAL DEL REPOSITORIO ALUMNO " + url +" --------------"
		erroresJSLint = Error.objects.filter(student=url).filter(branch=rama).filter(user=username).filter(tool="JSLint").filter(numorden=numordenew).order_by("numtypeoferror") #filtro por el nombre del repositorio(url del estudiante)
		erroresJSHint = Error.objects.filter(student=url).filter(branch=rama).filter(user=username).filter(tool="JSHint").filter(numorden=numordenew).order_by("numtypeoferror")
		print "Numero de errores JSLint antes del analisis -> ", len(erroresJSLint)
		print "Numero de errores JSHint antes del analisis -> ", len(erroresJSHint)

		print "calculo porcentajes de errores JSLint y JSHint"
		#calculo el porcentaje de errores JSLint y JSHint segun el numero de ficheros entregados
		if numfichanalyz != "0":
			nerrorstotal = int(numfichanalyz) * 200 #como mucho cda fichero tiene 200 errores(100 JSLint y 100 JSHint) por el momento * numficheros
			if(len(erroresJSLint) == 101 and len(erroresJSHint) == 101):
				nerrorsreal = (len(erroresJSLint) - 1) + (len(erroresJSHint) - 1)
			else:
				nerrorsreal = len(erroresJSLint) + len(erroresJSHint)
			porcentajeerrores = (nerrorsreal * 100) / nerrorstotal
			print "Numero de errores totales posible = " , nerrorstotal
			print "Numero de errores reales  = ", nerrorsreal
			print "Porcentaje de errores  = " , porcentajeerrores
		else:
			porcentajeerrores = 0;

		print "Antes de iniciar el resumen"
		#En el resumen tengo que hacer dos partes, la de JSLint y la de JSHint 
		resumen = ""
		sumerrors = 0
		if((len(erroresJSLint) != 0) or (len(erroresJSHint) != 0)):
			if(((len(erroresJSLint) == 1) and (len(erroresJSHint) == 0)) or
				((len(erroresJSLint) == 0) and (len(erroresJSHint) == 1))):
				resumen= "<p class='sumary'>ERROR SUMARY -> 1 error</p><p>"
				sumerrors = 1
			else:
				sumerrors = len(erroresJSLint) + len(erroresJSHint)
				resumen= "<p class='sumary'>ERROR SUMARY -> "+ str(sumerrors) +" errors</p><p>"
			cont = 1
			numerrores = 0
			trueerror = False
			
			if(len(erroresJSLint) != 0):
				while (cont < 84): #hacer el resumen global actualizar el 84 si pongo mas errores
					for e in erroresJSLint:
						if(e.numtypeoferror == cont):
							numerrores = numerrores + 1
							print "hay error general JSLint del tipo " , e.typeoferror
							trueerror = True
							errortype = e.typeoferror
					if(trueerror):
						if(numerrores == 1):
							resumen += "<li><strong>" + errortype + " :</strong> " + str(numerrores) +" error</li>"
						else:
							resumen += "<li><strong>" + errortype + " :</strong> " + str(numerrores) +" errors</li>"
					cont = cont + 1
					numerrores = 0
					trueerror = False

			cont = 1
			numerrores = 0
			trueerror = False
			
			if(len(erroresJSHint) != 0):
				while (cont < 28): #hacer el resumen global actualizar el 28 si pongo mas errores
					for e in erroresJSHint:
						if(e.numtypeoferror == cont):
							numerrores = numerrores + 1
							print "hay error general JSHint del tipo " , e.typeoferror
							trueerror = True
							errortype = e.typeoferror
					if(trueerror):
						if(numerrores == 1):
							resumen += "<li><strong>" + errortype + " :</strong> " + str(numerrores) +" error</li>"
						else:
							resumen += "<li><strong>" + errortype + " :</strong> " + str(numerrores) +" errors</li>"
					cont = cont + 1
					numerrores = 0
					trueerror = False
			resumen += "</p>"
		else:
			resumen= "<p class='sumary'>ERROR SUMARY -> 0 errors</p>"

		print "--------------DESPUES DE RESUMEN GENERAL DEL REPOSITORIO ALUMNO " +exercise +" --------------"
		student = StudentExercise.objects.get(urlStudentEx = url,branch=rama,user=username,numorden=numordenew)
		urlteacher = student.urlTeacherEx
		ficheros = FichJs.objects.filter(urlstudent=url).filter(branch=rama).filter(user=username).filter(numorden=numordenew)
		#estudiante = Student.objects.get(name=student.nameStudent)
		#estudiante.errors = int(estudiante.errors) + len(errores)
		#estudiante.save()
		student.sumary = resumen
		student.analizado = True
		student.nofichfind = nofich
		student.numfichanaliz = numfichanalyz
		student.porcenterrorsfich = porcentajeerrores
		student.numoferrors = str(sumerrors)
		print "lenfichfirst ", student.nameStudent , " = ", len(ficheros)
		if(len(ficheros)>= 1):
			student.firstfich = ficheros[0].name
			student.hayfirstfich = True
			print "entra en hay ficheros"
		else:
			student.firstfich = ""
			student.hayfirstfich = False
			print "entra en no hay ficheros"
		student.save()

		
		print "student " + url + " actualizado"
		print "fin de analizar a " + url
	else:
		#no entro nunca en este else desde profesor, desde alumno ya veremos pero creo que tampoco
		#hacer el resumen global del repositorio(ya vere como lo hago hablar con gregorio primero)
		urlteacher = StudentExercise.objects.get(urlStudentEx = url).urlTeacherEx
	

	if(borrarcarpeta == True):
		if(goanalyz == False):
			print "entro a borrar carpeta y no he analizado"
			os.chdir("..")
			shutil.rmtree("fichanaliz") #borro la carpeta que me he creado para analizar el repo
		else:
			print "entra a borrar carpeta"
			os.chdir(os.pardir)
			print "entra a borrar carpeta1"
			os.chdir(os.pardir)
			print "entra a borrar carpeta2"
			shutil.rmtree("fichanaliz") #borro la carpeta que me he creado para analizar el repo
			print "entra a borrar carpeta3"

def ranknumficheros(ejer,rama,username,numordernew):
	print "entra a ranknumficheros"
	#Cojo los ejercicios de los estudiantes y hago la lista de entregados y no entregados
	exerstudents = StudentExercise.objects.filter(urlTeacherEx = ejer).filter(branch=rama).filter(user=username).filter(numorden=numordernew)
	#localizo los que no tienen el ejercicio entregados y lo que si
	noentregado = []
	entregado = []
	for i in exerstudents:
		if i.nofichfind:
			noentregado.append(i)
		else:
			entregado.append(i)
	
	#Hago el ranking ordenando por ficheros entregados
	esprimer = True
	entregadodefinit1 = []

	print "3333333333333333333333333333333333333333333333333333333333333333333333333"
	print "3333333333333333333333333333333333333333333333333333333333333333333333333"
	print "3333333333333333333333333333333333333333333333333333333333333333333333333"
	print "3333333333333333333333333333333333333333333333333333333333333333333333333"
	print "3333333333333333333333333333333333333333333333333333333333333333333333333"
	
	print "Entra a ranking"
	for i in entregado:
		if esprimer == False:
			pos = 0 #no se donde se coloca aun
			colocar = False
			cont = 0 #para recorrer la lista definitiva
			anadirfin = False
			while (colocar != True):
				alumncomparar = entregadodefinit1[cont]
				print "ALUMNOS A COMPARAR : "
				print i.nameStudent, " vs " , alumncomparar.nameStudent
				print i.numfichanaliz, " vs " , alumncomparar.numfichanaliz
				if (int(i.numfichanaliz) > int(alumncomparar.numfichanaliz)):
					print "es mejor fich ", i.nameStudent
					pos = cont
					print "pos = ", pos
					colocar = True
				elif (int(i.numfichanaliz) == int(alumncomparar.numfichanaliz)):
					if(int(i.porcenterrorsfich) < int(alumncomparar.porcenterrorsfich)): #si el numero de ficheros es el mismo
						pos = cont							  #pero tiene menos porcentaje de errores (es mejor )
						colocar = True
						print "es mejor1 ", i.nameStudent
					else: #no es mejor
						if ((cont + 1) == len(entregadodefinit1)): #anado al final
							print "anado al final1 "
							anadirfin = True
							colocar = True
						else:
							print "sigo comparando1"
							cont = cont + 1 
							colocar = False

				else:#si el numero de ficheros es menor claramente es peor alumno en este sentido
					if ((cont + 1) == len(entregadodefinit1)): #anado al final
						print "anado al final "
						anadirfin = True
						colocar = True
					else:
						print "sigo comparando"
						cont = cont + 1 
						colocar = False

			#ANADO EN LA LISTA DEFINITIVA
			if anadirfin:
				entregadodefinit1.append(i)
			else:
				entregadodefinit1.insert(pos,i)
		else:
			print "es primer"
			esprimer = False
			entregadodefinit1.append(i)

	#busco los casos especiales y despues los quito demomento solo hay para JSLint
	casosespeciales1 = []
	for i in entregadodefinit1:
		try:
			Er = Error.objects.filter(exercise = ejer).filter(typeoferror="Stopping. ('X' scanned)").filter(branch=rama).filter(tool="JSLint").filter(user=username).filter(numorden=numordernew)
			for e in Er:
				if(e.student == i.urlStudentEx):
					print "estudiante " , i.nameStudent, " es caso especial"
					casosespeciales1.append(i)
		except:
			print "no errores"
	#quito los casos especiales de la lista definitiva
	#for i in casosespeciales1:
	#	pos = 0
	#	for e in entregadodefinit1:
	#		if(e.nameStudent == i.nameStudent):
	#			posdelete = pos
	#		pos = pos + 1

	#	entregadodefinit1.pop(posdelete)

	#hago el ranking

	print "44444444444444444444444444444444444444444444444444444444444444444444444444444444"
	print "44444444444444444444444444444444444444444444444444444444444444444444444444444444"
	print "44444444444444444444444444444444444444444444444444444444444444444444444444444444"
	print "44444444444444444444444444444444444444444444444444444444444444444444444444444444"
	print "44444444444444444444444444444444444444444444444444444444444444444444444444444444"


	rankingfich = "<br><br><table class='table table-striped'>"
	rankingfich += "<thead class='thead-inverse' style='background-color:black; color: white'><tr><th>Pos</th><th>Student</th>"	
	rankingfich += "<th>Num fichs</th><th>Percent errors</th></tr></thead><tbody>" 
  
	numrow = 1
	cont2 = 0
	primer = True

	
	print "RANKING FICHEROS"
	for i in entregadodefinit1:
		stop = False
		if primer == False:
			alumprev = entregadodefinit1[cont2]
			if(int(i.numfichanaliz) < int(alumprev.numfichanaliz)):
				numrow = numrow + 1
			if(len(casosespeciales1) != 0):	
				for al in casosespeciales1:
					if(i.nameStudent == al.nameStudent):
						stop = True

			if(stop == True):
				rankingfich += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i.nameStudent +" (JSLint Stopped)</td>"
				rankingfich += "<td>"+ i.numfichanaliz +"</td><td>"+ i.porcenterrorsfich +"</td></tr>"
			else:
				rankingfich += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i.nameStudent +"</td>"
				rankingfich += "<td>"+ i.numfichanaliz +"</td><td>"+ i.porcenterrorsfich +"</td></tr>"	
			
			cont2 = cont2 + 1	

		else:
			if(len(casosespeciales1) != 0):				
				for al in casosespeciales1:
					if(i.nameStudent == al.nameStudent):
						stop = True

			if(stop == True):
				rankingfich += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i.nameStudent +" (JSLint Stopped)</td>"
				rankingfich += "<td>"+ i.numfichanaliz +"</td><td>"+ i.porcenterrorsfich +"</td></tr>"
			else:
				rankingfich += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i.nameStudent +"</td>"
				rankingfich += "<td>"+ i.numfichanaliz +"</td><td>"+ i.porcenterrorsfich +"</td></tr>"
			
			primer = False
	
	rankingfich += "</tbody></table>"
	
	if(len(noentregado) != 0):
		rankingfich += "<table class='table table-striped'><thead class='thead-default' style='background-color: #F08080;'>"
		rankingfich += "<tr><th>Undelivered</th><th>Student</th></tr></thead><tbody>"

		for i in noentregado:
			numrow = numrow + 1
			rankingfich += "<tr><th scope='row'>"+str(numrow)+"</th><td>" + i.nameStudent +"</td></tr>"

		rankingfich += "</tbody></table>"
	print "sale de ranknumficheros"
	return rankingfich

def rankpercenterrors(ejer,rama,username,numordernew):
	print "entra a rankpercenterrors"
	#primero hago los resumenes del ejercicio JSLint
	exerstudents = StudentExercise.objects.filter(urlTeacherEx = ejer).filter(branch=rama).filter(user=username).filter(numorden=numordernew)
	#localizo los que no tienen el ejercicio entregados y lo que si
	noentregado = []
	entregado = []
	for i in exerstudents:
		if i.nofichfind:
			print "alumno no entregado"
			noentregado.append(i)
		else:
			print "alumno entregado"
			entregado.append(i)

	#ahora los que han entregado tengo que ordenarlos en funcion del numero de ficheros y luego del numero de errores
	#tengo que separar entre porcentaje de errores JSLint y JSHint
	esprimer = True #para ver que posicion voy mirando
	entregadodefinit = []

	print "1111111111111111111111111111111111111111111111111111111111111111111111111"
	print "1111111111111111111111111111111111111111111111111111111111111111111111111"
	print "1111111111111111111111111111111111111111111111111111111111111111111111111"
	print "1111111111111111111111111111111111111111111111111111111111111111111111111"
	print "1111111111111111111111111111111111111111111111111111111111111111111111111"
	print "1111111111111111111111111111111111111111111111111111111111111111111111111"
	
	print "Entra a percent"
	for i in entregado:
		if esprimer == False:
			pos = 0 #no se donde se coloca aun
			colocar = False
			cont = 0 #para recorrer la lista definitiva
			anadirfin = False
			while (colocar != True):
				alumncomparar = entregadodefinit[cont]
				print "ALUMNOS A COMPARAR : "
				print i.nameStudent, " vs " , alumncomparar.nameStudent
				print i.porcenterrorsfich, " vs " , alumncomparar.porcenterrorsfich
				if (int(i.porcenterrorsfich) < int(alumncomparar.porcenterrorsfich)):
					print "es mejor ", i.nameStudent
					pos = cont
					colocar = True
				elif (int(i.porcenterrorsfich) == int(alumncomparar.porcenterrorsfich)):
					if(int(i.numfichanaliz) > int(alumncomparar.numfichanaliz)): #si el porcentaje de errores es el mismo
						pos = cont							  #pero tiene mas ficheros (es mejor )
						colocar = True
						print "es mejor1 ", i.nameStudent
					else: #no es mejor
						if ((cont + 1) == len(entregadodefinit)): #anado al final
							print "anado al final1 "
							anadirfin = True
							colocar = True
						else:
							print "sigo comparando1"
							cont = cont + 1 
							colocar = False

				else:#si el porcentaje es mayor claramente es peor alumno
					if ((cont + 1) == len(entregadodefinit)): #anado al final
						print "anado al final "
						anadirfin = True
						colocar = True
					else:
						print "sigo comparando"
						cont = cont + 1 
						colocar = False

			#ANADO EN LA LISTA DEFINITIVA
			if anadirfin:
				entregadodefinit.append(i)
			else:
				entregadodefinit.insert(pos,i)
		else:
			print "es primer"
			esprimer = False
			entregadodefinit.append(i)
	
	print "222222222222222222222222222222222222222222222222222222222222222222222222222222"
	print "222222222222222222222222222222222222222222222222222222222222222222222222222222"
	print "222222222222222222222222222222222222222222222222222222222222222222222222222222"
	print "222222222222222222222222222222222222222222222222222222222222222222222222222222"
	print "222222222222222222222222222222222222222222222222222222222222222222222222222222"
	
	#busco casos especiales(los que ha dejado de comprobar errores y alomejor tienen muy pocos errores)
	#demomento solo los tengo para JSLint
	casosespeciales = []
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	for i in entregadodefinit:
		try:
			Er = Error.objects.filter(exercise = ejer).filter(typeoferror="Stopping. ('X' scanned)").filter(branch=rama).filter(tool="JSLint").filter(user=username).filter(numorden=numordernew)
			for e in Er:
				if(e.student == i.urlStudentEx):
					print "estudiante " , i.nameStudent, " es caso especial"
					casosespeciales.append(i)
		except:
			print "no errores"


	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	print "CASOS ESPECIALES"
	#quito los casos especiales de la lista definitiva
	#for i in casosespeciales:
	#	pos = 0
	#	for e in entregadodefinit:
	#		if(e.nameStudent == i.nameStudent):
	#			posdelete = pos
	#		pos = pos + 1

	#	entregadodefinit.pop(posdelete)

	#hago el ranking
	rankingtotal = "<br><br><table class='table table-striped'>"
	rankingtotal += "<thead class='thead-inverse' style='background-color:black; color: white'><tr><th>Pos</th><th>Student</th>"	
	rankingtotal += "<th>Percent errors</th><th>Num fichs</th></tr></thead><tbody>" 
  
	numrow = 1
	cont2 = 0
	primer = True

	print "A LA HORA DEL RANKING"
	for i in entregadodefinit:
		print "entra 1"
		stop = False
		if primer == False:
			print "entra primer false"
			alumprev = entregadodefinit[cont2]
			if(int(i.porcenterrorsfich) > int(alumprev.porcenterrorsfich)):
				numrow = numrow + 1
			
			if(len(casosespeciales) != 0):
				print "hay casos especiales"
				for al in casosespeciales:
					if(i.nameStudent == al.nameStudent):
						stop = True

			if(stop == True):
				rankingtotal += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i.nameStudent +" (JSLint stopped)</td>"
				rankingtotal += "<td>"+ i.porcenterrorsfich +"</td><td>"+ i.numfichanaliz +"</td></tr>"
			else:
				rankingtotal += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i.nameStudent +"</td>"
				rankingtotal += "<td>"+ i.porcenterrorsfich +"</td><td>"+ i.numfichanaliz +"</td></tr>"
			
			cont2 = cont2 + 1

		else:
			print "entra primer true"
			if(len(casosespeciales) != 0):
				print "hay casos especiales"
				for al in casosespeciales:
					if(i.nameStudent == al.nameStudent):
						stop = True

			if(stop == True):
				rankingtotal += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i.nameStudent +" (JSLint stopped)</td>"
				rankingtotal += "<td>"+ i.porcenterrorsfich +"</td><td>"+ i.numfichanaliz +"</td></tr>"
			else:
				rankingtotal += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i.nameStudent +"</td>"
				rankingtotal += "<td>"+ i.porcenterrorsfich +"</td><td>"+ i.numfichanaliz +"</td></tr>"
			
			primer = False
	
	rankingtotal += "</tbody></table>"
	
	print "antes de no entregado"
	if(len(noentregado) != 0):
		print "entra a no entregado"
		rankingtotal += "<table class='table table-striped'><thead class='thead-default' style='background-color: #F08080;'><tr>"
		rankingtotal += "<th>Undelivered</th><th>Student</th></tr></thead><tbody>"

		for i in noentregado:
			numrow = numrow + 1
			rankingtotal += "<tr><th scope='row'>"+str(numrow)+"</th><td>" + i.nameStudent +"</td></tr>"
		
		rankingtotal += "</tbody></table>"

	print "antes de return de ranking"
	return rankingtotal

def resumenGeneralTeacher(ejer,rama,username,numordernew):
	#puede que esto solo tenga que hacerlo una sola vez porque ahora analizo todos de golpe
	print "--------------ANTES DE RESUMEN GENERAL DEL REPOSITORIO PROFESOR --------------"
	erroresJSLint = Error.objects.filter(exercise=ejer).filter(branch=rama).filter(user=username).filter(tool="JSLint").filter(numorden=numordernew).order_by("numtypeoferror") #filtro por el nombre del repositorio(url del estudiante)
	erroresJSHint = Error.objects.filter(exercise=ejer).filter(branch=rama).filter(user=username).filter(tool="JSHint").filter(numorden=numordernew).order_by("numtypeoferror") #filtro por el nombre del repositorio(url del estudiante)

	resumen = ""

	if((len(erroresJSLint) != 0) or (len(erroresJSHint) != 0)):
		if(((len(erroresJSLint) == 1) and (len(erroresJSHint) == 0)) or
			((len(erroresJSLint) == 0) and (len(erroresJSHint) == 1))):
			resumen= "<p class='sumary'>1 error</p><p>"
		else:
			sumerrors = len(erroresJSLint) + len(erroresJSHint)
			resumen= "<p class='sumary'>"+ str(sumerrors) +" errors</p><ol>"
	cont = 1
	numerrores = 0
	trueerror = False

	if(len(erroresJSLint) != 0):
		while (cont < 84): #hacer el resumen global actualizar el 84 si pongo mas errores
			for e in erroresJSLint:
				if(e.numtypeoferror == cont):
					numerrores = numerrores + 1
					print "hay error general PROFESOR JSLint del tipo " , e.typeoferror
					trueerror = True
					errortype = e.typeoferror
			if(trueerror):
				if(numerrores == 1):
					resumen += "<li><strong>" + errortype + " :</strong> " + str(numerrores) +" error</li>"
				else:
					resumen += "<li><strong>" + errortype + " :</strong> " + str(numerrores) +" errors</li>"
			cont = cont + 1
			numerrores = 0
			trueerror = False	

	cont = 1
	numerrores = 0
	trueerror = False

	if(len(erroresJSHint) != 0):
		while (cont < 28): #hacer el resumen global actualizar el 28 si pongo mas errores
			for e in erroresJSHint:
				if(e.numtypeoferror == cont):
					numerrores = numerrores + 1
					print "hay error general PROFESOR JSHint del tipo " , e.typeoferror
					trueerror = True
					errortype = e.typeoferror
			if(trueerror):
				if(numerrores == 1):
					resumen += "<li><strong>" + errortype + " :</strong> " + str(numerrores) +" error</li>"
				else:
					resumen += "<li><strong>" + errortype + " :</strong> " + str(numerrores) +" errors</li>"
			cont = cont + 1
			numerrores = 0
			trueerror = False
	
	resumen += "</ol>"
	print "--------------DESPUES DE RESUMEN GENERAL DEL REPOSITORIO PROFESOR --------------"

	return resumen

def rankerror(ejer,rama,username,rol,numordernew):
	print "entro en rankerror"
	#########guardar los errores y el numero que hay
	if(rol == "teacher"):
		erroresJSLint = Error.objects.filter(exercise=ejer).filter(branch=rama).filter(user=username).filter(tool="JSLint").filter(numorden=numordernew).order_by("numtypeoferror") #filt
		erroresJSHint = Error.objects.filter(exercise=ejer).filter(branch=rama).filter(user=username).filter(tool="JSHint").filter(numorden=numordernew).order_by("numtypeoferror") #filt
	else:
		erroresJSLint = Error.objects.filter(student=ejer).filter(branch=rama).filter(user=username).filter(tool="JSLint").filter(numorden=numordernew).order_by("numtypeoferror") #filt
		erroresJSHint = Error.objects.filter(student=ejer).filter(branch=rama).filter(user=username).filter(tool="JSHint").filter(numorden=numordernew).order_by("numtypeoferror") #filt
	
	print "len(erroresJSLint) = ", len(erroresJSLint)
	print "len(erroresJSHint) = ", len(erroresJSHint)
	cont = 1
	numerrores = 0
	trueerror = False
	data = ""
	if(len(erroresJSLint) != 0):
		print "RANKERROR JSLINT"
		while (cont < 84): #actualizar el 84 si pongo mas errores
			for e in erroresJSLint:
				if(e.numtypeoferror == cont):
					numerrores = numerrores + 1
					trueerror = True
					errortype = e.typeoferror
			if(trueerror):
					data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

			cont = cont + 1
			numerrores = 0
			trueerror = False
	
	cont = 1
	numerrores = 0
	trueerror = False

	if(len(erroresJSHint) != 0):
		data += "JSHinterrorspace0errorspace"
		print "RANKERROR JSHINT"
		while (cont < 28): #actualizar el 28 si pongo mas errores
			for e in erroresJSHint:
				if(e.numtypeoferror == cont):
					numerrores = numerrores + 1
					trueerror = True
					errortype = e.typeoferror
			if(trueerror):
					data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

			cont = cont + 1
			numerrores = 0
			trueerror = False

	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"
	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"
	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"
	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"
	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"

	print "antes de errorsplit1"
	errorsplit = data.split("errorspace")
	print "despues de errorsplit1"
	#creo un array de errores para comparar luego
	salir = False
	arrayoferrors = []
	conterrors = 0
	print "antes de len(erroresplit) = ", len(errorsplit)
	if(len(errorsplit) > 1):
		print "len errorsplit es distinto de 0"
		while salir != True:
			if(errorsplit[conterrors] != "JSHint"):
				error = [errorsplit[conterrors],errorsplit[conterrors + 1]]
				arrayoferrors.append(error)
				conterrors = conterrors + 2
				print "conterrors = ", conterrors
				print "len(errorsplit) = ", len(errorsplit)
				if(conterrors == len(errorsplit) - 1):
					print "entro a poner salir a true"
					salir = True
			else:
				conterrors = conterrors + 2

		#ordeno los errores de mayor a menor ( y no se si hacerlo tmbn de menor a mayor)
		arrayoferrorsdefinit = []
		print "paso a ordenar de mayor a menor los errores"
		for i in arrayoferrors:
			#print "er: ",i[0]
			coloca = False
			if(len(arrayoferrorsdefinit) == 0):
				arrayoferrorsdefinit.append(i)

			else:
				contcoloca = 0
				poscoloca = 0
				anadiralfinal = False
				while coloca != True:
					errorcomparar = arrayoferrorsdefinit[contcoloca]
					if(int(i[1]) > int(errorcomparar[1])):
						poscoloca = contcoloca
						coloca = True
					else:
						if(len(arrayoferrorsdefinit) - 1 == contcoloca): #es el ultimo asique anado
							anadiralfinal = True
							coloca = True
						else:
							contcoloca = contcoloca + 1
				
				if(anadiralfinal):
					arrayoferrorsdefinit.append(i)
				else:
					arrayoferrorsdefinit.insert(poscoloca,i)



		rankingerrors = "<br><br><table class='table table-striped'>"
		rankingerrors += "<thead class='thead-inverse' style='background-color:black; color: white'><tr><th>Pos</th><th>Error</th>"	
		rankingerrors += "<th>Num errors</th></tr></thead><tbody>" 
	  
		numrow = 1
		cont3 = 0
		primer = True
		if(len(arrayoferrorsdefinit) != 0):
			for i in arrayoferrorsdefinit:
				if primer == False:
					errorprev = arrayoferrorsdefinit[cont3]
					if(int(i[1]) < int(errorprev[1])):
						numrow = numrow + 1
						
					rankingerrors += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i[0] +"</td>"
					rankingerrors += "<td>"+ i[1] +"</td></tr>"	
					cont3 = cont3 + 1	

				else:
					rankingerrors += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ i[0] +"</td>"
					rankingerrors += "<td>"+ i[1] +"</td></tr>"
					primer = False

		rankingerrors += "</tbody></table>"
	else:
		rankingerrors = ""
		print "no hay errores en rankingerrores"

	return rankingerrors, data

def resumenes(ejer,rama,username,numordernew):
	print "entra a resumenes"
	#primero hago los resumenes del ejercicio JSLint
	rankpercent = rankpercenterrors(ejer,rama,username,numordernew) #ranking porcentaje de errores JSLint y JSHint
	ranknumfich = ranknumficheros(ejer,rama,username,numordernew) #ranking numero ficheros JSLint y JSHint
	generalTeacher = resumenGeneralTeacher(ejer,rama,username,numordernew) #resumen general profesor
	rankerrors ,data = rankerror(ejer,rama,username,"teacher",numordernew) #ranking errores y data JSLint y JSHint conjunto
	print "antes de posexerteacher"
	reposexerteacher = StudentExercise.objects.filter(urlTeacherEx = ejer).filter(branch=rama).filter(user=username).filter(numorden=numordernew)
	numerrorestotal = 0
	for i in reposexerteacher:
		numerrorestotal = numerrorestotal + int(i.numoferrors)

	print "antes de exerteacher"
	exerteacher = TeacherExercise.objects.get(urlTeacherEx = ejer,branch=rama,user=username,numorden=numordernew)
	exerteacher.rankingpercent = rankpercent
	exerteacher.rankingfich = ranknumfich
	exerteacher.rankingerrors = rankerrors
	exerteacher.sumary = generalTeacher
	exerteacher.data = data
	exerteacher.numoferrors = str(numerrorestotal)
	exerteacher.save()

def deleteUser(username,rol):
	print "entro a deleteUser"
	if(rol == "teacher"):
		print "entro por teacher"
		repoteachers = TeacherExercise.objects.filter(user=username)
		for i in repoteachers:
			i.delete()
		repoalumnos = StudentExercise.objects.filter(user=username)
		for i in repoalumnos:
			i.delete()
		ficheros = FichJs.objects.filter(user=username)
		for i in ficheros:
			i.delete()
		errores = Error.objects.filter(user=username)
		for i in errores:
			i.delete()
		libraries = Library.objects.filter(user=username)
		for i in libraries:
			i.delete()
	else:
		print "entro por student"
		repoalumnos = StudentExercise.objects.filter(user=username)
		for i in repoalumnos:
			i.delete()
		ficheros = FichJs.objects.filter(user=username)
		for i in ficheros:
			i.delete()
		errores = Error.objects.filter(user=username)
		for i in errores:
			i.delete()
		libraries = Library.objects.filter(user=username)
		for i in libraries:
			i.delete()

def deleteData(repo,rama,username,numordernew):
	try:
		TeacherExercise.objects.get(urlTeacherEx = repo,branch=rama,user=username,numorden=numordernew).delete()
		repoalumnos = StudentExercise.objects.filter(urlTeacherEx = repo).filter(branch=rama).filter(user=username).filter(numorden=numordernew)
		for i in repoalumnos:
			i.delete()
		ficheros = FichJs.objects.filter(exercise=repo).filter(branch=rama).filter(user=username).filter(numorden=numordernew)
		for i in ficheros:
			i.delete()
		errores = Error.objects.filter(exercise=repo).filter(branch=rama).filter(user=username).filter(numorden=numordernew)
		for i in errores:
			i.delete()
	except:
		print "entra a borrar por el except"
		StudentExercise.objects.get(urlStudentEx=repo,branch=rama,user=username,numorden=numordernew).delete()
		ficheros = FichJs.objects.filter(urlstudent=repo).filter(branch=rama).filter(user=username).filter(numorden=numordernew)
		for i in ficheros:
			i.delete()
		errores = Error.objects.filter(student=repo).filter(branch=rama).filter(user=username).filter(numorden=numordernew)
		for i in errores:
			i.delete()
		print "sale de borrar por el except"

def saveLibrary(nameLibrary,username):
	print "entra a salvar ", nameLibrary
	LibraryToSave = Library(name = nameLibrary,user=username)
	print "entra a 1 "
	LibraryToSave.save()
	print "entra a 2 "

def globalSumaryErrors(usuario,rol): #hago ordenar los 5 errores mas comunes y el data de la evolucion del usuario
	print "entro a global sumary"
	erroresJSLint = Error.objects.filter(user=usuario).filter(tool="JSLint")
	erroresJSHint = Error.objects.filter(user=usuario).filter(tool="JSHint")

	
	print "len(erroresJSLint) = ", len(erroresJSLint)
	print "len(erroresJSHint) = ", len(erroresJSHint)

	cont = 1
	numerrores = 0
	trueerror = False
	data = ""
	if(len(erroresJSLint) != 0):
		print "RANKERROR JSLINT"
		while (cont < 84): #actualizar el 84 si pongo mas errores
			for e in erroresJSLint:
				if(e.numtypeoferror == cont):
					numerrores = numerrores + 1
					trueerror = True
					errortype = e.typeoferror
			if(trueerror):
					print "anado a data JSLINT = ", errortype
					data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

			cont = cont + 1
			numerrores = 0
			trueerror = False
	
	cont = 1
	numerrores = 0
	trueerror = False

	if(len(erroresJSHint) != 0):
		data += "JSHinterrorspace0errorspace"
		print "RANKERROR JSHINT"
		while (cont < 28): #actualizar el 28 si pongo mas errores
			for e in erroresJSHint:
				if(e.numtypeoferror == cont):
					numerrores = numerrores + 1
					trueerror = True
					errortype = e.typeoferror
			if(trueerror):
					print "anado a data JSHINT = ", errortype
					data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

			cont = cont + 1
			numerrores = 0
			trueerror = False

	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"
	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"
	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"
	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"
	print "555555555555555555555555555555555555555555555555555555555555555555555555555555"

	errorsplit = data.split("errorspace")
	#creo un array de errores para comparar luego
	salir = False
	arrayoferrors = []
	conterrors = 0
	rankingerrors = ""
	print "len(errorsplit) = ", len(errorsplit)
	if(len(errorsplit) > 1):

		while salir != True:
			if(errorsplit[conterrors] != "JSHint"):
				error = [errorsplit[conterrors],errorsplit[conterrors + 1]]
				print "anado a arrayoferrors -> ",error[0]
				arrayoferrors.append(error)
				conterrors = conterrors + 2
				print "conterrors = ", conterrors
				print "len(errorsplit) = ", len(errorsplit)
				if(conterrors == len(errorsplit) - 1):
					print "entro a poner salir a true"
					salir = True
			else:
				conterrors = conterrors + 2

		#ordeno los errores de mayor a menor ( y no se si hacerlo tmbn de menor a mayor)
		arrayoferrorsdefinit = []
		print "paso a ordenar de mayor a menor los errores"
		for i in arrayoferrors:
			coloca = False
			print "error: ", i[0]
			if(len(arrayoferrorsdefinit) == 0):
				arrayoferrorsdefinit.append(i)

			else:
				contcoloca = 0
				poscoloca = 0
				anadiralfinal = False
				while coloca != True:
					errorcomparar = arrayoferrorsdefinit[contcoloca]
					if(int(i[1]) > int(errorcomparar[1])):
						poscoloca = contcoloca
						coloca = True
					else:
						if(len(arrayoferrorsdefinit) - 1 == contcoloca): #es el ultimo asique anado
							anadiralfinal = True
							coloca = True
						else:
							contcoloca = contcoloca + 1
				
				if(anadiralfinal):
					arrayoferrorsdefinit.append(i)
				else:
					arrayoferrorsdefinit.insert(poscoloca,i)

		rankingerrors = "<table class='table table-striped'>"
		rankingerrors += "<thead class='thead-inverse' style='background-color:black; color: white'><tr><th>Pos</th><th>Error</th>"	
		rankingerrors += "<th>Num errors</th></tr></thead><tbody>" 
	  
		numrow = 1
		cont3 = 0
		primer = True

		salir = False
		i = 0
		while(salir != True):
			if primer == False:
				errorprev = arrayoferrorsdefinit[cont3]
				if(int(arrayoferrorsdefinit[i][1]) < int(errorprev[1])):
					numrow = numrow + 1
					
				print "anado el error ",arrayoferrorsdefinit[i][0], " en la pos ", str(numrow)
				rankingerrors += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ arrayoferrorsdefinit[i][0] +"</td>"
				rankingerrors += "<td>"+ arrayoferrorsdefinit[i][1] +"</td></tr>"	
				cont3 = cont3 + 1	

			else:
				print "anado el error ",arrayoferrorsdefinit[i][0], " en la pos ", str(numrow)
				rankingerrors += "<tr><th scope='row'>"+str(numrow)+"</th><td>"+ arrayoferrorsdefinit[i][0] +"</td>"
				rankingerrors += "<td>"+ arrayoferrorsdefinit[i][1] +"</td></tr>"
				primer = False

			i = i+1
			print "i = ", i
			if(i==5):
				salir = True

		rankingerrors += "</tbody></table>"

		###########################ahora hago los datos para la grafica
		data = ""
		if(rol == "teacher"):
			print "rol profesor global"
			ejercicios = TeacherExercise.objects.filter(user=usuario)
			for i in ejercicios:
				name = i.urlTeacherEx.split("/")[4]+ "("+ i.branch + ")("+str(i.numorden)+")"
				numerrores = i.numoferrors
				data +=  name + "errorspace" + numerrores + "errorspace" 
				print "exer = ", name, ", numerrores = ", numerrores
		else:
			print "rol estudiante global"
			ejercicios = StudentExercise.objects.filter(user=usuario)
			for i in ejercicios:
				name = i.urlStudentEx.split("/")[4] + "("+ i.branch + ")("+str(i.numorden)+")"
				numerrores = i.numoferrors
				data +=  name + "errorspace" + numerrores + "errorspace" 
				print "exer = ", name, ", numerrores = ", numerrores


	print "salgo de global sumary"
	return rankingerrors,data

def compararerrors(ejer,rama,usuario,numordernew):
	useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
	print "usuario activo compararerrors = ", useractive.username
	dataerrorcomparar = ""
	if(useractive.first_name == "teacher"):
		#primero veo si hay ultimo ejercicio de un usuario (porque puede ser el primero)
		try:
			lastexer = TeacherExercise.objects.get(user=usuario,islast=True)
			#si hay ultimo ejercicio lo que tengo que hacer es coger los errores de uno y de otro y compararlos
			lasterroresJSLint = Error.objects.filter(exercise=lastexer.urlTeacherEx,branch=lastexer.branch,tool="JSLint",user=usuario,numorden=lastexer.numorden)
			lasterroresJSHint = Error.objects.filter(exercise=lastexer.urlTeacherEx,branch=lastexer.branch,tool="JSHint",user=usuario,numorden=lastexer.numorden)
			errorscompararJSLint = Error.objects.filter(exercise=ejer,branch=rama,tool="JSLint",user=usuario,numorden=numordernew)
			errorscompararJSHint = Error.objects.filter(exercise=ejer,branch=rama,tool="JSHint",user=usuario,numorden=numordernew)
			gocomparar = True
			#por ultimo tendre que actualizar el lastexer
		except: 
			#solo entrara la primera vez, pongo a ultimo ejercicio al ultimo ejercicio
			print "no hay ultimo ejercio1" 
			lastexer = TeacherExercise.objects.get(urlTeacherEx=ejer,branch=rama,user=usuario,numorden=numordernew)
			lastexer.islast = True
			gocomparar = False
	else:
		#primero veo si hay ultimo(porque puede ser el primero)
		try:
			lastexer = StudentExercise.objects.get(user=usuario,islast=True)
			lasterroresJSLint = Error.objects.filter(student=lastexer.urlStudentEx,branch=lastexer.branch,tool="JSLint",user=usuario,numorden=lastexer.numorden)
			lasterroresJSHint = Error.objects.filter(student=lastexer.urlStudentEx,branch=lastexer.branch,tool="JSHint",user=usuario,numorden=lastexer.numorden)
			errorscompararJSLint = Error.objects.filter(student=ejer,branch=rama,tool="JSLint",user=usuario,numorden=numordernew)
			errorscompararJSHint = Error.objects.filter(student=ejer,branch=rama,tool="JSHint",user=usuario,numorden=numordernew)
			gocomparar = True
		except: 
			#solo entrara la primera vez, pongo a ultimo ejercicio al ultimo ejercicio
			print "no hay ultimo ejercio2" 
			lastexer = StudentExercise.objects.get(urlStudentEx=ejer,branch=rama,user=usuario,numorden=numordernew)
			lastexer.islast = True
			gocomparar = False

	if(gocomparar == True):

		arraylasterrors = []

		cont = 1
		numerrores = 0
		trueerror = False
		data = ""
		if(len(lasterroresJSLint) != 0):
			print "RANKERROR JSLINT"
			while (cont < 84): #actualizar el 84 si pongo mas errores
				for e in lasterroresJSLint:
					if(e.numtypeoferror == cont):
						numerrores = numerrores + 1
						trueerror = True
						errortype = e.typeoferror
				if(trueerror):
						print "anado a last data JSLINT = ", errortype, "con ", numerrores, " errores"
						data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

				cont = cont + 1
				numerrores = 0
				trueerror = False
		
		cont = 1
		numerrores = 0
		trueerror = False

		if(len(lasterroresJSHint) != 0):
			data += "JSHinterrorspace0errorspace"
			print "RANKERROR JSHINT"
			while (cont < 28): #actualizar el 28 si pongo mas errores
				for e in lasterroresJSHint:
					if(e.numtypeoferror == cont):
						numerrores = numerrores + 1
						trueerror = True
						errortype = e.typeoferror
				if(trueerror):
						print "anado a last data JSHINT = ", errortype, "con ", numerrores, " errores"
						data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

				cont = cont + 1
				numerrores = 0
				trueerror = False

		if(data != ""): #Es porque hay errores
			errorsplit = data.split("errorspace")
			#creo un array de errores para comparar luego
			salir = False
			conterrors = 0
			while salir != True:
				if(errorsplit[conterrors] != "JSHint"):
					error = [errorsplit[conterrors],errorsplit[conterrors + 1]]
					print "anado a arraylasterrors -> ",error[0], "con ", error[1], " errores"
					arraylasterrors.append(error)
					conterrors = conterrors + 2
					print "conterrors = ", conterrors
					print "len(errorsplit) = ", len(errorsplit)
					if(conterrors == len(errorsplit) - 1):
						print "entro a poner salir a true"
						salir = True
				else:
					conterrors = conterrors + 2

		arrayerrorscompar = []

		cont = 1
		numerrores = 0
		trueerror = False
		data = ""
		print "len(errorscompararJSLint) = ", len(errorscompararJSLint)
		if(len(errorscompararJSLint) != 0):
			print "RANKERROR JSLINT"
			while (cont < 84): #actualizar el 84 si pongo mas errores
				for e in errorscompararJSLint:
					if(e.numtypeoferror == cont):
						numerrores = numerrores + 1
						trueerror = True
						errortype = e.typeoferror
				if(trueerror):
						print "anado a comparar data JSLINT = ", errortype
						data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

				cont = cont + 1
				numerrores = 0
				trueerror = False
		
		cont = 1
		numerrores = 0
		trueerror = False

		print "len(errorscompararJSHint) = ", len(errorscompararJSHint)
		if(len(errorscompararJSHint) != 0):
			data += "JSHinterrorspace0errorspace"
			print "RANKERROR JSHINT"
			while (cont < 28): #actualizar el 28 si pongo mas errores
				for e in errorscompararJSHint:
					if(e.numtypeoferror == cont):
						numerrores = numerrores + 1
						trueerror = True
						errortype = e.typeoferror
				if(trueerror):
						print "anado a comparar data JSHINT = ", errortype
						data +=  errortype + "errorspace" + str(numerrores) + "errorspace" 

				cont = cont + 1
				numerrores = 0
				trueerror = False

		if(data != ""): #Es porque hay errores
			errorsplit = data.split("errorspace")
			#creo un array de errores para comparar luego
			salir = False
			conterrors = 0
			while salir != True:
				if(errorsplit[conterrors] != "JSHint"):
					error = [errorsplit[conterrors],errorsplit[conterrors + 1]]
					print "anado a comparar arrayerrorscompar -> ",error[0], "con ", error[1], " errores"
					arrayerrorscompar.append(error)
					conterrors = conterrors + 2
					print "conterrors = ", conterrors
					print "len(errorsplit) = ", len(errorsplit)
					if(conterrors == len(errorsplit) - 1):
						print "entro a poner salir a true"
						salir = True
				else:
					conterrors = conterrors + 2

		##ya tengo los arrays de errores a comparar, cada error tiene [name,numerrores]

		#ahora comparo los errores
		arraydefinit = []
		if(len(arraylasterrors) == 0 and len(arrayerrorscompar) != 0): 
			#si en el ultimo analisis no habia errores y en el actual si
			print "entra a comparar por 1"
			arraydefinit = arrayerrorscompar
		elif(len(arraylasterrors) != 0 and len(arrayerrorscompar) == 0):
			#si en el ultimo analisis habia errores, y en el actual no
			print "entra a comparar por 2"
			for i in arraylasterrors:
				error = [i[0],"-"+i[1]]
				arraydefinit.append(error)
		elif(len(arraylasterrors) == 0 and len(arrayerrorscompar) == 0):
			#si en el ultimo analisis no habia errores y en el actual tampoco
			print "entra a comparar por 3"
			arraydefinit = []
		else:
			print "entra a comparar por 4"
			for i in arraylasterrors: #primero comparo todos los que habia antes y luego veo si hay alguno nuevo
				nameError = i[0]
				print "Error a comparar = ", nameError
				#lo busco en el otro array a ver si esta
				estaError = False
				numerroresprev = 0
				for e in arrayerrorscompar:
					if(e[0] == nameError): #si esta calculo la diferencia de errores
						estaError = True
						numerrores = int(e[1])

				if(estaError == True):
					print "comparo con los que he cometido ahora"
					print "antes = ", i[1]
					print "ahora = ", numerrores
					difError = numerrores - int(i[1])
				else:
					print "ahora no lo he cometido, pues es el numero en negativo"
					difError = -int(i[1])

				print "diferencia de errores = ",difError
				error = [i[0],str(difError)]
				arraydefinit.append(error)

			print "miro a ver si hay errores que antes no habia cometido"
			for i in arrayerrorscompar: #miro si hay alguno que antes no habia para ello ahora busco en el arraydefinit
				nameError = i[0]
				estaError = False
				print "Error a comparar = ", nameError
				for e in arraydefinit:
					if(e[0] == nameError): #si esta no tengo que volver a anadirlo
						print "ya lo habia cometido el error"
						estaError = True
				
				if(estaError == False): #si el error no estaba lo anado
					print "no estaba cometido antes, lo anado"
					arraydefinit.append(i)

		if(len(arraydefinit) != 0):
			for i in arraydefinit:
				dataerrorcomparar += i[0] + "errorspace" + i[1] + "errorspace"
				print "error = ", i[0], ", numerrores = ", i[1]
	
	return dataerrorcomparar		

@csrf_exempt
def index(request):
	if request.method == "GET":
	    #print "template = " + str(template)
	    print "hola"
	    print "estoy en get"
	    #listaexerteacher = TeacherExercise.objects.all() 
	    #listafiles = Library.objects.all()
	    return render(request,'checkexercises/index.html',{'logearse': True})
	    #return render(request,'checkexercises/index.html',{'listexercisesteach': listaexerteacher,
	    #					'listLibraries': listafiles})

	    	
	elif request.method == "POST":
		print "estoy en post"
		#comprobar si ese repositorio esta analizado
		if request.POST.get('urlanalizall'):#no se si hacer solo if en vez de elif
			useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
			print "usuario activo urlanaliz = ", useractive.username
			if(useractive.first_name == "teacher"):
				isteacher = True
				isstudent = False
			else:
				isteacher = False
				isstudent = True
			#print "urlteacher = " + request.POST.get('urlanalizall')
			#try: #si no esta analizado viene con listForks
			#    print "listforks = " + request.POST.get('listForks')
			    #arrayforks = request.POST.get('listForks')
			#except: #si ya esta analizado el post viene sin listForks
			#	print "no listForks"
			
			is_teacher = TeacherExercise.objects.filter(urlTeacherEx=request.POST.get('urlanalizall')).filter(branch=request.POST.get('rama')).filter(user= useractive.username)
			
			if(len(is_teacher) != 0):
				print "This teacher just exist"
				numordenprev = is_teacher[len(is_teacher)-1].numorden
				print "ultimo numorden = ", numordenprev
				numordernew = numordenprev + 1
			
			else:
				print "Does not exist this teacher"
				numordernew = 1
			
			teacher = TeacherExercise(urlTeacherEx = request.POST.get('urlanalizall'),
										  branch=request.POST.get('rama'),
										  user= useractive.username,
										  numorden = numordernew)
			teacher.save()
			print "guardo al profesor"		
			
			try:
				#ahora ya lo siguiente es comun tanto si existia como si no
				listforksplit = request.POST.get('listForks').split(",")
				es_url_avatar = False #par es url de repo, impar es de avatar
				listforks = []
				listurlavatar = []
				for i in listforksplit:
					if es_url_avatar:   
						listurlavatar.append(i)
						es_url_avatar = False
					else:
						listforks.append(i)
						es_url_avatar = True

				contportfolio = 1
				contavatar = 0
				for i in listforks:
					name = i.split("/")[3]
					print "name = ", name
					#estudiante = Student(name=name,
					#					 errors="0")
					#estudiante.save()
					student = StudentExercise(urlTeacherEx = request.POST.get('urlanalizall'),
											  urlStudentEx = i,
											  nameStudent = name,
											  urlAvatar = listurlavatar[contavatar],
											  numportfolio = contportfolio,
											  numfichanaliz = "0",
											  branch=request.POST.get('rama'),
											  user= useractive.username,
											  numorden= numordernew)
					student.save()
					print "save student " + i
					contportfolio = contportfolio + 1
					contavatar = contavatar + 1
			
				repoalumnos = StudentExercise.objects.filter(urlTeacherEx = request.POST.get('urlanalizall')).filter(branch=request.POST.get('rama')).filter(user=useractive.username).filter(numorden=numordernew)
				try:
					for repo in repoalumnos:
						analiz_repo(repo.urlStudentEx,request.POST.get('urlanalizall'),
										request.POST.get('rama'),useractive.username,numordernew)
					
					resumenes(request.POST.get('urlanalizall'),request.POST.get('rama'),useractive.username,numordernew)
					erroresglobales,dataglobal = globalSumaryErrors(useractive.username,useractive.first_name)
					usuario = Usuario.objects.get(user= useractive.username)
					if(erroresglobales == ""):
						print "no habia errores globales"
						if(usuario.rankingerrors != ""):
							print "si habia ranking errores globales"
							erroresglobales = usuario.rankingerrors
							name1 = request.POST.get('urlanalizall').split("/")[4]+ "("+ request.POST.get('rama') + ")("+str(numordernew)+")"
							dataglobal = usuario.data + name1 + "errorspace0errorspace"
						else:
							print "no habia ranking globales"
							erroresglobales = "NO ERRORS"
							name1 = request.POST.get('urlanalizall').split("/")[4]+ "("+ request.POST.get('rama') + ")("+ str(numordernew)+")"
							dataglobal = name1 + "errorspace0errorspace"
					usuario.rankingerrors = erroresglobales
					usuario.data = dataglobal
					usuario.save()
					dataerrorcomparar = compararerrors(request.POST.get('urlanalizall'),request.POST.get('rama'),useractive.username,numordernew)
					try:
						lastexer = TeacherExercise.objects.get(user=useractive.username,islast=True)
						lastexer.islast = False
						lastexer.save()
					except:
						print "no hay ultimo ejercicio profesor"
					
					teacher = TeacherExercise.objects.get(urlTeacherEx = request.POST.get('urlanalizall'),branch=request.POST.get('rama'),user=useractive.username,numorden=numordernew)
					teacher.datacomparar = dataerrorcomparar
					teacher.islast = True
					teacher.save()
					#aqui hacer lo de comparar y luego analizar al ultimo o eso incluso lo puedo hacer en la misma funcion
				except:
					print "fallo al analizar, borro los datos de este repo"
					listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
					listafiles = Library.objects.filter(user=useractive.username)
					deleteData(request.POST.get('urlanalizall'),request.POST.get('rama'),useractive.username,numordernew) #ver si funciona cuando falla la descarga del repo
					return render(request, 'checkexercises/index.html', {'listexercisesteach': listaexerteacher,
									'listLibraries': listafiles,'failanalize': "fallo al analizar",
									'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher})
				#LOS COJO DE NUEVO ANALIZADOS
				teacher = TeacherExercise.objects.get(urlTeacherEx = request.POST.get('urlanalizall'),branch=request.POST.get('rama'),user=useractive.username,numorden=numordernew)
				repoalumnos = StudentExercise.objects.filter(urlTeacherEx = request.POST.get('urlanalizall')).filter(branch=request.POST.get('rama')).filter(user=useractive.username).filter(numorden=numordernew)
				ficheros = FichJs.objects.filter(exercise=request.POST.get('urlanalizall')).filter(branch=request.POST.get('rama')).filter(user=useractive.username).filter(numorden=numordernew)
				listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
				listafiles = Library.objects.filter(user=useractive.username)
				print "len(repoalumnos) == ", len(repoalumnos)
				nomostrar = False
				if(len(repoalumnos) == 0):
					repoalumnos = "r"
					nomostrar = True
				#if (teacher.porcentaje != "0"):
				#	return render(request, 'checkexercises/index.html', {'repos': repositorios ,
				#				 'urlteach': teacher.urlTeacherEx, 'porcenteach': teacher.porcentaje,
				#				 'sumaryteach': teacher.sumary})
				#else:
				#	return render(request, 'checkexercises/index.html', {'repos': repositorios ,
				#				 'urlteach': teacher.urlTeacherEx})
				return render(request, 'checkexercises/index.html', {'repos': repoalumnos ,
								 'urlteach': teacher.urlTeacherEx,'sumaryteach': teacher.sumary,
								 'fichs': ficheros ,'ranktotal': teacher.rankingpercent,'rankfich': teacher.rankingfich,
								  'listexercisesteach': listaexerteacher,'infoerrores': teacher.data,
								   'rankerrors': teacher.rankingerrors,'rama': request.POST.get('rama'),
								    'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,
								    'is_student': isstudent,'is_teacher': isteacher,'numord': numordernew,
								    'errorescomparar': teacher.datacomparar,'nomostrar': nomostrar})
			except:
				print "no forks"
				#LOS COJO DE NUEVO ANALIZADOS
				try:					
					resumenes(request.POST.get('urlanalizall'),request.POST.get('rama'),useractive.username,numordernew)
					erroresglobales,dataglobal = globalSumaryErrors(useractive.username,useractive.first_name)
					usuario = Usuario.objects.get(user= useractive.username)
					if(erroresglobales == ""):
						print "no habia errores globales"
						if(usuario.rankingerrors != ""):
							print "si habia ranking errores globales"
							erroresglobales = usuario.rankingerrors
							name1 = request.POST.get('urlanalizall').split("/")[4]+ "("+ request.POST.get('rama') + ")("+str(numordernew)+")"
							dataglobal = usuario.data + name1 + "errorspace0errorspace"
						else:
							print "no habia ranking globales"
							erroresglobales = "NO ERRORS"
							name1 = request.POST.get('urlanalizall').split("/")[4]+ "("+ request.POST.get('rama') + ")("+ str(numordernew)+")"
							dataglobal = name1 + "errorspace0errorspace"
					usuario.rankingerrors = erroresglobales
					usuario.data = dataglobal
					usuario.save()
					dataerrorcomparar = compararerrors(request.POST.get('urlanalizall'),request.POST.get('rama'),useractive.username,numordernew)
					try:
						lastexer = TeacherExercise.objects.get(user=useractive.username,islast=True)
						lastexer.islast = False
						lastexer.save()
					except:
						print "no hay ultimo ejercicio profesor"
					
					teacher = TeacherExercise.objects.get(urlTeacherEx = request.POST.get('urlanalizall'),branch=request.POST.get('rama'),user=useractive.username,numorden=numordernew)
					teacher.datacomparar = dataerrorcomparar
					teacher.islast = True
					teacher.save()
				except:
					print "fallo en resumenes de no forks"
				teacher = TeacherExercise.objects.get(urlTeacherEx = request.POST.get('urlanalizall'),branch=request.POST.get('rama'),user=useractive.username,numorden=numordernew)
				repoalumnos = "repos"
				nomostrar = True
				ficheros = FichJs.objects.filter(exercise=request.POST.get('urlanalizall')).filter(branch=request.POST.get('rama')).filter(user=useractive.username).filter(numorden=numordernew)
				listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
				listafiles = Library.objects.filter(user=useractive.username)

				return render(request, 'checkexercises/index.html', {'repos': repoalumnos ,
								 'urlteach': teacher.urlTeacherEx,'sumaryteach': teacher.sumary,
								 'fichs': ficheros ,'ranktotal': teacher.rankingpercent,'rankfich': teacher.rankingfich,
								  'listexercisesteach': listaexerteacher,'infoerrores': teacher.data,
								   'rankerrors': teacher.rankingerrors,'rama': request.POST.get('rama'),
								    'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,
								    'is_student': isstudent,'is_teacher': isteacher,'numord': numordernew,
								    'errorescomparar': teacher.datacomparar,'nomostrar': nomostrar})
		
		elif request.POST.get('repodelete'):
			print "dentro del borrar en el views post"
			useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
			print "usuario activo repodelete = ", useractive.username
			if(useractive.first_name == "teacher"):
				isteacher = True
				isstudent = False
			else:
				isteacher = False
				isstudent = True
			try: #anadir la rama al get , intentar buscar el repo como profesor o como alumno
				is_teacher = TeacherExercise.objects.get(urlTeacherEx=request.POST.get('repodelete'),
														 branch=request.POST.get('rama'),
														 user=useractive.username)
				print "This teacher just exist"
				deleteData(request.POST.get('repodelete'),request.POST.get('rama'),useractive.username)
				print "despues de borrar"
				message = "REPOSITORY WAS DELETED"
				listafiles = Library.objects.filter(user=useractive.username)
				try:
					listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
					return render(request, 'checkexercises/index.html', {'Message1': message,
								'listexercisesteach': listaexerteacher,'listLibraries': listafiles,
								'autenticado': True,'userlogin':useractive.username,
								'is_student': isstudent,'is_teacher': isteacher})
				except:
					return render(request, 'checkexercises/index.html', {'Message1': message,
									'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher})
			except:
				print "no existe el profesor"
				message = "THIS REPOSITORY DOESN\'T EXIST"
				listafiles = Library.objects.filter(user=useractive.username)
				try: 
					listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
					return render(request, 'checkexercises/index.html', {'Message2': message,
									'listexercisesteach': listaexerteacher,'listLibraries': listafiles,
									'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher})
				except:
					return render(request, 'checkexercises/index.html', {'Message2': message,
									'listLibraries': listafiles,
									'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher})

		elif request.POST.get('savelibrary'):
			useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
			print "usuario activo savelibrary = ", useractive.username
			if(useractive.first_name == "teacher"):
				isteacher = True
				isstudent = False
				listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
			else:
				isteacher = False
				isstudent = True
				listaexerteacher = StudentExercise.objects.filter(user=useractive.username)
			try:
				is_library = Library.objects.get(name=request.POST.get('savelibrary'),user=useractive.username)
				print "Libreria ", request.POST.get('savelibrary'), "ya esta guardada"
				message = "FILE '"+request.POST.get('savelibrary')+"' EXISTS"
				listafiles = Library.objects.filter(user=useractive.username)
				usuario = Usuario.objects.get(user= useractive.username)
				if(usuario.rankingerrors != ""):
					return render(request, 'checkexercises/index.html', {'MessageFile2': message,
								'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
								'autenticado': True,'userlogin':useractive.username,
								'is_student': isstudent,'is_teacher': isteacher,'global': True,
			    					 'infoerroresGlobal': usuario.data,'rankerrorsglobal': usuario.rankingerrors})
				else:
					return render(request, 'checkexercises/index.html', {'MessageFile2': message,
								'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
								'autenticado': True,'userlogin':useractive.username,
								'is_student': isstudent,'is_teacher': isteacher})
			except:
				print "Libreria ", request.POST.get('savelibrary'), "no esta guardada"
				splitLibrary = (request.POST.get('savelibrary').split(".js"))
				print "Len splitLibrary = ", len(splitLibrary)
				print "splitLibrary = ", splitLibrary
				is_Library1 = False
				if(len(splitLibrary) == 1):
					message = "FILE '"+request.POST.get('savelibrary')+"' IS NOT A .js FILE"
					print "no es .js"

				else:
					if(len(splitLibrary) == 2):
						if(splitLibrary[1] == ""):
							is_Library1 = True
							print "es .js"
							message = "FILE '"+request.POST.get('savelibrary')+"' SAVED"
							saveLibrary(request.POST.get('savelibrary'),useractive.username)
						else:
							message = "FILE '"+request.POST.get('savelibrary')+"' IS NOT A .js FILE"
							print "no es .js 1"
					else:
						message = "FILE '"+request.POST.get('savelibrary')+"' IS NOT A .js FILE"
						print "no es .js 2"

				listafiles = Library.objects.filter(user=useractive.username)
				usuario = Usuario.objects.get(user= useractive.username)
				if(is_Library1 == True):
					if(usuario.rankingerrors != ""):
						return render(request, 'checkexercises/index.html', {'MessageFile1': message,
									'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
									'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher,'global': True,
			    					 'infoerroresGlobal': usuario.data,'rankerrorsglobal': usuario.rankingerrors})
					else:
						return render(request, 'checkexercises/index.html', {'MessageFile1': message,
									'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
									'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher})
				else:
					if(usuario.rankingerrors != ""):
						return render(request, 'checkexercises/index.html', {'MessageFile2': message,
									'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
									'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher,'global': True,
			    					 'infoerroresGlobal': usuario.data,'rankerrorsglobal': usuario.rankingerrors})
					else:
						return render(request, 'checkexercises/index.html', {'MessageFile2': message,
									'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
									'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher})
		elif request.POST.get('deletelibrary'):
			useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
			print "usuario activo deletelibrary = ", useractive.username
			if(useractive.first_name == "teacher"):
				isteacher = True
				isstudent = False
				listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
			else:
				isteacher = False
				isstudent = True
				listaexerteacher = StudentExercise.objects.filter(user=useractive.username)
			try:
				is_library = Library.objects.get(name=request.POST.get('deletelibrary'),user=useractive.username)
				Library.objects.get(name = request.POST.get('deletelibrary'),user=useractive.username).delete()
				message = "FILE '"+request.POST.get('deletelibrary')+"' WAS DELETED"
				listafiles = Library.objects.filter(user=useractive.username)
				usuario = Usuario.objects.get(user= useractive.username)
				if(usuario.rankingerrors != ""):
					return render(request, 'checkexercises/index.html', {'MessageFile1': message,
								'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
								'autenticado': True,'userlogin':useractive.username,
								'is_student': isstudent,'is_teacher': isteacher,'global': True,
			    					 'infoerroresGlobal': usuario.data,'rankerrorsglobal': usuario.rankingerrors})
				else:
					return render(request, 'checkexercises/index.html', {'MessageFile1': message,
								'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
								'autenticado': True,'userlogin':useractive.username,
								'is_student': isstudent,'is_teacher': isteacher})
			except:
				message = "FILE '"+request.POST.get('deletelibrary')+"' DOESN\'T EXIST"
				listafiles = Library.objects.filter(user=useractive.username)
				usuario = Usuario.objects.get(user= useractive.username)
				if(usuario.rankingerrors != ""):
					return render(request, 'checkexercises/index.html', {'MessageFile2': message,
								'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
								'autenticado': True,'userlogin':useractive.username,
								'is_student': isstudent,'is_teacher': isteacher,'global': True,
			    					 'infoerroresGlobal': usuario.data,'rankerrorsglobal': usuario.rankingerrors})
				else:
					return render(request, 'checkexercises/index.html', {'MessageFile2': message,
								'listexercisesteach': listaexerteacher, 'listLibraries': listafiles,
								'autenticado': True,'userlogin':useractive.username,
								'is_student': isstudent,'is_teacher': isteacher})
		elif request.POST.get('createuser'):
			try:
				user = User.objects.get(username=request.POST.get('createuser'))
				print "usuario ya existe"
				return render(request,'checkexercises/index.html',{'autenticado': False,
		    					'errorlogin': "USER NAME EXISTS",'logearse':True})
			except:
				print "usuario no existe"
				try:
					print "antes de coger al usuario activo en crear usuario"
					useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
					print "usuario activo antes de crear usuario es  = ", useractive.username
					useractive.is_active = False
					useractive.save()			
					print "despues de coger al usuario activo en crear usuario"
				except:
					print "no hay usuario activo en crear usuario"

				try:
					name = request.POST.get('createuser') 
					email = request.POST.get('createmail')
					password = request.POST.get('createpassword')
					rol = request.POST.get('createrol')
					print "vamos a crear al usuario ", name, " con email: ",email, " ,y password = ", password, " y rol: ", rol

					#user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
					user = User.objects.create_user(name, email, password)
					print "despues de create_user"
					user.first_name = rol
					print "despues de user.rol"
					# At this point, user is a User object that has already been saved
					# to the database. You can continue to change its attributes
					# if you want to change other fields.
					user.save()

					#creo el usuario y despues hago el login
					#tengo que contemplar el caso de que crear usuario de error!!!!!!!!!!!!!!!!!!!!!!
					userlogin = authenticate(username=name, password=password)
					login(request, userlogin)

					useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
					print "usuario activo despues de crear usuario es  = ", useractive.username
					if(useractive.first_name == "teacher"):
						isteacher = True
						isstudent = False
					else:
						isteacher = False
						isstudent = True

					usuario = Usuario(user= useractive.username)
					usuario.save()
					#tengo que filtrar por user tambien las listas estas
					listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
					listafiles = Library.objects.filter(user=useractive.username)
					print "despues de user.save()"
					return render(request,'checkexercises/index.html',{'listexercisesteach': listaexerteacher,
			    					'listLibraries': listafiles,'autenticado': True, 'userlogin':useractive.username,
			    					'is_student': isstudent,'is_teacher': isteacher})
				except: #no se si llega a entrar por aqui
					print "mal datos de crear usuario"
					return render(request,'checkexercises/index.html',{'autenticado': False,
		    					'errorlogin': "CAN\'T CREATE USER.CHECK YOUR DATA",'logearse':True})

		elif request.POST.get('loginuser'):
			try:
				user = User.objects.get(username=request.POST.get('loginuser'))
				print "usuario ya existe"
			
				try:
					print "antes de coger al usuario activo en loguear usuario"
					useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
					print "usuario activo antes de logear usuario es  = ", useractive.username
					useractive.is_active = False
					useractive.save()			
					print "despues de coger al usuario activo en loguear usuario"
				except:
					print "no hay usuario activo en login"
				###contemplar el caso en el que el login falle
				name = request.POST.get('loginuser') 
				password = request.POST.get('loginpassword')
				print "vamos a loguear al usuario ", name, " ,y password = ", password
				try:
					userlogin = authenticate(username=name, password=password)
					print "entre medias del userlogin y el login de = ", userlogin.username
					login(request, userlogin)
					userlogin.is_active = True
					userlogin.save()
					useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
					if(useractive.first_name == "teacher"):
						isteacher = True
						isstudent = False
						listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
					else:
						isteacher = False
						isstudent = True
						listaexerteacher = StudentExercise.objects.filter(user=useractive.username)
					print "usuario activo despues de logear usuario es  = ", useractive.username, "con rol = ", useractive.first_name
				
					listafiles = Library.objects.filter(user=useractive.username)
					usuario = Usuario.objects.get(user= useractive.username)
					if(usuario.rankingerrors != ""):
						return render(request,'checkexercises/index.html',{'listexercisesteach': listaexerteacher,
			    					'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,
			    					'is_student': isstudent,'is_teacher': isteacher,'global': True,
			    					 'infoerroresGlobal': usuario.data,'rankerrorsglobal': usuario.rankingerrors})
					else:
						return render(request,'checkexercises/index.html',{'listexercisesteach': listaexerteacher,
			    					'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,
			    					'is_student': isstudent,'is_teacher': isteacher})
				except:
					print "usuario existe"
					print "mal contrasena de login usuario"
					return render(request,'checkexercises/index.html',{'autenticado': False,
		    			'errorlogin': "CAN\'T LOGIN USER. WRONG PASSWORD",'logearse':True})			
			except:
				print "usuario no existe"
				return render(request,'checkexercises/index.html',{'autenticado': False,
		    			'errorlogin': "CAN\'T LOGIN USER.USER DOESN\'T EXIST",'logearse':True})
		
		elif request.POST.get('urlanalizstudent'):
			print "estoy dentro de analizar la url de un estudiante"
			print "url = ", request.POST.get('urlanalizstudent')
			useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
			print "usuario activo urlanaliz = ", useractive.username
			if(useractive.first_name == "teacher"):
				isteacher = True
				isstudent = False
			else:
				isteacher = False
				isstudent = True
			#hacer try por si falla algo que se borre de la base de datos
			is_student = StudentExercise.objects.filter(urlStudentEx = request.POST.get('urlanalizstudent')).filter(branch=request.POST.get('rama')).filter(user= useractive.username)
			if(len(is_student) != 0 ):
				print "student exists"
				numordenprev = is_student[len(is_student)-1].numorden
				print "ultimo numorden = ", numordenprev
				numordernew = numordenprev + 1
			
			else:
				print "Does not exist this teacher"
				numordernew = 1
			
			name = request.POST.get('urlanalizstudent').split("/")[3]
			print "name = ", name
			#estudiante = Student(name=name,
			#					 errors="0")
			#estudiante.save()
			student = StudentExercise(urlTeacherEx = "",
									  urlStudentEx = request.POST.get('urlanalizstudent'),
									  nameStudent = name,
									  urlAvatar = request.POST.get('urlavatar'),
									  numportfolio = "",
									  numfichanaliz = "0",
									  branch=request.POST.get('rama'),
									  user= useractive.username,
									  numorden=numordernew)
			student.save()

			try:
				analiz_repo(request.POST.get('urlanalizstudent'),"",
										request.POST.get('rama'),useractive.username,numordernew)
				rankerrors ,data = rankerror(request.POST.get('urlanalizstudent'),request.POST.get('rama'),useractive.username,"student",numordernew)
				exerstudent = StudentExercise.objects.get(urlStudentEx = request.POST.get('urlanalizstudent'),branch=request.POST.get('rama'),user=useractive.username,numorden=numordernew)
				exerstudent.data = data
				exerstudent.rankingerrors = rankerrors
				exerstudent.save()
				erroresglobales,dataglobal = globalSumaryErrors(useractive.username,useractive.first_name)
				try:
					fich1analizado = FichJs.objects.filter(urlstudent=request.POST.get('urlanalizstudent'),user=useractive.username,numorden=numordernew)[0]
					print "fichero = ",fich1analizado.name
					exeranalizado = StudentExercise.objects.get(urlStudentEx=request.POST.get('urlanalizstudent'),user=useractive.username,numorden=numordernew)
					exeranalizado.datafich = fich1analizado.data
					exeranalizado.divdata = fich1analizado.name + "graphic"
					print "divdata = ", exeranalizado.divdata
					exeranalizado.save()
				except:
					print "no se han encontrado ficheros para este repositorio"

				usuario = Usuario.objects.get(user= useractive.username)
				if(erroresglobales == ""):
					print "no habia errores globales"
					if(usuario.rankingerrors != ""):
						print "si habia ranking errores globales"
						erroresglobales = usuario.rankingerrors
						name1 = request.POST.get('urlanalizstudent').split("/")[4]+ "("+ request.POST.get('rama') + ")("+str(numordernew)+")"
						dataglobal = usuario.data + name1 + "errorspace0errorspace"
					else:
						print "no habia ranking globales"
						erroresglobales = "NO ERRORS"
						name1 = request.POST.get('urlanalizstudent').split("/")[4]+ "("+ request.POST.get('rama') + ")("+ str(numordernew)+")"
						dataglobal = name1 + "errorspace0errorspace"
				
				usuario.rankingerrors = erroresglobales
				usuario.data = dataglobal
				usuario.save()
				dataerrorcomparar = compararerrors(request.POST.get('urlanalizstudent'),request.POST.get('rama'),useractive.username,numordernew)
				try:
					lastexer = StudentExercise.objects.get(user=useractive.username,islast=True)
					lastexer.islast = False
					lastexer.save()
				except:
					print "no hay ultimo ejercicio alumno"
				
				Student = StudentExercise.objects.get(urlStudentEx = request.POST.get('urlanalizstudent'),branch=request.POST.get('rama'),user=useractive.username,numorden=numordernew)
				Student.datacomparar = dataerrorcomparar
				Student.islast = True
				Student.save()
			except:
					print "fallo al analizar en estudiante, borro los datos de este repo"
					listaexerstudent = StudentExercise.objects.filter(user=useractive.username)
					listafiles = Library.objects.filter(user=useractive.username)
					deleteData(request.POST.get('urlanalizstudent'),request.POST.get('rama'),useractive.username,numordernew) #ver si funciona cuando falla la descarga del repo
					return render(request, 'checkexercises/index.html', {'listexercisesteach': listaexerstudent,
									'listLibraries': listafiles,'failanalize': "fallo al analizar",
									'autenticado': True,'userlogin':useractive.username,
									'is_student': isstudent,'is_teacher': isteacher})
			
			repostudent = StudentExercise.objects.get(urlStudentEx=request.POST.get('urlanalizstudent'),branch=request.POST.get('rama'),user=useractive.username,numorden=numordernew) #cojo el usuario que esta activo
			ficheros = FichJs.objects.filter(urlstudent=request.POST.get('urlanalizstudent')).filter(branch=request.POST.get('rama')).filter(user=useractive.username).filter(numorden=numordernew)
			listaexerstudent = StudentExercise.objects.filter(user=useractive.username) #creo que esto debe cambiar
			listafiles = Library.objects.filter(user=useractive.username)
			print "antes del render de alumno"
			nomostrar = False
			print "len(ficheros)", len(ficheros)
			if(len(ficheros) == 0):
				nomostrar = True
			return render(request, 'checkexercises/index.html', {'repos': "repostudent" ,'repoavatar': repostudent.urlAvatar,'infoerrores': repostudent.data,
							   'rankerrors': repostudent.rankingerrors,'urlstudent': repostudent.urlStudentEx,'fichs': ficheros ,'listexercisesteach': listaexerstudent,
							   'rama': request.POST.get('rama'),'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,'is_student': True,'is_teacher': False,
							   'graficfich1': repostudent.datafich,'grafdiv': repostudent.divdata,'numord': numordernew,
							   'errorescomparar': repostudent.datacomparar,'nomostrar': nomostrar})	

		elif request.POST.get('logoutuser'):
			print "antes de request"
			useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
			print "usuario activo urlanaliz = ", useractive.username
			useractive.is_active = False
			useractive.save()
			print "despues de request"
			useractive = User.objects.filter(is_active=True).filter(is_staff=False)
			print "len useractive = ", len(useractive)
			return render(request,'checkexercises/index.html',{'logearse': True})

		elif request.POST.get('mainMenu'):
			useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
			if(useractive.first_name == "teacher"):
				isteacher = True
				isstudent = False
				listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
			else:
				isteacher = False
				isstudent = True
				listaexerteacher = StudentExercise.objects.filter(user=useractive.username)
			
			listafiles = Library.objects.filter(user=useractive.username)
			usuario = Usuario.objects.get(user= useractive.username)
			if(usuario.rankingerrors != ""):
				return render(request,'checkexercises/index.html',{'listexercisesteach': listaexerteacher,
	    					'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,
	    					'is_student': isstudent,'is_teacher': isteacher,'global': True,
	    					 'infoerroresGlobal': usuario.data,'rankerrorsglobal': usuario.rankingerrors})
			else:
				return render(request,'checkexercises/index.html',{'listexercisesteach': listaexerteacher,
						'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,
						'is_student': isstudent,'is_teacher': isteacher})

		elif request.POST.get('urlrepeat'):
			useractive = User.objects.get(is_active=True,is_staff=False) #cojo el usuario que esta activo
			if(useractive.first_name == "teacher"):
				print "entra a urlrepeat teacher"
				isteacher = True
				isstudent = False
				teacher = TeacherExercise.objects.get(urlTeacherEx = request.POST.get('urlrepeat'),branch=request.POST.get('rama'),user=useractive.username,numorden=request.POST.get('num'))
				repoalumnos = StudentExercise.objects.filter(urlTeacherEx = request.POST.get('urlrepeat')).filter(branch=request.POST.get('rama')).filter(user=useractive.username).filter(numorden=request.POST.get('num'))
				print "len(repoalumnos) == ", len(repoalumnos)
				nomostrar = False
				if(len(repoalumnos) == 0):
					repoalumnos = "r"
					nomostrar = True
				ficheros = FichJs.objects.filter(exercise=request.POST.get('urlrepeat')).filter(branch=request.POST.get('rama')).filter(user=useractive.username).filter(numorden=request.POST.get('num'))
				listaexerteacher = TeacherExercise.objects.filter(user=useractive.username)
				listafiles = Library.objects.filter(user=useractive.username)
				return render(request, 'checkexercises/index.html', {'repos': repoalumnos ,
							 'urlteach': teacher.urlTeacherEx,'sumaryteach': teacher.sumary,
							 'fichs': ficheros ,'ranktotal': teacher.rankingpercent,'rankfich': teacher.rankingfich,
							  'listexercisesteach': listaexerteacher,'infoerrores': teacher.data,
							   'rankerrors': teacher.rankingerrors,'rama': request.POST.get('rama'),
							    'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,
							    'is_student': isstudent,'is_teacher': isteacher,'numord': int(request.POST.get('num')),
							    'errorescomparar': teacher.datacomparar,'nomostrar': nomostrar})	
			else:
				print "entra a urlrepeat student"
				isteacher = False
				isstudent = True
				repostudent = StudentExercise.objects.get(urlStudentEx=request.POST.get('urlrepeat'),branch=request.POST.get('rama'),user=useractive.username,numorden=request.POST.get('num')) #cojo el usuario que esta activo
				ficheros = FichJs.objects.filter(urlstudent=request.POST.get('urlrepeat')).filter(branch=request.POST.get('rama')).filter(user=useractive.username).filter(numorden=request.POST.get('num'))
				listaexerstudent = StudentExercise.objects.filter(user=useractive.username) #creo que esto debe cambiar
				listafiles = Library.objects.filter(user=useractive.username)
				print "antes del render de alumno"
				nomostrar = False
				print "len(ficheros)", len(ficheros)
				if(len(ficheros) == 0):
					nomostrar = True
				return render(request, 'checkexercises/index.html', {'repos': "repostudent" ,'repoavatar': repostudent.urlAvatar,'infoerrores': repostudent.data,
							   'rankerrors': repostudent.rankingerrors,'urlstudent': repostudent.urlStudentEx,'fichs': ficheros ,'listexercisesteach': listaexerstudent,
							   'rama': request.POST.get('rama'),'listLibraries': listafiles,'autenticado': True,'userlogin':useractive.username,'is_student': True,'is_teacher': False,
							   'graficfich1': repostudent.datafich,'grafdiv': repostudent.divdata,'numord': int(request.POST.get('num')),
							   'errorescomparar': repostudent.datacomparar,'nomostrar': nomostrar})	

		elif request.POST.get('deluser'):
				nameuser = request.POST.get('deluser')
				keyuser = request.POST.get('delpassword')
				print "vamos a eliminar al usuario ", nameuser , "con key ", keyuser
				try:#primero veo si ese usuario existe
					user = Usuario.objects.get(user= nameuser)
					userexist = authenticate(username=nameuser, password=keyuser)#compruebo que la contrasena es correcta
					if userexist is not None:
						print "contrasena correcta"
						userexist = User.objects.get(username=nameuser)
						rol = userexist.first_name
						print "rol = ", rol
						deleteUser(user.user,rol)
						user.delete()
						print "usuario borrado"
						userexist.delete()
						print "usuario borrado definitivamente"
						mensaje = "USER '"+ nameuser + "'' WAS DELETED"
						return render(request,'checkexercises/index.html',{'autenticado': False,
		    					'errordel': mensaje,'logearse':True})
					else:
						print "contrasena incorrecta"
						return render(request,'checkexercises/index.html',{'autenticado': False,
		    					'errordel': "CAN\'T DELETE USER.WRONG PASSWORD",'logearse':True})
						
				except:
					print "no existe el usuario"
					return render(request,'checkexercises/index.html',{'autenticado': False,
		    					'errordel': "CAN\'T DELETE USER.USER DOESN\'T EXISTS",'logearse':True})
		else:
			print "entra en el else"
			return render(request, 'checkexercises/index.html', {'repos': listforks})
			#nada de momento 

		#return render_to_response('checkexercises/index.html', {'repos': listforks}, context_instance=RequestContext(request))
		#return render(request,'checkexercises/index.html')
  

@csrf_exempt
def redir(request):
	if request.method == "GET":  
	    #print "template = " + str(template)
	    print "estoy en get de redir aaaaaaaa "
	    return HttpResponseRedirect('http://www.as.com/')