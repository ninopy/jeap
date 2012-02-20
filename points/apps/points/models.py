#coding=utf-8
from uliweb.orm import *

class mpoints(Model):
	p_name    = Field(CHAR)
	p_desc 	  = Field(TEXT)
	p_av_addr = Field(CHAR)

class mdeps(Model):
	d_name           = Field(CHAR)
	d_parent_name    = Field(CHAR)

class events(Model):
	username = Field(CHAR)
	action   = Field(CHAR)
	objs     = Field(CHAR)
	datetime = Field(datetime.datetime, auto_now_add=True)	
