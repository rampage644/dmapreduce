#!/usr/bin/env python
from __future__ import print_function

import os
import re


NAME_PTRN = "{NAME}"
ABS_PATH_PTRN = "{ABS_PATH}"

MANIFEST_TMPLT = """
Channel = {ABS_PATH}/debug.{NAME}.log, /dev/debug, 0, 0, 0, 0, 99999999, 99999999
Channel = /dev/null, /dev/stdin, 0, 0, 999999, 999999, 0, 0
Channel = {ABS_PATH}/stdout.{NAME}, /dev/stdout, 0, 0, 0, 0, 9999999, 9999999
Channel = {ABS_PATH}/stderr.{NAME}, /dev/stderr, 0, 0, 0, 0, 9999999, 9999999
Channel = {ABS_PATH}/nvram.{NAME}.conf, /dev/nvram, 0, 0, 999999, 999999, 0, 0
Channel = {ABS_PATH}/test.py, /dev/test.py, 0, 0, 999999, 999999, 0, 0
Channel = {ABS_PATH}/mount/python.tar, /dev/python.tar, 0, 0, 99999999, 99999999, 0, 0
Channel = {ABS_PATH}/input.txt, /dev/input.txt, 0, 0, 99999999, 99999999, 0, 0

Version = 20130611
Program = {ABS_PATH}/{NAME}.nexe

Memory = 0x100000000, 0
SyscallsMax = 13333
Timeout = 3600
"""

NVRAM_TMPLT = """
[fstab]
channel=/dev/python.tar, mountpoint=/, access=ro
[env]
name=Node, value=1
[debug]
verbosity=0
[args]
args={NAME}.nexe
"""




def generate_manifest(name):
	manifest = re.sub(
		NAME_PTRN, 
		name,
		MANIFEST_TMPLT)
	manifest = re.sub(
		ABS_PATH_PTRN,
		os.path.dirname(os.path.abspath(__file__)),
		manifest)
	return manifest


def generate_nvram(name):
	nvram = re.sub(
		NAME_PTRN, 
		name,
		NVRAM_TMPLT)
	return nvram

if __name__ == "__main__":
	# get list on 'nexe-binaries'
	nexes = filter(lambda x: '.nexe' in x, os.listdir('.'))
	# foreach nexe generate manifest and nvram.conf
	for nexe in nexes:
		# remove trailing .nexe
		nexe = nexe.replace('.nexe', '')
		with open("%s.manifest" % nexe, 'w') as mfile:
			print(generate_manifest(nexe), file=mfile)
		with open("nvram.%s.conf" % nexe, 'w') as nfile:
			print(generate_nvram(nexe), file=nfile)
