.. NPC Image Analysis documentation master file, created by
   sphinx-quickstart on Fri May 20 16:15:03 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NPC Image Analysis's documentation!
==============================================

**NPC Image Analysis** is a Python app for analyzing 3D images of Neural Progenitor Cells (NPCs). In particular, it
was made to answer the specific question of analyzing the radial process of the cells. This application
aims to allow you to use a default implementation to get you started, but also allows the user to
customize the analysis process.

.. note::
   This project is still under active development.

Why NPC Image Analysis?
=======================
Originally, this project was aimed to answer a specific question by looking at NPCs in developing zebrafish
brains. The purpose of this, what to hopefully eliminate some of the biase that can come with trying to
perform image analysis. As the sole developer of this project, I grew attached to continuously iterating
on this project. While working on it and trying to explain this image analysis project to my PI, I found
that the growing Python scripts might be overwhelming for a non-programmer. Thus, this project has been 
born to hopefully bridge the gap between trying to analyze the images in a specific context.

This may have other purposes beyond this specific context, so I decided to share it here. 

Check out the :doc:`Usage` section for further information.

You can find the source code `here <http://github.com/Anhardy1999/NPC_Image_Analysis>`_

Navigation
===========

.. toctree::
   Usage
   Default Analysis Usage
   Custom Analysis Usage
   Region Properties
   Examples
   


.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   Image_Analysis_App
   Image_Analysis

   






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
