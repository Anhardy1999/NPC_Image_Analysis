Default Analysis
================

The default analysis was created based off an analysis process that worked generally
will on all of the images that this project was originally created for.

As such, this process is automatic when you click the button to start the analysis
preventing any intervention. 

This can be used as a general guide for what analysis processes might work. 
Image analysis is a process that doesn't work for all images so it can require tweaking
to better suit images loaded into the application. 

.. note:: 
    The default analysis presumes that you are using the skeleton file and the image to be analyzed. 

Image Processing Steps
----------------------
    - Skeleton Dilation (Default dilation is 10)
    - Cropping of the image to the length/size/volume of the skeleton
    - Median filter with a cube width of 3
    - Background subtraction using a gaussion blur of strength 7.
    - Adaptive Histogram Equalization: This consists of using scikit image's adaptive histogram equalization option. It is then multipled to the background subtracted image to give the final contrast.
    - Multiotsu mask at 2 classes (there are presumed only 2 classes, background and regions of interest)
    - Default morphology: Dilation morphology and then closing morphology
    - Labels are added to the image.

This information can also be found in the "Help" section of the application.

