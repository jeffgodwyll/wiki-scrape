Installation
------------

Download, install, setup and authenticate [Google Cloud
SDK](https://cloud.google.com/sdk/docs/quickstart-mac-os-x)

Create app engine project - https://appengine.google.com

Set up project cloud SDK to link to project:

    gcloud config set project <project-id>

Install libs:

    pip install -r requirements -t lib

(I prefer to use this approach when _vendoring_,
https://www.jeffgodwyll.com/posts/2015/google-appegine-vendoring-done-right/)


Run locally
-----------

Run this project locally from the command line and from the project root:

    dev_appserver.py .


Deploy
------

    gcloud app deploy app.yaml

Demo deployed to: https://scrape--wiki.appspot.com/
