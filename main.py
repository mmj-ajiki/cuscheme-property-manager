#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] main.py
#
# [DESCRIPTION]
#  [EN] Sample Server for generating notes using the Custom URL Scheme in eYACHO/GEMBA Note.
#  [JA] eYACHO/GEMBA NoteのカスタムURLスキームを使用してノートを生成するためのサンプルサーバー。
#
# [HISTORY]
# [3] 2026-08-31: Added media feature
# [2] 2026-04-21: Fixed TemplateResponse() due to the Starlette change
# [1] 2024-09-09: Initial version
#

# --- Standard Libraries / 標準ライブラリ ---
import base64
import csv
from datetime import datetime
import json
import mimetypes
import os
import shutil
import sys
from typing import List
import urllib.parse

# --- Third-Party Libraries / サードパーティライブラリ ---
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# --- Local (Application) Libraries / ローカル（アプリケーション）ライブラリ ---
from utils.config import (
    ACCESS_ID,
    ACCESS_TOKEN,
    APP_LANG,
    APP_URI_SCHEME,
    CSV_FILE,
    IMAGE_FOLDER,
    PDF_FOLDER,
    PROFILES_FILE,
    print_config,
)

app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# [EN] Global variable to store the last created note ID
# [JA] 最後に作成されたノートIDを保持するグローバル変数
_last_note_id = None

# [EN] Flag for development option
# [JA] 開発用オプションの判定フラグ
is_dev = "--reload" in sys.argv

# [EN] Print config variables if running in development mode
# [JA] 開発モードで実行されている場合、設定値を出力する
if is_dev:
    print_config()

# [EN] Load the profile configuration at startup
# [JA] サーバー起動時にプロファイル設定ファイルを読み込む
PROFILES = {}
try:
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            PROFILES = json.load(f)
        print(f"[INFO] Successfully loaded {PROFILES_FILE} / プロファイル設定を読み込みました")
    else:
        print(f"[WARNING] {PROFILES_FILE} not found. / プロファイル設定ファイルが見つかりません")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Failed to load {PROFILES_FILE}: {e}")
    sys.exit(1)


@app.get("/", response_class=HTMLResponse)
async def top_page(request: Request):
    """
    [EN] Display the top page. Switches the HTML template based on the 'APP_LANG' environment variable.
    [JA] トップページの表示。環境変数 'APP_LANG' に応じて表示するHTMLテンプレートを切り替えます。
    """
    target_page = "error.html"
    title = "Property Management Web App"

    if APP_LANG is not None:
        target_page = f"index_{APP_LANG}.html"
    else:
        print("[ERROR] Environment variables are missing / 環境変数が設定されていません")

    if APP_LANG == "ja":
        title = "不動産管理アプリ"

    return templates.TemplateResponse(
        name=target_page,
        context={"request": request, "title": title, "note_id": _last_note_id},
        request=request,
    )


@app.get("/single", response_class=HTMLResponse)
async def create_single_note(request: Request, type: str = "property"):
    """
    [EN] Generate URL parameters for creating a single-page note and pass them to the template.
    [JA] 単一ページのノート作成用URLパラメータを生成し、テンプレートに渡します。
    """
    internal_id = '123456789'

    # [EN] Find the profile to be used
    # [JA] 利用するプロファイルを探す
    profile = PROFILES.get(type, PROFILES["property"])
    
    # [EN] Construct highly readable parameter strings using f-strings
    # [JA] f-stringsを使用して可読性の高いパラメータ文字列を構築
    para = (
        f"?access_id={ACCESS_ID}&access_token={ACCESS_TOKEN}"
        f"&template_id={urllib.parse.quote(profile["template_id"])}"
        f"&folder_uri={urllib.parse.quote(profile["folder_uri"])}"
        f"&internal_id={internal_id}"
        f"&note_new_uri={urllib.parse.quote(profile["note_new_uri"])}"
    )

    target_page = f"property_{APP_LANG}.html" if APP_LANG is not None else "error.html"

    return templates.TemplateResponse(
        name=target_page,
        context={"request": request, "protocol": APP_URI_SCHEME, "parameters": para},
        request=request,
    )


