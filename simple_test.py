"""
Simple tests for string reversal
"""
from hypothesis import given, strategies as st
from simple_code import reverse_string
from conftest import requirement


@requirement("REQ-1")
def test_basic_reversal():
    """Test basic string reversal"""
    assert reverse_string("hello") == "olleh"


@requirement("REQ-1", "REQ-2")
@given(st.text())
def test_reverse_twice_is_original(s):
    """Reversing twice returns the original - tests with random strings"""
    assert reverse_string(reverse_string(s)) == s


@requirement("REQ-3")
def test_empty_string():
    """Empty string reverses to empty string"""
    assert reverse_string("") == ""
