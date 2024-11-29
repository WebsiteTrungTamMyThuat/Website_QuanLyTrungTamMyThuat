document.addEventListener('DOMContentLoaded', function () 
{
    const loginRegister = document.getElementById('loginRegister');
    const userLoggedIn = document.getElementById('userLoggedIn');
    const dropdownMenu = document.createElement('div');
    dropdownMenu.classList.add('dropdown-menu', 'deactive');
    dropdownMenu.innerHTML = `
        <ul>
            <li><a href="/dieukhien/${idtaikhoan}">Bảng điều khiển</a></li>
            <li><a href="/user/lichsukh">Lịch sử mua hàng</a></li>
            <li><a id="logoutButton" href="/user/logout">Đăng xuất</a></li>
        </ul>
    `;
    userLoggedIn.appendChild(dropdownMenu);

    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

    if (isLoggedIn) {
        loginRegister.classList.add('deactive');
        userLoggedIn.classList.remove('deactive');
    } else {
        loginRegister.classList.remove('deactive');
        userLoggedIn.classList.add('deactive');
    }

    userLoggedIn.addEventListener('click', function() {
        dropdownMenu.classList.toggle('deactive');
    });

    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('isLoggedIn');
            window.location.href = '/user/dangnhap';  // Chuyển hướng về trang đăng nhập
        });
    }
});

/**
 * add event listener on multiple elements
 */

const addEventOnElements = function (elements, eventType, callback) {
    for (let i = 0, len = elements.length; i < len; i++) {
        elements[i].addEventListener(eventType, callback);
    }
};

/**
 * MOBILE NAVBAR TOGGLE
 */

const navbar = document.querySelector("[data-navbar]");
const navTogglers = document.querySelectorAll("[data-nav-toggler]");
const overlay = document.querySelector("[data-overlay]");

const toggleNav = function () {
    navbar.classList.toggle("active");
    overlay.classList.toggle("active");
};

addEventOnElements(navTogglers, "click", toggleNav);

/**
 * active header when window scroll down to 100px
 */

const header = document.querySelector("[data-header]");

const headerActive = function () {
    if (window.scrollY > 100) {
        header.classList.add("active");
    } else {
        header.classList.remove("active");
    }
};

window.addEventListener("scroll", headerActive);

function initParadoxWay() {
    "use strict";

    if ($(".testimonials-carousel").length > 0) {
        var j2 = new Swiper(".testimonials-carousel .swiper-container", {
            preloadImages: false,
            slidesPerView: 1,
            spaceBetween: 20,
            loop: true,
            grabCursor: true,
            mousewheel: false,
            centeredSlides: true,
            pagination: {
                el: ".tc-pagination",
                clickable: true,
                dynamicBullets: true,
            },
            navigation: {
                nextEl: ".listing-carousel-button-next",
                prevEl: ".listing-carousel-button-prev",
            },
            breakpoints: {
                1024: {
                    slidesPerView: 3,
                },
            },
        });
    }

    // bubbles -----------------

    setInterval(function () {
        var size = randomValue(sArray);
        $(".bubbles").append(
            '<div class="individual-bubble" style="left: ' +
            randomValue(bArray) +
            "px; width: " +
            size +
            "px; height:" +
            size +
            'px;"></div>'
        );
        $(".individual-bubble").animate(
            {
                bottom: "100%",
                opacity: "-=0.7",
            },
            4000,
            function () {
                $(this).remove();
            }
        );
    }, 350);
}

//   Init All ------------------
$(document).ready(function () {
    initParadoxWay();
    document.querySelectorAll('[name="payment"]').forEach(function (element) {
        element.addEventListener('change', function () {
            console.log(this.value);
            if (this.value === "transfer") {
                document.getElementById('collapseTransfer').classList.add('show');
                document.getElementById('collapseOnePay').classList.remove('show');
            } else {
                document.getElementById('collapseOnePay').classList.add('show');
                document.getElementById('collapseTransfer').classList.remove('show');
            }
        });
    });
});


//List page
let thisPage = 1;
let limit = 12;
let list = document.querySelectorAll('.grid-container .card');

function loadItem() {
    let beginGet = limit * (thisPage - 1);
    let endGet = limit * thisPage - 1;
    list.forEach((card, key) => {
        if (key >= beginGet && key <= endGet) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    })
    listPage();
}

loadItem();

