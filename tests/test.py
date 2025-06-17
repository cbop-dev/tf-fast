import pytest, os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from app import app

@pytest.fixture()
def theSetup():
    app = app()
    #lexes = app.getLexemes(sections=[1])

mylog("hello")