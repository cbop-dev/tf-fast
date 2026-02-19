import pytest, os,sys, csv, re
from tffast.tfData.tfBHS import TfBHS
from tffast.env import debug,mylog
bhs=None
@pytest.fixture()
def BHS():
    global bhs
    if(not bhs):
        bhs= TfBHS()
    return bhs


def test_getLex_test(BHS):
    tests=[
        {'id': 1437603, 'lex':'רֵאשִׁית'}
    ]
    for t in tests:
        assert(BHS.getLemma(t['id']) == t['lex'])

def test_getChapters(BHS):
    tests=[
        {'abbrev': 'Isa', 'chap':47, 'node':427010}
    ]

    for t in tests:
        assert(BHS.getChapter(BHS.lookupBook(t['abbrev']),t['chap']) == t['node'])


def test_properName(BHS):
    props=[
        228531
    ]

    notProps=[
        228546
    ]

    propNames=[
        'בָּבֶל'
    ]
    for p in props:
        assert(BHS.isProperNoun(p))

    for n in notProps:
        assert(not BHS.isProperNoun(n))

    for pn in propNames:
        assert(BHS.lexemes[pn].isProper)

    
def test_countLexSection(BHS):
    tests = [
        {'section':1428929, 'lemma': 'זעק', 'count': 1},
        {'section':426597, 'lemma': 'זעק', 'count': 13},
       
        
        #lex id of 'זעק' is: 439447
    ]

    for t in tests:
        assert(BHS.countLexInSection(t['lemma'], t['section'])==t['count'])

def test_getLexemes2(BHS):
    tests = [
        {'sections': [1414389], 'lexemes':{ #Gen 1:1
            'ברא':{
                'count':1
            }
        }},
        {'sections': [426591], 'lexemes':{ #Gen 
            'ברא':{
                'count':11
            }
        }},
        # # Gen
    
    ]

    for t in tests:
        lexes = BHS.getLexemes2(sections=t['sections'])
        assert(len(lexes['lexemes'].keys())>1)
        print(lexes['lexemes'].keys())

        for (l,obj) in t['lexemes'].items():
            assert(l in lexes['lexemes'].keys())
            if (l in lexes['lexemes'].keys()):
                assert(lexes['lexemes'][l]['count']==obj['count'])


def test_handyDictionary(BHS):
    tests=[
        {'bookname': 'Genesis', 'chap':1,'verses':[1], 'numLexes':9},
        {'bookname': 'Genesis', 'chap':1,'verses':[], 'numLexes':104}
    ]
    for t in tests:
        d=BHS.getHandyDictionary(t['bookname'],t['chap'],t['verses'])
        assert(len(d)==t['numLexes'])




import pytest


def test_book_drift_report(BHS):
    T = BHS.api.T
    F = BHS.api.F
    L = BHS.api.L
    def getWordNode(section,wordindex=0):
        secNode = T.nodeFromSection(section)
        return L.d(secNode,'word')[wordindex]
    book_nodes = F.otype.s('book')
    
    print(f"\n{'Book':<15} | {'Node':<7} | {'Word':<10} | {'Mapped Str':<10}")
    print("-" * 60)
    
    for b_node in book_nodes:
        # Get the name string for this book node
        b_name = T.bookName(b_node)
        
        # Get the first word node of the book
        # We use T.nodeFromSection with the book name
        try:
            first_word_node = getWordNode((b_name, 1, 1), 0)
            actual_word = F.g_word_utf8.v(first_word_node)
            mapped_strong = F.strongs.v(first_word_node)
            
            print(f"{b_name:<15} | {first_word_node:<7} | {actual_word:<10} | {str(mapped_strong):<10}")
        except Exception as e:
            print(f"{b_name:<15} | Error finding first node: {e}")

    #assert 0 == 1

def test_find_exact_divergence(BHS):
    T = BHS.api.T
    F = BHS.api.F
    L = BHS.api.L
    def getWordNode(section,wordindex=0):
        secNode = T.nodeFromSection(section)
        return L.d(secNode,'word')[wordindex]
    print("\n--- SCANNING GENESIS FOR FIRST DIVERGENCE ---")
    for n in range(1, 1000): # Scan the first 1000 nodes
        actual_word = F.g_word_utf8.v(n)
        mapped_strong = F.strongs.v(n)
        
        # We need a way to verify if 'mapped_strong' actually belongs to 'actual_word'
        # Let's print the first 50 nodes to look for the shift manually
        if n < 51:
            print(f"{n}: {actual_word} -> {mapped_strong}")

    #assert(False)

import re

def NOTtest_calculate_offsets(BHS):
    T = BHS.api.T
    F = BHS.api.F
    L = BHS.api.L
    def getWordNode(section,wordindex=0):
        secNode = T.nodeFromSection(section)
        return L.d(secNode,'word')[wordindex]
    # Helper to mimic the CSV parser for the special bracket format
    def parse_addr(s):
        return [int(x) for x in re.findall(r'\d+', s)]

    print(f"\n{'Book':<15} | {'TF Node':<7} | {'BHSsort':<8} | {'Offset (TF-BHS)'}")
    print("-" * 55)

    for b_node in F.otype.s('book'):
        b_name = T.bookName(b_node)
        
        # Get TF's absolute first word node for this book
        tf_first_node = getWordNode((b_name, 1, 1), 0)
        
        # Now, we simulate finding the CSV's BHSsort for that same address.
        # Since I can't read your whole CSV here, this logic assumes 
        # you'll run this inside your mapping loop.
        
        # To find the offset in your actual data, use this logic:
        # if row_address == (b_name, 1, 1, 1):
        #    offset = tf_first_node - int(row['BHSsort'])
        #    print(f"{b_name}: {offset}")
    
    #assert 0 == 1



