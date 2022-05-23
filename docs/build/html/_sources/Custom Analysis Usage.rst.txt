Custom Analysis Options
========================

Custom analysis allows you to customize the image processing steps. 
This is created to allow the user the opportunity to tailor the processing to the best of their ability
without having to worry about the code behind it. 

For information on what an operation might do, the `scikit image page <https://scikit-image.org/docs/stable/api/api.html>`_ (which these processing steps draw on) will 
be linked to allow the user to read more on its purpose. 

Below is a general list of the steps.

Main Processing Options
-------------------------
- Skeleton Dilation
    - Utilizes the `Morphology Binary Dilation Operation <https://scikit-image.org/docs/0.19.x/api/skimage.morphology.html#skimage.morphology.binary_dilation>`_
- Median Filter
    - Uses the `Median Filter <https://scikit-image.org/docs/0.19.x/api/skimage.filters.html#skimage.filters.median>`_ from skimage
- Background Subtraction 
    - Utilizes SciKit Image `Gaussian Filter <https://scikit-image.org/docs/0.19.x//api/skimage.filters.html#skimage.filters.gaussian>`_
- Sobel Filter
    - Uses the `Sobel Filter <https://scikit-image.org/docs/0.19.x/api/skimage.filters.html#skimage.filters.sobel>`_
- Adaptive Histogram Equalization
    - This consists of using scikit image's adaptive histogram equalization option. It is then multipled to the background subtracted image to give the final contrast.
    - Uses the `Adaptive Histogram Equalization <https://scikit-image.org/docs/0.19.x/api/skimage.exposure.html#skimage.exposure.equalize_adapthist>`_ from skimage
- Rescale Intensity operation
    - Uses the `Rescale Intensity <https://scikit-image.org/docs/0.19.x/api/skimage.exposure.html#skimage.exposure.rescale_intensity>`_ from skimage

Mask Options
-------------
- `MultiOtsu Mask <https://scikit-image.org/docs/0.19.x/api/skimage.filters.html#skimage.filters.threshold_multiotsu>`_
- `Otsu Mask <https://scikit-image.org/docs/0.19.x/api/skimage.filters.html#skimage.filters.threshold_otsu>`_
- `Yen Mask <https://scikit-image.org/docs/0.19.x/api/skimage.filters.html#skimage.filters.threshold_yen>`_
- `Li Mask <https://scikit-image.org/docs/0.19.x/api/skimage.filters.html#skimage.filters.threshold_li>`_

Morphology Options
-------------------
- Default Morphology
    - Includes binary dilation and the closing. Used in the default analysis process
- `Binary Closing Morphology <https://scikit-image.org/docs/0.19.x/api/skimage.morphology.html#skimage.morphology.binary_closing>`_
- `Binary Opening Morphology <https://scikit-image.org/docs/0.19.x/api/skimage.morphology.html#skimage.morphology.binary_opening>`_
- `Binary Dilation Morphology <https://scikit-image.org/docs/0.19.x/api/skimage.morphology.html#skimage.morphology.binary_dilation>`_
- `Binary Erosion Morphology <https://scikit-image.org/docs/0.19.x/api/skimage.morphology.html#skimage.morphology.binary_erosion>`_
- `Get Labels <https://scikit-image.org/docs/0.19.x/api/skimage.measure.html#skimage.measure.label>`_ 
    - Obtain the labels after the morphology to get your ROIs

Undo/Redo
-----------
 .. note:: 
     Previous image can only go back once.

- Use Previous Image (will use the previously created image prior to the most recent action)
- Use Most Recent Image (this will return you to the current image if you clicked previous image)
- Use Original Image (reset to the originally loaded in image)
- Use Previous Mask (will use the previously created mask prior to the most recent action)
- Use Most Recent Image (this will return you to the current mask if you clicked previous mask)

This information can also be found in the "Help" section of the application.