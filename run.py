#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
Groups together code used for creating a NuPIC model and dealing with IO.
(This is a component of the One Hot Gym Prediction Tutorial.)
"""
import importlib
import sys
import csv
import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

import nupic_output


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
DATA_NAME = "cleanTrafficData"
DATA_DIR = "./data/"
MODEL_PARAMS_DIR = "./model_params"

# 2011-01-12 01:00:00
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "hourly_traffic_count"})
  return model



def getModelParamsFromName(roadName):
  importName = "model_params.%s_model_params" % (
    roadName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % roadName)
  return importedModelParams



def runIoThroughNupic(inputData, model, roadName, plot):
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  if plot:
    output = nupic_output.NuPICPlotOutput([roadName])
  else:
    output = nupic_output.NuPICFileOutput([roadName])

  counter = 0
  for row in csvReader:
    counter += 1
    if (counter % 100 == 0):
      print "Read %i lines..." % counter
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    traffic_count = float(row[1])
    result = model.run({
      "timestamp": timestamp,
      "hourly_traffic_count": traffic_count
    })

    if plot:
      result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    output.write([timestamp], [traffic_count], [prediction])

  inputFile.close()
  output.close()



def runModel(roadName, plot=False):
  print "Creating model from %s..." % roadName
  model = createModel(getModelParamsFromName(roadName))
  inputData = "%s/%s.csv" % (DATA_DIR, roadName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, roadName, plot)



if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]

  if len(args)>0:
    DATA_NAME = args[0]
  else:
    DATA_NAME = "cleanTrafficData10003"

  if "--plot" in args:
    plot = True
  runModel(DATA_NAME, plot=plot)