# Traffic prediction with NuPIC

The program in this folder used the Cortical Learning Algorithm (CLA) in the Numenta Platform for Intelligent Computing (NuPIC) to predict traffic volume data. For more information about NuPIC, please visit the [NuPIC wiki](https://github.com/numenta/nupic/wiki)

## Requirements

+ [NuPIC](https://github.com/numenta/nupic/wiki)
+ pandas (for data cleaning)
+ matplotlib (for plotting)

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

We only selected monitoring stations that has consecutive hourly count data for more than 60 days for further analysis. For those stations, we picked one direction and aggregate all traffic count from all lanes, and then select the longest continuous recording segment. The cleaned data file will be saved in "data/" with one file per monitoring stations.

You can reproduce the data selection and cleaning procedures by running the script

    ./dataPreProcess.py

### 3. Exploratory Analysis

Before running any algorithms, we did some exploratory analysis of the data. It is clear that  traffic data from different stations usually have distinct daily and weekly pattern:

![WeeklyPattern](https://github.com/ywcui1990/TrafficPrediction/blob/master/result/SmartTraffic_Presentation/Slide4.png)


Some monitoring stations also show a seasonal variation of traffic volume

![SeasonalVariation](https://github.com/ywcui1990/TrafficPrediction/blob/master/result/SmartTraffic_Presentation/Slide5.png)

You can reproduce the exploratory analysis by running

    ./exploratoryAnalysis.py

It might be more fun if you can explore the data yourself. There are new patterns there yet to be discovered!

### 4. Train CLA to predict traffic data

We used the swarm procedure in NuPIC to optimize model parameters. For more information of the swarming algorithm, please visit this [wiki](https://github.com/numenta/nupic/wiki/Swarming-Algorithm). 

To train CLA for a single recording station, you can use the swarm.py script

    ./swarm.py "./data/cleanTrafficData10003.csv" 

There is also a script, run_swarm.py that fit models for every recording station (in ./data/). To use the script, you can simply run

    ./run_swarm.py

The parameters for the best models are saved in './model_params'. The previous steps leave some artifacts on your file system. You can get rid of those files by running

    ./cleanup.py

### 5. Make predictions with CLA

Now you have the parameters for the best models for each monitoring station. The next step is to make predictions using the CLA. To generating predictions for a single station, run

    ./run.py "cleanTrafficData10003" [--plot]

If '--plot' is not specified, the prediction will be wrote to the ./prediction directory. If '--plot' is specified, the script will attept to plot on screen using matplotlib (assuming it is installed)

To generate predictions for all monitoring stations, run
    
    ./runAllModels.py 

Then all the predictions will be saved in the ./prediction directory

### 6. Quantify prediction accuracy

You can visualizing the quality of prediction by just plotting the predicted and measured volume count together (they should be located in ./prediction now). Here is an example prediction of CLA. It accurately captured the "rush hour" during weekdays and lack of "rush hour" on weekends.

![CLAPrediction](https://github.com/ywcui1990/TrafficPrediction/blob/master/result/CLAprediction.png)

There is also a script that quantify the quality of prediction and compare it with several other simple methods. The result is shown in ./result/ErrorRate.pdf, and can be reproduced by running

    ./analyPerformance.py

![Results](https://github.com/ywcui1990/TrafficPrediction/blob/master/result/ErrorRateModified.png)