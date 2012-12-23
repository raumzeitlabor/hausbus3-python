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

// wrapper to output value. defaults to just the value, if nothing matches.
function printValue(data, key, sub_key) {
	if (key == "temperature") {
		return data[key][sub_key] + " °C";
	} else if (key == "system") {
		if (sub_key == "uptime") {
			// Source: http://thesmithfam.org/blog/2005/11/19/python-uptime-script/. Ported to JS
			MINUTE  = 60;
			HOUR    = MINUTE * 60;
			DAY     = HOUR * 24;
			
			total_seconds = data[key][sub_key];
			days    = Math.floor( total_seconds / DAY );
			hours   = Math.floor( ( total_seconds % DAY ) / HOUR );
			minutes = Math.floor( ( total_seconds % HOUR ) / MINUTE );
			seconds = Math.floor( total_seconds % MINUTE );
			
			string = "";
			if (days > 0)
				string += days + " " + ((days == 1)? "day" : "days" ) + ", ";
			if (string.length > 0 || hours > 0)
				string += hours + " " + ((hours == 1)? "hour" : "hours" ) + ", ";
			if (string.length > 0 || minutes > 0)
				string += minutes + " " + ((minutes == 1)?"minute" : "minutes" ) + ", ";
			string += seconds + " " + ((seconds == 1 )?"second" : "seconds" );
			
			return string;
		} else if (sub_key == "features") {
			string = ""
			for (var feature in data[key][sub_key]) { // iterate through all features
				if ("enabled" in data[key][sub_key][feature] && data[key][sub_key][feature]["enabled"] == true) {
					string += feature + ": ";
					if (feature.match(/^https*$/i)) { // create link for webservices
						string += "<a href=\"" + feature + "://" + window.location.hostname + ":" + data[key][sub_key][feature]["port"] + "\">";
						string += feature + "://" + window.location.hostname + ":" + data[key][sub_key][feature]["port"] + "</a>";
					} else { // "enabled" for all other features
						string += "enabled";
					}
					string +="<br>";
				} else {
					string += feature + ": " + "disabled" + "<br>";
				}
			}
			return string;
		}
	} else if (key == "windows") {
		if (sub_key == "state") {
			string = "<table class=\"windows\">";
			for (var i = 0; i < data[key][sub_key].length; i++) {
				string += "<tr>";
				for (var j = 0; j < data[key][sub_key][i].length; j++) {
					string += "<td>" + data[key][sub_key][i][j] + "</td>";
				}
				string += "</tr>";
			}
			string += "</table>";
			return string;
		}
	}
	return data[key][sub_key];
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
					out += "<tr><th>"+sub_key + "</th><td>" + printValue(data,key,sub_key) +"</td></tr>";
				}
				out += "</table></div></section>"
			}
			$("#output").html(out);
		}
	});	
});
