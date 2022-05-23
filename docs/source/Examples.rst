Example Usage 
=============

Using NPC Image Analysis
**************************
.. image:: ../Example_Images/1.jpg
    :width: 400 
    :align: center

Above is what the application will look like upon initialization. The
application's simple interface was designed to not overwhelm the user 
with too much information and options at one time. 

We'll start with loading in the images.
When the loading button is clicked, the status screen will inform you of the order
of the images. 

.. warning::
    You must import the images in a specific order:
    
    1. Skeleton file first (this must be a .tiff or .tif file)
    
    2. Your image for analysis

    They must be the same size, or else the application will not be able
    to process the images. 

After the images are loaded, the "Status" screen of the application will list
the images loaded and will ask the user to confirm that these are correct.

.. image:: ../Example_Images/2.jpg
    :width: 400 
    :align: center

Choosing an analysis option
*****************************

Clicking "Perform Analysis" will open another small window. There are two options to choose for analysis: The "Default Analysis" option and the "Custom Analysis" option.

Default Analysis
-----------------

When you select "Default Analysis" this will ask you to input the image spacing. This is asking for the "z" spacing of your
images. 

.. note:: 
    The spacing indicates the distance between each "z" plane image to create the depth of the image. 

For this example, we are using .5.

.. image:: ../Example_Images/3.jpg
    :width: 400 
    :align: center

Pressing "Okay" will initiate the analysis. A napari viewer will open. While this process is occuring, the
screen may remain white and the app may be unresponsive as it operates. Don't panic, this is a sign that it is working.

If it remains white and the app is unresponsive for an extended period of time, you should consider the size of your images
as this will contribute to the amount of time processing will take. 

When the process is complete, you will be able to interact with the napari viewer and see what the final results are.

.. note::
    If you are unhappy with this final result, you can begin a new process with the Custom Analysis option.
    This will start a new napari viewer and cannot continue with the default analysis as you will be restarting
    from the beginning. 

    You can follow through the default analysis process and tweak it by visiting the :doc:`Default Analysis Usage` page.

Custom Analysis
-------------------

Selecting "Custom Analysis" will expand the current window with the image processing options. Additionally,
it will ask the same question as in the default analysis "What is the image spacing?" Again, you will provide the "z" spacing
of your images. 

.. note:: 
    The spacing indicates the distance between each "z" plane image to create the depth of the image. 

Here we will be using .5

.. image:: ../Example_Images/7.jpg
    :width: 600 
    :align: center

Upon entering your spacing, a napari viewer window will open. It will be empty and allow you the option to begin
your image processing.

.. image:: ../Example_Images/8.jpg
    :width: 600 
    :align: center

We will start with a skeleton dilation. Clicking "Skeleton Dilation" will prompt you to input how much you would like
to dilate the skeleton image. 

The default is 10. For this example, we will use 10. 

.. warning::
    This operation can take some time, so if it appears that application is frozen, keep in mind the size of the images as this
    is a contributing factor to the processing power and time consumption of each operation.

.. image:: ../Example_Images/9.jpg
    :width: 600 
    :align: center

This process will return the dilated skeleton as well as the cropped image called 'ROI'. The "status" window will also update with the process
that was just performed and what value was performed to allow the user to keep track of what operations they have performed so far.

Next, we will apply a median filter. Upon clicking "Median Filter" the application will prompt you to
input the cube width to use. The default is 3 which we will use for this example.

This will return the image after the median filter has been applied. 

.. image:: ../Example_Images/10.jpg
    :width: 600 
    :align: center

We will apply a background subtraction after this to even out the surrounding background and make it easier for the 
final step of identify our regions of interest easier. Clicking this will prompt the user to input a gaussian sigma 
or how strong the blur will be. 

The default is 7. In this case, we'll use 10.

.. image:: ../Example_Images/11.jpg
    :width: 600 
    :align: center

While we could apply the sobel filter which will define the edges of the objects within this image, it's not really
necessary here. We want to make the images within the radial process is clear so defining the edges of this particular image
may not work in our favor.

