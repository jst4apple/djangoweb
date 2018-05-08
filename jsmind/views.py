# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
#from models import InterationRe,IndirectRe,Node,UserInfo

def auth(func):
	def inner(request):
		if request.user.is_authenticated():
			return func(request)
		else:
			return  render(request, 'registration/login.html', context={'next': request.path})
	return inner
@auth
def index(request):
	userinfo = {
		'username':request.user.username
	}
	
	return render(request, 'jsmind/index.html', context = {'userinfo':userinfo})
		

@auth
def getcenter(request):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		id = request.POST.get('type_id')
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")

#create a relationship
@auth
def rel_create(request):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		request.POST.get('start')
		request.POST.get('end')
		
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")
		
#delete a relationship  should build a forget mechanism don't delte the data immedaitally
@auth
def rel_del(request):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		id = request.POST.get('type_id')
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")		
		
@auth
def node_create(request):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		id = request.POST.get('type_id')
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")
		
@auth
def node_delete(request):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		id = request.POST.get('type_id')
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")