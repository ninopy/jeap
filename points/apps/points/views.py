#coding=utf-8
from uliweb import expose
from uliweb import settings
from models import mpoints
from models import mdeps
from models import events
from models import comments
from uliweb.orm import get_model
from forms import DepsForm
from forms import CommForm
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

@expose('/message/<m>')
def message(m):
	return {'m':m}

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
                    return redirect('/message/添加错误，重名')
                n.status = '开启'
                n.adminname = request.user
                n.save()
                ne = events()
                ne.username = request.user
                ne.action = '增加了知识点'
                ne.objs = form.data.p_name
                ne.save()
                return redirect('/message/添加完成') 
            else:
                message='错误'
                return {'form':form}
 
@expose('/points/edit_p/<p_name>/<id>')
def edit_p(p_name,id):
	if require_login():
		return redirect(url_for(login))
	p = mpoints.get(mpoints.c.id == id)
	if cmp(p.adminname,request.user.username):
		return redirect('/message/您不是该知识点的管理者')
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
                ne.username = request.user.username
                ne.action = '修改了知识点'
                ne.objs = form.data.p_name
                ne.save()
                return redirect('/message/添加完成')
            else:
                message='错误'
                return {'form':form}
	


@expose('/points/display_p/<p_name>/<id>')
def display_p(p_name,id):
	if request.method == 'POST':
		form = CommForm()
		flag = form.validate(request.params)
		if flag:
			co = comments(**form.data)
			co.username = request.user.username
			co.comm_objs = p_name
			co.save()
	pd = mdeps.filter(mdeps.c.d_name==p_name)
	cd = mdeps.filter(mdeps.c.d_parent_name==p_name)
	p = mpoints.get(mpoints.c.p_name == p_name)
	if not p:
		return redirect('/message/该知识点不存在，您可以添加')
	comm = comments.filter(comments.c.comm_objs==p_name)
	form = CommForm()
	return {'p':p,'pd':pd,'cd':cd,'comm':comm,'form':form}
	
@expose('/points/delete_p/<id>')
def delete_p(id):
	if require_login():
		return redirect(url_for(login))
	p = mpoints.get(mpoints.c.id == id)
	if cmp(p.adminname,request.user.username):
		return redirect('/message/您不是该知识点的管理者')
	p.delete()
	ne = events()
	ne.username = request.user
	ne.action = '删除了知识点'
	ne.objs = p.p_name
	ne.save()
	return redirect('/message/删除成功')
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
                ne.username = request.user.username
                ne.action = '增加了知识点依赖'
                ne.objs = p_name
                ne.save()
                return redirect('/message/添加完成')
            else:
                message='错误'
                return {'form':form}
 
