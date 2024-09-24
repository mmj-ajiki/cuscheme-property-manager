@echo off
rem
rem Environment Variables for the Custom URL Scheme in GEMBA Note
rem
rem Language en - English, ja - Japanese
set APP_LANG=en
rem URL Scheme of the target application
rem eyachoch6（eYACHO）、eyachoch6s（eYACHO Viewer）、gembanotech6（GEMBA Note）、gembanotech6s（GEMBA Note Viwer）
set APP_URI_SCHEME=gembanotech6
rem template_id: Update it with your note template
set NOTE_TEMPLATE_ID=https://mps-gd.metamoji.com/link/*****.mmjloc
rem folder_uri: Update it with your folder
set FOLDER_URI=https://mps-gd.metamoji.com/link/*****.mmjloc
rem note_new_uri
set NOTE_NEW_URI=http://127.0.0.1:8000/created_note
rem CSV file for multiple notes
set CSV_FILE=csv/propertyList.csv
rem set CSV_FILE=csv/propertyList_ja.csv
rem recordset_uri
set RECORDSET_URI=http://127.0.0.1:8000/recordset
rem page_template_id: Update it with your page template
set PAGE_TEMPLATE_ID=https://mps-gd.metamoji.com/link/*****.mmjloc
rem tag_namespace: Update it with your tag scheme
set TAG_NAMESPACE=com.metamoji.package.gemba.*****.*****
rem ----- END OF FILE -----