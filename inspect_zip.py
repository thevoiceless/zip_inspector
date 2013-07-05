#!/usr/bin/env python

import argparse
import binascii

def swapEndian(bytes):
	return [bytes[i] for i in range(len(bytes) - 1, -1, -1)]

def hexlistToString(bytes):
	return ''.join(binascii.hexlify(b) for b in bytes)

def printBytes(bytes, sameline = False):
	s = hexlistToString(bytes)
	if sameline:
		print s,
	else:
		print s

def bytesEquals(bytes):
	return int(''.join(binascii.hexlify(b) for b in swapEndian(bytes)), 16)

def printChars(f, n):
	if (n > 0):
		s = [chr(int(binascii.hexlify(f.read(1)), 16)) for i in range(n)]
		print ''.join(s)
	else:
		print '<None>'

def twoBytes(f):
	bytes = [f.read(1) for i in range(2)]
	return bytes

def fourBytes(f):
	bytes = [f.read(1) for i in range(4)]
	return bytes

parser = argparse.ArgumentParser()
parser.add_argument('zip', help = 'zip file to inspect')
args = parser.parse_args()

z = args.zip
bytes = ''
loc_file_flags = []
cent_dir_file_flagas = []

LOCAL_FILE_SIG = '504b0304'
FILE_DATA_DESC_SIG = '504b0708'
ARCHIVE_EXTRA_DATA_SIG = '504b0608'
CENT_DIR_FILE_SIG = '504b0102'
CENT_DIR_DIGITAL_SIG = '504b0505'
CENT_DIR_ZIP64_END_RECORD_SIG = '504b0606' # Not handled
CENT_DIR_ZIP64_END_LOCATOR_SIG = '504b0607' # Not handled
CENT_DIR_END_RECORD_SIG = '504b0506'



with open(z, 'rb') as f:
	byte = f.read(1)
	while byte:
		bytes += binascii.hexlify(byte)
		if (bytes.endswith(LOCAL_FILE_SIG)):
			print '--- Found file'
			bytes = ''

			print ' Version:',
			printBytes(twoBytes(f))

			print ' Flags:',
			loc_file_flags = twoBytes(f)
			printBytes(loc_file_flags)
			
			print ' Compression:',
			printBytes(twoBytes(f))
			
			print ' Mod time:',
			printBytes(twoBytes(f))
			
			print ' Mod date:',
			printBytes(twoBytes(f))
			
			print ' CRC-32:',
			printBytes(fourBytes(f))
			
			print ' Compressed size:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			c_size = bytesEquals(lilendian)
			print '=', c_size
			
			print ' Uncompressed size:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			uc_size = bytesEquals(lilendian)
			print '=', uc_size
			
			print ' File name length:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			filename_len = bytesEquals(lilendian)
			print '=', filename_len
			
			print ' Extra field length:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			extra_len = bytesEquals(lilendian)
			print '=', extra_len
			
			print ' File name:',
			printChars(f, filename_len)
			
			print ' Extra field:',
			printChars(f, extra_len)

			print

		elif (bytes.endswith(FILE_DATA_DESC_SIG)):
			print '--- Found file descriptor'
			# File data descriptor should only be present if bit 3 of the flags is set
			# Convert flags to binary, reverse them to change from little-endian, and check the bit in the third index
			if (int(bin(int(hexlistToString(loc_file_flags), 16))[2:].zfill(16)[::-1][3]) & 1 == 0):
				print '> Error: Bit 3 of bit flags should be set'
			bytes = ''

			print ' CRC-32:',
			printBytes(fourBytes(f))

			print ' Compressed size:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			c_size = bytesEquals(lilendian)
			print '=', c_size
			
			print ' Uncompressed size:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			uc_size = bytesEquals(lilendian)
			print '=', uc_size

			print

		elif (bytes.endswith(ARCHIVE_EXTRA_DATA_SIG)):
			print '--- Found extra archive data'
			bytes = ''

			print 'Extra data length:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			archive_extra_len = bytesEquals(lilendian)
			print '=', archive_extra_len

			print 'Extra data:',
			printChars(f, archive_extra_len)

		elif (bytes.endswith(CENT_DIR_FILE_SIG)):
			print '--- Found central directory file'
			bytes = ''

			print ' Version:',
			printBytes(twoBytes(f))

			print ' Version needed:',
			printBytes(twoBytes(f))

			print ' Flags:',
			cent_dir_file_flagas = twoBytes(f)
			printBytes(cent_dir_file_flagas)

			print ' Compression:',
			printBytes(twoBytes(f))

			print ' Mod time:',
			printBytes(twoBytes(f))
			
			print ' Mod date:',
			printBytes(twoBytes(f))

			print ' CRC-32:',
			printBytes(fourBytes(f))
			
			print ' Compressed size:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			c_size = bytesEquals(lilendian)
			print '=', c_size
			
			print ' Uncompressed size:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			uc_size = bytesEquals(lilendian)
			print '=', uc_size

			print ' File name length:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			filename_len = bytesEquals(lilendian)
			print '=', filename_len
			
			print ' Extra field length:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			extra_len = bytesEquals(lilendian)
			print '=', extra_len

			print ' File comment length:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			comment_len = bytesEquals(lilendian)
			print '=', comment_len

			print ' Disk start number:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			disk_start = bytesEquals(lilendian)
			print '=', disk_start

			print ' Internal attributes:',
			printBytes(twoBytes(f))

			print ' External attributes:',
			printBytes(fourBytes(f))

			print ' Offset of local header:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			header_offset = bytesEquals(lilendian)
			print '=', header_offset

			print ' File name:',
			printChars(f, filename_len)

			print ' Extra field:',
			printChars(f, extra_len)

			print ' File comment:',
			printChars(f, comment_len)

			print

		elif (bytes.endswith(CENT_DIR_DIGITAL_SIG)):
			print '--- Found central directory digital signature'
			bytes = ''

			print ' Length of signature data:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			sig_data_len = bytesEquals(lilendian)
			print '=', sig_data_len

			print ' Signature data:',
			printChars(f, sig_data_len)

			print

		elif (bytes.endswith(CENT_DIR_END_RECORD_SIG)):
			print '--- Found end of central directory'
			bytes = ''

			print ' This disk number:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			centdir_this_disk = bytesEquals(lilendian)
			print '=', centdir_this_disk

			print ' Central directory starting disk number:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			centdir_start_disk = bytesEquals(lilendian)
			print '=', centdir_start_disk

			print ' Central directory entries on this disk:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			centdir_entries_this_disk = bytesEquals(lilendian)
			print '=', centdir_entries_this_disk

			print ' Central directory entries total:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			centdir_entries_total = bytesEquals(lilendian)
			print '=', centdir_entries_total

			print ' Size of central directory:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			centdir_size = bytesEquals(lilendian)
			print '=', centdir_size

			print ' Offset of central directory on starting disk:',
			lilendian = fourBytes(f)
			printBytes(lilendian, True)
			centdir_offset = bytesEquals(lilendian)
			print '=', centdir_offset

			print ' Comment length:',
			lilendian = twoBytes(f)
			printBytes(lilendian, True)
			centdir_comment_len = bytesEquals(lilendian)
			print '=', centdir_comment_len

			print ' Comment:',
			printChars(f, centdir_comment_len)

		byte = f.read(1)