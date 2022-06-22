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

function clickData() {
    let preveiwContainer = document.querySelector('.products-preview');
    let previewBox = preveiwContainer.querySelectorAll('.preview');


    document.querySelectorAll('.products-container .product').forEach(product =>{
      product.onclick = () =>{
        preveiwContainer.style.display = 'flex';
        let name = product.getAttribute('data-name');
        previewBox.forEach(preview =>{
          let target = preview.getAttribute('data-target');
          if(name == target){
            preview.classList.add('active');
          }
        });
      };
    });

    previewBox.forEach(close =>{
      close.querySelector('.fa-times').onclick = () =>{
        close.classList.remove('active');
        preveiwContainer.style.display = 'none';
      };
    });
}

fetchData();
clickData();