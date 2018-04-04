from PIL import Image, ImageFont, ImageDraw
from random import randint
import json, sys, requests
from datetime import time, datetime
from time import strftime

# Defines location of different image files to create show image.
backgroundImagePath = "GenericShowBackgrounds/"
colouredBarsPath = "ColouredBars/"
try:
	apiKey = sys.argv[1]
	url = "https://ury.org.uk/api/v2/show/allshows?current_term_only=0&api_key=" + apiKey
	debugMode = sys.argv[2]
except IndexError as e:
	log("ERROR", "System Argument(s) not passed in.", str(e))


def getShows():
    """
    A function to return a dictionary of shows with show id mapping to the show title.
    Return:
        The dictionary of shows with show ids mapping to the show title.
    """
    try:
    	log("DEBUG", "Running getShows() function.")
    	data = requests.get(url).json()
    	shows = {}

    	for show in data["payload"]:
            showID = data["payload"][show]["show_id"]
            showTitle = data["payload"][show]["title"]
            if showID != 13031:
                shows[showID] = showTitle

    	return shows
    except IOError as e:
    	log("API","Could not acess API.", str(e))
    	sys.exit(0)


def applyBrand(showName, outputName, branding):
    """
    A function to create a show image for given show name, output file name and branding.
    Args:
        showName (str): Show name to add to image.
        outputName (str): The name of the outputfile, standard form including the show id.
        branding (str): The branding to be applied.
    Return:
        The function outputs a JPG image to a sub folder called ShowImages.
    """
    
    ##########################################
    ##########################################
    ## Hack to get branding from show name
    #branding = "Old"
    branding = brandingFromShowName(showName)
    ##########################################
    ##########################################

    log("DEBUG", "Running applyBrand() function.", showID)
    showName = stripPrefix(showName)
    # Determines which overlay to apply to the show image.
    if branding == "Speech":
        log("DEBUG", "Branding speech.", showID)
        brandingOverlay = "GreenSpeech.png"
    elif branding == "News":
        log("DEBUG", "Branding news.", showID)
        brandingOverlay = "News.png"
    elif branding == "Music":
        log("DEBUG", "Branding music.", showID)
        brandingOverlay = "PurpleMusic.png"
    elif branding == "OB":
        log("DEBUG", "Branding OB.", showID)
        brandingOverlay = "RedOB.png"
    elif branding == "Old":
        log("DEBUG", "Branding old.", showID)
        brandingOverlay = "WhitePreShowImageFormat.png"
    elif branding == "Flagship":
        log("DEBUG", "Branding old.", showID)
        brandingOverlay = "Flagship.png"
    else:
        log("DEBUG", "Branding generic show.", showID)
        brandingOverlay = "BlueGeneral.png"

    #maxNumberOfLines = 4
    normalizedText, lines, text = normalize(showName, True)
    if lines > 4:
        normalizedText, lines, text = normalize(showName, False)
        if lines > 6:
            log("DCM", "Show name is far too long, runs over 6 lines", showID, "Within function applyBrand().")
            raise Exception 
            
# Determines which background image to use for the show image.
    try:
        img = Image.open(backgroundImagePath + str(randint(1,25)) +".png")
    except IOError as e:
        log("Error", "Background image could not be opened.", str(e))

# Opens overlay and pastes over the background image
    try:
        overlay = Image.open(colouredBarsPath + brandingOverlay)
        img.paste(overlay, (0, 0), overlay)
    except IOError as e:
        log("Error", "Overlay image could not be opened.", str(e))

# ShowName formatting
    log("DEBUG", "Formatting the showName.", showID)
    # textFont = ImageFont.truetype(<font-file>, <font-size>)
    textFont = ImageFont.truetype("Raleway-Bold.ttf", text)
    
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(normalizedText, textFont)
        
    # changes the start position, to centre text vertically
    if text == 65:
        if lines == 3:
            textLineHeight = 230
        elif lines == 2:
            textLineHeight = 275
        elif lines == 1:
            textLineHeight = 300
        elif lines == 4:
            textLineHeight = 205
        else:
            textLineHeight = 205
    else:
        if lines == 1:
            textLineHeight = 320
        elif lines == 2:
            textLineHeight = 295
        elif lines == 3:
            textLineHeight = 275
        elif lines == 4:
            textLineHeight = 250
        elif lines == 5:
            textLineHeight = 235
        else:
            textLineHeight = 215

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, textLineHeight),normalizedText,(255,255,255),textFont, align='center')

