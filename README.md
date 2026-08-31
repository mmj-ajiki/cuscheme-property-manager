# cuscheme-property-manager

[[English](./README_en.md)]

## カスタムURLスキームによるサンプルWebアプリケーション

このサーバーは、株式会社MetaMoJiのデジタルノート製品 eYACHO / GEMBA Noteが提供するカスタムURLスキームを利用して、不動産管理向けノートを生成するためのエンドポイントを提供する。

なお、このバージョンはPython、FastAPI、およびJinja2（テンプレートエンジン）で実装されている。

### Pythonをインストールする

[https://www.python.org/downloads/](https://www.python.org/downloads/)からPythonをインストールする。

### 必要なパッケージのインストール

コマンドプロンプト上で、次のコマンドを実行し、必要なPythonのパッケージをインストールする。

```bash
pip install -r requirements.txt
```

### バックアップファイルを復元する

アプリ開発実践編のバックアップファイルをダウンロードし、eYACHO/GEMBA Noteに復元する。

| ファイル名 | 説明 |
| ----- | ----- |
| [PracticalAppDev__0.2.4__backup.gncproj](https://product.metamoji.com/manual/gemba_apps/gemba_dev_advanced/jp/contents/backup/PracticalAppDev__0.2.4__backup.gncproj) | アプリ開発実践編のバックアップファイル |

### 環境変数を設定する

日本語環境設定ファイルのテンプレートとして **env_ja.tpl** があるので、各変数に適切な値をを設定する。
このファイルを **.env** に名称変更する。

| 環境変数名 | 説明 |
| ---- | ---- |
| ACCESS_ID | アクセストークンとなるキーを設定する |
| ACCESS_TOKEN | eYACHO / GEMBA Noteへアクセスするトークン |
| APP_LANG | 使用する言語 en - 英語, ja - 日本語 |
| APP_URI_SCHEME | どのアプリを起動するか、そのURIスキーム |
| CSV_FILE | 複数ページを作成するCSVファイル |
| IMAGE_FOLDER | 画像ファイルを一時的に保存するフォルダ |
| PDF_FOLDER | PDFファイルを一時的に保存するフォルダ |
| PROFILES_FILE | プロファイル設定ファイル |

### プロファイルを設定する

カスタムURL起動に必要とするパラメータへの値はプロファイル設定ファイル（utils/profiles_<言語>.json）から、利用する環境に合わせて値を設定する。
ちなみに初期設定では、**property**と**property_media**の2つの環境を定義し、通常の不動産物件フォームと不動産物件画像フォームの異なる2つの帳票を扱うことを前提としている。

**profiles_ja.jsonの例：**  

```json
{
  "property": {
    "template_id": "https://mps.metamoji.com/link/N8xGqjVWr2Dm7KcLpY4sTbZh.mmjloc",
    "page_template_id": "https://mps.metamoji.com/link/Q3mRkXv9HtCp6JnBwL5dFsYa.mmjloc",
    "tag_namespace": "com.metamoji.package.gemba.7A91E5F4-3D2C-4B8A-9F17-6C2E4D8A91B3.Property",
    "folder_uri": "https://mps.metamoji.com/link/Y2dLpWm6HxKq9TrVcN4gFjZb.mmjloc",
    "note_new_uri": "http://localhost:8000/created_note",
    "recordset_uri": "http://localhost:8000/recordset"
  },
  "property_media": {
    "template_id": "https://mps.metamoji.com/link/Z7pNcTg4VmKx2QrHbD8jWyLf.mmjloc",
    "page_template_id": "https://mps.metamoji.com/link/M5hKvQx8RpTn3GcZjW7dBySa.mmjloc",
    "tag_namespace": "com.metamoji.package.gemba.C8F2A7D1-5E4B-43C9-B2A6-1D7F9E3C5A84.propertyPhoto",
    "folder_uri": "https://mps.metamoji.com/link/Y2dLpWm6HxKq9TrVcN4gFjZb.mmjloc",
    "note_new_uri": "http://localhost:8000/created_note",
    "recordset_uri": "http://localhost:8000/recordset_media"
  }
}
```

各キーの説明は次の通り。

| キー | 説明 |
| ---- | ---- |
| template_id | 対象となるノートテンプレートID |
| page_template_id | 対象となるページテンプレートID |
| tag_namespace | 対象となるタグスキーマの名前空間 |
| folder_uri | 作成するノートを保存するフォルダURI |
| note_new_uri | 作成されたノート情報を返すエンドポイント（POSTメソッド） |
| recordset_uri | 対象となるレコードを収集するエンドポイント（GETメソッド） |

template_id、page_template_id、folder_uri、そしてtag_namespaceへ設定する値は、開発パッケージ上で、以下の手順で取得する。

#### ノートテンプレートIDを取得する

新規に作成するノートのひな型になるテンプレートは、template_idキーに指定する。
そのIDは次の手順で取得する。

- **新規ノート作成**ボタンをクリックする。
- **ノートテンプレート**タブに切り替える。
- 対象テンプレート上で右クリックあるいは長押しする。
- **テンプレート情報**を選択する。
- URLが見つかるのでコピーして **template_id** キーの値として設定する。

![図1: ノートテンプレートIDの取得][img1]

[img1]: ./image/note_template_id-ja.png

#### ページテンプレートIDを取得する

作成するノートに追加するページのひな型となるテンプレートは、page_template_idキーに指定する。

- **新規ノート作成**ボタンをクリックする。
- **用紙テンプレート**タブに切り替える。
- 対象テンプレート上で右クリックあるいは長押しする。
- **テンプレート情報**を選択する。
- URLが見つかるのでコピーして **page_template_id** キーの値として設定する。

![図2: ページテンプレートIDの取得][img2]

[img2]: ./image/page_template_id-ja.png

#### ノートを保存するフォルダを取得する

作成したノートを保存するフォルダを **folder_uri** キーに指定する。
このURIを取得するため、対象フォルダーを右クリックあるいは長押しし、コンテキストメニューの中から **URL** を選択する。

![図3: フォルダURIを取得][img3]

[img3]: ./image/folder_url-ja.png

#### タグスキーマの名前空間を取得する

ページ生成時に対象となるタグスキーマの名前空間は、tag_namespaceキーに指定する。

- 対象の開発パッケージ上で右クリックあるいは長押しする。
- コンテキストメニューの中から**操作** > **タグスキーマ一覧**を選択する。
- 「タグスキーマ一覧」ダイアログ上で対象のタグスキーマを選択する。
- 「タグスキーマの編集」ダイアログ上で**タグID**を右クリックあるいは長押しする。
- **クリップボードにコピー**を選択し、**tag_namespace** キーの値として設定する。

![図4: タグスキーマの名前空間の取得][img4]

[img4]: ./image/tag_namespace-ja.png

#### 取得するプロファイル情報

次の節から述べるサンプルを動作確認するため、バックアップファイルから復元した開発パッケージから以下の情報を取得する。

**トップページ項目とプロファイル取得パターン**  

| トップページ項目（リンク） | プロファイル取得パターン |
| --- | --- |
| 1つのページを生成 | パターン1 |
| 複数のページを生成 | パターン1 |
| 画像とPDFからページを生成 | パターン2 |

**プロファイル取得パターン１**  

| 取得する項目 | 取得する箇所 |
| --- | --- |
| ノートテンプレートID | ノート作成 > ノートテンプレート > 物件フォーム |
| ページテンプレートID | ノート作成 > ページテンプレート > 物件フォーム |
| ノートを保存するフォルダ | 適当な個人フォルダ、チームフォルダを決めてURLを取得する |
| タグスキーマの名前空間 | タグスキーマ一覧から「物件」を選択する |

プロファイル設定ファイル（環境変数 PROFILES_FILE が指定するJSONファイル）の **property** キー以下の該当するキーの値として設定する。

**プロファイル取得パターン２**  

| 取得する項目 | 取得する箇所 |
| --- | --- |
| ノートテンプレートID | [Create Note] > ノートテンプレート > 物件画像フォーム |
| ページテンプレートID | [Create Note] > ページテンプレート > 物件画像フォーム |
| ノートを保存するフォルダ | 適当な個人フォルダ、チームフォルダを決めてURLを取得する（パターン1と同じでもよい） |
| タグスキーマの名前空間 | タグスキーマ一覧から「物件画像」を選択する |

プロファイル設定ファイル（環境変数 PROFILES_FILE が指定するJSONファイル）の **property_media** キー以下の該当するキーの値として設定する。

### サーバーを起動する

コマンドプロンプトから次のコマンドを実行し、サーバーを起動する。

開発・デバッグ環境：

ソースコード編集内容が自動的に反映される。また、処理途中のログをコンソールに出力する。

```bash
uvicorn main:app --reload
```

本番環境：

```bash
uvicorn main:app
```

コマンドの説明:

| コマンドの要素 | 説明 |
| ---- | ---- |
| uvicorn | FastAPIベースの非同期Python Webアプリケーションを実行する |
| main:app | Pythonファイルmain.pyの中で、FastAPIが生成する変数がapp |
| --reload | 実行中にソースコードが変更されたとき、サーバーが自動的にリロードされる |

デフォルトのポート番号は**8000**。  
ポート番号を指定するときは **--port [ポート番号]** を後ろに付与する。

### サーバーへアクセスする

Webブラウザを開き、次のURLへアクセスする。

[http://localhost:8000/](http://localhost:8000/)

サーバー起動直後の初期状態では、2つのリンク項目を含んだトップページが現れる。

![図5: トップページ][img5]

[img5]: ./image/top_page-ja.png

- 1つのページを生成
  - 1つのノートを新規に作成し、その中に物件ページ1枚を作成する。
  - 物件情報を記入して「作成」ボタンをクリックする。
  - 指定したeYACHO/GEMBA Noteが開き、処理が開始する。
    - 処理の特徴：物件の属性(Name,Type,Price,Address)と属性値がカスタムURLに与えられる。
  ![図6: 1ページノートを生成][img6]
- 複数のページを生成
  - 1つのノートを新規に作成し、CSVファイル ([csv/propertyList_ja.csv](csv/propertyList_ja.csv))から複数の物件ページを作成する。
  - リンク「クリックすると…」をクリックする。
  - 指定したeYACHO/GEMBA Noteが開き、処理が開始する。
    - 処理の特徴：recordset_uriに指定したURIによる複数タグインスタンスの生成
  ![図7: 複数ページノートを生成][img7]
- 画像とPDFからページを生成
  - 画像とPDFを含む物件画像ページ1枚を作成する。
  - 物件名、画像ファイル、PDFファイルを指定して、「作成」ボタンをクリックする。
  - 指定したeYACHO/GEMBA Noteが開き、処理が開始する。
    - 処理の特徴：recordset_uriに指定したURIによる画像とPDFの処理
  ![図8: 物件画像・PDFページを生成][img8]

[img6]: ./image/single_property_page-ja.png
[img7]: ./image/multi_property_page-ja.png
[img8]: ./image/media_property_page-ja.png

上3つのどちらかを実行してノートが生成された場合に次のリンクが有効となる。

- 最後に生成したノートを開く
  - 「開く」ボタンをクリックすると、表示されているノートIDを開く。

### 注意事項

- このサーバーはあくまでもサンプルであり、複数ユーザーアクセス向けには設計されていない。
- アップロードした画像ファイルとPDFファイルは削除されないので、適宜削除する。
- .env ファイルはGitHubなどのバージョン管理システムにはコミットしない。
- 保存用フォルダ（IMAGE_FOLDERとPDF_FOLDER）は初回実行時に自動作成されるが、定期的に手動でクリーンアップする。
- 指定したファイル名によっては、認識できない場合がある。

### 変更履歴

- 2026-08-31 - 画像送信を追加、バックアップファイルをアプリ開発実践編のパッケージに変更
- 2026-04-21 - Starlette仕様変更に伴う改修、バックアップファイルを1.0.4へ更新
- 2025-10-23 - GEMBA Note V7に伴う更新
- 2025-04-22 - 環境変数.envを参照、「最後に生成したノートを開く」を追加
- 2025-03-03 - バックアップファイルを1.0.1から1.0.3へ更新
- 2024-09-24 - 環境変数APP_LANGとAPP_URI_SCHEMEを追加
- 2024-09-09 - 初回リリース
