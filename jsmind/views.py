# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
import sys
from django.http import HttpResponse
from django.shortcuts import render
import base64
from urllib import parse
# Create your views here.
from django.shortcuts import render, redirect
#from models import InterationRe,IndirectRe,Node,UserInfo

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("********************", os.getcwd())
from agraph.server import agraph, genRelations,uri2str,uri2name
from datamap.tree import *
from datamap.entry import Execute
from pythonfun import fundef,Cls,ClsNameSpace,ModuleLoad
default_scope_func = {'fundef':fundef,'Cls':Cls, 'ClsNameSpace':ClsNameSpace,'ModuleLoad':ModuleLoad}



import logging
import logging.config
import time

log_filename = "logging.log"
logging.basicConfig(level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a',
	filename = log_filename)
	
	
def auth(func):
	def inner(request):
		if request.user.is_authenticated:
			userinfo = {
				'username':request.user.username
			}
			return func(request, userinfo)
		else:
			return  render(request, 'registration/login.html', context={'next': request.path})
	return inner
@auth
def index(request, userinfo):
	return render(request, 'jsmind/index.html', context = {'userinfo':userinfo})




str2cmd = lambda strs:'for expr in [%s]:exec(expr)'%strs

	#return {param['name']:param['root'],param['children']:[roots.append(parent) or insertChild(parent)  for parent in parents if not parent in childrens and not parent in roots]}
	#insertChild = lambda s: not s in parents and  {param['name']:s} or {param['name']:s, param['children']:[pairs.add(parents[i], childrens[i]) or insertChild(childrens[i])  for i in range(0,len(parents)) if parents[i] == s and not (parents[i], childrens[i]) in pairs]}
	#return {param['name']:param['root'],param['children']:[roots.append(parent) or insertChild(parent)  for parent in parents if not parent in childrens and not parent in roots]}






@auth
def repoClass(request, userinfo):
	catalog = request.GET.get('catalog', "")
	repo = request.GET.get('repo',"owl")
	lang = request.GET.get('lang', "zh")
	relation = request.GET.get('rel', "rdfs:subClassOf")
	cmdlist = ['query = """SELECT ?s ?o ?sName ?oName WHERE { \
				?s  rdfs:subClassOf  ?o; \
					rdfs:label ?sName FILTER (lang(?sName) = "zh"). \
					?o rdfs:label ?oName FILTER (lang(?oName) = "zh")"""' , 'agraph.repoOpen(catalog, repo)', 
					'elementmap = lambda elem : (uri2str(elem, "sName"), uri2str(elem, "oName"),uri2name(elem,"s"), uri2name(elem,"o"))',
					'elementgen = lambda elem : elem[2][0] and elem[3][0] and parents.append(elem[3][0] + \':"%s"\'%elem[1]) or childrens.append(elem[2][0] + \':"%s"\'%elem[0])',
					'parents ,childrens,roots = ([],[],[])',
					'genRelations(elementmap, elementgen, query_lang)',
					'len(parents) or genRelations(elementmap, elementgen, query)',
					'data = pairs2Tree(parents, childrens)',
					'viewstyle = "height:100%"']
	#print [catalog, repo, lang, relation]
	#agraph.repoOpen(catalog, repo)
	
	
	#query_lang = """
	#	SELECT ?s ?o ?sName ?oName WHERE {
	#		?s  %s  ?o;
	#			rdfs:label ?sName FILTER (lang(?sName) = "%s").
	#		?o rdfs:label ?oName FILTER (lang(?oName) = "%s")
	#	}"""%(relation, lang, lang)
	#
	#query ="""
	#	SELECT ?s ?o ?sName ?oName WHERE {
	#		?s  %s  ?o;
	#			rdfs:label ?sName.
	#		?o rdfs:label ?oName 
	#	}"""%relation	
	
	elementmap = lambda elem : (uri2str(elem, "sName"), uri2str(elem, "oName"),uri2name(elem,"s"), uri2name(elem,"o"))
	elementgen = lambda elem : elem[2][0] and elem[3][0] and parents.append(elem[3][0] + ':"%s"'%elem[1]) or childrens.append(elem[2][0] + ':"%s"'%elem[0])
	parents ,childrens,roots = ([],[],[])
	genRelations(elementmap, elementgen, query_lang)	
	len(parents) or genRelations(elementmap, elementgen, query)
		
	
	data = pairs2Tree(parents, childrens)
	logging.info(data)
	viewstyle = "height:100%"
	
	return 

	
@auth
def repoConn(request, userinfo):
	
	isjson = request.GET.get('isjson', False)
	catalog = request.GET.get('catalog', "")
	repo = request.GET.get('repo','sys')
	query = request.GET.get('query',"""
							SELECT ?s ?p ?o {
								?s  ?p  ?o;}
							""")
	print [catalog, repo, query]
	agraph.repoOpen(catalog, repo)
	
	parents ,childrens= ([],[])
	elementmap = lambda elem : (uri2name(elem,"s"), uri2name(elem,"o"))
	elementgen = lambda elem : elem[0][1] and elem[1][1] and (parents.append(elem[0]) or childrens.append(elem[1]))
	genRelations(elementmap, elementgen, query)	
	logging.info(parents)
	logging.info(childrens)
	data = pairs2TreeWithCatalog(parents, childrens)
	if isjson:
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		viewstyle = "height:100%"
		return render(request, 'jsmind/grapdep.html', context = {'viewstyle':viewstyle, 'data':json.dumps(data), 'userinfo':userinfo})
		
