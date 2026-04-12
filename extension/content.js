setTimeout(() => {
    console.log("Extension running...");

    // Try multiple selectors (BBC + others)
    let title =
        document.querySelector("h1") ||
        document.querySelector("[data-testid='headline']") ||
        document.querySelector("h2");

    if (title && title.innerText.trim() !== "") {
        console.log("Title found:", title.innerText);

        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title: title.innerText })
        })
        .then(res => res.json())
        .then(data => {
            // 🔥 Better popup (not alert)
            let box = document.createElement("div");
            box.innerHTML = "📰 " + title.innerText + "<br><br><b>" + data.result + "</b>";

            box.style.position = "fixed";
            box.style.top = "20px";
            box.style.right = "20px";
            box.style.background = "black";
            box.style.color = "white";
            box.style.padding = "15px";
            box.style.zIndex = "9999";
            box.style.borderRadius = "10px";
            box.style.maxWidth = "300px";

            document.body.appendChild(box);
        })
        .catch(err => {
            console.log("Fetch error:", err);
        });

    } else {
        console.log("No title found");
    }
}, 4000); // give page more time to load