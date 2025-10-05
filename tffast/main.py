import sys, os
from collections import namedtuple
from .env import mylog, debug
from pathlib import Path
from tf.app import use
from tf.advanced import sections

from fastapi import Depends, FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from wordcloud import WordCloud, STOPWORDS

from .tfData.tfLXX import TfLXX
from .tfData.tfDataset import TfDataset
from .tfData.tfNT import TfN1904
from .tfData.tfBHS import TfBHS
from .env import mylog, debug
#debugOn=debug
#debugOn=True
#debug = True

mylog("LOADING APP!!!========================")
mylog("--------------DEBUGGING ON--------------")
posDict = TfLXX.posDict
posGroups =TfLXX.posGroups
tfLxxBooksDict=TfLXX.booksDict

theBooksDict = tfLxxBooksDict
enableLXX=True
enableNT=True
enableBHS=True
#debug = True
LXX = None
BHS=None
NT = None
theDB = None
if (enableLXX):
	LXX = TfLXX()

if (enableBHS):
	from .tfData.tfBHS import TfBHS
	bhsPosGroups=TfBHS.posGroups
	bhsPosDict=TfBHS.posDict
	tfBHSBooksDict=TfBHS.booksDict
	BHS=TfBHS()
	bhsA = BHS.api
	theDB = BHS
	theBooksDict=BHS.booksDict

if (enableNT):
	from .tfData import tfNT
	NT=TfN1904()
	NTa = NT.api
	theDB = NT
	theBooksDict=NT.booksDict
mylog(f"about to load LXX. Python version: {sys.version}")


datapath="CenterBLC/LXX"
version="1935"

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{db}/lex/common/")
@app.get("/lex/common/")
def getCommonRoute(db='lxx'):
	return ''

@app.get("/{db}/lex/{lexid}")
@app.get("/lex/{lexid}")
def getLexInfo(lexid: int,db='lxx'):
	tf=getAPI(db)
	api=tf.api
	lexid=int(lexid)
	lex=tf.TfData.getLex(lexid)
	if (lex):
		theLexObj = {'id': lexid}
		theLexObj['total'] = lex.total
		theLexObj['gloss'] = lex.gloss
		theLexObj['beta']=lex.beta

		if (db == 'lxx'):
		
			theLexObj['greek'] = lex.lemma
			theLexObj['pos'] = lex.pos if lex.pos else 'proper noun or name'
		elif (enableBHS and  db == 'bhs'):
		
			theLexObj['hebrew'] = lex.lemma
			theLexObj['hebrew_plain'] = lex.plain
			theLexObj['pos'] = lex.pos
		
		return theLexObj

	else:
		return ''


@app.get("/bhs/test")
def bhsTest():
	return "Hello BHS World!"

@app.get("/{db}/lex/freq/{lexid}")
@app.get("/lex/freq/{lexid}")
def getLexCount(lex: int, db='lxx'):
	
	if (db == 'lxx'):
		return LXX.api.F.freq_lemma.v(lexid)
	elif (enableBHS and db == 'bhs'):
		mylog("db == bhs...")
		count = str(bhsA.F.freq_lex.v(lexid))
		mylog("count: " + count)
		return count

