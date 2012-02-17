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

@expose('/course/')
def index_c():
	courses = mcourses.all()
	return {'courses':courses}

@expose('/course/add_c')
def add_c():
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
                return '<a href="/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
 
@expose('/course/edit_c/<c_name>/<id>')
def edit_c(c_name,id):
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
	c=mcourses.get(int(id))
	c.delete()
	return '<a href="/">删除完成</a>'
######################################
@expose('/course/add_cc/<c_name>')
def add_cc(c_name):
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
            else:
                message='错误'
                return {'form':form}

@expose('/course/add_cp/<c_name>')
def add_cp(c_name):
        form = CDPForm()
        if request.method == 'GET':
            return {'form':form,'c_name':c_name}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = cdp(**form.data)
                n.c_name = c_name
                n.save()
                return '<a href="/">添加完成</a>'
            else:
                message='错误'
                return {'form':form}
 
