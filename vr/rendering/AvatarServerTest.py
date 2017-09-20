import sys
import AvatarServer
sys.path.append('../') # Add directory of avatar_data.py to path
import avatar_data

file_index = 1
# TODO put these somewhere sensible for reference.
feature_labels = ['LController','RController','Headset']
target_labels = ['Front', 'Back','LeftElbow','RightElbow','LeftKnee','RightKnee']

# Read in some data.
features, targets = avatar_data.read_data('../../',k=file_index, target_labels=target_labels)

# Flatten out the labels into full x,y,z to match the numpy arrays.
# TODO this methodology should go into a helper function.
feature_labels_full = [avatar_data.generate_labels_for_target(label) for label in feature_labels]
flatten = lambda l: [item for sublist in l for item in sublist]
feature_labels_full = flatten(feature_labels_full)
target_labels_full = [avatar_data.generate_labels_for_target(label) for label in target_labels]
target_labels_full = flatten(target_labels_full)

# Connect to a client.
server = AvatarServer.AvatarServer(port=54321)
server.connect_to_client()

# Transmit the first 100 frames.
for i in range(0, 100):
    # Generate json compatible dictionaries.
    feature_dict = AvatarServer.generate_dictionary_for_data(features[i, :], feature_labels_full)
    target_dict = AvatarServer.generate_dictionary_for_data(targets[i, :], target_labels_full)
    # Combine dictionaries into one message.
    message = AvatarServer.merge_dictionaries(feature_dict, target_dict)
    server.send_object(message)

input()
server.close_connection()


