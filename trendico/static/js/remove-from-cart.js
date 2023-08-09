document.addEventListener('DOMContentLoaded', () => {
    const removeButtons = document.querySelectorAll('.delete');
    const cartSummary = document.querySelector('.cart-summary');

    removeButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            event.preventDefault();

            const cartItemId = button.parentElement.getAttribute('data-cart-item-id');
            const actionUrl = button.parentElement.getAttribute('data-action');

            try {
                const response = await fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCSRFToken(), // Call a function to retrieve the CSRF token
                    },
                });

                if (response.ok) {
                    // Remove the deleted cart item from the DOM
                    const productWidget = button.closest('.product-widget');
                    productWidget.remove();

                    // Update the cart summary
                    updateCartSummary();
                } else {
                    console.error('Error removing cart item');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });

    function getCSRFToken() {
        const cookies = document.cookie.split('; ');
        for (const cookie of cookies) {
            const [name, value] = cookie.split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    function updateCartSummary() {
        fetch("{% url 'cart_summary' %}")
            .then(response => response.json())
            .then(data => {
                const small = cartSummary.querySelector('small');
                const h5 = cartSummary.querySelector('h5');

                small.textContent = `${data.cart_item_count} Item(s) selected`;
                h5.textContent = `SUBTOTAL: $${data.cart_total.toFixed(2)}`;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Call updateCartSummary initially
    updateCartSummary();
});
