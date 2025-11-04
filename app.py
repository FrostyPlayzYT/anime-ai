from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Anime Finder AI 🌸</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }

    body {
      background: linear-gradient(135deg, #1a1a2e, #16213e);
      color: #f5f5f5;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      min-height: 100vh;
      padding: 30px;
    }

    h1 {
      font-size: 2.5rem;
      background: linear-gradient(90deg, #ff6ec7, #a767ff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 0 15px rgba(255, 110, 199, 0.5);
      margin-bottom: 25px;
    }

    form {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 10px;
      margin-bottom: 30px;
    }

    input {
      padding: 12px 18px;
      width: 320px;
      border-radius: 25px;
      border: none;
      outline: none;
      font-size: 1rem;
      color: #333;
    }

    button {
      background: linear-gradient(90deg, #a767ff, #ff6ec7);
      color: white;
      border: none;
      border-radius: 25px;
      padding: 12px 20px;
      font-size: 1rem;
      cursor: pointer;
      transition: 0.3s ease;
      box-shadow: 0 0 15px rgba(255, 110, 199, 0.4);
    }

    button:hover {
      transform: scale(1.05);
      box-shadow: 0 0 25px rgba(255, 110, 199, 0.6);
    }

    .card {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 20px;
      padding: 30px;
      width: 90%;
      max-width: 700px;
      text-align: center;
      box-shadow: 0 0 30px rgba(0,0,0,0.4);
      animation: fadeIn 1s ease;
    }

    .card img {
      width: 250px;
      border-radius: 15px;
      margin-bottom: 20px;
      box-shadow: 0 0 15px rgba(167,103,255,0.5);
      transition: 0.4s;
    }

    .card img:hover {
      transform: scale(1.05);
      box-shadow: 0 0 30px rgba(255,110,199,0.8);
    }

    .card h2 {
      color: #ff9ff3;
      margin-bottom: 10px;
    }

    .card p {
      line-height: 1.6;
      color: #ddd;
      margin-bottom: 10px;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    footer {
      margin-top: 40px;
      color: #aaa;
      font-size: 0.9rem;
    }
  </style>
</head>
<body>
  <h1>🌸 Anime Finder AI 🌸</h1>
  <form method="POST">
    <input name="anime" placeholder="Search for an anime..." required>
    <button>Search</button>
  </form>

  {% if anime %}
  <div class="card">
    <img src="{{ anime['image'] }}" alt="{{ anime['title'] }}">
    <h2>{{ anime['title'] }}</h2>
    <p><b>Score:</b> {{ anime['score'] }}</p>
    <p>{{ anime['description']|safe }}</p>
  </div>
  {% endif %}

  <footer>Powered by AniList API 💫</footer>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    anime = None
    if request.method == "POST":
        name = request.form["anime"]

        query = """
        query ($search: String) {
          Media(search: $search, type: ANIME) {
            title { romaji english }
            description
            averageScore
            coverImage { large }
          }
        }
        """
        variables = {"search": name}

        res = requests.post("https://graphql.anilist.co", json={"query": query, "variables": variables})
        data = res.json()

        if data.get("data") and data["data"].get("Media"):
            a = data["data"]["Media"]
            anime = {
                "title": a["title"]["english"] or a["title"]["romaji"],
                "description": a["description"],
                "score": a["averageScore"],
                "image": a["coverImage"]["large"],
            }

    return render_template_string(HTML, anime=anime)

if __name__ == "__main__":
    app.run(debug=True)
