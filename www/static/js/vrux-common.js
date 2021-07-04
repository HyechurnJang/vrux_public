function getCookie(name) {
	var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
	return value?unescape(value[2]):null;
}

function showError(xhr, exception) {
	console.log(xhr);
	console.log(exception);
	window.alert("Error !");
}

function showHtmlPage(name) {
	$("#main").load("/html/" + name + ".html" );
}

function showHtmlPage1(name) {
//function showHtmlPage(name) {
	$.ajax({
		type: "GET",
		url: "/html/" + name + ".html",
		dataType: "text/html",
		success : function (data) {
			$("#main").html(data);
		},
		error : showError
	});
}

function setUserAuth() {
	$.ajax({
		type: "POST",
		url: "/auth/token",
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify({ refreshToken: refreshToken }),
		success : function (data) {
			token = data.token;
			authorization = "Bearer " + token;
			$.ajaxSetup({
				beforeSend: function (xhr) { xhr.setRequestHeader("Authorization", authorization); }
			})
			$.ajax({
				type: "GET",
				url: "/vra/csp/gateway/am/api/userinfo",
				headers: {
					"Accept": "application/json",
				},
				success : function (data) {
					user = data;
					main();
				},
				error: showError
			});
		},
		error: showError
	});
}

function getView(view) {
	$.ajax({
		type: "GET",
		url: "/vra" + view.url,
		headers: {
			"Accept": "application/json"
		},
		success : view.action,
		error : function(xhr, exception) {
			console.log(xhr);
			console.log(exception);
			if (xhr.status == 401) {
				console.log("try auth");
			}
		}
	});
}

function postView(view, data) {
	$.ajax({
		type: "POST",
		url: "/vra" + view.url,
		headers: {
			"Content-Type": "application/json; charset=utf-8",
			"Accept": "application/json"
		},
		dataType: "json",
		data: JSON.stringify(data),
		success : view.action,
		error: function (xhr, exception) {
			console.log(xhr);
			console.log(exception);
			if (xhr.status == 401) {
				console.log("try auth");
			}
		}
	});
}