const myForm = document.getElementById('myForm')
const formGewicht = document.getElementById('gram')
const formCategorie = document.getElementById('categorie')
const formDieet = document.getElementById('dieet')


function fetchData(weight, category, dieet) {
    fetch(`http://127.0.0.1:5000/get-products/${weight}/${category}/${dieet}`).then(response => {
        if (!response.ok) {
            throw Error("ERROR")
        }
        return response.json();
    }).then(result => {

        let index = 1
        document.getElementById("title").style.display = "block";
        document.getElementById("storage").style.display = "block";


        const html = result.map(user => {
            return `<div class="product" data-name="p-${index++}">
                     <img alt="Qries" src="${user.image}">
                     <h3>${user.name}</h3>
                     <div class="price">€${user.price}</div>
                     </div>
                    `}).join('');

        console.log(html);

        document.querySelector('#app').innerHTML = html
    }).catch(error => {
        console.log(error);
    });
}

myForm.addEventListener('submit', (e) => {
    e.preventDefault()
    fetchData(formGewicht.value, 10, formDieet.value)
})



const wrapper = document.querySelector(".user-details"),
selectBtn = wrapper.querySelector(".select-btn"),
searchInp = wrapper.querySelector("input"),
options = wrapper.querySelector(".options");

let categories = ["salades-pizza-maaltijden", "vlees-kip-vis-vega", "kaas-vleeswaren-tapas", "zuivel-plantaardig-en-eieren", "bakkerij-en-banket", "ontbijtgranen-en-beleg",
                            "snoep-koek-chips-en-chocolade", "tussendoortjes", "frisdrank-sappen-koffie-thee", "wijn-en-bubbels", "bier-en-aperitieven", "pasta-rijst-en-wereldkeuken", "soepen-sauzen-kruiden-olie",
                            "sport-en-dieetvoeding", "diepvries", "drogisterij", "baby-en-kind", "huishouden", "huisdier", "koken-tafelen-vrije-tijd"];

function addCategory(selectedCategorie) {
    options.innerHTML = "";
    categories.forEach(categorie => {
        let isSelected = categorie == selectedCategorie ? "selected" : "";
        let li = `<li onclick="updateName(this)" class="${isSelected}">${categorie}</li>`;
        options.insertAdjacentHTML("beforeend", li);
    });
}
addCategory();
function updateName(selectedLi) {
    searchInp.value = "";
    addCategory(selectedLi.innerText);
    wrapper.classList.remove("active");
    selectBtn.firstElementChild.innerText = selectedLi.innerText;
}
searchInp.addEventListener("keyup", () => {
    let arr = [];
    let searchWord = searchInp.value.toLowerCase();
    arr = categories.filter(data => {
        return data.toLowerCase().startsWith(searchWord);
    }).map(data => {
        let isSelected = data == selectBtn.firstElementChild.innerText ? "selected" : "";
        return `<li onclick="updateName(this)" class="${isSelected}">${data}</li>`;
    }).join("");
    options.innerHTML = arr ? arr : `<p style="margin-top: 10px;">Oops! Country not found</p>`;
});
selectBtn.addEventListener("click", () => wrapper.classList.toggle("active"));
