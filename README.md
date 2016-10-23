Installation
------------

Download, install, setup and authenticate [Google Cloud
SDK](https://cloud.google.com/sdk/docs/quickstart-mac-os-x)

Create app engine project

Set up project cloud SDK to link to project:

    gcloud config set project <project-id>

Install libs:

    pip install -r requirements -t lib

Deploy
------

    gcloud app deploy app.yaml


