# cuscheme-property-manager

[[English](./README_en.md)]

## カスタムURLスキーマによるサンプルWebアプリケーション

このサーバーは、株式会社MetaMoJiのデジタルノート製品 eYACHO / GEMBA Noteが提供するカスタムURLスキーマを利用して、不動産管理向けノートを生成するためのエンドポイントを提供する。

なお、このバージョンはPython、FastAPI、およびJinja2（テンプレートエンジン）で実装されている。

### Pythonをインストールする

[https://www.python.org/downloads/](https://www.python.org/downloads/)からPythonをインストールする。

### 必要なパッケージのインストール

コマンドプロンプト上で、次のコマンドを実行し、必要なPythonのパッケージをインストールする。

```bash
pip install -r requirements.txt
```

### バックアップファイルを復元する

不動産管理アプリのバックアップファイルをダウンロードし、eYACHO/GEMBA Noteに復元する。

| ファイル名 | 説明 |
| ----- | ----- |
| [PropertyManagementMaster__1.0.3__backup.gncproj](https://product.metamoji.com/manual/gemba_apps/gemba_dev_basic/jp/dev_kit/backup/PropertyManagementMaster__1.0.3__backup.gncproj) | 不動産管理パッケージのバックアップファイル |

### 環境変数を設定する

日本語環境設定ファイルのテンプレートとして **.env_jp** があるので、ノートテンプレートID (NOTE_TEMPLATE_ID)、ページテンプレートID (PAGE_TEMPLATE_ID)、保存するフォルダ (FOLDER_URI)、対象タグスキーマの名前空間 (TAG_NAMESPACE)を設定する。
このファイルを **.env** に名称変更する。

#### カスタムURLスキーマのパラメータと環境変数の関係

本PythonプログラムからカスタムURL起動に必要とするパラメータへの値は環境変数を通して与える。

| パラメータ名 | 環境変数名 | 説明  |
| ---- | ---- | ---- |
| - | APP_LANG | 使用する言語 en - 英語, ja - 日本語 |
| - | APP_URI_SCHEME | どのアプリを起動するか、そのURIスキーム |
| access_id | - | アクセストークンとなるキーを設定する |
| access_token  | - | eYACHO / GEMBA Noteへアクセスするトークン |
| template_id | NOTE_TEMPLATE_ID | 対象となるノートテンプレートID |
| page_template_id | PAGE_TEMPLATE_ID | 対象となるページテンプレートID |
| folder_uri  | FOLDER_URI | 作成するノートを保存するフォルダURI |
| tag_namespace | TAG_NAMESPACE | 対象となるタグスキーマの名前空間 |
| internal_id | - | サーバーでの内部ID |
| note_new_uri | NOTE_NEW_URI | 作成されたノート情報を返すエンドポイント（POSTメソッド） |
| - | CSV_FILE | 複数ページを作成するCSVファイル |
| recordset_uri | RECORDSET_URI | 対象となるレコードを収集するエンドポイント（GETメソッド）|

template_id、page_template_id、folder_uri、そしてtag_namespaceへ設定する値は、不動産管理開発パッケージ上で、以下の手順で取得する。

#### ノートテンプレートIDを取得する

新規に作成するノートのひな型になるテンプレートは、template_idパラメータに指定する。
そのIDは次の手順で取得する。

- **新規ノート作成**ボタンをクリックする
- **ノートテンプレート**タブに切り替える
- 対象テンプレート上で右クリックあるいは長押しする
- **テンプレート情報**を選択する
- URLが見つかるのでコピーして環境変数**NOTE_TEMPLATE_ID**へ設定する

![図1: ノートテンプレートIDの取得][img1]

[img1]: ./image/note_template_id-ja.png

#### ページテンプレートIDを取得する

作成するノートに追加するページのひな型となるテンプレートは、page_template_idパラメータに指定する。そのIDは次の手順で取得する。

- **新規ノート作成**ボタンをクリックする
- **用紙テンプレート**タブに切り替える
- 対象テンプレート上で右クリックあるいは長押しする
- **テンプレート情報**を選択する
- URLが見つかるのでコピーして環境変数**PAGE_TEMPLATE_ID**へ設定する

![図2: ページテンプレートIDの取得][img2]

[img2]: ./image/page_template_id-ja.png

#### ノートを保存するフォルダを取得する

作成したノートを保存するフォルダをfolder_uriパラメータに指定する。
このURIを取得するため、対象フォルダーを右クリックあるいは長押しし、コンテキストメニューの中から **URL** を選択する。

![図3: フォルダURIを取得][img3]

[img3]: ./image/folder_url-ja.png

#### タグスキーマの名前空間を取得する

ページ生成時に対象となるタグスキーマの名前空間は、tag_namespaceパラメータに指定する。
それを取得手順は次の通りである。

- 対象の開発パッケージ上で右クリックあるいは長押しする
- コンテキストメニューの中から**操作** > **タグスキーマ一覧**を選択する
- 「タグスキーマ一覧」ダイアログ上で対象のタグスキーマを選択する
- 「タグスキーマの編集」ダイアログ上で**タグID**を右クリックあるいは長押しする
- **クリップボードにコピー**を選択し、環境変数**TAG_NAMESPACE**に設定する

![図4: タグスキーマの名前空間の取得][img4]

[img4]: ./image/tag_namespace-ja.png

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

| コマンドの要素 |  説明  |
| ---- | ---- |
|  uvicorn  | FastAPIベースの非同期Python Webアプリケーションを実行する |
|  main:app  | Pythonファイルmain.pyの中で、FastAPIが生成する変数がapp |
|  --reload  | 実行中にソースコードが変更されたとき、サーバーが自動的にリロードされる |

デフォルトのポート番号は**8000**。  
ポート番号を指定するときは **--port [ポート番号]** を後ろに付与する。

### サーバーへアクセスする

Webブラウザを開き、次のURLへアクセスする。

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

サーバー起動直後の初期状態では、2つのリンク項目を含んだトップページが現れる。

![図5: トップページ][img5]

[img5]: ./image/top_page-ja.png

- 1つのページを生成
  - 1つのノートを新規に作成し、その中に物件ページ1枚を作成する。
  - 物件情報を記入して「作成」ボタンをクリックする。
  - 指定したeYACHO/GEMBA Noteが開き、生成が開始する。
  ![図6: 1ページノートを生成][img6]
- 複数のページを生成
  - 1つのノートを新規に作成し、CSVファイル ([csv/propertyList_ja.csv](csv/propertyList_ja.csv))から複数の物件ページを作成する。
  - リンク「クリックすると…」をクリックする。
  - 指定したeYACHO/GEMBA Noteが開き、が開始する。
  ![図7: 複数ページノートを生成][img7]

[img6]: ./image/single_property_page-ja.png

[img7]: ./image/multi_property_page-ja.png

上2つのどちらかを実行してノートが生成された場合に次のリンクが有効となる。

- 最後に生成したノートを開く
  - 「開く」ボタンをクリックすると、表示されているノートIDを開く。

### 注意事項

このサーバーはあくまでもサンプルであり、複数ユーザーアクセス向けには設計されていない。

### 変更履歴

- 2025-04-22 - 環境変数.envを参照、「最後に生成したノートを開く」を追加
- 2025-03-03 - バックアップファイルを1.0.1から1.0.3へ更新
- 2024-09-24 - 環境変数APP_LANGとAPP_URI_SCHEMEを追加
- 2024-09-09 - 初回リリース
