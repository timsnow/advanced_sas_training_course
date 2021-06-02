# From Python itself
from os import path
import logging

# From bumps
from bumps.names import *
from bumps.fitters import fit

# From matplotlib
from matplotlib import pyplot as plt

# From sasmodels
from sasmodels.data import empty_data1D
from sasmodels.core import load_model
from sasmodels.bumps_model import Model, Experiment


class DataFitter1D():

	def __init__(self, loggingLevel = logging.WARNING):
		# Set up a logger for the class first
		self.sasLogger = logging.getLogger('sasmodels')
		self.sasLogger.setLevel(loggingLevel)

		self.consoleLogHandler = logging.StreamHandler()
		self.consoleLogHandler.setLevel(loggingLevel)

		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.consoleLogHandler.setFormatter(formatter)
		self.sasLogger.addHandler(self.consoleLogHandler)

		# Now set up a data handler for sasmodels
		self.dataHolder = empty_data1D(1)
		self.parameterDictionary = {}
		self.contextDictionary = {}
		self.fittingProblem = None


	def loadData(self, xData = None, yData = None, dxData = None, dyData = None):
		if (len(xData) != len(yData)):
			raise AssertionError('q axis and intensity dataset are of different lengths (x and y axis data), data holder not initialised.')

		if (xData is None):
			raise ValueError('No q axis given (x axis), data holder not initialised.')

		if (yData is None):
			raise ValueError('No intensity data given (y axis), data holder not initialised.')

		self.dataHolder.x = xData
		self.dataHolder.y = yData
		self.dataHolder.qmin = xData.min()
		self.dataHolder.qmax = xData.max()

		if (dxData is None):
			self.sasLogger.warning('No dq data given (dx). Uncertainties of 5 % have been added.')
			self.dataHolder.dx = self.dataHolder.x * 0.05
		else:
			self.dataHolder.dx = dxData

		if (dyData is None):
			self.sasLogger.warning('No intensity uncertainties provided (dy). Uncertainties of 5 % have been added.')
			self.dataHolder.dy = self.dataHolder.y * 0.05
		else:
			self.dataHolder.dy = dyData


	def loadFittingParameters(self, passedParameters = None):
		if (passedParameters is None):
			raise ValueError("No parameters were passed, no parameters were loaded.")
		else:
			self.parameterDictionary = passedParameters


	def setFittingRange(self, qMin, qMax):
		# Check data holder exists and if not return, if it does, check they're within range and set them
		if (self.dataHolder.x.min() is None):
			raise ValueError("No dataset loaded. Please load a dataset first before altering the fitting limits.")

		if (qMin > qMax):
			# Could reorder them but for safety I'm gong to return here and prompt the user to change them
			raise ValueError("Lower fitting bound given larger than the upper bound, please format correctly and retry. Fitting range unchanged.")

		if ((qMin < self.dataHolder.x.min()) and (qMin > self.dataHolder.x.max())):
			if ((qMax > self.dataHolder.x.max()) and (qMax < self.dataHolder.x.min())):
				self.dataHolder.qmin = qMin
				self.dataHolder.qmax = qMax
			else:
				raise ValueError("Upper fitting bound given not within dataset range, fitting range unchanged.")
		else:
			raise ValueError("Lower fitting bound given not within dataset range, fitting range unchanged.")


	def parameterParserFromString(self, parameterString = None):
		# Check data holder exists and if not return, if it does, check they're within range and set them
		if (parameterString is None):
			raise ValueError("Parameters have been passed. No fitting parameters have been set.")

		self.parameterDictionary.clear()
		self.contextDictionary.clear()
		parameterList = parameterString.split(':')

		for parameter in parameterList:

			keyValuePair = parameter.split(',')
			if (len(keyValuePair) == 1):
				continue
			elif (len(keyValuePair) == 2):
				self.contextDictionary[keyValuePair[0]] = keyValuePair[1]
			else:
				self.parameterDictionary[keyValuePair[0]] = keyValuePair[1:]


	def parameterParserFromTextFile(self, pathToFile = None):
		# Check file exists first
		if (path.exists(pathToFile)):
			fileHandle = open(pathToFile)
		else:
			raise OSError("The filepath given leads to a file that doesn't exist!")	

		fileText = fileHandle.readline()
		fileText.strip('\n')
		self.parameterParserFromString(fileText)


	def fitData(self):
		# Initalise the kernel and set up the limits to fit within
		kernel = load_model(self.contextDictionary['model_name'])
		initialFitValues = {}
		
		for key, value in self.parameterDictionary.items():
			initialFitValues[key] = float(value[1])

		model = Model(kernel, **initialFitValues)

		for key, value in self.parameterDictionary.items():
			# Is this parameter to be fitted?
			if value[0] == 'True':
				modelAttribute = getattr(model, key)
				modelBounds = getattr(modelAttribute, 'bounds')
				setattr(modelAttribute, 'fixed', False)
				setattr(modelAttribute, 'limits', [float(value[3]), float(value[4])])
				setattr(modelBounds, 'limits', [float(value[3]), float(value[4])])

		# Initial guess of fit model against data
		experimentProblem = Experiment(data=self.dataHolder, model=model)
		self.fittingProblem = FitProblem(experimentProblem)

		# Use the guess to fit the data against the model
		result = fit(self.fittingProblem)
		
		# Simulate the result and plot this data using matplotlib
		self.fittingProblem.simulate_data()
