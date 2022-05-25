Usage
=====

Requirements
------------

Python 3.6 or above

Installation
------------

``pip install npc-image-analysis``

However, the sourcecode of this program can be found at this `github page <https://github.com/Anhardy1999/NPC_Image_Analysis>`_


General Usage
-------------

This software is intended to be modifiable in order to answer particular needs to identify organelles and structures.
Using this software, you will be able to look within the radial process of a specific cell of interest. This is used in conjuction with ImageJ's Simple Neurite Tracer.

To use this software, you will need... 
    - A greyscale tiff image that contains the channel for the organelles or structures of interest you would like analyzed
    - The skeleton file created from the simple neurite tracer as a .tiff file. You cannot use the .trace file for this as it cannot be read in.

After you load in your images using the "Load Images" button, you can selected "Perform Analysis".
You will be provided with two options, "Default Analysis" and "Custom Analysis". If you would like to just see what a default analysis would look like, selected Default Analysis.

This will ask for the Z spacing of your images. This only effects the presentation of your images not the analysis. From there, depending on the size of the image, it can take a while for the analysis to complete. If it looks temporarily frozen, that's possibly why.
You can find more information about the Default Analysis option and what operations are performed, selected the Default Analysis under the help window.

You can see examples of this file being used in the `github page <https://github.com/Anhardy1999/NPC_Image_Analysis>`_

While this program is tailored to a specific use case. The default analysis presumes that you are loading using a skeleton mask (or a skeleton/mask file in general) along with
an image to be analyzed. As a result, the program will require you to load two images and certain operations will presume that both files are loaded. However,
you can use most of the operations the skeleton file.

Why use a skeleton mask?
--------------------------
Originally this was used to isolate the file to a specific location for the analysis, however, this also reduced the overall file size and image size lowering the memory usage and
time required to process images. 