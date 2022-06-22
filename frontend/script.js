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
        console.log(result);
        let index = 1

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
    fetchData(formGewicht.value, formCategorie.value, formDieet.value)
})

