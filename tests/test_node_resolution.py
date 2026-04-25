import unittest
from tffast.tfData.tfBHS import TfBHS
from tffast.tfData.tfLXX import TfLXX
from tffast.MyDatasets import getDataset
#global LXX, BHS
class TestNodeResolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bhs = getDataset('bhs')
        cls.lxx = getDataset('lxx')

    def test_lxx_book_resolution(self):
        """Test LXX full books and abbreviations map to the same Book Node"""
        gen_short = self.lxx.lookupBook("Gen")
        gen_long = self.lxx.lookupBook("Genesis")
        self.assertIsNotNone(gen_short)
        self.assertEqual(gen_short, gen_long)

    def test_bhs_book_resolution(self):
        """Test BHS full books and abbreviations map to the same Book Node"""
        deut_short = self.bhs.lookupBook("Deut")
        deut_long = self.bhs.lookupBook("Deuteronomy")
        self.assertIsNotNone(deut_short)
        self.assertEqual(deut_short, deut_long)
        
        sam_short = self.bhs.lookupBook("2Sam")
        sam_long = self.bhs.lookupBook("2Samuel")
        sam_spaced = self.bhs.lookupBook("2 Sam")
        self.assertIsNotNone(sam_short)
        self.assertEqual(sam_short, sam_long)
        self.assertEqual(sam_short, sam_spaced)
        
        kgs_spaced = self.bhs.lookupBook("1 Kings")
        kgs_short = self.bhs.lookupBook("1Kgs")
        self.assertIsNotNone(kgs_spaced)
        self.assertEqual(kgs_spaced, kgs_short)

    def test_lxx_chapter_resolution(self):
        """Test LXX chapter lookup evaluates correctly regardless of book name string"""
        book_node = self.lxx.lookupBook("Gen")
        ch_node = self.lxx.getChapter(book_node, 1)
        self.assertIsNotNone(ch_node)
        self.assertNotEqual(ch_node, 0)
        
        # Test string vs int chapter
        ch_node_str = self.lxx.getChapter(book_node, "1")
        self.assertEqual(ch_node, ch_node_str)

    def test_bhs_verse_resolution(self):
        """Test BHS graph traversal evaluates 'Deut 1:1' correctly"""
        book_node = self.bhs.lookupBook("Deut")
        verse_node = self.bhs.getNodeFromBcV(book_node, 1, 1)
        self.assertIsNotNone(verse_node)
        self.assertNotEqual(verse_node, 0)
        
        # Cross test with full name
        verse_node_full = self.bhs.getNodeFromBcV(self.bhs.lookupBook("Deuteronomy"), 1, 1)
        self.assertEqual(verse_node, verse_node_full)

    def test_lxx_verse_resolution(self):
        """Test LXX graph traversal evaluates 'Gen 1:1' vs 'Genesis 1:1'"""
        gen_short_node = self.lxx.getNodeFromBcV("Gen", 1, 1)
        gen_long_node = self.lxx.getNodeFromBcV("Genesis", 1, 1)
        
        self.assertIsNotNone(gen_short_node)
        self.assertNotEqual(gen_short_node, 0)
        self.assertEqual(gen_short_node, gen_long_node)

    def test_numbered_books_dictionaries(self):
        """Test that all datasets support spaced numbered book aliases directly in their booksDict"""
        from tffast.tfData.tfVulgate import TfVulgate
        from tffast.tfData.tfWEB import TfWEB
        from tffast.tfData.tfNT import TfN1904
        from tffast.tfData.tfSBLGNT import TfSBLGNT
        
        def check_dict_for_alias(dictionary, alias):
            found = False
            for node, data in dictionary.items():
                syns = [str(s).lower() for s in data.get('syn', [])]
                if alias.lower() in syns:
                    found = True
                    break
            self.assertTrue(found, f"Alias '{alias}' not found in dictionary")

        # Check BHS & LXX
        check_dict_for_alias(TfBHS.booksDict, "1 Sam")
        check_dict_for_alias(TfBHS.booksDict, "2 Kings")
        check_dict_for_alias(TfLXX.booksDict, "1 Sam")

        # Check Vulgate & WEB
        check_dict_for_alias(TfVulgate.booksDict, "1 Cor")
        check_dict_for_alias(TfVulgate.booksDict, "2 Sam")
        check_dict_for_alias(TfWEB.booksDict, "1 Cor")
        check_dict_for_alias(TfWEB.booksDict, "2 Sam")
        
        # Check NT1904 & SBLGNT
        check_dict_for_alias(TfN1904.booksDict, "1 Cor")
        check_dict_for_alias(TfSBLGNT.booksDict, "1 Cor")
        
if __name__ == '__main__':
    unittest.main()
