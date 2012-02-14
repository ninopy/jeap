#coding=utf-8
from uliweb.form import *
from uliweb import settings

class CoursesForm(Form):
	c_name    = StringField(label="课程名称", required=True)	
	c_desc    = TextField(label="课程描述", required=True)	

class C_Deps_PForm(Form):
	c_deps_p = StringField(label="依赖的知识点名称")

class C_Deps_CForm(Form):
	c_parent_c = StringField(label="依赖的课程名称")
