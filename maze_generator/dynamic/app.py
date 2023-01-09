from flask import Flask, jsonify
import requests
from random import choices
from random import randint

dynamic = Flask(__name__)

requests.put(url = 'http://fa22-cs340-adm.cs.illinois.edu:34999/addMG', json={'name': 'dynamic(Each maze is a word, it a narrative horror game!)', 'url': 'http://fa22-cs340-127.cs.illinois.edu:6003/', 'author':'Jerry Guo', 'weight': 1})

@dynamic.route('/generate', methods=["GET"])
def GET_encoded_maze():
    maze_encoded = {"geom": generate_a_maze()}
    return jsonify(maze_encoded), 200


def generate_a_maze():

  start_states = [
  ['988088c','1040004','1060204','0444400','1464604','1000004','3220226'], #do
  ['988088c','1202424','5444404','4442420','1020004','1400604','3220226'], #not
  ['9a8088c','5640004','5042004','0002000','1046464','1044044','3220226'], #play
  ['9aa088c','1404604','1404404','0000200','1404204','1400604','3220226'], #this
  ['9aa0a8c','5444604','5444404','0200200','1404204','1424204','3220226'], #maze
  ['988088c','5240024','5642464','0000000','1206004','5646004','3220226'], #blood
  ['9aa0aac','1400404','1620404','0220220','1404224','1620264','3220226'], #run
  ['9a8288c','5246004','1220024','4444440','1202224','5602224','3620226']] #hurry

  init = randint(0,7)

  init_state = start_states[init]
  new_state = []

  for row in init_state:
    curr_row = row
    for ind, cell in enumerate(row):
      if cell == '0':
         curr_row = row[0:ind] + generate_single_cell() + row[ind+1:]
    new_state.append(curr_row)

  return new_state



def generate_single_cell():
  bit_1 = choices([0,1], [0.6,0.4])[0]
  bit_2 = choices([0,1], [0.6,0.4])[0]
  bit_3 = choices([0,1], [0.6,0.4])[0]
  bit_4 = choices([0,1], [0.6,0.4])[0]
  bin_literal = f'0b{bit_1}{bit_2}{bit_3}{bit_4}'
  print(bin_literal)
  hex_literal = hex(int(bin_literal, 2))
  return hex_literal[2]




# if __name__ == "__main__":
#     dynamic.run(host='0.0.0.0',port=6003, debug=False,use_reloader=False)