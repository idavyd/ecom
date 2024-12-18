from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = quantity
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", '\"')
            profile.update(old_cart=cart_str)

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product_id, product_quantity):
        product_id = str(product_id)
        product_quantity = int(product_quantity)
        our_cart = self.cart
        our_cart[product_id] = product_quantity
        self.session.modified = True
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", '\"')
            profile.update(old_cart=cart_str)
        return our_cart

    def remove(self, product):
        product_id = str(product.id)
        self.cart.pop(product_id)
        self.session.modified = True
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", '\"')
            profile.update(old_cart=cart_str)

    def total(self):
        totals_per_prod = []
        for key, value in self.cart.items():
            product = Product.objects.get(id=int(key))
            if product.is_sale:
                x = product.sale_price * value
                totals_per_prod.append(x)
            else:
                x = product.price * value
                totals_per_prod.append(x)
        return sum(totals_per_prod)

    def db_add(self, product, quantity):
        product_id = str(product)
        product_quantity = quantity
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", '\"')
            profile.update(old_cart=cart_str)

    def clear(self):
        self.cart = self.session['cart'] = {}