@app.get("/{db}/wordcloud")
@app.get("/wordcloud")
def wordCloudRoute(db='lxx',restrict='',invert='',title='',sections='',exclude='',pos='',maxWords='0'):
	
	theLexemesResp=lexemesRoute(db,restrict=restrict,exclude=exclude,pos='',sections=sections)
	theLexemes=theLexemesResp['lexemes']
	response = ''	

	if (theLexemes.values()):
		filteredLexemes= {}
		if (not 'gloss' in list(theLexemes.values())[0].keys()):
			filteredLexemes = {k:int(v['count']) for (k,v) in theLexemes.items()}
			#mylog("Wait! no glosses??")
		else:
			#filteredLexemes = {v['gloss'].split(";")[0].strip():int(v['count'])
			#	for (k,v) in sorted(theLexemes.items(),key=lambda i:i[1]['count'],reverse=True) if not (v['gloss'].split(";")[0].strip() in filteredLexemes)}
			for (k,v) in sorted(theLexemes.items(),key=lambda i:i[1]['count'],reverse=True):
				engGloss=v['gloss'].split(";")[0].strip()
				if not (engGloss in filteredLexemes.keys()):
					filteredLexemes[engGloss]=v['count']

		
		#mylog({l:v for (l,v) in filteredLexemes.items() if 'lord' in l or 'God' in l})
		title=''
		if(invert):
			for (k,v) in filteredLexemes.items():
				filteredLexemes[k]=-filteredLexemes[k]

		if (title and sections):
		
			titles = []
			if(sections):
				sections=sections.split(',')
				titles = titles + [str(sectionFromNode(int(s))) for s in sections if int(s) > 0]
		
			title = consolidateBibleRefs(titles)
		#	mylog("title: " + title)
		
		
		if(maxWords):
			response=Response(genWordCloudSVG(filteredLexemes,title=title,maxWords=int(maxWords)), media_type='image/svg+xml')
		else:
			response=Response(genWordCloudSVG(filteredLexemes,title=title), media_type='image/svg+xml')
	else:
		the404 = {":-(":15,"404":25, "try again!":10,"formless":3, "void": 2 }
		response=Response(genWordCloudSVG(the404), media_type='image/svg+xml')
		
	return response

@app.get("/{db}/lex")
@app.get("/lex")
def lexemesRoute(db='lxx',proper='',sections='',restrict='',exclude='',pos='',beta='',plain='',common='',groups='',min='',gloss='',):
	tf=getAPI(db)
	api=tf.api
	theDicts=getDicts(db)
	checkProper =  True if proper != 'false' else False
	#mylog("lex route: checkProper = " + str(checkProper))
	#sections = sections if sections else []
	#if(sections and len(sections > 0 )):
	#	mylog("Have sections: " + sections)
	#	sections = [int(s) for s in sections.split(',')]
	sections = [int(s) for s in sections.split(',')] if (sections) else []
	restrictParamsList= restrict.split(',') if (restrict) else []
	excludeParamsList= exclude.split(',') if (exclude) else []
	pos = True if pos else False
	beta = True if beta else True
	plain = True if plain else False
	common = True if common else False
	#if (common):
#		mylog("using common flag...")
	restrictedIds=set([int(x) for x in restrictParamsList if x.isdigit()])

	for (abbrev,iArray) in theDicts['groups'].items():
		if (abbrev in restrictParamsList):
			restrictedIds.update(theDicts['groups'][abbrev])
			#restrictedIds.remove(abbrev)
	mylog("restrictedIds: " + str(restrictedIds))

	excludedIds=set([int(x) for x in excludeParamsList if x.isdigit()])
	for (abbrev,iArray) in theDicts['groups'].items():
		if (abbrev in excludeParamsList):
			excludedIds.update(theDicts['groups'][abbrev])
	mylog("excludedIds: " + str(excludedIds))

	min = min if ( min) else 1
	gloss = True if ( gloss and int(gloss) != 0) else False
	#mylog("Gloss: " + str(gloss))
	#mylog("calling getLexemes with common = " + str(common))
	returnObject= tf.TfData.getLexemes2(sections=sections, restrict=list(restrictedIds), 
						exclude=list(excludedIds), min=int(min), gloss=gloss,pos=pos,checkProper=checkProper, 
						beta=beta, common=common,plain=plain)
	#mylog("getLexemes about to return with common value of: [" + ",".join(returnObject['common']) + "]")
	return returnObject

@app.get("/chapters/")
@app.get("/{db}/chapters/")
def allChaptersRoute(db='lxx'):
	tf=getAPI(db)
	api=tf.api
	booksChaps={}
	#booksDict = tfLxxBooksDict
	
	if (enableBHS and db == 'bhs'):
		booksDict = tfBHSBooksDict
	
	for bid in theBooksDict.keys():
		booksChaps[bid]=getChaptersDict(bid, db)
	
	return booksChaps

@app.get("/{db}/chapters/{book}")
@app.get("/chapters/{book}")
def chaptersRoute(book: int, db='lxx'):
	return getChaptersDict(book, db)

@app.get("/{db}/books")
@app.get("/books")
def booksRoute(db='lxx'):
	return getBooksDict(db)

