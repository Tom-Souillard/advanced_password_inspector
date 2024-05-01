from flask import Flask

# Create an instance of the Flask application
app = Flask(__name__)

# Define a route for the URL '/'
@app.route('/')
def hello():
    return "Hello! Docker is working fine!"

# If this file is executed directly, run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
