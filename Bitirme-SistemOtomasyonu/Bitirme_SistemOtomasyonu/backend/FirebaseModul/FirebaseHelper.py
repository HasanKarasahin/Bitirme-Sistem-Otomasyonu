import pyrebase
import firebase_admin
from firebase_admin import credentials,auth,db
from Bitirme_SistemOtomasyonu.backend.IOHelper import IOHelper

class FirebaseHelper():

    __config = {
        "apiKey": "AIzaSyBWy2eEe5UPpS1uh0J9mmdWZrdh5Y_vxhE",
        "authDomain": "bitirme-firebase.firebaseapp.com",
        "databaseURL": "https://bitirme-firebase.firebaseio.com",
        "projectId": "bitirme-firebase",
        "storageBucket": "bitirme-firebase.appspot.com",
        "messagingSenderId": "1096228390788"
    }

    __cred = credentials.Certificate('Bitirme_SistemOtomasyonu/backend/FirebaseModul/serviceAccountKey.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(__cred, {
        'databaseURL': 'https://bitirme-firebase.firebaseio.com'
    })

    __firebase = pyrebase.initialize_app(__config)

    __db = __firebase.database()

    __auth=__firebase.auth()

    path=IOHelper()

    def listener(event):

        # print(event.event_type)  # can be 'put' or 'patch'
        # print(event.path)  # relative to the reference, it seems
        #print(event.data['-LafRwfyDC2duP06Vky3']['color'])  # new data at /reference/event.path. None if deleted
        print("--"*25)
        print(event.path)
        print("--"*25)


    #firebase_admin.db.reference('Yoklama_Talep').listen(listener)

    def yuz_tanima(self,id):
        taninanKisiler=yid.init(id)
        #return render_template('yuz_bul.html',adet=y.getFotograftakiYuzSayisi(id))
        print(taninanKisiler)

        self.yoklama_listesini_ekle(id,taninanKisiler)


    def getDatabase(self):
        return self.__db

    def addAuthentication(self,form,nodeName):
        try:
            user=self.__auth.create_user_with_email_and_password(form['frm_email'],form['frm_sifre'])
            self.__addNewUser(form,user,nodeName)
            return user['localId']
        except:
            return False

    def __addNewUser(self,form,user,nodeName):
        userData = {
        "isim":form['frm_isim'],
        "soyIsim":form['frm_soyisim'],
        "email":user['email'],
        "uuid":user['localId']
        }

        if (nodeName=="Ogrenci"):
            userData["numara"]=form['frm_numara']
            userData["cinsiyet"]=form['frm_cinsiyet']

        self.getDatabase().child(nodeName).child(user['localId']).set(userData)

    def deleteAuthUser(self,nodeName,uuid):
        try:
            auth.delete_user(uuid)
            self.__deleteNodeUser(nodeName,uuid)
            return True
        except:
            return False
    def __deleteNodeUser(self,nodeName,uuid):
        self.getDatabase().child(nodeName).child(uuid).remove()

    def deleteTalep(self,uuid):
        self.getDatabase().child("Yoklama_Talep").child(uuid).remove()

    def getKullanicilar(self,nodeName):
        users = (self.getDatabase().child(nodeName).get())
        return users

    def getDersListesi(self,state=False):

        if(state):
            dersler = self.getDatabase().child("Ders").get()

            for ders in dersler.each():
                
                ogretmen = self.getDatabase().child("Ogretmen").child(ders.val()['dersinOgretmeni']).get()
                ders.val()['dersinOgretmeni']=ogretmen.val()['isim'] + " " + ogretmen.val()['soyIsim']
        else:
            dersler = self.getDatabase().child("Ders").get()
        
        return dersler

    def getTalepler(self,kontrol=False):
        talepler = self.getDatabase().child("Yoklama_Talep").get()
        print("Dosya Durumu4")
        if kontrol and talepler.val() != None:
            print("Dosya Durumu3")
            for talep in talepler.each():
                print(talep.val()['imageUuid'])
                print("Dosya Durumu2")
                if (self.checkFile(talep.val()['imageUuid'])):
                    self.getImages(talep.val()['imageUuid'])

                
                    print("Dosya Yok")
        
        return talepler

    def getKey(self):
        return self.__db.generate_key()

    def getKullaniciEmail(self,rootNodeName,uuid):
        kullanici = self.getDatabase().child(rootNodeName).child(uuid).get()
        return kullanici.val()['email']


    def ekleTalep(self,form,key):

        talepData = {
        "talep_eden_uuid":form['frm_talepeden'],
        "talep_eden_email":self.getKullaniciEmail("Ogretmen",form['frm_talepeden']),
        "tarih":form['frm_tarih'],
        "imageUuid":key,
        "yoklama_kontrol":False,
        "ders_id ":form['frm_ders'],
        "yoklama_listesi":list("e")
        }
        
        
        try:
            self.__resimEkle(key)
            self.getDatabase().child("Yoklama_Talep").child(key).set(talepData)
            return True
        except:
            return False

    def __resimEkle(self,key):
        storage=self.__firebase.storage()
        storage.child("images/"+key+".png").put("Bitirme_SistemOtomasyonu/static/download/"+key+".png")

    def getImages(self,resimNodeName):
        storage=self.__firebase.storage()
        storage.child("images/"+resimNodeName).download("Bitirme_SistemOtomasyonu/static/download/"+resimNodeName+".png")

    def getInfo(self):
        user = auth.get_user_by_email("billgates@hotmail.com")
        print('Successfully fetched user data: {0}'.format(user.uid))

    def checkFile(self,imagePath):
        return self.path.checkFile(imagePath)

    def yoklama_listesini_ekle(self,resimid,yoklamaListesi):
        print("Yoklama Sonucu : ")
        if(not yoklamaListesi):
            yoklamaListesi={
                "0":"empty"
                }
        self.getDatabase().child("Yoklama_Talep").child(resimid).child("yoklama_sonuc").set(yoklamaListesi)
        self.getDatabase().child("Yoklama_Talep").child(resimid).child("yoklama_kontrol").set(True)

        talep = self.getDatabase().child("Yoklama_Talep").child(resimid).get()

        key=talep.val()['tarih']+talep.val()['ders_id']

        sonuc= self.getDatabase().child("Yoklama_Talep_Sonuc").child(key).get()

        if(sonuc.val()):
            if (sonuc.val()['yoklama_listesi']):
                try:
                    if(sonuc.val()['yoklama_listesi'][0]!="empty"):
                        yoklamaListesi=list(set(yoklamaListesi + sonuc.val()['yoklama_listesi']))
                    
                    Yoklama_Sonuc_Data={
                    "id":key,
                    "ders_id":talep.val()['ders_id'],
                    "tarih":talep.val()['tarih'],
                    "yoklama_listesi":yoklamaListesi
                    }

                    self.getDatabase().child("Yoklama_Talep_Sonuc").child(Yoklama_Sonuc_Data['id']).set(Yoklama_Sonuc_Data);
                
                except TypeError:
                    print("Hata")
        else:
            try:
                #yoklamaListesi=list(set(yoklamaListesi))
                print("Yoklama Listesi {0}".format(yoklamaListesi))
                Yoklama_Sonuc_Data={
                "id":key,
                "ders_id":talep.val()['ders_id'],
                "tarih":talep.val()['tarih'],
                "yoklama_listesi":yoklamaListesi
                }

                self.getDatabase().child("Yoklama_Talep_Sonuc").child(Yoklama_Sonuc_Data['id']).set(Yoklama_Sonuc_Data);
                
            except TypeError:
                print("Hata")
        

    def addDers(self,form):
        key = self.getKey()

        ders_cizelgesi={
            "0":"20-05-2019",
            "1":"22-05-2019",
            "2":"24-05-2019",
            "3":"26-05-2019",
            "4":"28-05-2019",
            "5":"30-05-2019",
            "6":"31-06-2019"
            }

        dersData = {
        "dersinAdi":form['frm_dersinAdi'],
        "dersinOgretmeni":form['frm_dersinOgretmeni'],
        "dersiAlanOgrenciListesi":form.getlist('frm_check'),
        "uuid":key,
        "ders_cizelgesi":ders_cizelgesi
        }

        self.getDatabase().child("Ders").child(key).set(dersData)