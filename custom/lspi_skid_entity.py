# *****************************************************************************
# Â© Copyright IBM Corp. 2018.  All Rights Reserved.
#
# This program and the accompanying materials
# are made available under the terms of the Apache V2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# *****************************************************************************

'''
The entity module contains sample entity types
'''

import logging
import datetime as dt
import json
import importlib
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func

from . import metadata
from . import bif
from . import ui
from . import estimator as est

logger = logging.getLogger(__name__)

SAMPLE_FN_1 = '''
def f(df,parameters):
    series = df[parameters["input_items"][0]]
    out = series*parameters['param_1']
    return(out)
'''


class EmptyEntityType(metadata.EntityType):

    def __init__(self, name, db, db_schema=None, timestamp='evt_timestamp',
                 description=''):
        args = []
        kw = {'_timestamp': 'evt_timestamp',
              '_db_schema': db_schema,
              'description': description
              }
        super().__init__(name, db, *args, **kw)


class LSPI_Smart_Skid(metadata.BaseCustomEntityType):
    '''
    This sample shows simulated time series data for an industrial boiler.
    It demostrates how to perform Monte Carlo simulation. It also
    shows how to apply heuristics to detect leaks.
    '''

    def __init__(self, name, db, generate_days=0, db_schema=None, description=None, drop_existing=False):
        # constants
        constants = []

        # granularities
        granularities = []

        columns = []
        # columns
        columns.append(Column('injection_rate', Float())) #gal/day
        columns.append(Column('lead_time', Float())) #days
        columns.append(Column('min_supply', Float())) #gal
        columns.append(Column('tank_fill_level', Float())) #gal

        functions = []
        # simulation settings
        sim = {
            'data_item_mean': {'injection_rate': 100,
                               'lead_time': 3,
                               'min_supply': 600,
                               'tank_fill_level': 3000,
                               },
            'data_item_sd': {'injection_rate': 50,
                             'lead_time': 2,
                             'min_supply': 300,
                             'tank_fill_level': 1000
                             }
        }

        ids = ['lp-12332','lp-2334','lp-20011','lp-20022','lp-387721','lp-2277']

        generator = bif.EntityDataGenerator(ids, **sim)
        functions.append(generator)

        # # temperature depends on set point
        # functions.append(bif.RandomNoise(input_items=['injection_rate'],
        #                                  standard_deviation=50,
        #                                  output_items=['temperature']))
        # # discharge percent is a uniform random value
        # functions.append(bif.RandomUniform(min_value=0.1,
        #                                    max_value=0.2,
        #                                    output_item='discharge_perc'))
        # # discharge_rate
        # functions.append(bif.PythonExpression(
        #     expression='df["input_flow_rate"] * df["discharge_perc"]',
        #     output_name='discharge_flow_rate'
        # ))
        # # output_flow_rate
        # functions.append(bif.PythonExpression(
        #     expression='df["input_flow_rate"] * df["discharge_flow_rate"]',
        #     output_name='output_flow_rate'
        # ))
        #
        # # roughing out design of entity with fake recommendations
        # functions.append(bif.RandomDiscreteNumeric(
        #     discrete_values=[0.001,
        #                      0.001,
        #                      0.001,
        #                      0.5,
        #                      0.7],
        #     probabilities=[0.9, 0.05, 0.02, 0.02, 0.01],
        #     output_item='p_leak'
        # ))

        # dimension columns
        dimension_columns = [
            Column('customer', String(50)),
            Column('pipeline', String(50)),
            Column('warehouse', String(50))
        ]

        super().__init__(name=name,
                         db=db,
                         constants=constants,
                         granularities=granularities,
                         columns=columns,
                         functions=functions,
                         dimension_columns=dimension_columns,
                         output_items_extended_metadata={},
                         generate_days=generate_days,
                         drop_existing=drop_existing,
                         description=description,
                         db_schema=db_schema)