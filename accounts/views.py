from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from shop.models import Product
from .models import UserProfile, Wishlist
from .forms import RegisterForm, LoginForm, ProfileEditForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('shop:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # SECURITY: Validate 'next' URL to prevent open redirect
            next_url = request.GET.get('next', '')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('shop:home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# SECURITY: Logout must require POST to prevent CSRF logout attacks
@require_POST
def logout_view(request):
    logout(request)
    return redirect('shop:home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            profile.phone = form.cleaned_data['phone']
            profile.city = form.cleaned_data['city']
            profile.address = form.cleaned_data['address']
            profile.save()
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': profile.phone,
            'city': profile.city,
            'address': profile.address,
        })
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'accounts/wishlist.html', {'wishlist_items': items})


@require_POST
@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
    if wishlist_item.exists():
        wishlist_item.delete()
        added = False
    else:
        Wishlist.objects.create(user=request.user, product=product)
        added = True
    return JsonResponse({'status': 'ok', 'added': added})
