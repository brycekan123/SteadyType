chrome.storage.local.get("isAutocorrectEnabled", (data) => {
  if (data.isAutocorrectEnabled) {
    document.addEventListener("input", async (event) => {
      if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {
        const originalText = event.target.value;
        
        try {
          // Make an API call to the server for real-time correction
          const response = await fetch("http://localhost:5000/autocorrect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: originalText })
          });
          const data = await response.json();
          
          // Replace the text with the AI-corrected text
          const correctedText = data.corrected_text;
          event.target.value = correctedText;
        } catch (error) {
          console.error("Error fetching corrected text:", error);
        }
      }
    });
  }
});
