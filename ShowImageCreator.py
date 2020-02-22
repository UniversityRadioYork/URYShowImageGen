import datetime
from random import randint
import sys
import textwrap

from PIL import Image, ImageFont, ImageDraw
import requests


# Defines location of different image files to create show image.
BACKGROUND_IMAGE_PATH = "GenericShowBackgrounds/"
COLOURED_BARS_PATH = "ColouredBars/"


def log(msg, showid="", stream=sys.stdout):
    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stream.write("{} - ShowID({}), {}\n".format(cur_time, showid, msg))


def debug(msg, showid="", stream=sys.stdout):
    if debugMode.upper() == 'T':
        log(msg, showid, stream)


def error(msg, showid="", stream=sys.stderr):
    log(msg, showid, stream)
    sys.exit(1)


def getShows(apiKey):
    """Returns a dictionary of shows with show id mapping to the show title.
    """
    debug("getShows()")
    url = "https://ury.org.uk/api/v2/show/allshows?current_term_only=1&api_key=" + apiKey
    try:
        req = requests.get(url)
        req.raise_for_status()
        data = req.json()
    except requests.exceptions.HTTPError as e:
        error("Could not access API - {}".format(e))
    shows = {}
    for show in data["payload"]:
        show_payload = data["payload"][show]
        showID = show_payload["show_id"]
        showTitle = show_payload["title"]
        showSubType = show_payload["subtype"]["class"]
        shows[showID] = [showTitle, show_payload["photo"], showSubType]
        debug(showTitle)
    return shows

def getIfDefaultImage(image):
    return image == "/images/default_show_profile.png"

def setImage(apiKey, showId):
    r = requests.put('https://ury.org.uk/api-dev/v2/show/' + str(showId) + '/showphoto?api_key=' + apiKey, json={'tmp_path': '/tmp/autogenshowimg/' + showID + '.jpg'})
    return r.status_code == 200

def applyBrand(showName, outputName, branding):
    """Creates a show image for given show name, output file name and branding.
    Args:
        showName (str): Show name to add to image.
        outputName (str): The name of the outputfile, standard form including the show id.
        branding (str): The branding to be applied.
    Return:
        A JPG image to a sub folder called ShowImages.
    """
    debug("applyBrand()")

    showName = stripPrefix(showName)
    # Determines which overlay to apply to the show image.
    if branding == "speech":
        brandingOverlay = "GreenSpeech.png"
    elif branding == "news":
        brandingOverlay = "News.png"
    elif branding == "music":
        brandingOverlay = "PurpleMusic.png"
    elif branding == "event":
        brandingOverlay = "RedEvent.png"
    elif branding == "primetime":
        brandingOverlay = "Flagship.png"
    elif branding == "collab":
        brandingOverlay = "Flagship.png"
    else: # Should be "regular"
        brandingOverlay = "BlueGeneral.png"
    debug("Branding {}".format(branding if branding != "" else "generic"), showID)

    # maxNumberOfLines = 4
    lines = normalize(showName)
    debug("Lines: " + str(lines))
    debug("Line count: " + str(len(lines)))
    if len(lines) > 6:
        error("Show name is far too long, runs over 6 lines", showID)
    if len(lines) > 4:
        text_size = 40
    else:
        text_size = 70
    debug("Text Size:", text_size)
    normalizedText = "\n".join(lines)

    # Determines which background image to use for the show image.
    img_path = BACKGROUND_IMAGE_PATH + str(randint(1, 25)) + ".png"
    try:
        img = Image.open(img_path)
    except IOError as e:
        error("Background image {} could not be opened - {}".format(img_path, str(e)))

    # Opens overlay and pastes over the background image
    overlay_path = COLOURED_BARS_PATH + brandingOverlay
    try:
        overlay = Image.open(overlay_path)
        img.paste(overlay, (0, 0), overlay)
    except IOError as e:
        error("Overlay image {} could not be opened - {}".format(overlay_path, str(e)))

    # ShowName formatting
    debug("Formatting showname", showID)
    textFont = ImageFont.truetype("Raleway-Bold.ttf", text_size)
    debug("Normalised Text: " + normalizedText)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(normalizedText, textFont)

    # changes the start position, to centre text vertically
    textLineHeight = max(200, 350 - (h/2))

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800 - w) / 2, textLineHeight), normalizedText, (255, 255, 255), textFont, align='center')

    # website URY formatting
    debug("Applying website branding", showID)
    websiteURL = 'URY.ORG.UK \n @URY1350'
    websiteTextSize = 50
    websiteFont = ImageFont.truetype("Raleway-SemiBoldItalic.ttf", websiteTextSize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(websiteURL, websiteFont)
    websiteURLHeight = 510

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800 - w) / 2, websiteURLHeight), websiteURL, (255, 255, 255), websiteFont, align='center')

    # Saves the image as the output name in a subfolder ShowImages
    debug("Saving the final image", showID)
    img.convert('RGB').save('ShowImages/{}.jpg'.format(outputName))


