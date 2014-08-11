# Smart traffic prediction with NuPIC

The program in this folder used the Cortical Learning Algorithm (CLA) in the Numenta Platform for Intelligent Computing (NuPIC) to predict traffic volume data. For more information about NuPIC, please visit the [NuPIC wiki](https://github.com/numenta/nupic/wiki)

## Requirements

-NuPIC
-pandas (for data cleaning)
-matplotlib (for exploratory data analysis)

## Program Phases

### 1. Download the traffic data

The traffic data used for this project can be downloaded and unzipped 
by running th script:

    ./downloadTrafficData.py 

The data file should be available as data/VOL_2011.csv

You may also download the data manually from the Department of Transportation
of the New York State [website](https://www.dot.ny.gov/divisions/engineering/technical-services/highway-data-services/hdsb)


### 2. Data Selection and Cleaning

The raw traffic data is a big csv file with the following columns:
RCStation, Start_Time, Direction, Lane, Count