@app.get("/{db}/getrefs/{id}")
@app.get("/getrefs/{id}")
def getrefsRoute(id: int, db='lxx',sections='',detail=''):

	return getLexRefs(id, db,sections,detail)

@app.get("/{db}/words/{id}")
@app.get("/words/{id}")
def getWords(id,db='lxx',features=''):
	tf=getAPI(db)
	api=tf.api
	if (not features):
		try:
			words = [{'id': w, 'text': getText(w,db),'lemma': tf.getLemma(w)} for w in api.L.d(id) if api.F.otype.v(w) == 'word']
		except:
			words = []
	else:
#		features = ['sp','gn','tense','mood']
		words = [{'id': w, 'text': getText(w,db),'lemma': tf.getLemma(w),
			'features': {'pos':api.F.sp.v(w)}} for w in api.L.d(id) if api.F.otype.v(w) == 'word']
		for w in words:
			if (api.F.sp.v(w['id']) == "verb"):
				w['features']['tense'] = api.F.tense.v(w['id'])
		
	return words

@app.get("/{db}/text/{id:int}")
@app.get("/text/{id:int}")
def textRoute(id,db='lxx'):
	tf=getAPI(db)
	api=tf.api
	return {'section': getRef(id,db), 'text': getText(id,db), 'id':int(id), 
	'type': api.F.otype.v(int(id))} if api else ''

class Word(BaseModel):
	word:str
	id:int=0

class VerseWords(BaseModel):
	verse: int
	words: list[Word]

class TextAndReference(BaseModel):
	text: str
	reference: str
	words: list[VerseWords]=[]

class TextReference(BaseModel):
	book:str
	chapter: int
	verses: list[int]
class TextsOptions(BaseModel):
	showVerses:bool=False
	lexemes:bool=False

class TextsRequest(BaseModel):
	refs: list[TextReference]|None =None# book name, chapter, verses
	sections: list[int] |None = None
	options: TextsOptions =TextsOptions()
class TextsResponse(BaseModel):
	texts: list[TextAndReference]
