from web.app import app

if __name__ == "__main__":
    print("Starting web translator application...")
    print("Navigate to http://localhost:5000/ in your web browser")
    app.run(debug=True)