"""colors is a simple module for creating a color dictionary"""

color = {}  # declare a color dictionary
color['yellow'] = [1.0, 1.0, 0.0, 1.0]  # fill each entry of the color dictionary with a list of three floats
color['blue'] = [0.0, 0.0, 1.0, 1.0]
color['red'] = [1.0, 0.0, 0.0, 1.0]
color['green'] = [0.0, 1.0, 0.0, 1.0]
color['sienna'] = [0.627, 0.322, 0.176, 1.0]
color['hotpink'] = [1.0, 0.412, 0.706, 1.0]
color['white'] = [1.0,1.0,1.0, 1.0]
color['dimgrey'] = [0.412, 0.412, 0.412, 1.0]
color['darkgrey'] = [0.663, 0.663, 0.663, 1.0]

def generate_alpha_colors(alpha=0.5):
    extra_colors = {}
    for c, v in color.items():
        new_str = "{0}{1}".format(c, "_alpha")
        new_color = v
        new_color[3] = alpha
        extra_colors[new_str] = new_color
    color.update(extra_colors)

if __name__ == "__main__":
    print('colors')

