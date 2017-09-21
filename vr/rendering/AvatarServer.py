"""
Module for transmitting avatar data to the Unity renderer.
"""

import json
import socket


def generate_labels_full(feature_labels, target_labels):
    """
    Generates the full set of labels for the data to be rendered.
    :param feature_labels: labels for features
    :param target_labels:  labels for targets and predictions
    :return: feature, target and predicted labels in full
    """
    feature_labels_full = [generate_labels_for_target(label) for label in feature_labels]
    flatten = lambda l: [item for sublist in l for item in sublist]
    feature_labels_full = flatten(feature_labels_full)
    target_labels_full = [generate_labels_for_target(label) for label in target_labels]
    target_labels_full = flatten(target_labels_full)
    pred_labels = [label + str("Pred") for label in target_labels]
    pred_labels_full = [generate_labels_for_target(label) for label in pred_labels]
    pred_labels_full = flatten(pred_labels_full)
    return feature_labels_full, target_labels_full, pred_labels_full


def generate_labels_for_target(target_label, quaternion=False):
    """
    Generates a set of flattened labels i.e. with X,Y,Z appended

    :param target_label: label to flatten
    :param quaternion: if set to true, will add a W for the last component of the quaternion. 
    :return: list of labels with X,Y,Z appended
    """

    coords = ['X', 'Y', 'Z']
    if quaternion:
        coords.append('W')
    return ["{0}{1}".format(target_label, coord) for coord in coords]


def send_data_to_render(server, features, targets, targets_predicted,feature_labels_full,target_labels_full, pred_labels_full ):
    """
    Sends data to the specified server to render
    :param server: server to send data to
    :param features: feature data to render
    :param targets: target data to render
    :param targets_predicted: predicted data to render
    :param feature_labels_full: feature labels
    :param target_labels_full: target labels
    :param pred_labels_full: predicted data labels
    :return: returns nothing
    """
    for f, t, p in zip(features, targets, targets_predicted):
        message = generate_message(f, feature_labels_full,t, target_labels_full,p, pred_labels_full)
        server.send_object(message)
    return


def generate_message(f, feature_labels_full,t, target_labels_full,p, pred_labels_full):
    """
    Generates a message that is sent to the renderer from input data to be rendered.
    :param f: feature data to be rendered
    :param feature_labels_full: labels for feature data
    :param t: target data to be rendered
    :param target_labels_full: labels for target data
    :param p: predicted target data to be rendered
    :param pred_labels_full: labels for predicted data
    :return: a dictionary containing the message to be sent to the renderer
    """
    feature_dict = generate_dictionary_for_data(f, feature_labels_full)
    target_dict = generate_dictionary_for_data(t, target_labels_full)
    pred_dict = generate_dictionary_for_data(p, pred_labels_full)
    return merge_dictionaries(feature_dict, target_dict, pred_dict)


def add_quaternion_to_message(dictionary, quaternion, label):
    """
    Adds a quaternion with the specified label to an existing dictionary. 
    
    Use in conjunction with generate_message to send a quaternion along with 
    other feature data to renderer.
    :param dictionary: A dictionary that is intended to be sent to the renderer
    :param quaternion: Array of length 4 that represents the quaternion.
    :param label: The label that matches this quaternion, e.g. "Headset". 
    :return: The message with a quaternion dictionary appended. 
    """
    label = label + "Quaternion"
    full_labels = generate_labels_for_target(label, True)
    quat_dict = generate_dictionary_for_data(quaternion, full_labels)
    return merge_dictionaries(dictionary, quat_dict)

class PrettyFloat(float):
    """
    Class that represents float to 4 decimal places. 
    Used for transmitting smaller json strings for rendering. 
    """
    def __repr__(self):
        return '%.4f' % self


def pretty_floats(obj):
    """
    Converts floats in an object into 'class:PrettyFloat'.
    :param obj: The object containing floats to be converted.
    :return: The object, with floats replaced by 'class:PrettyFloat'
    """
    if isinstance(obj, float):
        result = PrettyFloat(float('%.4f' % obj))
        return result
    elif isinstance(obj, dict):
        return dict((k, pretty_floats(v)) for k, v in list(obj.items()))
    elif isinstance(obj, (list, tuple)):
        return list(map(pretty_floats, obj))
    return obj


