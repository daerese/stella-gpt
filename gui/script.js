

eel.expose(playAudio)
eel.expose(log_on_js)

const startBtn = document.getElementById('start-btn')

startBtn.addEventListener('click', () => {

   eel.start()

})


document.getElementById('call-py').addEventListener('click', () => {

   eel.call_from_py()
})

function log_on_js() {

   console.log("Called from python")
}

function onlyPlayAudio() {
   let audio = new Audio("audio/message.wav")
   
   console.log(audio)

   audio.play()


   eel.py_print("From JavaScript: playing audio... ====")

}


// * Play audio

function playAudio()  {

   // eel.py_print("From JavaScript: playing audio...")

   console.log("Before playing audio...")



    // * The canplaythrough event is fired when the user agent can play the media

    // * This is a workaround in order to play the audio automatically 
    // * without user interaction
   //  audio.addEventListener("canplaythrough", () => {
   //      audio.play().catch(e => {
   //         window.addEventListener('click', () => {
   //            audio.play()
   //         }, { once: true })
   //      })
   //   }, { once: true });

   let audio = new Audio("audio/message.wav")

   audio.play()

   console.log("After Attempting to play audio")

   // eel.py_print()

}