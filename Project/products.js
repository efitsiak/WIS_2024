// Αλληλεπίδραση 1: Αναζήτηση προϊόντος
document.getElementById("searchBtn").addEventListener("click", function() {
    var searchInput = document.getElementById("searchInput").value;
    fetch("/search?name=" + searchInput)
        .then(response => response.json())
        .then(data => {
            var productsTable = document.getElementById("productsTable");
            productsTable.innerHTML = ""; // Αδειάζει τον πίνακα πριν προσθέσει νέα δεδομένα
            data.forEach(product => {
                var row = productsTable.insertRow();
                row.insertCell(0).innerHTML = product.id;
                row.insertCell(1).innerHTML = product.name;
                row.insertCell(2).innerHTML = product.production_year;
                row.insertCell(3).innerHTML = product.price;
                row.insertCell(4).innerHTML = product.color;
                row.insertCell(5).innerHTML = product.size;
            });
        })
        .catch(error => console.error('Error:', error));
});

// Αλληλεπίδραση 2: Προσθήκη προϊόντος
document.getElementById("addProductForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var jsonData = {};
    formData.forEach((value, key) => { jsonData[key] = value });
    fetch("/add-product", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => {
        if (response.ok) {
            alert("ΟΚ");
            document.getElementById("addProductForm").reset(); // Αδειάζει τη φόρμα μετά την επιτυχή υποβολή
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .catch(error => console.error('Error:', error));
});
