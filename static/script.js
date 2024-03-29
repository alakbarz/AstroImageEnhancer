var form = document.getElementById("controlsForm");

var processing = document.getElementById("processing")

function process() {
  processing.style.visibility = "visible"
  processing.style.opacity = 1;
  form.submit()
}

var stackForm = document.getElementById("stackForm")

function upload() {
  processing.style.opacity = 1;
  stackForm.submit()
}

var revertValue = document.getElementById("revert");

function revert() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/process", true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var response = this.responseText;
      window.location.replace("/edit");
    }
  };
  xhttp.send();
}

function undo() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/undo", true)
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var response = this.responseText;
      window.location.replace("/edit");
    }
  };
  xhttp.send();
}

var brightness = document.getElementById("sliderBrightness");
var outputBrightness = document.getElementById("spanBrightness");
brightness.oninput = function () {
  outputBrightness.innerHTML = this.value + "%";
}

var contrast = document.getElementById("sliderContrast");
var outputContrast = document.getElementById("spanContrast");
contrast.oninput = function () {
  outputContrast.innerHTML = this.value;
}

var denoise = document.getElementById("sliderDenoise");
var denoiseValue = denoise.value
var outputDenoise = document.getElementById("spanDenoise");
denoise.oninput = function () {
  denoiseValue = this.value;
  outputDenoise.innerHTML = denoiseValue;
}

var star = document.getElementById("sliderStar");
var outputStar = document.getElementById("spanStar");
star.oninput = function () {
  starValue = this.value;
  outputStar.innerHTML = this.value;
}