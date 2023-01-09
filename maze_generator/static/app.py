from flask import Flask, jsonify
import requests


static = Flask(__name__)

requests.put(url = 'http://fa22-cs340-adm.cs.illinois.edu:34999/addMG', json={'name': 'static(this way)', 'url': 'http://fa22-cs340-127.cs.illinois.edu:6002/', 'author':'Jerry Guo', 'weight': 0.7})


@static.route('/generate', methods=["GET"])
def GET_encoded_maze():
    maze_encoded = {"geom": ['ba8088a','4046442','5044406','0000200','5444646','5664406','3220226']}
  #   "extern": {
  #   "-1_0": { "geom": ['988088c','1000024','5644444','4046440','1020204','1022204','3220226'] },
  #   "-1_1": { "geom": ['988088c','5200464','5446404','0000020','5646464','5006024','3220226'] },
  #   "1_0": { "geom": ['9aa0aac','1400404','1620404','0220220','1404224','1620264','3220226'] },
  #   "0_-1": { "geom": ['9a8288c','5246004','1220024','4444440','1202224','5602224','3620226'] }
  # }}
    return jsonify(maze_encoded), 200




# if __name__ == "__main__":
#     static.run(host='0.0.0.0',port = 6002, debug=False,use_reloader=False)