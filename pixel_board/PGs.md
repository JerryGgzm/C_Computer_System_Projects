## Notice: The shared middleware is not in this directory, please copy the PGs folder into the shared middleware directory to use them. 
### PGs are now updated to the week3 version

The default PG was designed to draw rectangles at random places on the pixel board with a color randomly selected from the palette.
Connect to the shared middleware, and then navigate to the PGs directory, run the following command to use the default PG:
python app.py


Connect to the shared middleware, and then navigate to the PGs/pg_convert directory and add your favorite image, then run the following command to use the new PG:
- "python app.py image_path image_width image_height"
- you can test the PG with the default command "python app.py chimitan2_resize.png 100 100"
- The upleft corner of the image will be at (0,0) on the board.
