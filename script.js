var brightness = document.getElementById("sliderBrightness");
var outputBrightness = document.getElementById("spanBrightness");
outputBrightness.innerHTML = brightness.value;
brightness.oninput = function() {
  outputBrightness.innerHTML = this.value;
}

var contrast = document.getElementById("sliderContrast");
var outputContrast = document.getElementById("spanContrast");
outputContrast.innerHTML = contrast.value;
contrast.oninput = function() {
  outputContrast.innerHTML = this.value;
}

var denoise = document.getElementById("sliderDenoise");
var outputDenoise = document.getElementById("spanDenoise");
outputDenoise.innerHTML = "None";
denoise.oninput = function() {
  outputDenoise.innerHTML = this.value + "%";
}

var star = document.getElementById("sliderStar");
var outputStar = document.getElementById("spanStar");
outputStar.innerHTML = "None";
star.oninput = function() {
  outputStar.innerHTML = this.value + "%";
}

var denoiseToggled = false
buttonDenoise = document.getElementById("buttonDenoise")

function toggleDenoise() {
  if (denoiseToggled != true) {
    outputDenoise.innerHTML = "1%"
    denoiseToggled = true
    buttonDenoise.style.backgroundColor = "#4CAF50"
    buttonDenoise.innerHTML = "Disable Denoising"
  } else {
    outputDenoise.innerHTML = "None"
    denoiseToggled = false
    buttonDenoise.style.backgroundColor = "#bbb"
    buttonDenoise.innerHTML = "Enable Denoising"
  }
}

var starToggled = false
buttonStar = document.getElementById("buttonStar")

function toggleStar() {
  if (starToggled != true) {
    outputStar.innerHTML = "1%"
    starToggled = true
    buttonStar.style.backgroundColor = "#4CAF50"
    buttonStar.innerHTML = "Disable Enhancement"
  } else {
    outputStar.innerHTML = "None"
    starToggled = false
    buttonStar.style.backgroundColor = "#bbb"
    buttonStar.innerHTML = "Enable Enhancement"
  }
}