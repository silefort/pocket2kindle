# Pocket 2 Kindle

This python app uses calibre to fetch your articles from your Pocket account and send it to your Kindle

## Install
These instructions are for Ubuntu:

    sudo apt-get install calibre
    git clone git@github.com:silefort/pocket2kindle.git
    cd pocket2kindle

## Configure
    cp conf/config.ini.sample conf/config.ini
    vim conf/config.ini

Edit your config file

## Execute
./process-recipe.py

## Acknowledgements
* https://github.com/chris838/calibre-kindle-server
