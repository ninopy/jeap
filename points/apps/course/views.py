#coding=utf-8
from uliweb import expose
from uliweb import settings
from models import mcourses
from models import mc_deps_ps  as cdp #depend points
from models import mc_deps_cs  as cdc #depend courses
from uliweb.orm import get_model
from forms import C_Deps_PForm as CDPForm
from forms import C_Deps_CForm as CDCForm
from forms import CoursesForm
from points.models import events

from uliweb import function
require_login = function('require_login')
from uliweb.contrib.auth.views  import login



@expose('/course/')
def index_c():
	courses = mcourses.all()
	return {'courses':courses}

@expose('/course/add_c')
def add_c():
        if require_login():
             return redirect(url_for(login))
        form = CoursesForm()
        if request.method == 'GET':
            return {'form':form}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = mcourses(**form.data)
                c = mcourses.get(mcourses.c.c_name == form.data.c_name)
                if c:
                   return '<a href=/course/>添加错误,重名</a>'
                n.save()
                ne = events()
                ne.username = request.user
                ne.action = '增加了课程'
                ne.objs = form.data.c_name
                ne.save()
                return '<a href="/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
 
@expose('/course/edit_c/<c_name>/<id>')
def edit_c(c_name,id):
    if require_login():
          return redirect(url_for(login))
    if request.method == 'GET': 
		c = mcourses.get(mcourses.c.id == id)
		form = CoursesForm(data ={'c_name':c.c_name,'c_desc':c.c_desc})
		return {'form':form}	
    elif request.method == 'POST':
            form = CoursesForm()
            flag = form.validate(request.params)
            if flag:
                n=mcourses.get(int(id))
                n.c_desc = form.data.c_desc
                n.save()
                ne = events()
                ne.username = request.user
                ne.action = '修改了课程'
                ne.objs = form.data.c_name
                ne.save()
                return '<a href="/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
	


@expose('/course/display_c/<c_name>/<id>')
def display_c(c_name,id):
	p_cdc = cdc.filter(cdc.c.c_name==c_name)
	c_cdc = cdc.filter(cdc.c.c_parent_c==c_name)
	c = mcourses.get(mcourses.c.c_name == c_name)
	p_cdp = cdp.filter(cdp.c.c_name==c_name)
	return {'c':c,'p_cdc':p_cdc,'c_cdc':c_cdc,'p_cdp':p_cdp}
	
@expose('/course/delete_c/<id>')
def delete_c(id):
    if require_login():
        return redirect(url_for(login))
    c=mcourses.get(int(id))
    c.delete()
    ne = events()
    ne.username = request.user
    ne.action = '删除了课程'
    ne.objs = c.c_name
    ne.save()
    return '<a href="/">删除完成</a>'
######################################
@expose('/course/add_cc/<c_name>')
def add_cc(c_name):
    	if require_login():
        	return redirect(url_for(login))
        form = CDCForm()
        if request.method == 'GET':
            return {'form':form,'c_name':c_name}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = cdc(**form.data)
                n.c_name = c_name
                n.save()
                return '<a href="/">添加完成</a>'
                ne = events()
                ne.username = request.user
                ne.action = '增加了课程依赖'
                ne.objs = c_name
                ne.save()
            else:
                message='错误'
                return {'form':form}

@expose('/course/add_cp/<c_name>')
def add_cp(c_name):
    	if require_login():
        	return redirect(url_for(login))
        form = CDPForm()
        if request.method == 'GET':
            return {'form':form,'c_name':c_name}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = cdp(**form.data)
                n.c_name = c_name
                n.save()
                ne = events()
                ne.username = request.user
                ne.action = '增加了知识点依赖'
                ne.objs = c_name
                ne.save()
                return '<a href="/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
 
