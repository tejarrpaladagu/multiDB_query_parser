

### Install required python packages

```
   $ pip3 install -r requirements.txt
```

### Config and start webservice

##### Configure MySQL settings

In ``config.py`` file, fill in your real MySQL connection settings

```
_DB_CONF = {
 'host':'<YOUR-MYSQL-HOST>',
 'port':3306,
 'user':'<YOUR-MYSQL-USERNAME>',
 'passwd':'<YOUR-MYSQL-PASSWORD>',
 'db':'<YOUR-MYSQL-DATABASE>'
}
```

##### Start Webservice

```
   $  flask run
```

### Test webservice 

Post man collection included for quick test run
```
 http://localhost:5000/
 
 http://localhost:5000/test - test sql query run  connects to aws db 
 
 http://localhost:5000/runsqlquery - Post method runs query sent on aws db
    json post format {"sql":"<query-to-run>"}

```
### Build and Run using docker 
1. install docker in your local pc and make sure it is running 
2. Build the docker container using commmand 
`docker build -t dbproject1:latest .`
3. Run the container locally 
`docker run -d -p 5000:5000 dbproject1`


![Home page](https://user-images.githubusercontent.com/18380025/184508000-1c85d4ab-cbb6-48d6-be1e-51eab2cd3d73.PNG)

![querying](https://user-images.githubusercontent.com/18380025/184508015-b4168837-1955-476d-aa61-3ff5bb2cf19e.PNG)

![data_f](https://user-images.githubusercontent.com/18380025/184508006-2e55b1c5-d343-4a2f-898c-c1dbd4f62979.PNG)






