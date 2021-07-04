
var mainCatalogs = {
	url: "/catalog/api/items",
	action: function (data) {
		for (var content of data.content) {
			for (var projectId of content.projectIds) {
				$("#project-" + projectId).append(`
<div class="col">
	<div class="catalog card shadow-sm">
		<div class="catalog-icon">
			<img class="catalog-icon-img card-img-top" src="/vra/icon/api/icons/${content.iconId}"></img>
			<h5 class="card-title">${content.name}</h5>
		</div>
		<div class="catalog-body">
			<div class="card-body">
				<p class="card-text">${content.type.name}</p>
				<a href="#" class="btn btn-primary">Request</a>
			</div>
		</div>
	</div>
</div>
`)
			}
		}
	}
}


var mainProjects = {
	url: "/iaas/api/projects",
	action: function (data) {
		var index = 0;
		for (var content of data.content) {
			$("#project-carousel-indicators").append(`<button type="button" data-bs-target="#project-carousel" data-bs-slide-to="${index}" ${index==0?'class="active" aria-current="true" ':''}aria-label="${content.name}"></button>`);
			$("#project-carousel-inner").append(`
<div class="carousel-item${index==0?' active':''}">
	<div class="carousel-panel d-block">
		<div id="project-${content.id}" class="carousel-cards row row-cols-4 g-3"></div>
		<div class="carousel-caption d-none d-md-block">
			<h1>${content.name}</h1>
		</div>
	</div>
</div>
`);
			index++;
		}
		getView(mainCatalogs)
	}
}
