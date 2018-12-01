$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        console.log(" length");
        console.log(res.items);
        $("#order_id").val(res.id);
        $("#cust_id").val(res.cust_id);
        var items = res.items;
        for(var i=0;i< items.length;i++){
            item = items[i];
            console.log(item.status);
            $("#item_order_status").val(item.status); 
        } 
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#cust_id").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    /// Clears all form fields
    function clear_item_form_data() {
        $("#item_product_id").val("");
        $("#item_order_id").val("");
        $("#item_name").val("");
        $("#item_quantity").val("");
        $("#item_price").val("");
        $("#item_status").val("");
    }

    // Updates the form with data from the response
    function update_item_form_data(res) {
        $("#item_order_id").val(res.order_id);
        $("#item_product_id").val(res.prod_id);
        $("#item_name").val(res.prod_name);
        $("#item_quantity").val(res.prod_qty);
        $("#item_price").val(res.prod_price);
        $("#item_status").val(res.status);
    }

    // add items to orders
    var items_for_order = [];

    function update_items_view() {
        $("#items_for_order").empty();
        $("#items_for_order").append('<table class="table-striped">');
        var header = '<tr>'
        header += '<th style="width:10%">Product ID</th>'
        header += '<th style="width:40%">Name</th>'
        header += '<th style="width:25%">Quantity</th>'
        header += '<th style="width:25%">Price</th></tr>'
        header += '<th style="width:25%">Status</th></tr>'
        $("#items_for_order").append(header);
        for(var i = 0; i < items_for_order.length; i++) {
            item = items_for_order[i];
            var row = "<tr><td>"+item.prod_id+"</td><td>"+item.prod_name+"</td><td>"+item.prod_qty+"</td><td>"+item.prod_price+"</td></tr>"+item.status+"</td></tr>";
            $("#items_for_order").append(row);
        }

        $("#items_for_order").append('</table>');
    }

    // ****************************************
    // Create an Order
    // ****************************************

    $("#create-btn").click(function () {

        var customer_id = $("#cust_id").val();
        var items = items_for_order;

        var data = {
            "cust_id": customer_id,
            "items": items
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message("res.responseJSON.message")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-btn-item").click(function () {

        var product_id = $("#item_product_id").val();
        var name = $("#item_name").val();
        var quantity = $("#item_quantity").val();
        var price = $("#item_price").val();
        var status = $("#item_status").val();

        var data = {
            "prod_id": product_id,
            "prod_name": name,
            "prod_qty": quantity,
            "prod_price": price,
            "status": status
        };

        items_for_order.push(data);
        console.log(data);

        clear_item_form_data();

        update_items_view();

    });


    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data()
    });

    $("#clear-btn-item").click(function () {
        $("#prod_id").val("");
        clear_item_form_data()
    });

})