@app.post("/texts")
@app.post("/{db}/texts")
@app.post("/texts/")
@app.post("/{db}/texts/")
def postTextsRoute(request: TextsRequest, db='lxx'):
	mylog("postTextsRoute", debugOn=True, showTime=True)
	texts = list()
	tfAPI = getAPI(db)

	showVerses= request.options.showVerses
	getLexemes = request.options.lexemes
	mylog('postTextsRoute. request.refs = ' + str(request))
	mylog('postTextsRoute. request.refs = ' + str(request.refs))
	mylog("postTextsRoute. request.options: ")
	mylog(request.options)
	mylog("postTextsRoute: getLexemes=" + str(getLexemes))
	lexemes = dict() # dict[lemma:str,dict{id:int,count:int}]
	wordsArray= list() # list[{'id':int,'word':str,'pos':str,...}]
	mylog("postTextsRoute. showVerses = " + str(showVerses))
	textsAndRefsResponse=list()#TextAndReference
	if request.refs:
		
		for ref in request.refs:
			refString=ref.book + ' ' + str(ref.chapter) + ":" + ",".join(map(str,ref.verses))
			text=''
			nodes = list()
			words = list()
			firstVerse = True
		
			for v in ref.verses:
				
				#mylog(f"postTextsRoute verse loop for {str(r[0])} {str(r[1])}:[{','.join(map(str,r[2]))}]")
				node=tfAPI.TfData.getNodeFromBcV(ref.book,ref.chapter,v)## book, chap, verse
					
				textToAdd = tfAPI.TfData.getText(node)
				if (getLexemes and len(textToAdd) > 0):
					nodes.append(node)

				
				#mylog("textToAdd = '" + textToAdd + "'; showVerses = " +str(showVerses))
				if (len(textToAdd) > 0 and showVerses):
					#mylog("ADDING VERSE:"+ str(v))
					if (not firstVerse):
						text+= ' '
					#else:
					#	text+='FIRST VERSE!!:'
					text+='('+str(v)+') '
				text+= textToAdd
				firstVerse = False
			verses=list()
			if (getLexemes):
			#add all section lexemes to response 'lexemes' dictionary:
				mylog("postTextsRoute: getting Lexemes...",debugOn=True,showTime=True)
				
				for n in nodes:
					v=tfAPI.TfData.getVerseNumberFromNode(n)
					verseData={'verse':v, 'words':[]}
					for w in tfAPI.api.L.d(n):
						if tfAPI.api.F.otype.v(w) == 'word':					
							word=tfAPI.TfData.getText(w)
							lemma=tfAPI.api.F.lemma.v(w)
							id=tfAPI.TfData.lexemes[lemma].id
							beta=tfAPI.TfData.lexemes[lemma].beta
							verseData['words'].append({'word':word,'id':id })
							if (lemma not in lexemes.keys()):
								lexemes[lemma]={'id':id,'count':1}
							else:
								lexemes[lemma]['count']+=1
					verses.append(verseData)
			
			txtRef = TextAndReference(text=text,reference=refString,words=verses)
			
			textsAndRefsResponse.append(txtRef)
		mylog("postTextsRoute, @ end of refs loop:", debugOn=True, showTime=True)	
	elif request.sections:
		#firstNode = True

		if (getLexemes):
			mylog("postTextsRoute: getting Lexemes from sections...")
			sectionsLexemes=tfAPI.TfData.getLexemes2(sections=request.sections)
			mylog("postTextsRoute sectionsLexemes = ")
			mylog(sectionsLexemes)
			for l in sectionsLexemes['lexemes'].items():
				lemma = l[0]
				lemmaInfo= l[1] # dict[id,count,beta]
				if l[0] not in lexemes.keys():
					lexemes[lemma]={'id': lemmaInfo['id'],'count':lemmaInfo['count']} 
		
		for node in request.sections:
			#words=list()
			verses=list()
			curVerse={'verse':0, 'words':list()}
			sectRef = tfAPI.api.T.sectionFromNode(node)
			if(len(sectRef)==3):
				v=sectRef[2]
				curVerse['verse']=v

			refString = sectRef[0]
			if(len(sectRef) > 1):
				refString += ' ' +str(sectRef[1])
				if(len(sectRef) > 2):
					refString += ':' + str(sectRef[2])
			textToAdd = tfAPI.TfData.getText(node)
			text=''
			if(showVerses and textToAdd and (tfAPI.api.F.otype.v(node) == 'verse')):
				sect = tfAPI.api.T.sectionFromNode(node)
				if (len(sect)==3):
					text+= '('+str(sect[2])+') '
			if (getLexemes):
				curVerse['words'].extend([{'word':tfAPI.TfData.getText(w),'id':lexemes[tfAPI.getLemma(w)]['id']} for w in tfAPI.api.L.d(node) if tfAPI.api.F.otype.v(w) == 'word'])
			text+=textToAdd
			txtRef = TextAndReference(text=text,reference=refString,words=[curVerse])
			textsAndRefsResponse.append(txtRef)
			
	retObj= dict()
	retObj['texts']=textsAndRefsResponse
	if (getLexemes):
		retObj['lexemes']=lexemes
		#retObj['words']=wordsArray
	mylog("postTextsRoute finishing.", debugOn=True, showTime=True)
	return retObj

@app.get("/texts/")
@app.get("/{db}/texts/")
def textsRoute(db='lxx',sections='',refs=''):
	tf=getAPI(db)
	api=tf.api
	texts = []
	if(api):
		
		#refs=[]
		ids=sections.split(",")
		if not len(ids):
			refs=refs.split(";")
		try:
			for id in ids:
				texts.append({'section':getRef(id,db), 'text':getText(id,db), 'id': int(id)})
		except:
			texts=[]
	return texts

@app.get("/{db}/node")
@app.get("/node")
def getNodeFromRefRoute(db='lxx',book='',chapter='',verse=''):
	tf=getAPI(db)
	api=tf.api
	node = 0
	if(api):
		

		if (book and len(book) > 0):
			ref = book + " " + chapter if chapter and len(chapter) > 0 else book
			ref += ":" + verse if chapter and len(chapter) > 0 and verse and len(verse) > 0 else ''
			if (db=='lxx'):
				theDB=LXX
			elif(db=='bhs'):
				theDB=BHS
			elif(db=='nt'):
				theDB=NT
			mylog("getNodeFromRefRoute calling nodeFromSectionStr with ref=" + ref)
			secs = sections.nodeFromSectionStr(tf.TfData.dataset,ref)

			if ((type(secs) is int) and secs > 0):
				node = secs

	return str(node)

