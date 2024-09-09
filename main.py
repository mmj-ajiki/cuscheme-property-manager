#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] main.py
#
# [DESCRIPTION]
#  Sample Server for generating notes using the Custom URL Scheme
# 
# [NOTES]
#
import os, csv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Dict, Any
import urllib.parse
    
app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Collect parameters from the environment variables defined in env.bat or env.sh
# template_id
template = os.environ.get("TEMPLATE_ID")
# folder_uri
folder = os.environ.get("FOLDER_URI")
# note_new_uri
note_uri = os.environ.get("NOTE_NEW_URI")
# CSV fuke
csv_file = os.environ.get("CSV_FILE")
# recordset_uri
recordset_uri = os.environ.get("RECORDSET_URI")
# page_template_id
page_template = os.environ.get("PAGE_TEMPLATE_ID")
# tag_namespace
tag_namespace = os.environ.get("TAG_NAMESPACE")

#
# GET Method
# End Point: /
#
# [DESCRIPTION]
#  Top page of this sample server
#
# [INPUTS] None
# 
# [OUTPUTS]
#  Response to return HTML text
# 
# [NOTES]
#  Open templates/index.html
#
@app.get("/", response_class=HTMLResponse)
async def topPage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Property Management Web App"})
#
# HISTORY
# [1] SEP-09-2024 - Initial version
#

#
# GET Method
# End Point: /single
#
# [DESCRIPTION]
#  Top page of this sample server
#
# [INPUTS] None
# 
# [OUTPUTS]
#  Response to return HTML text
# 
# [NOTES]
#  A note is generated by the following custom URL:
#   gembanotech6:///nsk/new?access_id=<Access ID>&
#       access_token=<Access Token>&
#       template_id=<Template ID>&
#       folder_uri=<Folder URL>&
#       internal_id=<Server Internal ID>&
#       note_new_uri=<Endpoint for the created note>&
#       <Property 1>=<Value 1>&<Property 2>=<Value 2>&...&<Property n>=<Property n>
#
@app.get("/single", response_class=HTMLResponse)
async def createSingleNote(request: Request):
    para = "?"

    id = 'abcdefg'
    token = 'abcdefg123'
    para += 'access_id=' + id + '&access_token=' + token
    # template_id
    para += '&template_id=' + urllib.parse.quote(template)
    # folder_uri
    para += '&folder_uri=' + urllib.parse.quote(folder)
    # internal_id
    internal = '123456789'
    para += '&internal_id=' + internal
    # note_new_uri (for new)
    para += '&note_new_uri=' + urllib.parse.quote(note_uri)
    # note_uri (for open)
    #para += '&note_uri=' + urllib.parse.quote(note_uri)
   
    return templates.TemplateResponse("property.html", {"request": request, "parameters": para})
#
# HISTORY
# [1] SEP-09-2024 - Initial version
#

#
# GET Method
# End Point: /multiple
#
# [DESCRIPTION]
#  Create multiple pages of a note
#
# [INPUTS] None
# 
# [OUTPUTS]
#  Response to return HTML text
# 
# [NOTES]
#  Multiple notes are generated by the following custom URL:
#   gembanotech6:///nsk/new?access_id=<Access ID>&
#       access_token=<Access Token>&
#       template_id=<Note Template ID>&
#       folder_uri=<Folder URL>&
#       internal_id=<Server Internal ID>&
#       note_new_uri=<Endpoint for the created notes>&
#       recordset_uri=<Endpoint to return a set of records>&
#       page_template_id=<Page Template ID>&
#       tag_namespace=<Namespace>
#
@app.get("/multiple")
async def createMultipleNotes(request: Request):
    url = 'gembanotech6:///nsk/new?'

    id = 'abcdefg'
    token = 'abcdefg456'
    url += 'access_id=' + id + '&access_token=' + token
    # template_id
    url += '&template_id=' + urllib.parse.quote(template)
    # folder_uri
    url += '&folder_uri=' + urllib.parse.quote(folder)
    # internal_id
    internal = '987654321'
    url += '&internal_id=' + internal
    # note_new_uri
    url += '&note_new_uri=' + urllib.parse.quote(note_uri)
    # recordset_uri
    url += '&recordset_uri=' + urllib.parse.quote(recordset_uri)
    # page_template_id
    url += '&page_template_id=' + urllib.parse.quote(page_template)
    # tag_namespace
    url += '&tag_namespace=' + urllib.parse.quote(tag_namespace)
    
    return templates.TemplateResponse("multiple.html", {"request": request, "url": url})
#
# HISTORY
# [1] SEP-09-2024 - Initial version
#

#
# POST Method
# End Point: /created_note
#
# [DESCRIPTION]
#  Method used for specifying the 'note_new_uri' parameter to receive the created note
#
# [INPUTS] 
#  note - A list consisting of [ { "noteid": <Note ID>, "internal_id": <Internal ID> } ]
# 
# [OUTPUTS]
#  [{ "noteid": <Note ID>, "internal_id": <Internal ID> }]
# 
# [NOTES]
#
@app.post("/created_note")
async def getNote(request: Request): 
    results = await request.json()
    print("Created Note]", results)
    return results
#
# HISTORY
# [1] SEP-09-2024 - Initial version
#

#
# GET Method
# End Point: /recordset
#
# [DESCRIPTION]
#  Get a set of records of property elements from the CSV file
#
# [INPUTS] 
#  None
# 
# [OUTPUTS]
#  [{'Name':<Property Name1>, 'Type':<Property Type1>, 'Price': <Price1>, 'Address': <Address1>},{...},...]
# 
# [NOTES]
#
@app.get("/recordset")
def getRecordSet():
    output = []
    # Read a CSV file
    skip = True
    with open(csv_file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if skip == False:
                json = {'Name':row[0], 'Type':row[1], 'Price':row[2], 'Address':row[3]}
                output.append(json)
            else:
                skip = False # Skip the first row
    print(output)
    return output
#
# HISTORY
# [1] SEP-09-2024 - Initial version
#