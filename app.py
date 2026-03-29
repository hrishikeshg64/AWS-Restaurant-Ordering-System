from flask import Flask, render_template, request, redirect, url_for
import pymysql
import boto3
import os

app = Flask(__name__)

# ===============================
# DATABASE CONNECTION (HARDCODED FOR RDS)
# ===============================
def get_db_connection():
    try:
        return pymysql.connect(
            # Using your specific RDS Endpoint
            host="your-rds-endpoint",
            user="admin",
            password="your-password", 
            database="your database-name",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10
        )
    except Exception as e:
        print(f"CRITICAL: Could not connect to RDS. Error: {e}")
        return None


# ===============================
# SNS CONFIGURATION (AWS SDK)
# ===============================
sns = boto3.client(
    "sns",
    region_name="us-west-2"
)

TOPIC_ARN = "arn-from-SNS"


# ===============================
# ROUTES
# ===============================

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/order', methods=['POST'])
def order():
    # 1. Get data from the HTML Form
    name = request.form.get('name')
    email = request.form.get('email')
    food = request.form.get('food')
    quantity = request.form.get('quantity')

    db = get_db_connection()
    
    if db is None:
        return render_template_string(ERROR_HTML, error="RDS Connection Refused. Check Security Groups!")

    try:
        # 2. Insert into MySQL Database
        with db.cursor() as cursor:
            sql = "INSERT INTO orders (name, email, food, quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, food, quantity))
        db.commit()

        # 3. Send AWS SNS Notification
        message = f"New Order Received!\n\nName: {name}\nEmail: {email}\nFood: {food}\nQty: {quantity}"
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject="🍽️ RG Restaurant Order"
        )

        # 4. Show Success Page
        return render_template_string(SUCCESS_HTML, name=name)

    except Exception as e:
        return render_template_string(ERROR_HTML, error=str(e))
    
    finally:
        if db:
            db.close()


# ===============================
# STYLED RESPONSE TEMPLATES
# ===============================
# (Using Python strings to keep it in one file for you)

COMMON_STYLE = """
<style>
    body { 
        margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center;
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1350');
        background-size: cover; font-family: 'Poppins', sans-serif; color: white;
    }
    .card {
        background: rgba(255,255,255,0.1); backdrop-filter: blur(15px);
        padding: 50px; border-radius: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.2);
    }
    .btn {
        display: inline-block; margin-top: 20px; padding: 10px 25px; 
        background: #ff4757; color: white; text-decoration: none; border-radius: 8px;
    }
</style>
"""

SUCCESS_HTML = f"""
{COMMON_STYLE}
<div class="card">
    <h1 style="font-size: 50px;">✅</h1>
    <h2>Order Success!</h2>
    <p>Thank you <strong>{{{{name}}}}</strong>. Your food is being prepared.</p>
    <a href="/" class="btn">Place Another Order</a>
</div>
"""

ERROR_HTML = f"""
{COMMON_STYLE}
<div class="card">
    <h1 style="font-size: 50px;">❌</h1>
    <h2 style="color: #ff6b6b;">Oops! Error Occurred</h2>
    <p style="max-width: 300px;">{{{{error}}}}</p>
    <a href="/" class="btn" style="background: #555;">Try Again</a>
</div>
"""

from flask import render_template_string

# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    # Make sure you have created the 'restaurant' database and 'orders' table in RDS!
    app.run(host='0.0.0.0', port=5000, debug=True)
