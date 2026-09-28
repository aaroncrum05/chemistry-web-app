from flask import Flask
app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Engineering Toolkit</title>
        </head>
        <body>
            <h1>Engineering Toolkit</h1>
            <p>My first Python web application is running.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)