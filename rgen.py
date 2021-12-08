#!env python
from pathlib import Path
import rstr
import re
import os
import time
import sys
import signal
import argparse
import logging

unique = set()
outfile = ''
rgx = ''

_start = time.time()

def signal_handler(sig, frame):
	if outfile is not False:
		logging.error("^C issued. Exiting gracefully.");
		logging.info("Total: {} passwords".format(len(unique)))
	sys.exit(0)

def append_new_line(file_name, text_to_append):

	try:
		with open(file_name, "a+") as file_object:
			file_object.seek(0)
			data = file_object.read(100)
			if len(data) > 0:
				file_object.write("\n")
			file_object.write(text_to_append)
	except:
		pass

def rand_by_regex(pattern):

	ok = False
	rvar = False
	final_string = ""
	global unique

	while True:

		r_string = rstr.xeger(pattern)

		if r_string not in unique:

			if outfile is False:
				unique.add(r_string)
				print(r_string)
			else:
				unique.add(r_string)
				append_new_line(outfile, r_string)
			break

if __name__ == '__main__':

	total_passwords = 0

	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--regex",     dest="regex",     help="Regular expression in single quotes", type=str)
	parser.add_argument("-f", "--forever",   dest="forever",   action="store_true", help="Run until Control-C is pressed")
	parser.add_argument("-n", "--numpasses", dest="numpasses", help="Number of passwords to generate (>0 disables -f, 0 enables -f)", type=int)
	parser.add_argument("-o", "--output",    dest="output",    help="Output file path. - prints to stdout", type=str)
	parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
	args = parser.parse_args()

	if args.debug is not False:
		logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
	else:
		logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)


	signal.signal(signal.SIGINT, signal_handler)

	if args.output == '-':
		outfile = False

	if args.output is not None:

		if outfile is not False:

			if os.path.exists(args.output):

				os.unlink(args.output)
				Path(args.output).touch()
				outfile = args.output

			else:

				with open(args.output, 'a'):
					logging.debug("Created file {}".format(args.output))

				outfile = args.output

	if args.numpasses is not None and args.numpasses > 0:
		cnt = args.numpasses
	else:
		if args.forever is True:
			cnt = 0
		else:
			if outfile is not False:
				logging.debug("Number of passwords was < 1, forever mode enabled.")
				args.forever = True

	if args.forever is True:
		cnt = 0

	if args.regex is not None and args.regex != '':
		rgx = re.compile(args.regex)

	if args.forever is True:

		while True:

			rand_by_regex(rgx)
			total_passwords += 1
			_stop = time.time()
			_duration = _stop - _start
			_per_second = int(total_passwords / _duration)

			if len(unique) % 1000 == 0:
				logging.debug(f"Generation rate: {_per_second} passwords/second")

			if len(unique) % 10000 == 0:
				if outfile is not False:
					logging.info("Generated {} matching passwords".format(len(unique)))

	else:

		for pw_count in range(0, cnt):

			if pw_count % 10000 == 0:
				if outfile is not False:
					logging.info("Generated {} matching passwords".format(len(unique)))

			if pw_count == cnt:
				if outfile is not False:
					logging.info("List ready at passwords.txt, {} passwords generated.".format(len(unique)))
				break

			rand_by_regex(rgx)

	if outfile is not False:
		logging.info("Finished!")
		sys.exit(0)
