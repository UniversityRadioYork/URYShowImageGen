'''
    To Do:
        - Centre Text to middle of box, depending on number of lines of text.
        - Should Name the file differently with only alpha numeric characters.
        - Should email/ log error if show name is uncompatable.
'''

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint

def add_text(showName):
    """
    Args:
        showName (str): Show name to add to image.
    Output:
        The function outputs a JPG image to a sub folder called ShowImages.
    """
    print(showName) #Prints to the console which show is being processed.

    # This looks at the name of the show weather it is a flagship or not.
    if showName == '':
        raise Exception("No show name provided.")
    elif showName[:10] == 'URY Brunch': #AM Flagship
        img = Image.open("AMFlagshipBackground.png")
    elif showName[:6] == 'URY:PM': #PM Flagship
        img = Image.open("PMFlagshipBackground.png")
    
    # If the show is not flagship, there is a list of backgrounds to randomly generate a show image.
    else:
        rGI = randint(0,7)
        RandomBackgrounds = ["Other1.png","Other2.png","Other3.png","Other4.png","Other5.png","Other6.png","Other7.png","Other8.png"] #List of different backgrounds.
        img = Image.open(RandomBackgrounds[rGI])
    
    #This works out if the show name will fit neatly on the image, if the show name is less than 14 characters the normalize function will not be called.
    if len(showName) <= 14:
        prshowName = showName
    else:
        prshowName = normalize(showName)
    
    #Adds the text to the selected image.
    font_size = 85
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Raleway-SemiBoldItalic.ttf", font_size)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(prshowName)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((60, 60),prshowName,(255,255,255),font)
    img.save('Showimages/%s.jpg' %showName)

def normalize(input):
    """
    Args:
        input (str): Takes in a string for a show name.
    Returns:
        A string containg line breaks so the text is not longer that 14 characters (including spaces)
    """
    output = []
    for word in input.split(" "):
        if len(word) > 14:
            raise Exception("Word too long for image. Contact DCM.")
        elif len(output) > 0 and (len(output[-1]) + len(word) < 14):
            output[-1] += " " + word
        else:
            output.append(word)

    if len(output) > 4:
        raise Exception("Spans too many lines for image. Contact DCM bitches.")

    return "".join(item + "\n" for item in output)

################
#### Tests #####
################
#add_text('URY Brunch Some Show Name')
#add_text('URY:PM Some Show Name')
#add_text('Some Show Name')
#add_text('Building Bridges - TheRoadtoRockandRoll and Roll')
#print(normalize("Building Bridges - The Road to Rock and Roll"))


## This runs through a file to generate show images.
output =[]
f = open('Shows.txt', 'r')
for line in f:
    output.append(line)
f.close()
for i in range(0,len(output)):
    output[i] = output[i].rstrip('\n')
for el in output:
    add_text(el)
    
