document.addEventListener('DOMContentLoaded', () => {
    const removeButtons = document.querySelectorAll('.delete');
    const cartSummary = document.querySelector('.cart-summary');
    const clearAllBtn = document.getElementById('clearAllBtn');
    const checkoutBtn = document.getElementById('checkoutBtn');

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
                        'X-CSRFToken': getCSRFToken(),
                    },
                });

                if (response.ok) {
                    const productWidget = button.closest('.product-widget');
                    productWidget.remove();

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
        fetch('cart_summary/')
            .then(response => response.json())
            .then(data => {
                const small = cartSummary.querySelector('small');
                const h5 = cartSummary.querySelector('h5');

                if (small && h5) {
                    small.textContent = `${data.cart_item_count} Item(s) selected`;
                    h5.textContent = `SUBTOTAL: $${data.cart_total.toFixed(2)}`;
                }

                // Enable/disable buttons based on cart_item_count
                const isCartEmpty = data.cart_item_count === 0;
                clearAllBtn.classList.toggle('disabled', isCartEmpty);
                checkoutBtn.classList.toggle('disabled', isCartEmpty);
                clearAllBtn.style.pointerEvents = isCartEmpty ? 'none' : 'auto';
                checkoutBtn.style.pointerEvents = isCartEmpty ? 'none' : 'auto';
                clearAllBtn.style.opacity = isCartEmpty ? '0.5' : '1';
                checkoutBtn.style.opacity = isCartEmpty ? '0.5' : '1';
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    updateCartSummary();
});
