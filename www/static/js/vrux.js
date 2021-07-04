var refreshToken = null;
var token = null;
var authorization = null;
var user = null;

function main() {
	refreshToken = getCookie("refreshToken");
	if (refreshToken == null) {
		showHtmlPage("login");
	} else {
		if (user == null) { setUserAuth(); }
		else { showHtmlPage("main"); }
	}
}

$(document).ready(function() {
	main();
});