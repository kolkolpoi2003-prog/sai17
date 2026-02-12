document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('quickViewModal');
    if (!modal) return;

    const backdrop = modal.querySelector('.modal-backdrop');
    const panel = modal.querySelector('.modal-panel');
    const closeBtn = modal.querySelector('.modal-close');
    const content = modal.querySelector('.modal-content');

    // Open Modal
    document.body.addEventListener('click', async (e) => {
        const btn = e.target.closest('.quick-view-btn');
        if (!btn) return;

        e.preventDefault();
        const productSlug = btn.dataset.productSlug;
        if (!productSlug) return;

        // Show loading state
        openModal();
        content.innerHTML = `
            <div class="flex items-center justify-center h-96">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
            </div>
        `;

        try {
            const response = await fetch(`/shop/product/${productSlug}/quick-view/`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            renderProduct(data);
        } catch (error) {
            console.error('Error:', error);
            content.innerHTML = `
                <div class="flex flex-col items-center justify-center h-96 text-red-500">
                    <p>Не удалось загрузить информацию о товаре.</p>
                    <button class="mt-4 px-4 py-2 bg-gray-100 rounded-full text-black" onclick="closeQuickView()">Закрыть</button>
                </div>
            `;
        }
    });

    // Close Modal
    function closeQuickView() {
        backdrop.classList.add('opacity-0');
        panel.classList.remove('opacity-100', 'scale-100');
        panel.classList.add('opacity-0', 'scale-95');
        setTimeout(() => {
            modal.classList.add('hidden');
            document.body.style.overflow = '';
        }, 300);
    }

    if (closeBtn) closeBtn.addEventListener('click', closeQuickView);
    if (backdrop) backdrop.addEventListener('click', closeQuickView);

    window.openModal = function () {
        modal.classList.remove('hidden');
        // Trigger reflow
        void modal.offsetWidth;
        backdrop.classList.remove('opacity-0');
        panel.classList.remove('opacity-0', 'scale-95');
        panel.classList.add('opacity-100', 'scale-100');
        document.body.style.overflow = 'hidden';
    }

    // Expose close function globally if needed
    window.closeQuickView = closeQuickView;

    function renderProduct(product) {
        let imagesHtml = '';
        if (product.images && product.images.length > 0) {
            imagesHtml = `
                <div class="aspect-[3/4] bg-gray-100 rounded-xl overflow-hidden mb-4">
                    <img src="${product.images[0]}" class="w-full h-full object-cover" alt="${product.name}">
                </div>
                <div class="grid grid-cols-4 gap-2">
                    ${product.images.map(img => `
                        <div class="aspect-square bg-gray-50 rounded-lg overflow-hidden cursor-pointer hover:opacity-80 transition-opacity">
                            <img src="${img}" class="w-full h-full object-cover">
                        </div>
                    `).join('')}
                </div>
            `;
        }

        content.innerHTML = `
            <div class="flex flex-col lg:flex-row gap-8">
                <div class="lg:w-1/2">
                    ${imagesHtml}
                </div>
                <div class="lg:w-1/2 flex flex-col">
                    ${product.brand ? `<p class="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2">${product.brand}</p>` : ''}
                    <h2 class="text-3xl font-heading font-bold mb-4 leading-tight">${product.name}</h2>
                    
                    <div class="flex items-baseline gap-4 mb-6">
                        <span class="text-2xl font-bold">${product.price} ₽</span>
                        ${product.old_price ? `<span class="text-lg text-gray-400 line-through">${product.old_price} ₽</span>` : ''}
                    </div>

                    <div class="text-sm text-gray-600 leading-relaxed mb-8 flex-grow">
                        ${product.description ? product.description.slice(0, 150) + '...' : ''}
                    </div>

                    <div class="mt-auto space-y-4">
                         <a href="${product.url}" class="block w-full py-4 bg-black text-white text-center font-bold uppercase tracking-widest rounded-full hover:bg-gray-800 transition-colors">
                            Подробнее
                        </a>
                    </div>
                </div>
            </div>
        `;
    }
});
