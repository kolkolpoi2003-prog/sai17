from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.views.decorators.http import require_POST
from .models import Product, Category, Brand
from .forms import FittingRequestForm



def home(request):
    """Главная страница"""
    categories = Category.objects.filter(is_active=True, parent__isnull=True)[:8]
    hits = Product.objects.filter(is_hit=True, status=Product.Status.AVAILABLE).select_related('category', 'brand').prefetch_related('images')[:8]
    sales = Product.objects.filter(
        old_price__isnull=False,
        status=Product.Status.AVAILABLE
    ).select_related('category', 'brand').prefetch_related('images')[:8]
    new_products = Product.objects.filter(is_new=True, status=Product.Status.AVAILABLE).select_related('category', 'brand').prefetch_related('images')[:8]

    context = {
        'form': FittingRequestForm(),
        'categories': categories,
        'hits': hits,
        'sales': sales,
        'new_products': new_products,
    }
    return render(request, 'shop/home.html', context)


def catalog(request):
    """Каталог с фильтрацией и сортировкой"""
    products = Product.objects.filter(status=Product.Status.AVAILABLE).select_related('category', 'brand').prefetch_related('images')

    # Фильтр по категории
    category_slug = request.GET.get('category')
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        # Включаем подкатегории
        category_ids = [current_category.id]
        children = current_category.children.all()
        category_ids.extend(children.values_list('id', flat=True))
        products = products.filter(category_id__in=category_ids)

    # Фильтр по бренду
    brand_slug = request.GET.get('brand')
    current_brand = None
    if brand_slug:
        current_brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=current_brand)

    # Фильтр по цене (с валидацией)
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        try:
            price_min = Decimal(price_min)
            products = products.filter(price__gte=price_min)
        except (InvalidOperation, ValueError):
            pass
    if price_max:
        try:
            price_max = Decimal(price_max)
            products = products.filter(price__lte=price_max)
        except (InvalidOperation, ValueError):
            pass

    # Только акции
    on_sale = request.GET.get('on_sale')
    if on_sale:
        products = products.filter(old_price__isnull=False)

    # Сортировка
    sort = request.GET.get('sort', '-created')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'newest': '-created',
        'popular': '-is_hit',
    }
    products = products.order_by(sort_options.get(sort, '-created'))

    categories = Category.objects.filter(is_active=True, parent__isnull=True)
    brands = Brand.objects.filter(is_active=True)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'current_category': current_category,
        'current_brand': current_brand,
        'current_sort': sort,
    }
    return render(request, 'shop/catalog.html', context)


def category_detail(request, slug):
    """Товары конкретной категории"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    category_ids = [category.id]
    children = category.children.all()
    category_ids.extend(children.values_list('id', flat=True))

    products = Product.objects.filter(
        category_id__in=category_ids,
        status=Product.Status.AVAILABLE
    ).select_related('category', 'brand').prefetch_related('images')

    # Сортировка
    sort = request.GET.get('sort', '-created')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'newest': '-created',
    }
    products = products.order_by(sort_options.get(sort, '-created'))

    brands = Brand.objects.filter(is_active=True)

    context = {
        'category': category,
        'products': products,
        'brands': brands,
        'subcategories': children,
        'current_sort': sort,
    }
    return render(request, 'shop/catalog.html', context)


def product_detail(request, slug):
    """Карточка товара"""
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand').prefetch_related('images', 'reviews__user'),
        slug=slug
    )
    related = Product.objects.filter(
        category=product.category,
        status=Product.Status.AVAILABLE
    ).exclude(id=product.id).prefetch_related('images')[:4]

    avg_rating = product.reviews.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']

    context = {
        'product': product,
        'related_products': related,
        'avg_rating': avg_rating,
    }
    return render(request, 'shop/product_detail.html', context)


def search(request):
    """Поиск товаров"""
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query),
            status=Product.Status.AVAILABLE
        ).select_related('category', 'brand').prefetch_related('images').distinct()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        results = []
        for p in products[:5]:
            img = p.main_image
            results.append({
                'name': p.name,
                'price': str(p.price),
                'url': p.get_absolute_url(),
                'image': img.image.url if img else '',
            })
        return JsonResponse({'results': results})

    return render(request, 'shop/search_results.html', {
        'products': products,
        'query': query,
    })


def about(request):
    """О нас"""
    return render(request, 'shop/about.html')


@require_POST
def fitting_request(request):
    """Обработка заявки на примерку"""
    form = FittingRequestForm(request.POST)
    if form.is_valid():
        # Здесь можно добавить логику сохранения заявки в БД или отправки письма
        # Пока просто возвращаем успешный ответ
        return JsonResponse({'status': 'success', 'message': 'Ваша заявка принята! Мы свяжемся с вами в ближайшее время.'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


def quick_view(request, slug):
    """Быстрый просмотр товара (JSON)"""
    product = get_object_or_404(
        Product.objects.select_related('brand').prefetch_related('images'),
        slug=slug
    )
    
    images = []
    if product.main_image:
        images.append(product.main_image.image.url)
    for img in product.images.all():
        if not img.is_main:
            images.append(img.image.url)
            
    # Если нет изображений, добавим заглушку или оставим пустым
    
    data = {
        'id': product.id,
        'name': product.name,
        'price': f"{product.price:,.0f}".replace(',', ' '),
        'old_price': f"{product.old_price:,.0f}".replace(',', ' ') if product.old_price else None,
        'description': product.description,
        'url': product.get_absolute_url(),
        'images': images,
        'is_available': product.is_available,
        'brand': product.brand.name if product.brand else None,
    }
    return JsonResponse(data)
