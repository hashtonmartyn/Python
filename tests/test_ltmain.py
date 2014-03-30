'''
Created on 30/03/2014

@author: Henry
'''
import unittest
import mock
from nose.tools import assert_true, assert_equal
from py_src import ltmain

class Test_Printer(unittest.TestCase):

    def setUp(self):
        self.printer = ltmain.Printer()

    def tearDown(self):
        self.printer = None

    def test_write_appends_text(self):
        """
        Printer.write should append strings to its buffer until it is called with
        "\n", then it should call Printer.flush
        """
        assert_equal(self.printer.cur, "")
        buffer = ""
        
        for ch in "abcdefhijklmnopqrstuvwxyz0123456789":
            buffer += ch
            self.printer.write(ch)
            assert_equal(buffer, self.printer.cur)
    
    @mock.patch('py_src.ltmain.Printer.flush')    
    def test_write_calls_flush_for_new_line(self, flush_mock):
        self.printer.write("\n")
        flush_mock.assert_called_once_with()
        
    def test_readlines_returns_none(self):
        self.assertIsNone(self.printer.readlines())
        
    def test_read_returns_none(self):
        self.assertIsNone(self.printer.read())
        
def test_findLoc_returns_none_for_zero_len_body():
    assert_true(ltmain.findLoc("", 0, 0) is None)
    
def test_findLoc_lineno_equal_line_index_plus_one_equal_than_len_body():
    mock_body = mock.MagicMock()
    mock_body.lineno = 0
    total = 0
    loc = ltmain.findLoc([mock_body], mock_body.lineno, total)
    assert_equal(loc["start"], mock_body.lineno)
    assert_equal(loc["end"], total)
    
def test_findLoc_lineno_equal_line_index_plus_one_less_than_len_body():
    body = []
    line = 0
    total = 0
    for i in range(3):
        mock_body = mock.MagicMock()
        mock_body.lineno = i
        body.append(mock_body)
    loc = ltmain.findLoc(body, line, total)
    assert_equal(loc["start"], line)
    assert_equal(loc["end"], 0)
    
def test_findLoc_lineno_greater_than_line_and_line_not_equal_zero():
    body = []
    line = -1
    total = 0
    for i in range(3):
        mock_body = mock.MagicMock()
        mock_body.lineno = i
        body.append(mock_body)
    loc = ltmain.findLoc(body, line, total)
    assert_equal(loc["start"], body[-1].lineno)
    assert_equal(loc["end"] + 1, body[0].lineno)
    
def test_findLoc_lineno_less_than_line_index_plus_one_equal_len_body_line_less_than_total():
    body = []
    line = 5
    total = 10
    for i in range(3):
        mock_body = mock.MagicMock()
        mock_body.lineno = i
        body.append(mock_body)
    loc = ltmain.findLoc(body, line, total)
    assert_equal(loc["start"], body[-1].lineno)
    assert_equal(loc["end"] + 1, total + 1)


def test_asUnicode_encodes_in_range_characters():
    """
    Tests that ordinals up to but not including 128 will be returned as unicode
    strings.
    """
    for ordinal in range(128):
        uni_ch = ltmain.asUnicode(chr(ordinal))
        assert_true(isinstance(uni_ch, unicode),
                    "Expected unicode type but got %s for %s" % (uni_ch.__class__.__name__,
                                                                 chr(ordinal)))
        assert_equal(u"%s" % chr(ordinal), uni_ch)
        
def test_asUnicode_doesnt_encode_out_of_range_characters():
    """
    Tests that ordinals in the range 128-255 are returned as normal strings.
    """
    for ordinal in range(128, 255):
        ch = ltmain.asUnicode(chr(ordinal))
        assert_true(isinstance(ch, str),
                    "Expected str type but got %s for %s" % (ch.__class__.__name__,
                                                             chr(ordinal)))
        assert_equal(chr(ordinal), ch)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()