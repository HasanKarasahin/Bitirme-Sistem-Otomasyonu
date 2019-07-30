
    $(function () {
        $('.pop').on('click', function () {
            $('.imagepreview').attr('src', $(this).find('img').attr('src'));
            $('#imagemodal').modal('show');
        });

        $(document).ready(function () {
            $("#myInput").on("keyup", function () {
                var value = $(this).val().toLowerCase();
                $("#myTable1 tr").filter(function () {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                });
            });
        });
		
		 $(document).ready(function () {
            $("#myInput").on("keyup", function () {
                var value = $(this).val().toLowerCase();
                $("#myTable tr").filter(function () {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                });
            });
        });
		
		$('#exampleModal1').on('show.bs.modal', function (event) {
			var button = $(event.relatedTarget) // Button that triggered the modal
			var recipient = button.data('whatever') // Extract info from data-* attributes
			// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
			// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
			var modal = $(this)
			//modal.find('.modal-title').text('New message to ' + recipient)
			
			
			//modal.find('.modal-body bulunanOgrencilertbl').innerHTML=
			
			//document.getElementById('bulunanOgrencilertbl').innerHTML='<tr><th scope="row">1</th><td>Mark</td><td>Otto</td><td>@mdo</td></tr>'
			
			//firebasedengelen();
			
			

			var table = document.getElementById("bulunanOgrencilertbl");
			
			if(table){
				table.innerHTML = "";
				var a = recipient.split(","),i;
				
				for (i = 0; i < a.length; i++) {
				//document.getElementById("updateAvailable_" + a[i]).style.visibility= "visible";
				
				infoOgrenci=getOgrenciOzel(a[i]);
				
				var tr = table.insertRow();
				
				var tdSayac=tr.insertCell();
				var tdNumara = tr.insertCell();
				var tdİsimSoyisim = tr.insertCell();
				
				
				tdSayac.appendChild(document.createTextNode(i+1));
				tdNumara.appendChild(document.createTextNode(infoOgrenci["numara"]));
				tdİsimSoyisim.appendChild(document.createTextNode(infoOgrenci["isim"] + " " + infoOgrenci["soyIsim"] ));
				
				
				tr.appendChild(tdSayac)
				tr.appendChild(tdNumara)
				tr.appendChild(tdİsimSoyisim)
				
				table.appendChild(tr)
				
				
			}
			}
			
			
			
			//console.log(getOgrenciOzel("9G3Qywyr7yfUguvteXXP8rMV20i2"));
		
			
		})
    });

   