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

SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "timestamp",
      "fieldType": "datetime"
    },
    {
      "fieldName": "hourly_traffic_count1",
      "fieldType": "float",
      "maxValue": 5800.0,
      "minValue": 500.0
    },
    {
      "fieldName": "hourly_traffic_count2",
      "fieldType": "float",
      "maxValue": 1300.0,
      "minValue": 20.0
    }    
  ],
  "streamDef": {
    "info": "hourly_traffic_count1",
    "version": 1,
    "streams": [
      {
        "info": "Traffic Data",
        "source": "file://cleanTrafficData2.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },

  "inferenceType": "TemporalMultiStep",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": "hourly_traffic_count1"
  },
  "iterationCount": -1,
  "swarmSize": "medium"
}
