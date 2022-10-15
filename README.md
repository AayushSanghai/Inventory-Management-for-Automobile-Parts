# Inventory Management for Automobile Shop with multiple warehouses
 Programmed a one stop solution to increase efficiency of the shop in both turnaround time of repairs and profit margin using Python Flask and MongoDB.


## Abstract

A large repair shop with several distinct buildings storing extra parts has a problem keeping track of inventory. The shop has become quite successful and employs several master mechanics as well as apprentices. They have become popular because of their efficiency in repairing vehicles, both cars and scooters/motorcycles. They service all makes and models, and they can occasionally reduce costs by reusing parts from “parts machines” which they keep on the lot. Recently, the manager has noticed that they are often ordering common parts which they already have in stock, or they also must wait on repairs when it is found that parts are not on site. The manager found that often mechanics simply did not know where the parts were stored, and therefore assumed that none were available. This has caused both excess expenditure and delays in repairs. 
	The purpose of this project is to provide the repair shop with a means to track what parts they have in inventory, including subparts of a larger assembly, when and by whom parts are used and when parts should be reordered. This database will also track the location of parts in storage. The goal is to increase the efficiency of the shop both in turnaround time of repairs and profit margin.
 
 
 ## Introduction
 
 A webapp will be used by staff and mechanics to interface with the database. We plan to use Python Flask for the front-end and MongoDB for the backing data store. The interface will handle displaying data and allowing the user to take actions on inventory, as well as visualizations of usage rates, availability, and profits on parts sales. This interface will also allow parts checks, and scheduling for repairs when all parts are available.
	Parts are placed in bins, and bins are linked to physical locations. Bins only hold one “type” of part at a time. Bins need not be an actual “bin”, only a container or simply a shelf location. Bins may have minimum limits set that will automatically create a notification to reorder parts, visible to users of the webapp.
 
The database will store part information, such as sizes, material types, categories (bolts, shims, nuts, and so on), manufacturer, and part numbers. Since the shop keeps used cars and motorcycles for their usable spare parts, the database will need to track both the vehicle and the parts left on the vehicle that could be reused. These would be designated “assemblies” or parts. The names of mechanics would be stored to track who is using what parts, and the names and contacts of suppliers must be stored to allow easy ordering of replacement parts. A history of inventory actions will be kept in a separate collection. For this project, you will need to enter the data manually.



## System Architecture


![image](https://user-images.githubusercontent.com/61236166/195969833-9e6f122c-5bf7-4f28-b665-6b5728ad3ab4.png)



## Technologies Used

### 1- Python and it's framework Flask
### 2- MongoDB
### 3- HTML
### 4- CSS
### 4-JavaScript



## Database Description

- The core mechanism is ”bin” which holds one kind of parts with the count determined by capacity which are in turn physically located for ease of tracking. 
- Each location can have any no. of positions and can contain any no. of bins. These have an ergonomic arrangement for making parts easy to find.
- Each bin has an identifier and a location code that includes the storage location(storage location have a name, address and location code) code plus a position code. They also track their capacity .
- Bins have an item id, a position & location code, a quantity, a maximum quantity. a bin may also be a logical (rather than physical) .
- Several actions can be performed on the items viz: Purchase, Receive, Dispense, Modify, Remove



## Layout

![image](https://user-images.githubusercontent.com/61236166/195968367-7f129011-9d6d-45ec-9731-5108ad8d78bc.png)


## Screenshot of Interfaces

#### MongoDB Interface and Different Collection
<img src="https://user-images.githubusercontent.com/61236166/195968553-27504e2a-0a43-4f6b-8604-b16e1b26ca60.png" width="425"/> <img src="https://user-images.githubusercontent.com/61236166/195968584-22b67c75-212a-4a27-a852-234a926da46c.png" width="575"/>


#### Dashboard and Items Tab

<img src="https://user-images.githubusercontent.com/61236166/195968699-65eafeb6-7f06-4fbd-b4d0-58f7fa6caa4c.png" width="500"/> <img src="https://user-images.githubusercontent.com/61236166/195968715-fc112229-1271-412d-a9ba-20dece914503.png" width="500"/>


#### Order List and Bin Location


<img src="https://user-images.githubusercontent.com/61236166/195968779-9cac217c-23a2-400c-afe6-c094f3701fbd.png" width="500"/> <img src="https://user-images.githubusercontent.com/61236166/195968783-c6efd2c0-90cf-4cdc-8cd5-eb4728bcd458.png" width="500"/>


#### Reports Tab and Some Useful Vizualizations


<img src="https://user-images.githubusercontent.com/61236166/195968872-7c2a9c5a-a6c7-40f8-adf6-e3ce04cb8d3d.png" width="400"/> <img src="https://user-images.githubusercontent.com/61236166/195968874-6b6fcbbf-465c-4b44-a181-2f156d8b16f1.png" width="600"/>




## How To Run The Project

#### 1- First please download all the file present in this repository
#### 2- Now you will need to download MongoDB Compass
#### 3- Once you have downloaded all the files from the repository, and downloaded MongoDB, you will need to connect your MongoDB Compass(the database) to your backend. You can do this by going to the app.py file and using the pass from connection string.
#### 4- Now you can follow the steps below to run the project.
#### 5- You may need to recreate virtual environment if you are using a Linux machine. If so, just type pip install flask in your command line.
#### 6- Now, in your command line, navigate to the venv folder of the project and once your home folder is venv, type chmod +x Scripts/Activate
#### 7- And voi.la, the program must start running on your local server.




## Hope you liked the project. Do contact me if you face any trouble running the project or if you have any questions.














