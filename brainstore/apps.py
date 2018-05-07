# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from models import Node,Edge

class BrainstoreConfig(AppConfig):
    name = 'brainstore'


class Relations:
	@classmethod
	def connect(cls,entity0,entity1):
		edge = Edge(entity0, entity1, name=cls.name)
		edge.save()
		
	@classmethod
	def search_down(cls, self, entity):
		queryset = Edge().objects.filter(entity0 = entity AND name = cls.name)
	
	@classmethod
	def search_up(cls, self, entity)
		queryset = Edge().objects.filter(entity1 = entity AND name = cls.name)
		
class ConsturctRelation(Relations):
	name = "_construct"
		
class ClassfiyRelation(Relations):
	name = "_classfiy"


class Entity:
	@classmethod
	def define(cls):
		Node.objects.create(name = cls.name)
	
	@classmethod	
	def search(cls):
		Node.objects.get(name = cls.name)

	