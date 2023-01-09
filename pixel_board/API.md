# API.md

# Overview

The theme of my pixel board is "Nightfall Lighting", which randomly assigns one of (Black, White,  Bitter Chocolate Bark, #EFDFA1(Cream Orange), Majolica Blue, #4C6D76(a dark shade of cyan with hints of green)) to each player. On the other hand, the pixel board accomplishes rate limitation by making the PGs edit one pixel every 0.03 second, and only allows the same PG send editing request once every 20 seconds. There can only be 5 PGs editing the board at the same time. The PG was designed to draw rectangles on the pixel board with the its assigned color.

# Technical Details: Middleware & PGs

- POST/get_url : The currently connected PG share its URL with the middleware so that the middleware can track how long has past since the PG's most recent request.
- GET/settings: The middleware share the pixel board's settings(width, height, availible colors) to the PG connected to it. Moreover, this API will check for number of users that are editing the board simutaneously at that time as well as how long since the PG's last request to determine whetehr the PG is allowed to make its modifications.
- GET/pixels: The middleware shares the current state of the pixel board with the PG.
- POST/notify_in_use: A PG may use this API to notify the middleware that it is going to start editing the pixel board.
- POST/notify_done: A PG may use this API to notify the middleware that it has finished its modification. The url and time will also be sent to the middleware for recording.
- PUT/get_changes: This API helps the middleware get information of which particular pixels are going to be changed by the PG to what color. There will be a 0.03s interval betwwen each modification to each pixel.


# Technical Details: Middleware & Frontend

- GET / : render the frontend page of the pixel board by a HTML template. I didn't change anything in it.

# Add/Remove PG
PGs will be added to/removed from the middleware by their unique URL, and be save into/removed from a list. 

# Run The Pixel Board

First, execute the "python app.py" command in the main directory to run the middleware.
Then, navigate to the "PGs" directory, and execute the "python app.py" command again to start a PG.

Python libraries needed:
- flask
- requests
- time
- datetime
- random
- json

Service needed:
- docker

# Defend Mode
I have already implemented(but commented it out) part of week2's PG defending function. Basically, if a PG found itself has already drew something previously, it will request the current board and its previous edited pixels. If any pixel's color has been changed, it will make adjustment to the color of that pixel. I believe letting the PG check the aprticular pixels instead of the whole board is more efficient.

# Image Drawing
Navigate to the pg_convert directory and add your favorite image, then run the following command to use the new PG:
- python app.py image_path image_width image_height

The upleft corner of the image will be at (0,0) on the board.





