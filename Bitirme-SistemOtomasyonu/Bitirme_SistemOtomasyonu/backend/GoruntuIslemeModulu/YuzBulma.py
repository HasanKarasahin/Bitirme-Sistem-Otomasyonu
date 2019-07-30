import face_recognition
class YuzBulma(object):
    
    def getFotograftakiYuzSayisi(self,id):

        image = face_recognition.load_image_file('Bitirme_SistemOtomasyonu/static/download/'+id+'.png')
        face_locations = face_recognition.face_locations(image)

        return len(face_locations)


