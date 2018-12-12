$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#cust_id").val(res.cust_id);
        var items = res.items;
        for(var i=0;i< items.length;i++){
            item = items[i];
            $("#item_order_status").val(item.status); 
        } 
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#cust_id").val("");
        $("#order_id").val("");
        $("#item_order_status").val("");
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
        var items = res.items;
        $("#item_order_id").val(items[0].order_id);
        $("#item_product_id").val(items[0].prod_id);
        $("#item_name").val(items[0].prod_name);
        $("#item_quantity").val(items[0].prod_qty);
        $("#item_price").val(items[0].prod_price);
        $("#item_status").val(items[0].status);
    }

    // add items to orders
    var items_for_order = [];

    function update_items_view() {
        $("#items_for_order").empty();
        $("#items_for_order").append('<table class="table-striped">');
        var header = '<tr>'
        header += '<th style="width:20%">Product ID</th>'
        header += '<th style="width:20%">Name</th>'
        header += '<th style="width:20%">Quantity</th>'
        header += '<th style="width:20%">Price</th></tr>'
        header += '<th style="width:20%">Status</th></tr>'
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
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message("res.responseJSON.message")
        });
    });

    // ****************************************
    // Update an Order
    // ****************************************

    $("#update-btn").click(function () {

        var order_id = $("#order_id").val();
        var cust_id = $("#cust_id").val();
        //var items = items_for_order;
        var item_store = [];
        var custom_id;
        var data;

        var ajax1 = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: ''
        })
    
        ajax1.done(function(res){
            custom_id = res.cust_id;
            var items = res.items;
            for(var i=0;i<items.length;i++){
                item_store.push(items[i]);
            }
            var data1 = {
                "cust_id": cust_id,
                "items": item_store
            };
            ajax = $.ajax({
                type: "PUT",
                url: "/orders/" + order_id,
                contentType:"application/json",
                data: JSON.stringify(data1)
            })

            ajax.done(function(res){
                //update_form_data(res)
                flash_message("Success");
            });

            ajax.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
            });
        });

        ajax1.done(function(res){
            flash_message("Success");
        });

        ajax1.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Request a Refund
    // ****************************************

    $("#request-refund-btn-item").click(function () {

        var order_item_id = $("#order_item_id").val();
        var item_store = [];
        var custom_id;
        var data;

        var ajax1 = $.ajax({
            type: "PUT",
            url: "/orders/" + order_item_id + "/request-refund",
            contentType:"application/json",
            data: ''
        })

        ajax1.done(function(res){
            flash_message("Success");
        });

        ajax1.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Approve a Refund
    // ****************************************

    $("#approve-refund-btn-item").click(function () {

        var order_item_id = $("#order_item_id").val();
        var item_store = [];
        var custom_id;
        var data;

        var ajax1 = $.ajax({
            type: "PUT",
            url: "/orders/" + order_item_id + "/approve-refund",
            contentType:"application/json",
            data: ''
        })

        ajax1.done(function(res){
            flash_message("Success");
        });

        ajax1.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Approve a Refund
    // ****************************************

    $("#deny-refund-btn-item").click(function () {

        var order_item_id = $("#order_item_id").val();
        var item_store = [];
        var custom_id;
        var data;

        var ajax1 = $.ajax({
            type: "PUT",
            url: "/orders/" + order_item_id + "/deny-refund",
            contentType:"application/json",
            data: ''
        })

        ajax1.done(function(res){
            flash_message("Success");
        });

        ajax1.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });








    // ****************************************
    // Search Orders by field
    // ****************************************

    $("#search-btn").click(function () {
        var order_id = $("#order_id").val();
        var customer_id = $("#cust_id").val();
        var status = $("#item_order_status").val();

        var queryString = "";

        if (order_id) {
            queryString += 'order_id=' + order_id;
        }
        if (customer_id) {
            queryString += 'cust_id=' + customer_id;
        }
        if (status) {
            if (queryString.length > 0) {
                queryString += '&status=' + status;
            } else {
                queryString += 'status=' + status;
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/orders?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#order_results").empty();
            $("#order_results").append('Orders:');
            $("#order_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:20%">ID</th>'
            header += '<th style="width:20%">Customer ID</th>'
            header += '<th style="width:20%">Status</th></tr>'
            $("#order_results").append(header);
            var temp = 0;
            var j = 0;
            for(var i = 0; i < res.length; i++) {
                order = res[i];
                var items = order.items;
                var status;
                for(var j = 0;j<items.length;j++){
                    var item = items[j];
                    status = item.status
                }
                if(customer_id == order.cust_id && order_id == order.id){
                    temp = 1;
                    var row = "<tr><td>"+order.id+"</td><td>"+order.cust_id+"</td><td>"+status+"</td></tr>";
                    $("#order_results").append(row);
                    j = i;
                } 
                if(j) {
                  update_form_data(res[j]);
                }
            }
            $("#order_results").append('</table>');
            if(temp == 0){
                flash_message("Invalid Customer Id or Order ID ");
            } else {
                flash_message("Success");
            }
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    
    // ****************************************
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        var order_id = $("#order_id").val();
        var ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: ''
        })
        ajax.done(function(res){
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Delete an Order
    // ****************************************

    $("#delete-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data();
            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message("Server error!");
        });
    });

    // ****************************************
    // Cancel an Order
    // ****************************************

    $("#cancel-btn").click(function () {

        var order_id = $("#order_id").val();
        var item_store = [];
        var custom_id;
        var data;

        var ajax1 = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
            contentType:"application/json",
            data: ''
        })
    
        ajax1.done(function(res){
            custom_id = res.cust_id;
            var items = res.items;
            for(var i=0;i<items.length;i++){
                item_store.push(items[i]);
            }
            for(var j = 0;j<item_store.length;j++){
                item_store[j].status = "canceled";
            }
            var data1 = {
                "cust_id": custom_id,
                "items": item_store
            };
            ajax = $.ajax({
                type: "PUT",
                url: "/orders/" + order_id,
                contentType:"application/json",
                data: JSON.stringify(data1)
            })

            ajax.done(function(res){
                update_form_data(res[0]);
                flash_message("Order has been Canceled!");
            });

            ajax.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
            });
        });


        ajax1.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data();
    });

    // ****************************************
    // View Orders
    // ****************************************

    $("#list-btn").click(function () {

        var ajax = $.ajax({
            type: "GET",
            url: "/orders",
            contentType:"application/json"
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#order_results").empty();
            $("#order_results").append('Orders:');
            $("#order_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:20%">ID</th>'
            header += '<th style="width:20%">Customer ID</th>'
            header += '<th style="width:20%">Status</th></tr>'
            $("#order_results").append(header);
            for(var i = 0; i < res.length; i++) {
                order = res[i];
                var items = order.items;
                var status;
                for(var j = 0;j<items.length;j++){
                    var item = items[j];
                    status = item.status;
                }
                var row = "<tr><td>"+order.id+"</td><td>"+order.cust_id+"</td><td>"+status+"</td></tr>";
                $("#order_results").append(row);
            }

            $("#order_results").append('</table>');

            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });

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

        clear_item_form_data();

        update_items_view();

    });

    // ****************************************
    // View Items
    // ****************************************

    $("#list-btn-item").click(function () {

        var ajax = $.ajax({
            type: "GET",
            url: "/orders",
            contentType:"application/json"
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#item_results").empty();
            $("#item_results").append('Items:');
            $("#item_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:20%">ID</th>'
            header += '<th style="width:20%">Order ID</th>'
            header += '<th style="width:20%">Product ID</th>'
            header += '<th style="width:20%">Name</th>'
            header += '<th style="width:20%">Quantity</th>'
            header += '<th style="width:20%">Price</th></tr>'
            $("#item_results").append(header);
    
            var t = res[0];
            var items = res[3];
            for(var i = 0; i < res.length; i++) {
                items = res[i].items;
                for(var j = 0; j < items.length; j++){
                    item = items[0];
                    var row = "<tr><td>"+item.id+"</td><td>"+item.order_id+"</td><td>"+item.prod_id+"</td><td>"+item.prod_name+"</td><td>"+item.prod_qty+"</td><td>"+item.prod_price+"</td></tr>";
                    $("#item_results").append(row);
                }
            }

            $("#item_results").append('</table>');

            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message("res.responseJSON.message");
        });

    });

    // ****************************************
    // Search Items by field
    // ****************************************

    $("#search-btn-item").click(function () {

        var product_id = $("#item_product_id").val();
        var order_id = $("#item_order_id").val();
        var name = $("#item_name").val();
        var quantity = $("#item_quantity").val();
        var price = $("#item_price").val();

        var queryString = "";

        if (product_id) {
            queryString += 'prod_id=' + product_id;
        }
        if (order_id) {
            if (queryString.length > 0) {
                queryString += '&order_id=' + order_id;
            } else {
                queryString += 'order_id=' + order_id;
            }
        }
        if (name) {
            if (queryString.length > 0) {
                queryString += '&prod_name=' + name;
            } else {
                queryString += 'prod_name=' + name;
            }
        }
        if (quantity) {
            if (queryString.length > 0) {
                queryString += '&prod_qty=' + quantity;
            } else {
                queryString += 'prod_qty=' + quantity;
            }
        }
        if (price) {
            if (queryString.length > 0) {
                queryString += '&prod_price=' + price;
            } else {
                queryString += 'prod_price=' + price;
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/orders?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#item_results").empty();
            $("#item_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:20%">ID</th>'
            header += '<th style="width:20%">Order ID</th>'
            header += '<th style="width:20%">Product ID</th>'
            header += '<th style="width:20%">Name</th>'
            header += '<th style="width:20%">Quantity</th>'
            header += '<th style="width:20%">Price</th></tr>'
            $("#item_results").append(header);
            var k = 0;
            for(var i = 0; i < res.length; i++) {
                item = res[i].items;
                for(var j = 0;j<item.length;j++){
                    prd_name = item[j].prod_name;
                    if(prd_name == name){
                    var row = "<tr><td>"+item[j].id+"</td><td>"+item[j].order_id+"</td><td>"+item[j].prod_id+"</td><td>"+item[j].prod_name+"</td><"+"</td><td>"+item[j].prod_qty+"</td><td>"+"</td><td>"+item[j].prod_price+"</td></tr>";
                    $("#item_results").append(row); 
                    k = i;      
                    }
                }
                if(k) {
                  update_item_form_data(res[k]);
                  $("#item_id").val(res[i].id);
                }
            }

            $("#item_results").append('</table>');

            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data();
    });

    $("#clear-btn-item").click(function () {
        $("#prod_id").val("");
        clear_item_form_data();
    });

})