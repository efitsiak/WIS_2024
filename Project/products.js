const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    window.open = api;
    const searchButton = document.getElementById('search-button');
    const addProductForm = document.getElementById('dataForm');

    if (searchButton) {
        searchButton.addEventListener('click', searchButtonOnClick);
    }

    if (addProductForm) {
        addProductForm.addEventListener('submit', productFormOnSubmit);
    }
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const searchInput = document.getElementById('inputSearch').value;
    const resultsTable = document.getElementById('resultsTable');
    console.log("Search input:", searchInput); // Debug statement

    const colorsMapping = {
        1: 'red',
        2: 'yellow',
        3: 'blue'
    };

    const sizesMapping = {
        1: 'small',
        2: 'medium',
        3: 'large',
        4: 'extra large'
    };

    fetch(`${api}/search?name=${encodeURIComponent(searchInput)}`)
        .then(response => response.json())
        .then(data => {
            resultsTable.innerHTML = ''; // Καθαρίζουμε τον πίνακα πριν εμφανίσουμε τα αποτελέσματα
            data.forEach(product => {

             const color = colorsMapping[product.color];
             const size = sizesMapping[product.size];

                const row = resultsTable.insertRow();
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.production_year}</td>
                    <td>${product.price}</td>
                    <td>${color}</td>
                    <td>${size}</td>
                `;
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE
        event.preventDefault();
        const formData = {
            name: document.getElementById('inputName').value,
            year: document.getElementById('inputYear').value,
            price: document.getElementById('inputPrice').value,
            color: document.getElementById('inputColor').value,
            size: document.getElementById('inputSize').value,
        };

        fetch('/add-product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/products';
            } else {
                throw new Error('Form submission failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    
    // END CODE HERE
}
