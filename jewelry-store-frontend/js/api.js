const API_BASE_URL = 'http://localhost:8000';

class API {
    static getToken() {
        return localStorage.getItem('token');
    }

    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const token = this.getToken();
        
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` }),
                ...options.headers
            },
            ...options
        };

        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(url, config);
            
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.reload();
                return;
            }

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'حدث خطأ');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth
    static async login(username, password) {
        return this.request('/api/auth/login', {
            method: 'POST',
            body: { username, password }
        });
    }

    static async register(userData) {
        return this.request('/api/auth/register', {
            method: 'POST',
            body: userData
        });
    }

    static async getCurrentUser() {
        return this.request('/api/auth/me');
    }

    // Products
    static async getProducts(filters = {}) {
        const queryParams = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) queryParams.append(key, value);
        });
        return this.request(`/api/products/?${queryParams.toString()}`);
    }

    static async getProduct(id) {
        return this.request(`/api/products/${id}`);
    }

    // Categories
    static async getCategories() {
        return this.request('/api/categories/');
    }

    // Cart
    static async getCart() {
        return this.request('/api/carts/');
    }

    static async addToCart(productId, quantity = 1) {
        return this.request('/api/carts/items', {
            method: 'POST',
            body: { product_id: productId, quantity }
        });
    }

    static async removeFromCart(itemId) {
        return this.request(`/api/carts/items/${itemId}`, {
            method: 'DELETE'
        });
    }

    static async clearCart() {
        return this.request('/api/carts/clear', {
            method: 'DELETE'
        });
    }

    // Orders
    static async createOrder(orderData) {
        return this.request('/api/orders/', {
            method: 'POST',
            body: orderData
        });
    }

    static async getOrders() {
        return this.request('/api/orders/');
    }

    // AI Design
    static async generateDesign(designData) {
        return this.request('/api/ai/generate-design', {
            method: 'POST',
            body: designData
        });
    }

    static async getUserDesigns() {
        return this.request('/api/designs');
    }

    static async createDesignRequest(requestData) {
        return this.request('/api/design-requests', {
            method: 'POST',
            body: requestData
        });
    }

    static async getDesignRequests() {
        return this.request('/api/design-requests');
    }
}