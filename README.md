# NPC Image Analysis

A Python package to assist in performing image analysis on Neural Progenitor Cells (NPCS).  In particular, it was made to answer the specific question of analyzing the radial process of the cells. This application aims to allow you to use a default implementation to get you started, but also allows the user to customize the analysis process.

![1](https://user-images.githubusercontent.com/96258085/169920909-2001e637-31bf-44ca-afc6-cbf81f0f8dfd.jpg)


**NPC Analysis** aims to bridge the gap between those who want to perform image analysis but are less technical and are blocked by complicated and lengthy python code documentation.  This provides a simple GUI for users to perform image analysis, specifically on the radial process of Neural Progenitor Cells. However, this application can likely be used for any analysis that requires the inital use of a mask to limit the analysis to a specific region. 

NPC Image Analysis utilizes skimage's image processing tools as well as napari for viewing the images in 3D.


## ReadTheDocs
You can find full documentation here: [ReadTheDocs](https://npc-image-analysis.readthedocs.io/en/latest/index.html) 

The page contains information on the internal classes, using both the Default and Custom analysis and further elaborates on some of the image processing steps.

## Installation

In the command line type: 

```pip install npc-analyze-image```

It would be preferred to do this in its own environment, but this is not required.

## How to use

Once the package is installed run 
```python -m NPCAnalysis``` 

The program shall initiate. Full information on usage and using the functions can be found on the [ReadTheDocs](https://npc-image-analysis.readthedocs.io/en/latest/index.html) page.


