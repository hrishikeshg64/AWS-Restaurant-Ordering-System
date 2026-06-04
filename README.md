# Cloud-Based Three-Tier Restaurant Ordering System

A secure, scalable, and event-driven restaurant ordering application deployed on AWS. This project leverages a classic three-tier architecture to separate presentation, business logic, and data storage, integrated with an automated cloud notification system.

---

## 🛠️ Tech Stack & Services

* **Frontend & Backend:** Python, Flask, HTML5/CSS3
* **Compute:** Amazon EC2
* **Database:** Amazon RDS (MySQL)
* **Messaging/Alerts:** Amazon SNS (Simple Notification Service)
* **Security:** AWS IAM (Identity and Access Management), Security Groups

---

## 🚀 Deployment Steps

### 1. Database Provisioning
* Launch an Amazon RDS (MySQL) instance inside your private or public subnets.
* Configure the database security group to allow inbound traffic on port `3306` **only** from your EC2 instance's security group.

### 2. Notification Pipeline Setup
* Create an Amazon SNS Standard Topic (e.g., `Order_Notifications`).
* Create an Email Subscription under the topic, inputting the target email address.
* Confirm the subscription by clicking the activation link sent to that inbox.

### 3. Identity and Access Management (IAM)
* Create an IAM Role with an attached policy allowing `sns:Publish` permissions.
* Attach this IAM Role to your EC2 instance profile to grant programmatic access via the AWS SDK (`boto3`).

### 4. Application Configuration & Host
* Launch your EC2 instance and clone the codebase.
* Update your Flask configuration with the RDS Database Endpoint and the SNS Topic ARN.
* Install project dependencies, initialize the database schema, and run the Flask application.
