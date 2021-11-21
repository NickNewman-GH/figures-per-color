import matplotlib.pyplot as plt
import numpy as np
from skimage import color
from skimage.measure import label, regionprops

def det_color(hsv):
    colors = []
    auto_diff = np.mean(np.diff(hsv))
    same_colors = np.array([hsv[1]])
    prev_color = hsv[1]
    l = len(hsv)
    for ci in range(2, l):
        if hsv[ci] - prev_color > auto_diff:
            prev_color = hsv[ci]
            colors.append(np.mean(same_colors))
            same_colors = np.array([hsv[ci]])
        else:
            prev_color = hsv[ci]
            same_colors = np.append(same_colors, hsv[ci])
        if ci == l - 1:
            colors.append(np.mean(same_colors))
    return colors

def figure_per_color(image, colors):
    fig_per_color = {}
    auto_diff = np.mean(np.diff(np.unique(image)))
    binary = np.zeros((image.shape[0], image.shape[1]))
    binary[image > 0] = 1
    labeled = label(binary)
    for l in range(1, np.max(labeled) + 1):
        c = np.mean(image[labeled == l])
        for color in colors:
            if abs(color - c) <= auto_diff:
                fig_per_color[color] = 1 if color not in fig_per_color else fig_per_color[color] + 1
                break
    return fig_per_color

image = plt.imread("imgs/balls_and_rects.png")

image = color.rgb2hsv(image)

binary = np.zeros((image.shape[0], image.shape[1]))
binary[image[:,:,0] > 0] = 1

rects = np.zeros_like(image)

labeled = label(binary)
print(f"Total figures {np.max(labeled)}")

regions = regionprops(labeled)

for region in regions:
    if region.image[0, 0] == 1:
        binary[labeled == region.label] = 0

circles = image.copy()
circles[binary == 0] = np.array([0, 0, 0])
rects = image.copy()
rects[binary != 0] = np.array([0, 0, 0])

circles_colors = det_color(np.unique(circles[:, :, 0]))
rects_circles = det_color(np.unique(rects[:, :, 0]))

# print(f"""Circles colors -> 
# {circles_colors}
# Rectangles colors -> 
# {rects_circles}""")

circles_per_color = figure_per_color(circles[:, :, 0], circles_colors)
rects_per_color = figure_per_color(rects[:, :, 0], rects_circles)

circles_per_color = [str(key) + ": " + str(circles_per_color[key]) + "\n" for key in sorted(circles_per_color)]
rects_per_color = [str(key) + ": " + str(rects_per_color[key]) + "\n" for key in sorted(rects_per_color)]

print(f"""
Circles for each color -> 
{''.join(circles_per_color)}
Rectangles for each color -> 
{''.join(rects_per_color)}""")