[![Build Status](https://travis-ci.org/Squad002/restaurant-service.svg?branch=main)](https://travis-ci.org/Squad002/restaurant-service) [![Coverage Status](https://coveralls.io/repos/github/Squad002/restaurant-service/badge.svg?branch=main)](https://coveralls.io/github/Squad002/restaurant-service?branch=main)

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

    # Start Elasticsearch
    docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.0

### Docker Image
    docker build -t restaurant-service:latest . 
    docker run -p 5000:5000 restaurant-service 

## Tests with coverage
Inside restaurant-service run (it will automatically use the configuration in pyproject.toml):

    pytest