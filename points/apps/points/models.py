#coding=utf-8
from uliweb.orm import *

class mpoints(Model):
	p_name    = Field(CHAR)
	p_desc 	  = Field(str)
	p_av_addr = Field(CHAR)

class mdeps(Model):
	d_name           = Field(CHAR)
	d_parent_name    = Field(CHAR)
	
