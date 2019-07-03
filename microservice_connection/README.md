When a system is consist of some microservices, it is important to check if all alive and best if we can visualize it, live (in few minutes). The brief idea is - each micro-service would have two api(s) - ping and healthCheck. 

ping api of a micro-service says - I am OK.
healthcheck api of a micro-service shows the status of all dependent micro-service(s), example given below. 
The dependency is part of the healthCheck api development. (Later you will obvserve that in this structure PING api is actually part of healthCheck api). 

Both API response in json format. On regular interval we call healthCheck API and store the response in a postgres database. From database we parse the response and render d3 data and graph files. 
Please note that - API development is not part of this project. We just did the later part (store response in DB and render d3 graphs from there). Automation done in python scripts.

For quick view please open the index.html file with your browser. The index.html file should be viewed as the image microservice_connection_check.png

Summary :
Let us assume, we have some microservices up and running. Our system need to have the following features :


   1. Each micro-service need to have a health_check API with two endpoints.

         a) /ping
            If this micorservice itself is OK
            this will return status code 200
            json response : 
            {"error":false,"message":"OK"}

         b) /healthCheck
          that will return status code 5xx    
          example : http://myapp.mydomain.com/api/healthCheck 
          json response :  
               { 
                 "error": true, 
                 "message": "ERROR", 
                 "status": 
                  { 
                   "CORE_API": "YES", 
                   "BILLING": "NO", 
                   "NAVIGATOR": "YES", 
                   "CARROTCAKE": "YES" 
                  } 
               }  

   It means the 'myapp' microservice depends on the CORE_API microservice. So it called http://CORE_API.mydomain.com/api/ping and found OK. same for other dependent microservices . Finally prepared the json response. Here we see - the 'myapp' microservice received error from "BILLING". So, it made the overall response "ERROR. Here if any dependency fails we call it ERROR status. If all OK we will give http status_code 200 

    2. A python script 'check_th_service_health', will run regularly like every 3 min, may be managed by CRON (We ran it as Nagios monitoring plugin in 3 min interval).
    Example : python check_th_service_health WEBSITE  

    This script will find the 'WEBSITE' in 'application_list.yaml' file and call related healthCheck API of this microservices and save the response in database (please check config.txt file for db credential). Thus you are regularly collecting api response in database table named 'daily_nagios_check'.
    Sample database table dump 'daily_nagios_check.sql.tar.gz' provided here for convenience. You can load the uncompressed file in a Postgres database.

    3. Now, we need to get data from the postgres table and create/refresh necessary node and links in the adapted D3 graph. This is done by 'generate_node_link.py'. It ran every 3 minutes, managed by CRON and reflects the latest update in graph. It actually updates the nodes and links file and their colours based on the reachability (green for OK, red for broken).

    4. Please open the index.html file with any browser and visualize the dependency live. If any dependency is OK the colour is green, else read.

Note : please install the necessary python libraries.  I could not find time to make a pip requirement file. 