@app.get("/{db}/verses")
@app.get("/verses")
def getVersesFromRange(db='lxx',book='',chapter='',showVerses='0',start='',end=''):
	tf=getAPI(db)
	api=tf.api
	
	if(api):
		book = book.strip()
		chapter = chapter.strip()
		showVerses = True if showVerses == '1' or showVerses == "true" else False
		if (showVerses == '0'):
			showVerses = False
		if (len(chapter) > 0):
			chapter = int(chapter)

		startVerse = start.strip()
		if (len(startVerse) > 0):
			startVerse = int(startVerse)
		endVerse = end.strip()
		
		if (len(endVerse) > 0):
			endVerse = int(endVerse)

		verses = ''
		startNode = getNodeFromBcV(book,chapter,startVerse,db)
		endNode = getNodeFromBcV(book,chapter,endVerse,db)
		ref = ''
		if (startNode == 0  and endNode == 0):
			mylog("got nothing")
		else:
			if ((startNode == 0 or startNode == None) and (endNode != 0 and endNode != None)):
				mylog(f"got end node {endNode} but no start node! trying to fix...")
				for i in range(startVerse + 1,endVerse+1, 1):
					if (startNode == None):
						startNode = getNodeFromBcV(book,chapter,i,db)
			
			if ((endNode == 0 or endNode == None) and (startNode != None and startNode != 0)):
				mylog(f"got start node {startNode} but no end node! trying to fix with range:")
				for i in range(endVerse-1, startVerse-1, -1):
					if (endNode == 0 or endNode == None):
						endNode = getNodeFromBcV(book,chapter,i,db)
			if (startNode != None and endNode != None and startNode > 0 and endNode > 0 and endNode >= startNode):
				verses = getVersesFromNodeRange(startNode,endNode,showVerses,db)
				mylog("calling getVersesFromNodeRange("+str(startNode)+","+str(endNode)+")")
				start = api.T.sectionFromNode(startNode)
				if (startNode < endNode):
					ref = start[0] + " " + str(start[1]) +":"+str(start[2])+"-"+str(api.T.sectionFromNode(endNode)[-1])
				else:
					ref = start[0] + " " + str(start[1]) +":"+str(start[2])
			else:
				mylog("got no nodes from range!")
			
	return {'text': verses, 'reference': ref} if verses and ref else {}
	
@app.get("/{db}/verses/")
@app.post("/{db}/verses/")
def getVersesPost(db='lxx'):
	return request.form['chapters'] if request.form['chapters'] else ''

@app.get("/{db}/verse")
@app.get("/verse")
def getVerse(db='lxx',book='',chapter='',verse=''):
	tf=getAPI(db)
	api=tf.api
	if(api):
		book = book.strip()
		chapter = int(chapter.strip())
		verse = int(verse.strip())
		ref = ''
		node = getNodeFromBcV(book,chapter,verse,db)
		mylog("getVerse url calling getNodeFromBcV("+ ",".join([book,str(chapter),str(verse)])+")")
		mylog("got node " + str(node))
		if ((type(int(node)) == int) and int(node) > 0):
			text = getText(node,db)
			mylog("Go text:'"+text+"' for node " + str(node))
			sec = api.T.sectionFromNode(node)
			ref = sec[0] + " "
			if (sec[1] > 0):
				ref += str(sec[1])
				if (sec[2] > 0):
					ref += ":" + str(sec[2])
		else:
			text = ''

		
	return {'text': text, 'reference': ref} if text and ref else {}
	
################################
# non-route functions:         #

