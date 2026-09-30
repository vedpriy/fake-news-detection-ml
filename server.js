const express = require("express");
const cors = require("cors");
const { execFile } = require("child_process");
const path = require("path");

const app = express();

app.use(cors());
app.use(express.json());


// Home route
app.get("/", (req, res) => {
    res.send("Fake News Detection Backend is running!");
});


// Prediction route
app.post("/predict", (req, res) => {

    const news = req.body.news;

    // Check if news was provided
    if (!news || !news.trim()) {
        return res.status(400).json({
            error: "News text is required"
        });
    }

    console.log("Received news:", news);

    const scriptPath = path.join(__dirname, "prediction.py");

    // Run Python prediction.py
    execFile(
        "python",
        [scriptPath, news],
        { maxBuffer: 1024 * 1024 },
        (error, stdout, stderr) => {

            if (error) {
                console.error("Python error:", stderr || error.message);

                return res.status(500).json({
                    error: "Prediction failed"
                });
            }

            console.log("Prediction:", stdout.trim());

            res.json({
                prediction: stdout.trim()
            });
        }
    );
});


// Start server
app.listen(5000, () => {
    console.log("Server running on http://localhost:5000");
});