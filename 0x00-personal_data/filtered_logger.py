#!/usr/bin/env python3
"""Module for personal data projects """
import re


def filter_datum(fields: list[str], redaction: str, 
                 message: str, separator: str) -> str:
    """ return log message obfuscated """
    return re.sub(r'{}(?={})'.format('|'.join(fields), re.escape(separator)), redaction, message)