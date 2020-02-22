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
        shows[showID] = showTitle
    return shows


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

    ##########################################
    ##########################################
    # Hack to get branding from show name
    # branding = "Old"
    branding = brandingFromShowName(showName)
    ##########################################
    ##########################################

    showName = stripPrefix(showName)
    # Determines which overlay to apply to the show image.
    if branding == "Speech":
        brandingOverlay = "GreenSpeech.png"
    elif branding == "News":
        brandingOverlay = "News.png"
    elif branding == "Music":
        brandingOverlay = "PurpleMusic.png"
    elif branding == "OB":
        brandingOverlay = "RedOB.png"
    elif branding == "Old":
        brandingOverlay = "WhitePreShowImageFormat.png"
    elif branding == "Flagship":
        brandingOverlay = "Flagship.png"
    else:
        brandingOverlay = "BlueGeneral.png"
    debug("Branding {}".format(branding if branding != "" else "generic"), showID)

    # maxNumberOfLines = 4
    lines = normalize(showName)
    debug("Lines: lines)
    debug("Line count: " + len(lines))
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
    if showName.startswith("URY Brunch -"):
        output = showName[12:]
    elif showName.startswith("URY:PM - "):
        output = showName[9:]
    elif showName.startswith("URY Afternoon Tea: "):
        output = showName[19:]
    elif showName.startswith("URY Brunch: "):
        output = showName[12:]
    else:
        output = showName
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
# ShowsDict = getShows(apiKey)
ShowsDict = {
    12209: 'URY:PM - URY Chart Show',
    12868: 'URY:PM - Roku Radio',
    12374: 'URY Newshour',
    12928: 'No Ducks Given',
    12957: '(20,000 Leagues) Into the Void',
    13000: "What's That Topic?",
    13008: 'Stage',
    13049: 'York Sport Report',
    13053: 'National Award Nominated URY:PM with National Award Nominated K-Spence',
    13065: 'URY Brunch: The Saturday Lie-In',
    13067: "Georgie and Angie's Book Corner",
    13070: 'Gully Riddems',
    13071: 'Indie Unearthed',
    13073: 'Building Bridges - The Road to Rock and Roll',
    13074: 'Castle Sessions',
    13120: 'Pardon my French',
    13123: 'Your Opinion is Wrong',
    13125: 'The Night Call',
    13126: 'InsomniHour',
    13130: "What's on my playlist?",
    13134: "Diggin' Deep",
    13140: 'Barry Tomes',
    13141: 'Topics & Tunes',
    13149: 'RapChat',
    13156: 'Morning Glory',
    13159: 'The 20th Century Collection',
    11628: 'Retrospectre!',
    13167: 'Star Struck Jack and The Mystery Cat',
    13177: 'Kick back Sundays with Kate ',
    13179: 'URY:PM (( URY Music ))',
    13184: 'The Late Night Bass Podcast',
    13186: 'These Charming Girls',
    13189: 'Grumpy Youngish Men',
    13192: "Leckie's listeners",
    13202: 'Dylan with a Mike!',
    13204: 'The Right Faces For Radio',
    13209: 'Things Can Only Get Bitter',
    13227: 'Fringe: Full Metal Racket',
    13228: 'URY Brunch: Star-Struck Jack and the Mystery Cat',
    13232: 'URY Brunch - Breakfast Club',
    13233: "URY Brunch - We're All Ears",
    13235: 'Catchy Chunes',
    13245: 'In Between Days',
    13246: 'No DLC Required',
    13255: 'The Breakz Showcase ',
    13256: 'URY Brunch - Amateur Hour',
    13257: "Grandad's Jazz",
    13258: 'URY:PM - Peculiarities',
    13259: 'Tales from the Phantasmagoria',
    13260: 'URY:PM - Willis Weekly',
    13261: 'Almost Audible',
    13262: 'Cream Cheese',
    13263: "#URYonTOUR: Freshers' 2016",
    13264: 'URY:PM - No Ducks Given',
    13265: 'Screen',
    13266: 'URY Brunch - The Culture Show',
    13267: 'URY Whisper Show',
    13268: 'URY Brunch - Smile!',
    13269: 'Midweek Marauders',
    13270: 'Hidden Gems',
    13271: 'Go Funk Yourself',
    13272: 'The Brighter Side of Life',
    13273: "Peck's Picks",
    13274: 'Toons in the Afternoons',
    13275: 'Roger That',
    13276: 'The Eclectic Mix',
    13277: 'The Alternative Music Show',
    13278: 'DESERT ISLAND DISCO',
    13279: 'coHEARence',
    13280: 'Formula 1 Analysis',
    13282: 'AM-bassador',
    13283: 'Liv and the guy',
    13284: 'Monday Chills ',
    13285: 'Your Weekend',
    13287: 'Non-Stop-Tom',
    13288: 'Cool Britannia',
    13289: 'Nothing but Chuuuunes with Hayds',
    13290: 'The Ben and Jasper Show',
    13291: 'Why Not?',
    13292: 'Alternative Juice',
    13293: "Chef Will - Where there's a Will, there's a...",
    13294: 'NOUVEAU.',
    13295: 'Kiltie Pleasures with Jonny ',
    13296: 'Brain Waves',
    13297: 'The Sounds of Time',
    13298: "Josh and Tom's Afternoon Antics",
    13299: 'Music for Old People',
    13300: 'GAYdio',
    13301: 'PolChat',
    13302: 'Vanbrugh Chair Debate',
    13303: 'URY Presents: UYCB 2016 Winter Concert',
    13304: 'NICturnal',
    13305: 'Speech Showcase',
    13306: 'More Songs About Chocolate And Girls...',
    13307: 'URY Does RAG Courtyard Takeover'
}

for key in ShowsDict:
    showName = ShowsDict[key]
    showID = str(key)
    branding = 'OB'
    applyBrand(showName, showID, branding)

debug("Program complete")
