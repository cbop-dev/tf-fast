from .tfDataset import TfDataset, POS
import os
from tffast.utils.greekUtils import GreekUtils
from tffast.utils.hebrewUtils import HebrewUtils

class TfBHS(TfDataset):

    posDict ={
        'subs': [POS.NOUN.value],
        'nmpr': [POS.PROPER_NOUN.value],
        'verb': [POS.VERB.value],
        'adjv': [POS.ADJECTIVE.value],
        'advb': [POS.ADVERB.value],
        'intj': [POS.INTERJECTION.value],
        'prps': [POS.PRONOUN_PRS.value],
        'prep': [POS.PREPOSITION.value],
        'prde': [POS.PRONOUN_DEM.value],
        'inrg': [POS.PRONOUN_INTER.value],
        'conj': [POS.CONJUNCTION.value],
        'nega': [POS.PARTICLE.value],
        'prin': [POS.PRONOUN_RELA.value],
        'art': [POS.ARTICLE.value],	
    }
    booksDictOLD = """
    {
        426591:{"abbrev":"Gen","syn":["Genesis",'Gen','Ge']},
        426592:{"abbrev":"Exod","syn":["Exodus",'Exod','Exodus']},
        426593:{"abbrev":"Lev","syn":["Leviticus",'Lev','Leviticus']},
        426594:{"abbrev":"Num","syn":["Numeri",'Num','Numbers']},
        426595:{"abbrev":"Deut","syn":["Deuteronomium",'Deut','Deuteronomy','Dt','Deu']},
        426596:{"abbrev":"Josh","syn":["Josua",'Josh','Joshua',"Josua"]},
        426597:{"abbrev":"Judg","syn":["Judices",'Judg','Judges','Jdg','Jdgs',"Judgs"]},
        426598:{"abbrev":"1Sam","syn":["Samuel_I",'1Sam','1Samuel','ISamuel','1Sa','1Sam','ISa','ISam']},
        426599:{"abbrev":"2Sam","syn":["Samuel_II",'2Sam','2Samuel','IISamuel','2Sa','2Sam','IISa','IISam']},
        426600:{"abbrev":"1Kgs","syn":["Reges_I",'1Kgs','1Kings','IKings','1Kg','IKg']},
        426601:{"abbrev":"2Kgs","syn":["Reges_II",'2Kgs','2Kings','IIKings','2Kg','IIKg']},
        426602:{"abbrev":"Isa","syn":["Jesaia",'Isa','Isaiah','Is',"Jesaia"]},
        426603:{"abbrev":"Jer","syn":["Jeremia",'Jer','Jeremiah',"Jeremia","Jerem","Jere"]},
        426604:{"abbrev":"Ezek","syn":["Ezechiel",'Ezek','Ezekiel',"Ezechiel"]},
        426605:{"abbrev":"Hos","syn":["Hosea",'Hos']},
        426606:{"abbrev":"Joel","syn":["Joel"]},
        426607:{"abbrev":"Amos","syn":["Amos","Am"]},
        426608:{"abbrev":"Obad","syn":["Obadia",'Obad','Obadiah','Ob',"Obed"]},
        426609:{"abbrev":"Jonah","syn":["Jona",'Jonah','Jon']},
        426610:{"abbrev":"Mic","syn":["Micha",'Mic','Micah',"Micha","Mica"]},
        426611:{"abbrev":"Nah","syn":["Nahum",'Nah']},
        426612:{"abbrev":"Hab","syn":["Habakuk",'Hab','Habakkuk']},
        426613:{"abbrev":"Zeph","syn":["Zephania",'Zeph','Zephaniah']},
        426614:{"abbrev":"Hag","syn":["Haggai",'Hag','Haggai']},
        426615:{"abbrev":"Zech","syn":["Sacharia",'Zech','Zechariah']},
        426616:{"abbrev":"Mal","syn":["Maleachi",'Mal','Malachi']},
        426617:{"abbrev":"Ps","syn":["Psalmi",'Ps(s)','Psalms','Psa']},
        426618:{"abbrev":"Job","syn":["Iob",'Job','Jb']},
        426619:{"abbrev":"Prov","syn":["Proverbia",'Prov','Proverbs','Pr']},
        426620:{"abbrev":"Ruth","syn":["Ruth","Ru"]},
        426621:{"abbrev":"Cant","syn":["Canticum",'Song','SongofSongs','SongofSolomon','Canticles','Cant']},
        426622:{"abbrev":"Qoh","syn":["Ecclesiastes",'Eccl','Ecclesiastes','Qoheleth','Qoh',"Eccl"]},
        426623:{"abbrev":"Lam","syn":["Threni",'Lam','Lamentations']},
        426624:{"abbrev":"Esth","syn":["Esther",'Esth','Est']},
        426625:{"abbrev":"Dan","syn":["Daniel","Dan"]},
        426626:{"abbrev":"Ezra","syn":["Esra","Ezr"]},
        426627:{"abbrev":"Neh","syn":["Nehemia",'Nehemiah',"Neh"]},
        426628:{"abbrev":"1Chr","syn":["Chronica_I",'1Chr','1Chronicles','1Chron','1Ch','IChronicles','IChron','ICh','IChr']},
        426629:{"abbrev":"2Chr","syn":["Chronica_II",'2Chr','2Chronicles','2Chron','2Ch','IIChronicles','IIChron','IICh','IIChr']},
    }
    """
    booksDict= {426591: {'abbrev': 'Gen', 'syn': ['Genesis', 'Gen', 'Ge'], 'name': 'Genesis'},
        426592: {'abbrev': 'Exod',   'syn': ['Exodus', 'Exod', 'Exodus'], 'name': 'Exodus'},
        426593: {'abbrev': 'Lev',   'syn': ['Leviticus', 'Lev', 'Leviticus'], 'name': 'Leviticus'},
        426594: {'abbrev': 'Num',   'syn': ['Numeri', 'Num', 'Numbers'], 'name': 'Numbers'},
        426595: {'abbrev': 'Deut',   'syn': ['Deuteronomium', 'Deut', 'Deuteronomy', 'Dt', 'Deu'], 'name': 'Deuteronomy'},
        426596: {'abbrev': 'Josh',   'syn': ['Josua', 'Josh', 'Joshua', 'Josua'], 'name': 'Joshua'},
        426597: {'abbrev': 'Judg',   'syn': ['Judices', 'Judg', 'Judges', 'Jdg', 'Jdgs', 'Judgs'], 'name': 'Judges'},
        426598: {'abbrev': '1Sam',   'syn': ['Samuel_I',    '1Sam',    '1Samuel',    'ISamuel',    '1Sa',    '1Sam',    'ISa',    'ISam'], 'name': '1_Samuel'},
        426599: {'abbrev': '2Sam',   'syn': ['Samuel_II',    '2Sam',    '2Samuel',    'IISamuel',    '2Sa',    '2Sam',    'IISa',    'IISam'], 'name': '2_Samuel'},
        426600: {'abbrev': '1Kgs',   'syn': ['Reges_I', '1Kgs', '1Kings', 'IKings', '1Kg', 'IKg'], 'name': '1_Kings'},
        426601: {'abbrev': '2Kgs',   'syn': ['Reges_II', '2Kgs', '2Kings', 'IIKings', '2Kg', 'IIKg'], 'name': '2_Kings'},
        426602: {'abbrev': 'Isa',   'syn': ['Jesaia', 'Isa', 'Isaiah', 'Is', 'Jesaia'], 'name': 'Isaiah'},
        426603: {'abbrev': 'Jer',   'syn': ['Jeremia', 'Jer', 'Jeremiah', 'Jeremia', 'Jerem', 'Jere'], 'name': 'Jeremiah'},
        426604: {'abbrev': 'Ezek',   'syn': ['Ezechiel', 'Ezek', 'Ezekiel', 'Ezechiel'], 'name': 'Ezekiel'},
        426605: {'abbrev': 'Hos', 'syn': ['Hosea', 'Hos'], 'name': 'Hosea'},
        426606: {'abbrev': 'Joel', 'syn': ['Joel'], 'name': 'Joel'},
        426607: {'abbrev': 'Amos', 'syn': ['Amos', 'Am'], 'name': 'Amos'},
        426608: {'abbrev': 'Obad',   'syn': ['Obadia', 'Obad', 'Obadiah', 'Ob', 'Obed'], 'name': 'Obadiah'},
        426609: {'abbrev': 'Jonah', 'syn': ['Jona', 'Jonah', 'Jon'], 'name': 'Jonah'},
        426610: {'abbrev': 'Mic',   'syn': ['Micha', 'Mic', 'Micah', 'Micha', 'Mica'], 'name': 'Micah'},
        426611: {'abbrev': 'Nah', 'syn': ['Nahum', 'Nah'], 'name': 'Nahum'},
        426612: {'abbrev': 'Hab',   'syn': ['Habakuk', 'Hab', 'Habakkuk'], 'name': 'Habakkuk'},
        426613: {'abbrev': 'Zeph',   'syn': ['Zephania', 'Zeph', 'Zephaniah'], 'name': 'Zephaniah'},
        426614: {'abbrev': 'Hag',   'syn': ['Haggai', 'Hag', 'Haggai'], 'name': 'Haggai'},
        426615: {'abbrev': 'Zech',   'syn': ['Sacharia', 'Zech', 'Zechariah'], 'name': 'Zechariah'},
        426616: {'abbrev': 'Mal',   'syn': ['Maleachi', 'Mal', 'Malachi'], 'name': 'Malachi'},
        426617: {'abbrev': 'Ps',   'syn': ['Psalmi', 'Ps(s)', 'Psalms', 'Psa'], 'name': 'Psalms'},
        426618: {'abbrev': 'Job', 'syn': ['Iob', 'Job', 'Jb'], 'name': 'Job'},
        426619: {'abbrev': 'Prov',   'syn': ['Proverbia', 'Prov', 'Proverbs', 'Pr'], 'name': 'Proverbs'},
        426620: {'abbrev': 'Ruth', 'syn': ['Ruth', 'Ru'], 'name': 'Ruth'},
        426621: {'abbrev': 'Cant',   'syn': ['Canticum',    'Song',    'SongofSongs',    'SongofSolomon',    'Canticles',    'Cant'], 'name': 'Song_of_songs'},
        426622: {'abbrev': 'Qoh',   'syn': ['Ecclesiastes', 'Eccl', 'Ecclesiastes', 'Qoheleth', 'Qoh', 'Eccl'], 'name': 'Ecclesiastes'},
        426623: {'abbrev': 'Lam',   'syn': ['Threni', 'Lam', 'Lamentations'], 'name': 'Lamentations'},
        426624: {'abbrev': 'Esth',   'syn': ['Esther', 'Esth', 'Est'], 'name': 'Esther'},
        426625: {'abbrev': 'Dan', 'syn': ['Daniel', 'Dan'], 'name': 'Daniel'},
        426626: {'abbrev': 'Ezra', 'syn': ['Esra', 'Ezr'], 'name': 'Ezra'},
        426627: {'abbrev': 'Neh',   'syn': ['Nehemia', 'Nehemiah', 'Neh'], 'name': 'Nehemiah'},
        426628: {'abbrev': '1Chr',   'syn': ['Chronica_I',    '1Chr',    '1Chronicles',    '1Chron',    '1Ch',    'IChronicles',    'IChron',    'ICh',    'IChr'], 'name': '1_Chronicles'},
        426629: {'abbrev': '2Chr',   'syn': ['Chronica_II',    '2Chr',    '2Chronicles',    '2Chron',    '2Ch',    'IIChronicles',    'IIChron',    'IICh',    'IIChr'], 'name': '2_Chronicles'}}
 
    posGroups={
        "CONT":[0,1,2,3,4],
        "CONTENT":[0,1,2,3,4],
        "SYNT":[10,11],
        "SYNTAX":[10,11],
        "PREP":[7],
        "PREPOSITIONS":[7],
        "PREPOSITION":[7],
        "PART":[5,9,11,13],#I'm counting the article as a particle
        "PARTICLES":[5,9,11,13],
        "PARTICLE":[5,9,11,13],
        "PRON":[6,8,12],
        "PRONOUNS":[6,8,12],
        "PRONOUN":[6,8,12],
    }

    def properNounKey(self):
        return 1
        
    def __init__(self,dataset=None):
        self.booksDict = TfBHS.booksDict
        #super().__init__('ETCBC/bhsa',dbname="bhs", version="2021",dataset=dataset)
        #modpath=my_path = os.path.abspath("/home/cbrannan/tmp/tf-bhs-strong/")
        mod="cbop-dev/tf-bhsa-strongs/tf"
        version="2021"
        
        super().__init__('ETCBC/bhsa',dbname="bhs", mod=mod,version=version,dataset=dataset)
        self.lang="hebrew"
        #super().__init__('ETCBC/bhsa-min',dbname="bhs", version="2021",dataset=dataset)
		
    def getLemma(self,wordid):
        return HebrewUtils.normalize(self.getLemmaFeature().v(wordid).strip())
    
    def getLemmaFeature(self):
        return self.api.F.voc_lex_utf8

    def getPlain(self,wordID):
        return self.api.F.lex_utf8.v(wordID)

    def isProperNoun(self,wordID):
        return self.api.F.sp.v(wordID) == 'nmpr'

    def normalize(self,string):
        
        return HebrewUtils.normalize(string)
