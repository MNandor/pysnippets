#!/bin/python3 -i


USE_TERMINAL_WIDTH = True
# Read terminal size
defaultWidth = -1
if USE_TERMINAL_WIDTH: 
	import os

# Print a list, nicely formatted
def prln(l,  width=-1, separator='|'):

	if USE_TERMINAL_WIDTH and width == -1:
		try:
			width = os.get_terminal_size().columns
		except:
			width = 1e4
	elif width == -1:
		width = 1e4
	
	SEPLEN = len(separator)

	# Count Columns
	columnCount = max([len(x) for x in l])

	# Calculate the maximum width of each column
	columnWidths = []
	for column in range(columnCount):
		# If not all data is the same length,
		# Ignore lines that don't span to this column
		relevant = [x for x in l if len(x) > column]
		
		maxWidth = max([len(str(x[column])) for x in relevant])
		columnWidths += [maxWidth]

	# If we can't fit, we need to truncate some columns
	availableChars = width - (columnCount + 1)*SEPLEN
	if sum(columnWidths) > availableChars:
		availableForOne = availableChars / columnCount
		totalToSplit = availableChars
		splitAmong = []

		# Columns that take up less than the average
		# Get to keep their width
		for i, w in enumerate(columnWidths):
			if w <= availableForOne:
				totalToSplit -= w	
			else:
				splitAmong += [i]

		reducedWidth = totalToSplit // len(splitAmong)

		for offender in splitAmong:
			columnWidths[offender] = reducedWidth

	
	# Actually do the printing
	vertline = lambda: 	print('-'*(sum(columnWidths)+(columnCount+1)*SEPLEN ))

	vertline()
	for line in l:
		print(separator, end='')
		for c in range(columnCount):
			w = columnWidths[c]
			item = line[c]

			# Ints are right justified
			if isinstance(item, int):
				item = str(item)

				if len(item) < w:
					item = item.rjust(w, ' ')

			# Floats shout display parts before the decimal point
			# And then as many decimals as possible
			elif isinstance(item, float):
				digits = len(str(int(item)))
				decimals = max(w-1-digits, 0)
				item = f'{item:{w}.{decimals}f}'

			# Treat everything else as a string
			else:
				item = str(item)
				item = item.ljust(w, ' ')


			# In all cases use the same shortening for now
			if len(str(item)) > w:
				item = str(item)[:w-3]+'.'*min(3, w)

			print(item, end=separator)
		print()
	vertline()
	





if __name__ == '__main__':

	a = [
	(5, "asd"),
	(55555555555555, "a", "asd"),
	("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "asd", "asd")
	]

	b = [
	('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'The quick, brown fox jumps over the lazy dog.'),
	('', 'The quick, brown fox jumps over the lazy dog.'),
	]

	prln(a, 80)
	prln(a, 40, ' | ')
	prln(a)
	prln(b, 80)
	prln(b, 80, separator="____")
