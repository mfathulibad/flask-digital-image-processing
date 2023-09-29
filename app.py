import numpy as np
from PIL import Image
import image_processing
import os
from flask import Flask, render_template, request, make_response
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile
import threading
import random

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("dashboard.html", file_path="img/image_here.jpg")


@app.route("/general")
@nocache
def general():
    return render_template('general.html')


@app.route("/positioning")
@nocache
def positioning():
    return render_template('positioning.html')

@app.route("/lighting")
@nocache
def lighting():
    return render_template('lighting.html')

@app.route("/analyze")
@nocache
def analyze():
    return render_template('analyze.html')

@app.route("/image_filtering")
@nocache
def image_filtering():
    return render_template('image_filtering.html')

@app.route("/about")
@nocache
def about():
    return render_template('about.html')

@app.route("/filter")
@nocache
def quiz():
    return render_template('filter.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("dashboard.html", file_path="img/img_now.jpg")


@app.route("/normal", methods=["POST"])
@nocache
def normal(): 
    copyfile("static/img/img_normal.jpg", "static/img/img_now.jpg")
    return render_template("general.html", file_path="img/img_now.jpg")


@app.route("/grayscale", methods=["POST"])
@nocache
def grayscale():
    image_processing.grayscale()
    return render_template("general.html", file_path="img/img_now.jpg")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    return render_template("general.html", file_path="img/img_now.jpg")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    return render_template("general.html", file_path="img/img_now.jpg")


@app.route("/move_left", methods=["POST"])
@nocache
def move_left():
    image_processing.move_left()
    return render_template("positioning.html", file_path="img/img_now.jpg")


@app.route("/move_right", methods=["POST"])
@nocache
def move_right():
    image_processing.move_right()
    return render_template("positioning.html", file_path="img/img_now.jpg")


@app.route("/move_up", methods=["POST"])
@nocache
def move_up():
    image_processing.move_up()
    return render_template("positioning.html", file_path="img/img_now.jpg")


@app.route("/move_down", methods=["POST"])
@nocache
def move_down():
    image_processing.move_down()
    return render_template("positioning.html", file_path="img/img_now.jpg")


@app.route("/brightness_addition", methods=["POST"])
@nocache
def brightness_addition():
    image_processing.brightness_addition()
    return render_template("lighting.html", file_path="img/img_now.jpg")


@app.route("/brightness_substraction", methods=["POST"])
@nocache
def brightness_substraction():
    image_processing.brightness_substraction()
    return render_template("lighting.html", file_path="img/img_now.jpg")


@app.route("/brightness_multiplication", methods=["POST"])
@nocache
def brightness_multiplication():
    image_processing.brightness_multiplication()
    return render_template("lighting.html", file_path="img/img_now.jpg")


@app.route("/brightness_division", methods=["POST"])
@nocache
def brightness_division():
    image_processing.brightness_division()
    return render_template("lighting.html", file_path="img/img_now.jpg")


@app.route("/histogram_equalizer", methods=["POST"])
@nocache
def histogram_equalizer():
    image_processing.histogram_equalizer()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/edge_detection", methods=["POST"])
@nocache
def edge_detection():
    image_processing.edge_detection()
    return render_template("filter.html", file_path="img/img_now.jpg")


@app.route("/blur", methods=["POST"])
@nocache
def blur():
    image_processing.blur()
    return render_template("image_filtering.html", file_path="img/img_now.jpg")


@app.route("/sharpening", methods=["POST"])
@nocache
def sharpening():
    image_processing.sharpening()
    return render_template("filter.html", file_path="img/img_now.jpg")


@app.route("/histogram_rgb", methods=["POST"])
@nocache
def histogram_rgb():
    # Fungsi yang akan dijalankan dalam thread terpisah
    def process_histogram():
        image_processing.histogram_rgb()

    # Buat thread baru untuk menjalankan operasi histogram
    histogram_thread = threading.Thread(target=process_histogram)
    histogram_thread.start()  # Mulai thread

    if image_processing.is_grey_scale("static/img/img_now.jpg"):
        return render_template("histogram.html", file_paths=["img/grey_histogram.jpg"])
    else:
        return render_template("histogram.html", file_paths=["img/red_histogram.jpg", "img/green_histogram.jpg", "img/blue_histogram.jpg"])



@app.route("/thresholding", methods=["POST"])
@nocache
def thresholding():
    lower_thres = int(request.form['lower_thres'])
    upper_thres = int(request.form['upper_thres'])
    image_processing.threshold(lower_thres, upper_thres)
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/crop_normal", methods=["POST"])
@nocache
def crop_normal():
    n_value = request.form.get('n_value')
    n_value = int(n_value)

    image_processing.crop_normal(n_value)
    # Define the directory where the image tiles are stored
    tile_directory = 'static/img/tiles/'

    # List all tile files in the directory
    tile_files = os.listdir(tile_directory)

    # Sort the tile files by their names (assuming naming convention tile_1.jpg, tile_2.jpg, etc.)
    tile_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    return render_template('quiz.html', tile_files=tile_files, n = n_value)

@app.route("/rgb_table", methods=["POST"])
@nocache
def rgb_table():
    target = os.path.join(APP_ROOT, "static/img")
    image_dimensions = image_processing.get_image_dimensions("static/img/img_now.jpg")
    rgb_values = image_processing.get_image_rgb("static/img/img_now.jpg")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("quiz_table.html", file_path="img/img_now.jpg", img_dim=image_dimensions, img_rgb_val=rgb_values)

@app.route("/crop_random", methods=["POST"])
@nocache
def crop_random():
    n_value = request.form.get('n_value')
    n_value = int(n_value)

    image_processing.crop_normal(n_value)
    # Define the directory where the image tiles are stored
    tile_directory = 'static/img/tiles/'

    # List all tile files in the directory
    tile_files = os.listdir(tile_directory)

    # Shuffle the tile_files list randomly
    random.shuffle(tile_files)

    return render_template('quiz.html', tile_files=tile_files, n=n_value)

@app.route("/identitykernel", methods=["POST"])
@nocache
def identity_kernel():
    image_processing.identity_kernel()
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/bilateral_filter", methods=["POST"])
@nocache
def bilateral_filter():
    image_processing.bilateral_filter()
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/normal_filter", methods=["POST"])
@nocache
def normal_filter(): 
    copyfile("static/img/img_normal.jpg", "static/img/img_now.jpg")
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/zero_padding", methods=["POST"])
@nocache
def zero_padding():
    image_processing.zero_padding()
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/low_pass_filter", methods=["POST"])
@nocache
def low_pass_filter():
    ksize = int(request.form["low-pass-filter"])
    image_processing.low_pass_filter(ksize)
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/high_pass_filter", methods=["POST"])
@nocache
def high_pass_filter():
    ksize = int(request.form["high-pass-filter"])
    image_processing.high_pass_filter(ksize)
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/band_pass_filter", methods=["POST"])
@nocache
def band_pass_filter():
    ksize_low = int(request.form["low-pass-filter"])
    ksize_high = int(request.form["high-pass-filter"])
    image_processing.band_pass_filter(ksize_low, ksize_high)
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/blur_filter", methods=["POST"])
@nocache
def blur_filter():
    ksize = int(request.form["blur-filter"])
    image_processing.blur_filter(ksize)
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/mean_filter", methods=["POST"])
@nocache
def mean_filter():
    ksize = int(request.form["mean-filter"])
    image_processing.mean_filter(ksize)
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/median_blur", methods=["POST"])
@nocache
def median_blur():
    ksize = int(request.form["median-blur"])
    image_processing.median_blur(ksize)
    return render_template("filter.html", file_path="img/img_now.jpg")

@app.route("/gaussian_blur", methods=["POST"])
@nocache
def gaussian_blur():
    ksize = int(request.form["gaussian-blur"])
    image_processing.gaussian_blur(ksize)
    return render_template("filter.html", file_path="img/img_now.jpg")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
