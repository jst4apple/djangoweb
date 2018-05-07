# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *

connect('jsnode', host='localhost', port=27017)
class UserInfo(Document):
	name = StringField(max_length=16)
	nodecnt = IntField(default=0)
	relatiocnt = IntField(default=0)
	centernode = ReferenceField('Node')

class Base(Document):
	user = ReferenceField(UserInfo)
	name = StringField(max_length=16)
	isabstract = BooleanField()
	meta = {'allow_inheritance': True}

class connect:
	relid = ObjectIdFiled()
	node = ReferenceField('Node')
	
class Node(Base):
	cahe = ListField(EmbeddedDocumentField(connect))

	
class DirectRe(Node):
	start = ReferenceField(Node)
	end = ReferenceField(Node)
	
	cahe = ListField(ReferenceField(Node))
	
class IndirectRe(Node):
	chain = ListField(ReferenceField(DirectRe))

class LikeRe(Node):
	chain = ReferenceField(DirectRe)
	
class InterationRe(Node):
	cnt      = IntField(default=0)
	mincnt   = IntField(default=0)
	relation = ReferenceField(DirectRe)
	
class ClassRelation:
	name = "class"
	def __init__(self, name)
		self.dataset = ClassRelation.dataset
		
	def AddRel(self):
		self.dataset.
		
		
	def GetRel(self):
	
	
	