# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Relation, Entity, Edge
from users.models import User
rootuser = User.objects.get(username = "root")
@Relation.define
class ConsturctRelation(Relation):
	name = "_construct"
	call = "constrcut"
	called = "constructed"
	author = rootuser

@Relation.define
class ClassfiyRelation(Relation):
	name = "_classfiy"
	call = "classified"
	called = "cotian"
	author = rootuser
@Relation.define
class SameWords(Relation):
	name = "_soundlike"
	call = "_soundlike"
	called = "_soundlike"
	author = rootuser
	
@Entity.define
class Things(Entity):
	name = "_things"
	author = rootuser

