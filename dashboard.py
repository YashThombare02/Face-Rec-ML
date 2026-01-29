from flask import Flask, render_template_string
import os

app = Flask(__name__)

DEPLOY_LOG = "C:/face_recognition/deploy.log"
VERSION_FILE = "C:/face_recognition/version.txt"

HTML = """
<h1>🚀 Face Recognition Deployment Dashboard</h1>

<h3>📦 Version</h3>
<pre>{{ version }}</pre>

<h3>📝 Deployment Log</h3>
<pre>{{ log }}</pre>

<h3>❤️ Health</h3>
<pre>{{ health }}</pre>
"""

@app.route("/")
def dashboard():
    version = "Unknown"
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE) as f:
            version = f.read()

    log = "No deployments yet"
    if os.path.exists(DEPLOY_LOG):
        with open(DEPLOY_LOG) as f:
            log = f.read()

    health = "OK" if os.path.exists("C:/face_recognition/app") else "FAILED"

    return render_template_string(
        HTML,
        version=version,
        log=log,
        health=health
    )

if __name__ == "__main__":
    app.run(port=5000)
