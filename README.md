# geneva-webtool



[GENEVA: GENe Expression Variance Analysis](https://buttelab.ucsf.edu/)

GENEVA is a semi-automated framework for exploring massive amounts of RNA-seq datasets. 

To use the user interface of the tool visit https://buttelab.ucsf.edu/

```
Steps to installing web app locally:
1. Install Python 3
2. Install Django, Django Rest Swagger and Django Rest Framework python modules
    - pip3 install django==1.11.5
    - More detailed instructions here: https://docs.djangoproject.com/en/1.11/topics/install/
    - pip3 install django-rest-swagger==2.1.2
    - pip3 install djangorestframework==3.7.1

3. Install Requests python module
    - pip3 install requests
4. Else install all packages from requirement.txt file
	- pip3 install -r requirements.txt    
5. Clone this GitHub repository to a local directory (git clone https://github.com/lgragert/hla-who-to-unos.git)
6. Change directory to /conversion_tool/
7. Run command to start web server  
    - python3 manage.py runserver 8080  
8. Go to http://127.0.0.1:8080/ with your web browser. 

```


[Butte LAB](https://buttelab.ucsf.edu/)