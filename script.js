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
var denoiseValue = denoise.value
var outputDenoise = document.getElementById("spanDenoise");
outputDenoise.innerHTML = "None";
denoise.oninput = function() {
  denoiseValue = this.value;
  outputDenoise.innerHTML = denoiseValue + "%";
}

var star = document.getElementById("sliderStar");
var outputStar = document.getElementById("spanStar");
outputStar.innerHTML = "None";
star.oninput = function() {
  starValue = this.value;
  outputStar.innerHTML = this.value + "%";
}

var denoiseToggled = false;
var denoiseValue = 0;
buttonDenoise = document.getElementById("buttonDenoise");

function toggleDenoise() {
  if (denoiseToggled != true) {
    denoise.value = denoiseValue
    outputDenoise.innerHTML = denoiseValue + "%"
    denoise.disabled = false;
    denoiseToggled = true
    buttonDenoise.style.backgroundColor = "#4CAF50"
    buttonDenoise.innerHTML = "Disable Denoising"
  } else {
    denoise.value = 0
    outputDenoise.innerHTML = "None"
    denoise.disabled = true;
    denoiseToggled = false
    buttonDenoise.style.backgroundColor = "#bbb"
    buttonDenoise.innerHTML = "Enable Denoising"
  }
}

var starToggled = false;
var starValue = 0;
buttonStar = document.getElementById("buttonStar");

function toggleStar() {
  if (starToggled != true) {
    star.value = starValue
    outputStar.innerHTML = starValue + "%"
    star.disabled = false;
    starToggled = true
    buttonStar.style.backgroundColor = "#4CAF50"
    buttonStar.innerHTML = "Disable Enhancement"
  } else {
    star.value = 0
    outputStar.innerHTML = "None"
    star.disabled = true;
    starToggled = false
    buttonStar.style.backgroundColor = "#bbb"
    buttonStar.innerHTML = "Enable Enhancement"
  }
}