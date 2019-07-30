// Your web app's Firebase configuration
var firebaseConfig = {
apiKey: "AIzaSyBWy2eEe5UPpS1uh0J9mmdWZrdh5Y_vxhE",
authDomain: "bitirme-firebase.firebaseapp.com",
databaseURL: "https://bitirme-firebase.firebaseio.com",
projectId: "bitirme-firebase",
storageBucket: "bitirme-firebase.appspot.com",
messagingSenderId: "1096228390788",
appId: "1:1096228390788:web:d7c7f4f48dcee763"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
database = firebase.database();
function initload() {
getOgrenci();
//getOgretmen();
//ogretmenEkle();
getTalep();
getTalepler();
}
function getOgrenci() {
var ref = database.ref('Ogrenci')
ref.on('value', gotData, errData)
function gotData(data) {
console.log(data);
//window.location.href = 'newPage/test';
//var pathname = window.location.pathname;
//onsole.log(pathname);
//data.forEach(function(element) {
//console.log(element.val().isim);
//});
tableCreate1(data, "myTableOgrenci");
}
function errData(err) {
console.log("Hata");
}
}

function getOgrenciOzel(id){
	//var info="";
	var infoOgrenci=[];
	
	var rootRef = database.ref();
		var urlRef = rootRef.child("Ogrenci/"+id);
		urlRef.once("value", function(snapshot) {
		
		snapshot.forEach(function(child) {
		
		infoOgrenci[child.key]=child.val();
		});
		//tdTalepEden.appendChild(document.createTextNode(isimsoyisim));
		
	});
	return infoOgrenci;
}


function getOgretmen() {
    var ref = database.ref('Ogretmen')
    ref.on('value', gotData, errData)
    function gotData(data) {
    console.log(data);
    //window.location.href = 'newPage/test';
    //var pathname = window.location.pathname;
    //onsole.log(pathname);
    //data.forEach(function(element) {
    //console.log(element.val().isim);
    //});
	
	
	
    //tableCreate1(data, "myTableOgretmen");
    }
    function errData(err) {
    console.log("Hata");
    }
}

function getTalepler() {
    var ref = database.ref('Yoklama_Talep')
    ref.on('value', gotData, errData)
    function gotData(data) {
    //console.log(data);
    tableCreate1(data, "myTable");
    }
    function errData(err) {
    console.log("Hata");
    }
}

var deger = 0;
function getTalep() {

    var h2 = document.getElementById("myh2talep");
    if (h2) {
        console.log("Fonksiyon Giris")

        var ref = database.ref('Yoklama_Talep')
        ref.on('value', gotData, errData)
        function gotData(data) {


            data.forEach(function (item) {
                //console.log(item.val())
                if (!item.val().yoklama_kontrol) {
                    //window.location.href = '/yuz_tanima/' + item.val().imageUuid
					//window.open('/yuz_tanima/' + item.val().imageUuid);
					
					$.getJSON($SCRIPT_ROOT + '/yuz_tanima', {
					id: item.val().imageUuid
					}, function (data) {
						//$("#result").text(data.result);
						console.log(data)
					});
					return false;
                }
            });

            //console.log("Talep" + deger)
            //console.log("Fonksion Ýçi")
            //window.location.href = 'yoklama_talebi';
            //console.log(data);
            //window.location.href = 'newPage/test';
            //var pathname = window.location.pathname;
            //onsole.log(pathname);
            //data.forEach(function(element) {
            //console.log(element.val().isim);
            //});
        }
        function errData(err) {
            console.log("Hata");
        }
        deger++;

        console.log("Fonksion Son")
    }
}


class Ogretmen {
constructor(email, isim, soyIsim, uuid) {
this.email = email;
this.isim = isim;
this.soyIsim = soyIsim;
this.uuid = uuid;
}
get getEmail() {
return this.email;
}
get getSifre() {
return this.uuid;
}
set cuuid(value) {
this.uuid = value
}
calcArea() {
return this.height * this.width;
}
}
function ogretmenEkleClick() {
email = document.getElementById("frm_email").value;
isim = document.getElementById("frm_isim").value;
soyisim = document.getElementById("frm_soyisim").value;
sifre = document.getElementById("frm_sifre").value;
var ogretment = new Ogretmen(email, isim, soyisim, sifre);
ogretmenEkle(ogretment);
}
function ogretmenEkle(ogretment) {
//var newPostKey = firebase.database().ref().child('Ogretmen').push().key;
//const ogr=new Ogretmen("Hasan@hotmail","Karasahin","Hasan",newPostKey);
//database.ref("Ogretmen/"+newPostKey).set(ogr);
var promise = firebase.auth().createUserWithEmailAndPassword(ogretment.getEmail, ogretment.getSifre);
promise
.then(
function test(user) {
ogretment.cuuid = user.user.uid;
database.ref("Ogretmen/" + user.user.uid).set(ogretment);
}).catch(e => console.log(e.message));
}
function ogretmenSil() {
var ref = database.ref('testDeger');
//ref.remove(); <---- Data siliniyor.
deleteUser()
}
function deleteUser() {
console.log(firebase.auth().INTERNAL.delete)
/*
var user = firebase.auth().getUser("nBHZICjhR6OMDvnzDvXIHx8Gb1D2");
user.delete().then(function() {
// User deleted.
var ref = firebase.database().ref(
"users/".concat(user.uid, "/")
);
ref.remove();
});*/
}
function tableCreate1(data, tableName) {
var table = document.getElementById(tableName);
    if (table){
        table.innerHTML = "";
		var sayac=1;
        data.forEach(function (element) {
            var tr = table.insertRow();
			var tdNumara = tr.insertCell();
            var tdTalepEden = tr.insertCell();
			var tdDersinAdi = tr.insertCell();
            var tdTarih = tr.insertCell();
            var tdResim = tr.insertCell();
            var tdConfig = tr.insertCell();
            //tdIsim.appendChild(document.createTextNode(element.val().isim));
            //tdSoyisim.appendChild(document.createTextNode(element.val().soyIsim));
            //tdEmail.appendChild(document.createTextNode(element.val().email));
			
			tdNumara.appendChild(document.createTextNode(sayac));
			
			
			var rootRef = database.ref();
				var urlRef = rootRef.child("Ogretmen/"+element.val().talep_eden_uuid);
				urlRef.once("value", function(snapshot) {
				var isimsoyisim="";
				snapshot.forEach(function(child) {
					if(child.key=="isim" || child.key=="soyIsim"){
						//tdDersinAdi.appendChild(document.createTextNode(child.val()));
						
						isimsoyisim+=child.val()+" ";
					}
				});
				tdTalepEden.appendChild(document.createTextNode(isimsoyisim));
			});
			
			
			var rootRef = database.ref();
				var urlRef = rootRef.child("Ders/"+element.val().ders_id);
				urlRef.once("value", function(snapshot) {
				snapshot.forEach(function(child) {
					if(child.key=="dersinAdi"){
						tdDersinAdi.appendChild(document.createTextNode(child.val()));
					}
					//console.log(child.key+": "+child.val());
					//tdDersinAdi.appendChild(document.createTextNode(child.val()['dersinAdi']));
				});
			});
			
            tdTarih.appendChild(document.createTextNode(element.val().tarih));
			
			
            tdResim.innerHTML='<a href="#" class="pop"> <img class="pop" data-toggle="modal" width="200" height="200" src="../static/download/'+element.val().imageUuid+'.png" class="rounded mx-auto d-block" alt="..."></a>';
			
			yesilbtn="";
			
			if (element.val().yoklama_kontrol){
					yesilbtn='<button class="btn btn-success" data-toggle="modal" data-target="#exampleModal1" data-whatever="'+element.val().yoklama_sonuc+'"><span class="glyphicon glyphicon-plus"></span> Result </button>'
			}
			
			resim='<a href="#" class="pop"><img class="pop" data-toggle="modal" width="50" height="50" src="../static/ogrenciResimleri/'+element.val().imageUuid+'" class="rounded mx-auto d-block" alt="..."></a>'
			
            //tdConfig.innerHTML =yesilbtn + '<button type="button" class="btn btn-danger"><a href="/delete/talep/'+element.val().imageUuid+'">Sil</a></button>';
            tdConfig.innerHTML =yesilbtn + '<button type="button" class="btn btn-danger"><a href="/delete/talep/'+element.val().imageUuid+'">Sil</a></button>';
			
			
			tr.appendChild(tdNumara)
            tr.appendChild(tdTalepEden)
            tr.appendChild(tdDersinAdi)
            tr.appendChild(tdTarih)
            tr.appendChild(tdResim)
            tr.appendChild(tdConfig)
            table.appendChild(tr)
			
			sayac=sayac+1;
        });
    }
}