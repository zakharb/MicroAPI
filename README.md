<p align="center">
  <a href="https://www.linkedin.com/in/zakharb/microapi">
  <img src="img/logo.png" alt="logo" />
</p>

<p align="center">

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=30&pause=1000&color=05998B&center=true&width=500&lines=++Microservice+architecture;+with+FastAPI+and+Docker" alt="description" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1-blue" height="20"/>
  <img src="https://img.shields.io/badge/python-3.11-blue" height="20"/>
</p>


<p align="center">
  <img src="img/usage.gif" alt="usage" />
</p>


## Getting Started

[MicroAPI](https://github.com/zakharb/microapi) is fully separates API in Async mode based on [Microservices](https://en.wikipedia.org/wiki/Microservices)   

For CRUD operations is used `Customer - Product - Price - Order` model  

> The `Customer` buys a `Product` with a different `Price` and receives an `Order`  
> The `Price` is calculated including taxes/discounts depending on the type of customer/  

Each part is work like Microservice  
The Microservice runs in separate Docker container   

Microservice has its own Database  
Database can be switch from Postgres to MongoDB or other  


### Requirements

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

### Installing

Clone the project

```
git clone git@github.com:zakharb/microapi.git
cd microapi
```

Start docker-compose

```
docker-compose up -d
```

<p align="center">
  <img src="img/install.gif" alt="animated" />
</p>

## Usage  

### Customers  
Get, put, update, delete `Customers` via API [Customers](http://localhost:8080/api/v1/customers/docs)    
<p align="center">
  <img src="img/customers.gif" alt="animated" />
</p>

### Products    
Get, put, update, delete `Products` via API [Products](http://localhost:8080/api/v1/products/docs)  
<p align="center">
  <img src="img/products.png" />
</p>

### Prices    
Get `Prices` via API [Prices](http://localhost:8080/api/v1/prices/docs)  
<p align="center">
  <img src="img/prices.png" />
</p>

### Orders    
Get `Orders` via API [Orders](http://localhost:8080/api/v1/orders/docs)  
<p align="center">
  <img src="img/orders.png" />
</p>


## Configuration  
</a>  

To solve problem with performance each Service run in container  
[Uvicorn]((https://www.uvicorn.org/)) work as ASGI server and connect to one piece with [Nginx](https://www.nginx.com/)  
Main configuration is `docker-compose.yml`  

- every service located in separate directory `name-service`  
- use `Dockerfile` to change docker installation settings  
- folder `app` contain FastAPI application  
- all services connected to one piece in `docker-compose.yml`  
- example of service + DB containers (change `--workers XX` to increase multiprocessing)  

### Examples  
`Customer` service
```
  customer_service:
    build: ./customer-service
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    #command: gunicorn main:app --workers 4 --worker-class --host 0.0.0.0 --port 8000
    volumes:
      - ./customer-service/:/app/
    ports:
      - 8001:8000
    environment:
      - DATABASE_URI=postgresql://customer_db_username:customer_db_password@customer_db/customer_db_dev
    depends_on:
       - customer_db
    logging:
        driver: none 
  
  customer_db:
    image: postgres:latest
    volumes:
      - postgres_data_customer:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=customer_db_username
      - POSTGRES_PASSWORD=customer_db_password
      - POSTGRES_DB=customer_db_dev
    logging:
        driver: none 
```


## Client  
There is client for work with Microservices  
`Microapiclient` is used for generating data and testing

It is located in folder `client`

### Install  
```
cd client
python3 -m venv venv
source venv/bin/activate 
python -m pip install -e .
```

### Run
```
cd client
source venv/bin/activate 
python -m microapiclient

  __   __   _                      _____   _____  _______ 
 (__)_(__) (_)        _           (_____) (_____)(_______)
(_) (_) (_) _    ___ (_)__  ___  (_)___(_)(_)__(_)  (_)   
(_) (_) (_)(_) _(___)(____)(___) (_______)(_____)   (_)   
(_)     (_)(_)(_)___ (_)  (_)_(_)(_)   (_)(_)     __(_)__ 
(_)     (_)(_) (____)(_)   (___) (_)   (_)(_)    (_______)

usage: __main__.py [-h]
                   {getcustomer,postcustomer,getproduct,postproduct,getprice,postorder,postorders,generateorder}
                   ...

positional arguments:
  {getcustomer,postcustomer,getproduct,postproduct,getprice,postorder,postorders,generateorder}
    getcustomer         Get customer from DB
    postcustomer        Post new customer into DB
    getproduct          Get product by name from DB
    postproduct         Post new product into DB
    getprice            Get price_net and price_gross
    postorder           Post order into DB
    postorders          Bulk write orders into DB
    generateorder       Generate order into CSV file

optional arguments:
  -h, --help            show this help message and exit

```

### Examples  

- Generate Customers  
```
python -m microapiclient postcustomer --customer-count 50
```  
- Generate Products   
```
python -m microapiclient postproduct --product-count 50
```  
- Generate Orders to file  
```
python -m microapiclient generateorder --order-count 1000 --task-count 32
```  
- Bulk write Orders from file to DB  
```
python -m microapiclient postorders --order-file orders.csv --task-count 32
```  
- View logs in `client.log`  
```
cat client.log | more
```

## Deployment

Edit `Dockerfile` for each Microservice and deploy container

## Versioning

Using [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/zakharb/microapi/tags). 

## Authors

* **Zakhar Bengart** - *Initial work* - [Ze](https://github.com/zakharb)

See also the list of [contributors](https://github.com/zakharb/microapi/contributors) who participated in this project.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation - see the [LICENSE](LICENSE) file for details
