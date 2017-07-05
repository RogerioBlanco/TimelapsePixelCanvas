# TimelapsePixelCanvas

This is a script to create sequential screenshots of the area you want.
#### How you can use this?

Well, first you need Python 2.7 and install this:
* pip install Pillow

##### for windows
if you needs pip 
save from https://bootstrap.pypa.io/get-pip.py
* python get-pip.py

after pip installation

* python -m pip install Pillow

#####After you can execute the code like this:

* ./timelapse_pixel_canvas.py -x 0 -y 0 -s 10
OR
* /timelapse_pixel_canvas.py --start_x 0 --end_x 100 --start_y 0 --end_y 100 -s 20

### What is each parameter? 

* **-s** or **--seconds** it is the time will wait of every screenshot. Default: 60
* **-r** or **--radius** it is the radius of your area you want. Works only with -x and -y. Default: 1
* **-x** it is your point initial axis x
* **-y** it is your point initial axis y
* **--start_x** it is the point X axis what you want to begin. Ex: 156
* **--end_x** it is the point X axis what you want to end. Ex: 200
* **--start_y** it is the point y axis what you want to begin. Ex: -4000
* **-d** or **--directory'** it's the directory you want to put the images.
