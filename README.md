# tf-fast

## Description

A python (FastAPI)[https://fastapi.tiangolo.com/] service handling some HTTP REST requests for Text-Fabric datasets. (This was ported from an earlier version, (tf-flask)[https://github.com/cbop-dev/tf-flask], which used (Flask)[https://flask.palletsprojects.com].)

It currently handles a limited set of queries for versions of BHS, LXX, and the Greek NT (Nestle's 1904 edition).
See text-fabric for information on the underlying data platform, and [ETCBC/bhsa](https://etcbc.github.io/bhsa/) (also on [github](https://github.com/ETCBC/bhsa)), [CBLC/LXX](https://github.com/CenterBLC/LXX), and [CBLC/N1904](https://github.com/CenterBLC/N1904) for info on the datasets here employed.

This is a work in progress. 

## Examples

### Text of a node

The server will return the text of a given TF node, at `http://localhost:5000/<db>/text/<node-id>`, where `<db>` is either `bhsa`, `lxx`, or `nt` and `<node-id>` is the numeral id of a given node in that dataset. E.g., a fetch request at `http://localhost:5000/nt/text/382716` will return the following json object (for Matt 1:3):

```
{
  "id": 382716,
  "section": "Matthew 1 3",
  "text": "Ἰούδας δὲ ἐγέννησεν τὸν Φαρὲς καὶ τὸν Ζαρὰ ἐκ τῆς Θάμαρ, Φαρὲς δὲ ἐγέννησεν τὸν Ἐσρώμ, Ἐσρὼμ δὲ ἐγέννησεν τὸν Ἀράμ,",
  "type": "verse"
}
```

See app.py for various url-paths and types of responses. 

## Requirements

* python3.9+
* pip 25.1+
* Disk space: 600GB-1TB (for TF installation and datasets)

### Package installed automatically

When installing (see below), the following packages will automatically be installed in the local tf-fast project directory:

* pytest
* fastapi[standard]
* httpx
* wordcloud
* text-fabric

## Installation

	git clone https://github.com/cbop-dev/tf-fast.git
	cd tf-fast
	python3 -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt

	# run development server (defaults to http://localhost:8000):
	fastapi dev tffast/main.py

	## change port:
	fastapi dev --port 5000 tffast/main.py

	#production run (change port with `... run --port XXXX ... `):
	fastapi run tffast/main.py

	# try calling from outside of venv:
	deactivate
	.venv/bin/gunicorn -b localhost:5000 app:app


If all goes well, create, enable, and start systemd service. (google it)

## TO DO:

- [ ] Documentation