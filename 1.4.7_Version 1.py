import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw

def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list
    
def flag(original_image):
    '''Set a circular logo at the center of the canvas.
    The Image must be a PIL''' 
    width, height = original_image.size
    circle_ratio = int(min(width,height)*.25) #Dimensions for the resize function (used later) need to be int
    
    mid_pic= PIL.Image.open(os.path.join(os.getcwd(), 'earth.png'))
    mid_pic=mid_pic.resize((circle_ratio, circle_ratio))
    
#Drawing Layer was not needed, in place of it we used a paste function
    # frame_mask = PIL.Image.new('RGBA', (width, height), (0,0,0,0))
    # drawing_layer = PIL.ImageDraw.Draw(frame_mask)
    # drawing_layer.circle((height/2)-circle_ratio,(width/2),(height/2)+circle_ratio,(width/2),fill=(color))

    result = original_image.copy()
    result.paste(mid_pic, (width/2-circle_ratio/2,height/2-circle_ratio/2))
    return result

def flag_all_images(directory=None):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    #load all the images
    image_list, file_list = get_images(directory)  

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = os.path.splitext(file_list[n])
        
        # Round the corners with radius = 30% of short side
        new_image = flag(image_list[n])
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)