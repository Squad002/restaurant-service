# GoOutSafe - Restaurant microservice

### Local
    # Install Dependencies
    pip install -r requirements/dev.txt

    # Deploy
    flask deploy

    # Run 
    export FLASK_APP="app.py"
    export FLASK_ENV=development
    flask run

### Docker Image
    docker build -t gooutsafe-restaurant-service:latest . 
    docker run -p 5000:5000 gooutsafe-restaurant-service 

## Tests with coverage
Inside restaurant-service run (it will automatically use the configuration in pyproject.toml):

    pytest