We'll enhance the contrast of the image now. One of the byproducts of a background subtraction is that it can also lower the contrast
of the overall image as we try to smooth out the background. We'll try the "Rescale Intensity" option first. 

Clicking this button will prompt you to enter two values, the minimum intensity value of the image and the maximum intensity values in the image.
They are percentages in this case, but the defaults for rescaled intensity is .5 and 99.5 for minimum and maximum respectively.

.. note:: 
    Choosing the minimum and maximum intensity values means that you will be deciding what the minimum intensity values allowed within the total 
    image allowed and the maximum intensity values allowed in the overall image. If you choose .5 and 99.5, you will be clipping the darkest and 
    brightest 0.5% of pixels within the image thus increasing the overall contrast of the image. 

We will use 99.65 and 99.98 for the minimum and maximum values respectively.

.. image:: ../Example_Images/12.jpg
    :width: 600 
    :align: center

This returns the above. While it is not terrible, it's not exactly what we're looking for right now and adjusting the contrast this way will require 
a little more playing around. 

We'll click the previous image button to go back one step. This will add the previous image we were working with to the viewer once more and the status will
update with our selection.

.. note:: 
    You can only go back one step at the moment. 

We should return to the background subtracted image now. We'll go ahead and use the "Adaptive Histogram Equalizaiton" option which will operate automatically.
The purpose of this option is to provide an automatic contrast that doesn't require any input from the user. The Rescale Intensity option allows more freedom for the user
and can be applied after the adaptive histogram equalization operation is performed to continue to tweak the contrast. 

.. image:: ../Example_Images/13.jpg
    :width: 600 
    :align: center

We now have our final contrasted image. From here, it's time to select a mask option. In the default analysis, the multiotsu mask is used. If you don't like the mask that is used
you can use the "Use Most Recent Image" option to return to the image prior to using the mask and play around with the options you would like to use. 

We'll use the multiotsu mask with 2 classes. 

.. image:: ../Example_Images/14.jpg
    :width: 600 
    :align: center

Great! This is looking pretty good, but we can probably define this mask a little bit. The default morphology option allows the user to use the morphological steps that are used in the
Default Analysis. The default analysis uses the Dilation and Closing morphological adjustments in that order.

We can see what each of those look like here by using them in that order instead of pressing Default Morphology. 

.. image:: ../Example_Images/15.jpg
    :width: 600 
    :align: center
    
This final mask looks pretty good. Once you're pleased with the final mask, you can generate labels by pressing the "Get Labels" options. Labels will be generated and added to the viewer.

.. image:: ../Example_Images/16.jpg
    :width: 600 
    :align: center

From here, we can start getting data from our analysis.

Getting ROI Properties
************************
From here you can begin the process of obtaining properties of the identified regions of interest (ROI) by clicking the
"Get ROI Properties" button.

Clicking this button will open up a new window allowing you to select the data you would like to obtain.
For this example, we'll select "area", "mean_intensity", and "centroids". 

After that, click the "Start ROI Properties Analysis" button.

.. image:: ../Example_Images/5.jpg
    :width: 400 
    :align: center

After this process is completed, you will be presented with a table containing data for each region of interest and the properties
you selected.  

.. image:: ../Example_Images/6.jpg
    :width: 600 
    :align: center

Clicking the "Export ROI Properties" button will open the save dialog and allow you to save your data.
If you would like to get additional properties, you can return to the window with your property options and
generate a new table. 

Example Data Returned
**********************

.. note:: 
    This does not include all of the data that can be returned. Additionally, all data returned regarding points or coordinates
    (this includes bbox, centroids, coords) are returned in z, x, y order (plane, row, column)
.. csv-table:: Sample Data
    :file: ../test_properties.csv
    :widths: 30,30,30,30,30,30
    :header-rows: 1

The data above is generated using sci-kit image's regionprops table module. If you would like to
read more about it and the function you can find it `here <https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.regionprops_table>`_.