# website URY formatting
    log("DBEUG", "Applying website branding.", showID)
    websiteURL = 'URY.ORG.UK \n @URY1350'
    websiteTextSize = 50
    websiteFont = ImageFont.truetype("Raleway-SemiBoldItalic.ttf", websiteTextSize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(websiteURL, websiteFont)
    websiteURLHeight = 510 

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, websiteURLHeight), websiteURL,(255,255,255),websiteFont, align='center')

# Saves the image as the output name in a subfolder ShowImages
    log("DEBUG", "Saving the final image.", showID)
    try:
    	img.save('ShowImages/%s.jpg' %outputName)
    except "Not enough storage space!":
        log("Error", "Not enough storage space to save the show image!", showId)


def brandingFromShowName(showName):
    """
    A function to determine the branding to be applied based on the show name.
    Args:
        showName (str): The show name.
    Return:
        A string of what branding to apply.
    """
    if showName[:13] == "URY Presents:":
        output = 'OB'
    elif showName == "The URY Pantomime 2016: Beauty and the Beast":
        output = 'OB'
    elif showName[:1] == "#":
        output = 'OB'
    
    elif showName == "Georgie and Angie's Book Corner":
        output = 'Speech'
    elif showName == "Stage":
        output = 'Speech'
    elif showName == "Speech Showcase":
        output = 'Speech'
    elif showName == "Screen":
        output = 'Speech'
    
    elif showName == "URY Newshour":
        output = 'News'
    elif showName == "York Sport Report":
        output = 'News'
    elif showName == "URY SPORT: Grandstand":
        output = 'News'
    elif showName == "University Radio Talk":
        output = 'News'
    
    elif showName == "URY:PM - (( URY Music ))":
        output = 'Music'
    elif showName == "((URY)) Music: Bedtime Mix":
        output = 'Music'
    
    elif showName[:10] == "URY Brunch":
        output = 'Flagship'
    elif showName[:17] == "URY Afternoon Tea":
        output = 'Flagship'
    elif showName[:8] == "URY:PM -":
        output = 'Flagship'
    elif showName == "National Award Nominated URY:PM with National Award Nominated K-Spence":
        output = 'Flagship'
    
    else:
        output = ''
    return output


def stripPrefix(showName):
    """
    A function to strip the prefix from the show name.
    Args:
        showName (str): The show name.
    Return:
        The show name without the prefix.
    """
    if showName[:12] == "URY Brunch -":
        log("DEBUG", "Removing 'URY Brunch -' from the title.", showID)
        output = showName[12:]
    elif showName[:9] == "URY:PM - ":
        log("DEBUG", "Removing 'URY:PM -' from the title.", showID)
        output = showName[9:]
    elif showName[:19] == "URY Afternoon Tea: ":
        log("DEBUG", "Removing 'URY:PM -' from the title.", showID)
        output = showName[19:]
    elif showName[:12] == "URY Brunch: ":
        log("DEBUG", "Removing 'URY:PM -' from the title.", showID)
        output = showName[12:]
    else:
        log("DEBUG", "No prefix to be removed from the title.", showID)
        output = showName
    return output


def normalize(input, firstAttmpt):
    """
    A function to split the show name into seperate lines of maximum lengths.
    Args:
        input (str): The Show name.
        firstAttmpt (Bool): Is this the first attempt at normalising the text?
    Return:
        Two strings. firstLine is the first line of text. otherLines is the string of other lines with line breaks inserted when necessary.
    """
    log("DEBUG", "Running normalize() function.", showID)
    words = input.split(" ")
    LinesList = []

    longestWord = 0
    for word in words:
        if len(word) > longestWord:
            longestWord = len(word)

    if longestWord <= 17 and firstAttmpt:
        maxLineLength = 17
        text = 65
    else:
        maxLineLength = 30
        text = 40

    for word in words:
        if len(word) > maxLineLength:
            log("DCM", "Word too long for image.", showID, "Within function normalize().")
            raise Exception
        elif len(LinesList) > 0 and (len(LinesList[-1]) + len(word) < maxLineLength):
            LinesList[-1] += " " + word
        else:
            LinesList.append(word)

    normalizedText = "".join(item + "\n" for item in LinesList)
    lines = normalizedText.count('\n')
    return normalizedText, lines, text


def log(typeM="DEBUG", message="NONE", showNum="NULL", errorMessage="No exception error message."):
    """
    A function to output logs to a log file for debugging or exceptions.
    Args:
        typeM (str): The type of log to make.
        mesage (str): The message to explain the log.
        showNum (str): The show ID (if there is one).
        errorMessage (str): The exception (if there is one).
    """
    if  (debugMode.upper() == 'T') or (typeM.upper() == "DCM") or (typeM.upper() == "API") or (typeM.upper() == "ERROR"):
        try:
            f=open("logfile.log","a")
            now = datetime.now()
            curTime = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            f.write(curTime + " - [" + typeM.upper() + "] Show ID: {" + showNum + "} " + message + "\n" + errorMessage + "\n")
            f.close()
        except IOError as e:
            pass
    else:
        pass


