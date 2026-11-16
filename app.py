
from flask import Flask
from database import init_db
from routes import main

# =========================================
# VELORA — MAIN APPLICATION
# =========================================

app = Flask(__name__)

# Secret key for sessions and security
app.secret_key = "velora_change_this_secret_key"

# Initialize database
init_db()

# Register main routes
app.register_blueprint(main)


# =========================================
# ERROR HANDLERS
# =========================================

@app.errorhandler(404)
def page_not_found(error):
    return """
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="/">Return to VELORA Home</a>
    """, 404


@app.errorhandler(500)
def server_error(error):
    return """
    <h1>500 - Server Error</h1>
    <p>Something went wrong. Please try again later.</p>
    <a href="/">Return to VELORA Home</a>
    """, 500


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
