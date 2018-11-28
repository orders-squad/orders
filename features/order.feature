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