def getVersesFromNodeRange(startNode,endNode,showVerses=False,db='lxx'):
	text = ''
	mylog("getVersesFromNodeRange(" +str(startNode) + ","+str(endNode)+")")
	tf=getAPI(db)
	api=tf.api
	if(api):
		if (startNode == endNode):
			text += api.T.text(startNode)
			mylog("	got single node; text= " + text)
		elif (startNode > 0 and endNode >= startNode):
			onFirstNode = True
			for i in range(startNode,endNode+1,1):
				if(api.F.otype.v(i) =='verse'):
					if(showVerses):
						sec=api.T.sectionFromNode(i)
						if (sec[2]):
							if(not onFirstNode):
								text+=''
							text+= '('+str(sec[2])+') '
					text += api.T.text(i)
				else:
					mylog("Node " + str(i) + " was not a verse, but is: " + api.F.otype.v(i) +", text = " + api.T.text(i))
				onFirstNode=False
			mylog("	got range. text = " + text)

	return text.strip()

# returns refs as {'refs': <string array>, 'nodes': <int array of verses>, 'bookCounts': <dict of booksids->count>, 'total', <total instances in BHS>}
def getLexRefs(id,db='lxx',sections='',detail=''):
	tf=getAPI(db)
	#tf.TfData
	api=tf.api
	if(api):
		# optionally limits to instances within any of the selected sections, exluding all others:
		#NB: this should be lex id, not the node id!!
		id=int(id)
		
		sectionsArray = [int(s) for s in sections.split(',')] if sections else []
		mylog("getrefs: sections = [" + ",".join([str(s) for s in sectionsArray])+"]")
		lex= tf.TfData.getLex(id) 
		if(lex):
			
			rNodes = {}
			bookCounts = {}
			queryDetail = 'verse'
			verseCounts={}
			if (detail):
				if (detail == "book"):
					queryDetail = 'book'
				elif (detail == "chapter"):
					queryDetail = 'chapter'

			#refs = {}
			for n in api.N.walk():
				if (api.F.otype.v(n) == 'word' and tf.getLemma(n) == lex.lemma and (len(sectionsArray) == 0 or (len(set(api.L.u(n)) & set(sectionsArray)) > 0) )):
					sectionTuple= api.T.sectionTuple(n)
					if (queryDetail == 'book'):
						sectionNode = sectionTuple[0]
					elif (queryDetail == 'chapter'):
						sectionNode = sectionTuple[1]
					else:
						sectionNode = sectionTuple[2]

					#rNodes.add(sectionNode) # gets node of containing verse
					refTuple = api.T.sectionFromNode(n) # gets tuple of containing verse
					if (queryDetail == 'book'):
						refString = refTuple[0]
					elif (queryDetail == 'chapter'):
						refString = refTuple[0] + " " + str(refTuple[1])
					else:
						refString = refTuple[0] + " " + ":".join(map(str,refTuple[1:]))
					#refs.add(refString)
					bookid=api.L.u(n)[-1]
					if bookid not in bookCounts:
						bookCounts[bookid]=1
					else:
						bookCounts[bookid] +=1
					if sectionNode not in rNodes:
						rNodes[sectionNode]=refString
						verseCounts[sectionNode]=1
					else:
						verseCounts[sectionNode] +=1
						#rNodes[sectionNode]=refString+"(" + str(verseCounts[sectionNode]) + ")"

			return {'refs': list(rNodes.values()), 'nodes': list(rNodes.keys()), 'bookcounts': dict(bookCounts), 'total': sum(bookCounts.values())}
		else:
			return {}
	else:
		return {}

def getText(nodeId,db='lxx'):
	tf=getAPI(db)
	api=tf.api
	if(api):
		try:
			return api.T.text(int(nodeId)).strip()
		except:
			return ''
	return ''
def getRef(nodeId, db='lxx'):
	tf=getAPI(db)
	api=tf.api
	if(api):
		try:
			return " ".join(map(str, api.T.sectionFromNode(int(nodeId))))
		except:
			return ''
	return ''
def getNodeFromBcV(book,chapter,verse,db='lxx'):
	node = 0
	tf=getAPI(db)
	api=tf.api
	if(api):
		mylog("calling nodeFromSection(" + book + "," + str(chapter) +"," + str(verse)+")")
		
		node=api.T.nodeFromSection((book,int(chapter),int(verse)))
		if (type(node) != int):
			node = 0
		mylog("...got node " + str(node))
	return node
