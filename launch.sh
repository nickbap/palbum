#!/usr/bin/bash

# These variables may need to be updating depending on your project setup
URL=http://127.0.0.1:5000

if [[ "$OSTYPE" == "linux-gnueabihf" ]]; then
        # raspberry pi
        PALBUM_PATH=/home/$USER/Documents/palbum
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macos
        PALBUM_PATH=/Users/nickbautista/documents/projects/palbum
else
        printf 'ERROR: path to palbum is not set!'
        exit 1
fi

wait_for_palbum () {
  echo "Launching palbum"
  until $(curl --output /dev/null --silent --head --fail $URL); do
    printf '.'
    sleep 1
done
chromium-browser $URL --start-fullscreen
echo "Ready!"
}

start_palbum () {
    cd $PALBUM_PATH  && venv/bin/flask run
}

wait_for_palbum &
start_palbum