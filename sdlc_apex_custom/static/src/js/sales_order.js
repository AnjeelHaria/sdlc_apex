odoo.define('sdlc_apex_custom.sales_order',[], function (require) {
    'use strict';

    var ajax = require('web.ajax');

    $(document).ready(function () {
        $('#add_line').click(function () {
            var newLine = $('.order_line:first').clone();
            newLine.find('input').val('');
            newLine.find('.product_select').html('<option value="" disabled selected>Select a product</option>');
            newLine.appendTo('#order_lines');
        });

        $('form').submit(function (e) {
            e.preventDefault();

            var orderLines = [];
            $('#order_lines .order_line').each(function () {
                var product_id = $(this).find('select[name="product_id"]').val();
                var quantity = $(this).find('input[name="quantity"]').val();
                orderLines.push(product_id + ',' + quantity);
            });

            var form = $(this);
            form.append('<input type="hidden" name="order_lines" value="' + JSON.stringify(orderLines) + '"/>');
            form.unbind('submit').submit();
        });

        $(document).on('input', '.product_search', function () {
            var $input = $(this);
            var searchTerm = $input.val();
            var $select = $input.siblings('.product_select');

            ajax.jsonRpc('/search_products', 'call', {'search_term': searchTerm}).then(function (products) {
                $select.html('<option value="" disabled selected>Select a product</option>');
                products.forEach(function (product) {
                    $select.append('<option value="' + product.id + '">' + product.name + '</option>');
                });
            });
        });
    });
});
