import face_recognition
from PIL import Image, ImageDraw
from Bitirme_SistemOtomasyonu.backend.IOHelper import IOHelper
from Bitirme_SistemOtomasyonu.backend.FirebaseModul.FirebaseHelper import FirebaseHelper
class YuzTanima(object):
    def __init__(self):
        self.path = IOHelper()
        self.known_face_encodings = []
        self.known_face_names = []
        self.train()

    def __getEncoding(self,resimYolu):
        image_of_temp = face_recognition.load_image_file("Bitirme_SistemOtomasyonu/static/ogrenciResimleri/"+resimYolu)
        temp_encoding = face_recognition.face_encodings(image_of_temp)[0]
        return temp_encoding

    def train(self):
        resimYollari = self.path.getImagesPath()

        for yol in resimYollari:
            self.known_face_encodings.append(self.__getEncoding(yol))
            self.known_face_names.append(yol)

    def init(self,id):

        if(self.path.checkFile(id)):
            FirebaseHelper().getImages(id)

        known_list=[]

        # Load test image to find faces in
        test_image = face_recognition.load_image_file('Bitirme_SistemOtomasyonu/static/download/'+id+'.png')

        # Find faces in test image
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        # Loop through faces in test image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            name = "Unknown Person"

            # If match
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                known_list.append(name[0:len(name)-4])

        return known_list