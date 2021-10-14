import os
import json

BASE_PATH = "C:\\Users\\User\\Documents\\Discord_Note"

def getPATH(ctx):
    return BASE_PATH+ str(ctx.guild.id)+".txt"

class Notes:
    _path = ""
    _noteData = {}
    
    def __init__(self,path):
        if __name__ == "__bot__":
            self._path = path
            try:
                with open(self._path, "r") as file: #呼叫note.json文件
                    self._noteData = json.load(file)
            except(FileNotFoundError, json.decoder.JSONDecodeError):
                print("__note init error__")
                pass
    
    def getAllData(self):
        return self._noteData
    
    def get(self,name):
        return self._noteData[name] if name in self._noteData else False

    def write(self,name,content):
        self._noteData[name] = content
        self._save()

    def delete(self,name):
        if name in self._noteData:
            del self._noteData[name]
            self._save()
            return True
        else:
            return False

    def _save(self):
        path = os.path.join(self._path,"estdir")
        os.makedirs(path,exist_ok=True) 
        #os.path.dirname(self._path)
        #os.makedirs -> 在此path創立資料夾
        #os.path.dirname -> return 為去除檔案名稱，回傳目錄的路徑
        try:
            with open(self._path,"w") as file:
                 json.dump(self._noteData,file)  # json.dump()是要把dict轉成str
        except:
            print("_save open error!")
            pass
    

