from flask import Flask, render_template_string, request, jsonify
import requests, os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)

client = OpenAI(api_key=os.getenv("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"))
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🌸 Anime Finder AI 3.0</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    * {margin:0;padding:0;box-sizing:border-box;font-family:'Poppins',sans-serif;}
    body {
      background: var(--bg, linear-gradient(135deg,#1a1a2e,#16213e));
      color: var(--text,#fff);
      transition: 0.3s;
      min-height: 100vh;
      text-align: center;
      padding: 40px;
    }
    h1 {font-size:2.6rem;margin-bottom:20px;
      background:linear-gradient(90deg,#ff9ff3,#a18cd1);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
    form {margin-bottom:40px;}
    input {padding:12px 18px;border-radius:25px;border:none;width:300px;}
    button {background:linear-gradient(90deg,#a18cd1,#fbc2eb);border:none;
      border-radius:25px;padding:12px 18px;font-weight:600;color:white;cursor:pointer;}
    .card {
      background:rgba(255,255,255,0.08);
      backdrop-filter:blur(15px);
      border-radius:20px;
      padding:30px;
      width:90%;
      max-width:750px;
      margin:auto;
      box-shadow:0 0 25px rgba(0,0,0,0.4);
      animation:fadeIn 0.6s ease;
    }
    img.cover {width:240px;border-radius:15px;margin-bottom:15px;}
    .characters {display:flex;flex-wrap:wrap;justify-content:center;margin-top:15px;}
    .char {margin:10px;text-align:center;}
    .char img {width:100px;border-radius:10px;}
    .ai-response, iframe {margin-top:20px;}
    #chatbox {
      position:fixed;bottom:20px;right:20px;
      background:rgba(255,255,255,0.1);
      backdrop-filter:blur(10px);
      border-radius:20px;
      width:300px;
      padding:15px;
      display:flex;
      flex-direction:column;
      gap:10px;
      box-shadow:0 0 15px rgba(255,159,243,0.5);
    }
    #chatbox textarea {width:100%;height:80px;border-radius:10px;border:none;padding:10px;}
    #chatbox button {background:#a18cd1;border:none;padding:10px;border-radius:10px;color:white;cursor:pointer;}
    .theme-toggle {
      position:fixed;top:15px;right:20px;
      background:#ff9ff3;border:none;padding:10px 14px;
      border-radius:20px;cursor:pointer;color:#000;font-weight:600;
    }
    @keyframes fadeIn {from{opacity:0;transform:translateY(15px);}to{opacity:1;transform:none;}}
  </style>
</head>
<body>
  <button class="theme-toggle" onclick="toggleTheme()">🌗 Theme</button>
  <h1>🌸 Anime Finder AI 3.0 🌸</h1>
  <form method="POST">
    <input name="anime" placeholder="Search anime..." required>
    <button>Search</button>
  </form>

  {% if anime %}
  <div class="card">
    <img src="{{ anime['image'] }}" class="cover">
    <h2>{{ anime['title'] }}</h2>
    <p><b>Score:</b> {{ anime['score'] }}</p>
    <p>{{ anime['description']|safe }}</p>

    {% if characters %}
    <div class="characters">
      {% for c in characters %}
      <div class="char">
        <img src="{{ c['image'] }}" alt="{{ c['name'] }}">
        <p>{{ c['name'] }}</p>
      </div>
      {% endfor %}
    </div>
    {% endif %}

    {% if trailer %}
      <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ trailer }}" frameborder="0" allowfullscreen></iframe>
    {% endif %}

    {% if ai_info %}
    <div class="ai-response">
      <h3>💬 AI Insight</h3>
      <p>{{ ai_info }}</p>
    </div>
    {% endif %}
  </div>
  {% endif %}

  <div id="chatbox">
    <textarea id="msg" placeholder="Ask the Anime AI..."></textarea>
    <button onclick="sendChat()">Send</button>
    <div id="chat-response"></div>
  </div>

  <script>
    async function sendChat() {
      const msg = document.getElementById('msg').value;
      if(!msg.trim()) return;
      document.getElementById('chat-response').innerHTML = "💭 Thinking...";
      const res = await fetch('/chat', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({message:msg})
      });
      const data = await res.json();
      document.getElementById('chat-response').innerHTML = data.reply;
    }

    function toggleTheme(){
      if(document.body.style.getPropertyValue('--bg')){
        document.body.style.removeProperty('--bg');
        document.body.style.removeProperty('--text');
      } else {
        document.body.style.setProperty('--bg','#f5f5f5');
        document.body.style.setProperty('--text','#222');
      }
    }
  </script>

  <footer style="margin-top:30px;color:#ccc;">Powered by AniList, OpenAI, and YouTube 💫</footer>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    anime = characters = trailer = ai_info = None
    if request.method == "POST":
        name = request.form["anime"]

        # AniList query for anime details + characters
        query = """
        query ($search: String) {
          Media(search: $search, type: ANIME) {
            title { romaji english }
            description
            averageScore
            coverImage { large }
            characters(sort: ROLE, perPage: 5) {
              edges {
                node {
                  name { full }
                  image { medium }
                }
              }
            }
          }
        }
        """
        res = requests.post("https://graphql.anilist.co", json={"query": query, "variables": {"search": name}})
        data = res.json()
        media = data.get("data", {}).get("Media")

        if media:
            anime = {
                "title": media["title"]["english"] or media["title"]["romaji"],
                "description": media["description"],
                "score": media["averageScore"],
                "image": media["coverImage"]["large"],
            }

            characters = [
                {"name": c["node"]["name"]["full"], "image": c["node"]["image"]["medium"]}
                for c in media["characters"]["edges"]
            ]

            # Search trailer
            yt_res = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={anime['title']} trailer&type=video&key={YOUTUBE_API_KEY}")
            yt_data = yt_res.json()
            if yt_data.get("items"):
                trailer = yt_data["items"][0]["id"]["videoId"]

            # AI-generated insight
            prompt = f"Explain what makes the anime '{anime['title']}' unique, what themes it explores, and who would enjoy it. Keep it under 120 words."
            ai_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful anime expert who writes friendly and descriptive summaries."},
                    {"role": "user", "content": prompt},
                ]
            )
            ai_info = ai_response.choices[0].message.content

    return render_template_string(HTML, anime=anime, characters=characters, trailer=trailer, ai_info=ai_info)


@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an anime chatbot. Talk casually and passionately about anime, give recommendations, and answer questions."},
            {"role": "user", "content": msg},
        ]
    )
    return jsonify({"reply": ai_response.choices[0].message.content})


if __name__ == "__main__":
    app.run(debug=True)
