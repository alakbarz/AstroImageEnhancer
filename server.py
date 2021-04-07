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
    contrast = "1"
    denoise = "0"
    enhance = "0"
    brightnessBackup = "0"
    contrastBackup = "0"
    denoiseBackup = "0"
    enhanceBackup = "0"
    revert = "0"
    undo = False


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
        files = [os.path.join(imageDirectory, x) for x in files if x.endswith(
            ('.jpg')) or x.endswith(('.jpeg'))]

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
                    criteria = (cv2.TERM_CRITERIA_EPS |
                                cv2.TERM_CRITERIA_COUNT, 3000,  1e-5)
                    s, M = cv2.findTransformECC(cv2.cvtColor(
                        image, cv2.COLOR_BGR2GRAY), first_image, M, cv2.MOTION_HOMOGRAPHY, criteria, None, 5)
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
        Image.contrast = "1"
        Image.denoise = "0"
        Image.enhance = "0"

        image = request.files["image"]
        Image.filename = image.filename
        image.save(f"static/uploads/{Image.filename}")
        shutil.copyfile(
            f"static/uploads/{Image.filename}", f"static/uploads/backup-{Image.filename}")
        return render_template("index.html", revert=Image.revert, image=Image.filename, brightness=Image.brightness, contrast=Image.contrast, denoise=Image.denoise, enhance=Image.enhance)
    else:
        now = datetime.datetime.now()
        timestamp = now.strftime("%d-%m-%Y-%H%M%S")
        return render_template("index.html", dateTime=timestamp, revert=Image.revert, image=Image.filename, brightness=Image.brightness, contrast=Image.contrast, denoise=Image.denoise, enhance=Image.enhance)


@app.route("/process", methods=["GET", "POST"])
def process():
    if request.method == "POST":

        Image.brightnessBackup = Image.brightness
        Image.contrastBackup = Image.contrast
        Image.denoiseBackup = Image.denoise
        Image.enhanceBackup = Image.enhance

        shutil.copyfile(
            f"static/uploads/{Image.filename}", f"static/uploads/undo-{Image.filename}")
        shutil.copyfile(
            f"static/uploads/backup-{Image.filename}", f"static/uploads/original-{Image.filename}")

        dateTime = datetime.datetime.now()

        # Brightness
        # if request.form["sliderBrightness"] != Image.brightness:
        Image.brightness = request.form["sliderBrightness"]
        img = cv2.imread(f"static/uploads/original-{Image.filename}")
        img = cv2.add(img, np.array([float(Image.brightness)]))
        # img = cv2.convertScaleAbs(img, beta=int(Image.brightness))
        cv2.imwrite(f"static/uploads/{Image.filename}", img)

        # Contrast
        # if request.form["sliderContrast"] != Image.contrast:
        Image.contrast = request.form["sliderContrast"]
        img = cv2.imread(f"static/uploads/{Image.filename}")
        img = cv2.multiply(img, np.array([float(Image.contrast)]))
        cv2.imwrite(f"static/uploads/{Image.filename}", img)

        # Denoising
        if request.form["sliderDenoise"] == "0":
            pass
        elif request.form["sliderDenoise"] != Image.denoise:
            Image.denoise = int(request.form["sliderDenoise"])
            output = None               # Do not output image
            strength = Image.denoise    # Denoising filter strength
            strengthColour = strength   # "Same as h, but for color images only"
            templateWindowSize = 7      # "should be odd. (recommended 7)"
            searchWindowSize = 21       # "should be odd. (recommended 21)"
            img = cv2.imread(f"static/uploads/{Image.filename}")
            img = cv2.fastNlMeansDenoisingColored(img,
                                                  output,
                                                  strength,
                                                  strengthColour,
                                                  templateWindowSize,
                                                  searchWindowSize)
            cv2.imwrite(f"static/uploads/{Image.filename}", img)

        # if request.form["sliderStar"] != Image.enhance:
        #     Image.enhance = request.form["sliderStar"]
        #     kernelSize = int(Image.enhance)
        #     kernel = np.ones((kernelSize, kernelSize), np.uint8)
        #     img = cv2.dilate(img, kernel, iterations=1)
        #     cv2.imwrite(f"static/uploads/{Image.filename}", img)

        # Star Enhancement
        if request.form["sliderStar"] == "0":
            pass
        elif request.form["sliderStar"] != Image.enhance:
            Image.enhance = request.form["sliderStar"]
            n = int(Image.enhance)/2

            imgThreshold = cv2.imread(f"static/uploads/{Image.filename}", 0)
            imgThreshold = cv2.GaussianBlur(imgThreshold, (1, 1), 0)
            threshold = cv2.adaptiveThreshold(
                imgThreshold, 50, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            threshold = cv2.multiply(threshold, np.array(n))
            threshold = cv2.cvtColor(threshold,cv2.COLOR_GRAY2RGB)

            img = cv2.imread(f"static/uploads/{Image.filename}")
            img = cv2.add(img, threshold)

            # Gaussian blur kernel
            # kernelGaussian = np.array([[ 1, 4, 6, 4, 1],
            #                            [ 4,16,24,16, 4],
            #                            [ 6,24,36,24, 6],
            #                            [ 4,16,24,16, 4],
            #                            [ 1, 4, 6, 4, 1]])
            # kernelGaussian = kernelGaussian * (1/256)
            # img = cv2.filter2D(img, -1, kernelGaussian)

            # Unsharp mask kernel
            kernelUnsharp = np.array([[ 1, 4, 6, 4, 1],
                                      [ 4,16,24,16, 4],
                                      [ 6,24, -476,24, 6],
                                      [ 4,16,24,16, 4],
                                      [ 1, 4, 6, 4, 1]])
            kernelUnsharp = kernelUnsharp * (-1/256)
            img = cv2.filter2D(img, -1, kernelUnsharp)

            # Sharpening kernel
            # kernelSharpen = np.array([[ 0,-1, 0],
            #                           [-1, 5,-1],
            #                           [ 0,-1, 0]])

            # img = cv2.filter2D(img, -1, kernelSharpen)

            cv2.imwrite(f"static/uploads/{Image.filename}", img)

        return render_template("index.html", dateTime=dateTime, image=Image.filename, brightness=Image.brightness, contrast=Image.contrast, denoise=Image.denoise, enhance=Image.enhance)

    if request.method == "GET":
        shutil.copyfile(
            f"static/uploads/backup-{Image.filename}", f"static/uploads/{Image.filename}")
        print("Reverted")
        Image.brightness = "0"
        Image.contrast = "1"
        Image.denoise = "0"
        Image.enhance = "0"
        return "Sucess"


@app.route("/undo")
def undo():
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%H%M%S")
    Image.brightness = Image.brightnessBackup
    Image.contrast = Image.contrastBackup
    Image.denoise = Image.denoiseBackup
    Image.enhance = Image.enhanceBackup
    shutil.copyfile(
        f"static/uploads/undo-{Image.filename}", f"static/uploads/{Image.filename}")
    print("Undid")
    return render_template("index.html", dateTime=timestamp, revert=Image.revert, image=Image.filename, brightness=Image.brightness, contrast=Image.contrast, denoise=Image.denoise, enhance=Image.enhance)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
