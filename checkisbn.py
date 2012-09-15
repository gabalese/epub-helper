#! /usr/bin/env python3

import sys

def is_valid(isbn):
	sum = 0
	isbn = isbn.replace("-","").replace(" ","")
	# in caso di isbn13
	if len(isbn) == 13:
		for d, i in enumerate(isbn):
			if (int(d) + 1) % 2 != 0:
				sum += int(i)
			else:
				sum += int(i) * 3
		if sum % 10 == 0:
			return True
		else:
			return False
	# in caso di isbn10
	elif len(isbn) == 10:
		if isbn[-1] == "X" or "x": #a final x stands for 10
			isbn = list(isbn) #a string object is immutable
			isbn[-1] = 10
		for d, i in enumerate(isbn[::-1]):
			sum += (int(d)+1) * int(i)
		if (sum % 11) == 0:
			return True
		else:
			return False
	else:
		return False

if __name__ == "__main__":
	if is_valid(sys.argv[1]):
		print(sys.argv[1],"\t", "is a valid ISBN")
	else:
		print(sys.argv[1],"\t" ,"is NOT a valid ISBN")