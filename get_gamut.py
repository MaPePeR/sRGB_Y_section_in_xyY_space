import colour
from colour import XYZ_to_xy, MSDS_CMFS
import numpy as np
import base64

#From colour.plotting.diagrams.plot_spectral_locus()

cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]

illuminant = colour.plotting.CONSTANTS_COLOUR_STYLE.colour.colourspace.whitepoint

# Keep first and last point and every 4th inbetween
xy = XYZ_to_xy(cmfs.values, illuminant)

locus = np.array(xy, dtype=np.float32)

def distance_to_segment(x0, y0, x1, y1, x2, y2):
    return np.abs(
            (x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)
        ) / np.sqrt(
            (x2 - x1) ** 2 + (y2 + y1) ** 2
        )

def reduce_point_count(points, desired_count):
    while len(points) > desired_count:
        distances = distance_to_segment(points[1:-1, 0], points[1:-1, 1], points[:-2, 0], points[:-2, 1], points[2:, 0], points[2:, 1])
        minindex = np.argmin(distances) + 1
        points = points[np.arange(len(points)) != minindex]
    return points


def max_distance_interval(points, a, b):
    if a + 1 >= b:
        #Empty interval cannot be split again, so set distance to -1
        return (a, -1)
    distances = distance_to_segment(points[a + 1:b, 0], points[a + 1:b, 1], points[a, 0], points[a, 1], points[b, 0], points[b, 1])
    maxindex = np.argmax(distances)
    return (a + maxindex + 1, distances[maxindex])

def RDP(points, max_count):
    if len(points) <= max_count:
        return points
    intervals = {(0, len(points) - 1): max_distance_interval(points, 0, len(points) - 1)}
    point_count = 2
    while point_count < max_count:
        (interval, (maxindex, d)) = max(intervals.items(), key=lambda t: t[1][1])
        a, b = interval
        if d <= 0:
            raise "Cannot find line to split? Should not happen"
        del intervals[interval]
        intervals[(a, maxindex)] = max_distance_interval(points, a, maxindex)
        intervals[(maxindex, b)] = max_distance_interval(points, maxindex, b)
        point_count += 1
    indizes = set(a for a, b in intervals.keys())
    indizes.add(len(points) - 1)
    return points[sorted(indizes)]

#small_locus = reduce_point_count(locus, 100)
small_locus = RDP(locus, 100)

#import matplotlib.pyplot as plt
#plt.plot(locus[:, 0], locus[:, 1])
#plt.plot(small_locus[:, 0], small_locus[:, 1])
#plt.show()

converted = base64.b64encode(small_locus)

for i in range(0, len(converted), 100):
    print(converted[i:i+100].decode("ascii"))


