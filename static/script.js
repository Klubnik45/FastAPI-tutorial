let closeBtn = document.querySelector("#closeBtn");
let saveBtn = document.querySelector("#saveBtn");
let addPage = document.getElementById("add-book");
let addBtn = document.getElementById("addBtn");
let updatePage = document.querySelectorAll("#book-list>li>form");
let addCloseBtn = ""
let addSaveBtn = ""

addPage.classList.add("hide-page");

addBtn.addEventListener("click", function(){
    addPage.classList.remove("hide-page");
});

console.log(updatePage);