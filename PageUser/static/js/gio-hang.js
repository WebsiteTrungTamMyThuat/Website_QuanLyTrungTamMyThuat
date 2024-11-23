var data = [
    {
        "id": 1,
        "name": "CĂN BẢN CHÌ",
        "price": 1000,
        "img": "../../static/img/tranh-chan-dung.jpeg"
    },
    {
        "id": 2,
        "name": "CĂN BẢN CHÌ TEST",
        "price": 1000,
        "img": "../../static/img/tranh-ky-hoa.jpg"
    },
    {
        "id": 3,
        "name": "CĂN BẢN CHÌ",
        "price": 1000,
        "img": "../../static/img/tranh-mau-nuoc.jpg"
    }
];
function renderCart() {
    const cartOrder = document.getElementById('cartOrder');
    cartOrder.innerHTML = '';
    let total = 0;
    data.forEach(item => {
        total += item.price;
        const cartItem = document.createElement('div');
        cartItem.className = 'cart__order-item border-b';
        cartItem.innerHTML = `
            <div class="cart__order-item__img">
                <img src="${item.img}" alt="">
            </div>
            <div class="cart__order-item__info">
                <h3>${item.name}</h3>
                <h3>${item.price}$</h3>
            </div>
            <button class="btn-remove" data-id="${item.id}">
                <ion-icon name="close-outline"></ion-icon>
            </button>
        `;
        cartOrder.appendChild(cartItem);
    });
    const totalElement = document.createElement('div');
    totalElement.className = 'cart__order-total';
    totalElement.innerHTML = `
        <h3>Tổng cộng: </h3>
        <h3>${total}$</h3>
    `;
    cartOrder.appendChild(totalElement);
    attachRemoveEventListeners();
}
function attachRemoveEventListeners() {
    document.querySelectorAll('.btn-remove').forEach(button => {
        button.addEventListener('click', function() {
            const id = parseInt(this.getAttribute('data-id'));
            data = data.filter(item => item.id !== id);
            renderCart();
        });
    });
}
function attachOnePayEventListeners() {
    document.querySelectorAll('.onepay').forEach(item => {
        item.addEventListener('click', function() {
            document.querySelectorAll('.onepay').forEach(el => {
                el.classList.remove('onepay-momo', 'onepay-visa', 'onepay-bank');
            });
            const ariaLabel = this.getAttribute('aria-label');
            if (ariaLabel === 'momo') {
                this.classList.add('onepay-momo');
            } else if (ariaLabel === 'visa') {
                this.classList.add('onepay-visa');
            } else if (ariaLabel === 'atm') {
                this.classList.add('onepay-bank');
            }
        });
    });
}
document.addEventListener('DOMContentLoaded', function() {
    renderCart();
    attachOnePayEventListeners();
});