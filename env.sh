#!/bin/sh
#
# Environment Variables for the Custom URL Scheme in GEMBA Note
#
# Language en - English, ja - Japanese
export APP_LANG=en
# URL Scheme of the target application
# eyachoch6（eYACHO）、eyachoch6s（eYACHO Viewer）、gembanotech6（GEMBA Note）、gembanotech6s（GEMBA Note Viwer）
export APP_URI_SCHEME=gembanotech6
# template_id: Update it with your note template
export NOTE_TEMPLATE_ID=https://mps-gd.metamoji.com/link/*****.mmjloc
# folder_uri: Update it with your folder
export FOLDER_URI=https://mps-gd.metamoji.com/link/*****.mmjloc
# note_new_uri
export NOTE_NEW_URI=http://127.0.0.1:8000/created_note
# CSV file for multiple notes
export CSV_FILE=csv/propertyList.csv
# export CSV_FILE=csv/propertyList_ja.csv
# recordset_uri
export RECORDSET_URI=http://127.0.0.1:8000/recordset
# page_template_id: Update it with your page template
export PAGE_TEMPLATE_ID=https://mps-gd.metamoji.com/link/*****.mmjloc
# tag_namespace: Update it with your tag scheme
export TAG_NAMESPACE=com.metamoji.package.gemba.*****.*****
# ----- END OF FILE -----