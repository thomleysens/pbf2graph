# pbf2graph

[![travis](https://img.shields.io/travis/thomleysens/pbf2graph.svg)](https://travis-ci.org/thomleysens/pbf2graph)
[![codecov](https://codecov.io/gh/thomleysens/pbf2graph/branch/master/graph/badge.svg)](https://codecov.io/gh/thomleysens/pbf2graph)


> ***Transform PBF OSM file to routable directed Graph-Tool graph***

> ***Repo created and maintained by Thomas LEYSENS - thomleysens - (AME department, Gustave Eiffel University)***

> :warning: ***This repo is under development. Could use a lot of memory for heavy PBF file (> 200 Mo) and cause memory error***


:warning: ***Because ```pbf2graph``` use some Python librairies only available on Linux and MacOS, there are two ways of using this repo:*** 
* ***[with container](#with-container) (for all users, Windows users have to use this method)*** 
* ***[without container](#without-container) (experimented Linux|MacOS users and Linux|MacOS developpers)***


## 1 Without container

> *For Linux|MacOS users & Linux|MacOS developpers*

### 1.1 Clone the repo
* Install Git for your OS
* Go to the [front page of the repo](https://github.com/thomleysens/pbf2graph).
* Click on the ```Code``` button and copy the HTTPS link
* Open a command prompt inside the directory you want to clone the repo:
  ```cmd
  git clone https://github.com/thomleysens/pbf2graph.git
  ```
* Depending of the git configuration, it may ask for your credentials
* Then it will clone the repo to your computer

### 1.2 Install the environment
* Install [Anaconda](https://docs.anaconda.com/anaconda/install/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
* Install the project environment by using the [```env.yml```](env.yml) file in this directory (*for more details, see [Anaconda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)*):
  * Go to the directory where the ```environment.yml``` file is
  * Open a command prompt:
    ```cmd
    conda update conda
    conda env create -f environment.yml
    ```
  * Conda will install the required Python libraries

### 1.3 Usage

#### 1.3.1 Download data

* You may visit [Geofabrik](https://download.geofabrik.de/) to download Protocolbuffer Binary Format (PBF) OpenStreetMap (OSM) file

#### 1.3.2 Information on osmium memory parameters

* See:
	- [osmium documentation](https://osmcode.org/osmium-concepts/#indexes)
	- [pyosmium documentation](https://docs.osmcode.org/pyosmium/latest/intro.html#handling-geometries)

#### 1.3.3 Command line to get graph file

* Transform .pbf file to graph-tool .gt file (*in directory root*):
	```cmd
	conda activate pbf2graph
	python pbf2gt.py [Path to .pbf file] [Path to output .gt file]
	```
* Example:
	```cmd
	python pbf2gt.py data/nord-pas-de-calais-latest.osm.pbf data/npdc.gt
	```
	
## 2 With container

> *For all users, Windows users have to use this method*

> *The container use the [```continuumio/miniconda3``` image](https://hub.docker.com/r/continuumio/miniconda3) as base*

### 2.1 Get the DockerFile
We provide a [DockerFile](DockerFile) to build and run a container (*Linux, Miniconda and the ```pbf2graph``` repo*):
* Click on [DockerFile](DockerFile)
* Then click on ```Raw``` button
* Copy/Paste the raw content to a new text file (*in a directory of your choice*) on your computer and name it ```DockerFile``` (***NO EXTENSION***)
* In the same directory create an empty directory named ```data```

### 2.2 Install Docker or Podman

> *Podman seems to have some limitations compared to Docker but appears to be simpler to install and use for beginners.*

* See [Docker installation](https://docs.docker.com/engine/install/)
* See [Podman installation](https://podman.io/getting-started/installation.html)

### 2.3 Build the container

> *Container must be built just once (unless ```pbf2graph``` repo has changed and you want to get the changes)*

#### 2.3.1 With Docker

* In the directory with the DockerFile, open a shell:
	```cmd
	docker build -t pbf2graph .
	```

#### 2.3.2 With Podman

* In the directory with the DockerFile, open a shell:
	```cmd
	podman --storage-opt ignore_chown_errors=true build -t pbf2graph .
	```

### 2.4 Run the container

> *The container will run with a possibility to read/write files between a local directory and a ```data``` directory in the running container*

#### 2.4.1 Download data

* You may visit [Geofabrik](https://download.geofabrik.de/) to download Protocolbuffer Binary Format (PBF) OpenStreetMap (OSM) file
* Then you can put the downloaded ```.pbf``` file to the ```data``` directory you created. 

#### 2.4.2 With Docker

* In the directory with the DockerFile, open a shell:
	```cmd
	docker run -v [absolute/path/to/data/directory]:/data -it pbf2graph
	```
* You might obtain something like this:
	```cmd
	(pbf2graph) root@9c45011mf78:/#
	```
* You can now use ```pbf2graph```, see [2.3.4 Command line to use ```pbf2gt.py```](#2.3.4-command-line-to-get-graph-file)

#### 2.4.3 With Podman

* In the directory with the DockerFile, open a shell:
	```cmd
	podman run -v [absolute/path/to/data/directory]:/data -it pbf2graph
	```
* You might obtain something like this:
	```cmd
	(pbf2graph) root@9c45011mf78:/#
	```
* You can now use ```pbf2graph```, see [2.3.4 Command line to use ```pbf2gt.py```](#2.3.4-command-line-to-get-graph-file)
	
#### 2.4.4 Command line to get graph file

* In the previous shell:
	```cmd
	python pbf2gt.py data/[PBF file] data/[GT file]
	```
* Example:
	```cmd
	python pbf2gt.py data/nord-pas-de-calais-latest.osm.pbf data/npdc.gt
	```	
* Once program executed, you will obtain a ```.gt``` file in your local data directory
* You can quit the container with ```exit``` command

#### 2.4.5 Information on osmium memory parameters

* See:
	- [osmium documentation](https://osmcode.org/osmium-concepts/#indexes)
	- [pyosmium documentation](https://docs.osmcode.org/pyosmium/latest/intro.html#handling-geometries)

## Information about imported & used libraries (*with version & license*)

> *See [Libraries with license file](libraries_with_license.md)*