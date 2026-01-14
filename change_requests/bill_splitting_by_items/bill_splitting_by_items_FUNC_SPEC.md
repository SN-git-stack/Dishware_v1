# Functional Specification: Bill Splitting by Items

## 1. Logic Flow & Algorithms
### Step-by-Step Breakdown:

1. **Initial Order Selection:** When a group selects items for bill splitting, the system will identify all distinct items across orders within that group.
2. **Item-Level Cost Calculation:** Calculate individual item costs based on quantities ordered and corresponding menu prices.
3. **Total Cost Computation:** For each order within the group, compute the total cost by summing the costs of selected items.
4. **Equal Split Option:** Offer users the option to split the bill equally among all customers in the group for each order (default).
5. **Item-Level Payment Processing:** If a user selects specific items or wants to pay for an individual item differently, update the payment processing workflow accordingly:
    *   For equal splits: Process payments based on total costs of orders and handle partial payments if necessary.
    *   For item-level splits: Handle multiple payments and track item-wise payments separately.

## 2. API & Data Changes

*   **OrderItem Table Update:** Introduce a new column `item_cost` in the existing OrderItem table to store individual item costs for accurate calculations.
*   **Payment Processing Workflow:** Modify the payment processing workflow to accommodate:
    *   **Split Bill Endpoint:** Create a new endpoint (`POST /split-bill`) for initiating bill splitting and receiving payment details (e.g., card numbers or cash amounts).
    *   **Item-Level Payment Tracking:** Store item-wise payments in a separate database table (`item_payments`) with columns `order_id`, `item_name`, `payment_amount`.
*   **Database Schema Update:** Implement the following to ensure accurate data synchronization:
    *   **Sync Strategy:** Create a new API endpoint (`POST /sync-data`) for syncing data when internet connectivity is restored.
    *   **Local Cache Storage:** Utilize a local database or caching mechanism (e.g., Redis) to store temporary item-wise payment data during offline mode.

## 3. Error Handling & Edge Cases

*   **Offline Mode Error Handling:**
    +   **Sync Failed Errors:** If the sync process fails, display an error message informing users about the failure and prompting them to try again when internet connectivity is restored.
    +   **Data Inconsistency Detection:** Implement a data validation mechanism to detect inconsistencies in item-wise payments during online mode. Display warnings or errors if discrepancies are found.
*   **Edge Cases:**
    +   **Large Groups or Complex Orders:** Apply performance optimization techniques (e.g., lazy loading) for handling large groups or complex orders with many items.
    +   **Partial Payments or Cancellations:** Implement a flexible payment processing system to handle:
        *   Partial payments by storing the remaining balance in `item_payments`.
        *   Item cancellations by updating the corresponding item costs and reprocessing the total order cost.

## 4. UI/UX Rules

*   **UI Updates:**
    +   **Item Selection Interface:** Design an intuitive interface for users to select items from their orders during bill splitting.
    +   **Payment Processing Display:** Update payment processing information (e.g., remaining balances, split percentages) in real-time as users make payments or cancel items.
*   **Error Messages and Warnings:**
    +   Display user-friendly error messages and warnings when encountering issues like data inconsistencies or sync failures.