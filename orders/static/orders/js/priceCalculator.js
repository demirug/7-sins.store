let csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value

$('input').change(function () {
    updateData();

    $.ajax({
        url: '/orders/update/',
        type: 'post',
        data: {
            'pk': $(this).attr('name'),
            'quantity': $(this).val(),
            'csrfmiddlewaretoken': csrf_token,
        },
        success: function (response) {}
    });
})

function updateData() {
     let totalPrice = 0
     $('.product').each(function () {
        let price = $(this).find('#price').text();
        let obj =  $(this).find('#count')
        if(Number(obj.val()) > Number(obj.attr('max'))) {
            obj.val(obj.attr('max'));
        }

        if(Number(obj.val()) < Number(obj.attr('min'))) {
            obj.val(obj.attr('min'));
        }

        let count = obj.val();
        $(this).find('#total').text(price * count);
        totalPrice += price * count
    })

    $('#totalPrice').text(totalPrice);
}

updateData();