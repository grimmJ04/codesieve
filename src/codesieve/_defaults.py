import os

LEVEL = os.getenv('CODESIEVE_LEVEL', 1)
LIMIT = os.getenv('CODESIEVE_STR_LIMIT', 2 ** 14)
DIST = os.getenv('CODESIEVE_DIST', 's2s')