def brandingFromShowName(showName):
    """Determines the branding to be applied based on the show name.
    Args:
        showName (str): The show name.
    Return:
        What branding to apply.
    """

    show_map = {
        "URY Presents:": "OB",
        "The URY Pantomime 2016: Beauty and the Beast": "OB",
        "#": "OB",

        "Georgie and Angie's Book Corner": "Speech",
        "Stage": "Speech",
        "Speech Showcase": "Speech",
        "Screen": "Speech",

        "URY Newshour": "News",
        "York Sport Report": "News",
        "URY SPORT: Grandstand": "News",
        "University Radio Talk": "News",

        "URY:PM - (( URY Music ))": "Music",
        "((URY)) Music: Bedtime Mix": "Music",

        "URY Brunch": "Flagship",
        "URY Afternoon Tea": "Flagship",
        "URY:PM - ": "Flagship",
        "National Award Nominated URY:PM with Nation Award Nominated K-Spence": "Flagship",
    }

    for k in show_map:
        if showName.startswith(k):
            return show_map[k]
    return ""


def stripPrefix(showName):
    """Strips any prefix from the show name.
    Args:
        showName (str): The show name.
    Return:
        The show name without the prefix.
    """
    prefixes = [
        "URY Brunch - ",
        "URY:PM - ",
        "URY Afternoon Tea: ",
        "URY Brunch: ",
        "URY Breakfast: ",
        "URY Speech: ",
        "URY Music: ",
        "URY News & Sport: ",
        "URY Sport: "
        ]
    output = showName
    for prefix in prefixes:
        if showName.startswith(prefix):
            output = showName[len(prefix):]
            break

    return output


def normalize(input_str):
    """Splits the show name into separate lines of maximum lengths.
    Args:
        input (str): The Show name.
    Return:
        List of strings of limited length, depending on the size of the input text
    """
    debug("normalize()")

    lines = textwrap.wrap(input_str, width=17, break_long_words=False, break_on_hyphens=False)
    if len(lines) > 4 or len(max(lines, key=len)) > 17:
        lines = textwrap.wrap(input_str, width=20, break_long_words=False, break_on_hyphens=False)
    if len(max(lines, key=len)) > 20:
        error("Word too long for image", showID)
    return lines


if len(sys.argv) < 3:
    error("System arguments not passed in")
else:
    apiKey = sys.argv[1]
    debugMode = sys.argv[2]

################################
################################
#    Uses API To Get Shows     #
################################
################################
debug("Program start")
ApiShowsDict = getShows(apiKey)

for showKey in ApiShowsDict:

        show = ApiShowsDict[showKey]
        if getIfDefaultImage(show[1]):
            # The show uses the default image, let's make it one.
            showName = show[0]
            showID = str(showKey)
            branding = show[2]
            applyBrand(showName, showID, branding)


debug("Program complete")
