
const startBtn = document.getElementById('startBtn');
const outputDiv = document.getElementById('output');
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'en-US'; // Set the language


const BASE_URL = "http://localhost:5000"

const flaskBtn = document.getElementById('testFlask');

const toggleButton = document.getElementById('toggleButton');
const micIcon = document.getElementById('micIcon');
const messageText = document.getElementById('messageText');
// const helperText = document.getElementById('helperText');

// ***************
// * Utility functions
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

//* Check if the user's microphone is available
async function checkMicrophone() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        return true;
    } catch (error) {
        return false;
    }
}

function startListener(text="", holdText=false) {
    /**
     * Toggles the appropriate elements that let the user
     * know that their microphone is being recorded
     * 
     * @param {str} text - Set the helper text. If not set, 
     * then it is reset to the starting text.
     * 
     * @param {bool} holdText - If set to true, the text
     * will stay as it is on the screen.
     */


    micIcon.classList.remove('fa-microphone-lines-slash');

    micIcon.classList.add("mic-active")

    micIcon.classList.add('fa-microphone-lines');

    
    // * If the button was disabled, re-enable it
    if (toggleButton.disabled) {
        toggleButton.disabled = false;
    }


    if (!holdText) {
        
        if (!text) {
            text = "Listening"
        }
        messageText.innerHTML = text
    }



}

function stopListener(text="", holdText=false, temporary=false) {
    /**
     * Toggles the appropriate elements will let the user 
     * know that they're microphone is no longer being recorded.
     * 
     * @param {str} text - Set the helper text. If not set, 
     * then it is reset to the starting text.
     * 
     * @param {bool} temporary - If set to true, the toggle button
     * for the microhphone will be disabled. Use this whenever the 
     * program is waiting for a resposne from ChatGPT.
     */

    micIcon.classList.remove('fa-microphone-lines');
    micIcon.classList.remove('mic-active');
    micIcon.classList.add('fa-microphone-lines-slash');

    if (temporary) {
        toggleButton.disabled = true
    }

    if (!holdText) {
        if (!text) {
            text = "Toggle the microphone and start speaking..."
        }
    
        messageText.innerHTML = text
    }
}

function setText(text) {
    messageText.innerHTML = text
}

// ***************


// * Speech recognition functions
recognition.onstart = () => {
    console.log("recording...")
};

recognition.onresult = async (event) => {
    console.log("called")
    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;

        if (event.results[i].isFinal) {
            finalTranscript += transcript;
        } else {
            interimTranscript += transcript;
        }
    }

    // outputDiv.innerHTML = `
    //     <p><strong>Interim Transcript:</strong> ${interimTranscript}</p>
    //     <p><strong>Final Transcript:</strong> ${finalTranscript}</p>
    // `;
    
    messageText.innerHTML = `<strong>You:</strong> ${interimTranscript}`
   
   if (finalTranscript.trim() !== "") {
       await handleInput(finalTranscript.trim())
       
    //    console.log(finalTranscript);
    }

};

recognition.onend = () => {
    // startBtn.textContent = 'Start Recording';
    console.log("Not recording")


    if (toggleButton.checked) {
        stopListener("", true);
    }

    // document.getElementById('toggleButton').checked = false
};

// startBtn.addEventListener('click', () => {
//     if (recognition && !recognition.recognizing) {
//         recognition.start();
//     } else {
//         recognition.stop();
//     }
// });


toggleButton.addEventListener('change', function () {
    if (this.checked) {

        if (checkMicrophone()) {

            startListener()
    
            if (recognition && !recognition.recognizing) {
                recognition.start();
            }
        } else {
            alert('Microphone not available or permission denied.');
            return;
        }

    } else {

        stopListener()

        if (recognition && !recognition.recognizing) {
            recognition.stop()
        }
    }
});