def test_tsv_drift_report_robust(BHS):
    # 1. Setup API and Helper
    T = BHS.api.T
    F = BHS.api.F
    L = BHS.api.L

    def getWordNode(section, wordindex=0):
        secNode = T.nodeFromSection(section)
        return L.d(secNode, 'word')[wordindex]

    # 2. Load the TSV and index the first word of every verse
    tsv_anchors = {}
    file_path = "/home/cbrannan/tmp/tf-bhs-strong/BHS-with-Strong-no-extended.csv"
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                addr_str = row.get('〔KJVverseID｜book｜chapter｜verse〕', '')
                match = re.findall(r'\d+', addr_str)
                if not match: continue
                
                # addr matches: [KJVid, book, chap, verse]
                _, b, c, v = map(int, match)
                
                # Anchor: Store the very first BHSsort encountered for each address
                if (b, c, v) not in tsv_anchors:
                    tsv_anchors[(b, c, v)] = int(row['BHSsort'])
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    # 3. Compare BHS nodes with TSV BHSsort
    print(f"\n{'Book':<15} | {'TF Node':<8} | {'BHSsort':<8} | {'Delta'}")
    print("-" * 55)

    # We iterate through book nodes in BHS order
    # 'enumerate' provides the 1-based index (Genesis=1, Exodus=2, etc.)
    for i, b_node in enumerate(F.otype.s('book')):
        b_name = T.bookName(b_node)
        b_num = i + 1 
        
        try:
            # Word 1 (index 0) of the book start (1:1)
            tf_node = getWordNode((b_name, 1, 1), 0)
            
            # Retrieve the BHSsort using the 1-based index
            tsv_bhs_sort = tsv_anchors.get((b_num, 1, 1))
            
            if tsv_bhs_sort is not None:
                delta = tf_node - tsv_bhs_sort
                print(f"{b_name:<15} | {tf_node:<8} | {tsv_bhs_sort:<8} | {delta:+d}")
            else:
                print(f"{b_name:<15} | No TSV data for {b_name} (Book {b_num})")
        except Exception:
            continue

#    assert 0 == 1
import os

def test_verify_strongs_alignment_cons(BHS):
    # 1. Access the API
    T = BHS.api.T
    F = BHS.api.F
    L = BHS.api.L
    
    def get_word_info(book, c, v, node_idx=0):
        """Helper to get node, consonantal text, and strongs."""
        try:
            verse_node = T.nodeFromSection((book, c, v))
            word_nodes = L.d(verse_node, 'word')
            target_node = word_nodes[node_idx]
            
            # g_cons_utf8: Purely consonants. No vowels, no accents.
            return target_node, F.g_cons_utf8.v(target_node), F.strongs.v(target_node)
        except Exception as e:
            return None, None, None

    # 2. Test Case 1: Genesis 1:1, Node 2 ('Reshit')
    # Consonantal: ראשׁית
    gen_node, gen_cons, gen_strong = get_word_info('Genesis', 1, 1, 1)
    print(f"\n[Check Genesis] Node {gen_node}: {gen_cons} -> Strongs: {gen_strong}")
    
    assert gen_cons == 'ראשׁית'
    assert gen_strong is not None

    # 3. Test Case 2: 1 Samuel 1:1, Node 2 ('Wayyehi' root)
    # The verb 'yehi' consonantal form is 'יהי'
    sam_node, sam_cons, sam_strong = get_word_info('1_Samuel', 1, 1, 1)
    print(f"[Check 1 Sam] Node {sam_node}: {sam_cons} -> Strongs: {sam_strong}")
    
    # Note: g_cons_utf8 follows the surface form, not the dictionary root.
    # So 'יהי' (yehi) will be 'יהי', not 'היה' (hayah).
    assert sam_cons == 'יהי'
    assert sam_strong is not None

    print("\nConsonantal alignment check passed!")

def test_getLexemes2_counts(BHS):
    tests=[{'lexid': 5950, 'total': 1,'sections':[426631],'secCount':1}] #rishon

    for t in tests:
        lex = BHS.getLex(t['lexid'])
        print(f"got lex '${lex.lemma}'. Total: ${lex.total}")
        assert lex.total == t['total']
        res = BHS.getLexemes2(sections=t['sections'])
        assert len(res)
        print("here's the lexes!")
        print(res)
        found=[lex for lem,lex in res['lexemes'].items() if int(lex['id'])==int(t['lexid'])]
        print(f"len of found=${len(found)}")
        assert len(found)
        assert found[0]['count']==t['secCount']
        assert found[0]['total']==t['total']
        
#def test_normalize