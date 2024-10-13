const selectBtn = document.getElementById("select-btn");
// const cameraBtn = document.getElementById("camera-btn");
const generateBtn = document.getElementById("generate-btn");
const imageDisplay = document.getElementById("image-display");
const downloadBtn = document.getElementById('download-btn');


// Function to handle selection of an image
function handleImageSelect() {
  generateBtn.style.display = 'inline-block';
  downloadBtn.style.display = 'none';
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "image/*";
  fileInput.onchange = function(event) {
    const selectedFile = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
      imageDisplay.src = event.target.result;
    };
    reader.readAsDataURL(selectedFile);
  };
  fileInput.click();
}

// Function to handle click on generate button
async function handleGenerate() {
  console.dir('here');
  const dataURL = imageDisplay.src; // Get base64 image
  if (dataURL) {
      const formData = new FormData();
      formData.append("image", dataURL); // Send the base64 image as part of form data

      // Send to FastAPI
      const response = await fetch("/upload-canvas-image", {
          method: "POST",
          body: formData
      });
    
    // imageDisplay.style.display = 'none';
    const data = await response.json();
    imageDisplay.innerHTML = "";
    imageDisplay.src = data.image_url; // Set the image source to the result of FileReader
    imageDisplay.style.display = 'inline-block'; // Show the preview
    imageDisplay.style.alignContent = 'center';
    generateBtn.style.display = 'none';
    downloadBtn.style.display = 'inline-block';
    
    // Set up download action
    downloadBtn.addEventListener('click', () => {
        const a = document.createElement('a');
        a.href = data.image_url;
        a.download = 'funny_image.png';
        a.click();
    });
}


}

// Add event listeners to buttons
//selectBtn.addEventListener("change", handleImageSelect);
// cameraBtn.addEventListener("click", handleCamera);
//generateBtn.addEventListener("click", handleGenerate);


