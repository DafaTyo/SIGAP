"""Tests for PII utilities."""

from __future__ import annotations

from app.utils.pii import mask_nik


def test_mask_nik_standard_length():
    nik = "3175123456781234"
    masked = mask_nik(nik)
    assert masked == "3175********1234"


def test_mask_nik_short():
    short = "1234567"
    masked = mask_nik(short)
    assert masked == "123***7"  # half length is 3 (123), mask 3, remainder 1
