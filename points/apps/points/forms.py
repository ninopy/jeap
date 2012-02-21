#coding=utf-8
from uliweb.form import *
from uliweb import settings

class PointsForm(Form):
	p_name    = StringField(label="知识点名字", required=True)	
	p_desc    = TextField(label="知识点描述", required=True,cols=200)	
	p_av_addr = StringField(label="知识点音视频网址")	

class DepsForm(Form):
	d_parent_name = StringField(label="依赖的知识点名称")

class CommForm(Form):
	comm_desc = TextField(label="留下您的建议",required=True,cols=200,rows=6)
