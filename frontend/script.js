const newsInput = document.getElementById("newsInput");
const checkButton = document.getElementById("checkButton");
const result = document.getElementById("result");

// Your deployed Python Flask backend on Render
const API_URL = "YOUR_RENDER_BACKEND_URL";

checkButton.addEventListener("click", async () => {

    const news = newsInput.value.trim();

    // Check if user entered anything
    if (!news) {
        result.textContent = "Please enter some news.";
        return;
    }

    result.textContent = "Checking...";

    try {

        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                news: news
            })
        });

        const data = await response.json();

        if (!response.ok) {
            result.textContent = data.error || "Prediction failed.";
            return;
        }

        result.textContent = data.prediction;

    } catch (error) {

        console.error(error);

        result.textContent = "Unable to connect to the backend.";
    }
});