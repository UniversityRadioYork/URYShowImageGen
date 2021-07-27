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

## Docker

Docker will run the `daemon.py` file, calling the ShowImageGen once an hour.

-   Build the image: `docker build -t show-image-gen .`
- Set the `.env` file. As `DEBUG_MODE` and `DRY_RUN` are booleans, set `1` for true, `0` for false.
-   Run the container, mounting the ouput directory to `/tmp/showimages`, and adding the `.env`, i.e.:

    `docker run -v /mnt/showimages:/tmp/showimages --env-file .env -d --name show-image-gen show-image-gen`
