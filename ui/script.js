let subtitles = [];
let imageFiles = {}; // Dictionary to store image Object URLs
let allFilesProcessed = false; // Flag to indicate all files are processed

let divPreload = document.getElementById('preload');
let divLoading = document.getElementById('loading');
let divApp = document.getElementById('app');

let loadingMessage = document.getElementById('loadingMessage');
let loadingGif = document.getElementById('loadingGif');

// Hide loading elements initially
divLoading.style.display = 'none';
//loadingGif.style.display = 'none';
divApp.style.display = 'none';

document.getElementById('zipUpload').addEventListener('change', function(event) {
    let file = event.target.files[0];
    let audioPlayer = document.getElementById('audioPlayer');

    // Show loading elements
    divLoading.style.display = 'block';
    document.getElementById('text-helper').textContent = 'Loading your project, this can take some seconds...';
//    loadingGif.style.display = 'block';

    let fileProcessingPromises = []; // Array to hold file processing promises

    JSZip.loadAsync(file) // Load zip file
        .then(function(zip) {
            // Process each file in the zip
            Object.keys(zip.files).forEach(function(filename) {
                let fileProcessing = zip.files[filename].async('blob').then(function(fileData) {
                    if (filename.endsWith('.mp3')) {
                        // Load audio file
                        audioPlayer.src = URL.createObjectURL(fileData);
                    } else if (filename.endsWith('.json')) {
                        // Load JSON file
                        let reader = new FileReader();
                        reader.onload = function() {
                            subtitles = JSON.parse(reader.result);
                        };
                        reader.readAsText(fileData);
                    } else if (filename.endsWith('.png')) {
                        // Load image file and create Object URL
                        imageFiles[filename] = URL.createObjectURL(fileData);
                    }
                });
                fileProcessingPromises.push(fileProcessing);
            });

            return Promise.all(fileProcessingPromises);
        })
        .then(function() {
            allFilesProcessed = true;
            audioPlayer.load();
            console.log("All files processed");

            console.log(imageFiles);

            // Hide loading elements after processing is complete
            divLoading.style.display = 'none';
            divPreload.style.display = 'none';
            divApp.style.display = 'block';
        })
        .catch(function(err) {
            console.error('Error processing the zip file:', err);

            // Hide loading elements if an error occurs
            divLoading.style.display = 'none';
            divPreload.style.display = 'none';
        });
});

document.getElementById('audioPlayer').addEventListener('timeupdate', function() {
    if (!allFilesProcessed) return; // Don't proceed if not all files are processed

    let currentTimeMillis = this.currentTime;
    let subtitleText = '';
    let gptText = '';
    let imageFile = '';

    subtitles.forEach(item => {
        if (currentTimeMillis >= item.secs) {
            subtitleText = item.data.text;
            if (item.data.gpt){
                gptText = item.data.gpt;
            }
            if (item.data.image_file){
                imageFile = item.data.image_file;
            }
        }
    });
    if (imageFile && imageFiles[imageFile]) {
        // Use the Object URL from the dictionary if it exists
        document.getElementById('imageDisplay').src = imageFiles[imageFile];
    }

    document.getElementById('time').textContent = currentTimeMillis;
    document.getElementById('subtitle').textContent = subtitleText;
    document.getElementById('imageSubtitle').textContent = gptText;
    document.getElementById('text-helper').textContent = '';
});