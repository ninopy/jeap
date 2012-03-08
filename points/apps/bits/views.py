#coding=utf-8
from uliweb import expose
from uliweb import settings
from models import mreg
from models import mbits
from models import mmeanings
from uliweb.orm import get_model
from forms import RegForm
from forms import BitsForm
from forms import MeaningsForm
from uliweb import function
require_login = function('require_login')
from uliweb.contrib.auth.views  import login
from points.models import events



@expose('/regs/')
def index_r():
	regs = mreg.all()
	return {'regs':regs}

@expose('/regs/add_r/<reg_name>')
def add_r(reg_name):
        if require_login():
            return redirect(url_for(login))
        form = RegForm()
        if request.method == 'GET':
            form.reg_name.data = reg_name
            return {'form':form}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = mreg(**form.data)
                r = mreg.get(mreg.c.reg_name == form.data.reg_name)
                if r:
                    return redirect('/message/添加错误，重名') 
                n.adminname = request.user
                n.save()
                ne = events()
                ne.username = request.user
                ne.action = '增加了寄存器'
                ne.objs = form.data.p_name
                ne.save()
                return redirect('/message/添加完成') 
            else:
                message='错误'
                return {'form':form}
 
@expose('/regs/edit_r/<reg_name>/<id>')
def edit_r(reg_name,id):
    if require_login():
         return redirect(url_for(login))
    r = mreg.get(mreg.c.id == id)
    if cmp(r.adminname,request.user.username) and (request.user.is_superuser == False):
        return redirect('/message/您不是该知识点的管理者')
    if request.method == 'GET': 
		r = mreg.get(mreg.c.id == id)
		form = RegForm(data ={'reg_name':r.reg_name,'reg_desc':r.reg_desc,\
							'reg_address':r.reg_address,'device_name':r.device_name,'device_id':r.device_id})
		return {'form':form}	
    elif request.method == 'POST':
            form = RegForm()
            flag = form.validate(request.params)
            if flag:
                n=mreg.get(int(id))
                n.reg_name= form.data.reg_name
                n.reg_desc= form.data.reg_desc
                n.reg_address= form.data.reg_address
                n.device_name= form.data.device_name
                n.device_id= form.data.device_id
                n.save()
                return redirect('/message/编辑完成')
            else:
                message='错误'
                return {'form':form}
	


@expose('/regs/display_r/<reg_name>/<id>')
def display_r(reg_name,id):
	r = mreg.get(mreg.c.id == id)
	b = mbits.filter(mbits.c.reg_id == id)
	return {'r':r,'b':b}


def regcal(sbit,ebit,value):
	value  = (value << (31-ebit)) & 0xFFFFFFFF 
	value  = value >> (31 + sbit - ebit)
	return value

@expose('/regs/search/<id>')
def search(id):
    m = []
    b1 = []
    r = mreg.get(mreg.c.id == id)
    b = mbits.filter(mbits.c.reg_id == id)
    if request.method == 'POST':
        rvalue = request.params.get('rvalue')
    for n in b:
        n.val = regcal(int(n.bits_sbit),int(n.bits_ebit),int(rvalue,16)) 
        b1.append(n)
        mean = mmeanings.filter(mmeanings.c.bits_id==n.id).filter(mmeanings.c.val==str(n.val))
        for me1 in mean:
            m.append(me1)
    return {'r':r,'b1':b1,'m':m,'rvalue':rvalue}
	
@expose('/regs/delete_r/<id>')
def delete_r(id):
    if require_login():
         return redirect(url_for(login))
    r = mreg.get(mreg.c.id == id)
    if cmp(r.adminname,request.user.username) and (request.user.is_superuser == False):
        return redirect('/message/您不是该知识点的管理者')
	r.delete()
	return redirect('/message/删除完成')
##########################################################
@expose('/regs/add_b/<reg_name>/<reg_id>')
def add_b(reg_name,reg_id):
        if require_login():
            return redirect(url_for(login))
        form = BitsForm()
        if request.method == 'GET':
            b=mbits.filter(mbits.c.reg_id==reg_id) 
            return {'form':form,'reg_name':reg_name,'b':b}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = mbits(**form.data)
                b = mbits.get(mbits.c.bits_name == form.data.bits_name)
                if b:
                    return redirect('/message/添加错误，重名') 
                n.reg_name = reg_name
                n.reg_id = reg_id
                n.save()
                ne = events()
                ne.username = request.user.username
                ne.action = '增加了位说明'
                ne.objs = reg_name
                ne.save()
                return redirect('/regs/add_b/%s/%s'% (reg_name,reg_id))
            else:
                message='错误'
                return {'form':form}

@expose('/regs/delete_b/<id>')
def delete_b(id):
    if require_login():
         return redirect(url_for(login))
    b = mbits.get(mbits.c.id == id)
    r = mreg.get(mreg.c.id == b.reg_id)
    if cmp(r.adminname,request.user.username) and (request.user.is_superuser == False):
        return redirect('/message/您不是该知识点的管理者')
    b.delete()
    return redirect('/message/删除完成')


##########################################################
@expose('/regs/add_mean/<bits_name>/<bits_id>')
def add_mean(bits_name,bits_id):
        if require_login():
            return redirect(url_for(login))
        form = MeaningsForm()
        if request.method == 'GET':
            m=mmeanings.filter(mmeanings.c.bits_id==bits_id)
            return {'form':form,'m':m}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = mmeanings(**form.data)
                m = mmeanings.filter(mmeanings.c.val == form.data.val).filter(mmeanings.c.bits_id==bits_id)
                for m1 in m:
                    return redirect('/message/改值已经存在') 
                n.bits_name = bits_name
                n.bits_id = bits_id
                n.save()
                return redirect('/regs/add_mean/%s/%s'% (bits_name,bits_id))
            else:
                message='错误'
                return {'form':form}



