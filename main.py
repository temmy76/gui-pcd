import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2 as cv

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getRGBfromImage(filename):
	r = []
	g = []
	b = []
	image = cv.imread("static/upload/{}".format(filename))
	image = cv.resize(image, (200,200))
	reso = image.shape
	width = reso[1]
	length = reso[0]
	for i in range(0,length-1):
		for j in range(0,width-1):
			B, G, R = image[i, j]
			b.append(B)
			g.append(G)
			r.append(R)
	
	return r, g, b


	
@app.route('/')
def upload_form():
	return render_template('template.html')

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
		return render_template('template.html', filename=filename)
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
	
	return render_template('template.html', filename=filename, red=r, green=g, blue=b)
	
@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/grayscale/<filename>', methods=['POST'])
def grayscaleImage(filename):
	r, g, b = getRGBfromImage(filename)
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	cv.imwrite("static/uploads/{}".format(filename), gray)
	return redirect(url_for('static', filename='uploads/grayscale/' + filename), code=301)



if __name__ == "__main__":
	app.run(debug=True)

