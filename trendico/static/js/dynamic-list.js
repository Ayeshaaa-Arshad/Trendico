$(document).ready(function() {
    var productListContainer = $('#product-list');
    var slickInitialized = false;
    var slickOptions = {
        slidesToShow: 4,
        slidesToScroll: 1,
        dots: false,
        arrows: true,
        autoplay: true,
        autoplaySpeed: 5000
    };
    function updateProductList(data) {
        var productHtml = '';

        data.forEach(function(product) {
            var discountPriceHtml = '';
            if (product.discount_price) {
                discountPriceHtml = `
                    <h4 class="product-price">$${product.discount_price}
                        <del class="product-old-price">$${product.price}</del>
                    </h4>`;
            } else {
                discountPriceHtml = `<h4 class="product-price">$${product.price}</h4>`;
            }

            var newLabelHtml = product.is_new ? '<span class="new">NEW</span>' : '';

            var saleLabelHtml = product.discount_price ? `<span class="sale">-${product.discount_percentage}%</span>` : '';

            var productTemplate = `
                <div class="product product-template">
                    <div class="product-img">
                        <img src="${product.image_url}" alt="">
                        <div class="product-label">
                            ${saleLabelHtml}
                            ${newLabelHtml}
                        </div>
                    </div>
                    <div class="product-body">
                        <p class="product-category">${product.category}</p>
                        <h3 class="product-name"><a href="#">${product.name}</a></h3>
                        ${discountPriceHtml}
                        <div class="product-rating">
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                            <i class="fa fa-star"></i>
                        </div>
                        <div class="product-btns">
                            <button class="add-to-wishlist"><i class="fa fa-heart-o"></i><span class="tooltipp">add to wishlist</span></button>
                            <button class="add-to-compare"><i class="fa fa-exchange"></i><span class="tooltipp">add to compare</span></button>
                            <button class="quick-view"><i class="fa fa-eye"></i><span class="tooltipp">quick view</span></button>
                        </div>
                    </div>
                    <div class="add-to-cart">
                        <a href="#"><button class="add-to-cart-btn"><i class="fa fa-shopping-cart"></i> add to cart</button></a>
                    </div>
                </div>
            `;

            productHtml += productTemplate;
        });

        productListContainer.slick('unslick');
        productListContainer.empty().append(productHtml);
        productListContainer.slick(slickOptions);

        var slickControls = productListContainer.find('.slick-prev, .slick-next');
        var prevArrow = productListContainer.find('.slick-prev');
        slickControls.css({
            'right': '5px',
        });
         prevArrow.css({
            'left': '5px',
        });

        if (!slickInitialized) {
            productListContainer.slick(slickOptions);
            slickInitialized = true;
        }
    }

    $('.category-link').on('click', function(e) {
        e.preventDefault();
        var category = $(this).data('category');

        console.log("Fetching products for category:", category);

        $.get(`get_products/${category}/`)
            .done(function(data) {
                console.log("Data received from server:", data);
                updateProductList(data);
            })
            .fail(function(xhr, status, error) {
                console.error(error);
            });
    });

    console.log("Initializing Slick Slider on page load...");
    productListContainer.slick(slickOptions);

});
