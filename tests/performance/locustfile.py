"""
Performance tests for E-commerce Microservices
Uses Locust for load testing and performance monitoring
Run with: locust -f locustfile.py --host=http://localhost:5000
"""
from locust import HttpUser, task, between
import random
import json


class UserServiceUser(HttpUser):
    """
    Simulates user behavior for the User Service
    Tests authentication, registration, and profile operations
    """
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Called when a simulated user starts"""
        # Register a test user
        username = f"loadtest_user_{random.randint(1, 100000)}"
        self.user_data = {
            "username": username,
            "email": f"{username}@loadtest.com",
            "password": "LoadTest123!"
        }
        
        # Register
        response = self.client.post(
            "/api/users/register",
            json=self.user_data,
            name="/api/users/register [POST]"
        )
        
        if response.status_code == 201:
            # Login and get token
            login_response = self.client.post(
                "/api/users/login",
                json={
                    "username": self.user_data["username"],
                    "password": self.user_data["password"]
                },
                name="/api/users/login [POST]"
            )
            
            if login_response.status_code == 200:
                data = login_response.json()
                self.token = data.get("token")
                self.user_id = data.get("user", {}).get("id")
                self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def health_check(self):
        """Test health endpoint - low weight"""
        self.client.get("/health", name="/health [GET]")
    
    @task(10)
    def login(self):
        """Test user login - high weight (common operation)"""
        self.client.post(
            "/api/users/login",
            json={
                "username": self.user_data["username"],
                "password": self.user_data["password"]
            },
            name="/api/users/login [POST]"
        )
    
    @task(5)
    def get_profile(self):
        """Test getting user profile"""
        if hasattr(self, 'headers') and hasattr(self, 'user_id'):
            self.client.get(
                f"/api/users/{self.user_id}",
                headers=self.headers,
                name="/api/users/{id} [GET]"
            )
    
    @task(2)
    def update_profile(self):
        """Test updating user profile"""
        if hasattr(self, 'headers') and hasattr(self, 'user_id'):
            update_data = {
                "email": f"updated_{random.randint(1, 1000)}@loadtest.com"
            }
            self.client.put(
                f"/api/users/{self.user_id}",
                json=update_data,
                headers=self.headers,
                name="/api/users/{id} [PUT]"
            )


class ProductServiceUser(HttpUser):
    """
    Simulates user behavior for the Product Service
    Tests product browsing, search, and CRUD operations
    """
    wait_time = between(1, 5)
    host = "http://localhost:8080"  # Product service runs on 8080
    
    @task(10)
    def browse_products(self):
        """Test browsing all products - most common operation"""
        self.client.get("/api/products", name="/api/products [GET]")
    
    @task(8)
    def view_product_details(self):
        """Test viewing specific product"""
        product_id = random.randint(1, 100)
        self.client.get(
            f"/api/products/{product_id}",
            name="/api/products/{id} [GET]"
        )
    
    @task(5)
    def search_products(self):
        """Test product search"""
        keywords = ["laptop", "phone", "tablet", "monitor", "keyboard"]
        keyword = random.choice(keywords)
        self.client.get(
            f"/api/products/search?keyword={keyword}",
            name="/api/products/search [GET]"
        )
    
    @task(3)
    def browse_by_category(self):
        """Test browsing products by category"""
        categories = ["Electronics", "Clothing", "Books", "Home"]
        category = random.choice(categories)
        self.client.get(
            f"/api/products/category/{category}",
            name="/api/products/category/{cat} [GET]"
        )
    
    @task(1)
    def check_low_stock(self):
        """Test low stock alert - admin operation"""
        self.client.get(
            "/api/products/low-stock?threshold=10",
            name="/api/products/low-stock [GET]"
        )
    
    @task(2)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/api/products/health", name="/api/products/health [GET]")


class MixedWorkloadUser(HttpUser):
    """
    Simulates realistic e-commerce user journey
    Combines interactions across multiple services
    """
    wait_time = between(2, 6)
    
    @task
    def user_shopping_journey(self):
        """
        Simulates a complete shopping journey:
        1. Browse products
        2. Search for specific items
        3. View product details
        4. Check user profile
        """
        # Browse products (Product Service - port 8080)
        self.client.get(
            "http://localhost:8080/api/products",
            name="Journey: Browse products"
        )
        
        # Search for something
        self.client.get(
            "http://localhost:8080/api/products/search?keyword=laptop",
            name="Journey: Search products"
        )
        
        # View specific product
        product_id = random.randint(1, 50)
        self.client.get(
            f"http://localhost:8080/api/products/{product_id}",
            name="Journey: View product"
        )
        
        # Check if user is logged in (User Service - port 5000)
        self.client.get(
            "http://localhost:5000/health",
            name="Journey: Check user service"
        )
