# cuscheme-property-manager

[[英語版](./README.md)]

## カスタムURLスキーマによるサンプルWebアプリケーション

このサーバーは、株式会社MetaMoJiのデジタルノート製品 eYACHO / GEMBA Noteが提供するカスタムURLスキーマを利用して、不動産管理向けノートを生成するためのエンドポイントを提供する。

このバージョンはPython ＋ FastAPIで実装されている。

### Pythonをインストールする

[https://www.python.org/downloads/](https://www.python.org/downloads/)からPythonをインストールする。

### 必要なパッケージのインストール

コマンドプロンプト上で、次のコマンドを実行し、必要なPythonのパッケージをインストールする。

```bash
pip install -r requirements.txt
```

### 環境変数の設定

環境変数はファイル env.batあるいはenv.shに定義する。環境に応じてどちらかのファイルにノートテンプレート、ページテンプレート、保存フォルダ、対象タグスキーマを設定する。これらの変数の値を取得する方法は後ほど述べる。  

コマンドプロンプトからバッチファイルあるいはシェルファイルを実行し、環境変数を設定する。

Windows環境:

```bash
env.bat
```

Linux環境:

```bash
env.sh
```

### サーバーを起動する

コマンドプロンプトから次のコマンドを実行し、サーバーを起動する。

開発版:

```bash
uvicorn main:app --reload 
```

本番環境:

```bash
uvicorn main:app
```

### サーバーへアクセスする

Webブラウザを開き、次のURLへアクセスする。

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

トップページが現れる。

![図1: トップページ][img1]

- 1つのページを生成
  - 1つのノートを新規に作成し、その中に物件フォーム1枚を作成する
- 複数のページを生成
  - 1つのノートを新規に作成し、CSVファイル ([csv/propertyList_ja.csv](csv/propertyList_ja.csv))から複数の物件フォームを作成する

[img1]: ./image/top_page-ja.png

### eYACHO/GEMBA Noteバックアップファイル

| ファイル名 | 説明 |
| ----- | ----- |
| [PropertyManagementMaster__1.0.1__backup.gncproj](https://product.metamoji.com/manual/gemba_apps/gemba_dev_basic/jp/dev_kit/backup/PropertyManagementMaster__1.0.1__backup.gncproj) | 不動産管理パッケージのバックアップファイル |

### カスタムURLスキームに必要なパラメータ

| パラメータ名 | 環境変数名 | 説明  |
| ---- | ---- | ---- |
| - | APP_LANG | 使用する言語 en - 英語, ja - 日本語 |
| - | APP_URI_SCHEME | どのアプリを起動するか、そのURIスキーム |
| access_id | - | アクセストークンとなるキーを設定する |
| access_token  | - | eYACHO / GEMBA Noteへアクセスするトークン |
| template_id | NOTE_TEMPLATE_ID | 対象となるノートテンプレートID |
| folder_uri  | FOLDER_URI | 作成するノートを保存するフォルダURI |
| internal_id | - | サーバーでの内部ID |
| note_new_uri | NOTE_NEW_URI | 作成されたノート情報を返すエンドポイント（POSTメソッド） |
| - | CSV_FILE | 複数ページを作成するCSVファイル |
| recordset_uri | RECORDSET_URI | 対象となるレコードを収集するエンドポイント（GETメソッド）|
| page_template_id | PAGE_TEMPLATE_ID | 対象となるページテンプレートID |
| tag_namespace | TAG_NAMESPACE | 対象となるタグスキーマの名前空間 |

#### ノートテンプレートIDを取得する

新規に作成するノートのひな型になるテンプレートは、template_idパラメータに指定する。
そのIDは次の手順で取得する。

- **新規ノート作成**ボタンをクリックする
- **ノートテンプレート**タブに切り替える
- 対象テンプレート上で右クリックあるいは長押しする
- **テンプレート情報**を選択する
- URLが見つかるのでコピーして環境変数へ設定する

![図2: ノートテンプレートIDの取得][img2]

[img2]: ./image/note_template_id-ja.png

#### ノートを保存するフォルダを取得する

作成したノートを保存するフォルダをfolder_uriパラメータに指定する。
このURIを取得するため、対象フォルダーを右クリックあるいは長押しし、コンテキストメニューの中から **URL** を選択する。

![図3: フォルダURIを取得][img3]

[img3]: ./image/folder_url-ja.png

#### ページテンプレートIDを取得する

作成するノートに追加するページのひな型となるテンプレートは、page_template_idパラメータに指定する。そのIDは次の手順で取得する。

- **新規ノート作成**ボタンをクリックする
- **用紙テンプレート**タブに切り替える
- 対象テンプレート上で右クリックあるいは長押しする
- **テンプレート情報**を選択する
- You can find the URL

![図4: ページテンプレートIDの取得][img4]

[img4]: ./image/page_template_id-ja.png

#### タグスキーマの名前空間を取得する

ページ生成時に対象となるタグスキーマの名前空間は、tag_namespaceパラメータに指定する。
それを取得手順は次の通りである。

- 対象の開発パッケージ上で右クリックあるいは長押しする
- コンテキストメニューの中から**操作** > **タグスキーマ一覧**を選択する
- 「タグスキーマ一覧」ダイアログ上で対象のタグスキーマを選択する
- 「タグスキーマの編集」ダイアログ上で**タグID**を右クリックあるいは長押しする
- **クリップボードにコピー**を選択し、環境変数ファイル(env.bat or env.sh)の**TAG_NAMESPACE**に設定する

![図5: タグスキーマの名前空間の取得][img5]

[img5]: ./image/tag_namespace-ja.png

### 変更履歴

- 2024-09-24 - 環境変数APP_LANGとAPP_URI_SCHEMEを追加
- 2024-09-09 - 初回リリース
