document.addEventListener('DOMContentLoaded', () => {
    const wishlistContainer = document.querySelector('.wishlist');

    wishlistContainer.addEventListener('click', async (event) => {
        const deleteButton = event.target.closest('.delete');
        if (!deleteButton) return;

        event.preventDefault();

        const form = deleteButton.closest('.remove-from-wishlist-form');
        const wishlistItemId = form.getAttribute('data-wishlist-item-id');
        console.log('Removing item:', wishlistItemId);

        try {
            const response = await fetch(`/remove_from_wishlist/${wishlistItemId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken(),
                },
            });

            if (response.ok) {
                const jsonResponse = await response.json();
                if (jsonResponse.success) {
                    console.log(jsonResponse.message);
                    form.parentElement.remove();

                    const wishlistCountElement = document.querySelector('.qty');
                    wishlistCountElement.textContent = jsonResponse.wishlist_item_count;
                } else {
                    console.error(jsonResponse.message);
                }
            } else {
                console.error('Error removing wishlist item');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    const addToWishlistButtons = document.querySelectorAll('.add-to-wishlist');

    addToWishlistButtons.forEach(async (button) => {
        button.addEventListener('click', async (event) => {
            event.preventDefault();

            const productId = button.getAttribute('data-product-id');
            console.log('Product ID:', productId);

            try {
                const response = await fetch(`/wishlist/${productId}`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ product_id: productId }),
                });

                if (response.ok) {
                    const jsonResponse = await response.json();
                    if (jsonResponse.success) {
                        console.log(jsonResponse.message);

                        window.location.reload();
                    } else {
                        console.error(jsonResponse.error);
                    }
                } else {
                    console.error('Error adding product to wishlist');
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
});
