const micButton = document.getElementById("micButton");
const resetButton = document.getElementById("resetButton");
const statusBox = document.getElementById("status");
const outputText = document.getElementById("outputText");
const orderSummary = document.getElementById("orderSummary");
const summaryText = document.getElementById("summaryText");

let recognition = null;
let orderCompleted = false;


// Fully stop recognition safely
function stopRecognition() {
    if (recognition) {
        try { recognition.onresult = null; } catch(e){}
        try { recognition.onend = null; } catch(e){}
        try { recognition.onerror = null; } catch(e){}
        try { recognition.stop(); } catch(e){}
        try { recognition.abort(); } catch(e){}
        recognition = null;
    }
}


// Create recognition instance
function createRecognition() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
        alert("Use Google Chrome desktop for voice input.");
        return null;
    }
    const rec = new SR();
    rec.lang = "en-US";
    rec.interimResults = false;
    rec.continuous = false;
    return rec;
}


// SPEAK BUTTON
micButton.onclick = () => {

    if (orderCompleted) {
        statusBox.textContent = "Order complete. Click New Order.";
        return;
    }

    recognition = createRecognition();
    if (!recognition) return;

    recognition.start();
    statusBox.textContent = "Listening...";

    recognition.onresult = async (event) => {

        if (orderCompleted) return;

        const spokenText = event.results[0][0].transcript;

        outputText.textContent =
            "Customer: " + spokenText + "\n\nBarista: ...";

        statusBox.textContent = "Processing...";

        const response = await fetch("http://localhost:8000/voice-agent", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ text: spokenText })
        });

        const data = await response.json();

        outputText.textContent =
            "Customer: " + spokenText + "\n\nBarista: " + data.reply;

        if (data.is_complete) {

            summaryText.textContent = data.summary;
            orderSummary.classList.remove("hidden");

            orderCompleted = true;
            micButton.disabled = true;

            stopRecognition();
            statusBox.textContent =
                "✅ Order complete! Summary will stay until New Order.";

            return;
        }

        statusBox.textContent = "Click Speak to continue.";
    };

    recognition.onend = () => {};
    recognition.onerror = () => {};
};


// NEW ORDER BUTTON
resetButton.onclick = () => {
    orderCompleted = false;
    outputText.textContent = "";
    summaryText.textContent = "";
    orderSummary.classList.add("hidden");
    micButton.disabled = false;

    fetch("http://localhost:8000/voice-agent", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text: "start over" })
    });

    statusBox.textContent = "New order started. Click Speak.";
};
