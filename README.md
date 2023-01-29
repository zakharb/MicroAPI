<p align="center">
  <a href="https://www.linkedin.com/in/zakharb/microapi">
  <img src="logo.png" alt="logo" />
</p>

<p align="center">

<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=30&pause=1000&color=05998B&center=true&width=500&lines=++Microservice+architecture;+with+FastAPI+and+Docker" alt="description" ></a>

</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1-blue" height="20"/>
  <img src="https://img.shields.io/badge/python-3.11-blue" height="20"/>
</p>


<p align="center">
  <img src="usage.gif" alt="usage" />
</p>


## Getting Started

[MicroAPI](https://github.com/zakharb/microapi) is fully separates API in Async mode  
Each Service has its own Database and runs in Docker containers   
Easily expandability With Micro Service architecture  
Database can be switch from Postgres to MongoDB or other 

### Prerequisites

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

Check services:  

- [Customers](http://localhost:8080/api/v1/customers/docs)  
- [Products](http://localhost:8080/api/v1/products/docs)  
- [Prices](http://localhost:8080/api/v1/prices/docs)  
- [Orders](http://localhost:8080/api/v1/orders/docs)  

<p align="center">
  <img src="install.gif" alt="animated" />
</p>

## Usage

All parameters send via arguments. 
- set server and port  
- set sending speed  
- set file with logs examples  

### Examples

Start with 2 msg/sec and standart port

```
python3 -m syslogen 192.168.1.1 -i examples_messages.txt -c 2
```

Start with 4 msg/sec and port 5514
```
python3 -m syslogen 192.168.1.1 -p 5514 -i examples_messages.txt -c 4
```

## Deployment

Edit Dockerfile and spicify server IP address

Build image
```
docker build --network host -t syslogen .
```

Run image
```
docker run syslogen
```
## Versioning

Using [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/zakharb/syslogen/tags). 

## Authors

* **Zakhar Bengart** - *Initial work* - [Ze](https://github.com/zakharb)

See also the list of [contributors](https://github.com/zakharb/contributors) who participated in this project.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation - see the [LICENSE](LICENSE) file for details



![logo](logo.png)

## MicroAPI  
### Micro services with FastAPI and Docker  


![](https://img.shields.io/badge/version-1.0-blue)
![](https://img.shields.io/badge/python-3.9-blue)

## Content  
[Important info](#important_info)  
[Install](#install)  
[Configuration](#configuration)  
[Client](#client)  
[Usage](#usage)  


<a name="important_info"/>

## Important info  
</a>  

> MicroAPI work as fully separates API in Async mode  
> Stack: FastAPI + Uvicorn + Nginx  
> Each Service has its own Database and run in docker containers   
> Easily expandability With Micro Service architecture  
> Database can be easily switch from Postgres to MongoDB or other  

<a name="install"/>  

## Install  
</a>  

- Install `docker` and `docker-compose`  
- Clone repo  
- Run `docker-compose up -d`   
- Check services:  
--  http://localhost:8080/api/v1/customers/docs  
--  http://localhost:8080/api/v1/products/docs  
--  http://localhost:8080/api/v1/prices/docs  
--  http://localhost:8080/api/v1/orders/docs  

<a name="configuration"/>  

## Configuration  
</a>  

> To solve problem with performance each Service run in container  
> Uvicorn work as ASGI server and connect to one piece with Nginx  
> Main configuration is `docker-compose.yml`  

- every service located in separate directory `name-service`  
- use `Dockerfile` to change docker installation settings  
- folder `app` contain FastAPI application  
- all services connected to one piece in `docker-compose.yml`  
- example of service + DB containers (change `--workers XX` to increase multiprocessing)  
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

<a name="client"/>  

## Client  
</a>  

- Folder `client` contains client to work with services  
```
└─$ python -m microapiclient
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

- Install  
```
cd client
python3 -m venv venv
source venv/bin/activate 
python -m pip install -e .
```
- Run  
```
cd client
source venv/bin/activate 
python -m microapiclient
```

<a name="usage"/>  

## Usage  
</a>  

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