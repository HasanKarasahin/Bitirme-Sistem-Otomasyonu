"""
Routes and views for the flask application.
"""
from flask import render_template,request,redirect,url_for,jsonify
from Bitirme_SistemOtomasyonu import app
from flask.ext.uploads import UploadSet , configure_uploads, IMAGES

from Bitirme_SistemOtomasyonu.backend.FirebaseModul.FirebaseHelper import FirebaseHelper
from Bitirme_SistemOtomasyonu.backend.GoruntuIslemeModulu.YuzBulma import YuzBulma
from Bitirme_SistemOtomasyonu.backend.GoruntuIslemeModulu.YuzTanima import YuzTanima

f=FirebaseHelper()
y=YuzBulma()
yid=YuzTanima()
database=f.getDatabase()

photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST']='Bitirme_SistemOtomasyonu/static/newimg'
configure_uploads(app,photos)

@app.route('/')
@app.route('/anasayfa')
def anasayfa():
    #f.resimEkle()
    mesaj1="Karadeniz Teknik Üniversitesi"
    mesaj2="Yüz Tanıma İle Yoklama Sistemi"
    return render_template(
        'index.html',
        title='Home Page',
        mesaj1=mesaj1,
        mesaj2=mesaj2
    )

@app.route('/ogretmen',methods=['GET', 'POST'])
def ogretmen():
    
    if request.method == "POST":
        result=f.addAuthentication(request.form,"Ogretmen")
        if(result!=False):
            result=True
        ogretmenlerListesi=f.getKullanicilar("Ogretmen")
        return render_template('page_ekle_ogretmen.html',result=result,ogretmenlerListesi=ogretmenlerListesi)

    ogretmenlerListesi=f.getKullanicilar("Ogretmen")

    return render_template('page_ekle_ogretmen.html',ogretmenlerListesi=ogretmenlerListesi)

@app.route('/ogrenci',methods=['GET', 'POST'])
def ogrenci():
    
    if request.method == 'POST':
        result=f.addAuthentication(request.form,"Ogrenci")
        ogrenciListesi=f.getKullanicilar("Ogrenci")

        if(result==False):
            return render_template('page_ekle_ogrenci.html',result=False,ogrenciListesi=ogrenciListesi)
        else:
            config("ogrenciResimleri")
            filename=photos.save(request.files['file'],name=result+".png")
            return render_template('page_ekle_ogrenci.html',result=True,ogrenciListesi=ogrenciListesi)
        #return filename
        
    ogrenciListesi=f.getKullanicilar("Ogrenci")
    return render_template('page_ekle_ogrenci.html',ogrenciListesi=ogrenciListesi)

@app.route('/ders',methods=['GET', 'POST'])
def ders():

    if request.method=="POST":
        print("Form Ekranındaki Check")
        
        print(request.form.getlist('frm_check'))
        f.addDers(request.form)
        
    ogretmenListesi=f.getKullanicilar("Ogretmen")
    ogrenciListesi=f.getKullanicilar("Ogrenci")

    dersListesi=f.getDersListesi(True)
    return render_template('page_ekle_ders.html',ogretmenListesi=ogretmenListesi,ogrenciListesi=ogrenciListesi,dersListesi=dersListesi)

@app.route('/yuz_bul/<string:id>')
def yuz_bul(id):
    adet=y.getFotograftakiYuzSayisi(id)
    #return render_template('yuz_bul.html',adet=y.getFotograftakiYuzSayisi(id))
    print(adet)
    return redirect('/yoklama_talebi')

#@app.route('/yuz_tanima/<string:id>')
@app.route('/yuz_tanima')
def yuz_tanima():
    id = request.args.get('id', "aaa", type=str)
    taninanKisiler=yid.init(id)
    #return render_template('yuz_bul.html',adet=y.getFotograftakiYuzSayisi(id))
    print(taninanKisiler)

    f.yoklama_listesini_ekle(id,taninanKisiler)

    return jsonify(result="geri donus yapildi")
    #return redirect('/yoklama_talebi')

@app.route('/yoklama_talebi',methods=['GET', 'POST'])
def yoklama_talebi():

    ogretmenListesi=f.getKullanicilar("Ogretmen")
    dersListesi=f.getDersListesi()

    if request.method=="POST":
        config("download")
        key=f.getKey()
        filename=photos.save(request.files['file'],name=key+".png")
        result=f.ekleTalep(request.form,key)
        
        talepListesi=f.getTalepler()
        return render_template('yoklama_talebi.html',result=result,talepListesi=talepListesi,ogretmenListesi=ogretmenListesi,dersListesi=dersListesi)
        #return request.form["testemail"]

    talepListesi=f.getTalepler(kontrol=True)
    return render_template('yoklama_talebi.html',talepListesi=talepListesi,ogretmenListesi=ogretmenListesi,dersListesi=dersListesi)

@app.route('/delete/<string:kullanici>/<string:uuid>')
def delete(kullanici,uuid):

    if kullanici.lower()=="ogretmen":
        f.deleteAuthUser("Ogretmen",uuid)
        return redirect('/ogretmen')
    elif kullanici.lower()=="ogrenci":
        f.deleteAuthUser("Ogrenci",uuid)
        return redirect('/ogrenci')
    elif kullanici.lower()=="talep":
        f.deleteTalep(uuid)
        return redirect('/yoklama_talebi')
    else:
        return "Sayfa Hatasi"

def config(path):
    app.config['UPLOADED_PHOTOS_DEST']='Bitirme_SistemOtomasyonu/static/'+path
    configure_uploads(app,photos)


