// Ripple effect from 'Medium' site
(function () {
  var cleanUp, debounce, i, len, ripple, rippleContainer, ripples, showRipple;

  debounce = function (func, delay) {
    var inDebounce;
    inDebounce = undefined;
    return function () {
      var args, context;
      context = this;
      args = arguments;
      clearTimeout(inDebounce);
      return (inDebounce = setTimeout(function () {
        return func.apply(context, args);
      }, delay));
    };
  };

  showRipple = function (e) {
    var pos, ripple, rippler, size, style, x, y;
    ripple = this;
    rippler = document.createElement("span");
    size = ripple.offsetWidth;
    pos = ripple.getBoundingClientRect();
    x = e.pageX - pos.left - size / 2;
    y = e.pageY - pos.top - size / 2;
    style =
      "top:" +
      y +
      "px; left: " +
      x +
      "px; height: " +
      size +
      "px; width: " +
      size +
      "px;";
    ripple.rippleContainer.appendChild(rippler);
    return rippler.setAttribute("style", style);
  };

  cleanUp = function () {
    while (this.rippleContainer.firstChild) {
      this.rippleContainer.removeChild(this.rippleContainer.firstChild);
    }
  };

  ripples = document.querySelectorAll("[ripple]");

  for (i = 0, len = ripples.length; i < len; i++) {
    ripple = ripples[i];
    rippleContainer = document.createElement("div");
    rippleContainer.className = "ripple--container";
    ripple.addEventListener("mousedown", showRipple);
    ripple.addEventListener("mouseup", debounce(cleanUp, 2000));
    ripple.rippleContainer = rippleContainer;
    ripple.appendChild(rippleContainer);
  }
})();

var actionBar = document.querySelector(".action-bar");
var menuIcon = document.querySelector("#menu");
var sideNav = document.querySelector(".side-nav");
var width = document.documentElement.clientWidth;
var nav = document.querySelector("nav");
var list = nav.querySelectorAll("li");

sideNav.style.width = width - actionBar.clientHeight + "px";

menuIcon.addEventListener("click", openSideNav);

window.addEventListener("click", (e) => {
  if (e.target.parentNode != menuIcon) {
    closeSideNav();
  }
});

window.addEventListener("resize", closeSideNav);

function openSideNav() {
  sideNav.style.transform = "translateX(0)";
}

function closeSideNav() {
  sideNav.style.transform = "translateX(-320px)";
}

for (let i = 0; i < list.length; i++) {
  list[i].onclick = function () {
    var c = 0;
    while (c < list.length) {
      list[c++].className = "";
    }
    list[i].className = "active";
  };
}
