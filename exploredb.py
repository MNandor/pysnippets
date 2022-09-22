#!/bin/python3 -i

'''
Python script for exploring and modifying local SQLite databases
'''

import sqlite3
import sys
from prln import prln

# Connect to db
args = sys.argv[1:]

if len(args) < 1:
	print('Please provide database file')
	exit(1)

dbname = args[0]
db = sqlite3.connect(dbname)
cur = db.cursor()

# Table definitions
cur.execute('select * from sqlite_master')
headers = [(x[1], x[4]) for x in cur.fetchall()]
headers = [x for x in headers if x[0] not in ['android_metadata', 'sqlite_sequence']]
tablenames = [x[0] for x in headers if x[1]]
tablefields = [x[1].split('(')[1].split(')')[0].split(',') for x in headers if x[1]]



#  _____                 _   _                 
# |  ___|   _ _ __   ___| |_(_) ___  _ __  ___ 
# | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# |  _|| |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
                                             


def displayHelp():
	print('\nHelp\n')
	print('''
Run any of these functions:

h() - display this help
t(),d() - display table definitions
a() - display all content
su() - display summarized content
se(),sl* - select from table
u(),r()* - run an sql command (such as an update)
c()** - commit to databse file
snap(), ss() - create snapshot
snap(1), ss(1) - display content of snaps[1]

* type sql after calling function
** run this before exiting or changes will be lost


''')

def displayTableDefinitions():
	print('\nTable Definitions\n')
	for i in range(len(tablenames)):
		print(tablenames[i])
		print(', '.join(tablefields[i]))



def displayContent(summarize=False):
	print('\nContent\n')
	for i in tablenames:
		print(i)
		cur.execute('select * from '+i)

		res = cur.fetchall()

		if summarize:
			res = res[-20:]

		prln(res, separator='| ')

		print('\n\n')

def runSql():
	print('note: this can modify db!')
	sql = input()
	cur.execute(sql)

	print('check with s(), commit with c()')


def selectSql():
	print('type sqlite select directly')
	sql = input()
	_select(sql)


def commit():
	db.commit()



	

def _select(sql):
	if not(sql.lower().startswith('select')):
		sql = 'select '+sql

	cur.execute(sql)

	l = cur.fetchall()
	prln(l)




#  ____                        _           _       
# / ___| _ __   __ _ _ __  ___| |__   ___ | |_ ___ 
# \___ \| '_ \ / _` | '_ \/ __| '_ \ / _ \| __/ __|
#  ___) | | | | (_| | |_) \__ \ | | | (_) | |_\__ \
# |____/|_| |_|\__,_| .__/|___/_| |_|\___/ \__|___/
#                   |_|                            


snaps = []
def snap(num = None):
	global snaps

	if snaps == []:
		print('\nRun snap() to create a snapshot')
		print('Or snap(5) to compare current DB with snaps[5]')
		print('Note, snaps[0] was automatically created on startup\n')

	if num == None:
		m = {}
		for table in tablenames:
			cur.execute(f'select * from {table}')
			res = cur.fetchall()
			m[table] = res
		snaps += [m]

		print(f'Created snaps[{len(snaps)-1}]')
	else:
		for table in tablenames:
			cs = snaps[num][table]
			cur.execute(f'select * from {table}')
			res = cur.fetchall()

			print(table+'\n')
			if cs == res:
				continue

			rem = sorted(list(set(cs)-set(res)))
			add = sorted(list(set(res)-set(cs)))

			for a in add: print('+', a)
			for a in rem: print('-', a)

snap()

def edit():
	table = input('Which table to edit?' )
	cur.execute(f'select * from {table}')
	res = cur.fetchall()
	with open('/tmp/exploredb.txt', 'wt') as ofs:
		for row in res:
			for item in row:
				if isinstance(item, str):
					item = f'"{item}"'
				else:
					item = str(item)
				ofs.write(item)
				ofs.write('\t')
			ofs.write('\n')
				



#  __  __       _       
# |  \/  | __ _(_)_ __  
# | |\/| |/ _` | | '_ \ 
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|

h=displayHelp
t=displayTableDefinitions
d=displayTableDefinitions
a = lambda: displayContent(False)
su = lambda: displayContent(True)
se = selectSql
sl = selectSql
r = runSql
u = runSql
c = commit
ss = snap

if __name__ == "__main__":
                      
	displayContent(True)
	displayHelp()
	displayTableDefinitions()
