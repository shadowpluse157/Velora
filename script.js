
/* =========================================
   VELORA — MAIN JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    // ---------- 1. NAVBAR ACTIVE LINK ----------

    const currentPage = window.location.pathname;

    document.querySelectorAll(".nav-link").forEach(link => {
        const linkPage = new URL(link.href).pathname;

        if (linkPage === currentPage) {
            link.classList.add("active");
        }
    });


    // ---------- 2. PRODUCT SEARCH ----------

    const searchInput = document.querySelector("#productSearch");
    const productCards = document.querySelectorAll(".product-item");

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const searchValue = searchInput.value.toLowerCase().trim();

            productCards.forEach(card => {
                const productName =
                    card.dataset.name?.toLowerCase() || "";

                const productCategory =
                    card.dataset.category?.toLowerCase() || "";

                const matches =
                    productName.includes(searchValue) ||
                    productCategory.includes(searchValue);

                card.style.display = matches ? "" : "none";
            });
        });
    }


    // ---------- 3. CATEGORY FILTER ----------

    const categoryFilters =
        document.querySelectorAll('input[name="category"]');

    categoryFilters.forEach(filter => {
        filter.addEventListener("change", () => {

            const selectedCategory = filter.value.toLowerCase();

            productCards.forEach(card => {

                const cardCategory =
                    card.dataset.category?.toLowerCase() || "";

                const matches =
                    selectedCategory === "all" ||
                    cardCategory === selectedCategory;

                card.style.display = matches ? "" : "none";

            });

        });
    });


    // ---------- 4. PRICE SORTING ----------

    const sortSelect = document.querySelector("#sortProducts");

    if (sortSelect) {
        sortSelect.addEventListener("change", () => {

            const container =
                document.querySelector("#productsContainer");

            if (!container) return;

            const cards = Array.from(
                container.querySelectorAll(".product-item")
            );

            const sortValue = sortSelect.value;

            cards.sort((a, b) => {

                const priceA = Number(a.dataset.price || 0);
                const priceB = Number(b.dataset.price || 0);

                if (sortValue === "low-high") {
                    return priceA - priceB;
                }

                if (sortValue === "high-low") {
                    return priceB - priceA;
                }

                if (sortValue === "name") {
                    return (a.dataset.name || "").localeCompare(
                        b.dataset.name || ""
                    );
                }

                return 0;

            });

            cards.forEach(card => container.appendChild(card));

        });
    }


    // ---------- 5. PRODUCT QUANTITY ----------

    const quantityInput = document.querySelector("#quantity");

    const decreaseBtn = document.querySelector("#decreaseQuantity");
    const increaseBtn = document.querySelector("#increaseQuantity");

    if (quantityInput) {

        const getQuantity = () => {
            return Math.max(1, Number(quantityInput.value) || 1);
        };

        if (decreaseBtn) {
            decreaseBtn.addEventListener("click", () => {
                quantityInput.value = Math.max(
                    1,
                    getQuantity() - 1
                );
            });
        }

        if (increaseBtn) {
            increaseBtn.addEventListener("click", () => {
                const maxStock = Number(quantityInput.max) || Infinity;

                quantityInput.value = Math.min(
                    maxStock,
                    getQuantity() + 1
                );
            });
        }

        quantityInput.addEventListener("change", () => {
            const maxStock = Number(quantityInput.max) || Infinity;

            quantityInput.value = Math.min(
                maxStock,
                getQuantity()
            );
        });

    }


    // ---------- 6. ADD TO CART FEEDBACK ----------

    document.querySelectorAll(".add-to-cart-btn").forEach(button => {

        button.addEventListener("click", () => {

            const originalText = button.textContent;

            button.textContent = "Added ✓";
            button.disabled = true;

            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
            }, 1500);

        });

    });


    // ---------- 7. WISHLIST ----------

    document.querySelectorAll(".wishlist-btn").forEach(button => {

        button.addEventListener("click", () => {

            const isActive = button.classList.toggle("active");

            button.innerHTML = isActive ? "♥" : "♡";

            button.style.color = isActive
                ? "#ff4d8d"
                : "";

        });

    });


    // ---------- 8. REMOVE CART ITEM ----------

    document.querySelectorAll(".remove-cart-item").forEach(button => {

        button.addEventListener("click", event => {

            const confirmed = confirm(
                "Are you sure you want to remove this product?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    // ---------- 9. CHECKOUT VALIDATION ----------

    const checkoutForm = document.querySelector("#checkoutForm");

    if (checkoutForm) {

        checkoutForm.addEventListener("submit", event => {

            if (!checkoutForm.checkValidity()) {

                event.preventDefault();
                event.stopPropagation();

                alert("Please complete all required fields.");

            }

            checkoutForm.classList.add("was-validated");

        });

    }


    // ---------- 10. PASSWORD VISIBILITY ----------

    document.querySelectorAll(".toggle-password").forEach(button => {

        button.addEventListener("click", () => {

            const input = document.querySelector(
                button.dataset.target
            );

            if (!input) return;

            input.type = input.type === "password"
                ? "text"
                : "password";

        });

    });


    // ---------- 11. BACK TO TOP ----------

    const backToTop = document.querySelector("#backToTop");

    if (backToTop) {

        window.addEventListener("scroll", () => {

            backToTop.style.display =
                window.scrollY > 300 ? "block" : "none";

        });

        backToTop.addEventListener("click", () => {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        });

    }


    // ---------- 12. CURRENT YEAR ----------

    const yearElement = document.querySelector("#currentYear");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

});
