from django.shortcuts import render
from django.http import HttpResponseRedirect
from user.models import Product, Transaction, Comment
from user.forms import ProductForm, CommentForm
from django.utils import timezone
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def list_products(request):
    products = Product.objects.all().order_by('seller', 'last_updated',)
    return render(request, 'list_products.html', locals())


@login_required
def add_product(request):
    f = ProductForm()
    if request.POST:
        product_name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['price']
        inventory = request.POST['inventory']
        seller = get_user(request)
        date_time = timezone.localtime(timezone.now())

        p = Product.objects.create(
            name = product_name,
            description = description,
            price = price,
            inventory = inventory,
            seller = seller,
            last_updated = date_time
        )
        return HttpResponseRedirect('/list_products/')
    f = ProductForm()
    return render(request, 'add_product.html', locals())


def list_seller(request):
    sellers = User.objects.all()
    return render(request, 'list_sellers.html', locals())


def product_detail(request, id):
    if id:
        p = Product.objects.filter(id=id)[0]
        can_purchase = request.user.username and (str(p.seller) != request.user.username) 
    else:
        return HttpResponseRedirect("/list_products/")

    if request.POST:
        f = CommentForm(request.POST)
        content = request.POST['content']
        product = Product.objects.filter(id=id)[0]
        writer = get_user(request)
        date_time = timezone.localtime(timezone.now())

        Comment.objects.create(
            content = content,
            product = product,
            writer = writer,
            post_time = date_time
        )
    f = CommentForm()
    return render(request, 'product.html', locals())

def seller_detail(request, id):
    if id:
        s = User.objects.filter(id=id)[0]
        return render(request, 'seller.html', locals())
    else:
        return HttpResponseRedirect("/list_sellers/")


@login_required
def purchase(request, id):
    if id:
        p = Product.objects.filter(id=id)[0]
        buyer = get_user(request)
        seller = p.seller
    else:
        return HttpResponseRedirect("/list_products/")

    errors = []
    if request.POST:
        number = int(request.POST['number'])
        at_most = int(Product.objects.filter(id=id)[0].inventory)
        if number > at_most:
            print("error")
            errors.append(f"only {at_most} product(s) remaining")
        product = p
        total = int(number)*p.price
        pay_time = timezone.localtime(timezone.now())

        if not errors:
            Transaction.objects.create(
                seller = seller,
                buyer = buyer,
                product = product,
                number = number,
                total = total,
                pay_time = pay_time
            )
            inventory = p.inventory
            Product.objects.filter(id=id).update(inventory=inventory-int(number))
            return HttpResponseRedirect('/buying_record/')
    return render(request, 'purchase.html', locals())


@login_required
def selling_record(request):
    transactions = Transaction.objects.order_by('-pay_time').filter(seller=get_user(request))
    return render(request, 'trading_record.html', locals())


@login_required
def buying_record(request):
    transactions = Transaction.objects.order_by('-pay_time').filter(buyer=get_user(request))
    return render(request, 'trading_record.html', locals())