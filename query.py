import sqlite3
import sys
import re
import copy
import random
import os

conn = sqlite3.connect('words.db')
c = conn.cursor()
def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')
def print_table(table):
  out = "\n"
  for row in table:
    for col in row:
      out += col
    out += "\n"
  print out
def is_word(str):
  p = re.compile('^[a-zA-Z]+$')
  m = p.match(str)
  if m:
    return True
  return False
def is_int(str):
  p = re.compile('^[0-9]+$')
  m = p.match(str)
  if m:
    return True
  return False
def no_underscore(str):
  p = re.compile('_+')
  m = p.match(str)
  if m:
    return False
  return True
def get_match_words(str):
  results = c.execute("SELECT word FROM words WHERE word LIKE '"+str+"'")
  words = [];
  for row in results:
    words.append(row[0])
  return words
def check_possible(table):
  # check rows
  for y in table:
    row = ""
    for x in y:
      row += x
    if no_underscore(row):
      continue
    words = get_match_words(row)
    if len(words) == 0:
      return False
  # check columns
  return True
def add_word_row(table, row):
  if(row >= len(table)):
    return table
  word = ""
  for x in table[row]:
    word += x
  possible_words = get_match_words(word)
  random.shuffle(possible_words)
  for item in possible_words:
    new_table = copy.deepcopy(table)
    fill_row(new_table,item,row)
    clear_screen()
    print_table(new_table)
    new_table = add_word_col(new_table, row)
    if (new_table != False):
      return new_table
  return False
def add_word_col(table, col):
  word = ""
  for y in table:
    word += y[col]
  possible_words = get_match_words(word)
  random.shuffle(possible_words)
  for item in possible_words:
    new_table = copy.deepcopy(table)
    fill_col(new_table,item,col)
    clear_screen()
    print_table(new_table)
    new_table = add_word_row(new_table, col+1)
    if (new_table != False):
      return new_table
  return False    
    

def fill_row(table,word,row):
  x = 0
  for char in word:
    table[row][x] = char
    x += 1
def fill_col(table,word,col):
  x = 0
  for char in word:
    table[x][col] = char
    x += 1

# Determine Board Size
if len(sys.argv) == 2:
  if is_word(sys.argv[1]):
    keyword = sys.argv[1]
    width = len(keyword)
    height = width
  elif is_int(sys.argv[1]):
    width = int(sys.argv[1])
    height = width
  else:
    width = 4
    height = 4
else:
  width = 4
  height = 4

# Create Board
table = []
for y in range(0,height):
  table.append([])
  for x in range(0,width):
    table[y].append("_")

if 'keyword' in globals():
  for x in range(0,height):
    test_table = copy.deepcopy(table)
    fill_row(test_table,keyword,x)
    if(check_possible(test_table)):
      table = copy.deepcopy(test_table)
      break
  else:
    sys.exit("Not possible")

table = add_word_row(table,0)
new_table = copy.deepcopy(table)


conn.commit()
conn.close()