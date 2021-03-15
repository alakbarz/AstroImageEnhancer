from os import removexattr
from flask import Flask, request, redirect
from flask.helpers import url_for
from flask.templating import render_template
import cv2
import numpy as np
import shutil
import datetime
import os

app = Flask(__name__)


class Image():
    filename = None
    brightness = "0"
    contrast = "0"
    denoise = "0"
    enhance = "0"
    revert = "0"


@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/stack", methods=["GET", "POST"])
def stack():
    if request.method == "POST":
        imageList = request.files.getlist("image")
        now = datetime.datetime.now()
        timestamp = now.strftime("%d-%m-%Y-%H%M%S")
        os.system(f"mkdir static/uploads/stack{timestamp}")

        for image in imageList:
            image.save(f"static/uploads/stack{timestamp}/{image.filename}")

        imageDirectory = f"static/uploads/stack{timestamp}"

        files = os.listdir(imageDirectory)
        files = [os.path.join(imageDirectory, x) for x in files if x.endswith(('.jpg')) or x.endswith(('.jpeg'))]

        def stackImagesECC(files):
            M = np.eye(3, 3, dtype=np.float32)

            first_image = None
            stacked_image = None

            for file in files:
                image = cv2.imread(file, 1).astype(np.float32) / 255
                print(file)
                if first_image is None:
                    # convert to gray scale floating point image
                    first_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    stacked_image = image
                else:
                    # Estimate perspective transform
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 3000,  1e-5)
                    s, M = cv2.findTransformECC(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), first_image, M, cv2.MOTION_HOMOGRAPHY, criteria, None, 5)
                    w, h, _ = image.shape
                    # Align image to first image
                    image = cv2.warpPerspective(image, M, (h, w))
                    stacked_image += image

            stacked_image /= len(files)
            stacked_image = (stacked_image*255).astype(np.uint8)
            return stacked_image

        stackedImaged = stackImagesECC(files)
        cv2.imwrite(imageDirectory + "/stacked.jpg", stackedImaged)
        Image.filename = f"stack{timestamp}/stacked.jpg"

        return redirect(url_for("upload"))


@app.route("/edit", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        Image.brightness = "0"
        Image.contrast = "0"
        Image.denoise = "0"
        Image.enhance = "0"

        image = request.files["image"]
        Image.filename = image.filename
        image.save(f"static/uploads/{Image.filename}")
        shutil.copyfile(
            f"static/uploads/{Image.filename}", f"static/uploads/backup-{Image.filename}")
        return render_template("index.html", revert=Image.revert, image=Image.filename, brightness=Image.brightness, contrast=Image.contrast, denoise=Image.denoise, enhance=Image.enhance)
    else:
        Image.brightness = "0"
        Image.contrast = "0"
        Image.denoise = "0"
        Image.enhance = "0"
        return render_template("index.html", revert=Image.revert, image=Image.filename, brightness=Image.brightness, contrast=Image.contrast, denoise=Image.denoise, enhance=Image.enhance)


@app.route("/process", methods=["GET", "POST"])
def process():
    if request.method == "POST":

        img = cv2.imread(f"static/uploads/{Image.filename}")
        dateTime = datetime.datetime.now()

        if request.form["sliderBrightness"] != Image.brightness:
            Image.brightness = request.form["sliderBrightness"]
            img = cv2.add(img, np.array([float(Image.brightness)]))
            # img = cv2.convertScaleAbs(img, beta=int(Image.brightness))
            cv2.imwrite(f"static/uploads/{Image.filename}", img)

        # if tempContrast != Image.contrast:
        #     Image.contrast = request.form["sliderContrast"]
        #     contrast.increaseContrast()

        Image.contrast = request.form["sliderContrast"]

        if request.form["sliderDenoise"] == "0":
            pass
        elif request.form["sliderDenoise"] != Image.denoise:
            Image.denoise = request.form["sliderDenoise"]
            output = None               # Do not output image
            strength = 10               # Denoising filter strength
            strengthColour = strength   # "Same as h, but for color images only"
            templateWindowSize = 7      # "should be odd. (recommended 7)"
            searchWindowSize = 21       # "should be odd. (recommended 21)"
            img = cv2.fastNlMeansDenoisingColored(img,
                                                  output,
                                                  strength,
                                                  strengthColour,
                                                  templateWindowSize,
                                                  searchWindowSize)
            cv2.imwrite(f"static/uploads/{Image.filename}", img)

        if request.form["sliderStar"] != Image.enhance:
            Image.enhance = request.form["sliderStar"]
            kernelSize = int(Image.enhance)
            kernel = np.ones((kernelSize, kernelSize), np.uint8)
            img = cv2.dilate(img, kernel, iterations=1)
            cv2.imwrite(f"static/uploads/{Image.filename}", img)

        return render_template("index.html", dateTime=dateTime, image=Image.filename, brightness=Image.brightness, contrast=Image.contrast, denoise=Image.denoise, enhance=Image.enhance)

    if request.method == "GET":
        shutil.copyfile(
            f"static/uploads/backup-{Image.filename}", f"static/uploads/{Image.filename}")
        return "Success"


@app.route("/revert")
def revert():
    shutil.copyfile(
        f"static/uploads/backup-{Image.filename}", f"static/uploads/{Image.filename}")
    return redirect(url_for("upload"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