function listPage() {
    let count = Math.ceil(list.length / limit);
    document.querySelector('.list-page').innerHTML = '';

    if (thisPage != 1) {
        let prev = document.createElement('li');
        prev.innerText = 'Trước';
        prev.setAttribute('onclick', "changePage(" + (thisPage - 1) + ")");
        document.querySelector('.list-page').appendChild(prev);
    }

    for (i = 1; i <= count; i++) {
        let newPage = document.createElement('li');
        newPage.innerText = i;
        if (i == thisPage) {
            newPage.classList.add('active');
        }
        newPage.setAttribute('onclick', "changePage(" + i + ")");
        document.querySelector('.list-page').appendChild(newPage);
    }

    if (thisPage != count) {
        let next = document.createElement('li');
        next.innerText = 'Tiếp';
        next.setAttribute('onclick', "changePage(" + (thisPage + 1) + ")");
        document.querySelector('.list-page').appendChild(next);
    }
}

function changePage(i) {
    thisPage = i;
    loadItem();
}


//FILTER DATEPICKER
const datepicker = document.querySelector(".datepicker");
const dateInput = document.querySelector(".date-input");
const yearInput = datepicker.querySelector(".year-input");
const monthInput = datepicker.querySelector(".month-input");
const cancelBtn = datepicker.querySelector(".cancel");
const applyBtn = datepicker.querySelector(".apply");
const nextBtn = datepicker.querySelector(".next");
const prevBtn = datepicker.querySelector(".prev");
const dates = datepicker.querySelector(".dates");

let selectedDate = new Date();
let year = selectedDate.getFullYear();
let month = selectedDate.getMonth();

// show datepicker
dateInput.addEventListener("click", () => {
  datepicker.hidden = false;
});

// hide datepicker
cancelBtn.addEventListener("click", () => {
  datepicker.hidden = true;
});

// handle apply button click event
applyBtn.addEventListener("click", () => {
  // set the selected date to date input
  dateInput.value = selectedDate.toLocaleDateString("en-US", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  // hide datepicker
  datepicker.hidden = true;
});

// handle next month nav
nextBtn.addEventListener("click", () => {
  if (month === 11) year++;
  month = (month + 1) % 12;
  displayDates();
});

// handle prev month nav
prevBtn.addEventListener("click", () => {
  if (month === 0) year--;
  month = (month - 1 + 12) % 12;
  displayDates();
});

// handle month input change event
monthInput.addEventListener("change", () => {
  month = monthInput.selectedIndex;
  displayDates();
});

// handle year input change event
yearInput.addEventListener("change", () => {
  year = yearInput.value;
  displayDates();
});

const updateYearMonth = () => {
  monthInput.selectedIndex = month;
  yearInput.value = year;
};

const handleDateClick = (e) => {
  const button = e.target;

  // remove the 'selected' class from other buttons
  const selected = dates.querySelector(".selected");
  selected && selected.classList.remove("selected");

  // add the 'selected' class to current button
  button.classList.add("selected");

  // set the selected date
  selectedDate = new Date(year, month, parseInt(button.textContent));
};

// render the dates in the calendar interface
const displayDates = () => {
  // update year & month whenever the dates are updated
  updateYearMonth();

  // clear the dates
  dates.innerHTML = "";

  //* display the last week of previous month

  // get the last date of previous month
  const lastOfPrevMonth = new Date(year, month, 0);

  for (let i = 0; i <= lastOfPrevMonth.getDay(); i++) {
    const text = lastOfPrevMonth.getDate() - lastOfPrevMonth.getDay() + i;
    const button = createButton(text, true, -1);
    dates.appendChild(button);
  }

  //* display the current month

  // get the last date of the month
  const lastOfMOnth = new Date(year, month + 1, 0);

  for (let i = 1; i <= lastOfMOnth.getDate(); i++) {
    const button = createButton(i, false);
    button.addEventListener("click", handleDateClick);
    dates.appendChild(button);
  }

  //* display the first week of next month

  const firstOfNextMonth = new Date(year, month + 1, 1);

  for (let i = firstOfNextMonth.getDay(); i < 7; i++) {
    const text = firstOfNextMonth.getDate() - firstOfNextMonth.getDay() + i;

    const button = createButton(text, true, 1);
    dates.appendChild(button);
  }
};

const createButton = (text, isDisabled = false, type = 0) => {
  const currentDate = new Date();

  // determine the date to compare based on the button type
  let comparisonDate = new Date(year, month + type, text);

  // check if the current button is the date today
  const isToday =
    currentDate.getDate() === text &&
    currentDate.getFullYear() === year &&
    currentDate.getMonth() === month;

  // check if the current button is selected
  const selected = selectedDate.getTime() === comparisonDate.getTime();

  const button = document.createElement("button");
  button.textContent = text;
  button.disabled = isDisabled;
  button.classList.toggle("today", isToday && !isDisabled);
  button.classList.toggle("selected", selected);
  return button;
};

displayDates();