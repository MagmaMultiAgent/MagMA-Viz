# MagmaViz

This is a project hoping to solve the problem of visualizing the training of multi-agent systems.

The current pipeline can be seen in the following diagram:

![302031428-853c530c-da6b-4b91-824f-86429a3db3b1](https://github.com/MagmaMultiAgent/MagmaViz/assets/14542948/add73f8f-34be-43b7-abb4-63189e7e4a23)

The idea is to send the current state of the environment, along with any statistic we want to visualize to a visualization server via UDP, putting as little extra load on the training as possible.

This repository contains the files for the visualization server, called MagmaViz.

Here's a screenshot of the page:
![magmaviz](https://github.com/MagmaMultiAgent/MagmaViz/assets/14542948/c64b8673-c05b-4969-b9be-84b5eb6f8837)

Sending data to this server can be done using a separate repository, which is included here as a submodule. If you would like more information about that part of the project and instructions, visit [this](https://github.com/MagmaMultiAgent/MagmaVizClient/tree/main) repository.

## How to use the server

You have two options:
1. Download one of the recent releases with the pre-built static files
2. Build it yourself
   1. install npm
   2. run the `build.sh` file

After you have your built static files, you can install the requirements from `requirements.txt` and run the app with the `run.sh` file.

Once the server is running you can start your train script and try to send data for visualization.

On the page you can add any number of visualizations, each of them can display exactly one statistic in a desired format. If you constructed a layout you like, you can save it to local storage.

The charts are not updated periodically by default, but you can set them to do so.

The sent data is automatically saved, but you can also manually save it. You can load saved data by choosing a file.
