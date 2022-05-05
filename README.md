
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