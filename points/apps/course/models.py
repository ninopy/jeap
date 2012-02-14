#coding=utf-8
from uliweb.orm import *

class mcourses(Model):
	c_name    = Field(CHAR)
	c_desc 	  = Field(str)

class mc_deps_ps(Model): # course depend points
	c_name      = Field(CHAR)
	c_deps_p    = Field(CHAR) 
	
class mc_deps_cs(Model): # course depend courses
	c_name      = Field(CHAR)
	c_parent_c  = Field(CHAR) 
