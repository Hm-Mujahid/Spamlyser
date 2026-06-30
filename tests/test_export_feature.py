"""Tests for models/export_feature.py."""

import sys
import warnings

import pandas as pd
import pytest

# fpdf may be mocked in conftest. Remove the stub if present so the real
# module is used when installed, and skip PDF tests otherwise.
if "fpdf" in sys.modules and not hasattr(sys.modules["fpdf"], "__version__"):
    del sys.modules["fpdf"]
try:
    __import__("fpdf")
except ImportError:
    pytest.skip("fpdf not installed — PDF tests skipped", allow_module_level=True)

from models.export_feature import _pdf_safe, dataframe_to_pdf

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestPdfSafe:
    def test_plain_ascii_unchanged(self):
        assert _pdf_safe("Free $5 win cash now") == "Free $5 win cash now"

    def test_rupee_replaced(self):
        result = _pdf_safe("WIN \u20b95000")
        assert "\u20b9" not in result
        assert "?" in result

    def test_emoji_replaced(self):
        result = _pdf_safe("reply YES \U0001f389")
        assert "\U0001f389" not in result
        assert "?" in result

    def test_euro_replaced(self):
        result = _pdf_safe("\u20ac1000 prize")
        assert "\u20ac" not in result

    def test_latin1_chars_preserved(self):
        assert _pdf_safe("\u00a3500") == "\u00a3500"

    def test_empty_string(self):
        assert _pdf_safe("") == ""

    def test_non_string_coerced(self):
        assert _pdf_safe(123) == "123"
        assert _pdf_safe(None) == "None"


class TestDataframeToPdf:
    def _valid_pdf(self, data: bytes) -> bool:
        return data[:5] == b"%PDF-"

    def test_ascii_dataframe_produces_valid_pdf(self):
        df = pd.DataFrame(
            [
                {
                    "message": "Free entry win cash",
                    "label": "SPAM",
                    "confidence": "0.98",
                },
                {"message": "See you at 5pm", "label": "HAM", "confidence": "0.95"},
            ]
        )
        out = dataframe_to_pdf(df)
        assert self._valid_pdf(out.getvalue())

    def test_unicode_dataframe_produces_valid_pdf(self):
        df = pd.DataFrame(
            [
                {"message": "WIN \u20b95000 NOW \U0001f389", "label": "SPAM"},
                {"message": "\u20ac1000 \u00a3500 \u2014 claim", "label": "SPAM"},
            ]
        )
        out = dataframe_to_pdf(df)
        assert self._valid_pdf(out.getvalue())

    def test_empty_dataframe_produces_valid_pdf(self):
        df = pd.DataFrame({"message": [], "label": []})
        out = dataframe_to_pdf(df)
        assert self._valid_pdf(out.getvalue())

    def test_custom_title_in_output(self):
        df = pd.DataFrame([{"message": "hello", "label": "HAM"}])
        out = dataframe_to_pdf(df, title="Test Export")
        assert self._valid_pdf(out.getvalue())

    def test_long_cell_value_truncated(self):
        long_msg = "A" * 50
        df = pd.DataFrame([{"message": long_msg, "label": "SPAM"}])
        out = dataframe_to_pdf(df)
        assert self._valid_pdf(out.getvalue())

    def test_returns_bytesio_at_start(self):
        df = pd.DataFrame([{"message": "test", "label": "HAM"}])
        out = dataframe_to_pdf(df)
        assert out.tell() == 0
