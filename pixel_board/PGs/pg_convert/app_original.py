from pixelation import pixelation

from flask import Flask, jsonify, render_template, request
import requests
import random
import json
import sys
 
app = Flask(__name__)

target_modifications = dict()
# defend_mode = 0
 
 
 
def activate_mg(filename, width, height):

    palette = []
    print("The function has been called.")
    #check if someone else is editing the canvas
    while True:
        requests.post("http://127.0.0.1:34000/get_url", json = {"url": "http://127.0.0.1:34001/"})
        r = requests.get("http://127.0.0.1:34000/settings")
        # print(r.status_code)
        # print(r.content)
        canvas_settings = r.json()
        if canvas_settings["availibility"] == 1:
            break
    
    #notify the canvas the user is now editing the canvas
    requests.post("http://127.0.0.1:34000/notify_in_use")
    
    palette = canvas_settings['palette']
    converted_image = pixelation(filename, width, height, palette)
    # print(converted_image)
    current_canvas = ((requests.get("http://127.0.0.1:34000/pixels")).json())["pixels"]
    # print("current canvas is:",current_canvas)
    # if the PG's pattern hasn't been set
    if len(target_modifications) == 0:
        #record the modifications
        
        # start_point_x = random.randint(0, canvas_settings["width"]-100)
        # start_point_y = random.randint(0, canvas_settings["height"]-100)
        start_point_x = 0
        start_point_y = 0

        for i in range(height):
            for j in range(width):
                # print("\nThe current index is:", (j,i))
                if current_canvas[i][j] != converted_image[i][j]:
                    # print("Hey we find the difference!")
                    target_modifications[f"{start_point_y+i},{start_point_x+j}"] = palette[converted_image[i][j]]
        # print("\npixels to be changed:", target_modifications)
                    
    
        #notify the canvas the user is now done with editing the canvas
        requests.put("http://127.0.0.1:34000/get_changes",json=target_modifications)
        requests.post("http://127.0.0.1:34000/notify_done")
        
    
    # if the PG's pattern has been set, check for pixels need for defend
    else:
        # defend_mode = 1
        pixels_to_defend = dict()
        current_canvas = (requests.get("http://127.0.0.1:34000/pixels").json())['pixels']
        for position in target_modifications.keys():
            if current_canvas[position[0]][position[1]] != target_modifications[position]:
                pixels_to_defend[position] = target_modifications[position]
    
        #notify the canvas the user is now done with editing the canvas
        requests.post("http://127.0.0.1:34000/notify_done", json = {'url' :"http://127.0.0.1:34001/"})
        requests.put("http://127.0.0.1:34000/get_changes",json=pixels_to_defend)
 
       
 
 
 
 
 
 
 
if __name__ == "__main__":
    argu = sys.argv
    print (argu)
    activate_mg(argu[1],int(argu[2]),int(argu[3]))
    
    app.run(port=34001, host='0.0.0.0')