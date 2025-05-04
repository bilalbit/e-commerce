# E-Commerce FastAPI Project

## Overview

This is a FastAPI-based e-commerce platform designed for managing products, orders, payments, reviews, and more. The API
supports role-based access for `CUSTOMER`, `ADMIN`, and `SELLER` users, secured with JSON Web Token (JWT)
authentication. It includes modular endpoints for categories, user management, products, orders, reviews, wishlists,
addresses, scam reports, notifications, and carts.

### Features

- **Categories**: Manage product categories.
- **Users**: User authentication, profile management, and password operations.
- **Products**: Create, update, and manage product inventory.
- **Orders**: Process and track customer orders.
- **Reviews**: Submit and manage product reviews.
- **Wishlist**: Allow users to save products for later.
- **Addresses**: Manage user shipping addresses.
- **Scam Reports**: Report and manage potential fraud.
- **Notifications**: Send and manage user notifications.
- **Cart**: Manage shopping cart items.
- **Security**: JWT-based authentication with role-based authorization.
- **Utilities**: Secure password hashing using `bcrypt`.

## Project Structure

```
ecommerce/
├── backend/
│   ├── modules/
│   │   ├── categories/    # Category management
│   │   ├── users/         # User management
│   │   ├── products/      # Product management
│   │   ├── orders/        # Order processing
│   │   ├── reviews/       # Review submission
│   │   ├── wishlists/     # Wishlist management
│   │   ├── addresses/     # Address management
│   │   ├── scam_reports/  # Scam report handling
│   │   ├── notifications/ # Notification system
│   │   ├── carts/         # Cart management
│   ├── database.py        # Database session management
│   ├── security.py        # JWT authentication and role-based authorization
│   ├── utils.py           # Password hashing and verification
│   ├── main.py            # FastAPI app entry point
│   ├── pyproject.toml     # Project metadata and dependencies (managed by uv)
│   ├── README.md          # Backend documentation
├── frontend/              # Frontend code (if applicable)
├── README.md              # Root repository documentation
```

## Module Operations

| Module       | Operations                                                                                                                               |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Category     | create_category, get_category_by_id, get_all_categories, update_category, delete_category                                                |
| User         | create_user, get_user_by_id, get_user_by_email, update_user, delete_user, authenticate_user, change_password, reset_password             |
| Product      | create_product, get_product_by_id, **get_all_products**, update_product, delete_product, get_products_by_seller, update_product_stock    |
| Order        | create_order, get_order_by_id, get_all_orders, update_order_status, delete_order, get_orders_by_user, cancel_order                       |
| Review       | create_review, get_review_by_id, get_reviews_by_product, **update_review**, delete_review, get_reviews_by_user                           |
| Wishlist     | add_to_wishlist, get_wishlist_by_user, remove_from_wishlist, clear_wishlist                                                              |
| Address      | create_address, get_address_by_id, get_addresses_by_user, update_address, delete_address, set_default_address                            |
| Scam Report  | create_scam_report, get_scam_report_by_id, get_all_scam_reports, update_scam_report_status, delete_scam_report, get_scam_reports_by_user |
| Notification | send_notification, get_user_notifications, mark_notification_as_read, delete_notification                                                |
| Cart         | add_to_cart, get_cart_by_user, update_cart_item, remove_from_cart, clear_cart                                                            |

## Prerequisites

