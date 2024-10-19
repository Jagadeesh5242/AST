# Project Title
Abstract Syntax tree (AST)

## Description
This project is a Rule Engine built using Abstract Syntax Tree (AST) to dynamically create, combine, and modify rules for determining user eligibility based on attributes like age, department, income, and experience. The Rule Engine consists of three tiers: a simple user interface (UI), an API, and a backend connected to a MongoDB database.

##Key Features:
Dynamic Rule Creation:
The system allows the creation of rules from a user-friendly string format (e.g., "(age > 30 AND department = 'Sales') OR salary > 50000").

Rule Combination: 
Multiple rules can be combined into a single logical unit, ensuring efficient evaluation.
Evaluation of Rules: The rules are evaluated against user data to check eligibility.
Error Handling: The system validates rule strings and handles invalid input gracefully.


## Technologies Used
- Python
- Flask
- MongoDB
- etc.

