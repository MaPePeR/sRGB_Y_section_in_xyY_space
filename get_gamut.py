import colour
from colour import XYZ_to_xy, MSDS_CMFS
import numpy as np
import base64

#From colour.plotting.diagrams.plot_spectral_locus()

cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]

illuminant = colour.plotting.CONSTANTS_COLOUR_STYLE.colour.colourspace.whitepoint

# Keep first and last point and every 4th inbetween
xy = XYZ_to_xy(np.concatenate([
    cmfs.values[(0,),:],
    cmfs.values[1:-1:4,:],
    cmfs.values[(-1,),:],
]), illuminant)

locus = np.array(xy, dtype=np.float32)
converted = base64.b64encode(locus)

for i in range(0, len(converted), 100):
    print(converted[i:i+100].decode("ascii"))


