import React, { useState } from "react";

function App() {
  const [longUrl, setLongUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");

  const shortenUrl = async () => {
    const response = await fetch("http://98.81.233.70:8000/shorten", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: longUrl })
    });

    const data = await response.json();
    setShortUrl(data.short_url);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Simple URL Shortener</h2>

      <input
        type="text"
        placeholder="Enter long URL"
        value={longUrl}
        onChange={(e) => setLongUrl(e.target.value)}
        style={{ width: "400px", padding: "8px" }}
      />

      <br /><br />

      <button onClick={shortenUrl} style={{ padding: "10px 20px" }}>
        Shorten
      </button>

      <br /><br />

      {shortUrl && (
        <div>
          <h3>Short URL:</h3>
          <a href={shortUrl} target="_blank" rel="noreferrer">
            {shortUrl}
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
