/**
 * add event listener on multiple elements
 */

const addEventOnElements = function (elements, eventType, callback) {
    for (let i = 0, len = elements.length; i < len; i++) {
      elements[i].addEventListener(eventType, callback);
    }
  }
  
  
  
  /**
   * MOBILE NAVBAR TOGGLE
   */
  
  const navbar = document.querySelector("[data-navbar]");
  const navTogglers = document.querySelectorAll("[data-nav-toggler]");
  const overlay = document.querySelector("[data-overlay]");
  
  const toggleNav = function () {
    navbar.classList.toggle("active");
    overlay.classList.toggle("active");
  }
  
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
  }
  
  window.addEventListener("scroll", headerActive);

 

// View Password codes
         
      
function myLogPassword(){
  var a = document.getElementById("logPassword");
  var b = document.getElementById("eye");
  var c = document.getElementById("eye-slash");
  if(a.type === "password"){
     a.type = "text";
     b.style.opacity = "0";
     c.style.opacity = "1";
  }else{
     a.type = "password";
     b.style.opacity = "1";
     c.style.opacity = "0";
  }
 }
 function myRegPassword(){

  var d = document.getElementById("regPassword");
  var b = document.getElementById("eye-2");
  var c = document.getElementById("eye-slash-2");

  if(d.type === "password"){
     d.type = "text";
     b.style.opacity = "0";
     c.style.opacity = "1";
  }else{
     d.type = "password";
     b.style.opacity = "1";
     c.style.opacity = "0";
  }
 }