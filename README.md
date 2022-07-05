# pbf2graph

[![travis](https://img.shields.io/travis/thomleysens/pbf2graph.svg)](https://travis-ci.org/thomleysens/pbf2graph)
[![codecov](https://codecov.io/gh/thomleysens/pbf2graph/branch/master/graph/badge.svg)](https://codecov.io/gh/thomleysens/pbf2graph)

> ***Transform PBF OSM file to routable directed Graph-Tool graph***

> ***Repo created and maintained by Thomas LEYSENS (AME department, Gustave Eiffel University)***

## 1. Get the repo
You can clone or download it.

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
* This method **allows** to update your local repo when the GitHub repo changes

### 1.2 Download the repo
* Go to the [front page of the repo](https://github.com/thomleysens/pbf2graph).
* Click on the ```Code``` button then on ```Download ZIP```
* Download and unzip it in your chosen directory
* This method **doesn't allow** to update your local repo when the GitHub repo changes. You will have to download it again.

## 2. Install the environment
* Install [Anaconda](https://docs.anaconda.com/anaconda/install/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
* Install the project environment by using the [```env.yml```](env.yml) file in this directory (*for more details, see [Anaconda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)*):
  * Go to the directory where the ```env.yml``` file leaves
  * Open a command prompt:
    ```cmd
    conda update conda
    conda env create -f env.yml
    ```
  * Conda will install the required Python libraries
  ```cmd
  conda activate pbf2graph
  ```

## 2. Usage

### 2.1 Download data

* You may visit [Geofabrik](https://download.geofabrik.de/) to download Protocolbuffer Binary Format (PBF) OpenStreetMap (OSM) file

### 2.2 Information on osmium memory parameters

* See:
	- [osmium documentation](https://osmcode.org/osmium-concepts/#indexes)
	- [pyosmium documentation](https://docs.osmcode.org/pyosmium/latest/intro.html#handling-geometries)

### 2.3 Command line to use ```pbf2gt.py```

* Transform .pbf file to graph-tool .gt file (*in directory root*):
	```cmd
	conda activate pbf2graph
	python pbf2graph/pbf2gt.py [Path to .pbf file] [Path to output .gt file]
	```
* Example:
	```cmd
	python pbf2graph/pbf2gt.py data/nord-pas-de-calais-latest.osm.pbf data/npdc.gt
	```
	
## 3. Imported & used libraries with version & license

> *See [Libraries with license file](libraries_with_license.md)*