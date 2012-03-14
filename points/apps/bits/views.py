#coding=utf-8
from uliweb import expose
from uliweb import settings
from models import msoc
from models import mdevice
from models import mreg
from models import mbits
from models import mmeanings
from uliweb.orm import get_model
from forms import SocForm
from forms import DeviceForm
from forms import RegForm
from forms import BitsForm
from forms import MeaningsForm
from uliweb import function
require_login = function('require_login')
from uliweb.contrib.auth.views  import login
from points.models import events



@expose('/regs/')
def index_device():
	return {}

@expose('/getregsdata')
def getregsdata():
    data = [{'id':'1','pId':'0','name':'SOC列表','open':'true'},]
    countid = 2
    soc = msoc.all()
    devices = mdevice.all()
    for s in soc:
        soc_url='/regs/display_soc/%s/%s' % (s.soc_name,s.id)
        data.append({'id':countid,'pId':'1','name':s.soc_name,'url':soc_url,'target':'_self'})
        sid = countid
        countid += 1
        for d in devices:
            if d.soc_name == s.soc_name:
                dev_url='/regs/display_device/%s/%s' % (d.device_name,d.id)
                data.append({'id':countid,'pId':sid,'name':d.device_name,'url':dev_url,'target':'_self'})
                countid += 1
    return json(data)

@expose('/regs/add_soc')
def add_soc():
    if require_login():
        return redirect(url_for(login))
    form = SocForm()
    if request.method == 'GET':
	    return {'form':form}
    elif request.method == 'POST':
        flag = form.validate(request.params)
        if flag:
            n = msoc(**form.data)
            s = msoc.get(msoc.c.soc_name == form.data.soc_name)		
            if s: 
                return redirect('/message/添加错误，重名/-1') 
        n.save()
        return redirect('/regs/')


@expose('/regs/display_soc/<soc_name>/<id>')
def display_soc(soc_name,id):
	s = msoc.get(msoc.c.id == id)
	d = mdevice.filter(mdevice.c.soc_name == soc_name)
	return {'s':s,'d':d}

@expose('/regs/delete_soc/<id>')
def delete_soc(id):
    if require_login():
         return redirect(url_for(login))
    if (request.user.is_superuser == False):
        return redirect('/message/只有管理员才能删除SOC/-1')
    s = msoc.get(msoc.c.id == id)
    s.delete()
    return redirect('/message/删除完成/-2')

@expose('/regs/delete_device/<id>')
def delete_device(id):
    if require_login():
         return redirect(url_for(login))
    d = mdevice.get(mdevice.c.id == id)
    if cmp(d.adminname,request.user.username) and (request.user.is_superuser == False):
        return redirect('/message/只有设备管理者才能删除/-1')
    d.delete()
    return redirect('/message/删除完成/-2')




@expose('/regs/add_device/<soc_name>/<id>')
def add_device(soc_name,id):
    if require_login():
        return redirect(url_for(login))
    form = DeviceForm()
    if request.method == 'GET':
        return {'form':form}
    elif request.method == 'POST':
        flag = form.validate(request.params)
        if flag:
            n = mdevice(**form.data)
            s = mdevice.filter(mdevice.c.device_name == form.data.device_name)\
                       .filter(mdevice.c.soc_name == soc_name)		
            for s1 in s:
                return redirect('/message/添加错误，重名/-1') 
        n.soc_name=soc_name
        n.adminname = request.user
        n.save()
        return redirect('/regs/')

@expose('/regs/display_device/<device_name>/<id>')
def display_device(device_name,id):
	d = mdevice.get(mdevice.c.id == id)
	r = mreg.filter(mreg.c.device_id == id)
	return {'r':r,'d':d}

##############################################333

