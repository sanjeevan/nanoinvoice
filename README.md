nanoinvoice
===========

Open source invoicing app. Built using Python 2.7 and Flask.

It uses the wkhtmltopdf binary to create PDF exports.

See http://nanoinvoice.com for live version of site.

## Installation

Create a virtualenv for the project and install python libs

    cd PROJECT_ROOT
    virtualenv venv
    ./venv/bin/activate 
    pip install -r requirements

Create these dirs:

    PROJECT_ROOT/{log,dist,instance,bin,files}

Copy the wkhtmltopdf binary into the `bin` folder:

    PROJECT_ROOT/bin/wkhtmltopdf

Create an application.cfg file using the example:

    cp application.cfg.sample instance/application.cfg

Setup nginx and supervisor to run the app using the configuration files
within the conf folder

## To compile scss files:

sass --watch screen.scss:../../dist/css/screen.css


