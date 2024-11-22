const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li');

allSideMenu.forEach((item) => {
	item.addEventListener('click', function () {
		this.classList.add('active');
		localStorage.setItem("active-page", item.id)
	});
})

document.addEventListener("DOMContentLoaded", function() {
	const path = window.location.pathname.replace("/admin/", "").split("/")[0].replace("/", "")
	
	if (path === "") setActivePage("dashboard")
	else setActivePage(path)
	
})

function setActivePage(activePage) {
	if (activePage !== "" && activePage !== null) {
		allSideMenu.forEach((item) => {
			item.classList.remove("active")
		})
		document.getElementById(activePage).classList.add("active")
	}
}

// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})


//resize textarea
// Select the textarea element
const textarea = document.getElementById("exampleFormControlTextarea1");

// Add an event listener to adjust the height on input
textarea.addEventListener("input", function () {
    this.style.height = "auto"; // Reset the height first
    this.style.height = (this.scrollHeight) + "px"; // Set height based on scroll height
});