@expose('/regs/add_r/<device_name>/<device_id>')
def add_r(device_name,device_id):
        if require_login():
            return redirect(url_for(login))
        form = RegForm()
        if request.method == 'GET':
            return {'form':form}
        elif request.method == 'POST':
            flag = form.validate(request.params)
            if flag:
                n = mreg(**form.data)
                r = mreg.filter(mreg.c.reg_name == form.data.reg_name).filter(mreg.c.device_id==device_id)
                for r1 in r:
                    return redirect('/message/添加错误，重名/-1') 
                n.adminname = request.user
                n.device_name = device_name
                n.device_id   = device_id
                n.save()
                ne = events()
                ne.username = request.user
                ne.action = '增加了寄存器'
                ne.objs = form.data.reg_name
                ne.save()
                return redirect('/message/添加完成/-2') 
            else:
                message='错误'
                return {'form':form}
 
@expose('/regs/edit_r/<id>')
def edit_r(id):
    if require_login():
         return redirect(url_for(login))
    r = mreg.get(mreg.c.id == id)
    if cmp(r.adminname,request.user.username) and (request.user.is_superuser == False):
        return redirect('/message/您不是该知识点的管理者/-1')
    if request.method == 'GET': 
		r = mreg.get(mreg.c.id == id)
		form = RegForm(data ={'reg_name':r.reg_name,'reg_desc':r.reg_desc,\
							'reg_address':r.reg_address})
		return {'form':form}	
    elif request.method == 'POST':
            form = RegForm()
            flag = form.validate(request.params)
            if flag:
                n=mreg.get(int(id))
                n.reg_name= form.data.reg_name
                n.reg_desc= form.data.reg_desc
                n.reg_address= form.data.reg_address
                n.save()
                return redirect('/message/编辑完成/-2')
            else:
                message='错误'
                return {'form':form}
	


@expose('/regs/display_r/<id>')
def display_r(id):
    ms = []
    r = mreg.get(mreg.c.id == id)
    b = mbits.filter(mbits.c.reg_id == id)
    for b1 in b:
        m = mmeanings.filter(mmeanings.c.bits_id==b1.id)
        for m1 in m:
            ms.append(m1)
    return {'r':r,'b':b,'ms':ms}


def regcal(sbit,ebit,value):
	value  = (value << (31-ebit)) & 0xFFFFFFFF 
	value  = value >> (31 + sbit - ebit)
	return value

@expose('/regs/search/<id>')
def search(id):
    m = []
    ms = []
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
    for b2 in b:
        m2 = mmeanings.filter(mmeanings.c.bits_id==b2.id)
        for m1 in m2:
            ms.append(m1)
    return {'r':r,'b1':b1,'m':m,'rvalue':rvalue,'ms':ms}
	
@expose('/regs/delete_r/<id>')
def delete_r(id):
    if require_login():
        return redirect(url_for(login))
    r = mreg.get(mreg.c.id == id)
    if cmp(r.adminname,request.user.username) and (request.user.is_superuser == False):
        return redirect('/message/您不是该知识点的管理者/-1')
    r.delete()
    return redirect('/message/删除完成/-2')
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
                b = mbits.filter(mbits.c.bits_name == form.data.bits_name)\
                         .filter(mbits.c.reg_id == reg_id)
                for b1 in b:
                    return redirect('/message/添加错误，重名/-1') 
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
        return redirect('/message/您不是该知识点的管理者/-1')
    b.delete()
    return redirect('/message/删除完成/-2')


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
                    return redirect('/message/该值已经存在/-1') 
                n.bits_name = bits_name
                n.bits_id = bits_id
                n.save()
                return redirect('/regs/add_mean/%s/%s'% (bits_name,bits_id))
            else:
                message='错误'
                return {'form':form}

@expose('/regs/delete_mean/<id>')
def delete_mean(id):
    if require_login():
         return redirect(url_for(login))
    m = mmeanings.get(mmeanings.c.id == id)
    b = mbits.get(mbits.c.id == m.bits_id)
    r = mreg.get(mreg.c.id == b.reg_id)
    if cmp(r.adminname,request.user.username) and (request.user.is_superuser == False):
        return redirect('/message/您不是该知识点的管理者/-1')
    m.delete()
    return redirect('/message/删除完成/-2')




