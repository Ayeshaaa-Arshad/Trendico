document.addEventListener('DOMContentLoaded', function() {
        const checkboxes = document.querySelectorAll('.item-checkbox');
        const itemTotals = document.querySelectorAll('.item-total');
        const totalElement = document.querySelector('.order-total');

        checkboxes.forEach((checkbox, index) => {
            checkbox.addEventListener('change', () => updateTotal(index));
        });

        function updateTotal(index) {
            let total = 0;
            checkboxes.forEach((checkbox, i) => {
                if (checkbox.checked) {
                    const cartItemPrice = parseFloat(checkbox.getAttribute('data-price'));
                    const cartItemQuantity = parseInt(checkbox.getAttribute('data-quantity'));
                    const itemTotal = cartItemPrice * cartItemQuantity;
                    total += itemTotal;

                    itemTotals[i].textContent = `$${itemTotal.toFixed(2)}`;
                } else {
                    itemTotals[i].textContent = '$0.00';
                }
            });

            totalElement.textContent = `$${total.toFixed(2)}`;
        }

        // Calculate and set initial item totals
        itemTotals.forEach((itemTotal, index) => {
            const cartItemPrice = parseFloat(checkboxes[index].getAttribute('data-price'));
            const cartItemQuantity = parseInt(checkboxes[index].getAttribute('data-quantity'));
            const initialTotal = cartItemPrice * cartItemQuantity;
            itemTotal.textContent = `$${initialTotal.toFixed(2)}`;
        });
    });