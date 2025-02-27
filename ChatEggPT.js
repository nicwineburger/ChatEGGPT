document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
var picturesSent = []
var responseArray = []
responseArray.push("Sure thing, I'd be glad to help you with that. How does this look?")
responseArray.push("Sounds tough, but I'll give it my best shot. Here you go!")
responseArray.push("No problem, coming right up. 🚀")
responseArray.push("Alright, if that's what you really want. I don't judge, I'm just a bot.")
responseArray.push("I have just the thing. One moment please.")

function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;
    
    const messagesDiv = document.getElementById("messages");
    
    // Add user message
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.textContent = message;
    messagesDiv.appendChild(userMessage);
    
    // Fake EGGGPT thinking delay
    const EGGGPTThinking = document.createElement("div");
    EGGGPTThinking.className = "message bot";
    EGGGPTThinking.textContent = "Thinking...";
    messagesDiv.appendChild(EGGGPTThinking);
    
    setTimeout(() => {
        EGGGPTThinking.remove(); // Remove "Thinking..."

        // Fake bot response with progressive typing
        const EGGGPTMessage = document.createElement("div");
        EGGGPTMessage.className = "message bot";
        messagesDiv.appendChild(EGGGPTMessage);
        
        let responseText = createResponse(userMessage.textContent)
        let i = 0;
        function typeText() {
            if (i < responseText.length) {
                EGGGPTMessage.textContent += responseText.charAt(i);
                i++;
                setTimeout(typeText, 50); // Adjust typing speed here
                messagesDiv.scrollTop = messagesDiv.scrollHeight;

            } else {
                const loadImage = document.createElement("img");
                loadImage.src = "assets/loading.gif"; // Change this to your actual image path
                loadImage.alt = "loading";
                loadImage.style.maxWidth = "10%"; // Ensures the image fits inside the chat
                messagesDiv.appendChild(loadImage);
                setTimeout(() => {
                    // Append image after text response is fully typed
                    loadImage.remove(); //remove loading image
                    const EGGGPTImage = document.createElement("img");
                    EGGGPTImage.src = selectPicture(userMessage.textContent); 
                    EGGGPTImage.alt = "Egg";
                    EGGGPTImage.style.maxWidth = "50%"; // Ensures the image fits inside the chat
                    messagesDiv.appendChild(EGGGPTImage);
                    EGGGPTImage.onload = () => {
                        messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    };
                }, 1000);
            }
        }
        typeText();
    
    }, 1000); // 1 second delay
    
    // Clear input
    input.value = "";
}

//read the message and say something silly
function createResponse(userMessage){

    let responseText = ""
    responseSelect = Math.floor(Math.random() *5)
    if (userMessage.includes("hot")){
        responseText = "Oh. Yeah, absolutely. I have exactly what you're looking for. Sicko."
    }
    else if (userMessage.includes("anime")){
        responseText = "Uwaiiiii you found me senpai 😳"
    }
    else if (userMessage.includes("food")){
        responseText = "Oh. Well, this is kind of all I have. Someone left it here a few weeks ago. Looks bad."
    }
    else{
        responseText = responseArray[responseSelect]
    }
    return responseText
}

//this will return a path to the asset we want
function selectPicture(userMessage) {
    let assetPath = "assets/"
    if(userMessage.includes("anime")){
        assetPath = assetPath + "egg_chan.jpg"
    }
    else if (userMessage.includes("hot")){
        assetPath = assetPath + "soft_boiled.jpg"
    }
    else if (userMessage.includes("food")){
        assetPath = assetPath + "cheggsteak.png"
    }
    else{
        assetPath = assetPath + randomPicture() + ".jpg"
    }
    return assetPath
}

function randomPicture(){
    let pictureSelect = Math.floor(Math.random() * 8) + 1
    if(picturesSent.includes(pictureSelect)){
        if(picturesSent.length > 8 ){ //if we've sent all the random pictures we have, reset the random picture array
            picturesSent = []
            return randomPicture()
        }
        else {
            return randomPicture()
        }
    }
    else{
        picturesSent.push(pictureSelect)
        return pictureSelect
    }

}