@auth
def viz(request, userinfo):
	viewstyle = "height:100%"
	isjson = request.GET.get('isjson', False)
	catalog = request.GET.get('catalog', "")
	repo = request.GET.get('repo','sys')
	query = request.GET.get('query',"""
							SELECT ?s ?p ?o {
								?s  ?p  ?o;}
							""")
	print [catalog, repo, query]
	agraph.repoOpen(catalog, repo)
	
	parents ,childrens= ([],[])
	elementmap = lambda elem : (uri2name(elem,"s"), uri2name(elem,"o"))
	elementgen = lambda elem : elem[0][1] and elem[1][1] and (parents.append(elem[0]) or childrens.append(elem[1]))
	genRelations(elementmap, elementgen, query)	
	logging.info(parents)
	logging.info(childrens)
	data = treeWithCatalog2dot(parents, childrens)
	
	if isjson:
		return HttpResponse(data, content_type="application/json")
	else:
		viewstyle = "height:100%"
		return render(request, 'jsmind/viz.html', context = {'viewstyle':viewstyle, 'data':data, 'userinfo':userinfo})
@auth
def showclass(request, userinfo):
	return render(request, 'jsmind/showclass/showobj.html')

		
@auth
def cal(request, userinfo):
	exe = Execute([('Public', 'D:/pythonLib/public.owl'),('Module','D:/pythonLib/module.owl')])
	cal = request.POST.getlist('cals[]',[])
	scope = {'request':request, 'userinfo':userinfo, 'user':request.user}
	scope.update(default_scope_func)
	
	if not len(cal):
		cal_bs64 = request.POST.get('cals',request.GET.get('cals',""))
		cal_str = str(base64.b64decode(cal_bs64),encoding = "utf-8")
		print(cal_str)
		cal = json.loads(cal_str)
	print('................',cal,'................')
	exe.execute("\n".join(cal), scope)
	print(scope['data'])
	if 'data_type' in scope:
		print(scope['data_type'])
		return HttpResponse(scope['data'], content_type=scope['data_type'])#"application/json"
	else:
		return scope['data']
		
@auth
def call(request, userinfo):
	scope = {'request':request, 'userinfo':userinfo, 'user':request.user}
	scope.update(default_scope_func)
	
	path = parse.unquote(request.POST.get('path',request.GET.get('path',"")))
	args_base64 = parse.unquote(request.POST.get('args',request.GET.get('args',"")))
	exe = Execute([('Public', 'D:/pythonLib/public.owl'),('Module','D:/pythonLib/module.owl'),('callmodule', path)])
	args = str(base64.b64decode(args_base64),encoding = "utf-8")
	print('---------------', path,args,'---------------')
	exe.execute('self.ontos["callmodule"].'+args, scope)
	print(scope['data'])
	if 'data_type' in scope:
		print(scope['data_type'])
		return HttpResponse(scope['data'], content_type=scope['data_type'])#"application/json"
	else:
		return scope['data']
		
@auth
def edit(request, userinfo):

	catalog = request.GET.get('catalog', "")
	repo = request.GET.get('repo',"owl")
	lang = request.GET.get('lang', "zh")
	relation = request.GET.get('rel', "?p")

	agraph.repoOpen(catalog, repo)
	query_lang = """
	SELECT ?s ?o ?sName ?oName WHERE {
		?s  %s  ?o;
			rdfs:label ?sName FILTER (lang(?sName) = "%s").
		?o rdfs:label ?oName FILTER (lang(?oName) = "%s")
	}"""%(relation, lang, lang)

	
	#query ="""
	#	SELECT ?s ?o ?sName ?oName WHERE {
	#		?s  %s  ?o;
	#			rdfs:label ?sName.
	#		?o rdfs:label ?oName 
	#	}"""%relation	
		
		
	query ="""
		SELECT ?s ?o  WHERE {
			?s  %s  ?o;
		}"""%relation	
	
	elementmap = lambda elem : (uri2name(elem,"s"), uri2name(elem,"o"))
	elementgen = lambda elem : elem[0][1] and elem[1][1] and parents.append(elem[0][0] + ':"%s"'%elem[0][1]) or childrens.append(elem[1][0] + ':"%s"'%elem[1][1])

	parents ,childrens,roots = ([],[],[])
	#genRelations(elementmap, elementgen, query_lang)	
	len(parents) or genRelations(elementmap, elementgen, query)
	
	logging.info(parents)
	logging.info(childrens)
	print("get data",parents)
	
	data = pairs2Tree(parents, childrens, name="topic")
	
	temp = {}
	#extendChild = lambda data, i :  temp.update(data['children'][i]) or data['children'].__setitem__(i, {}) or data['children'][i].update(temp)
	data = json.loads(json.dumps(data)) #to split the same node to more.
	
	updateid = lambda data,id : data.update({'id':"%s%s"%(data['topic'],id)}) or (data.has_key('children') and [updateid(data['children'][i], data['id']) for i in xrange(len(data['children']))]) 
	updateid(data,'0')
	
	#logging.info(data)
	return render(request, 'jsmind/jsmind.html', context = {'userinfo':userinfo,'data':json.dumps(data)})

	
@auth
def getcenter(request, auth):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		id = request.POST.get('type_id')
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")

#create a relationship
@auth
def rel_create(request, userinfo):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		request.POST.get('start')
		request.POST.get('end')
		
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")
		
#delete a relationship  should build a forget mechanism don't delte the data immedaitally
@auth
def rel_del(request, userinfo):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		id = request.POST.get('type_id')
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")		
		
@auth
def node_create(request, userinfo):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		id = request.POST.get('type_id')
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")
		
@auth
def node_delete(request, userinfo):
	if request.is_ajax():
		rsp = {'errorcode': 100, 'detail': 'Get success'}
		id = request.POST.get('type_id')
		return HttpResponse(json.dumps(rsp), content_type="application/json")
	else:
		return HttpResponse("error")