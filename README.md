# tf-fast

## Description

A python [FastAPI](https://fastapi.tiangolo.com/) service handling some HTTP REST requests for Text-Fabric datasets. (This was ported from an earlier version, [tf-flask](https://github.com/cbop-dev/tf-flask), which used [Flask](https://flask.palletsprojects.com).)

It currently handles a limited set of queries for versions of BHS, LXX, the Greek NT (SBL Greek NT and Nestle's 1904 edition).
See [text-fabric](https://github.com/annotation/text-fabric) for information on the underlying data platform, and [ETCBC/bhsa](https://etcbc.github.io/bhsa/) (also on [github](https://github.com/ETCBC/bhsa)), [CBLC/LXX](https://github.com/CenterBLC/LXX), and [CBLC/N1904](https://github.com/CenterBLC/N1904) for info on the datasets here employed.

This is a work in progress. 

## Examples

### Text of a node

The server will return the text of a given TF node, at `http://localhost:8000/<db>/text/<node-id>`, where `<db>` is either `bhsa`, `lxx`, or `nt` and `<node-id>` is the numeral id of a given node in that dataset. E.g., a fetch request at `http://localhost:8000/nt/text/382716` will return the following json object (for Matt 1:3):

```
{
  "id": 382716,
  "section": "Matthew 1 3",
  "text": "Ἰούδας δὲ ἐγέννησεν τὸν Φαρὲς καὶ τὸν Ζαρὰ ἐκ τῆς Θάμαρ, Φαρὲς δὲ ἐγέννησεν τὸν Ἐσρώμ, Ἐσρὼμ δὲ ἐγέννησεν τὸν Ἀράμ,",
  "type": "verse"
}
```

### Texts Post Request

Request several texts at once, and get lexical data using `options.lexemes` with either `refs` or `sections` with a `POST` request body to `http://localhost:8000/nt/texts` like the following:

```
 {
	'refs': [
		('Matthew',1,[1])
	],
	'options':{
		'lexemes': True
	}
},
```
Server JSON reponse:

```
{
	'texts': [
		'Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ.'
	], 
	'lexemes': {
		'βίβλος': {'id': 962, 'count': 1}, 
		'γένεσις': {'id': 1063, 'count': 1}, 
		'Ἰησοῦς': {'id': 2382, 'count': 1}, 
		'Χριστός': {'id': 5320, 'count': 1}, 
		'υἱός': {'id': 4989, 'count': 2}, 
		'Δαυίδ': {'id': 1144, 'count': 1}, 
		'Ἀβραάμ': {'id': 9, 'count': 1}
	}, 
	'words': [
		[	{'word': 'Βίβλος', 'id': 962}, 
			{'word': 'γενέσεως', 'id': 1063}, 
			{'word': 'Ἰησοῦ', 'id': 2382}, 
			{'word': 'Χριστοῦ', 'id': 5320}, 
			{'word': 'υἱοῦ', 'id': 4989}, 
			{'word': 'Δαυεὶδ', 'id': 1144}, 
			{'word': 'υἱοῦ', 'id': 4989}, 
			{'word': 'Ἀβραάμ.', 'id': 9}
		]
	]
}
```

See main.py for various url-paths and types of responses. 

## Requirements

* python3.13+
* python3.13-venv
* pip 25.1+
* Disk space: 600GB-1TB (for TF installation and datasets)
* RAM: if all the datasets are enabled (especially BHS), the service uses around 6-7 GB of RAM. Thus, the server needs at least 12 GB RAM to run smoothly; 16 GB minimum recommended.

### Packages installed automatically

When installing (see below), the following packages will automatically be installed in the local tf-fast project directory:

* wordcloud
* fastapi[standard]
* text-fabric[github]
* pytest
* httpx
* gunicorn
* uvicorn

## Installation

	git clone https://github.com/cbop-dev/tf-fast.git
	cd tf-fast
	python3 -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt

	# run development server (defaults to http://localhost:8000):
	## old: fastapi dev tffast/main.py
	##new:
	# development run:
	APP_ENV=dev gunicorn -c gunicorn_conf.py #edit this first and customize as needed

	# or more explictly on command line
	gunicorn tffast.main:app -w 3 -k uvicorn.workers.UvicornWorker --preload
	
	## or run on custom port (e.g., 5000):
	# gunicorn tffast.main:app -w 3 -k uvicorn.workers.UvicornWorker --preload --bind 0.0.0.0:5000

	#production run (mutatis mutandis, as above)
	gunicorn -c gunicorn_conf.py 


If all goes well, create, enable, and start a systemd service! 

## TO DO:

- [X] Enable BHSa
- [X] Added Vulgate and an English bible (World English Bible, Catholic Edition)
- [ ] Update this README (on-going: last updated 3 March 2026)
- [ ] Documentation of routes and usage
- [ ] extending/testing `/texts/` route 
- [ ] more (and major) refactoring...
- [ ] More awesome stuff!
