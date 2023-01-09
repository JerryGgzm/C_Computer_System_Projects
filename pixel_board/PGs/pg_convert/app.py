# updated to the shared-middleware version

from pixelation import pixelation
 
from flask import Flask, jsonify, render_template, request
import requests
import random
import json
import sys
 
app = Flask(__name__)
 
target_modifications = dict()
current_board = []
current_board_hash = 'haha'

# midware running on: http://127.0.0.1:5000
 
def activate_pg(filename, width, height):
 
    palette = []
 
    pg_info = {
        "name": "Here Comes Chimitan!",
        "author": "Jerry Guo(zemingg2)",
        "secret": "PG+emVtaW5nZzI=+Z48we91hAYJ91k8Z2oAq50OV7-IDbE"
    }
   
 
    register_response = requests.put("http://127.0.0.1:5000/register-pg", json = pg_info)
 
    # register the current pg on the midware
    if register_response.status_code != 400:
        pg_identity_token = register_response.json()["id"]
    else:
        return register_response.content["error"]
 
    # get the midware's settings
    settings_response = requests.get("http://127.0.0.1:5000/settings")
    canvas_settings = settings_response.json()
    palette = canvas_settings['palette']
    print("palette is ", canvas_settings['palette'])
    board_width = canvas_settings['width']
    board_height = canvas_settings['height']
    print(f"\nThe size of the board is {board_height},{board_width}")
    converted_image = pixelation(filename, width, height, palette)
 
    current_board_hash = 'haha'

    # current_board_response = requests.get("http://127.0.0.1:5000/pixels", headers = {"if_none_match": current_board_hash}, json={"id":pg_identity_token})
    #check if someone else is editing the canvas
    while True:
        
        current_board_response = requests.get("http://127.0.0.1:5000/pixels", headers = {"if_none_match": current_board_hash}, json={"id":pg_identity_token})
        # current_board_response = requests.get("http://127.0.0.1:5000/pixels")
        #check for any update on the board
        if current_board_response.status_code == 304:
            # if the board has not been changed, continue working on the current target_modifications
            print("\nThe board has not been changed.")

            if len(target_modifications) == 0:
                continue

            next_to_modify = list(target_modifications.keys())[0]
            modification = {
                "id": pg_identity_token,
                "row": int(next_to_modify.split(",")[0]),
                "col": int(next_to_modify.split(",")[1]),
                "color": palette.index(target_modifications[next_to_modify])
            }
            print(f"\ndrawing color is {target_modifications[next_to_modify]}")
            modification_response = requests.put("http://127.0.0.1:5000/update-pixel", json = modification)
            if modification_response.status_code == 200:
                target_modifications.pop(next_to_modify)


        else:
            # if the board has been changed, fetch the new board, and then find the new target_modifications to work on
            print("\changed")
            if current_board_response.status_code != 429:
                current_board_hash = current_board_response.headers["ETag"]
                # print(current_board_response.json())
                current_board = current_board_response.json()['pixels']
                # If the pg has not drawn anything yet
                start_point_x = 0
                start_point_y = 0
                proper_width = min(board_width, width)
                proper_height = min(board_height, height)
                for i in range(proper_height):
                    for j in range(proper_width):
                        if current_board[i][j] != converted_image[i][j]:
                            target_modifications[f"{start_point_y+i},{start_point_x+j}"] = palette[converted_image[i][j]]

                print("\npixels to be changed", len(target_modifications))
                if len(target_modifications) == 0:
                    continue

                next_to_modify = list(target_modifications.keys())[0]
                modification = {
                    "id": pg_identity_token,
                    "row": int(next_to_modify.split(",")[0]),
                    "col": int(next_to_modify.split(",")[1]),
                    "color": palette.index(target_modifications[next_to_modify])
                }
                print(f"\ndrawing color is {target_modifications[next_to_modify]}")
                modification_response = requests.put("http://127.0.0.1:5000/update-pixel", json = modification)
                if modification_response.status_code == 200:
                    target_modifications.pop(next_to_modify)
            
 
 
 
if __name__ == "__main__":
    argu = sys.argv
    print (argu)
    activate_pg(argu[1],int(argu[2]),int(argu[3]))
   
    app.run(port=34001, host='0.0.0.0')
 
 
 
