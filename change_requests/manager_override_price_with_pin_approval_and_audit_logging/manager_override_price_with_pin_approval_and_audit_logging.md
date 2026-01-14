# Change Request (CR)

**Project Name:** POS vNext
**CR Title:** Manager Override Price with PIN Approval and Audit Logging
**Date:** 26 Jul 2024
**Author:** Requested by User

## 1. Description
A new feature will be implemented to enable managers to override the price of an item at the POS during checkout. This process involves a multi-step approach:
-   Upon selecting the "Override Price" option, a popup window will appear prompting the manager to enter their PIN.
-   Once authenticated with the correct PIN, the manager can input a new price for the item.
-   After submitting this new price, an entry will be logged in the audit log containing the exact amount overridden. This includes details such as transaction ID, product ID, original price, and the overridden price.

## 2. Business Value / Justification
This feature is valuable due to its role in improving inventory management for near-expiry stock clearance, which must be achieved on a daily basis. The override functionality combined with PIN-based authentication ensures that only authorized personnel can modify prices, thereby maintaining data integrity and adhering to security policies.

## 3. User Acceptance Criteria (UAC)
-   [ ] Upon selecting "Override Price," the system displays a popup window for manager PIN entry.
-   [ ] After entering the correct PIN, managers can successfully input a new price for an item.
-   [ ] The system logs the exact override amount in the XML transaction audit log with relevant details (transaction ID, product ID, original price, and overridden price).
-   [ ] Unauthorized users are prevented from accessing or modifying prices without proper authentication via PIN entry.