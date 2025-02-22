# Clothing Store API

## 👤 Developers: Alikhan, Ilyas

### 📌 Overview
This project is a REST API for a clothing store, built with Flask and MongoDB. The API enables user authentication, product management, shopping cart functionality, and order processing.

### ⚡ Features
- ✅ User Authentication (Signup, Login, JWT tokens)
- ✅ Product Management (Create, Read, Update, Delete – CRUD)
- ✅ Shopping Cart (Add, Remove, View)
- ✅ Optimized MongoDB with Indexes (`id`, `category`, `price`)
- ✅ API Documentation
- ✅ Deployment on Render

### 📂 Project Structure
```
clothing_store_backend/
│── app.py              # Main Flask server
│── frontend/             # Frontend assets (CSS, JS, HTML)
|   ├── app.js
|   ├── index.html
|   ├── cart.html
|   ├── cart.js
|   ├── login.html
|   ├── profile.html
|   ├── signup.html
|   ├── user.js
|   ├── style.css                      
│── requirements.txt     # Dependencies
│── .env                 # Environment variables (ignored in Git)
│── .gitignore           # Ignored files
│── README.md            # Documentation
```

### 📦 Database Structure (MongoDB)

#### **Users Collection (`users`):**
```json
{
  "_id": ObjectId,
  "username": "test",
  "email": "test@example.com",
  "password": "hashed_password",  
  "role": "user",  
  "avatar": "https://example.com/avatar.jpg"
}
```

#### **Products Collection (`products`):**
```json
db.products.insertOne({
    _id: "https://moyo.moda/product/1099999",
    id: "1099999",
    name: "ОРИОН",
    price: "520 ₽",
    image_url: "https://cdn0.moyo.moda/ws/main/316x474/9999999.jpg",
    colors: ["black", "white", "red"],
    url: "https://moyo.moda/product/1099999",
    category: "muzhskie-maiki-futbolki"
});

###  Getting Started

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/QaissAA/nosql_finalproj
```

#### 2️⃣ Set Up a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

#### 3️⃣ Configure Environment Variables (`.env`)
Create a `.env` file and add:
```ini
SECRET_KEY=your_secret_key
MONGO_URI=your_mongo_uri
```

#### 4️⃣ Run the Server
```bash
flask run
```
API will be available at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### 📡 API Endpoints

#### 1. Authentication
| Method | Endpoint  | Description |
|--------|----------|-------------|
| POST   | `/signup` | Register a new user |
| POST   | `/login`  | Log in a user, returns JWT |

#### 2. Product Management
| Method | Endpoint        | Description |
|--------|----------------|-------------|
| GET    | `/products`     | Fetch all products |
| POST   | `/products`     | Add a new product (admin only) |
| PUT    | `/products/:id` | Update a product (admin only) |
| DELETE | `/products/:id` | Delete a product (admin only) |

#### 3. Shopping Cart
| Method  | Endpoint                  | Description |
|---------|---------------------------|-------------|
| POST    | `/cart`                    | Add product to cart |
| GET     | `/cart/:userId`            | View user’s cart |
| DELETE  | `/cart/:userId/:productId` | Remove product from cart |
