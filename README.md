# URYShowImageGen
Python program for automatically generating show images.

The show image is created by selecting a background image (dark filtered image currently manually croped to a square of 800px by 800px), it then has a branding image applied which is designed for each style (e.g. OB, Speech, Music, News).

## Installation
Clone this repository. Run `python3 -m venv venv`, and `venv/bin/pip install -r requirements.txt`.

## Usage
See run.sh for an example of running as a cron job task.

### Parameters
--apikey The API key from MyRadio that can retrieve all shows for the current term, and set show images.

--debug Logs loads to the screen to show you what it screwed up.

--outputdir Where this script will create the images on the local filesystem.

--apidir MyRadio API requires images to already be on the API server, if this is different from --outputdir, enter this.