- Python 3.8+
- MySQL/PostgreSQL database
- [uv](https://github.com/astral-sh/uv) (Python package and dependency manager)
- Environment variables (see `backend/.env.example`)

## Setup and Installation

This project uses **uv** for dependency management and running the application. Follow these steps to set up and start
the project from the `ecommerce/backend` folder:

1. **Install uv**:
    - Install uv by following the instructions at [uv GitHub](https://github.com/astral-sh/uv).
    - Example for Linux/macOS:
      ```bash
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```
    - For Windows, use PowerShell:
      ```powershell
      powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
      ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/bilal-dev-bit/e-commerce.git
   cd ecommerce
   ```

3. **Initialize the Project with uv**:
    - Navigate to the backend folder:
      ```bash
      cd backend
      ```
    - Create a virtual environment and install dependencies defined in `pyproject.toml`:
      ```bash
      uv venv
      source .venv/bin/activate  # On Windows: .venv\Scripts\activate
      uv sync
      ```

4. **Configure Environment Variables**:
    - Copy `backend/.env.example` to `backend/.env` and update values:
      ```env
      DATABASE_URL=mysql://user:password@localhost:3306/ecommerce
      SECRET_KEY=your-secret-key
      ALGORITHM=HS256
      ACCESS_TOKEN_EXPIRE_MINUTES=60
      ```
    - Generate a secure `SECRET_KEY` (e.g., using `openssl rand -hex 32`).

5. **Set Up the Database**:
    - Create the database:
      ```sql
      CREATE DATABASE ecommerce;
      ```
    - Initialize the database schema using the `db-init` endpoint:
       ```bash
       uv run uvicorn main:app --host 0.0.0.0 --port 8000 &
       curl -X POST "http://localhost:8000/db-init"
       ```
    - Stop the temporary server (Ctrl+C) after initialization.

6. **Run the Application**:
    - Start the FastAPI server from the `backend` folder:
      ```bash
      uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
      ```
    - Access the API at `http://localhost:8000`.
    - Interactive docs at `http://localhost:8000/docs`.

## API Usage

### Authentication

- **Login**: Obtain a JWT token via `POST /auth/login`.
  ```bash
  curl -X POST "http://localhost:8000/auth/login" \
       -d "username=user@example.com&password=yourpassword"
  ```
    - Response: `{"access_token": "your-jwt-token", "token_type": "bearer"}`
- **Protected Endpoints**: Include the JWT in the `Authorization` header:
  ```
  Authorization: Bearer your-jwt-token
  ```

### Roles

- `CUSTOMER`: Access products, orders, reviews, wishlists, addresses, carts, and scam reports.
- `ADMIN`: Manage categories, users, orders, scam reports, notifications, and moderate reviews.
- `SELLER`: Manage products and view reviews.

### Key Endpoints

#### Categories

- **POST /categories**: Create a category (Admin).
  ```json
  {
      "name": "Electronics"
  }
  ```

#### Users

- **POST /auth/register**: Register a new user.
  ```json
  {
      "email": "user@example.com",
      "password": "securepassword",
      "role": "CUSTOMER"
  }
  ```

#### Products

- **POST /products**: Create a product (Seller).
  ```json
  {
      "name": "Laptop",
      "price": 999.99,
      "category_id": 1,
      "stock": 50
  }
  ```

#### Orders

- **POST /orders**: Create an order (Customer).
  ```json
  {
      "items": [{"product_id": 1, "quantity": 2}]
  }
  ```

#### Reviews

- **POST /reviews**: Submit a review (Customer).
  ```json
  {
      "product_id": 1,
      "order_id": 1,
      "rating": 5,
      "comment": "Great product!"
  }
  ```

#### Wishlist

- **POST /wishlist**: Add to wishlist (Customer).
  ```json
  {
      "product_id": 1
  }
  ```

#### Addresses

- **POST /addresses**: Create an address (Customer).
  ```json
  {
      "street": "123 Main St",
      "city": "Anytown",
      "country": "USA"
  }
  ```

#### Scam Reports

- **POST /scam-reports**: Report a scam (Customer).
  ```json
  {
      "product_id": 1,
      "description": "Suspicious seller"
  }
  ```

#### Notifications

- **GET /notifications**: Get user notifications (Customer).
  ```bash
  curl -H "Authorization: Bearer your-jwt-token" "http://localhost:8000/notifications"
  ```

#### Cart

- **POST /cart**: Add to cart (Customer).
  ```json
  {
      "product_id": 1,
      "quantity": 2
  }
  ```

For detailed endpoint documentation, see `/docs` (Swagger UI).

## Modules

### Categories

- Manage product categories for organization.

### Users

- Handle user registration, authentication, and profile updates.

### Products

- Create and manage products, including stock updates.

### Orders

- Process customer orders and track status.

### Reviews

- Allow customers to review products, with admin moderation.

### Wishlist

- Enable customers to save products for later purchase.

### Addresses

- Manage customer shipping addresses.

### Scam Reports

- Allow reporting and management of potential fraud.

### Notifications

- Send and manage user notifications.

### Cart

- Manage shopping cart items for checkout.

## Security

- **Authentication**: JWT-based, with tokens issued via `POST /auth/login`.
- **Authorization**: Role-based access implemented in `security.py`:
    - `get_current_customer`: Restricts to `CUSTOMER` role for orders, reviews, etc.
    - `get_current_admin`: Restricts to `ADMIN` role for category management, scam report moderation.
    - `get_current_seller`: Restricts to `SELLER` role for product management.
- **Password Hashing**: Handled in `utils.py` using `bcrypt`.

## Utilities

- **utils.py**:
    - `hash_password`: Hashes passwords using `bcrypt`.
    - `verify_password`: Verifies passwords during login.

## Database Schema

- **categories**: `category_id`, `name`.
- **users**: `user_id`, `email`, `hashed_password`, `role`.
- **products**: `product_id`, `name`, `price`, `category_id`, `seller_id`, `stock`.
- **orders**: `order_id`, `customer_id`, `total_amount`, `status`.
- **reviews**: `review_id`, `product_id`, `user_id`, `rating`, `comment`.
- **wishlist**: `user_id`, `product_id`.
- **addresses**: `address_id`, `user_id`, `street`, `city`, `country`, `is_default`.
- **notifications**: `notification_id`, `user_id`, `message`, `is_read`.
- **cart**: `user_id`, `product_id`, `quantity`.

## License

MIT License. See `LICENSE` for details.

## Contact

For issues or questions, open a GitHub issue or contact [bilalmulugeta1610@gmail.com].