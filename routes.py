
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from database import (
    get_db_connection,
    get_all_products,
    get_product
)

main = Blueprint("main", __name__)


# =========================================
# HELPER: GET CART ITEMS
# =========================================

def get_cart_items():

    cart = session.get("cart", {})
    cart_items = []

    connection = get_db_connection()

    subtotal = 0

    for product_id, quantity in cart.items():

        product = connection.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

        if product is None:
            continue

        quantity = int(quantity)

        if quantity <= 0:
            continue

        item = dict(product)

        item["id"] = product["id"]
        item["name"] = product["name"]
        item["price"] = float(product["price"])
        item["quantity"] = quantity
        item["stock"] = product["stock"]

        item_total = item["price"] * quantity

        item["item_total"] = item_total

        cart_items.append(item)

        subtotal += item_total

    connection.close()

    shipping = 0 if subtotal == 0 or subtotal >= 5000 else 200

    total = subtotal + shipping

    return cart_items, subtotal, shipping, total


# =========================================
# HOME PAGE
# =========================================

@main.route("/")
def home():

    products = get_all_products()

    return render_template(
        "index.html",
        products=products
    )


# =========================================
# ALL PRODUCTS PAGE
# =========================================

@main.route("/products")
def products():

    all_products = get_all_products()

    return render_template(
        "products.html",
        products=all_products
    )


# =========================================
# PRODUCT DETAILS
# =========================================

@main.route("/product/<int:product_id>")
def product_detail(product_id):

    product = get_product(product_id)

    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("main.products"))

    return render_template(
        "product_detail.html",
        product=product
    )


# =========================================
# ADD TO CART
# =========================================

@main.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    product = get_product(product_id)

    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("main.products"))

    if product["stock"] <= 0:
        flash("This product is out of stock.", "error")
        return redirect(url_for("main.product_detail", product_id=product_id))

    try:
        quantity = int(request.form.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    quantity = max(1, quantity)

    cart = session.get("cart", {})

    current_quantity = int(cart.get(str(product_id), 0))

    new_quantity = current_quantity + quantity

    if new_quantity > product["stock"]:
        flash("Not enough stock available.", "error")
        return redirect(url_for("main.product_detail", product_id=product_id))

    cart[str(product_id)] = new_quantity

    session["cart"] = cart

    flash("Product added to your cart!", "success")

    return redirect(request.referrer or url_for("main.products"))


# =========================================
# CART PAGE
# =========================================

@main.route("/cart")
def cart():

    cart_items, subtotal, shipping, total = get_cart_items()

    return render_template(
        "cart.html",
        cart=cart_items,
        subtotal=subtotal,
        shipping=shipping,
        total=total
    )


# =========================================
# UPDATE CART QUANTITY
# =========================================

@main.route("/update-cart/<int:product_id>", methods=["POST"])
def update_cart(product_id):

    cart = session.get("cart", {})

    try:
        quantity = int(request.form.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    product = get_product(product_id)

    if product is None:
        cart.pop(str(product_id), None)

    elif quantity <= 0:
        cart.pop(str(product_id), None)

    elif quantity > product["stock"]:
        flash("Requested quantity is not available.", "error")

    else:
        cart[str(product_id)] = quantity

    session["cart"] = cart

    return redirect(url_for("main.cart"))


# =========================================
# REMOVE CART ITEM
# =========================================

@main.route("/remove-from-cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):

    cart = session.get("cart", {})

    cart.pop(str(product_id), None)

    session["cart"] = cart

    flash("Product removed from cart.", "success")

    return redirect(url_for("main.cart"))


# =========================================
# CHECKOUT PAGE
# =========================================

@main.route("/checkout")
def checkout():

    cart_items, subtotal, shipping, total = get_cart_items()

    if not cart_items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("main.products"))

    return render_template(
        "checkout.html",
        cart=cart_items,
        subtotal=subtotal,
        shipping=shipping,
        total=total
    )


# =========================================
# PLACE ORDER
# =========================================

@main.route("/place-order", methods=["POST"])
def place_order():

    cart_items, subtotal, shipping, total = get_cart_items()

    if not cart_items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("main.products"))

    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    city = request.form.get("city", "").strip()
    postal_code = request.form.get("postal_code", "").strip()
    payment_method = request.form.get("payment_method", "COD").strip()
    notes = request.form.get("notes", "").strip()

    if not all([full_name, email, phone, address, city]):
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("main.checkout"))

    if payment_method != "COD":
        flash("Only Cash on Delivery is currently available.", "error")
        return redirect(url_for("main.checkout"))

    connection = get_db_connection()

    try:

        # Recheck stock before placing order
        for item in cart_items:

            product = connection.execute(
                "SELECT stock FROM products WHERE id = ?",
                (item["id"],)
            ).fetchone()

            if product is None or product["stock"] < item["quantity"]:
                connection.rollback()
                flash(
                    f"Not enough stock for {item['name']}.",
                    "error"
                )
                return redirect(url_for("main.cart"))

        # Create order
        cursor = connection.execute("""
            INSERT INTO orders (
                full_name,
                email,
                phone,
                address,
                city,
                postal_code,
                payment_method,
                notes,
                total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            email,
            phone,
            address,
            city,
            postal_code,
            payment_method,
            notes,
            total
        ))

        order_id = cursor.lastrowid

        # Save order products and update stock
        for item in cart_items:

            connection.execute("""
                INSERT INTO order_items (
                    order_id,
                    product_id,
                    product_name,
                    quantity,
                    price
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                order_id,
                item["id"],
                item["name"],
                item["quantity"],
                item["price"]
            ))

            connection.execute("""
                UPDATE products
                SET stock = stock - ?
                WHERE id = ?
            """, (
                item["quantity"],
                item["id"]
            ))

        connection.commit()

        session.pop("cart", None)

        return redirect(
            url_for("main.order_success", order_id=order_id)
        )

    except Exception:

        connection.rollback()

        flash("Something went wrong. Please try again.", "error")

        return redirect(url_for("main.checkout"))

    finally:
        connection.close()


# =========================================
# ORDER SUCCESS PAGE
# =========================================

@main.route("/order-success/<int:order_id>")
def order_success(order_id):

    connection = get_db_connection()

    order = connection.execute(
        "SELECT * FROM orders WHERE id = ?",
        (order_id,)
    ).fetchone()

    connection.close()

    if order is None:
        flash("Order not found.", "error")
        return redirect(url_for("main.home"))

    return render_template(
        "order_success.html",
        order_id=order["id"],
        total=order["total"]
    )
