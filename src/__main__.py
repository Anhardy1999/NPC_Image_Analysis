# -------------------------------- Tkinter imports --------------------------------
from msilib.schema import ListBox
from pathlib import Path

from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, scrolledtext, simpledialog
from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk


# --------------------------------- Image analysis Imports --------------------------------
import napari
from numpy import spacing 
import pandas as pd 
from skimage import measure
import skimage.io as skio
import matplotlib.pyplot as plt 
import os

from logging import raiseExceptions
import os
import napari 
import numpy as np
import pandas as pd 
import imageio as io
from skimage import filters, morphology, measure, exposure, segmentation, restoration, feature, util
import skimage.io as skio
from scipy import ndimage as ndi

class Image_Processing():
    '''
    A class that will perform image processing operations.

    ...

    Attributes
    ----------
    image: ndarray
        an image to be processed
    skeleton: ndarray
        the skeleton of the image to be processed
    spacing: float
        the z spacing of the image
    viewer: napari.viewer
        the viewer to be used to view the image layers in 3D

    Methods
    -------
    skeleton_dilation(dilation=10)
        Dilates the skeleton of the image as many times as you indicate. 
        Crops the image to only the region of interest
    get_cropped()
        returns the cropped image
    median_filter(image, cube_width)
        Performs the median filter operation from skimage on the image passed. 
        Uses the cube width provided.
    background_subtract(image, gauss_sigma)
        Subtracts the background from the passed in image. Uses the gaussian 
        filter from skimage on the image passed in.
    sobel(image)
        Performs the sobel transformation on the passed in image using the sobel 
        filter from skimage
    ahe_contrast(image)
        Performs the adaptive histogram equalization on the passed in image using 
        the equalize_adapthist from skimage. Multiplies the image to the image 
        passed in to improve the contrast
    rescaled_intensity(image, vmin, vmax)
        Performs the rescale intensity operation on the passed in image using the 
        operation from skimage
    multiotsu_mask(image, classes)
        Performs the multiotsu mask operation using threshold_multiots from skimage 
        using the number of classes specified
    otsu_mask(image)
        Performs the otsu mask operation using threshold_otsu from skimage
    li_mask(image)
        Performs the li mask operation using threshold_li from skimage
    yen_mask(image)
        Performs the yen mask operation using threshold_yen from skimage
    default_morphology(image)
        Uses a default morphology operation consisting of closing and dilation 
        morphological operations.
    closing(image)
        Performs the closing operation on the provided mask 
    opening(image)
        Performs the opening operation on the provided mask 
    dilation(image)
        Performs the dilation operation on the provided mask 
    erosion(image)
        Performs the erosion operation on the provided mask 
    labels(image)
        Generates labels based on the mask created
    region_props(labels, intensity_image, properties)
        Generates the region properties from the labels depending on the properties 
        selected
    '''

    def __init__(self, image, skeleton, spacing, viewer):
        '''
        Parameters
        ----------
        image : ndarray
            The image to use for analysis
        skeleton : ndarray
            The binary image used to identify the area of interest of the image
        spacing : float
            The z spacing of the images being passed
        viewer : napari viewer
            The viewer to use for visualization of the images
        '''

        self.image = image
        self.skeleton = skeleton
        self.spacing = spacing
        self.viewer = viewer
        self.ROI = None
        self.median_skel = None
        self.final_contrast = None
        self.altered_image = self.image
        self.mask = None
        self.mask_morph = self.mask  

    def skeleton_dilation(self, dilation=10):
        ''' Dilates the skeleton provide.
        
        If the argument `dilation` isn't passed in, the default
        dilation value is used. Crops the image to be analyzed 
        to keep the image size small.

        Parameters
        ----------
        dilation : int, optional
            The amount of dilation applied to the skeleton
            (default is 10)
        
        Returns
        -------
        ROI
            An array for the cropped image with the dimensions of the skeleton         
        cropped_skeleton
            An array for the cropped skeleton with the size of the skeleton
        '''
        try:
            skel = self.skeleton
            for i in range(0,dilation):
                skel = morphology.dilation(skel)
                i+=1
                
            self.median_skel = filters.median(skel)
            p, x, y = np.where(self.median_skel)
            p1 = min(p)
            p2 = max(p)
            row1 = min(x)
            row2 = max(x)
            col1 = min(y)
            col2 = max(y)
            self.ROI = self.image[p1:p2, row1:row2, col1:col2]
            self.cropped_skel = self.median_skel[p1:p2, row1:row2, col1:col2]
            return self.ROI, self.cropped_skel
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

        
    def get_cropped(self):
        ''' Returns the cropped image used in the analysis. '''
        try:
            return self.ROI
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')


# -------------------- Processing Operations

    def median_filter(self,image = None, cube_width = 3):
        '''Performs the median filter operation from skimage 
        on the image passed.
        
        If the argument `cube_width` isn't provided, the default 
        value of 3 is passed.
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to
        cube_width : int, optional
            The width of the cube used as the footprint for the 
            filter (default is 3)

        Returns
        -------
        median
            The image after the median filter has been applied
        '''
        try:
            footprint = morphology.cube(cube_width)
            self.median = filters.median(image, selem = footprint)
            self.median = util.img_as_float(self.median)
            return self.median
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')


    def background_subtract(self,image = None, gauss_sigma = 7):
        '''Subtracts the background from the image provided
        
        If the argument `gauss_sigma` isn't provided, the default 
        value of 7 is passed.
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to
        gauss_sigma : int, optional
            The sigma used for the gaussian operation (default is 7)

        Returns
        -------
        subtract
            The image with the same shape as the input image after the 
            subtraction has been applied
        '''
        try:
            background = filters.gaussian(image, gauss_sigma)
            self.subtract = image - background
            return self.subtract
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')


    def sobel(self, image = None, mask = None):
        '''Performs the sobel transformation on a given image
        
        If the argument `mask` isn't provided, the mask will
        not be used.
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to
        mask : ndarray, optional
            mask to isolate the sobel filter to (default is None)

        Returns
        -------
        sobel
            The image of same shape as the input after the sobel filter 
            has been applied
        '''
        try:
            sobel = filters.sobel(image = image , mask = mask)
            return sobel
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')


