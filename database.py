
import sqlite3

DATABASE = "velora.db"


# =========================================
# DATABASE CONNECTION
# =========================================

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================
# INITIALIZE DATABASE
# =========================================

def init_db():

    connection = get_db_connection()

    cursor = connection.cursor()

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT,
            stock INTEGER DEFAULT 10
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            postal_code TEXT,
            payment_method TEXT NOT NULL,
            notes TEXT,
            total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Order items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)

    connection.commit()

    # Add sample products only if database is empty
    cursor.execute("SELECT COUNT(*) FROM products")

    product_count = cursor.fetchone()[0]

    if product_count == 0:

        sample_products = [

            (
                "Wireless Headphones",
                "Electronics",
                4500,
                "Premium wireless headphones with immersive sound.",
                "headphones.jpg",
                15
            ),

            (
                "Smart Watch",
                "Electronics",
                6500,
                "Modern smartwatch with smart features.",
                "smartwatch.jpg",
                12
            ),

            (
                "Premium Hoodie",
                "Fashion",
                3200,
                "Comfortable premium everyday hoodie.",
                "hoodie.jpg",
                20
            ),

            (
                "Running Shoes",
                "Shoes",
                5200,
                "Lightweight shoes designed for everyday comfort.",
                "shoes.jpg",
                10
            ),

            (
                "Gaming Mouse",
                "Gaming",
                2800,
                "High precision gaming mouse.",
                "mouse.jpg",
                18
            ),

            (
                "Leather Wallet",
                "Accessories",
                1800,
                "Minimal premium leather wallet.",
                "wallet.jpg",
                25
            ),

            (
                "Classic Sunglasses",
                "Accessories",
                2200,
                "Stylish sunglasses for everyday use.",
                "sunglasses.jpg",
                14
            ),

            (
                "Beauty Essentials Kit",
                "Beauty",
                3500,
                "A collection of everyday beauty essentials.",
                "beauty.jpg",
                16
            )

        ]

        cursor.executemany("""
            INSERT INTO products
            (name, category, price, description, image, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_products)

    connection.commit()
    connection.close()


# =========================================
# GET ALL PRODUCTS
# =========================================

def get_all_products():

    connection = get_db_connection()

    products = connection.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return products


# =========================================
# GET SINGLE PRODUCT
# =========================================

def get_product(product_id):

    connection = get_db_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    return product
