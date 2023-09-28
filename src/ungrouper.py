import os
import json
import shutil
import msvcrt

class WeTransferUngrouper:
    def __init__(self, srcDir, destDir) -> None:
        self.srcDir = srcDir
        self.destDir = destDir
        self.folders = []
        self.manifest = {}
        os.chdir(srcDir)

    def copyFile(self,source_file,destination):
        try:
            # Copy the source file to the destination
            shutil.copy(source_file, destination)
            print(f"File '{source_file}' copied to '{destination}' successfully.")
        except FileNotFoundError:
            print(f"Error: Source file '{source_file.path}' not found.")
        except IsADirectoryError:
            print(f"Error: Destination '{destination}' is a directory, not a file.")
        except PermissionError:
            print(f"Error: Permission denied when copying to '{destination}'.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def saveFile(self, srcFilePath, relPath):
        pathArray = relPath.split('\\')
        print(pathArray)
        currDestDir = self.destDir

        while len(pathArray):
            if len(pathArray) == 1:
                filePath = os.path.join(currDestDir,pathArray[0])
                self.copyFile(srcFilePath,filePath)
                break
            else:
                # is a folder
                currFolderName = pathArray.pop(0)
                currFolder = os.path.join(currDestDir,currFolderName) 

                # if doesnt exist then make a folder
                if not os.path.exists(currFolder):
                    os.mkdir(currFolder)
                
                currDestDir = currFolder

                
    def ungroup(self):
        for item in os.listdir(self.srcDir):
            if os.path.isdir(item):
                print(item)
                currFolder = os.path.join(self.srcDir,item)

                manifestPath = os.path.join(currFolder,"manifest.json")
                with open(manifestPath, "r") as json_file:
                    self.manifest = json.load(json_file)

                for file in os.listdir(currFolder):
                    if file != "manifest.json":
                        relPath = self.manifest[file.split('.')[0]]
                        srcFilePath = os.path.join(currFolder,file)
                        self.saveFile(srcFilePath, relPath)



if __name__ == "__main__":
    print("Make sure you have all the wetransfer downloads unzipped in the one folder!!!")

    # srcDir = r"C:\Danik\euro_trip\insta360\folder\wetransfer_prepped"
    # destDir = r"C:\Danik\Coding\random_files\wetransfer_helper\dest"

    srcDir = input("Enter path to folder to ungroup: ")
    destDir = input("Enter destination folder: ")

    helper = WeTransferUngrouper(srcDir,destDir)
    helper.ungroup()
    print("====== DONE ======")

    print("Press any key to exit...")
    msvcrt.getch()