// * Main function that handles the user input
async function handleInput(text) {
    /**
     * Handles the user input by sending it to python
     * to generate a ChatGPT response.
     * 
     * @param {str} text - The user input
     */



    recognition.stop()
    stopListener("Waiting for response...", false, true);

    let gptResponse = await eel.generate_gpt_response(text)()

    gptResponse = JSON.parse(gptResponse)

    let gptMessage = gptResponse["gptMessage"]


    // * Get the audio and start playing it.
    // * Then set the corresponding text.
    startAudio()

    let htmlMessage = `<strong>Stella:</strong> ${gptMessage}`

    console.log(gptResponse)


    setText(htmlMessage)
    // recognition.start()
    // startListener(htmlMessage)

}

// * Function to request the audio from Flask and play it.
// async function startAudio() {
//     /**
//      * Retrieves the most recent generated audio from 
//      * the flask server and plays the audio.
//      */

//     const response = await fetch('http://localhost:5000/audio')

//     const audioData = await response.blob()

//     const audio = new Audio(URL.createObjectURL(audioData));


//     audio.addEventListener("ended", () => {
//         recognition.start()
//     })

//     console.log(audio)
    
//     audio.play()

// }


// const playBtn = document.getElementById('playBtn')

// playBtn.addEventListener('click', async () => {
        // const response = await fetch('http://localhost:5000/audio')

        // const audioData = await response.blob()

        // const audio = new Audio(URL.createObjectURL(audioData));

        // console.log(audio)
        
        // audio.play()

// })

// * Test the flask server
// const testFlaskBtn = document.getElementById('testFlaskBtn')

// testFlaskBtn.addEventListener('click', async () => {
//     const response = await fetch('http://localhost:5000/members')


//     const data = await response.json()

//     console.log(data)
// })

// *****************************************
// * Canvas configuration
const canvas = document.getElementById('animationCanvas');
const ctx = canvas.getContext('2d');

// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;

// * Setting the intial size and color of the circle animation
const initialRadius = 50;
// const listeningColor = "hsl(340, 100%, 70%)";
// const initialColor = "hsl(195, 47%, 76%)";

// const listeningColor = "rgb(255, 190, 242)";
// const initialColor = "rgb(134, 225, 255)";

const listeningColor = "rgb(134, 225, 255)";
const initialColor = "rgb(134, 225, 255)";


let listening = false;
let audioPlaying = false;

initializeCircle(initialColor, initialRadius);

function initializeCircle(initialColor, initialRadius) {
    // Draw the initial glowing ball
    ctx.beginPath();
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const gradient = ctx.createRadialGradient(centerX, centerY, initialRadius / 2, centerX, centerY, initialRadius);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0.8)')
    gradient.addColorStop(1, initialColor);
    ctx.fillStyle = gradient;
    ctx.arc(centerX, centerY, initialRadius, 0, Math.PI * 2);
    ctx.fill();

    pulsateAnimation()
}


// let pulsateAnimationFrameId = 0;

// * Pulsating animation
function pulsateAnimation() {
    /**
     * * This animation occurs whenever the audio is not playing.
     */

    if (!audioPlaying) {
        // Calculate the pulsation radius based on a sine wave
        const baseRadius = 50; // Initial radius
        const pulsationAmplitude = 2.5; // Amplitude of the pulsation
        const pulsationFrequency = 1.25; // Frequency of the pulsation (in Hz)

        const pulsationPhase = Date.now() * 0.001 * pulsationFrequency; // Phase based on time
        const pulsatingRadius = baseRadius + pulsationAmplitude * Math.sin(pulsationPhase);

        
        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw the pulsating ball
        ctx.beginPath();
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const gradient = ctx.createRadialGradient(centerX, centerY, pulsatingRadius / 2, centerX, centerY, pulsatingRadius);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.8)');
        gradient.addColorStop(1, initialColor); // Use the same initial color
        ctx.fillStyle = gradient;
        ctx.arc(centerX, centerY, pulsatingRadius, 0, Math.PI * 2);
        ctx.fill();

        // Call the function recursively for the pulsating effect

        requestAnimationFrame(() => pulsateAnimation());
    }
    else {

        // console.log("Most recent radius ->", prevRadius)
        console.log("No longer pulsating...")
    }
}


// * Intializing the audio analyzation variables
let audioContext = null;
let analyser = null;
let dataArray = null;

let audio = null

