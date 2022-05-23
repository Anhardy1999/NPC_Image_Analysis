Region Properties
====================

area
********

The property calculates the area of the region of interest. For 3D options this
really means volume as it is taking into account the x, y, and z planes.

bbox
******

Calculates the boundary box points locations for each plane. This returns six columns
as it accounts for the highest and lowest x, y, and z planes coordinates.

bbox_area
**********

Calculates the bounding box area based on the bounding box coordinate points. As this is
3D this is closer to volume than area.

max_intensity
**************

Calculates the maximum intensity for each of the ROIs identified. This takes into account the 
passed in intensity_image. For this program, it uses the original image so that the intensity
values are not impacted by the processing steps.

mean_intensity
***************

Calculates the mean intensity for each of the the ROIs identified. This takes into account the 
passed in intensity_image. For this program, it uses the original image so that the intensity
values are not impacted by the processing steps.

min_intensity
**************

Calculates the min intensity for each of the the ROIs identified. This takes into account the 
passed in intensity_image. For this program, it uses the original image so that the intensity
values are not impacted by the processing steps.

equivalent_diameter
********************

Calculates the diameter of a circle with the same area as the region.

minor_axis_length
********************

The length of the minor axis of the ellipse that has the same normalized second central moments 
as the region; that is, the same normalized variance as the region which is a measure used to quantify 
whether the set obsevered occurences are clustered or dispersed. 

major_axis_length
*******************

The length of the major axis of the ellipse that has the same normalized second central moments 
as the region; that is, the same normalized variance as the region which is a measure used to quantify 
whether the set obsevered occurences are clustered or dispersed. 

centroid
*********

This returns the coordinates of the central point within the specific region of interest. Creates three columns
with x, y, and z coordinates.

coords
********

Returns the coordinate list (plane, row, col) of the region
