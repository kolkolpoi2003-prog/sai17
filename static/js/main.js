/**
 * OptikaStore — Main JavaScript
 * AJAX cart, live search, scroll animations, mobile menu, toasts
 */

document.addEventListener('DOMContentLoaded', () => {
    initScrollAnimations();
    initMobileMenu();
    initHeaderScroll();
    initCartButtons();
    initWishlistButtons();
    initLiveSearch();
    initCartPage();
});

// ============================================
// CSRF Token
// ============================================
function getCSRFToken() {
    const cookie = document.cookie.match(/csrftoken=([^;]+)/);
    if (cookie) return cookie[1];
    const meta = document.querySelector('[name=csrfmiddlewaretoken]');
    return meta ? meta.value : '';
}

// ============================================
// Toast Notifications
// ============================================
function showToast(message, duration = 2500) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) both';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// ============================================
// Scroll Animations (Intersection Observer)
// ============================================
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger animations based on position
                const delay = entry.target.classList.contains('product-card')
                    ? index * 60
                    : 0;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, delay);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.scroll-animate, .product-card').forEach(el => {
        observer.observe(el);
    });
}

// ============================================
// Mobile Menu
// ============================================
function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    const closeBtn = document.getElementById('mobile-menu-close');

    if (!btn || !menu) return;

    btn.addEventListener('click', () => {
        menu.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            menu.classList.add('hidden');
            document.body.style.overflow = '';
        });
    }

    // Close on link click
    menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.add('hidden');
            document.body.style.overflow = '';
        });
    });
}

// ============================================
// Header Shadow on Scroll
// ============================================
function initHeaderScroll() {
    const header = document.getElementById('main-header');
    if (!header) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                if (window.scrollY > 20) {
                    header.classList.add('header-scrolled');
                } else {
                    header.classList.remove('header-scrolled');
                }
                ticking = false;
            });
            ticking = true;
        }
    });
}

// ============================================
// AJAX Add to Cart
// ============================================
function initCartButtons() {
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.add-to-cart-btn');
        if (!btn || btn.id === 'detail-add-to-cart') return;

        e.preventDefault();
        const productId = btn.dataset.productId;
        if (!productId) return;

        btn.disabled = true;
        const originalText = btn.textContent;

        fetch(`/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken(),
            },
            body: 'quantity=1'
        })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') {
                    // Update cart counter
                    const counter = document.getElementById('cart-count');
                    if (counter) {
                        counter.textContent = data.total_items;
                        counter.classList.remove('hidden');
                    }

                    // Bounce animation on cart icon
                    const cartIcon = document.getElementById('cart-icon');
                    if (cartIcon) {
                        cartIcon.classList.add('cart-bounce');
                        setTimeout(() => cartIcon.classList.remove('cart-bounce'), 400);
                    }

                    // Button feedback
                    btn.textContent = '✓ Добавлено';
                    btn.classList.add('bg-emerald-800');
                    showToast('Товар добавлен в корзину');

                    setTimeout(() => {
                        btn.textContent = originalText;
                        btn.classList.remove('bg-emerald-800');
                        btn.disabled = false;
                    }, 1500);
                }
            })
            .catch(() => {
                btn.textContent = originalText;
                btn.disabled = false;
                showToast('Ошибка, попробуйте снова');
            });
    });
}

function initWishlistButtons() {
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.wishlist-btn, .wishlist-remove-btn');
        if (!btn) return;

        e.preventDefault();
        const productId = btn.dataset.productId;
        if (!productId) return;

        const isExplicitRemove = btn.classList.contains('wishlist-remove-btn');

        fetch(`/accounts/wishlist/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken(),
            },
        })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') {
                    // Update the main heart button if it exists on the page
                    const wishlistBtns = document.querySelectorAll(`.wishlist-btn[data-product-id="${productId}"]`);
                    wishlistBtns.forEach(wBtn => {
                        const svg = wBtn.querySelector('svg');
                        if (data.added) {
                            svg.setAttribute('fill', '#ef4444');
                            svg.setAttribute('stroke', '#ef4444');
                            svg.classList.add('text-red-500', 'fill-current');
                            wBtn.title = 'Удалить из избранного';
                        } else {
                            svg.setAttribute('fill', 'none');
                            svg.setAttribute('stroke', 'currentColor');
                            svg.classList.remove('text-red-500', 'fill-current');
                            wBtn.title = 'В избранное';
                        }
                    });

                    if (data.added) {
                        showToast('Добавлено в избранное');
                    } else {
                        showToast('Удалено из избранного');

                        // Handle removal from wishlist page or explicit remove button
                        if (window.location.pathname.includes('/wishlist/') || isExplicitRemove) {
                            const card = btn.closest('.product-card');
                            if (card) {
                                card.style.opacity = '0';
                                card.style.transform = 'scale(0.95)';
                                card.style.transition = 'all 0.3s ease';
                                setTimeout(() => {
                                    card.remove();
                                    // If no more items, show the empty message
                                    const grid = document.querySelector('.product-grid');
                                    if (grid && !grid.querySelector('.product-card')) {
                                        location.reload();
                                    }
                                }, 300);
                            }
                        }
                    }
                }
            });
    });
}

