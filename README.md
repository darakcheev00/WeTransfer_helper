# WeTransfer_helper
WeTransfer allows free transfers of up to 2GB at a time.

Use the grouper to efficiently package your files into 2GB folders which you can upload manually.

WeTransfer doesn't have an API so you will need to manually upload these generated folders.


**How it works**

The sender runs grouper.exe and enters the directory in which the files to be sent are located.

The receiver runs ungrouper.exe and enters the source and destination directory.
- Source directory: single folder where all downloaded unzipped WeTransfer folders are.
- Destination director: folder into which the files will be transfered.

Folders can be dragged into the the terminal instead of manually entering path.


**Note**
- Has been tested only on Windows.
- To use on mac just run with Python (update coming)
