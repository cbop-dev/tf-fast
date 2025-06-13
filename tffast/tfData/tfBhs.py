from .tfDataset import TfDataset

class TfBHS(TfDataset):

    posDict ={
        0: {'abbrev': 'subs', 'desc':'noun, substantive'},
        1: {'abbrev': 'nmpr', 'desc':'proper noun'},
        2: {'abbrev': 'verb', 'desc':'verb'},
        3: {'abbrev': 'adjv', 'desc':'adjective'},
        4: {'abbrev': 'advb', 'desc':'adverb'},
        5: {'abbrev': 'intj', 'desc':'interjection'},
        6: {'abbrev': 'prps', 'desc':'personal pronoun'},
        7: {'abbrev': 'prep', 'desc':'preposition'},
        8: {'abbrev': 'prde', 'desc':'demonstrative pronoun'},
        9: {'abbrev': 'inrg', 'desc':'interogative'},
        10: {'abbrev': 'conj', 'desc':'conjunction'},
        11: {'abbrev': 'nega', 'desc':'negative particle'},
        12: {'abbrev': 'prin', 'desc':'interogative pronoun'},
        13: {'abbrev': 'art', 'desc':'article'},	
    }
    booksDict = {
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
    bookDict = booksDict

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

    def __init__(self):
        TfDataset.__init__(self,'etcbc/bhsa')
		

    def getLemmaFeature(self):
        return self.api.F.voc_lex_utf8