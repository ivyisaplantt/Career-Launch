const form = document.getElementById('product-form');
const table = document.querySelector('#product-table tbody');

// Prevent page from reloading when form is submitted
form.addEventListener('submit', (e) => {
    e.preventDefault();
});

// Try to add a feature that checks which option was chosen for the stores.
const product = document.getElementById('product-name').value;
const storea = document.getElementById('store-a').value;
const storeb = document.getElementById('store-b').value;

const row = document.createElement('tr');
  row.innerHTML = `
    <td>${product}</td>
    <td>${storea}</td>
    <td>${storeb}</td>
  `;

// This allows us to only display one product at a time.
if (table.contains() == false) {
    table.appendChild(row);
} else {
    table.removeChild(table.childNodes[0]);
    table.appendChild(row);
}