from project import create_app

app = create_app()

if __name__ == '__main__':
    # Runs the application on the development server
    app.run(debug=True, host='0.0.0.0')
