const app = {
    state: {
        user: null,
        cart: null,
        products: [],
        categories: [],
        jewelers: [],
        currentDesign: null
    },

    init() {
        this.checkAuth();
        this.setupEventListeners();
        this.loadProducts();
        this.loadCategories();
        this.loadJewelers();
        this.loadCart();
    },

    async checkAuth() {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const user = await API.getCurrentUser();
                this.state.user = user;
                this.updateAuthUI();
            } catch (error) {
                localStorage.removeItem('token');
            }
        }
    },

    updateAuthUI() {
        const loginBtn = document.getElementById('loginBtn');
        const logoutBtn = document.getElementById('logoutBtn');
        
        if (this.state.user) {
            loginBtn.style.display = 'none';
            logoutBtn.style.display = 'block';
        } else {
            loginBtn.style.display = 'block';
            logoutBtn.style.display = 'none';
        }
    },

    setupEventListeners() {
        // Auth
        document.getElementById('loginBtn').addEventListener('click', () => this.openModal('loginModal'));
        document.getElementById('logoutBtn').addEventListener('click', () => this.logout());
        document.getElementById('loginForm').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('registerForm').addEventListener('submit', (e) => this.handleRegister(e));
        document.getElementById('showRegister').addEventListener('click', (e) => {
            e.preventDefault();
            this.closeModal('loginModal');
            this.openModal('registerModal');
        });
        document.getElementById('showLogin').addEventListener('click', (e) => {
            e.preventDefault();
            this.closeModal('registerModal');
            this.openModal('loginModal');
        });

        // Cart
        document.querySelector('.cart-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.openModal('cartModal');
            this.renderCart();
        });
        document.getElementById('checkoutBtn').addEventListener('click', () => this.handleCheckout());

        // Filters
        document.getElementById('filterBtn').addEventListener('click', () => this.handleFilter());

        // AI Design
        document.getElementById('aiDesignForm').addEventListener('submit', (e) => this.handleGenerateDesign(e));
        document.getElementById('requestDesignBtn').addEventListener('click', () => this.openDesignRequestModal());
        document.getElementById('designRequestForm').addEventListener('submit', (e) => this.handleDesignRequest(e));

        // Close modals
        document.querySelectorAll('.close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                modal.style.display = 'none';
            });
        });

        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    },

    openModal(modalId) {
        document.getElementById(modalId).style.display = 'block';
    },

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    },

    async handleLogin(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const data = await API.login(formData.get('username'), formData.get('password'));
            localStorage.setItem('token', data.access_token);
            const user = await API.getCurrentUser();
            this.state.user = user;
            this.updateAuthUI();
            this.closeModal('loginModal');
            this.showMessage('تم تسجيل الدخول بنجاح!');
            this.loadCart();
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const userData = Object.fromEntries(formData);
        try {
            await API.register(userData);
            this.showMessage('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول');
            this.closeModal('registerModal');
            this.openModal('loginModal');
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    },

    logout() {
        localStorage.removeItem('token');
        this.state.user = null;
        this.updateAuthUI();
        this.showMessage('تم تسجيل الخروج');
    },

    async loadProducts(filters = {}) {
        try {
            this.state.products = await API.getProducts(filters);
            this.renderProducts();
        } catch (error) {
            console.error('Error loading products:', error);
        }
    },

    async loadCategories() {
        try {
            this.state.categories = await API.getCategories();
            const select = document.getElementById('categoryFilter');
            this.state.categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.name;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    },

    async loadJewelers() {
        // Mock data for now - should fetch from API
        this.state.jewelers = [
            { id: 1, name: 'عبدالله السيد', shop_name: 'مجوهرات السيد', bio: 'خبرة 30 عاماً في صناعة المجوهرات', rating: 4.8 },
            { id: 2, name: 'نورة الماس', shop_name: 'نورة للمجوهرات الفاخرة', bio: 'تصاميم حصرية ونادرة', rating: 4.9 },
            { id: 3, name: 'الحرفي الذهبي', shop_name: 'استوديو الحرفي', bio: 'حرفية تقليدية وتصاميم عصرية', rating: 4.7 }
        ];
        this.renderJewelers();
    },

    async loadCart() {
        if (!this.state.user) return;
        try {
            this.state.cart = await API.getCart();
            this.updateCartCount();
        } catch (error) {
            console.error('Error loading cart:', error);
        }
    },

    updateCartCount() {
        const count = this.state.cart?.items?.reduce((sum, item) => sum + item.quantity, 0) || 0;
        document.querySelector('.cart-count').textContent = count;
    },

    renderProducts() {
        const grid = document.getElementById('productsGrid');
        grid.innerHTML = this.state.products.map(product => `
            <div class="product-card">
                <div class="product-image">💎</div>
                <div class="product-info">
                    <h3>${product.name}</h3>
                    <p class="product-price">${product.price} ريال</p>
                    <p class="product-meta">${product.material} ${product.karat} - ${product.weight}g</p>
                    <button class="btn btn-primary" onclick="app.addToCart(${product.id})">
                        أضف للسلة
                    </button>
                </div>
            </div>
        `).join('');
    },

    renderJewelers() {
        const grid = document.getElementById('jewelersGrid');
        grid.innerHTML = this.state.jewelers.map(jeweler => `
            <div class="jeweler-card">
                <h3>${jeweler.name}</h3>
                <p class="jeweler-shop">${jeweler.shop_name}</p>
                <p class="jeweler-rating">⭐ ${jeweler.rating}</p>
                <p class="jeweler-bio">${jeweler.bio}</p>
            </div>
        `).join('');
    },

    renderCart() {
        const container = document.getElementById('cartItems');
        if (!this.state.cart?.items?.length) {
            container.innerHTML = '<p>السلة فارغة</p>';
            document.getElementById('cartTotal').textContent = '0';
            return;
        }

        let total = 0;
        container.innerHTML = this.state.cart.items.map(item => {
            total += item.product.price * item.quantity;
            return `
                <div class="cart-item">
                    <div class="cart-item-info">
                        <h4>${item.product.name}</h4>
                        <p>${item.quantity} × ${item.product.price} ريال</p>
                    </div>
                    <div>
                        <span class="cart-item-price">${item.product.price * item.quantity} ريال</span>
                        <button class="btn btn-danger" onclick="app.removeFromCart(${item.id})">حذف</button>
                    </div>
                </div>
            `;
        }).join('');

        document.getElementById('cartTotal').textContent = total;
    },

    async addToCart(productId) {
        if (!this.state.user) {
            this.showMessage('يرجى تسجيل الدخول أولاً', 'error');
            this.openModal('loginModal');
            return;
        }
        try {
            await API.addToCart(productId);
            await this.loadCart();
            this.showMessage('تمت الإضافة للسلة!');
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    },

    async removeFromCart(itemId) {
        try {
            await API.removeFromCart(itemId);
            await this.loadCart();
            this.renderCart();
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    },

    handleFilter() {
        const filters = {
            category_id: document.getElementById('categoryFilter').value,
            material: document.getElementById('materialFilter').value,
            min_price: document.getElementById('minPrice').value,
            max_price: document.getElementById('maxPrice').value
        };
        this.loadProducts(filters);
    },

    async handleGenerateDesign(e) {
        e.preventDefault();
        if (!this.state.user) {
            this.showMessage('يرجى تسجيل الدخول أولاً', 'error');
            this.openModal('loginModal');
            return;
        }

        const formData = new FormData(e.target);
        const designData = Object.fromEntries(formData);
        
        const btn = e.target.querySelector('button[type="submit"]');
        const btnText = btn.querySelector('.btn-text');
        const loading = btn.querySelector('.loading');
        
        btnText.style.display = 'none';
        loading.style.display = 'inline';
        btn.disabled = true;

        try {
            const result = await API.generateDesign(designData);
            this.state.currentDesign = result;
            
            document.getElementById('generatedImage').src = `http://localhost:8000${result.generated_image_url}`;
            document.getElementById('generatedDesignResult').style.display = 'block';
            
            this.showMessage('تم توليد التصميم بنجاح!');
        } catch (error) {
            this.showMessage(error.message, 'error');
        } finally {
            btnText.style.display = 'inline';
            loading.style.display = 'none';
            btn.disabled = false;
        }
    },

    openDesignRequestModal() {
        const select = document.getElementById('jewelerSelect');
        select.innerHTML = this.state.jewelers.map(j => 
            `<option value="${j.id}">${j.name} - ${j.shop_name}</option>`
        ).join('');
        this.openModal('designRequestModal');
    },

    async handleDesignRequest(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const requestData = {
            jeweler_id: parseInt(formData.get('jeweler_id')),
            generated_design_id: this.state.currentDesign?.id,
            description: formData.get('description'),
            estimated_budget: formData.get('estimated_budget') ? parseFloat(formData.get('estimated_budget')) : null
        };

        try {
            await API.createDesignRequest(requestData);
            this.showMessage('تم إرسال طلبك بنجاح!');
            this.closeModal('designRequestModal');
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    },

    async handleCheckout() {
        if (!this.state.cart?.items?.length) {
            this.showMessage('السلة فارغة', 'error');
            return;
        }

        const payment_method_id = 1; // Default to bank transfer
        const shipping_address = this.state.user?.address || 'عنوان افتراضي';

        try {
            await API.createOrder({ payment_method_id, shipping_address });
            this.showMessage('تم إنشاء طلبك بنجاح!');
            this.closeModal('cartModal');
            await this.loadCart();
        } catch (error) {
            this.showMessage(error.message, 'error');
        }
    },

    showMessage(message, type = 'success') {
        const div = document.createElement('div');
        div.className = `alert alert-${type}`;
        div.textContent = message;
        div.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 15px 25px;
            background: ${type === 'error' ? '#dc3545' : '#28a745'};
            color: white;
            border-radius: 8px;
            z-index: 9999;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        `;
        document.body.appendChild(div);
        setTimeout(() => div.remove(), 3000);
    }
};

document.addEventListener('DOMContentLoaded', () => app.init());