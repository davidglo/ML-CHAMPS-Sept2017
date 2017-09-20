import pyglet
import pyglet.gl
from pyglet.window import key
import numpy as np
import colors
from square_class import square_class
import sys
sys.path.append('../')
import avatar_data

def initialize(features_data,targets_data,predicted_data):
    """Before calling the graphics window, we calculate a cube that no points leave in any time frame.
    This is a way to center the points. All data passed to this is (frame, feature, xyz) numpy array."""

    # Panel size, to constrain points within
    panel_pixels = 420

    # Set up arrays for standardized data
    features_standardized_data = np.zeros((len(features_data[:,0,0]),len(features_data[0,:,0]),len(features_data[0,0,:])))
    targets_standardized_data = np.zeros((len(targets_data[:,0,0]),len(targets_data[0,:,0]),len(targets_data[0,0,:])))
    predicted_standardized_data = np.zeros((len(predicted_data[:,0,0]),len(predicted_data[0,:,0]),len(predicted_data[0,0,:])))

    # Find max/min values in each dimension, creating lists [[xmin,xmax],[ymin,ymax],[zmin,zmax]]
    minmax_features = [[np.amin(features_data[:,:,i]),np.amax(features_data[:,:,i])] for i in range(len(features_data[0,0,:]))]
    minmax_targets = [(np.amin(targets_data[:,:,i]),np.amax(targets_data[:,:,i])) for i in range(len(targets_data[0,0,:]))]
    minmax_predicted = [(np.amin(predicted_data[:,:,i]),np.amax(predicted_data[:,:,i])) for i in range(len(predicted_data[0,0,:]))]
    # Then overall min/max list calculated
    minmax_total = [[min(minmax_features[i][0],minmax_targets[i][0],minmax_predicted[i][0]),max(minmax_features[i][1],minmax_targets[i][1],minmax_predicted[i][1])] for i in range(len(minmax_features))]

    # Shift and scale the data so that it is all within a cube, with edge length
    # the the greatest (max-min) value, such that all coorinates, for the entire time
    # frame, are within the cube.
    window_scaling = float(panel_pixels)/float(max([(minmax_total[0][1]-minmax_total[0][0]),(minmax_total[1][1]-minmax_total[1][0]),(minmax_total[2][1]-minmax_total[2][0])]))
    for i in range(3):
        features_standardized_data[:,:,i] = (- minmax_total[i][0] + features_data[:,:,i]) * window_scaling
        targets_standardized_data[:, :, i] = (- minmax_total[i][0] + targets_data[:, :, i]) * window_scaling
        predicted_standardized_data[:, :, i] = (- minmax_total[i][0] + predicted_data[:, :, i]) * window_scaling

    # Call graphicsWindow class
    window = graphicsWindow(features_standardized_data,targets_standardized_data,predicted_standardized_data,panel_pixels)  # initialize a window class
    pyglet.clock.schedule_interval(window.update, 1/20.)  # tell pyglet the on_draw() & update() timestep
    pyglet.app.run()  # run the infinite pyglet loop