@app.get("/multiple")
async def create_multiple_notes(request: Request, type: str = "property"):
    """
    [EN] Generate the URL for creating multiple-page notes and pass it to the template.
    [JA] 複数ページのノート作成用URLを生成し、テンプレートに渡します。
    """
    internal_id = '987654321'

    # [EN] Find the profile to be used
    # [JA] 利用するプロファイルを探す
    profile = PROFILES.get(type, PROFILES["property"])

    url = (
        f"{APP_URI_SCHEME}:///nsk/new?"
        f"access_id={ACCESS_ID}&access_token={ACCESS_TOKEN}"
        f"&template_id={urllib.parse.quote(profile["template_id"])}"
        f"&folder_uri={urllib.parse.quote(profile["folder_uri"])}"
        f"&internal_id={internal_id}"
        f"&note_new_uri={urllib.parse.quote(profile["note_new_uri"])}"
        f"&recordset_uri={urllib.parse.quote(profile["recordset_uri"])}"
        f"&page_template_id={urllib.parse.quote(profile["page_template_id"])}"
        f"&tag_namespace={urllib.parse.quote(profile["tag_namespace"])}"
    )

    target_page = f"multiple_{APP_LANG}.html" if APP_LANG is not None else "error.html"

    return templates.TemplateResponse(
        name=target_page,
        context={"request": request, "url": url},
        request=request,
    )


@app.get("/media", response_class=HTMLResponse)
async def create_media_note(request: Request, type: str = "property_media"):
    """
    [EN] Generate parameters for creating a single-page note including an image and a PDF.
    [JA] 画像とPDFを含む単一ページのノート作成用パラメータを生成します。
    """
    internal_id = '123454321'

    # [EN] Find the profile to be used
    # [JA] 利用するプロファイルを探す
    profile = PROFILES.get(type, PROFILES["property_media"])
    
    para = (
        f"?access_id={ACCESS_ID}&access_token={ACCESS_TOKEN}"
        f"&template_id={urllib.parse.quote(profile["template_id"])}"
        f"&folder_uri={urllib.parse.quote(profile["folder_uri"])}"
        f"&internal_id={internal_id}"
        f"&note_new_uri={urllib.parse.quote(profile["note_new_uri"])}"
        f"&page_template_id={urllib.parse.quote(profile["page_template_id"])}"
        f"&tag_namespace={urllib.parse.quote(profile["tag_namespace"])}"
    )
    recordset_uri_quoted = urllib.parse.quote(profile["recordset_uri"])
    target_page = f"media_{APP_LANG}.html" if APP_LANG is not None else "error.html"

    return templates.TemplateResponse(
        name=target_page,
        context={
            "request": request,
            "protocol": APP_URI_SCHEME,
            "parameters": para,
            "recordset_uri": recordset_uri_quoted
        },
        request=request,
    )


@app.get("/open", response_class=HTMLResponse)
async def open_last_note(request: Request):
    """
    [EN] Generate URL parameters to open the last created note.
    [JA] 最後に作成したノートを開くためのURLパラメータを生成します。
    """
    para = f"?access_id={ACCESS_ID}&access_token={ACCESS_TOKEN}"
    
    if _last_note_id is not None:
        para += f"&note_uri={urllib.parse.quote(_last_note_id)}"

    target_page = f"open_{APP_LANG}.html" if APP_LANG is not None else "error.html"

    return templates.TemplateResponse(
        name=target_page,
        context={"request": request, "protocol": APP_URI_SCHEME, "parameters": para, "note_id": _last_note_id},
        request=request,
    )


@app.post("/created_note")
async def get_note(request: Request):
    """
    [EN] Receive the created note information sent from the client and save it in a global variable.
    [JA] クライアントから送信された作成済みノート情報を受け取り、グローバル変数に保存します。
    """
    global _last_note_id

    try:
        results = await request.json()
    except Exception as e:
        # [EN] Exception handling for invalid JSON format
        # [JA] 不正なJSONデータが送られてきた場合の例外処理
        raise HTTPException(status_code=400, detail="Invalid JSON format") from e

    if is_dev:
        print("[Created Note]", results)
        
    if results and isinstance(results, list) and len(results) > 0:
        # [EN] Safely retrieve assuming the list element is a dictionary
        # [JA] リストの要素が辞書であることを前提に安全に取得
        _last_note_id = results[0].get('noteid')
        
    return results


