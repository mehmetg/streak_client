from pprint import pprint
class StreakBaseObject(object):

	def __init__(self, **kwargs):
		if kwargs:
			print(self.__class__)
			self.attributes = {}
			self.attributes.update(**kwargs)
		else:
			self.attributes = dict.fromkeys(self.__class__.disp_attr_keys)
			

	def show(self, displayAll = False):
		if displayAll:
			pprint(self.attributes)
		else:
			disp_attr = {}
			for key in self.disp_attr_keys:
				try:
					disp_attr[key] = self.attributes[key]
				except KeyError:
					if key == 'lowercaseEmail':
						disp_attr[key] = disp_attr['email'].lower()
					else:
						disp_attr[key] = None
			pprint(disp_attr)

	def to_dict(self, rw = False):
		return {k:v for (k,v) in self.attributes.iteritems() 
				if (v is not None and (not rw or (k in self.rw_attr_keys)))}
class StreakUser(StreakBaseObject):
	disp_attr_keys =	[
						'email',
						'lowercaseEmail',
						'lastSeenTimestamp',
						'isOauthComplete',
						'displayName',
						'userKey'
						]
	rw_attr_keys =		[
						]
class StreakPipeline(StreakBaseObject):
	disp_attr_keys =	[
						'creatorKey',
						'name',
						'description',
						'orgWide',
						'fields',
						'stages',
						'stageOrder',
						'aclEntries',
						'owner',
						'pipelineKey'
						]
	rw_attr_keys =		[
						'name',
						'description',
						'orgWide',
						'stageOrder'
						'owner'
						]

class StreakACLEntry(StreakBaseObject):
	disp_attr_keys =	[
						'fullName',
						'name',
						'email',
						'isOwner',
						'image'
						]
	rw_attr_keys =		[]

class StreakBox(StreakBaseObject):
	disp_attr_keys =	[
						'name',
						'notes',
						'stageKey',
						'fields',
						'followerKeys',
						'boxKey'
						]
	rw_attr_keys =		[
						'name',
						'notes',
						'stageKey',
						'stageOrder',
						'followerKeys'
						]
class StreakStage(StreakBaseObject):
	disp_attr_keys =	[
						'name',
						'key',
						'pipelineKey'
						]
	rw_attr_keys = 		[
						'name'
						]

class StreakField(StreakBaseObject):
	disp_attr_keys =	[
						'name',
						'key',
						'type'
						]
	rw_attr_keys = 		[
						'name',
						'type'
						]

class StreakReminder(StreakBaseObject):
	disp_attr_keys =	[
						'creatorKey',
						'creationDate',
						'remindDate',
						'message',
						'status'
						]
	rw_attr_keys = 		[]

class StreakFile(StreakBaseObject):
	disp_attr_keys =	[
						'fileOwner',
						'size',
						'mimeType',
						'fileName',
						'mainFileName'
						]
	rw_attr_keys = 		[]

class StreakThread(StreakBaseObject):
	disp_attr_keys =	[
						'subject',
						'names',
						'emailAddresses',
						'lastEmailTimestamp',
						'threadGmailId',
						'files',
						'key'
						]
	rw_attr_keys = 		[]

class StreakComment(StreakBaseObject):
	disp_attr_keys =	[
						'pipelineKey',
						'boxKey',
						'message',
						'timestamp',
						'creatorKey'
						'commentKey',
						'key'
						]
	rw_attr_keys = 		[
						'message'
						]

class StreakSnippet(StreakBaseObject):
	disp_attr_keys =	[
						'userKey',
						'creationDate',
						'partOfPipeline',
						'snippetText',
						'snippetName',
						'snippetType',
						'key'
						]
	rw_attr_keys =		[]