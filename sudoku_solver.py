"""
	Sudoku Solver by Tim Huisman

	Write your sudoku in input.txt in the following form (spaces are NOT omitted):
	...23.7..
	4....8.26
	.7...1...
	..716.2..
	.........
	..5.423..
	...5...6.
	92.7....5
	..4.19...

	Then run the program.

	NOTE: no external informational resources were used (except for test sudoku's),
	so there is no guarantee of success.
"""

f = open("./input.txt")
g = [[(int(val) if val in "123456789" else set(range(1,10))) for val in row[:9]] for row in f.read().split()[:9]]

def exists_empty_cell():
	for row in g:
		for val in row:
			if type(val) == set:
				return True
	return False

def transpose_sudoku():
	global g
	g = [[g[ix][iy] for ix in range(9)] for iy in range(9)]

# see if there is any direct conflict in rows/columns/blocks
def update_direct_possibilities(y, x):
	if type(g[y][x]) == int:
		return
	
	# row
	for ix in range(9):
		if type(g[y][ix]) == int:
			g[y][x].discard(int(g[y][ix]))
	
	# column
	for iy in range(9):
		if type(g[iy][x]) == int:
			g[y][x].discard(int(g[iy][x]))
	
	# block
	by, bx = y//3*3, x//3*3
	for iy in range(by, by+3):
		for ix in range(bx, bx+3):
			if type(g[iy][ix]) == int:
				g[y][x].discard(int(g[iy][ix]))

# take a look at both the line-common and block-common integers, and remove possibilities if amount is 6
def update_duality_possibilities():
	for by in range(0, 9, 3):
		for bx in range(0, 9, 3):
			# horizontal
			for iy in range(by, by+3):
				vals = set()
				
				for jy in range(by, by+3):
					if iy != jy:
						for jx in range(bx, bx+3):
							if type(g[jy][jx]) == int:
								vals.add(g[jy][jx])
				for ix in range(9):
					if ix//3 != bx//3:
						if type(g[iy][ix]) == int:
							vals.add(g[iy][ix])
				
				if len(vals) == 6:
					others = set(range(1, 10)) - vals
					for jy in range(by, by+3):
						if iy != jy:
							for jx in range(bx, bx+3):
								if type(g[jy][jx]) == set:
									g[jy][jx] -= others
					for ix in range(9):
						if ix//3 != bx//3:
							if type(g[iy][ix]) == set:
								g[iy][ix] -= others
			
			# vertical
			for ix in range(bx, bx+3):
				vals = set()

				for jx in range(bx, bx+3):
					if ix != jx:
						for jy in range(by, by+3):
							if type(g[jy][jx]) == int:
								vals.add(g[jy][jx])
				for iy in range(9):
					if iy//3 != by//3:
						if type(g[iy][ix]) == int:
							vals.add(g[iy][ix])
				
				if len(vals) == 6:
					others = set(range(1, 10)) - vals
					for jx in range(bx, bx+3):
						if ix != jx:
							for jy in range(by, by+3):
								if type(g[jy][jx]) == set:
									g[jy][jx] -= others
					for iy in range(9):
						if iy//3 != by//3:
							if type(g[iy][ix]) == set:
								g[iy][ix] -= others