@app.get("/recordset")
def get_record_set():
    """
    [EN] Read the CSV file and return the recordset of properties as a JSON list.
    [JA] CSVファイルを読み込み、プロパティのレコードセットをJSONリストとして返します。
    """
    output = []
    skip = True
    
    try:
        with open(CSV_FILE, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if not skip:
                    # [EN] Prevent IndexError due to rows with missing columns
                    # [JA] カラム数が不足している行によるIndexErrorを防ぐ
                    if len(row) >= 4:
                        json_data = {'Name': row[0], 'Type': row[1], 'Price': row[2], 'Address': row[3]}
                        output.append(json_data)
                    else:
                        print(f"[WARNING] Skipping invalid row: {row} / 不正な行をスキップしました")
                else:
                    skip = False # [EN] Skip the first row (header) / [JA] 最初の行（ヘッダー）をスキップ
    except FileNotFoundError:
        # [EN] Exception handling if the file does not exist
        # [JA] ファイルが存在しない場合の例外処理
        raise HTTPException(status_code=404, detail="CSV file not found")
    except Exception as e:
        # [EN] Exception handling for other reading errors
        # [JA] その他の読み込みエラー時の例外処理
        raise HTTPException(status_code=500, detail=f"Error reading CSV file: {str(e)}")
        
    if is_dev:
        print("[RECORDSET]", output)

    return output


@app.get("/recordset_media")
def recordset_media(request: Request):
    """
    [EN] Get image and PDF paths from request parameters, encode them in Base64, and return them.
    [JA] リクエストパラメータから画像・PDFのパスを取得し、Base64エンコードして返します。
    """
    output = []
    
    # [EN] Retrieve query parameter (Changed variable name from 'input' to avoid shadowing built-in function)
    # [JA] 組み込み関数の上書きを防ぐため、変数名を input から query_data に変更
    query_data = request.query_params.get("data")
    if not query_data:
        raise HTTPException(status_code=400, detail="Query parameter 'data' is missing")
        
    if is_dev:
        print("[RECORDSET MEDIA]", query_data)
    
    array = query_data.split(",")
    if len(array) < 3:
        raise HTTPException(status_code=400, detail="Invalid data format. Expected: Name,Image,PDF")
        
    p_name = array[0]
    image_file_path = array[1].strip('"')
    pdf_file_path = array[2].strip('"')

    # [EN] Exception handling for reading and encoding the image file
    # [JA] 画像ファイルの読み込みとエンコードの例外処理
    try:
        image_mime_type, _ = mimetypes.guess_type(image_file_path)
        image_mime_type = image_mime_type or "application/octet-stream"
        
        with open(image_file_path, "rb") as fp:
            image_encoded = base64.b64encode(fp.read()).decode("utf-8")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Image file not found: {image_file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading image: {str(e)}")

    # [EN] Exception handling for reading and encoding the PDF file
    # [JA] PDFファイルの読み込みとエンコードの例外処理
    try:
        pdf_mime_type, _ = mimetypes.guess_type(pdf_file_path)
        pdf_mime_type = pdf_mime_type or "application/pdf"
        
        with open(pdf_file_path, "rb") as fp:
            pdf_encoded = base64.b64encode(fp.read()).decode("utf-8")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"PDF file not found: {pdf_file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

    image_base64 = f"data:{image_mime_type};base64,{image_encoded}"
    pdf_base64   = f"data:{pdf_mime_type};base64,{pdf_encoded}"
    
    json_data = {'name': p_name, 'photo': image_base64, 'pdf': pdf_base64}
    output.append(json_data)

    return output


@app.post("/upload_media")
async def upload(files: List[UploadFile] = File(...)):
    """
    [EN] Save uploaded image and PDF files to the specified local folders.
    [JA] アップロードされた画像やPDFファイルをローカルの指定フォルダに保存します。
    """
    saved_files = []
    
    # [EN] Create folders if they do not exist (Prevents FileNotFoundError)
    # [JA] フォルダが存在しない場合は作成する（FileNotFoundErrorの防止）
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    os.makedirs(PDF_FOLDER, exist_ok=True)

    for file in files:
        if file.content_type and file.content_type.startswith("image/"):
            save_dir = IMAGE_FOLDER
        elif file.content_type == "application/pdf":
            save_dir = PDF_FOLDER
        else:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not an image or PDF. / 画像またはPDFではありません。"
            )

        time_str = datetime.now().strftime("%Y%m%d%H%M%S%f")
        file_name = f"{time_str}-{file.filename}"
        save_path = os.path.join(save_dir, file_name)

        try:
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except IOError as e:
            raise HTTPException(status_code=500, detail=f"Failed to save {file.filename}: {str(e)}")

        saved_file = os.path.join(save_dir, file_name)
        saved_files.append(saved_file)

    if is_dev:
        print("[SAVED FILES]", saved_files)
        
    return saved_files
