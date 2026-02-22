import os
from flask import Flask, render_template_string
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_KEY = os.getenv("REDIS_KEY", "visits")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Redis Counter</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 3rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 600px;
            margin: 0 20px;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .subtitle {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.9;
            line-height: 1.6;
        }
        .cta-button {
            display: inline-block;
            padding: 1rem 2.5rem;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 20px rgba(238, 90, 36, 0.3);
            border: 2px solid transparent;
        }
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(238, 90, 36, 0.4);
            background: linear-gradient(45deg, #ee5a24, #ff6b6b);
        }
        .tech-stack {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
        .tech-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            margin: 0.25rem;
            font-size: 0.9rem;
            font-weight: 500;
        }
        .emoji {
            font-size: 1.2em;
            margin-right: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="emoji"></span>Flask Redis Counter</h1>
        <p class="subtitle">
            A modern web application built with Flask and Redis<br>
            Track visitor counts with real time persistence
        </p>
        <a href="/count" class="cta-button">
            <span class="emoji">📊</span>View Visit Counter
        </a>
        <div class="tech-stack">
            <span class="tech-badge">🐍 Python</span>
            <span class="tech-badge">🌶️ Flask</span>
            <span class="tech-badge">🔴 Redis</span>
            <span class="tech-badge">🐳 Docker</span>
        </div>
    </div>
</body>
</html>
"""

COUNT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visit Counter - Flask Redis App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 3rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 600px;
            margin: 0 20px;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 2rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .counter-display {
            font-size: 4rem;
            font-weight: 800;
            margin: 2rem 0;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        .counter-label {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }
        .button-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            display: inline-block;
            padding: 1rem 2rem;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            min-width: 150px;
        }
        .btn-primary {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            box-shadow: 0 10px 20px rgba(238, 90, 36, 0.3);
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(238, 90, 36, 0.4);
        }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        .stats {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stat-item {
            display: inline-block;
            margin: 0.5rem 1rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        .emoji {
            font-size: 1.2em;
            margin-right: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="emoji">📊</span>Visit Counter</h1>
        <div class="counter-label">Total Visits</div>
        <div class="counter-display">{{ visits }}</div>
        <div class="button-group">
            <a href="/count" class="btn btn-primary">
                <span class="emoji">🔄</span>Refresh
            </a>
            <a href="/" class="btn btn-secondary">
                <span class="emoji">🏠</span>Home
            </a>
        </div>
        <div class="stats">
            <span class="stat-item">🐍 Flask</span>
            <span class="stat-item">🔴 Redis</span>
            <span class="stat-item">🐳 Docker</span>
            <span class="stat-item">⚡ Real-time</span>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route("/count")
def count():
    visits = r.incr(REDIS_KEY)
    return render_template_string(COUNT_TEMPLATE, visits=visits)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)