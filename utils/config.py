#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] config.py
# [DESCRIPTION] 
#  [EN] Setting configuration by referring to environment variables
#  [JA] 環境変数を取得し、変数に設定する
#
# [HISTORY]
# [1] 2026-08-31: First release

# --- Standard Libraries / 標準ライブラリ ---
import os

# --- Third-Party Libraries / サードパーティライブラリ ---
from dotenv import load_dotenv

# [EN] Load .env file
# [JA] .envファイルを読み込む
load_dotenv()

# [EN] Constants / 定数
# [JA] 定数設定
ACCESS_ID = os.environ.get('ACCESS_ID')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
APP_LANG = os.environ.get('APP_LANG')
APP_URI_SCHEME = os.environ.get('APP_URI_SCHEME')
CSV_FILE = os.environ.get('CSV_FILE')
IMAGE_FOLDER = os.environ.get('IMAGE_FOLDER')
PDF_FOLDER = os.environ.get('PDF_FOLDER')
PROFILES_FILE = os.environ.get('PROFILES_FILE')

def print_config():
    """
    [EN] Print loaded environment variables for debugging purposes.
         Called from main.py when in development mode.
    [JA] デバッグ目的で読み込んだ環境変数を出力します。
         開発モード時に main.py から呼び出されます。
    """
    print("=== Configuration Variables ===")
    print(f"ACCESS_ID: {ACCESS_ID}")
    
    # [EN] Mask the token for security
    # [JA] セキュリティのためトークンをマスク処理
    masked_token = "***MASKED***" if ACCESS_TOKEN else "None"
    print(f"ACCESS_TOKEN: {masked_token}")
    
    print(f"APP_LANG: {APP_LANG}")
    print(f"APP_URI_SCHEME: {APP_URI_SCHEME}")
    print(f"CSV_FILE: {CSV_FILE}")
    print(f"IMAGE_FOLDER: {IMAGE_FOLDER}")
    print(f"PDF_FOLDER: {PDF_FOLDER}")
    print(f"PROFILES_FILE: {PROFILES_FILE}")
    print("===============================")
  