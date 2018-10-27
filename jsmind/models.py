# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *

import os
import os.path

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
