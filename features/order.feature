Feature: The order store service back-end
	As an Order Store Owner
	I need a RESTful catalog service
	So that I can keep track of all my orders

Background:
	Given the following orders
	    | cust_id | prod_id | prod_name | prod_qty | prod_price | status  | 
	    | 1       | 1 	| echo dot  | 2        | 50.5       | ordered |   
	    | 2       | 2       | kindle    | 3        | 40.5       | ordered |
	    | 3       | 3       | backpack  | 1        | 23.4       | ordered |   

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
	And I set the "customer id" to "12"
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
	And I set the "order_Id" to "3"
	And I set the "customer id" to "3"
	And I press the "search" order button
	And I press the "retrieve" order button
	And I set the "order_Id" to "3"
    When I change "customer id" to "2"
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

Scenario: Delete an Order
        When I visit the "Home Page"
        And I set the "order_id" to "3"
        And I press the "delete" order button
        Then I should see the message "Success"

Scenario: Cancel a order
        When I visit the "Home Page"
        And I set the "order_id" to "2"
        And I press the "cancel" order button
        Then I should see "canceled" in the "order_status" field
        And I should see the message "Order has been Canceled!"

Scenario: List all items
        When I visit the "Home Page"
        And I press the "list" item button
        Then I should see "kindle" in the item results
        And I should see "2" in the item results
        And I should not see "pepper" in the item results

Scenario: Query an item
        When I visit the "Home Page"
        And I set the "name" to "kindle"
        And I press the "search" item button
        Then I should see the message "Success"
        And I should see "40.5" in the item results

Scenario: Read an item
        When I visit the "Home Page"
        And I set the "name" to "kindle"
        And I press the "search" item button
        Then I should see "2" in the "product_id" field
        Then I should see "kindle" in the "name" field
        Then I should see "3" in the "quantity" field
        Then I should see "40.5" in the "price" field
        Then I should see the message "Success"

Scenario: Request a refund of an ordered item
  When I visit the "Home Page"
  And I set the "order_item_id" to "1"
  And I press the "request-refund" item button
  Then I should see the message "Success"


Scenario: Approve a refund of an ordered item
  When I visit the "Home Page"
  And I set the "order_item_id" to "1"
  And I press the "approve-refund" item button
  Then I should see the message "Success"

Scenario: Deny a refund of an ordered item
  When I visit the "Home Page"
  And I set the "order_item_id" to "1"
  And I press the "deny-refund" item button
  Then I should see the message "Success"