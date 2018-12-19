# img2lut
Creates 3D LUT via an image

# What this does
The idea is really simple.

Think about how 3D LUTs are just representations of transformations.

This project will allow for generating an image that contains (almost) all possible RGB combinations. And the functionality that analyzes the result of such image being transformed by any color grading process. For smartphone apps, grading softwares, or whatever that will modify the look of an image and LET YOU SAVE THE RESULT, you can make a 3dlut that resembles exactly that modification process.

# How to use
1. Download texture.jpg, or call generate_texture() to make one
2. Import texture.jpg into any app/software you desire
3. Apply grading processes/color filters
4. Save the result as jpg(check if the result picture size changes, you can just rescale it back to 2210*850)
5. Use lut_from_texture() on the result image to generate your 3DLUT and enjoy it

# Dependencies
A part of this code, when performing a resize of the pregenerated CUBE file, calls a function from module pylut created by gregcotten. Since his original script will not run in Python 3.0, a 3.0 compatible version should be used. 

Please check my illuminascent/pylut repository for the file, and include it in your project.

If you wouldn't mind using a rather large CUBE file, it will be fine to just delete the resize part.
