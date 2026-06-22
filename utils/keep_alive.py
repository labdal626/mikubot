"""
Keep-alive web server for Render free tier.
UptimeRobot will ping this URL to prevent the bot from sleeping.
"""
from flask import Flask, jsonify
from threading import Thread
import os
import datetime

app = Flask(__name__)
START_TIME = datetime.datetime.utcnow()

@app.route('/')
def home():
    uptime = datetime.datetime.utcnow() - START_TIME
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>MikuBot - Online ✨</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }}
            body {{
                background: linear-gradient(135deg, #39C5BB 0%, #FF69B4 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                overflow: hidden;
            }}
            .container {{
                text-align: center;
                background: rgba(0,0,0,0.3);
                padding: 50px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                animation: float 3s ease-in-out infinite;
            }}
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-20px); }}
            }}
            h1 {{
                font-size: 4em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
                animation: glow 2s ease-in-out infinite alternate;
            }}
            @keyframes glow {{
                from {{ text-shadow: 0 0 10px #fff, 0 0 20px #FF69B4; }}
                to {{ text-shadow: 0 0 20px #fff, 0 0 30px #39C5BB; }}
            }}
            .status {{
                font-size: 1.5em;
                margin: 20px 0;
                padding: 10px 20px;
                background: rgba(0,255,127,0.2);
                border-radius: 50px;
                display: inline-block;
                border: 2px solid #00FF7F;
            }}
            .info {{
                margin-top: 30px;
                font-size: 1.1em;
                line-height: 2;
            }}
            .pulse {{
                display: inline-block;
                width: 12px;
                height: 12px;
                background: #00FF7F;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 1.5s infinite;
            }}
            @keyframes pulse {{
                0% {{ box-shadow: 0 0 0 0 rgba(0,255,127,0.7); }}
                70% {{ box-shadow: 0 0 0 15px rgba(0,255,127,0); }}
                100% {{ box-shadow: 0 0 0 0 rgba(0,255,127,0); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✨ MikuBot ✨</h1>
            <div class="status"><span class="pulse"></span>ONLINE & STABLE</div>
            <div class="info">
                <p>🤖 Discord Server Manager Bot</p>
                <p>⏱️ Uptime: {hours}h {minutes}m {seconds}s</p>
                <p>🎵 Powered by Hatsune Miku Magic</p>
                <p>📡 Keep-alive Server Active</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/status')
def status():
    return jsonify({
        "status": "online",
        "bot": "MikuBot",
        "version": "1.0.0",
        "uptime_seconds": int((datetime.datetime.utcnow() - START_TIME).total_seconds())
    })

@app.route('/ping')
def ping():
    return "pong", 200

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    server = Thread(target=run)
    server.daemon = True
    server.start()
