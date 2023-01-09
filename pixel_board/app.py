"""A server that provides a canvas to the users.
http://127.0.0.1:34000/ """
 
 
 
 
from flask import Flask, jsonify, render_template, request
import requests
import time
from datetime import datetime
 
app = Flask(__name__)
 
 
# Canvas Attributes:
 
canvas = {
    "canvas_width": 200,
    "canvas_height": 200
}
 
# palette = ["#FFFFFF", "#0F0705", "#4E2100", "#EFDFA1", "#253F56", "#4C6D76", "#000000"]
palette = ['C84113','13294B','FFA069','FFD0B4','FFFFFF','B34404','662702','0D1D35','717F93','B8BFC9','08101E']
current_canvas = [[0 for _ in range(canvas["canvas_width"])] for _ in range(canvas["canvas_height"])]
change_times = [[0]*canvas["canvas_width"]]*canvas["canvas_height"]
history_canvas = [current_canvas]
availibility = 1
user_count = 0
connected_PGs = dict()
waiting_time = 20
current_client_url = {'url':""}
 
@app.route('/', methods=["GET"])
def GET_index():
    '''Route for "/" (frontend)'''
    return render_template("index.html")
 
 
@app.route('/get_url', methods = ['POST'])
def GET_PG_url():
    global current_client_url
    current_client_url['url'] = (request.json)['url']
    return "okay", 200
   
 
 
@app.route('/settings', methods = ['GET'])
def GET_server_setting():
    current_user_availibility = 1
    # r = request.get_json()
    client_url = current_client_url['url']
    # print(r)
 
    # Rate Limited: check if it has been enough time past since the user's last request
    if client_url in connected_PGs:
        time_difference = (datetime.now() - connected_PGs[client_url]).total_seconds()
        if time_difference < waiting_time:
            current_user_availibility = 0
 
 
    setting = \
    {
    "width": canvas["canvas_width"],
    "height": canvas["canvas_height"],
    "palette": palette,
    "availibility": availibility and current_user_availibility
    }
    return jsonify(setting), 200
 
 
 
@app.route('/pixels', methods = ['GET'])
def GET_current_pixels():
    board = {
        "pixels": current_canvas
    }
    status_code = 200
    return jsonify(board), status_code
 
 
# notify the server a user is drawing
@app.route('/notify_in_use', methods = ['POST'])
def change_availibility_in_use():
    global user_count, availibility
    user_count += 1
    if user_count == 5:
        availibility = 0
    return "okay", 200
 
 
# notify the server it is free
@app.route('/notify_done', methods = ['POST'])
def change_availibility_free():
    global user_count, availibility
    user_count -= 1
    availibility = 1
 
    client_url = current_client_url['url']
 
    connected_PGs[client_url] = datetime.now()
    print(f"PGs URL: {client_url}")
    return "okay", 200
 
 
@app.route('/get_changes', methods = ['PUT'])
def update_canvas():
    updates = request.get_json()
    #if there is availible updates, archive the current canvas
    if (len(updates) != 0):
        history_canvas.append(current_canvas)
 
    for position in updates.keys():
        pos = position.split(",")
        current_canvas[int(pos[0])][int(pos[1])] = palette.index(updates[position])
        # current_canvas[int(pos[0])][int(pos[1])] = updates[position]
        change_times[int(pos[0])][int(pos[1])] += 1
        time.sleep(0.0003)
    return "okay", 200

 
 
if __name__ == "__main__":
    app.run(port=34000, host='0.0.0.0')
 
# How do we ensure the image persists across restarts of the app? (What data store(s) should we use instead of variables stored in memory?)
