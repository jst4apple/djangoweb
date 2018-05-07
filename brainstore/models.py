# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from users.models import User

class Node(models.Model):
	author = models.ForeignKey(User)
	name = models.CharField(max_length=64)
	relastioncache = []
	def __str__(self):			  # __unicode__ on Python 2
		return self.name
		
class Edge(models.Model):
	author = models.ForeignKey(User)
	name = models.CharField(max_length=64)
	call  = models.CharField(max_length=64)
	called = models.CharField(max_length=64)
	def __str__(self):			  # __unicode__ on Python 2
		return self.name
		
class Connect(models.Model):
	author = models.ForeignKey(User)
	entitystart = models.ForeignKey(Node, related_name = 'node_start')
	entityend = models.ForeignKey(Node, related_name = 'node_end')
	edge = models.ForeignKey(Edge)
	def __str__(self):			  # __unicode__ on Python 2
		return self.entitystart + ":" + self.entityend+ ":" + self.edge
		


#class RelationInfo:
#	@classmethod
#	def define(cls, author):
#		return Edge.objects.get_or_create(author = author, name = cls.name)
#	
#	@classmethod	
#	def search(cls, author):
#		return Edge.objects.get(author = author, name = cls.name)
		
class Relation:
	@staticmethod
	def define(cls):
		cls.edge = Edge.objects.get_or_create(author = cls.author, name = cls.name, call = cls.call, called = cls.called)
		
	@classmethod
	def connect(cls, author, entitystart, entityend):
		con = Connect(author = author, entitystart = entitystart, entityend = entityend, attr=cls.edge)
		con.save()
		
	@classmethod
	def search_down(cls,author, entity):
		queryset = Connect().objects.filter(entitystart = entity, attr=cls.edge, author = author)
	
	@classmethod
	def search_up(cls, author, entity):
		queryset = Connect().objects.filter(entityend = entity, attr=cls.edge,author = author)
	
	
class Entity:
	@staticmethod
	def define(cls):
		return Node.objects.get_or_create(author = cls.author, name = cls.name)
	
	@classmethod	
	def search(cls, author):
		return Node.objects.get(author = author , name = cls.name)

