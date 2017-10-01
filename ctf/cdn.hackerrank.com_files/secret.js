$.ajaxSetup({beforeSend: function(xhr){
  if (xhr.overrideMimeType)
  {
    xhr.overrideMimeType("application/json");
  }
}
});

$(document).ready(function(){
    $(".button").click(function(){
        $.getJSON("key.json", function(keyjson) {
        	document.write(keyjson)
        	//This isn't doing anything. How do I get all the keys?
			
			$.getJSON("_json/"+input+".json", function(json) {
				$(".news-body").html("Pulled: " + json["title"]);
			});

		});
    });
});
