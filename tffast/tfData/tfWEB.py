import sys, os, re
from tf.app import use
from .tfDataset import TfDataset
from ..env import mylog

class DummyApp:
    def __init__(self, api):
        self.api = api

class TfWEB(TfDataset):
    
    booksDict = {
        1006953: {"name": "GEN", "abbrev": "GEN", "syn": ["GEN", "gen"], "words": 1, "chapters": 1, "lemmas": 0},
        1006954: {"name": "EXO", "abbrev": "EXO", "syn": ["EXO", "exo"], "words": 1, "chapters": 1, "lemmas": 0},
        1006955: {"name": "LEV", "abbrev": "LEV", "syn": ["LEV", "lev"], "words": 1, "chapters": 1, "lemmas": 0},
        1006956: {"name": "NUM", "abbrev": "NUM", "syn": ["NUM", "num"], "words": 1, "chapters": 1, "lemmas": 0},
        1006957: {"name": "DEU", "abbrev": "DEU", "syn": ["DEU", "deu"], "words": 1, "chapters": 1, "lemmas": 0},
        1006958: {"name": "JOS", "abbrev": "JOS", "syn": ["JOS", "jos"], "words": 1, "chapters": 1, "lemmas": 0},
        1006959: {"name": "JDG", "abbrev": "JDG", "syn": ["JDG", "jdg"], "words": 1, "chapters": 1, "lemmas": 0},
        1006960: {"name": "RUT", "abbrev": "RUT", "syn": ["RUT", "rut"], "words": 1, "chapters": 1, "lemmas": 0},
        1006961: {"name": "1SA", "abbrev": "1SA", "syn": ["1SA", "1sa"], "words": 1, "chapters": 1, "lemmas": 0},
        1006962: {"name": "2SA", "abbrev": "2SA", "syn": ["2SA", "2sa"], "words": 1, "chapters": 1, "lemmas": 0},
        1006963: {"name": "1KI", "abbrev": "1KI", "syn": ["1KI", "1ki"], "words": 1, "chapters": 1, "lemmas": 0},
        1006964: {"name": "2KI", "abbrev": "2KI", "syn": ["2KI", "2ki"], "words": 1, "chapters": 1, "lemmas": 0},
        1006965: {"name": "1CH", "abbrev": "1CH", "syn": ["1CH", "1ch"], "words": 1, "chapters": 1, "lemmas": 0},
        1006966: {"name": "2CH", "abbrev": "2CH", "syn": ["2CH", "2ch"], "words": 1, "chapters": 1, "lemmas": 0},
        1006967: {"name": "EZR", "abbrev": "EZR", "syn": ["EZR", "ezr"], "words": 1, "chapters": 1, "lemmas": 0},
        1006968: {"name": "NEH", "abbrev": "NEH", "syn": ["NEH", "neh"], "words": 1, "chapters": 1, "lemmas": 0},
        1006969: {"name": "JOB", "abbrev": "JOB", "syn": ["JOB", "job"], "words": 1, "chapters": 1, "lemmas": 0},
        1006970: {"name": "PSA", "abbrev": "PSA", "syn": ["PSA", "psa"], "words": 1, "chapters": 1, "lemmas": 0},
        1006971: {"name": "PRO", "abbrev": "PRO", "syn": ["PRO", "pro"], "words": 1, "chapters": 1, "lemmas": 0},
        1006972: {"name": "ECC", "abbrev": "ECC", "syn": ["ECC", "ecc"], "words": 1, "chapters": 1, "lemmas": 0},
        1006973: {"name": "SNG", "abbrev": "SNG", "syn": ["SNG", "sng"], "words": 1, "chapters": 1, "lemmas": 0},
        1006974: {"name": "ISA", "abbrev": "ISA", "syn": ["ISA", "isa"], "words": 1, "chapters": 1, "lemmas": 0},
        1006975: {"name": "JER", "abbrev": "JER", "syn": ["JER", "jer"], "words": 1, "chapters": 1, "lemmas": 0},
        1006976: {"name": "LAM", "abbrev": "LAM", "syn": ["LAM", "lam"], "words": 1, "chapters": 1, "lemmas": 0},
        1006977: {"name": "EZK", "abbrev": "EZK", "syn": ["EZK", "ezk"], "words": 1, "chapters": 1, "lemmas": 0},
        1006978: {"name": "HOS", "abbrev": "HOS", "syn": ["HOS", "hos"], "words": 1, "chapters": 1, "lemmas": 0},
        1006979: {"name": "JOL", "abbrev": "JOL", "syn": ["JOL", "jol"], "words": 1, "chapters": 1, "lemmas": 0},
        1006980: {"name": "AMO", "abbrev": "AMO", "syn": ["AMO", "amo"], "words": 1, "chapters": 1, "lemmas": 0},
        1006981: {"name": "OBA", "abbrev": "OBA", "syn": ["OBA", "oba"], "words": 1, "chapters": 1, "lemmas": 0},
        1006982: {"name": "JON", "abbrev": "JON", "syn": ["JON", "jon"], "words": 1, "chapters": 1, "lemmas": 0},
        1006983: {"name": "MIC", "abbrev": "MIC", "syn": ["MIC", "mic"], "words": 1, "chapters": 1, "lemmas": 0},
        1006984: {"name": "NAM", "abbrev": "NAM", "syn": ["NAM", "nam"], "words": 1, "chapters": 1, "lemmas": 0},
        1006985: {"name": "HAB", "abbrev": "HAB", "syn": ["HAB", "hab"], "words": 1, "chapters": 1, "lemmas": 0},
        1006986: {"name": "ZEP", "abbrev": "ZEP", "syn": ["ZEP", "zep"], "words": 1, "chapters": 1, "lemmas": 0},
        1006987: {"name": "HAG", "abbrev": "HAG", "syn": ["HAG", "hag"], "words": 1, "chapters": 1, "lemmas": 0},
        1006988: {"name": "ZEC", "abbrev": "ZEC", "syn": ["ZEC", "zec"], "words": 1, "chapters": 1, "lemmas": 0},
        1006989: {"name": "MAL", "abbrev": "MAL", "syn": ["MAL", "mal"], "words": 1, "chapters": 1, "lemmas": 0},
        1006990: {"name": "TOB", "abbrev": "TOB", "syn": ["TOB", "tob"], "words": 1, "chapters": 1, "lemmas": 0},
        1006991: {"name": "JDT", "abbrev": "JDT", "syn": ["JDT", "jdt"], "words": 1, "chapters": 1, "lemmas": 0},
        1006992: {"name": "ESG", "abbrev": "ESG", "syn": ["ESG", "esg"], "words": 1, "chapters": 1, "lemmas": 0},
        1006993: {"name": "WIS", "abbrev": "WIS", "syn": ["WIS", "wis"], "words": 1, "chapters": 1, "lemmas": 0},
        1006994: {"name": "SIR", "abbrev": "SIR", "syn": ["SIR", "sir"], "words": 1, "chapters": 1, "lemmas": 0},
        1006995: {"name": "BAR", "abbrev": "BAR", "syn": ["BAR", "bar"], "words": 1, "chapters": 1, "lemmas": 0},
        1006996: {"name": "1MA", "abbrev": "1MA", "syn": ["1MA", "1ma"], "words": 1, "chapters": 1, "lemmas": 0},
        1006997: {"name": "2MA", "abbrev": "2MA", "syn": ["2MA", "2ma"], "words": 1, "chapters": 1, "lemmas": 0},
        1006998: {"name": "DAG", "abbrev": "DAG", "syn": ["DAG", "dag"], "words": 1, "chapters": 1, "lemmas": 0},
        1006999: {"name": "Matthew", "abbrev": "Matthew", "syn": ["Matthew", "matthew"], "words": 1, "chapters": 1, "lemmas": 0},
        1007000: {"name": "Mark", "abbrev": "Mark", "syn": ["Mark", "mark"], "words": 1, "chapters": 1, "lemmas": 0},
        1007001: {"name": "Luke", "abbrev": "Luke", "syn": ["Luke", "luke"], "words": 1, "chapters": 1, "lemmas": 0},
        1007002: {"name": "John", "abbrev": "John", "syn": ["John", "john"], "words": 1, "chapters": 1, "lemmas": 0},
        1007003: {"name": "Acts", "abbrev": "Acts", "syn": ["Acts", "acts"], "words": 1, "chapters": 1, "lemmas": 0},
        1007004: {"name": "Romans", "abbrev": "Romans", "syn": ["Romans", "romans"], "words": 1, "chapters": 1, "lemmas": 0},
        1007005: {"name": "1_Corinthians", "abbrev": "1_Corinthians", "syn": ["1_Corinthians", "1_corinthians", "1 Corinthians"], "words": 1, "chapters": 1, "lemmas": 0},
        1007006: {"name": "2_Corinthians", "abbrev": "2_Corinthians", "syn": ["2_Corinthians", "2_corinthians", "2 Corinthians"], "words": 1, "chapters": 1, "lemmas": 0},
        1007007: {"name": "Galatians", "abbrev": "Galatians", "syn": ["Galatians", "galatians"], "words": 1, "chapters": 1, "lemmas": 0},
        1007008: {"name": "Ephesians", "abbrev": "Ephesians", "syn": ["Ephesians", "ephesians"], "words": 1, "chapters": 1, "lemmas": 0},
        1007009: {"name": "Philippians", "abbrev": "Philippians", "syn": ["Philippians", "philippians"], "words": 1, "chapters": 1, "lemmas": 0},
        1007010: {"name": "Colossians", "abbrev": "Colossians", "syn": ["Colossians", "colossians"], "words": 1, "chapters": 1, "lemmas": 0},
        1007011: {"name": "1_Thessalonians", "abbrev": "1_Thessalonians", "syn": ["1_Thessalonians", "1_thessalonians", "1 Thessalonians"], "words": 1, "chapters": 1, "lemmas": 0},
        1007012: {"name": "2_Thessalonians", "abbrev": "2_Thessalonians", "syn": ["2_Thessalonians", "2_thessalonians", "2 Thessalonians"], "words": 1, "chapters": 1, "lemmas": 0},
        1007013: {"name": "1_Timothy", "abbrev": "1_Timothy", "syn": ["1_Timothy", "1_timothy", "1 Timothy"], "words": 1, "chapters": 1, "lemmas": 0},
        1007014: {"name": "2_Timothy", "abbrev": "2_Timothy", "syn": ["2_Timothy", "2_timothy", "2 Timothy"], "words": 1, "chapters": 1, "lemmas": 0},
        1007015: {"name": "Titus", "abbrev": "Titus", "syn": ["Titus", "titus"], "words": 1, "chapters": 1, "lemmas": 0},
        1007016: {"name": "Philemon", "abbrev": "Philemon", "syn": ["Philemon", "philemon"], "words": 1, "chapters": 1, "lemmas": 0},
        1007017: {"name": "Hebrews", "abbrev": "Hebrews", "syn": ["Hebrews", "hebrews"], "words": 1, "chapters": 1, "lemmas": 0},
        1007018: {"name": "James", "abbrev": "James", "syn": ["James", "james"], "words": 1, "chapters": 1, "lemmas": 0},
        1007019: {"name": "1_Peter", "abbrev": "1_Peter", "syn": ["1_Peter", "1_peter", "1 Peter"], "words": 1, "chapters": 1, "lemmas": 0},
        1007020: {"name": "2_Peter", "abbrev": "2_Peter", "syn": ["2_Peter", "2_peter", "2 Peter"], "words": 1, "chapters": 1, "lemmas": 0},
        1007021: {"name": "1_John", "abbrev": "1_John", "syn": ["1_John", "1_john", "1 John"], "words": 1, "chapters": 1, "lemmas": 0},
        1007022: {"name": "2_John", "abbrev": "2_John", "syn": ["2_John", "2_john", "2 John"], "words": 1, "chapters": 1, "lemmas": 0},
        1007023: {"name": "3_John", "abbrev": "3_John", "syn": ["3_John", "3_john", "3 John"], "words": 1, "chapters": 1, "lemmas": 0},
        1007024: {"name": "Jude", "abbrev": "Jude", "syn": ["Jude", "jude"], "words": 1, "chapters": 1, "lemmas": 0},
        1007025: {"name": "Revelation", "abbrev": "Revelation", "syn": ["Revelation", "revelation"], "words": 1, "chapters": 1, "lemmas": 0},
    }

    def __init__(self, dataset=None):
        db="web"
        # Since it's now on GitHub, we can let Text-Fabric resolve it automatically
        
        datasetPathname = "cbop-dev/tf-web-c"
            
        self.booksDict = TfWEB.booksDict
        self.dbname=db
        version="1.0"
        mylog(f"TfWEB.init('{datasetPathname}')...")
        
        super().__init__(datasetPathname, version='1.0', dbname=db, dataset=dataset)

    def getLemmaFeature(self):
        # We don't have lemmas, just words, so return text feature
        return self.api.F.text

    def getLemma(self, wordid):
        # Fallback to the 'text' feature for lemma
        return self.api.F.text.v(wordid)

    def getBeta(self,wordid):
        return self.api.F.text.v(wordid)

    def getPlain(self,wordid):
        return self.api.F.text.v(wordid)
        
    def getGloss(self,wordid):
        return ''

    def isProperNoun(self,wordid):
        text = self.api.F.text.v(wordid)
        if text and len(text) > 0:
            return text[0].isupper()
        return False

    def getText(self, nodeId):
        text = super().getText(nodeId)
        if self.api.F.otype.v(nodeId) != 'word':
            
            text = re.sub(r'\s+([.,!?;:])', r'\1', text)
            # handle quotes which might have spaces around them.
            text = text.replace(" ' ", "'").replace(" \u2019 ", "\u2019").replace(" \u201d ", "\u201d")
        return text

    def normalize(self,string):
        return string

    def pos(self,wordid):
        return ''
        
    def apparatusNote(self,book,chapter,verse):
        return ''
