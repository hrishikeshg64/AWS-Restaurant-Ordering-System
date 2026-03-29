Detailed Version (for GitHub README)

📌 Project Workflow / Architecture Steps

1. Frontend Layer (Presentation Tier)
   Hosted the web application on EC2
   Users can browse menu and place orders via browser
2. Application Layer (Backend)
   Built using Flask (Python)
   Handles incoming requests and order processing logic
   Connects to database and SNS service
3. Database Layer
   Used Amazon RDS (MySQL)
   Stores customer order details securely
4. Notification System (Event-Driven)
   Integrated Amazon SNS
   Sends email notifications instantly when an order is placed
5. Security Implementation
   Configured IAM Role for EC2 instance
   Granted permission to access SNS
   Avoided hardcoding AWS credentials (best practice 🔐)
6. Deployment Steps
   Launched EC2 instance and hosted Flask app
   Set up RDS instance and connected it with backend
   Configured SNS topic and email subscription
   Attached IAM Role to EC2 for secure service access
