#coding=utf-8
from uliweb.orm import *

class mreg(Model):
	reg_name     = Field(CHAR)
	reg_address  = Field(CHAR)
	reg_desc     = Field(CHAR)
	device_name  = Field(CHAR)
	device_id    = Field(CHAR)
	adminname    = Field(CHAR)

class mbits(Model):
	reg_name     = Field(CHAR)
	reg_id       = Field(CHAR)
	bits_name    = Field(CHAR)
	bits_sbit    = Field(CHAR)
	bits_ebit    = Field(CHAR)
	val          = Field(CHAR)
	bit_depend   = Field(bool)
	
class mmeanings(Model):
	bits_name      = Field(CHAR)
	bits_id        = Field(CHAR)
	val            = Field(CHAR)
	meanings       = Field(CHAR)
