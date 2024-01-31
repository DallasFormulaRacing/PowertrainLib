# PowertrainLib

This library will consist of various methods to visualize and analyze data to support our powertrain team's needs. Once the data is on the pi, the start-up script will run identify the network, validate the network, then connect to the network. Once a connection as been made the data from the latest testing session will be uploaded to both Box using the Box client for long term storage, and also MongoDB using the mongo client to be used in visualization. Plotly will then be used to visualize this data to the user.

## Tech Stack

Python version 3.11 or greater
MongoDB
Pandas

## Client Libraries

### Box

Box Upload File- https://developer.box.com/reference/post-files-content/
Box JWT Token for auth- https://developer.box.com/reference/resources/access-token/

### MongoDB Client Info

Pymongo Docs- https://pymongo.readthedocs.io/en/stable/

### Graphing Client

Plotly- https://plotly.com/python/

### Wifi Client

Wifi- https://wifi.readthedocs.io/en/latest/

### Discord Client

Discord.py- https://discordpy.readthedocs.io/en/stable/intro.html
