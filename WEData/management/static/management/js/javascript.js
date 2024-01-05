




// sortTable.js

function sortTable(columnIndex) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("myTable");
    switching = true;
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[columnIndex];
            y = rows[i + 1].getElementsByTagName("TD")[columnIndex];
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}



// Calculate 'Days Old' for each order
document.addEventListener("DOMContentLoaded", function() {
    const orders = document.querySelectorAll('[id^="days-old-"]');
    orders.forEach(function(order) {
        const orderDateStr = order.previousElementSibling.previousElementSibling.textContent.trim();
        const orderDate = new Date(orderDateStr);
        const currentDate = new Date();
        const timeDiff = currentDate - orderDate;
        const daysOld = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
        order.textContent = daysOld;
    });
});




document.getElementById('show-more').addEventListener('click', function() {
    localStorage.setItem('scrollPosition', window.scrollY || document.documentElement.scrollTop);
});

window.onload = function() {
    if (localStorage.getItem('scrollPosition')) {
        window.scrollTo(0, localStorage.getItem('scrollPosition'));
        localStorage.removeItem('scrollPosition');
    }
};