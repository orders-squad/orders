Feature: The order store service back-end
	As an Order Store Owner
	I need a RESTful catalog service
	So that I can keep track of all my orders

Background:
	Given the following orders
	    | cust_id | prod_id | prod_name | prod_qty | prod_price | status  | 
	    | 1       | 1 	| echo dot  | 2        | 50.5       | ordered |   
	    | 2       | 2       | kindle    | 3        | 40.5       | ordered |   

Scenario: The server is running
	When I visit the "Home Page"
	Then I should see "Order Demo REST API Service" in the title
	And I should not see "404 Not Found"

Scenario: Create an Order
	When I visit the "Home Page"
	And I set the "product_id" to "1"
	And I set the "Name" to "iPhone"
	And I set the "Quantity" to "1"
	And I set the "Price" to "400"
	And I set the "status" to "ordered"
	When I press the "create" item button
	And I set the "product_id" to "2"
	And I set the "Name" to "iPad"
	And I set the "Quantity" to "1"
	And I set the "Price" to "200"
	And I set the "status" to "ordered"
	When I press the "create" item button
	And I set the "customer id" to "123"
	And I press the "Create" order button
	Then I should see the message "Success"

Scenario: List all Orders
	When I visit the "Home Page"
	And I press the "List" order button
	Then I should see "1" in the results
	Then I should see "ordered" in the results
	And I should see "2" in the results

Scenario: Update an Order
	When I visit the "Home Page"
	And I set the "order_Id" to "1"
	And I set the "customer id" to "1"
	And I press the "search" order button
	When I change "order_Id" to "3"
	And I set the "customer id" to "1"
	And I press the "update" order button
	Then I should see the message "Success"

Scenario: Read an Order
	When I visit the "Home Page"
    	And I set the "order_id" to "1"
	And I set the "customer id" to "1"
    	And I press the "search" order button
	And I press the "retrieve" order button
    	Then I should see "1" in the "customer id" field	
	Then I should see "1" in the "order_id" field
    	Then I should see "ordered" in the "order_status" field
	Then I should see the message "Success"
