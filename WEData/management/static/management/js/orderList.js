function filterOrders() {
    var filterValue = document.getElementById('statusFilter').value;
    var tableBody = document.getElementById('orderTableBody');
    tableBody.innerHTML = ''; // Clear current content

    // Fetch orders based on the filter
    fetch(`/api/orders?status=${filterValue}`)
        .then(response => response.json())
        .then(orders => {
            orders.forEach(order => {
                var row = tableBody.insertRow();
                row.innerHTML = `
                    <td><a href="/orders/${order.id}">${order.number}</a></td>
                    <td>${order.customerName}</td>
                    <td>${order.date}</td>
                    <td>${order.status}</td>
                `;
            });
        });
}

// Initial load
filterOrders();
