import os
import json
from copy import copy
import shutil
import msvcrt

class File:
    def __init__(self,path,relPath,number):
        self.path = path
        self.relPath = relPath
        self.number = number
        self.name = path.split('\\')[-1]
        self.size = os.path.getsize(path)
        
    def __lt__(self,other):
        return self.size < other.size

class WeTransferGrouper:
    def __init__(self, path) -> None:
        self.mainDir = path
        self.allFiles = []
        self.buckets = []
        self.preserveStructure = False
        self.maxSize = 2*(10**9)
        self.manifest = {}
        print(self.mainDir)

    def printFiles(self):
        print(f"{len(self.allFiles)} files in total")
        for i,f in enumerate(self.allFiles):
            print(f"#{i+1}: \t {f.name}, \t size:{f.size}")

    def printBuckets(self):
        for i,(b,s) in enumerate(self.buckets):
            print(f"bucket #{i+1}: size:{round(s/(10**6),3)} MB")

    def findFiles(self):
        self.fileCount = 1

        def dfs(dir):
            for f in os.listdir(dir):
                path = os.path.join(dir, f)
                if os.path.isfile(path):
                    relPath = path[len(self.mainDir)+1:]
                    self.allFiles.append(File(path, relPath, self.fileCount))
                    self.manifest[self.fileCount] = relPath
                    self.fileCount += 1
                else:
                    if os.path.exists(path):
                        dfs(path)

        dfs(self.mainDir)           


    def groupFiles(self):
        self.allFiles.sort()

        array = copy(self.allFiles)
        tooLarge = []

        while len(array):
            folder = []
            folderSize = 0
            for i in range(len(array)-1,-1,-1):
                currFile = array[i]

                if currFile.size > self.maxSize:
                    tooLarge.append((currFile.name,currFile.size))
                    array.pop(i)
                elif self.maxSize - folderSize >= currFile.size:
                    folder.append(currFile)
                    folderSize += currFile.size
                    array.pop(i)

            self.buckets.append((folder,folderSize))
        
        self.printBuckets()
        print(f"tooLarge: {tooLarge}")

    def copyFile(self,source_file,destination):
        try:
            # Copy the source file to the destination
            shutil.copy(source_file.path, destination)
            os.chdir(destination)
            newName = str(source_file.number) + '.' + source_file.name.split('.')[-1]
            os.rename(source_file.name, newName)
            print(f"File '{source_file.path}' copied to '{destination}' successfully.")
        except FileNotFoundError:
            print(f"Error: Source file '{source_file.path}' not found.")
        except IsADirectoryError:
            print(f"Error: Destination '{destination}' is a directory, not a file.")
        except PermissionError:
            print(f"Error: Permission denied when copying to '{destination}'.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def prepDir(self):
        newDir = os.path.join(self.mainDir,"wetransfer_prepped")

        if not os.path.exists(newDir):
            os.mkdir(newDir)

            for i, (bucket,size) in enumerate(self.buckets):
                # make part folder
                currPartFolder = os.path.join(newDir,f"part_{i+1}")
                os.mkdir(currPartFolder)

                # add manifest as json
                manifest_path = os.path.join(currPartFolder,"manifest.json")
                with open(manifest_path, "w") as json_file:
                    json.dump(self.manifest, json_file, indent=4)

                for file in bucket:
                    self.copyFile(file,currPartFolder)


if __name__ == "__main__":
    maindir = input("Enter path to folder: ")
    # maindir = r"C:\Danik\euro_trip\insta360\folder"
    
    helper = WeTransferGrouper(maindir)
    helper.findFiles()
    helper.groupFiles()
    helper.prepDir()

    print("====== DONE ======")

    print("Press any key to exit...")
    msvcrt.getch()
