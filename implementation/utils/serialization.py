import pickle
from pickle import PicklingError

from sklearn.externals import joblib

from utils.log import LogFactory


class SerializationUtils:
    def __init__(self, logger=LogFactory.get_default_logger()):
        self.logger = logger

    def save_object(self, obj, name):
        """
        Save an object to a file

        :param obj:
        :param name:
        :return:
        """
        try:
            with open(name, 'wb') as file:
                pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)
        except PicklingError as e:
            self.logger.log("Could not dump object " + name)
            raise e

    def load_object(self, name):
        """
        Load object from file

        :param name:
        :return:
        """
        try:
            with open(name, 'rb') as file:
                return pickle.load(file)
        except EOFError as e:
            self.logger.log(str(e) + " for " + name)
            raise e

    def load_joblib_object(self, name):
        """
        Loads object with joblib library
        """
        try:
            return joblib.load(name)
        except EOFError as e:
            self.logger.log("Deserialization error for " + name)
            raise e

    def store_joblib_object(self, object, name):
        """
        Store object with joblib library
        """
        try:
            joblib.dump(object, name)
        except PicklingError as e:
            self.logger.log("Serialization error for " + name)
            raise e
