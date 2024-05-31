/*const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const searchButton = document.getElementById('search-button');
    const addProductForm = document.getElementById('add-product-form');

    if (searchButton) {
        searchButton.addEventListener('click', searchButtonOnClick);
    }

    if (addProductForm) {
        addProductForm.addEventListener('submit', postReqOnClick);
    }
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const searchInput = document.getElementById('search-input').value;
    const resultsBody = document.getElementById('results-body');

        // Κάνουμε ένα GET request στο endpoint /search
        fetch(`${api}/search?name=${encodeURIComponent(searchInput)}`)
            .then(response => response.json())
            .then(data => {
                // Καθαρίζουμε τα προηγούμενα αποτελέσματα
                resultsBody.innerHTML = '';
                // Προσθέτουμε τα νέα αποτελέσματα
                data.forEach(product => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${product.id}</td>
                        <td>${product.name}</td>
                        <td>${product.production_year}</td>
                        <td>${product.price}</td>
                        <td>${product.color}</td>
                        <td>${product.size}</td>
                    `;
                    resultsBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    // END CODE HERE
}*/

//productFormOnSubmit = (event) => {
    // BEGIN CODE HERE
    document.getElementById('dataForm').addEventListener('submit', function(event) {
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
    });
    
    // END CODE HERE
//}
