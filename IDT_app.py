#!/usr/bin/env python3

import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_core_components import Dropdown, Markdown, Slider, Upload, Link
from dash_html_components import A, Code, Div, H3, H5, Li, Pre, Ul
#from app import APP, SERVER, SERVER_URL
import sys
import urllib.parse
from flask import Flask, send_from_directory
import os
import base64
import glob

import colour
from colour.characterisation import idt_matrix
from colour import ILLUMINANT_SDS
from colour.colorimetry import sds_and_multi_sds_to_multi_sds
from colour.io import read_sds_from_csv_file
from colour.characterisation import RGB_SpectralSensitivities

__all__ = [
    'APP_NAME', 'APP_PATH', 'APP_DESCRIPTION', 'APP_UID', 
    'set_idt_output'
]

APP = dash.Dash(__name__)
APP_NAME = 'IDT Matrix Generator'
APP_PATH = '/apps/{0}'.format(__name__.split('.')[-1])
APP_DESCRIPTION = ('This app computes the Input Device Transform given a set of camera system spectral sensitivities.')
APP_UID = hash(APP_NAME)
SERVER = Flask(__name__)
SERVER_URL = os.environ.get('COLOUR_DASH_SERVER')

ILLUMINANTS_OPTIONS = [{
    'label': key,
    'value': key
} for key in sorted(ILLUMINANT_SDS.keys())]

image_filename = '/Users/gaylemcadams/Desktop/AMPAS Internship/Python/images/example.jpg' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

APP.layout = Div([
    H3([Link(APP_NAME, href=APP_PATH)], className='text-center'),
    Div([
        Markdown(APP_DESCRIPTION),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image)),
        H5(children='Illuminant'),
        Dropdown(
            id='illuminant-{0}'.format(APP_UID),
            options=ILLUMINANTS_OPTIONS,
            value=ILLUMINANTS_OPTIONS[0]['value'],
            clearable=False,
            className='app-widget'),
        H5(children='Camera System Spectral Sensitivities'),
        Upload(
            id='sensitivities-{0}'.format(APP_UID),
            accept='csv',
            className='app-widget',
            children=Div([
                A('Upload .csv File')
            ]),
            #contents=sds_and_multi_sds_to_multi_sds(read_sds_from_csv_file('sensitivities-{0}'.format(APP_UID))),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        Pre([Code(id='idt-matrix-{0}'.format(APP_UID), className='code shell')],
            className='app-widget app-output'),
            Ul([
            Li([Link('Back to index...', href='/', className='app-link')],
               className='list-inline-item'),
            Li([
                A('Permalink',
                  href=urllib.parse.urljoin(SERVER_URL, APP_PATH),
                  target='_blank')
            ],
               className='list-inline-item'),
            Li([
                A('colour-science.org',
                  href='https://www.colour-science.org',
                  target='_blank')
            ],
               className='list-inline-item'),
        ],
           className='list-inline text-center'),
    ],
        className='col-6 mx-auto')
])

@APP.callback(
    Output(
        component_id='idt-matrix-{0}'.format(APP_UID),
        component_property='children'),
    [
        Input('illuminant-{0}'.format(APP_UID), 'value'),
        Input('sensitivities-{0}'.format(APP_UID), 'contents')
    ])
def set_idt_output(illuminant, sensitivities):
    path = '/Users/gaylemcadams/Desktop/AMPAS Internship/Python/ArriAlexa.csv'
    sensitivities = sds_and_multi_sds_to_multi_sds(read_sds_from_csv_file(path).values())
    M = idt_matrix(sensitivities, colour.ILLUMINANT_SDS[illuminant])

    M = str(M)
    return M

if __name__ == '__main__':
    APP.run_server(debug=True)