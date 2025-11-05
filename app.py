from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = None
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎌 Anime Finder</title>
        <style>
            body {
                font-family: "Poppins", sans-serif;
                background: #0f0f0f;
                color: white;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            h1 {
                margin-top: 40px;
                font-size: 2.5em;
                background: -webkit-linear-gradient(#e2b0ff, #9f44d3);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            form {
                margin-top: 30px;
            }
            input[type="text"] {
                padding: 12px;
                width: 300px;
                border: none;
                border-radius: 10px;
                outline: none;
                font-size: 16px;
            }
            button {
                padding: 12px 25px;
                border: none;
                border-radius: 10px;
                background: linear-gradient(90deg, #7b3fe4, #9f44d3);
                color: white;
                font-size: 16px;
                cursor: pointer;
                transition: 0.3s;
            }
            button:hover {
                transform: scale(1.05);
                box-shadow: 0 0 10px #9f44d3;
            }
            .anime-grid {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                margin: 40px auto;
                max-width: 1200px;
            }
            .anime-card {
                background: #1a1a1a;
                border-radius: 15px;
                width: 250px;
                padding: 15px;
                text-align: left;
                transition: 0.3s;
            }
            .anime-card:hover {
                transform: scale(1.03);
                box-shadow: 0 0 10px rgba(155,0,255,0.3);
            }
            img {
                width: 100%;
                border-radius: 10px;
            }
            .anime-card h3 {
                margin: 10px 0 5px 0;
                font-size: 18px;
                color: #e0b0ff;
            }
            .anime-card p {
                font-size: 13px;
                color: #ccc;
                height: 70px;
                overflow: hidden;
            }
            .anime-card a {
                color: #b572ff;
                text-decoration: none;
                font-weight: bold;
            }
            .anime-card a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>🎌 Anime Finder</h1>
        <form method="POST">
            <input type="text" name="anime_name" placeholder="Search anime..." required />
            <button type="submit">Search</button>
        </form>
    """

    if request.method == "POST":
        anime_name = request.form.get("anime_name")
        try:
            response = requests.get(f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=12")
            data = response.json()

            if "data" in data and len(data["data"]) > 0:
                results = data["data"]
                html += "<div class='anime-grid'>"
                for anime in results:
                    title = anime.get("title", "Unknown")
                    image = anime["images"]["jpg"]["image_url"]
                    synopsis = anime.get("synopsis", "No synopsis available.")[:200] + "..."
                    url = anime["url"]
                    html += f"""
                    <div class="anime-card">
                        <img src="{image}" alt="{title}">
                        <h3>{title}</h3>
                        <p>{synopsis}</p>
                        <a href="{url}" target="_blank">More Info →</a>
                    </div>
                    """
                html += "</div>"
            else:
                html += "<p style='color:red;'>No results found for that anime.</p>"

        except Exception as e:
            html += f"<p style='color:red;'>Error: {str(e)}</p>"

    html += "</body></html>"
    return html


if __name__ == "__main__":
    app.run(debug=True)
