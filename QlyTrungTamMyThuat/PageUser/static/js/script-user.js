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
});


//List page
let thisPage = 1;
let limit = 12;
let list = document.querySelectorAll('.grid-container .card');

function loadItem(){
    let beginGet = limit * (thisPage - 1);
    let endGet = limit * thisPage - 1;
    list.forEach((card, key)=>{
        if(key >= beginGet && key <= endGet){
            card.style.display = 'block';
        }else{
            card.style.display = 'none';
        }
    })
    listPage();
}
loadItem();
function listPage(){
    let count = Math.ceil(list.length / limit);
    document.querySelector('.list-page').innerHTML = '';

    if(thisPage != 1){
        let prev = document.createElement('li');
        prev.innerText = 'Trước';
        prev.setAttribute('onclick', "changePage(" + (thisPage - 1) + ")");
        document.querySelector('.list-page').appendChild(prev);
    }

    for(i = 1; i <= count; i++){
        let newPage = document.createElement('li');
        newPage.innerText = i;
        if(i == thisPage){
            newPage.classList.add('active');
        }
        newPage.setAttribute('onclick', "changePage(" + i + ")");
        document.querySelector('.list-page').appendChild(newPage);
    }

    if(thisPage != count){
        let next = document.createElement('li');
        next.innerText = 'Tiếp';
        next.setAttribute('onclick', "changePage(" + (thisPage + 1) + ")");
        document.querySelector('.list-page').appendChild(next);
    }
}
function changePage(i){
    thisPage = i;
    loadItem();
}