#!/usr/bin/python

''' Process a recipe by downloading and formatting as an ebook, then sending via SMTP '''

import subprocess
import sys
import os
import filecmp
import json
import ConfigParser

# Read config.ini
config = ConfigParser.ConfigParser()
config.read("conf/config.ini")

# Deliver to this address
kindle_address = config.get('Kindle','address')
# print "kindle_address: " + kindle_address

# SMTP account settings for outgoing mail
smtp_server = config.get('Smtp Server', 'server')
smtp_port = config.get('Smtp Server', 'port')
smtp_username = config.get('Smtp Server', 'username')
smtp_password = config.get('Smtp Server','password')
# print "smtp_server: " + smtp_server
# print "smtp_port: " + smtp_port
# print "smtp_username: " + smtp_username
# print "smtp_password: " + smtp_password

# Personnal Mail address
personnal_address = config.get('Personnal Address', 'address')
# print "personnal_address: " + personnal_address

# Pocket credentials
pocket_username = config.get('Pocket', 'username')
pocket_password = config.get('Pocket', 'password')
pocket_tag = config.get('Pocket', 'tag')
# print "pocket_username: " + pocket_username
# print "pocket_password: " + pocket_password
# print "pocket_tag: " + pocket_tag

# Path to directories
log_dir = 'logs'
recipe_dir = 'recipes'
ebook_dir = 'ebooks'

# Get command line argument for name of recipe
# recipe_name = sys.argv[1]
recipe_name = 'pocket'

# Output will be redirected to files when run from cron
out_file = open( os.path.join( log_dir, 'out.log'), "w")
err_file = open( os.path.join( log_dir, 'err.log'), "w")
       
# Get name of input and output files
ebook = recipe_name + '_' + pocket_tag + '.mobi'
recipe = recipe_name + '.recipe'

# If old file exists, delete it
if os.path.exists( os.path.join(ebook_dir, 'old', ebook) ) :
    subprocess.call( ['rm', os.path.join(ebook_dir, 'old', ebook) ],
                     stdout=out_file, stderr=err_file)

# If current file exists, move it to old folder
if os.path.exists( os.path.join(ebook_dir, ebook) ) :
    subprocess.call( ['mv', 
                      os.path.join(ebook_dir, ebook), 
                      os.path.join(ebook_dir, 'old', ebook) ],
                     stdout=out_file, stderr=err_file)

# Build command list
command_list = ['ebook-convert',
        os.path.join( recipe_dir, recipe ),
        os.path.join( ebook_dir, ebook ),
        '--username',pocket_username,
        '--password',pocket_password,
        '-vv',
        '--output-profile', 'kindle']

# Download and format using calibre's command line convert tool
subprocess.call( command_list, stdout=out_file, stderr=err_file )

# If we have downloaded a newer copy :
if True : # not sure how to check this

    print "Sending " + ebook + " over email"

    # Send the .mobi over email
    command_list = ['calibre-smtp',
    '-vv',
    '--attachment', os.path.join( ebook_dir, ebook),
    '--subject', 'x',
    '--password', smtp_password,
    '--port', smtp_port,
    '--relay', smtp_server,
    '--username', smtp_username,
    smtp_username,
    kindle_address,
    'Automated message sent from Calibre Kindle Server']

    # Send email using calibre's command line SMTP tool
    subprocess.call( command_list, stdout=out_file, stderr=err_file )

    # Send a simple mail notification to your "real" address
    # to know your .mobi is waiting to be downloaded
    subject = 'A new Pocket Ebook with tag \'' + pocket_tag + '\' has been sent to your Kindle'
    command_list = ['calibre-smtp',
    '-vv',
    '--subject', subject,
    '--password', smtp_password,
    '--port', smtp_port,
    '--relay', smtp_server,
    '--username', smtp_username,
    smtp_username,
    personnal_address,
    'Automated message sent from Calibre Kindle Server']

    # Send email using calibre's command line SMTP tool
    subprocess.call( command_list, stdout=out_file, stderr=err_file )
