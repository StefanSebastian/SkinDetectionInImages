import pickle


def save_object(obj, name):
    """
    Save an object to a file

    :param obj:
    :param name:
    :return:
    """
    with open(name + '.pkl', 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)


def load_object(name):
    """
    Load object from file

    :param name:
    :return:
    """
    with open(name, 'rb') as file:
        return pickle.load(file)
