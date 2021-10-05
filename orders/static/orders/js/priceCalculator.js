$('input').change(function () {
    updateData();
})

function updateData() {
     let totalPrice = 0
     $('.product').each(function () {
        let price = $(this).find('#price').text();
        let count =  $(this).find('#count').val();
        $(this).find('#total').text(price * count);
        totalPrice += price * count
    })

    $('#totalPrice').text(totalPrice);
}

updateData();