TfAPI=namedtuple('tfAPI', ['api','getLemma','TfData'])
def getAPI(db='lxx'):
	
	api=None
	getLemma=lambda x: ''
	dataSet=None
	if (db=='lxx'):
		api=LXX.api
		getLemma =LXX.getLemma
		theBooksDict=LXX.booksDict
		dataSet=LXX
	elif (enableNT and db=='nt'):
		api=NTa
		getLemma = NT.getLemma
		theBooksDict=NT.booksDict
		dataSet=NT
	elif (enableBHS and db=='bhs'):
		api=BHS.api
		#api.lex= lambda i : api.F.voc_lex_utf8.v(i) if api.F.voc_lex_utf8.v(i) else tf.getLemma(i)
		getLemma=BHS.getLemma
		theBooksDict=tfBHSBooksDict
		dataSet=BHS
		#api.lex =lambda i : api.F.lex_utf8.v(i)
	return TfAPI(api,getLemma,dataSet)

def getDicts(db='lxx'):
	if (db=='lxx'):
		return {'dict': posDict, 'groups': posGroups}
	elif(db=='bhs'):
		return {'dict': bhsPosDict, 'groups': bhsPosGroups}
	else:
		return {'dict':{}, 'groups':{}}

def sectionFromNode(node,db='lxx'):
	tf=getAPI(db)
	api=tf.api
	string=''
	if(api):
		if (enableBHS and db=='bhs'):
			api=BHS.api
		section= api.T.sectionFromNode(node)
		string = ''
		if (len(section) == 3):
			string = str(section[0]) + " " + str(section[1]) + ":" + str(section[2])
		elif (len(section) == 2):
			string = str(section[0]) + " " + str(section[1])
		else:#book only:
			string = str(section[0])
	return string

def consolidateBibleRefs(strings):
	outString = ''
	if(len(strings) > 1):
		bookHash = {}
		for s in strings:
			if (" " in s):
				(book,chapV) = s.split(" ")
				if (book not in bookHash.keys()):
					bookHash[book] = {}#indexed by chaps
				if (":" in chapV):
					(chap, verse) = chapV.split(":")
					if (chap not in bookHash[book].keys()):
						bookHash[book][chap] = [verse]
					else:
						bookHash[book][chap].append(verse)
				else: # no verse given
					if (chapV not in bookHash[book].keys()):
						bookHash[book][chapV] = []
					#else: #chap exists, but no need to add since we don't have a verse
			else: #book only
				if (s not in bookHash.keys()):
					bookHash[s]={}

		#mylog(bookHash)
		
		for (b,cvs) in bookHash.items():
			outString = b + " " if not outString else outString + "; " + b
			cvss = ''
			for (c, vs) in cvs.items():
				if (cvss):
					cvss += "; " + c 
				else:
					cvss += " " + c

				vss = ",".join(vs)
				if (vss):
					cvss += ":" + vss
				
			outString += cvss
			
	else:
		outString = strings[0]
	
	return outString

	

def genWordCloudSVG(freqDataDict, title='',maxWords=200):
	wc = WordCloud(font_path="lib/fonts/SBL_BibLit_Regular.ttf", background_color="white",width=800,height=600, max_words=maxWords)
	wc.generate_from_frequencies(freqDataDict)
	svg = wc.to_svg(embed_font=True)
	
	if(title):
		svg = svg.replace("</svg>",'<text font-size="50" style="text-decoration: underline; font-family: \'Arial\'; font-variant: small-caps; font-weight: bold" transform="translate(149,650)">' + title +'</text></svg>')
		svg = svg.replace('height="600"', 'height="700"')
	return svg


def getChaptersDict(book, db='lxx'):
	mylog("getChapters(" + str(book) + "," + db +")")
	tf = getAPI(db)
	api=tf.api
	theDict=dict()
	if(api):
		theDict= dict([(api.F.chapter.v(c), c) for c in api.L.d(book) if api.F.otype.v(c)=='chapter'])
	return theDict
	
def getBooksDict(db='lxx'):
	tf=getAPI(db)
	api=tf.api
	theDict=dict()
	if(api):
		theDict= dict([(b, api.F.book.v(b)) for b in api.N.walk() if api.F.otype.v(b) == 'book'])
	return theDict


#app = create_app()