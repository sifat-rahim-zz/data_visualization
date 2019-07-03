When a system is consist of some microservices, it is important to check if all alive and best if we can visualize it, live (in few minutes).

Summary : 

we have some microservices up and running. Our system need to have the following features  -

   1. Each micro-service need to have a health_check API with two endpoints.
         a) /ping 
            If this micorservice itself is OK
            this will return status code 200
      
         b) /healthCheck
          that will return status code 200

    

This scripts automates the this task
