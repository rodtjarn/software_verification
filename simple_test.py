"""
Simple tests for string reversal
"""
from hypothesis import given, settings, strategies as st
from simple_code import reverse_string
from conftest import requirement, feature


@requirement("REQ-1")
@feature("F1.1", "F1.4")  # ASCII and special characters
def test_basic_reversal():
    """Test basic string reversal"""
    assert reverse_string("hello") == "olleh"


@requirement("REQ-1", "REQ-2")
@feature("F1.1", "F1.2", "F1.4", "F2.1", "F2.2", "F2.3")  # All string types, all idempotency
@given(st.text())
@settings(max_examples=500)
def test_reverse_twice_is_original(s):
    """Reversing twice returns the original - tests with random strings"""
    assert reverse_string(reverse_string(s)) == s


@requirement("REQ-1")
@feature("F1.3")  # Emoji handling
def test_emoji_reversal():
    """Test emoji string reversal"""
    assert reverse_string("hello👋world🌍") == "🌍dlrow👋olleh"
    assert reverse_string("🎉🎊🎈") == "🎈🎊🎉"


@requirement("REQ-3")
@feature("F3.1")  # Empty string handling
def test_empty_string():
    """Empty string reverses to empty string"""
    assert reverse_string("") == ""


@requirement("REQ-4")
@feature("F4.1", "F4.2", "F4.3")  # Length preservation for all types
@given(st.text())
@settings(max_examples=1000)
def test_length_preserved(s):
    """Reversing preserves string length"""
    assert len(reverse_string(s)) == len(s)
