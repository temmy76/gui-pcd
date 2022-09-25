import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2 as cv
import numpy as np

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getRGBfromImage(filename):
	image = cv.imread("static/uploads/{}".format(filename))
	image = cv.resize(image, (200,200))
	reso = image.shape
	width = reso[1]
	length = reso[0]
	b = []
	g = []
	r = []
	for i in range(0,length-1):
		for j in range(0,width-1):
			B, G, R = image[i, j]
			b.append(B)
			g.append(G)
			r.append(R)
	
	return r, g, b

@app.route('/')
def upload_form():
	return render_template('extractRGB.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('Image successfully uploaded and displayed below')
		return render_template('extractRGB.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/get_rgb/<filename>', methods=['POST'])
def getRGB(filename):
	r = []
	g = []
	b = []
	image = cv.imread("static/uploads/{}".format(filename))
	image = cv.resize(image, (200,200))
	reso = image.shape 
	width = reso[1]
	length = reso[0]
	for i in range(0, length-1):
		for j in range(0, width-1):
			B, G, R = image[i,j]
			b.append(B)
			g.append(G)
			r.append(R)
	
	return render_template('extractRGB.html', filename=filename, red=r, green=g, blue=b)
	
@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/grayscale')
def grayscale():
	return render_template('grayscale.html')

@app.route('/grayscale/<filename>', methods=['POST'])
def grayscaleImage(filename):
	r, g, b = getRGBfromImage(filename)
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	cv.imwrite("static/uploads/{}".format(filename), gray)
	return redirect(url_for('static', filename='uploads/grayscale/' + filename), code=301)

# create route that render brightness.html template
@app.route('/brightness')
def brightness():
	return render_template('brightness.html')

@app.route('/brightness', methods=['POST'])
def upload_brightness():
	# check if there is a file in the request
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	# get the file from the request
	file = request.files['file']
	# check if the file is empty
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	# check if the file is allowed
	if file and allowed_file(file.filename):
		# save the file to the uploads folder
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		# flash message to the user
		flash('Image successfully uploaded and displayed below')
		# return the template with the filename and original image
		return render_template('brightness.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

# create route for change the brightness of image
@app.route('/brightness/<filename>', methods=['POST'])
def brightnessImage(filename):
	r, g, b = getRGBfromImage(filename)
	# get the dimensions of the image
	image = cv.imread("static/uploads/{}".format(filename))
	reso = image.shape
	width = reso[1]
	length = reso[0]
	# get the value of brightness
	brightness = int(request.form['brightness'])
	# create numpy array for store the new value of brightness
	new_r = []
	new_g = []
	new_b = []
	# loop for change the brightness of image
	for i in range(0, len(r)):
		new_r.append(r[i] + brightness)
		new_g.append(g[i] + brightness)
		new_b.append(b[i] + brightness)
	# create numpy array for store the new value of brightness
	new_image = np.zeros((length, width, 3), np.uint8)
	# loop for change the brightness of image
	for i in range(0, length-1):
		for j in range(0, width-1):
			new_image[i,j] = [new_b[i], new_g[i], new_r[i]]
	new_filename = "brightness-" + filename
	# save the image
	cv.imwrite("static/uploads/{}".format(new_filename), new_image)
	return render_template('brightness.html', filename=filename, brightness=new_filename)

# create route for displaying brightness image
@app.route('/brightness/display/<filename>')
def display_brightness_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/bitwise')
def bitwise():
	return render_template('bitwise.html')

if __name__ == "__main__":
	app.run(debug=True)

