# cuscheme-property-manager

[[Japanese](./README_ja.md)]

## Sample Web App based on Custom URL Scheme

This server provides endpoints that can generate property management forms using the Custom URL Scheme in GEMBA Note, a digital note product of MetaMoJi Corporation.

This version is implemented on Python and FastAPI.

### Installing Python

Referring to [https://www.python.org/downloads/](https://www.python.org/downloads/), install Python.

### Installing the Server

Using a command prompt, run the following command to instal dependent packages of Python.

```bash
pip install -r requirements.txt
```

### Setting the Environment Variables

Several environment variables are defined in env.bat or env.sh. Update either of files with your note template, page template, folder to store generated notes, and target tag scheme.
To get these values, please have a look at the section 'Custom URL Scheme Parameres' below.  

Using a command prompt, set the variables with the batch file or the shell file.

Windows:

```bash
env.bat
```

Linux:

```bash
env.sh
```

### Running the Server

Using a command prompt, run the following command to run the app.

For debug:

```bash
uvicorn main:app --reload 
```

For production:

```bash
uvicorn main:app
```

### Accessing the Server

Using a web browser, access to the following URL:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

You can get the top page as follows:

![Figure 1: Top Page][img1]

- Single Form Generation
  - Create a property form page in a new note
- Multiple Forms Generation
  - Create a set of property form pages in a new note by referring to a CSV file ([csv/propertyList.csv](csv/propertyList.csv))

When you click both links, you will be asked to open the GEMBA Note app.

[img1]: ./image/top_page.png

### GEMBA Note Backup File

| File name | Description |
| ----- | ----- |
| [PropertyManagementMaster__1.0.1__backup.gncproj](https://product.metamoji.com/manual/gemba_apps/gemba_dev_basic/en/dev_kit/backup/PropertyManagementMaster__1.0.1__backup.gncproj) | Backup file for the Property Management package |

### Custom URL Scheme Parameres

|  Parameter Name  | Environment Variable | Description  |
| ---- | ---- | ---- |
| - | APP_LANG | Language: en - English ja - Japanese |
| - | APP_URI_SCHEME | URI scheme to invoke GEMBA Note or GEMBA Note Viewer |
| access_id | - | Key for keeing the specified access token |
| access_token  | - | The token to access the GEMBA Note server |
| template_id | NOTE_TEMPLATE_ID | Target note template ID |
| folder_uri  | FOLDER_URI | Folder to store the created note |
| internal_id | - | ID internally used in the server |
| note_new_uri | NOTE_NEW_URI | Endpoint to get a URL of the created note |
| - | CSV_FILE | CSV file name to generate multiple pages |
| recordset_uri | RECORDSET_URI | Endpoint to get a recordset |
| page_template_id | PAGE_TEMPLATE_ID | Target page template ID |
| tag_namespace | TAG_NAMESPACE | Target tag namespace |

#### How to get a note template ID

The target note to be created is specified with the 'template_id' parameter.
To get this ID,

- Click on the **Create Note** button
- Select the **Note Template** tab
- Right-click or long-press on the target template
- Choose **Template Info**
- You can find the URL

![Figure 2: How to get a template ID][img2]

[img2]: ./image/note_template_id.png

#### How to get a folder URI

A created note is placed in the specified URL of the 'folder_uri' parameter.
To get the URI, right-click or long-press on the target folder and select **URL** in the context menu.

![Figure 3: How to get a folder URI][img3]

[img3]: ./image/folder_url.png

#### How to get a page template ID

The target page to be created is specified with the 'page_template_id' parameter.
To get this ID,

- Click on the **Create Note** button
- Select the **Paper Template** tab
- Right-click or long-press on the target template
- Choose **Template Info**
- You can find the URL

![Figure 4: How to get a page template ID][img4]

[img4]: ./image/page_template_id.png

#### How to get a tag namespace

The target tag namespace is referred to from the 'tag_namespace' parameter.
To get this namespace,

- Right-click or long-press on the target development package
- Select **More** > **Tag Schema List** from the context menu
- On the Tag Schema List dialog, select the target tag schema
- Right-click or long-press on the **Tag ID** on the Edit Tag Schema dialog
- Select **Copy to Clipboard** and paste it to **TAG_NAMESPACE** in the environment variable file (env.bat or env.sh)

![Figure 5: How to get a tag namespace][img5]

[img5]: ./image/tag_namespace.png

### Updated History

- SEP-24-2024 - Added APP_LANG and APP_URI_SCHEME
- SEP-09-2024 - First release
