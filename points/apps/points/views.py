#coding=utf-8
from uliweb import expose
from uliweb import settings
from models import mpoints
from models import mdeps
from uliweb.orm import get_model
from forms import DepsForm

@expose('/')
def index():
	main = '知识点'
	return {'main':main}

@expose('/points/')
def index_p():
	points = mpoints.all()
	return {'points':points}

@expose('/points/add_p')
def add_p():
        from forms import PointsForm
        form = PointsForm()
        if request.method == 'GET':
            return {'form':form}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = mpoints(**form.data)
                p = mpoints.get(mpoints.c.p_name == form.data.p_name)
                if p:
                    return '<a href=/points/>添加错误，重名</a>'
                n.save()
                return '<a href="/points/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
 
@expose('/points/edit_p/<p_name>/<id>')
def edit_p(p_name,id):
	from forms import PointsForm
	if request.method == 'GET': 
		p = mpoints.get(mpoints.c.id == id)
		form = PointsForm(data ={'p_name':p.p_name,'p_desc':p.p_desc,'p_av_addr':p.p_av_addr})
		return {'form':form}	
	elif request.method == 'POST':
            form = PointsForm()
            flag = form.validate(request.params)
            if flag:
                n=mpoints.get(int(id))
                n.p_name= form.data.p_name
                n.p_desc= form.data.p_desc
                n.p_av_addr= form.data.p_av_addr
                n.save()
                return '<a href="/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
	


@expose('/points/display_p/<p_name>/<id>')
def display_p(p_name,id):
	pd = mdeps.filter(mdeps.c.d_name==p_name)
	cd = mdeps.filter(mdeps.c.d_parent_name==p_name)
	p = mpoints.get(mpoints.c.p_name == p_name)
	return {'p':p,'pd':pd,'cd':cd}
	
@expose('/points/delete_p/<id>')
def delete_p(id):
	p=mpoints.get(int(id))
	p.delete()
	return '<a href="/">添加完成</a>'
######################################
@expose('/points/add_d/<p_name>')
def add_d(p_name):
        form = DepsForm()
        if request.method == 'GET':
            return {'form':form,'p_name':p_name}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = mdeps(**form.data)
                n.d_name = p_name
                n.save()
                return '<a href="/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
 
