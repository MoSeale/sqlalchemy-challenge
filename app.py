#############Dependencies

import numpy as np
import pandas as pd

import sqlalchemy
import sqlalchemy.ext.automap import automap_base
import sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

