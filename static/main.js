var myModal = document.getElementById("basicModal");
var myInput = document.getElementById("Select-Instance");

myModal.addEventListener("shown.bs.modal", function () {
  myInput.focus();
});
