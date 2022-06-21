function fetchData() {
    fetch("http://127.0.0.1:5000/get-products").then(response => {
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

fetchData();