# see if a value has to be in a certain three-cell area, and remove from the possibilites in the rest of the other line/block
def update_three_cell_possibilities():
	for by in range(0, 9, 3):
		for bx in range(0, 9, 3):
			for iy in range(by, by+3):
				# row -> block
				vals = set(range(1, 10))
				
				for ix in range(9):
					if ix//3 != bx//3:
						if type(g[iy][ix]) == int:
							vals.discard(g[iy][ix])
						else:
							vals -= g[iy][ix]
				for jy in range(by, by+3):
					if jy != iy:
						for jx in range(bx, bx+3):
							if type(g[jy][jx]) == set:
								g[jy][jx] -= vals
				
				# block -> row
				vals = set(range(1, 10))
				
				for jy in range(by, by+3):
					if jy != iy:
						for jx in range(bx, bx+3):
							if type(g[jy][jx]) == int:
								vals.discard(g[jy][jx])
							else:
								vals -= g[jy][jx]
				for ix in range(9):
					if ix//3 != bx//3:
						if type(g[iy][ix]) == set:
							g[iy][ix] -= vals
			
			for ix in range(bx, bx+3):
				# column -> block
				vals = set(range(1, 10))
				
				for iy in range(9):
					if iy//3 != by//3:
						if type(g[iy][ix]) == int:
							vals.discard(g[iy][ix])
						else:
							vals -= g[iy][ix]
				for jx in range(bx, bx+3):
					if jx != ix:
						for jy in range(by, by+3):
							if type(g[jy][jx]) == set:
								g[jy][jx] -= vals
				
				# block -> column
				vals = set(range(1, 10))
				
				for jx in range(bx, bx+3):
					if jx != ix:
						for jy in range(by, by+3):
							if type(g[jy][jx]) == int:
								vals.discard(g[jy][jx])
							else:
								vals -= g[jy][jx]
				for iy in range(9):
					if iy//3 != by//3:
						if type(g[iy][ix]) == set:
							g[iy][ix] -= vals

def update_all_possibilities():
	for iy in range(9):
		for ix in range(9):
			update_direct_possibilities(iy, ix)
	update_duality_possibilities()
	update_three_cell_possibilities()

def write_single_value():
	for iy in range(9):
		for ix in range(9):
			if type(g[iy][ix]) == set:
				if len(g[iy][ix]) == 1:
					g[iy][ix] = list(g[iy][ix])[0]
					print(f"Put {g[iy][ix]} at ({ix+1}, {iy+1}): only valid value in that cell")
					return True
	
	return False

def write_single_cell():
	# row
	for iy in range(9):
		for val in range(1, 10):
			contains = []
			for ix in range(9):
				if type(g[iy][ix]) == set:
					if val in g[iy][ix]:
						contains.append(ix)
			if len(contains) == 1:
				g[iy][contains[0]] = val
				print(f"Put {val} at ({contains[0]+1}, {iy+1}): only valid cell (row)")
				return True
	
	# column
	for ix in range(9):
		for val in range(1, 10):
			contains = []
			for iy in range(9):
				if type(g[iy][ix]) == set:
					if val in g[iy][ix]:
						contains.append(iy)
			if len(contains) == 1:
				g[contains[0]][ix] = val
				print(f"Put {val} at ({ix+1}, {contains[0]+1}): only valid cell (column)")
				return True
	
	# block
	for by in range(0, 9, 3):
		for bx in range(0, 9, 3):
			for val in range(1, 10):
				contains = []
				for iy in range(by, by+3):
					for ix in range(bx, bx+3):
						if type(g[iy][ix]) == set:
							if val in g[iy][ix]:
								contains.append([iy, ix])
				if len(contains) == 1:
					g[contains[0][0]][contains[0][1]] = val
					print(f"Put {val} at ({contains[0][1]+1}, {contains[0][0]+1}): only valid cell (block)")
					return True
	
	return False

def sudoku_to_string():
	string = ""
	
	for row in range(9):
		string += " | ".join(" ".join((str(val) if type(val) == int else " ") for val in g[row][ix:ix+3]) for ix in range(0, 9, 3)) + ("\n" if row < 8 else "")
		if row == 2 or row == 5:
			string += (3*"------+-")[:-3]+"\n"
	
	return string

def sudoku_to_string_debug():
	text_width = [0]*9
	for iy in range(9):
		for ix in range(9):
			text_width[ix] = max(text_width[ix], len(str(g[iy][ix])))
	
	result = ""
	
	for iy in range(9):
		for ix in range(9):
			result += str(g[iy][ix]) + " "*(text_width[ix] - len(str(g[iy][ix])) + 1)
		if iy < 8:
			result += "\n"
	
	return result

##########################################

print("\nOriginal:\n" + sudoku_to_string() + "\n\nProcess:")
while exists_empty_cell():
	update_all_possibilities()

	if write_single_value():
		continue©
	if write_single_cell():
		continue
	
	print("I couldn't find a solution to the sudoku, sorry...\nThis is the furtherst I got:")
	print(sudoku_to_string_debug(), end="\n")
	break

print("\nSolution:\n" + sudoku_to_string())