# -------------------- Contrast Options


    def ahe_contrast(self, image = None):
        '''Performs the adaptive histogram equalization operation
        and multiplies the provided image and the AHE image
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to

        Returns
        -------
        final_contrast
            An ndarray of of the same size as the input after the AHE and multiplication 
            operations have been applied
        '''

        try:
            AHE = exposure.equalize_adapthist(image)
            self.final_contrast = AHE * image
            return self.final_contrast
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')
    

    def rescaled_intensity(self, image = None, vmin = .5, vmax = 99.5):
        ''' Rescales the intensity of the image using the intensities provided 
        
        If the arguments `vmin` and `vmax` aren't provided, the default 
        values of 0 and 255 are passed.
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to
        vmin : int, optional
            The minimum intensity value allowed for the image (default is 0)
        vmax : int, optional
            The maximum intensity value allowed for the image (default is 255)

        Returns
        -------
        final_contrast
            An ndarray of of the same size as the input after the rescaled intensity 
            operation has been applied
        '''
        
        try:
            vmin, vmax = np.percentile(image, q = (vmin, vmax))
            self.final_contrast = exposure.rescale_intensity(image, in_range = (vmin, vmax))

            return self.final_contrast
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')


# -------------------- Mask Operations


    def multiotsu_mask(self, image = None, classes = 2):
        '''Performs the multiotsu mask operation from skimage
        
        If the argument `classes` isn't provided, the default 
        value of 2 is passed.
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to
        classes : int, optional
            The number of classes in the image (default is 2)

        Returns
        -------
        mask_morph
            an array with the same shaqpe as the input after the 
            mask has been applied
        '''

        try:
            thresh = filters.threshold_multiotsu(image = image, classes = classes)
            self.mask = image >= thresh
            self.mask_morph = self.mask
            self.mask_morph = np.where(self.cropped_skel, self.mask, 0)
            
            return self.mask_morph

        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

    def otsu_mask(self, image = None):
        '''Performs the otsu mask operation from skimage
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to

        Returns
        -------
        mask_morph
            an array with the same shaqpe as the input after the 
            mask has been applied
        '''

        try:
            thresh = filters.threshold_otsu(image = image)
            self.mask = image >= thresh
            self.mask_morph = self.mask
            self.mask_morph = np.where(self.cropped_skel, self.mask, 0)
            return self.mask_morph

        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

    def li_mask(self, image = None):
        '''Performs the li mask operation from skimage
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to

        Returns
        -------
        mask_morph
            an array with the same shaqpe as the input after the 
            mask has been applied
        '''

        try:
            thresh = filters.threshold_li(image = image)
            self.mask = image >= thresh
            self.mask_morph = self.mask
            self.mask_morph = np.where(self.cropped_skel, self.mask, 0)
            return self.mask_morph
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

    def yen_mask(self, image = None):
        '''Performs the yen mask operation
        
        Parameters 
        ----------
        image : ndarray
            The image to apply the operation to

        Returns
        -------
        mask_morph
            an array with the same shaqpe as the input after the 
            mask has been applied
        '''

        try:
            thresh = filters.threshold_yen(image = image)
            self.mask = image >= thresh
            self.mask_morph = self.mask
            self.mask_morph = np.where(self.cropped_skel, self.mask, 0)
            return self.mask_morph
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

# -------------------- Morphology Operations

    def default_morphology(self):
        '''Performs the default morphology operations: Binary Dilation and Binary Closing
        from skimage

        Returns
        -------
        mask_closing
            an array of the same shape as the input image. The final mask 
            after the morphology operations are performed
        final_mask
            an array of the same shape as the input image. The final mask 
            isolated only to the area within the skeleton
        '''

        try:
            mask_dilate = morphology.binary_dilation(self.mask)
            mask_closing = morphology.binary_closing(mask_dilate)
            self.final_mask = np.where(self.cropped_skel, mask_closing, 0)
            self.mask_morph = self.final_mask

            return mask_closing, self.final_mask

        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

    def closing(self, mask = None):
        '''Performs the closing morphology operation from skimage

        Parameters
        ----------
        mask : ndarray
            The mask to perform the morph operation on

        Returns
        -------
        mask_morph
            The final mask of type ndarray after the morphology operation is performed
        '''
        try:
            self.mask_morph = morphology.binary_closing(mask)
            return self.mask_morph
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

    def opening(self, mask = None):
        '''Performs the opening morphology operation from skimage

        Parameters
        ----------
        mask : ndarray
            The mask to perform the morph operation on

        Returns
        -------
        mask_morph
            The final mask of type ndarray after the morphology operation is performed
        '''
        try:
            self.mask_morph = morphology.binary_opening(mask)
            return self.mask_morph
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

    def dilation(self, mask = None):
        '''Performs the dilation morphology operation from skimage

        Parameters
        ----------
        mask : ndarray
            The mask to perform the morph operation on

        Returns
        -------
        mask_morph
            The final mask of type ndarray after the morphology operation is performed
        '''

        try:
            self.mask_morph = morphology.binary_dilation(mask)
            return self.mask_morph
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

    def erosion(self, mask = None):
        '''Performs the erosion morphology operation from skimage

        Parameters
        ----------
        mask : ndarray
            The mask to perform the morph operation on

        Returns
        -------
        mask_morph
            The final mask of type ndarray after the morphology operation is performed
        '''
        try:
            self.mask_morph = morphology.binary_erosion(mask)
            return self.mask_morph
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')
    

# -------------------- Label Operations

    def labels(self, mask = None):
        '''Generates labels based on the provided mask

        Parameters
        ----------
        mask : ndarray
            The mask to perform the morph operation on

        Returns
        -------
        boundaries
            an array of the same shape as the input

        label_image
            an array with labels of the same shape as the input. All
            connected areas are under one label
        '''

        try:
            label_image = measure.label(mask)
            boundaries = segmentation.find_boundaries(label_image)
            return boundaries, label_image

        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

 

    def region_props(self, labels, intensity_image, properties):
        '''Generates a dictionary of properties requested for the labels
        provided

        Parameters
        ----------
        labels : ndarray
            The labeled image to generate the properties for
        intensity_image : ndarray
            The image to reference intensity values for
        properties : list
            A list of strings with the properties desired 

        Returns
        -------
        props
            a dictionary with the properties generated for each label
        '''
        
        try:
            props = measure.regionprops_table(labels, intensity_image, properties)
            return props
        except TypeError as e:
            print(f'This is not a valid type. Expected ndarray, but got {e}')