async function startAudio()  {
    if (audio) {
        audio.pause();
        audio.currentTime = 0;
    }


    // * Retrieve the audio from this route.
    const response = await fetch('http://localhost:5000/audio')

    const audioBlob = await response.blob()

    const newAudio = new Audio(URL.createObjectURL(audioBlob));

    // * Configuring the audio context and audio analyzer
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);


    // console.log("Audio element: ", newAudio)

    const source = audioContext.createMediaElementSource(newAudio);
    source.connect(analyser);
    analyser.connect(audioContext.destination);

    // * Copy the byte frequency data to our intialized Uint8Array (dataArray)
    // analyser.getByteFrequencyData(dataArray)

    audio = newAudio
    await audio.play();

    // Set audioPlaying flag to true
    audioPlaying = true;
    
    audio.addEventListener('ended', async () => {
        // Set audioPlaying flag to false when audio playback ends
        audioPlaying = false;
        startListener("", true)
        recognition.start()
    });

    // Stop the pulsateAnimation by canceling the animation frame request
    // cancelAnimationFrame(pulsateAnimationFrameId);

    // requestAnimationFrame(() => pulsateAnimation(true));
    
    animate(analyser, dataArray);


};

// ************************
// * Animation

function animate(analyser, dataArray, prevRadius = null) {

    if (audioPlaying) {
        analyser.getByteFrequencyData(dataArray);
    
        // Calculate the average frequency
        const averageFrequency = dataArray.reduce((sum, value) => sum + value, 0) / dataArray.length;
    
        // Calculate the ball radius based on the average frequency (with a larger range)
        const minRadius = 50;
        const maxRadius = 125;
        const radius = minRadius + (maxRadius - minRadius) * (averageFrequency / 255);
    
        // Calculate the color based on the average frequency (light pink and light purple)
        // const pinkHue = 340; // Light pink hue
        // const purpleHue = 140; // Light purple hue
        // const hue = pinkHue + (purpleHue - pinkHue) * (averageFrequency / 255);
        // const color = `hsl(${hue}, 100%, 70%)`;

        // // Inside the animate function
        // const minRed = 255; // Lowest red value
        // const maxRed = 255; // Highest red value
        // const minGreen = 182; // Lowest green value
        // const maxGreen = 0; // Highest green value
        // const minBlue = 193; // Lowest blue value
        // const maxBlue = 0; // Highest blue value

        // // Calculate the RGB values based on audio frequency
        // const red = Math.round(minRed + (maxRed - minRed) * (averageFrequency / 255));
        // const green = Math.round(minGreen + (maxGreen - minGreen) * (averageFrequency / 255));
        // const blue = Math.round(minBlue + (maxBlue - minBlue) * (averageFrequency / 255));


        // Create the RGB color string
        // const color = `rgb(${red}, ${green}, ${blue})`;

        // Inside the animate function
        const pinkRGB = [134, 225, 255]; // RGB values for pink hue
        const purpleRGB = [255, 190, 242]; // RGB values for purple hue

        // Calculate the RGB values based on audio frequency using pink and purple hues
        const red = Math.round(pinkRGB[0] + (purpleRGB[0] - pinkRGB[0]) * (averageFrequency / 255));
        const green = Math.round(pinkRGB[1] + (purpleRGB[1] - pinkRGB[1]) * (averageFrequency / 255));
        const blue = Math.round(pinkRGB[2] + (purpleRGB[2] - pinkRGB[2]) * (averageFrequency / 255));

        // Create the RGB color string
        const color = `rgb(${red}, ${green}, ${blue})`;
    
        // Clear the canvas with a transparent background
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    
        // Draw the glowing ball
        ctx.beginPath();
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const gradient = ctx.createRadialGradient(centerX, centerY, radius / 2, centerX, centerY, radius);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.8)');
        gradient.addColorStop(1, color);
        ctx.fillStyle = gradient;
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.fill();
    
        // Call the animate function recursively
        const prevRadius = radius
        requestAnimationFrame(() => animate(analyser, dataArray, prevRadius));

        // console.log(prevRadius)

    }

    else {

        pulsateAnimation()

    }
}