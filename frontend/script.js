const newsInput = document.getElementById("newsInput");
const checkButton = document.getElementById("checkButton");
const result = document.getElementById("result");


checkButton.addEventListener("click", async () => {

    const news = newsInput.value.trim();

    // Check if user entered anything
    if (!news) {
        result.textContent = "Please enter some news.";
        return;
    }

    result.textContent = "Checking...";

    try {

        const response = await fetch("http://localhost:5000/predict", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                news: news
            })
        });

        const data = await response.json();

        result.textContent = data.prediction;

    } catch (error) {

        console.error(error);

        result.textContent = "Unable to connect to the backend.";
    }
});