def merge_dictionaries(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def generate_dictionary_for_data(data_row, labels):
    """
    Generates a dictionary for a given row of data and labels. 
    TODO Automate this behaviour. 
    If the data contains serialised vectors, with labels ending in X, Y, Z or W (e.g. LControllerX), this method will 
    combine the vector in the resulting dictionary.
    
    :param data_row: List of data values. 
    :param labels: List of labels of length len(data_row) corresponding to data_row.
    :return: Dictionary with labels and values. 
    """
    dictionary = {}
    coordinate_labels = ["X", "Y", "Z", "W"]
    i = 0
    while i < len(labels):
        label = str(labels[i])
        value = data_row[i]

        if label.endswith(coordinate_labels[0]):
            label = label[:-len(coordinate_labels[0])]
            coordinate_label = 0
            vector = []
            while coordinate_label < len(coordinate_labels) and i < len(labels):
                if str(labels[i]).endswith(coordinate_labels[coordinate_label]):
                    vector.append(float(data_row[i]))
                    coordinate_label += 1
                    i += 1
                else:
                    break
            value = vector
        else:
            i+=1
        dictionary[label] = value

    return dictionary


class AvatarServer:
    """
    Class for transmitting avatar data to a client, using json strings.
    
    The API for transmitting to Unity is based on Json dictionaries, with the following known labels: 
    
    Features:
    "Headset" - The position of the headset. 
    "LController" - The position of the left controller. 
    "RController - The position of the right controller. 

    Targets:
    "LeftElbow" - The position of the left elbow. 
    "RightElbow" - The position of the right elbow. 
    "Back": - The position of the back. 
    "Front" - The position of the front. 
    "LeftKnee" - The position of the left knee. 
    "RightKnee" - The position of the right knee.

    Predictions:
    "LeftElbowPred - The predicted position of the left elbow. 
    "RightElbowPred" - The predicted position of the right elbow.
    "BackPred" - The predicted position of the back. 
    "FrontPred" - The predicted position of the front.
    "LeftKneePred" - The predicted position of the left knee. 
    "RightKneePred" - The predicted position of the right knee. 

    Every time the client receives a json dictionary, it treats it as a frame. Therefore, a full frame consisting of 
    features, targets and predictions would consist of the following json string: 
    
    '{
      "Headset":[0.0548,1.0083,-0.2196],
      "LeftKnee":[-0.282,-0.5943,-0.1825],
      "LController":[-0.1096,1.0379,0.1098],
      "RightElbowPred":[0.3172,0.2597,-0.4031],
      "RController":[0.0548,0.4237,0.1098],
      "RightKneePred":[0.0238,-0.5896,-0.203],
      "Back":[0.1008,0.2426,-0.4191],
      "LeftKneePred":[-0.1462,-0.6049,-0.1452],
      "RightElbow":[0.3412,0.2161,-0.3188],
      "RightKnee":[-0.0241,-0.5912,-0.1936],
      "LeftElbowPred":[-0.2924,0.6117,-0.1557],
      "LeftElbow":[-0.3916,0.5587,-0.2194],
      "BackPred":[0.0358,0.2301,-0.4564],
      "Front":[-0.0027,-0.0809,-0.0913],
      "FrontPred":[-0.0127,-0.1371,-0.1268]}\n'
    '}
    
    The method generate_dictionary_for_data in the module avatarServer can be used to generate a python dictionary 
    for a list of data. See AvatarServerTest.py for an example of sending features and targets. 
    """

    def __init__(self, host="localhost", port=54321):
        """
        Initialises the avatar socket server. 
        
        :param host: IP address to connect to, defaults to localhost. 
        :param port: Port to connect to. 
        """
        self.host = host
        self.port = port
        self.clientsocket = None
        self.clientaddr = None
        self.socket = None
        self.initialise_server(host, port)

    def initialise_server(self, host="localhost", port=54321):
        """
        Initialises the avatar socket server. 
        
        :param host: IP address to connect to, defaults to localhost. 
        :param port: Port to connect to. 
        :return: 
        """
        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        # start listening
        self.socket.listen(5)

    def connect_to_client(self):
        """
        Connects to a client. This is a blocking connection, so will not return until a client connects.
        :return: Socket that has connected.
        """
        print("Waiting for client to connect...")
        self.clientsocket, self.clientaddr = self.socket.accept()
        print(("Got a connection from %s" % str(self.clientaddr)))
        return self.clientsocket

    def is_connected(self):
        """
        Indicates whether the avatar server is connected to a client.
        :return: True if a client is connected, False otherwise. 
        """
        if self.clientsocket is None:
            return False
        # TODO make connection testing more robust.
        return True

    def close_connection(self):
        """
        Closes a connection with the active client.
        :return: 
        """
        if self.clientsocket is None:
            return
        print(("Closing connection with %s" % str(self.clientaddr)))
        self.clientsocket.shutdown(socket.SHUT_RDWR)
        self.clientsocket.close()
        self.clientsocket = None


    def send_object(self, dictionary):
        """
        Sends an object over the connection, by serializing it to json. 
        :param dictionary: The dictionary of values to be sent. 
        :return: 
        """
        if self.clientsocket is None:
            raise ValueError("No client connected.")
        json_obj = json.dumps(pretty_floats(dictionary), separators=(',',':')) + "\n"
        print(("Transmitting string", json_obj))

        try:
            self.clientsocket.sendall(json_obj.encode('ascii'))
        except socket.error as err:
            print(("Error trying to transmit: " + str(err)))
            print("Will now close connection...")
            self.close_connection()



