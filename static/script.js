let addPage = document.getElementById("add-book");
let addBtn = document.getElementById("addBtn");
addPage.classList.add("hide-page");

addBtn.addEventListener("click", function(){
    addPage.classList.remove("hide-page");
    let closeBtn = document.getElementById("closeBtn");
    closeBtn.addEventListener("click", function(){
        addPage.classList.add("hide-page");
    });
});