// ============================================
// Live Search
// ============================================
function initLiveSearch() {
    const input = document.getElementById('search-input');
    const results = document.getElementById('search-results');
    if (!input || !results) return;

    let debounceTimer;

    input.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        const query = input.value.trim();

        if (query.length < 2) {
            results.classList.add('hidden');
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/search/?q=${encodeURIComponent(query)}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(r => r.json())
                .then(data => {
                    if (data.results && data.results.length > 0) {
                        results.innerHTML = data.results.map(item => `
                        <a href="${item.url}" class="search-result-item">
                            ${item.image ? `<img src="${item.image}" class="w-10 h-10 object-contain rounded-lg bg-gray-50" alt="">` : ''}
                            <div class="flex-1 min-w-0">
                                <p class="text-sm font-medium text-gray-800 truncate">${item.name}</p>
                                <p class="text-sm text-emerald-600 font-bold">${parseInt(item.price).toLocaleString('ru-RU')} ₽</p>
                            </div>
                        </a>
                    `).join('');
                        results.classList.remove('hidden');
                    } else {
                        results.innerHTML = '<div class="p-4 text-sm text-gray-400 text-center">Ничего не найдено</div>';
                        results.classList.remove('hidden');
                    }
                });
        }, 300);
    });

    // Close search results on click outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('#search-wrapper')) {
            results.classList.add('hidden');
        }
    });
}

// ============================================
// Cart Page Interactivity
// ============================================
function initCartPage() {
    // Quantity buttons on cart page
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.cart-qty-btn');
        if (!btn) return;

        const productId = btn.dataset.productId;
        const item = btn.closest('.cart-item');
        const qtyEl = item.querySelector('.cart-qty-value');
        let qty = parseInt(qtyEl.textContent);

        if (btn.dataset.action === 'plus') {
            qty += 1;
        } else {
            qty -= 1;
        }

        if (qty < 1) {
            // Remove item
            removeCartItem(productId, item);
            return;
        }

        fetch(`/cart/update/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken(),
            },
            body: `quantity=${qty}`
        })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') {
                    qtyEl.textContent = qty;
                    updateCartTotals(data);
                }
            });
    });

    // Remove buttons on cart page
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.cart-remove-btn');
        if (!btn) return;

        const productId = btn.dataset.productId;
        const item = btn.closest('.cart-item');
        removeCartItem(productId, item);
    });
}

function removeCartItem(productId, itemEl) {
    fetch(`/cart/remove/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken(),
        },
    })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'ok') {
                itemEl.style.transition = 'all 0.3s ease';
                itemEl.style.opacity = '0';
                itemEl.style.transform = 'translateX(30px)';
                setTimeout(() => {
                    itemEl.remove();
                    updateCartTotals(data);
                    if (data.total_items === 0) {
                        location.reload();
                    }
                }, 300);
            }
        });
}

function updateCartTotals(data) {
    const counter = document.getElementById('cart-count');
    if (counter) {
        counter.textContent = data.total_items;
        if (data.total_items === 0) counter.classList.add('hidden');
    }

    const totalItems = document.getElementById('cart-total-items');
    if (totalItems) totalItems.textContent = data.total_items;

    const totalPrice = document.getElementById('cart-total-price');
    if (totalPrice) {
        totalPrice.textContent = parseInt(data.total_price).toLocaleString('ru-RU') + ' ₽';
    }
}
