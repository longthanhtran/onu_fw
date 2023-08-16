#!/usr/bin/env python3
# ODI DFP-34X-2C2 MAC_KEY key generator by rajkosto
# Gist https://gist.github.com/rajkosto/29c513b96ea6262d2fb1f965a52ce16f

import sys
import string
import hashlib

args = sys.argv
if len(args) != 2:
	sys.exit("Usage: odi_keygen.py YOURMACADDR")

macAddr = args[1].strip().replace(':','')
if len(macAddr) != 12:
	sys.exit("Mac address must be 12 hex digits (6 bytes)")

if not all(c in string.hexdigits for c in macAddr):
	sys.exit("Mac address can only contain 0-9, A-F characters (hex digits)")

cmacPrefix = 'hsgq1.9a'
hashText = cmacPrefix+macAddr.upper()
encodedText = hashText.encode('ascii')
md5Hash = hashlib.md5(encodedText).digest().hex()

print('ELAN_MAC_ADDR='+macAddr.lower())
print('MAC_KEY='+md5Hash.lower())
