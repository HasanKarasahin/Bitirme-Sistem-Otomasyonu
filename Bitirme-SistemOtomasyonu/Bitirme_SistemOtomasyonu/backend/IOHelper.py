import os

class IOHelper(object):
    # path = './/img//known//'

    

    def getImagesPath(self):
        files = []
        path = 'Bitirme_SistemOtomasyonu\\static\\ogrenciResimleri'
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                    files.append(file)

        
        return files

    def checkFile(self,imagePath):
        result=os.path.exists("Bitirme_SistemOtomasyonu/static/download/"+imagePath+".png")
        return not result