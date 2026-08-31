# cuscheme-property-manager

[[Japanese](./README.md)]

## Sample Web App using Custom URL Scheme

This server provides endpoints to generate notes for property management using the custom URL scheme provided by MetaMoJi's digital note product, eYACHO / GEMBA Note.

Note that this version is implemented in Python, FastAPI, and Jinja2 (template engine).

### Installing Python

Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### Installing the Server

Execute the following command on the command prompt to install the required Python packages.

```bash
pip install -r requirements.txt
```

### GEMBA Note Backup File

Click the following link to download the backup file and restore the property management app in GEMBA Note.

| File name | Description |
| ----- | ----- |
| [PropertyManagementMaster__1.0.3__backup.gncproj](https://product.metamoji.com/manual/gemba_apps/gemba_dev_basic/en/dev_kit/backup/PropertyManagementMaster__1.0.3__backup.gncproj) | Backup file for the Property Management package |

### Setting Environment Variables

There is a template for the English environment configuration file named env_en.tpl. Set appropriate values for each variable.
Rename this file to **.env**.

| Environment Variable Name | Description |
| ---- | ---- |
| ACCESS_ID | Set the key that serves as the access token |
| ACCESS_TOKEN | Token to access eYACHO / GEMBA Note |
| APP_LANG | Language to use: en - English, ja - Japanese |
| APP_URI_SCHEME | The URI scheme of the app to launch |
| CSV_FILE | CSV file to create multiple pages |
| IMAGE_FOLDER | Folder to temporarily save image files |
| PDF_FOLDER | Folder to temporarily save PDF files |
| PROFILES_FILE | Profile configuration file |

### Setting Profiles

For the parameters required to launch via custom URL, set the values according to your environment from the profile configuration file (utils/profiles_< language >.json).
By default, two environments, **property** and **property_media**, are defined. This setup assumes handling two different forms: a standard property form and a property photo form.

**Sample of profiles_en.json:**  

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

The description of each key is as follows:

| Key | Description |
| ---- | ---- |
| template_id | Target note template ID |
| page_template_id | Target page template ID |
| tag_namespace | Target tag schema namespace |
| folder_uri | Folder URI to save the generated note |
| note_new_uri | Endpoint to return the generated note info (POST method) |
| recordset_uri | Endpoint to collect target records (GET method) |

Retrieve the values to be set for template_id, page_template_id, folder_uri, and tag_namespace on the development package using the following steps.

#### How to get a note template ID

Specify the template that will serve as the base for the newly created note in the **template_id** key.
Obtain this ID using the following steps:

- Click on the **Create Note** button.
- Select the **Note Template** tab.
- Right-click or long-press on the target template.
- Choose **Template Info**.
- Copy the found URL and set it as the value for the **template_id** key.

![Figure 1: How to get a template ID][img1]

[img1]: ./image/note_template_id.png

#### How to get a page template ID

Specify the template that will serve as the base for pages added to the generated note in the **page_template_id** key.

- Click on the **Create Note** button.
- Select the **Paper Template** tab.
- Right-click or long-press on the target template.
- Choose **Template Info**.
- Copy the found URL and set it as the value for the **page_template_id** key.

![Figure 2: How to get a page template ID][img2]

[img2]: ./image/page_template_id.png

#### How to get a folder URI

A created note is placed in the specified URL of the **folder_uri** key.
To get the URI, right-click or long-press on the target folder and select **URL** in the context menu. Then copy the URL and set it to **FOLDER_URI** in .env file.

![Figure 3: How to get a folder URI][img3]

[img3]: ./image/folder_url.png

#### How to get a tag namespace

The target tag namespace is referred to from the **tag_namespace** parameter.
To get this namespace,

- Right-click or long-press on the target development package.
- Select **More** > **Tag Schema List** from the context menu.
- On the Tag Schema List dialog, select the target tag schema.
- Right-click or long-press on the **Tag ID** on the Edit Tag Schema dialog.
- Select **Copy to Clipboard** and set it as the value for the **tag_namespace** key.

![Figure 4: How to get a tag namespace][img4]

[img4]: ./image/tag_namespace.png

#### Retrieving Profile Information

To verify the operation of the sample applications described in the following sections, retrieve the information below from the development package restored from the backup file.

**Top Page Items and Profile Patterns**  

| Top Page Item (Link) | Profile Pattern |
| --- | --- |
| Single Form Generation | Pattern 1 |
| Multiple Forms Generation | Pattern 1 |
| Generate a form with image and PDF | Pattern 2 |

**Profile Pattern 1**  

| Item to Retrieve | Location |
| --- | --- |
| Note Template ID | [Create Note] > Note Template > Property Form |
| Page Template ID | [Create Note] > Page Template > Property Sheet |
| Folder URI | Select an appropriate personal folder or team folder and obtain its URL |
| Tag Namespace | Select "Property" from the Tag Schema List |

Set these values in the corresponding keys under the **property** section of the profile configuration file (the JSON file specified by the PROFILES_FILE environment variable).

**Profile Pattern 2**  

| Item to Retrieve | Location |
| --- | --- |
| Note Template ID | [Create Note] > Note Template > Property Photo |
| Page Template ID | [Create Note] > Page Template > Property Photo Sheet |
| Folder URI | Select an appropriate personal folder or team folder and obtain its URL (the same folder as Pattern 1 may be used) |
| Tag Namespace | Select "Property Photo" from the Tag Schema List |

Set these values in the corresponding keys under the **property_media** section of the profile configuration file (the JSON file specified by the PROFILES_FILE environment variable).

### Starting the Server

Development/Debugging environment:

Changes to the source code are automatically applied. Logs during processing are output to the console.

```bash
uvicorn main:app --reload 
```

Production environment:

```bash
uvicorn main:app
```

| Command Element | Description |
| ---- | ---- |
| uvicorn | Runs the FastAPI-based asynchronous Python web application |
| main:app | In the main.py Python file, app is the variable generated by FastAPI |
| --reload | The server automatically reloads when the source code is modified during execution |

The default port number is **8000**.
To specify a port number, append **--port [Port Number]** at the end.

### Accessing the Server

Open a web browser and access the following URL:

[http://localhost:8000/](http://localhost:8000/)

You can get the top page as follows:

![Figure 5: Top Page][img5]

[img5]: ./image/top_page.png

- Single Form Generation
  - A note with a property form page is generated.
  - Click the "New" button.
  - The specified eYACHO/GEMBA Note will open, and generation will begin.
    - Implementation: Attributes and values of a property are directly given to the custom URL.
  ![Figure 6: Single Page Generation][img6]
- Multiple Forms Generation
  - A set of property form pages are generated by referring to a CSV file ([csv/propertyList_en.csv](csv/propertyList_en.csv)).
  - Click the link (Click here...)
  - The specified eYACHO/GEMBA Note will open, and generation will begin.
    - Implementation: the URI specified to the recordset_uri key creates multiple tag instances.
  ![Figure 7: Multiple Pages Generation][img7]
- Generate a from with image and PDF
  - Creates one property photo page that includes an image and a PDF.
  - Specify the property name, image file, and PDF file, then click the "Create" button.
  - The specified eYACHO/GEMBA Note will open, and generation will begin.
    - Implementation: the URI specified to the recordset_uri key handles the image and PDF files.
    ![Figure 8: Generating a page with an image and PDF][img8]

[img6]: ./image/single_property_page.png
[img7]: ./image/multi_property_page.png
[img8]: ./image/media_property_page.png

The following link is available when a note is successfully generated with either of the above three links.

- Open the last generated note
  - When you click the Open button, the shown note ID on the page is opened.

### Notice

- This server is strictly a sample and is not designed for multi-user access.
- Uploaded image files and PDF files are not deleted automatically, so please delete them manually as needed.
- Security Notice: Do not commit the .env file to version control systems like GitHub, as it contains sensitive authentication information like ACCESS_TOKEN. (Adding it to .gitignore is recommended).
- Storage folders (IMAGE_FOLDER, PDF_FOLDER) are automatically created upon the first execution if they do not exist, but please clean them up periodically.
- Depending on the specified file name, it may not be recognized.

### Updated History

- AUG-31-2026 - Added form creation with image and PDF, upgraded backup file to 1.0.3
- APR-21-2026 - Fixed for Starlette
- OCT-23-2025 - Modified for V7
- APR-22-2025 - Referred to .env and added 'Open the last generated note'
- MAR-03-2025 - Upgraded backup file froｍ 1.0.1 to 1.0.2
- SEP-24-2024 - Added APP_LANG and APP_URI_SCHEME
- SEP-09-2024 - First release
