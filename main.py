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

def brightness_add(image, value):
	image = np.asarray(image).astype('uint16')
	image = image+value
	image = np.clip(image, 0, 255)
	new_image = image.astype('uint8')

	return new_image

def brightness_addcv(image, value):
    new_image = cv.add(image, value)
    return new_image

def brightness_subtraction(image, value):
	image = image.astype('uint16')
	image = image-value
	image = np.clip(image, 0, 255)
	new_image = image.astype('uint8')
	return new_image


def brightness_subtractioncv(image, value):
    new_image = cv.subtract(image, value)
    new_image = np.clip(new_image, 0, 255)
    return new_image

def brightness_multiplication(image, value):
    image = image.astype('uint16')
    image = image*value
    image = np.clip(image, 0, 255)
    new_image = image.astype('uint8')
    return new_image

def brightness_multiplicationcv(image, value):
    new_image = cv.multiply(image, value)
    new_image= np.clip(new_image, 0, 255)
    return new_image


def brightness_divide(image, value):
    image = image.astype('uint16')
    image = image/value
    image = np.clip(image, 0, 255)
    new_image = image.astype('uint8')
    return new_image

def brightness_dividecv(image, value):
	new_image = cv.divide(image, value)
	new_image = np.clip(new_image, 0, 255)
	return new_image

def bitwise_and(image1, image2):
    bit_and = cv.bitwise_and(image1, image2)
    return bit_and

def bitwise_and_nocv(image1, image2):
	bit_and = image1 & image2
	return bit_and

def bitwise_or(image1, image2):
    bit_or = cv.bitwise_or(image1, image2)
    return bit_or

def bitwise_or_nocv(image1, image2):
	bit_or = image1 | image2
	return bit_or

def bitwise_not(image):
    bit_not = cv.bitwise_not(image)
    return bit_not

def bitwise_not_nocv(image):
	bit_not = ~image
	return bit_not

def bitwise_xor(image1, image2):
    bit_xor = cv.bitwise_xor(image1, image2)
    return bit_xor

def bitwise_xor_nocv(image1, image2):
	bit_xor = image1 ^ image2
	return bit_xor

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

@app.route('/brightness/<filename>', methods=['GET', 'POST'])
def brightnessImage(filename):
	r, g, b = getRGBfromImage(filename)

	operation = request.form['operation']
	method = request.form['method']

	# get the dimensions of the image
	image = cv.imread("static/uploads/{}".format(filename))
	reso = image.shape
	width = reso[1]
	length = reso[0]
	# get the value of brightness
	brightness = int(request.form['brightness'])
	# check if the method is cv or not
	if method == 'opencv':
		print('menggunakan cv')
		if operation == 'add':
			new_image = brightness_addcv(image, brightness)
		elif operation == 'substract':
			new_image = brightness_subtractioncv(image, brightness)
		elif operation == 'multiply':
			new_image = brightness_multiplicationcv(image, brightness)
		elif operation == 'divide':
			new_image = brightness_dividecv(image, brightness)
		else:
			new_image = image
	else:
		print('tidak menggunakan cv')
		if operation == 'add':
			new_image = brightness_add(image, brightness)
		elif operation == 'substract':
			new_image = brightness_subtraction(image, brightness)
		elif operation == 'multiply':
			new_image = brightness_multiplication(image, brightness)
		elif operation == 'divide':
			new_image = brightness_divide(image, brightness)
		else:
			new_image = image

	new_filename = "brightness-" + filename
	# save the image
	cv.imwrite("static/uploads/{}".format(new_filename), new_image)
	return render_template('brightness.html', filename=filename, brightness=new_filename)

@app.route('/brightness/display/<filename>')
def display_brightness_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/bitwise')
def bitwise():
	return render_template('bitwise.html')

@app.route('/bitwise', methods=['POST'])
def upload_bitwise():
	if 'image1' not in request.files or 'image2' not in request.files:
		return redirect(request.url)

	image_1 = request.files['image1'] 
	image_2 = request.files['image2']

	if image_1.filename == None or image_2.filename == None:
		return redirect(request.url)

	if image_1 and allowed_file(image_1.filename) and image_2 and allowed_file(image_2.filename):
		# save the file to the uploads folder
		if image_1 and image_2:
			filename1 = secure_filename(image_1.filename)
			image_1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
			filename2 = secure_filename(image_2.filename)
			image_2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
			# flash message to the user
			print('Image successfully uploaded and displayed below')
			# return the template with the filename and original image
			return render_template('bitwise.html', image1=filename1, image2=filename2)
	else:
		print('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)


@app.route('/bitwise/<filename1>/<filename2>', methods=[ 'GET','POST'])
def bitwiseImage(filename1, filename2):
	# get the value of bitwise operation
	bitwise = request.form['bitwise']
	operation = request.form['operation']
	# get the images
	image1 = cv.imread("static/uploads/{}".format(filename1))
	image2 = cv.imread("static/uploads/{}".format(filename2))

	#resize the images to the same size
	image1 = cv.resize(image1, (200,200))
	image2 = cv.resize(image2, (200,200))

	if operation == 'manual':
		print("using manual")
		if bitwise == 'and':
			bitwise = bitwise_and_nocv(image1, image2)
		elif bitwise == 'or':
			bitwise = bitwise_or_nocv(image1, image2)
		elif bitwise == 'xor':
			bitwise = bitwise_xor_nocv(image1, image2)
		elif bitwise == 'not':
			bitwise = bitwise_not_nocv(image1)
		else:
			bitwise = bitwise_not_nocv(image1)

	else:
		print("using cv")
		if bitwise == 'and':
			bitwise = bitwise_and(image1, image2)
		elif bitwise == 'or':
			bitwise = bitwise_or(image1, image2)
		elif bitwise == 'xor':
			bitwise = bitwise_xor(image1, image2)
		elif bitwise == 'not':
			bitwise = bitwise_not(image1)
		else:
			bitwise = bitwise_not(image1)
	# save the image
	new_filename = "bitwise-" + filename1 + "-" + filename2
	cv.imwrite("static/uploads/{}".format(new_filename), bitwise)
	print(new_filename)
	return render_template('bitwise.html', image1=filename1, image2=filename2, result=new_filename)


@app.route('/bitwise/display/<filename>')
def display_bitwise_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
	app.run(debug=True)