class graphicsWindow(pyglet.window.Window):
    def __init__(self,features_array,targets_array,predicted_array,panel_pixels):
        super(graphicsWindow, self).__init__()  # constructor for graphicsWindow class
        # Set full screen, or window size, here
        #self.set_fullscreen(True)
        self.set_size(panel_pixels*3,550)
        # Color and size of features
        feature_colors = ['red','red','white']
        feature_sizes = [8,8,10]
        # Color and size of targets
        predicted_colors = ['hotpink','hotpink','hotpink','hotpink','hotpink','hotpink','hotpink','hotpink','hotpink']#['blue','yellow','green','sienna','blue','yellow','green','sienna']
        target_colors = ['blue','blue','blue','blue','blue','blue','blue','blue','blue']
        target_sizes = [8,8,8,8,8,8,8,8,8]
        # Class needs input pixels in a window
        self.panel_pixels = panel_pixels
        # Shifting of panels up
        self.window_yheight = 70
        # Frame number currently on
        self.frame = 0
        # Record whether going forward (0), stopped (1) or reversed (2)
        self.forward_pause_reverse = 0

        # Obtain array of feature and target data
        self.features_array = features_array
        self.targets_array = targets_array
        self.predicted_array = predicted_array
        # Set up corresponding array of square for output
        self.squares_features = []
        self.squares_targets = []
        self.squares_predicted = []
        for i in range(len(self.features_array[0, :, 0])):
            self.squares_features.append(square_class(i, feature_colors[i], self.features_array[0,i,:], feature_sizes[i]))
        for i in range(len(self.targets_array[0,:,0])):
            self.squares_targets.append(square_class(i, target_colors[i], self.targets_array[0,i,:], target_sizes[i]))
            self.squares_predicted.append(square_class(i, predicted_colors[i], self.predicted_array[0,i,:], target_sizes[i]))

        # Set up background panels and labels
        self.squares_background = []
        temp = 2.**0.5
        self.squares_background.append(square_class(1,'dimgrey',np.array([self.panel_pixels/2.,self.window_yheight+self.panel_pixels/2.]),self.panel_pixels/temp))
        self.squares_background.append(square_class(2, 'darkgrey', np.array([3.*self.panel_pixels/2., self.window_yheight+self.panel_pixels/2.]), self.panel_pixels/temp))
        self.squares_background.append(square_class(3,'dimgrey',np.array([5.*self.panel_pixels/2.,self.window_yheight+self.panel_pixels/2.]),self.panel_pixels/temp))
        self.labels = []
        self.labels.append(pyglet.text.Label('xz',font_name = 'Arial', font_size = 12, x = self.panel_pixels/2., y = self.window_yheight/2.))
        self.labels.append(pyglet.text.Label('yz',font_name = 'Arial', font_size = 12, x = 3.*self.panel_pixels/2., y = self.window_yheight/2.))
        self.labels.append(pyglet.text.Label('xy',font_name = 'Arial', font_size = 12, x = 5.*self.panel_pixels/2., y = self.window_yheight/2.))

    def update(self, dt):
        # Set positions of feature and target squares based on input data
        for i in range(len(self.features_array[self.frame,:,0])):
            self.squares_features[i].setPosition(self.features_array[self.frame,i,:])
        for i in range(len(self.targets_array[self.frame,:,0])):
            self.squares_targets[i].setPosition(self.targets_array[self.frame,i,:])
            self.squares_predicted[i].setPosition(self.predicted_array[self.frame,i,:])
        # Increment current frame and loop back to start if finished
        if self.forward_pause_reverse == 0:
            self.frame += 1
            if self.frame == len(self.features_array[:, 0, 0]):
                self.frame = 0
        elif self.forward_pause_reverse == 2:
            self.frame -= 1
            if self.frame == 0:
                self.frame = len(self.features_array[:, 0, 0])-1

    def draw_vertices(self,vertexList,lineColor):
        # Draw vertices given list in pyglet form and lineColor variable
        pyglet.gl.glColor4f(colors.color[lineColor][0], colors.color[lineColor][1], colors.color[lineColor][2], colors.color[lineColor][3])
        vertexList.draw(pyglet.gl.GL_TRIANGLE_FAN)  # draw

    def on_draw(self):
        pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)    # clear the graphics buffer
        adjustment = [[0,self.window_yheight],[self.panel_pixels,self.window_yheight],[self.panel_pixels*2,self.window_yheight]]
        # Set dimensions for each plot
        dimensions = [[0,1],[2,1],[0,2]]
        # Draw background panel squares first
        for j in range(len(self.squares_background)):
            vertexList = self.squares_background[j].getBackSquare()
            lineColor = self.squares_background[j].getColor()  # openGL color specification
            self.draw_vertices(vertexList,lineColor)
        # Print out xy etc. labels
        for label in self.labels:
            label.draw()
        # Print out frame number
        frame_label = pyglet.text.Label("'Space' to pause.   'Enter' to reverse.   Frame: %s"%(str(self.frame)),font_name = 'Arial', font_size = 12, x = 800, y = 520)
        frame_label.draw()
        # Draw squares corresponding to feature and target coordinates
        for j in range(3):
            for i in range(len(self.features_array[self.frame,:,0])): # Loop over features
                vertexList = self.squares_features[i].calculateSquareVertices(dimensions[j],adjustment[j])
                lineColor = self.squares_features[i].getColor()             # openGL color specification
                self.draw_vertices(vertexList,lineColor)
            for i in range(len(self.targets_array[self.frame,:,0])):
                vertexList = self.squares_targets[i].calculateSquareVertices(dimensions[j], adjustment[j])
                lineColor = self.squares_targets[i].getColor()  # openGL color specification
                self.draw_vertices(vertexList,lineColor)
                vertexList = self.squares_predicted[i].calculateSquareVertices(dimensions[j], adjustment[j])
                lineColor = self.squares_predicted[i].getColor()  # openGL color specification
                self.draw_vertices(vertexList,lineColor)

    def on_key_press(self, symbol, modifiers):
    #Upon pressing space, change self.forward_pause_reverse
        if (symbol == key.SPACE):
            if (self.forward_pause_reverse == 0) or (self.forward_pause_reverse == 2):
                self.forward_pause_reverse = 1
            elif self.forward_pause_reverse == 1:
                self.forward_pause_reverse = 0
        if (symbol == key.ENTER):
            if (self.forward_pause_reverse == 0) or (self.forward_pause_reverse == 1):
                self.forward_pause_reverse = 2
            elif (self.forward_pause_reverse == 2):
                self.forward_pause_reverse = 0


def renderFrames(features, targets, predicted = []):
    if predicted == []:
        predicted = targets
    colors.generate_alpha_colors()
    ntimesteps = features.shape[0]
    # Pick out one frame, to work out number of features/targets, and coordinates
    example_frame_features = avatar_data.get_frame_slice(0, features)
    example_frame_targets = avatar_data.get_frame_slice(0, targets)
    example_frame_predicted = avatar_data.get_frame_slice(0, predicted)
    features_data = np.zeros((ntimesteps,len(example_frame_features[:,0]),len(example_frame_features[0,:])))
    targets_data = np.zeros((ntimesteps, len(example_frame_targets[:, 0]), len(example_frame_targets[0, :])))
    predicted_data = np.zeros((ntimesteps, len(example_frame_predicted[:, 0]), len(example_frame_predicted[0, :])))
    # Put together each frame into 3D array
    for i in range(ntimesteps):
        features_data[i,:,:] = avatar_data.get_frame_slice(i, features)
        targets_data[i, :, :] = avatar_data.get_frame_slice(i, targets)
        predicted_data[i,:,:] = avatar_data.get_frame_slice(i, predicted)
    # Call intializer, with relevant data
    initialize(features_data,targets_data,predicted_data)

# this is the main game engine loop
if __name__ == '__main__':

    colors.generate_alpha_colors()
    # Get Cartesian coordinates from avatar_data.py
    (features, targets) = avatar_data.read_data('../',k=0,target_labels=['Front','Back'])
    renderFrames(features,targets,targets)