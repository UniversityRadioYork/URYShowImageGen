# Run the Show Image Gen as a Daemon istead of cronjob

import time

import ShowImageCreator

while True:
    ShowImageCreator.main(True)
    time.sleep(3600)

