# Change Request (CR)

**Project Name:** POS vNext
**CR Title:** Bill Splitting by Items
**Date:** 2024-07-26
**Author:** Requested by User

## 1. Description
The current bill splitting functionality supports only equal distribution of the total amount among all customers in a group. This limitation prevents groups from splitting bills based on actual items consumed, which may not be ideal for certain types of events or gatherings.

To address this, we need to introduce a new feature that allows users to split the bill by individual items ordered. This will involve modifying the existing payment processing workflow to accommodate item-level tracking and calculations for multiple customers.

## 2. Business Value / Justification
Improves customer experience by offering a more flexible and personalized way of handling group payments, which is expected to increase user satisfaction and loyalty.

## 3. User Acceptance Criteria (UAC)
- Users can select specific items from their order when splitting the bill.
- The system calculates the total cost for each item separately and provides an option for users to pay for individual items or split them equally among group members.
- The payment processing workflow accommodates multiple payment methods, including card payments and cash transactions.
- The system maintains accurate records of individual item costs and corresponding payments made by group members.