class ImageSeg_App():
    ''' A class used to create the Image Segmentation App
    
    ...

    Attributes
    ----------
    master : TK()  
        TK toplevel object to initialize the application

    Methods
    -------
    credits()
        Prints the credits for this application on the status screen
    help_info()
        Prints help information for this application based on the user's choice
    read_files()
        Allows the user to select the images needed for analysis
    bttn(window, text, bcolor, fcolor, command)
        window : top level object
        text : str
        bcolor : str
        fcolor : str
        command : method
        Creates the buttons for the custom analysis window
    default_analysis()
        Performs the default analysis operations for the images provided. 
    custom_analysis()
        Allows the user to customize the analysis for their images
    analyze()
        Creates the window for the user to choose their analysis option.
    recent_image()
        Allows the user to access the most recently created image.
    previous_image()
        Allows the user to access the image created prior to the most recent one
    original_image()
        Allows the user to access the original image essentially resetting their analysis.
    recent_mask()
        Allows the user to access the most recently created mask
    previous_mask()
        Allows the user to access the mask created prior to the most recent mask
    skeleton_dilate()
        Allows the user to dilate the skeleton mask loaded in to isolate their region of interest
    median_image()
        Allows the user to perform a median filter operation through the customization window
    background_subtract()
        Allows the user to perform a background subtract operation through the customization window
    sobel_image()
        Allows the user to perform a sobel filter operation through the customization window
    ahe()
        Allows the user to perform an adaptive histogram equalization operation through the customization window
    rescale_intensity()
        Allows the user to perform a rescaled intensity operation through the customization window
    multiotsu()
        Allows the user to perform a multiotsue mask operation through the customization window
    otsu()
        Allows the user to perform an otsu mask operation through the customization window
    yen()
        Allows the user to perform a yen mask operation through the customization window
    li()
        Allows the user to perform a li mask operation through the customization window
    defaul_morph()
        Allows the user to use the default morphology operations used in the default analysis
    closing_morph()
        Allows the user to use the closing morphology operation through the customization window
    opening_morph()
        Allows the user to use the opening morphology operation through the customization window
    dilation_morph()
        Allows the user to use the dilation morphology operation through the customization window
    erosion_morph()
        Allows the user to use the erosion morphology operation through the customization window
    properties_table()
        Creates the table with properties from the analysis as selected by the user
    props()
        Allows the user to select what properties they would like to include in their analysis 
    export()
        Exports the properties table as an excel file
    '''

    def __init__(self, master):
        self.master = master
        self.master.title('NPC Image Analysis')
        self.filetypes = [
            ('csv files', '*.csv'),
            ('All files', '*.*')
            ]
        self.help_txt = 'Help.txt' 
        self.default_txt = 'Default_Analysis_Info.txt' 
        self.custom_txt = 'Custom.txt' 
        self.skeleton = None
        self.main_image = None
        self.skeleton_path = None
        self.main_image_path = None
        self.ROI = None
        self.analysis_complete = False
        self.properties = ['label', 'area', 'bbox', 'bbox_area', 'intensity_mean', 
        'equivalent_diameter_area', 'axis_minor_length', 'axis_major_length', 'centroid']
        self.prev_image = self.main_image
        self.recent_image = self.main_image
        self.current_image = self.main_image
        self.default = None
        self.custom_processing = None
        self.multiotsuMask = None
        self.otsuMask = None
        self.liMask = None
        self.yenMask = None
        self.current_mask = None


        self.master.resizable(False, False)
        self.master.geometry("692x669")
        self.master.configure(bg = "#FFFFFF")
        self.frame_header = ttk.Frame(self.master)
        self.frame_header.pack()



        self.canvas = Canvas(
            self.master,
            bg = "#FFFFFF",
            height = 669,
            width = 692,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.pack()
        self.canvas.create_rectangle(
            0.0,
            0.0,
            800.0,
            669.0,
            fill="#212024",
            outline="")


        # status text box
        self.canvas.create_rectangle(
            18.0,
            38.0,
            675.0,
            345.0,
            fill="#C6C7D6",
            outline="")

        self.canvas.create_text(
            320.0,
            15.0,
            anchor="nw",
            text="Status",
            fill="#C7C7D7",
            font=("Roboto", 18 * -1)
        )

        self.frame_status = ttk.Frame(self.master,
        height = 307,
        width = 657
        )
        self.frame_status.place(x = 15, y = 38)
        self.text = scrolledtext.ScrolledText(self.frame_status, bg = '#C7C7D7', fg = '#2B0A54',
        height = 17, width = 80, wrap = tk.WORD, undo = True)
        self.text.yview_pickplace("end")
        self.text['font'] = ('Roboto','11')
        self.text.pack(side = BOTTOM, fill = BOTH)
        
        

        # buttons rectangle
        self.canvas.create_rectangle(
            150.0,
            360.0,
            540.0,
            645.0,
            fill="#C7C7D7",
            width = 3,
            outline="#000000")

# -------------------- Buttons

        def bttn_app(x, y, width, height, text, command):
            ''' Creates the buttons for the custom analysis. '''
            fcolor = "#2B0A54"
            bcolor = "#C7C7D7"


            def __on_enter(e):
                mybutton['background'] = bcolor
                mybutton['foreground'] = fcolor

            def __on_leave(e):
                mybutton['background'] = fcolor
                mybutton['foreground'] = bcolor

            mybutton = Button(text = text,  
            fg = bcolor,
            bg = fcolor,
            bd = 2,
            activeforeground = fcolor,
            activebackground = bcolor,
            command = command)
            mybutton['font'] = ('Roboto', 12)

            mybutton.bind("<Enter>", __on_enter)
            mybutton.bind("<Leave>", __on_leave)

            mybutton.place( x = x, y = y, width = width, height = height)


        bttn_app(
            x=193.0,
            y=408.0,
            width=148.0,
            height=54.0,
            text = 'Load Images',
            command = lambda: self.read_files()
        )

        bttn_app(
            x= 193.0,
            y= 483.0,
            width=148.0,
            height=54.0,
            text = "Perform Analysis",
            command = lambda: self.analyze(),
        )

        bttn_app(
            x=351.0,
            y=408.0,
            width=148.0,
            height=54.0,
            text = "Get ROI\nProperties", 
            command = lambda: self.props()
        )

        bttn_app(
            x= 351.0,
            y= 483.0,
            width=148.0,
            height=54.0,
            text = "Help",
            command = lambda: self.help_info()
        )

        bttn_app(
            x= 267.0,
            y= 556.0,
            width=148.0,
            height=54.0,
            text = "Credits",
            command = lambda: self.credits()
        )

   # -------------------- Backend Functions --------------------
        self.help_txt = '''
        
        GETTING STARTED

        This software is intended to be modifiable in order to answer particular needs to identify organelles and structures.
        Using this software, you will be able to look within the radial process of a specific cell of interest. This is used in conjuction with ImageJ's Simple Neurite Tracer.

        To use this software, you will need... 
            - A greyscale tiff image that contains the channel for the organelles or structures of interest you would like analyzed
            - The skeleton file created from the simple neurite tracer as a .tiff file. You cannot use the .trace file for this as it cannot be read in.

        After you load in your images using the "Load Images" button, you can selected "Perform Analysis".
        You will be provided with two options, "Default Analysis" and "Custom Analysis". If you would like to just see what a default analysis would look like, selected Default Analysis.

        This will ask for the "z" spacing of your images. This only effects the presentation of your images not the analysis. From there, depending on the size of the image, it can take a while for the analysis to complete. If it looks temporarily frozen, that's possibly why.
        You can find more information about the Default Analysis option and what operations are performed, selected the Default Analysis under the help window.

        You can see examples of this file being used in the ReadtheDocs page:
        https://npc-image-analysis.readthedocs.io/en/latest/Examples.html
        ''' 
        

        self.default_txt = '''
        
        DEFAULT ANALYSIS

        The default analysis operation performs the following functions:
            - Skeleton Dilation (Default Dilation is 10)
            - Cropping of the image to the length/size/volume of the skeleton
            - Median filter with a cube width of 3
            - Background subtraction using a gaussion blur of strength 7.
            - Adaptive Histogram Equalization: This consists of using scikit image's adaptive histogram equalization option. It is then multipled to the background subtracted image to give the final contrast.
            - Multiotsu mask at 2 classes (there are presumed only 2 classes, background and regions of interest)
            - Default morphology: Dilation morphology and then closing morphology
            - Labels are added to the image.
        ''' 

        self.custom_txt = '''
        
        CUSTOM ANALYSIS OPTIONS:

        - Skeleton Dilation 
        - Median Filter
        - Background Subtraction
        - Sobel Filter
        - Adaptive Histogram Equalization: This consists of using scikit image's adaptive histogram equalization option. It is then multipled to the background subtracted image to give the final contrast.
        - Rescale Intensity

        MASK OPTIONS

        - MultiOtsu Mask
        - Otsu Mask
        - Yen Mask
        - Li Mask

        MORPHOLOGY OPTIONS

        - Default Morphology (includes dilation and the closing. Used in the default analysis process)
        - Closing Morphology
        - Opening Morphology
        - Dilation Morphology
        - Erosion Morphology
        - Get Labels: Obtain the labels after the morpholgoy to get your ROIs

        UNDO/REDO
        * Previous image can only go back once.

        - Use Previous Image (will use the previously created image prior to the most recent action)
        - Use Most Recent Image (this will return you to the current image if you clicked previous image)
        - Use Original Image (reset to the originally loaded in image)
        - Use Previous Mask (will use the previously created mask prior to the most recent action)
        - Use Most Recent Image (this will return you to the current mask if you clicked previous mask)
        ''' 



    def credits(self):
        ''' Returns the credits for this program. '''

        self.text.config(state = "normal")
        self.text.insert(tk.END, " You can find the source code and information on the program on the Github: https://github.com/Anhardy1999/NPC_Image_Analysis \n\n")
        self.text.config(state = "disabled")

    def help_info(self):
        ''' Provides some help information about how to use the program.'''

        def getting_started():
            self.text.config(state='normal')   

            self.text.insert(tk.END, self.help_txt)

            self.text.config(state = 'disabled')
        
        def reading_default():
            self.text.config(state='normal')   

            self.text.insert(tk.END, self.default_txt)

            self.text.config(state = 'disabled')

        def reading_custom():
            self.text.config(state='normal')   

            self.text.insert(tk.END, self.custom_txt)

            self.text.config(state = 'disabled')


        def option_changed(choice):
            choice = self.option_var.get()

            if choice ==  "Getting Started":
                getting_started()

            elif choice == "Default Analysis":
                reading_default()

            elif choice == "Custom Analysis":
                reading_custom()


        self.top_option = Toplevel(self.master)
        self.top_option.configure(bg = "#212024")
        self.top_option.title("Analysis Options")

        self.help_options = ["Getting Started", "Default Analysis", "Custom Analysis"]
        self.option_var = tk.StringVar(self.top_option)

        paddings = {'padx':5, "pady": 5}
        label = ttk.Label(self.top_option, text = 'What would you like information on?')
        label.grid(column = 0, row = 0, sticky = tk.W, **paddings)

        option_menu = ttk.OptionMenu(
            self.top_option, 
            self.option_var,
            "              ",
            *self.help_options,
            command= option_changed
        )
        option_menu.grid(column = 1, row = 0, sticky = tk.W, **paddings)

        self.output_label = ttk.Label(self.top_option, background = "#212024", foreground = "white")
        self.output_label.grid(column = 0, row = 1, sticky = tk.W, **paddings)

    def read_files(self):
        ''' Loads the images in to perform analysis on. '''

        if self.main_image_path and self.skeleton_path is not None: 
            correct_files = messagebox.askyesno(title = 'Load new images', 
            message = 'There are other images loaded. Would you like to load other images instead?')
            if correct_files == True:
                self.text.config(state='normal')
                self.text.insert(tk.END, 'Please make sure that you are importing the skeleton file first and then the main fluorescence image.\n')
                self.text.config(state='disabled')

                self.skeleton_path = fd.askopenfilename(
                    title= 'Open a skeleton file.',
                    initialdir= '/',
                    filetypes = [
                        ('tiff', '*.tiff'),
                        ('tif', '*.tif'),
                        ('All files', '*.*')
                    ])

                self.main_image_path = fd.askopenfilename(
                    title= 'Open a main fluorescence image',
                    initialdir= '/',
                    filetypes = [
                        ('tiff', '*.tiff'),
                        ('tif', '*.tif'),
                        ('All files', '*.*')
                    ])

                self.text.config(state='normal')
                self.text.insert(tk.END, 'Imported folder.\n\n')
                self.text.insert(tk.END, 'Files imported are:\n')
                self.text.insert(tk.END, 'Skeleton file: ' + os.path.split(self.skeleton_path)[-1] + '\n')
                self.text.insert(tk.END, 'Main image file: ' + os.path.split(self.main_image_path)[-1] + '\n')
                self.text.insert(tk.END, 'Please verify that these are the correct files.\n')
                self.text.config(state='disabled')
                correct_files = messagebox.askyesno(title = 'File check', message = 'Please verify that these are the correct files.')
                if correct_files == True:
                    self.text.insert(tk.END, 'Files verified. Please select an analysis method.\n')
                    self.text.config(state='disabled')     
                    self.skeleton = skio.imread(self.skeleton_path, plugin='tifffile')   
                    self.main_image = skio.imread(self.main_image_path, plugin='tifffile')   
                else:
                    self.text.insert(tk.END, 'No files loaded. Please select new files.\n')
                    self.text.config(state='disabled')      
                    self.skeleton = None 
                    self.main_image = None 
        
        else:
            self.text.config(state='normal')
            self.text.insert(tk.END, 'Please make sure that you are importing the skeleton file first and then the main fluorescence image.\n')
            self.text.config(state='disabled')

            self.skeleton_path = fd.askopenfilename(
                title= 'Open a skeleton file.',
                initialdir= '/',
                filetypes = [
                    ('tiff', '*.tiff'),
                    ('tif', '*.tif'),
                    ('All files', '*.*')
                ])
            if self.skeleton_path == False:
                self.text.config(state='normal')
                self.text.insert(tk.END, 'Please load the skeleton file.\n\n')
                self.text.config(state='disabled')
                return

            self.main_image_path = fd.askopenfilename(
                title= 'Open a main fluorescence image',
                initialdir= '/',
                filetypes = [
                    ('tiff', '*.tiff'),
                    ('tif', '*.tif'),
                    ('All files', '*.*')
                ])

            self.text.config(state='normal')
            self.text.insert(tk.END, '\nImported files.\n\n')
            self.text.insert(tk.END, 'Files imported are:\n')
            self.text.insert(tk.END, 'Skeleton file: ' + os.path.split(self.skeleton_path)[-1] + '\n')
            self.text.insert(tk.END, 'Main image file: ' + os.path.split(self.main_image_path)[-1] + '\n')
            self.text.insert(tk.END, 'Please verify that these are the correct files.\n')
            self.text.config(state='disabled')
            correct_files = messagebox.askyesno(title = 'File check', message = 'Please verify that these are the correct files.\n\n')
            if correct_files == True:
                self.text.insert(tk.END, 'Files verified. Please select an analysis method.\n')
                self.text.config(state='disabled')         
                self.skeleton = skio.imread(self.skeleton_path, plugin='tifffile')   
                self.main_image = skio.imread(self.main_image_path, plugin='tifffile')    
                self.analysis_complete = False  
            else:
                self.text.insert(tk.END, 'No files loaded. Please select new files.\n')
                self.text.config(state='disabled')      
                self.skeleton = None 
                self.main_image = None 
    
# --------------------- Analysis Functions --------------------
    def bttn(self, window, text, bcolor, fcolor, command):
        ''' Creates the buttons for the custom analysis. '''

        def __on_enter(e):
            mybutton['background'] = bcolor
            mybutton['foreground'] = fcolor

        def __on_leave(e):
            mybutton['background'] = fcolor
            mybutton['foreground'] = bcolor

        mybutton = Button(window, width = 20, height = 2, text = text, 
        fg = bcolor,
        bg = fcolor,
        bd = 2,
        activeforeground = fcolor,
        activebackground = bcolor,
        command = command)

        mybutton.bind("<Enter>", __on_enter)
        mybutton.bind("<Leave>", __on_leave)

        mybutton.pack()

    def default_analysis(self):
        ''' Default analysis operation for loaded image. 

        Will initialize the image analysis function with the default 
        parameters without any customization. Creates a napari viewer
        used only for the default analysis.

        '''

        if self.main_image is not None:
            if self.custom_processing is not None:
                self.custom_processing = None
            self.text.config(state='normal')   
            self.text.insert(tk.END, 'Analyzing ' + os.path.split(self.main_image_path)[-1] + '\n')
            self.text.config(state='disabled')  
            spacing = simpledialog.askfloat('Spacing', 'What is the image spacing?')
            if spacing is None:
                return
            else:
                viewer = napari.Viewer(ndisplay = 3) 

                self.default = Image_Processing(image = self.main_image, skeleton = self.skeleton, 
                spacing = spacing, viewer = viewer)

                self.ROI, cropped_skel = self.default.skeleton_dilation()
                viewer.add_image(data = self.ROI, name = "ROI")
                viewer.add_image(data = cropped_skel, name = "Skeleton")
                median_image = self.default.median_filter(self.ROI)
                viewer.add_image(data = median_image, name = "Median")
                subtract_image = self.default.background_subtract(median_image)
                viewer.add_image(data = subtract_image, name = "Subtract")
                ahe_contrast = self.default.ahe_contrast(subtract_image)
                viewer.add_image(data = ahe_contrast, name = "AHE")
                multiotsu_mask = self.default.multiotsu_mask(ahe_contrast)
                viewer.add_image(data = multiotsu_mask, name = "Multiotsu Mask")
                mask_closing, final_mask = self.default.default_morphology()
                viewer.add_image(data = mask_closing, name = "Mask") 
                viewer.add_image(data = final_mask, name = "Final Mask")
                self.current_mask = final_mask
                self.boundaries, self.labeled_image = self.default.labels(self.current_mask)
                viewer.add_image(data = self.labeled_image, name = "Labels")

                self.analysis_complete = True
        else:
            self.text.config(state='normal')   
            self.text.insert(tk.END, "Please load in an image file first.\n")
            self.text.config(state='disabled')  

    def custom_analysis(self):
        ''' Function for the user to customize their analysis process. 
        
        This contains all of the possible analysis options available to the user. 
        This initializes a different napari viewer from the default analysis, and 
        will stop the default analysis viewer from continued use if one was created 
        prior to this. 
        '''

        if self.main_image is not None:
            self.top.geometry("485x550")

            frame_2 = Frame(self.top, height = 100, width= 100, bg = "#212024")
            frame_2.grid(row = 1, column = 0, ipadx= 5, ipady= 5)
            self.current_image = self.main_image
            self.prev_image = self.main_image

            self.bttn(frame_2, "Skeleton Dilation", "#141414", "#C6C7D6", command = lambda: self.skeleton_dilate())
            self.bttn(frame_2, "Median Filter", "#141414", "#C6C7D6",  command = lambda: self.median_image())
            self.bttn(frame_2, "Background Subtraction", "#141414", "#C6C7D6", command = lambda: self.background_subtract())
            self.bttn(frame_2, "Sobel Filter", "#141414", "#C6C7D6", command = lambda: self.sobel_image())
            self.bttn(frame_2, "Adaptive Histogram \nEqualization", "#141414", "#C6C7D6", command = lambda: self.ahe())
            self.bttn(frame_2, "Rescale Intensity", "#141414", "#C6C7D6", command = lambda: self.rescale_intensity())

            frame_3 = Frame(self.top, height = 100, width = 100, bg = "#212024")
            frame_3.grid(row = 0, column = 2,ipadx= 5, ipady= 5)
            self.bttn(frame_3, "Use previous image", "#141414", "#C6C7D6", command = lambda: self.previous_image())
            self.bttn(frame_3, "Use the most recent image", "#141414", "#C6C7D6", command = lambda: self.recent_image())
            self.bttn(frame_3, "Use original image", "#141414", "#C6C7D6", command = lambda: self.original_image())
            self.bttn(frame_3, "Use previous mask", "#141414", "#C6C7D6", command = lambda: self.previous_mask())
            self.bttn(frame_3, "Use the most recent mask", "#141414", "#C6C7D6", command = lambda: self.recent_mask())

            frame_4 = Frame(self.top, height = 100, width = 100, bg = "#212024")
            frame_4.grid(row = 0, column = 3,ipadx= 5, ipady= 5)
            self.bttn(frame_4, "MultiOtsu Mask", "#141414", "#C6C7D6", command = lambda: self.multiotsu())
            self.bttn(frame_4, "Otsu Mask", "#141414", "#C6C7D6", command = lambda: self.otsu())
            self.bttn(frame_4, "Yen Mask", "#141414", "#C6C7D6", command = lambda: self.yen())
            self.bttn(frame_4, "Li Mask", "#141414", "#C6C7D6", command = lambda: self.li())

            frame_5 = Frame(self.top, height = 100, width = 100, bg = "#212024")
            frame_5.grid(row = 1, column = 3,ipadx= 5, ipady= 5)
            self.bttn(frame_5, "Default Morphology", "#141414", "#C6C7D6", command = lambda: self.default_morph())
            self.bttn(frame_5, "Closing Morphology", "#141414", "#C6C7D6", command = lambda: self.closing_morph())
            self.bttn(frame_5, "Opening Morphology", "#141414", "#C6C7D6", command = lambda: self.opening_morph())
            self.bttn(frame_5, "Dilation Morphology", "#141414", "#C6C7D6", command = lambda: self.dilation_morph())
            self.bttn(frame_5, "Erosion Morphology", "#141414", "#C6C7D6", command = lambda: self.erosion_morph())
            self.bttn(frame_5, "Get Labels", "#141414", "#C6C7D6", command = lambda: self.label_image())

            spacing = simpledialog.askfloat('Spacing', 'What is the image spacing?')
            if spacing is None:
                return
            self.viewer = napari.Viewer(ndisplay = 3) 

            if self.default is not None:
                self.default = None

            self.custom_processing = Image_Processing(image = self.main_image, skeleton = self.skeleton, 
                spacing = spacing, viewer = self.viewer)
        
        else:
            self.text.config(state='normal')   
            self.text.insert(tk.END, "Please load in an image file first.\n")
            self.text.config(state='disabled')        

    def analyze(self):
        ''' Intialize the window for the user to choose their analysis option: Default or Custom '''

        if self.main_image is not None:
            self.top = Toplevel(self.master)
            self.top.geometry("160x300")
            self.top.configure(bg = "#212024")
            self.top.title("Analysis Options")

            frame_1 = Frame(self.top, bg = "#212024")
            frame_1.grid(row = 0, column = 0, ipadx= 5, ipady= 5)
            
            self.bttn(frame_1, "Default Analysis", "#141414", "#C6C7D6",  command = lambda: self.default_analysis())
            self.bttn(frame_1, "Custom Analysis", "#141414", "#C6C7D6",  command = lambda: self.custom_analysis())

           
        else:
            self.text.config(state='normal')   
            self.text.insert(tk.END, "Please load in an image file first.\n")
            self.text.config(state='disabled')  

    def recent_image(self):
        ''' Accesses the most recent image created. '''

        self.prev_image = self.current_image
        self.current_image = self.rec_image
        self.viewer.add_image(data = self.current_image, name = "recent image")
        self.text.config(state = "normal")
        self.text.insert(tk.END, "Most recent image restored")
        self.text.config(state = "disabled")

    def previous_image(self):
        ''' Accesses the image created prior to the most recent one '''

        self.rec_image  = self.current_image
        self.current_image = self.prev_image
        self.viewer.add_image(data = self.current_image, name = "previous image")
        self.text.config(state = "normal")
        self.text.insert(tk.END, "Previous image restored.")
        self.text.config(state = "disabled")


    def original_image(self):
        ''' Accesses the original image, esentially resetting the analysis '''

        self.prev_image = self.current_image
        self.current_image = self.main_image
        self.viewer.add_image(data = self.current_image, name = "original image")
        self.text.config(state = "normal")
        self.text.insert(tk.END, "Original image restored.")
        self.text.config(state = "disabled")

    def recent_mask(self):
        ''' Accesses the most recent mask created. '''

        self.prev_mask = self.current_mask
        self.current_mask = self.recent_mask
        self.viewer.add_image(data = self.current_mask, name = "recent mask")
        self.text.config(state = "normal")
        self.text.insert(tk.END, "Recent mask restored.")
        self.text.config(state = "disabled")

    def previous_mask(self):
        ''' Accesses the mask created prior to the most recent one '''

        self.recent_mask  = self.current_mask
        self.current_mask = self.prev_mask
        self.viewer.add_image(data = self.current_mask, name = "previous mask")
        self.text.config(state = "normal")
        self.text.insert(tk.END, "Previous mask restored.")
        self.text.config(state = "disabled")

# -------------------- Analysis Functions

    def skeleton_dilate(self):
        ''' Function to dilate the skeleton loaded in by the user to isolate to their region of interest. '''

        dilate = simpledialog.askinteger('Dilation', 'How much would you like to dilate the skeleton? Default is 10')
        
        try:
            self.ROI, cropped_skel = self.custom_processing.skeleton_dilation(dilate)
            self.prev_image = self.main_image
            self.current_image = self.ROI
            self.viewer.add_image(data = self.ROI, name = "ROI")
            self.viewer.add_image(data = cropped_skel, name = "Skeleton")

            self.text.config(state='normal')   
            self.text.insert(tk.END, f'Skeleton dilation performed with dilation {dilate}.\n')
            self.text.config(state='disabled') 

        except TypeError:
            return None 
          

    def median_image(self):
        ''' Function for the median filter button. Performs the median filter operation from scikit image. 
        
        Asks the user for the cube width value to use.
        The default value is 3.
        If the user does not provide a value, will simply cancel the operation.
        '''

        self.prev_image = self.current_image
        cube_width = simpledialog.askinteger('Cube Width', 'What width would you like to set the cube to (default 3)?')
        
        try:
            median_image = self.custom_processing.median_filter(self.prev_image, cube_width)
            self.viewer.add_image(data = median_image, name = "Median")
            self.current_image = median_image
            self.text.config(state='normal')   
            self.text.insert(tk.END, f'Median Filter performed with cube width {cube_width}.\n')
            self.text.config(state='disabled')    

        except TypeError:
            return

    def background_subtract(self):
        ''' Function for the background subtraction button. Subtracts the background from the image. 
        
        Asks the user for the gaussian sigma value to use.
        The default value is 7.
        If the user does not provide a value, will simply cancel the operation.
        '''

        self.prev_image = self.current_image
        gaussian_sigma = simpledialog.askfloat('Gaussian Sigma', 'How strong would you like the gaussian sigma to be? (Default = 7)', minvalue = 0.0, maxvalue = 100.0)
        
        try:
            background_subtract = self.custom_processing.background_subtract(self.prev_image, gaussian_sigma)
            self.viewer.add_image(data = background_subtract, name = "Background Subtracted image")
            self.current_image = background_subtract
            self.text.config(state='normal')   
            self.text.insert(tk.END, f'Background Subtraction performed with gaussian sigma {gaussian_sigma}.\n')
            self.text.config(state='disabled')   

        except TypeError:
            return

    def sobel_image(self):
        ''' Performs the sobel operation from scikit image. '''

        self.prev_image = self.current_image
        sobel_image = self.custom_processing.sobel(self.prev_image)
        self.viewer.add_image(data = sobel_image, name = "Sobel Image")
        self.current_image = sobel_image
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Sobel Filter performed.\n')
        self.text.config(state='disabled')   

    def ahe(self):
        ''' Performs the adaptive histogram equalization operation from scikit image. 
        
        In addition, this function will multiply the adaptive histogram equalization image
        will be multiplied to the previous image passed in to enhance the contrast. 
        '''

        self.prev_image = self.current_image
        ahe_image = self.custom_processing.ahe_contrast(self.prev_image)
        self.viewer.add_image(data = ahe_image, name = "Adaptive Histogram Equalization Contrast")
        self.current_image = ahe_image
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Adaptive Histogram Equalization Contrast performed.\n')
        self.text.config(state='disabled')   

    def rescale_intensity(self):
        ''' Performs the rescale intensity operation from scikit image. 
        
        Asks the user for the minimum and maximum intensity value to use.
        The default values are 0 (minimum) and 255 (maximum).
        If the user does not provide a value, will simply cancel the operation.
        '''

        self.prev_image = self.current_image

        try:
            vmin = simpledialog.askfloat('Minimum Intensity Value', 'This determines the minimum intensity values allowed for the image. Default value is .5.')
            vmax= simpledialog.askfloat('Maximum Intensity Value', 'This determines the maximum intensity values allowed for the image. Default value is 99.5.')            
            rescaled = self.custom_processing.rescaled_intensity(self.prev_image, vmin, vmax)
            self.viewer.add_image(data = rescaled, name = "Sigmoid Contrast")
            self.current_image = rescaled
            self.text.config(state='normal')   
            self.text.insert(tk.END, f'Sigmoid contrast performed with minimum intensity {vmin} and maximum intensity {vmax}.\n')
            self.text.config(state='disabled') 

        except TypeError:
            return 

# -------------------- Mask Functions

    def multiotsu(self):
        ''' MultiOtsu mask morphology operation. 
        
        Uses the current image and doesn't require any args.
        '''

        self.prev_mask = self.current_mask
        classes = simpledialog.askinteger("Classes", "How many classes are in the current image? Default is 2.")

        try:

            multiotsuMask = self.custom_processing.multiotsu_mask(self.current_image, classes)
            self.viewer.add_image(data = multiotsuMask, name = "Multiotsu Mask")
            self.multiotsuMask = multiotsuMask
            self.current_mask = self.multiotsuMask
            self.text.config(state='normal')   
            self.text.insert(tk.END, f'Multiotsu mask performed with class {classes}.\n')
            self.text.config(state='disabled')  
        
        except TypeError:
            return

    def otsu(self):
        ''' Otsu mask morphology operation. 
        
        Uses the current image and doesn't require any args.
        '''

        self.prev_mask = self.current_mask
        self.otsuMask = self.custom_processing.otsu_mask(self.current_image)
        self.current_mask = self.otsuMask
        self.viewer.add_image(data = self.current_mask, name = "Otsu Mask")
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Otsu mask performed.\n')
        self.text.config(state='disabled')  

    def yen(self):
        ''' Yen mask morphology operation. 
        
        Uses the current image and doesn't require any args.
        '''

        self.prev_mask = self.current_mask
        self.yenMask = self.custom_processing.yen_mask(self.current_image)
        self.current_mask = self.yenMask
        self.viewer.add_image(data = self.current_mask, name = "Yen Mask")
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Yen mask performed.\n')
        self.text.config(state='disabled')  

    def li(self):
        ''' Li mask morphology operation. 
        
        Uses the current image and doesn't require any args.
        '''
        self.prev_mask = self.current_mask
        self.liMask = self.custom_processing.li_mask(self.current_image)
        self.current_mask = self.liMask
        self.viewer.add_image(data = self.current_mask, name = "Li Mask")
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Li mask performed.\n')
        self.text.config(state='disabled')  


# -------------------- Morphology Functions

    def default_morph(self):
        ''' Performs the default morphology operation. 
        
        This operation consists of dilation and closing morphology steps.
        '''

        self.prev_mask = self.current_mask 
        self.mask_closing, self.current_mask = self.custom_processing.default_morphology()
        self.viewer.add_image(data = self.mask_closing, name = "Mask Closing") 
        self.viewer.add_image(data = self.current_mask, name = "Final Mask")
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Dilation and Closing morphology operations performed.\n')
        self.text.config(state='disabled')  

    def closing_morph(self):
        ''' Perfroms the closing morphology operation. '''

        self.prev_mask = self.current_mask
        self.current_mask = self.custom_processing.closing(self.prev_mask)
        self.viewer.add_image(data = self.current_mask, name = "Mask Closing") 
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Closing morphology performed.\n')
        self.text.config(state='disabled')  

    def opening_morph(self):
        ''' Performs the opening morphology operation. '''

        self.prev_mask = self.current_mask
        self.current_mask = self.custom_processing.opening(self.prev_mask)
        self.viewer.add_image(data = self.current_mask, name = "Mask Opening") 
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Opening morphology performed.\n')
        self.text.config(state='disabled')  

    def dilation_morph(self):
        ''' Performs the dilation morphology operation. '''

        self.prev_mask = self.current_mask
        self.current_mask = self.custom_processing.dilation(self.prev_mask)
        self.viewer.add_image(data = self.current_mask, name = "Mask Dilation")
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Dilation morphology performed.\n')
        self.text.config(state='disabled')   
    
    def erosion_morph(self):
        ''' Performs the erosion morphology operation. '''

        self.prev_mask = self.current_mask
        self.current_mask = self.custom_processing.erosion(self.prev_mask)
        self.viewer.add_image(data = self.current_mask, name = "Mask Erosion") 
        self.text.config(state='normal')   
        self.text.insert(tk.END, f'Erosion morphology performed.\n')
        self.text.config(state='disabled')  

# -------------------- Get Properties Functions 

    def properties_table(self):
        ''' Creates the table of properties for analysis. 

        This is created from the labels generated and based on the properties you selected.
        '''
        
        if self.analysis_complete == True:
            if self.default is not None:

                options = self.list_box.curselection()
                for i in options:
                    op = self.list_box.get(i)
                    self.selected_properties.append(op)

                self.properties = self.default.region_props(self.labeled_image, self.ROI, self.selected_properties)
                self.df = pd.DataFrame(self.properties)
                self.df.set_index("label")
                if self.main_image is not None:
                    self.top_2 = Toplevel(self.master)
                    self.top_2.geometry("500x400")
                    self.top_2.configure(bg = "#000000")
                    self.top_2.title("Properties Table")
                    frame_props = Frame(self.top_2)
                    frame_props.pack()
                    tree = ttk.Treeview(frame_props, height = '10') 

                    tree["column"] = list(self.df.columns)
                    tree["show"] = "headings"
                    for column in tree["columns"]:
                        tree.heading(column, text = column)

                    df_rows = self.df.to_numpy().tolist()
                    for row in df_rows:
                        tree.insert("", "end", values = row)

                    treescrolly = tk.Scrollbar(frame_props, orient="vertical", command = tree.yview)
                    treescrollx = tk.Scrollbar(frame_props, orient="horizontal", command = tree.xview)
                    tree.configure(yscrollcommand = treescrolly.set)
                    tree.configure(xscrollcommand = treescrollx.set)
                    treescrolly.pack(side = "right", fill = "y")
                    treescrollx.pack(side = "bottom", fill = "x")
                    tree.pack(side = "left")

                    ttk.Button(self.top_2, text = "Export ROI Properties", command = lambda: self.export()).pack(side = "top")


            elif self.custom_processing is not None: 

                options = self.list_box.curselection()
                for i in options:
                    op = self.list_box.get(i)
                    self.selected_properties.append(op)

                self.properties = self.custom_processing.region_props(self.labeled_image, self.ROI, self.selected_properties)
                self.df = pd.DataFrame(self.properties)
                self.df.set_index('label')
                if self.main_image is not None:
                    self.top_2 = Toplevel(self.master)
                    self.top_2.geometry("500x400")
                    self.top_2.configure(bg = "#000000")
                    self.top_2.title("Properties Table")
                    frame_props = Frame(self.top_2, bg = "#000000")
                    frame_props.pack()
                    tree = ttk.Treeview(frame_props, show = 'headings', height = '10')
                    


                    tree["column"] = list(self.df.columns)
                    tree["show"] = "headings"
                    for column in tree["columns"]:
                        tree.heading(column, text = column)

                    df_rows = self.df.to_numpy().tolist()
                    for row in df_rows:
                        tree.insert("", "end", values = row)

                    treescrolly = tk.Scrollbar(frame_props, orient="vertical", command = tree.yview)
                    treescrollx = tk.Scrollbar(frame_props, orient="horizontal", command = tree.xview)
                    treescrolly.pack(side = "right", fill = "y")
                    treescrollx.pack(side = "bottom", fill = "x")
                    tree.configure(yscrollcommand = treescrolly.set)
                    tree.configure(xscrollcommand = treescrollx.set)
                    tree.pack(side = "left")

                    ttk.Button(self.top_2, text = "Export ROI Properties", command = lambda: self.export()).pack(side = "top")

        else:
            self.text.insert(tk.END, 'Please perform an analysis first to get properties.\n\n')
            return          
            
    def label_image(self):

        ''' This will create labels for the image. 
        
        The returned labels are regions of interests determined by the
        final mask after all of the analysis is done. 
        Getting these labels will set analysis to complete and allow for 
        properties to be exported
        '''

        if self.current_mask is not None:
            self.boundaries, self.labeled_image = self.custom_processing.labels(self.current_mask)
            self.viewer.add_labels(data = self.boundaries, name = "Labels") 
            self.analysis_complete = True
            self.text.config(state='normal')   
            self.text.insert(tk.END, f'Labels added to the image.\n')
            self.text.config(state='disabled')  
        else:
            self.text.insert(tk.END, 'Please perform an analysis first to get labels.\n\n')
            return 
        
    def props(self):

        ''' Obtains properties of the identified regions of interest. 
        
        This is based on the labels obtained. 
        This step cannot be performed if the analysis is set to complete. 
        Properties can be changed based on what the user selects when prompted
        '''

        self.selected_properties = ["label"]

        if self.analysis_complete == True:
            self.props_table = Toplevel(self.master)
            self.props_table.geometry("300x300")
            self.props_table.configure(bg = "#000000")
            self.props_table.title("Region Properties Options")
            properties = ['area', 'bbox', 'bbox_area', 'max_intensity', 'mean_intensity',
            'min_intensity', 'equivalent_diameter', 'minor_axis_length', 'major_axis_length', 'centroid',
            'coords']
            self.list_box = Listbox(self.props_table, selectmode = 'multiple')
            for val in properties:
                self.list_box.insert(tk.END, val)
            self.list_box.pack(side = "top", fill = BOTH)
            ttk.Button(self.props_table, text = "Start ROI Property Analysis", command = lambda: self.properties_table()).pack(side = "bottom")
                

        else:
            self.text.config(state='normal')
            self.text.insert(tk.END, 'Please perform an analysis first to export properties.\n\n')
            self.text.config(state='disabled')
            
    def export(self):
        ''' Exports an excel sheet of the region propery information obtained.
        This exports the table created from the proerties_table function 
        '''

        if self.df is not None:
            filetype = [
                ('xlsx files', '*.xlsx'),
                ('All files', '*.*')
                ]


            filename = fd.asksaveasfilename(filetypes=filetype, defaultextension=filetype)
            if filename != '':
                with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                    self.df.to_excel(writer, sheet_name= os.path.split(filename)[-1])
                self.text.config(state='normal')
                self.text.insert(tk.END, 'Export complete.\n\n')
                self.text.config(state='disabled')
        else:
            return

def main():
    root = Tk()
    analysis_app = ImageSeg_App(root)
    root.mainloop()

# npc()

if __name__ == "__main__":
    main()
