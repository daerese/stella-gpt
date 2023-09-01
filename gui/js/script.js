
const outputDiv = document.getElementById('output');

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'en-US'; // Set the language


const BASE_URL = "http://localhost:5000"

const toggleButton = document.getElementById('toggleButton');
const micIcon = document.getElementById('micIcon');
const messageText = document.getElementById('messageText');

// * The speech recognition class will turn off after a few seconds of silence.
// * This variable will be used to determine when that happens.
// * The recognition needs to be constantly listening unless switched off. 
let endedFromSilence = false;

// * Awake helps determine the color of the audio main animation.
// * The color will signal to the user if Stella is awake and listening or not.
let awake = false;

// ***************
// * Utility functions
function setText(text) {
    messageText.innerHTML = text
}

function setEndedFromSilence(value) {

    endedFromSilence = value
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
            text = awake ? "Listening..." : `Say "Hey, Stella" to start`
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

            text = `Toggle the microphone and say "Hey, Stella" to start`
        }
    
        messageText.innerHTML = text
    }

    // * If the button isn't disabled 
    if (!toggleButton.disabled && toggleButton.checked) {
        toggleButton.checked = false
    } 
}


// ******************************
// * Speech recognition functions
recognition.onstart = () => {
    console.log("recording...")
};

recognition.onresult = async (event) => {
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

    messageText.innerHTML = `<strong>You:</strong> ${interimTranscript}`
   
   if (finalTranscript.trim() !== "") {


        console.log("FINAL TRANSCRIPT: ", finalTranscript)
        await handleInput(finalTranscript.trim())
       
    }

};

recognition.onend = () => {

    // * This event is also where we determine if the 

    if (toggleButton.checked) {

        if (toggleButton.disabled) {
            setEndedFromSilence(true);
            stopListener();
        }

        // * If the toggle button isn't disabled, and the button is checked
        // * Then the recognition turned off on its own. Turn the recognition back on.
        // * This ensures the recognition is constantly listening.
        else {
            console.log("Restarting listener...")
            recognition.start()
        }
    }

};

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
async function handleInput(text = "") {
    /**
     * Handles the user input by sending it to python
     * to generate a ChatGPT response.
     * 
     * @param {str} text - The user input
     */

    console.log("WHATS BEING SENT: ", text)

    if (!awake) {
        if (text.toLowerCase().includes("hey stella")) {
            awake = true
        }
        else {
            startListener("", false)
        }

    }

    if (awake) {

        // * If awake, send the input to chatGPT and wait for a response
        recognition.stop()
    
        stopListener("Waiting for response...", false, true);
    
        let gptResponse = await eel.generate_gpt_response(text)()
        gptResponse = JSON.parse(gptResponse)

        let gptStatus = gptResponse["status"]
        console.log(gptResponse)

        if (gptStatus === 200) {
            let gptMessage = gptResponse["gptMessage"]
    
            let gptSleep = gptResponse["go_to_sleep"]
            
            // * Code for if the user needs no more assistance.
            awake = gptSleep ? false : true
        
            // * Get the audio and start playing it.
            // * Then set the corresponding text.
            startAudio()
        
            let htmlMessage = `<strong>Stella:</strong> ${gptMessage}`
        
            setText(htmlMessage)
        }
        else {
            setText(gptResponse["statusMessage"])

            startListener("", true)
            recognition.start()
        }


    }

}

// *****************************************
// * Canvas configuration
const canvas = document.getElementById('animationCanvas');
const ctx = canvas.getContext('2d');

// * Setting the intial size and color of the circle animation
const initialRadius = 50;

const initialColor = "rgb(194, 189, 255)";
const listeningColor = "rgb(134, 225, 255)";

let listening = false;
let audioPlaying = false;

initializeCircle(initialColor, initialRadius);

function initializeCircle(initialColor, initialRadius) {
    /**
     * * This creates the circle that is the focus of the animation.
     * * It then starts the idle animation (pulsate)
     */
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
        gradient.addColorStop(1, awake ? listeningColor : initialColor); // Use the same initial color
        ctx.fillStyle = gradient;
        ctx.arc(centerX, centerY, pulsatingRadius, 0, Math.PI * 2);
        ctx.fill();

        // Call the function recursively for the pulsating effect

        requestAnimationFrame(() => pulsateAnimation());
    }
}
// *****************************************

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


    // * Retrieve the audio from this local route.
    const response = await fetch('http://localhost:5000/audio')

    const audioBlob = await response.blob()

    const newAudio = new Audio(URL.createObjectURL(audioBlob));

    // * Configuring the audio context and audio analyzer
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

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
    
    animate(analyser, dataArray);


};

// ************************
// * Main vocal animation
function animate(analyser, dataArray, prevRadius = null) {

    if (audioPlaying) {
        analyser.getByteFrequencyData(dataArray);
    
        // * Calculate the average frequency
        const averageFrequency = dataArray.reduce((sum, value) => sum + value, 0) / dataArray.length;
    
        // * Calculate the ball radius based on the average frequency (with a larger range)
        const minRadius = 50;
        const maxRadius = 125;
        const radius = minRadius + (maxRadius - minRadius) * (averageFrequency / 255);

        // * Inside the animate function
        const blueRGB = [134, 225, 255]; // RGB values for pink hue
        const purpleRGB = [255, 190, 242]; // RGB values for purple hue

        // * Calculate the RGB values based on audio frequency using pink and purple hues
        const red = Math.round(blueRGB[0] + (purpleRGB[0] - blueRGB[0]) * (averageFrequency / 255));
        const green = Math.round(blueRGB[1] + (purpleRGB[1] - blueRGB[1]) * (averageFrequency / 255));
        const blue = Math.round(blueRGB[2] + (purpleRGB[2] - blueRGB[2]) * (averageFrequency / 255));

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
    }

    else {

        pulsateAnimation()

    }
}