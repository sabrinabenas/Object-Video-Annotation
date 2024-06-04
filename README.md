# Object Video Annotation
OVA is a simple GUI for making video annotations of object recognition experiments

Some code are adapted from https://github.com/Wahl-lab/EXPLORE

## Instructions 

Basically, you upload your behavior video, select the position of the object, give them a name and a key label ('p' reserved).

After that, you will see a frame just to remember the key label of each object in case you have many objects.

After pressing _finish_, you will see the video and pressing each key label will select the frames that the animal explores the object.

## Installation
- clone repo
- create conda env
  ```sh
  conda env create -f environment.yml
  ```
- conda activate OVA