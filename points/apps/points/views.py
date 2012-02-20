#coding=utf-8
from uliweb import expose
from uliweb import settings
from models import mpoints
from models import mdeps
from models import events
from uliweb.orm import get_model
from forms import DepsForm
from uliweb import function
require_login = function('require_login')
from uliweb.contrib.auth.views  import login
from course.models import mcourses

@expose('/')
def index():
	event = events.all().order_by(events.c.datetime.desc()).limit(10)
	courses = mcourses.all().order_by(mcourses.c.id.desc()).limit(10)
	points = mpoints.all().order_by(mpoints.c.id.desc()).limit(10)
	return {'event':event,'courses':courses,'points':points}

@expose('/points/')
def index_p():
	points = mpoints.all()
	return {'points':points}

@expose('/points/add_p')
def add_p():
        if require_login():
			return redirect(url_for(login))
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
                ne = events()
                ne.username = request.user
                ne.action = '增加了知识点'
                ne.objs = form.data.p_name
                ne.save()

                return '<a href="/points/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
 
@expose('/points/edit_p/<p_name>/<id>')
def edit_p(p_name,id):
	if require_login():
		return redirect(url_for(login))
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
                ne = events()
                ne.username = request.user
                ne.action = '修改了知识点'
                ne.objs = form.data.p_name
                ne.save()
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
	if require_login():
		return redirect(url_for(login))
	p=mpoints.get(int(id))
	p.delete()
	ne = events()
	ne.username = request.user
	ne.action = '删除了知识点'
	ne.objs = p.p_name
	ne.save()
	return '<a href="/">ok</a>'
######################################
@expose('/points/add_d/<p_name>')
def add_d(p_name):
        if require_login():
			return redirect(url_for(login))
        form = DepsForm()
        if request.method == 'GET':
            return {'form':form,'p_name':p_name}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = mdeps(**form.data)
                n.d_name = p_name
                n.save()
                ne = events()
                ne.username = request.user
                ne.action = '增加了知识点依赖'
                ne.objs = p_name
                ne.save()
                return '<a href="/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
 