################################
################################
#### Uses API To Get Shows #####
################################
################################
log("DEBUG", "Program Started!")
#ShowsDict = getShows()
ShowsDict = {12209: 'URY:PM - URY Chart Show', 12868: 'URY:PM - Roku Radio', 12374: 'URY Newshour', 12928: 'No Ducks Given', 12957: '(20,000 Leagues) Into the Void', 13000: "What's That Topic?", 13008: 'Stage', 13049: 'York Sport Report', 13053: 'National Award Nominated URY:PM with National Award Nominated K-Spence', 13065: 'URY Brunch: The Saturday Lie-In', 13067: "Georgie and Angie's Book Corner", 13070: 'Gully Riddems', 13071: 'Indie Unearthed', 13073: 'Building Bridges - The Road to Rock and Roll', 13074: 'Castle Sessions', 13120: 'Pardon my French', 13123: 'Your Opinion is Wrong', 13125: 'The Night Call', 13126: 'InsomniHour', 13130: "What's on my playlist?", 13134: "Diggin' Deep", 13140: 'Barry Tomes', 13141: 'Topics & Tunes', 13149: 'RapChat', 13156: 'Morning Glory', 13159: 'The 20th Century Collection', 11628: 'Retrospectre!', 13167: 'Star Struck Jack and The Mystery Cat', 13177: 'Kick back Sundays with Kate ', 13179: 'URY:PM (( URY Music ))', 13184: 'The Late Night Bass Podcast', 13186: 'These Charming Girls', 13189: 'Grumpy Youngish Men', 13192: "Leckie's listeners", 13202: 'Dylan with a Mike!', 13204: 'The Right Faces For Radio', 13209: 'Things Can Only Get Bitter', 13227: 'Fringe: Full Metal Racket', 13228: 'URY Brunch: Star-Struck Jack and the Mystery Cat', 13232: 'URY Brunch - Breakfast Club', 13233: "URY Brunch - We're All Ears", 13235: 'Catchy Chunes', 13245: 'In Between Days', 13246: 'No DLC Required', 13255: 'The Breakz Showcase ', 13256: 'URY Brunch - Amateur Hour', 13257: "Grandad's Jazz", 13258: 'URY:PM - Peculiarities', 13259: 'Tales from the Phantasmagoria', 13260: 'URY:PM - Willis Weekly', 13261: 'Almost Audible', 13262: 'Cream Cheese', 13263: "#URYonTOUR: Freshers' 2016", 13264: 'URY:PM - No Ducks Given', 13265: 'Screen', 13266: 'URY Brunch - The Culture Show', 13267: 'URY Whisper Show', 13268: 'URY Brunch - Smile!', 13269: 'Midweek Marauders', 13270: 'Hidden Gems', 13271: 'Go Funk Yourself', 13272: 'The Brighter Side of Life', 13273: "Peck's Picks", 13274: 'Toons in the Afternoons', 13275: 'Roger That', 13276: 'The Eclectic Mix', 13277: 'The Alternative Music Show', 13278: 'DESERT ISLAND DISCO', 13279: 'coHEARence', 13280: 'Formula 1 Analysis', 13282: 'AM-bassador', 13283: 'Liv and the guy', 13284: 'Monday Chills ', 13285: 'Your Weekend', 13287: 'Non-Stop-Tom', 13288: 'Cool Britannia', 13289: 'Nothing but Chuuuunes with Hayds', 13290: 'The Ben and Jasper Show', 13291: 'Why Not?', 13292: 'Alternative Juice', 13293: "Chef Will - Where there's a Will, there's a...", 13294: 'NOUVEAU.', 13295: 'Kiltie Pleasures with Jonny ', 13296: 'Brain Waves', 13297: 'The Sounds of Time', 13298: "Josh and Tom's Afternoon Antics", 13299: 'Music for Old People', 13300: 'GAYdio', 13301: 'PolChat', 13302: 'Vanbrugh Chair Debate', 13303: 'URY Presents: UYCB 2016 Winter Concert', 13304: 'NICturnal', 13305: 'Speech Showcase', 13306: 'More Songs About Chocolate And Girls...', 13307: 'URY Does RAG Courtyard Takeover'}

for key in ShowsDict:
    showName = ShowsDict[key]
    showID = str(key)
    branding = 'OB'
    applyBrand(showName, showID, branding)

log("DEBUG", "Program Complete!")