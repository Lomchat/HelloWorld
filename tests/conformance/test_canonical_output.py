"""Byte-exact conformance tests for the canonical greeting.

The output of this program is its public contract. Downstream consumers
(scripts, pipelines, monitoring probes) may depend on it byte for byte. These
tests pin down every observable property of the greeting, through every
entry point of the application, so that any deviation, however small, is
caught immediately.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
import zlib
from pathlib import Path

import pytest

pytestmark = pytest.mark.conformance

EXPECTED_GREETING = "Hello, World!"
EXPECTED_STDOUT = b"Hello, World!\n"
SNAPSHOT = Path(__file__).parent / "snapshots" / "canonical_greeting.txt"

# Reference fingerprints of the canonical greeting.
EXPECTED_DIGESTS = {
    "md5": "65a8e27d8879283831b664bd8b7f0ad4",
    "sha1": "0a0a9f2a6772942557ab5355d76af442f8f65e01",
    "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
}
EXPECTED_CRC32 = 0xEC4AC3D0


class TestCharacterLevel:
    @pytest.mark.parametrize(
        ("index", "expected"),
        list(enumerate(EXPECTED_GREETING)),
        ids=[f"{i}-{c!r}" for i, c in enumerate(EXPECTED_GREETING)],
    )
    def test_character_at_position(self, greeting, index, expected):
        assert greeting[index] == expected


class TestByteLevel:
    @pytest.mark.parametrize(
        ("index", "expected"),
        list(enumerate(EXPECTED_STDOUT)),
        ids=[f"{i}-0x{b:02x}" for i, b in enumerate(EXPECTED_STDOUT)],
    )
    def test_stdout_byte_at_position(self, stdout_bytes, index, expected):
        assert stdout_bytes[index] == expected

    def test_stdout_length(self, stdout_bytes):
        assert len(stdout_bytes) == 14

    def test_stdout_ends_with_a_single_line_feed(self, stdout_bytes):
        assert stdout_bytes.endswith(b"\n")
        assert not stdout_bytes.endswith(b"\n\n")

    def test_stdout_uses_unix_line_endings(self, stdout_bytes):
        assert b"\r" not in stdout_bytes

    def test_stdout_has_no_byte_order_mark(self, stdout_bytes):
        assert not stdout_bytes.startswith(b"\xef\xbb\xbf")

    def test_stdout_matches_the_snapshot(self, stdout_bytes):
        assert stdout_bytes == SNAPSHOT.read_bytes()


class TestStructure:
    def test_length(self, greeting):
        assert len(greeting) == 13

    def test_matches_the_expected_pattern(self, greeting):
        assert re.fullmatch(r"[A-Z][a-z]+, [A-Z][a-z]+!", greeting)

    def test_starts_with_capital_h(self, greeting):
        assert greeting.startswith("H")

    def test_ends_with_an_exclamation_mark(self, greeting):
        assert greeting.endswith("!")

    def test_contains_exactly_one_comma(self, greeting):
        assert greeting.count(",") == 1

    def test_contains_exactly_one_space(self, greeting):
        assert greeting.count(" ") == 1

    def test_contains_exactly_one_exclamation_mark(self, greeting):
        assert greeting.count("!") == 1

    def test_contains_exactly_two_words(self, greeting):
        assert len(greeting.split()) == 2

    def test_words_are_title_case(self, greeting):
        assert all(word.strip(",!").istitle() for word in greeting.split())

    def test_has_no_surrounding_whitespace(self, greeting):
        assert greeting == greeting.strip()

    def test_has_no_consecutive_spaces(self, greeting):
        assert "  " not in greeting

    def test_has_no_line_breaks(self, greeting):
        assert len(greeting.splitlines()) == 1


class TestEncoding:
    def test_is_ascii(self, greeting):
        assert greeting.isascii()

    def test_is_printable(self, greeting):
        assert greeting.isprintable()

    def test_is_nfc_normalized(self, greeting):
        assert unicodedata.is_normalized("NFC", greeting)

    def test_is_nfkc_normalized(self, greeting):
        assert unicodedata.is_normalized("NFKC", greeting)

    def test_utf8_round_trip(self, greeting):
        assert greeting.encode("utf-8").decode("utf-8") == greeting

    def test_utf8_and_ascii_encodings_are_identical(self, greeting):
        assert greeting.encode("utf-8") == greeting.encode("ascii")

    def test_latin1_and_ascii_encodings_are_identical(self, greeting):
        assert greeting.encode("latin-1") == greeting.encode("ascii")


class TestFingerprint:
    @pytest.mark.parametrize(("algorithm", "expected"), list(EXPECTED_DIGESTS.items()))
    def test_digest(self, greeting, algorithm, expected):
        digest = hashlib.new(algorithm, greeting.encode(), usedforsecurity=False)
        assert digest.hexdigest() == expected

    def test_crc32(self, greeting):
        assert zlib.crc32(greeting.encode()) == EXPECTED_CRC32
