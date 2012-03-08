#coding=utf-8
from uliweb.form import *
from uliweb import settings

class RegForm(Form):
    device_name  = StringField(label="所属设备名称",required=True)
    device_id    = StringField(label="所属设备ID号")
    reg_name     = StringField(label="寄存器名字",required=True)
    reg_address  = StringField(label="寄存器的偏移地址")
    reg_desc     = StringField(label="寄存器说明",required=True)



class BitsForm(Form):
	bits_name    = StringField(label="位名称", required=True)	
	bits_sbit   = StringField(label="开始位", required=True)	
	bits_ebit   = StringField(label="结束位",required=True)	
	bites_depend = BooleanField(label="是否依赖其他寄存器")

class MeaningsForm(Form):
	val      = StringField(label="值")
	meanings = StringField(label="含义")
