function keyImage(key) {
	switch(key) {
		case "temperature":
			return "images/temperature.svg";
			break;
		case "io_ports":
			return "images/chip.svg";
			break;
		case "windows":
			return "images/window.svg";
			break;
		case "pinpad":
			return "images/keys.svg";
			break;
		default:
			return "images/chip.svg";
	}
}

$(document).ready(function() {
	$.ajax({
		url: '/_/state',
		success: function(data) {
			var out = "";
			for (var key in data) {
				out += "<section>";							
				out += "<img src=\""+ keyImage(key)+"\">";
				out += "<div><h2>" + key + "</h2><table>";
				for (var sub_key in data[key]) {
					out += "<tr><th>"+sub_key + "</th><td>" + data[key][sub_key]+"</td></tr>";
				}
				out += "</table></div></section>"
			}
			$("#output").html(out);
		}
	});	
});
