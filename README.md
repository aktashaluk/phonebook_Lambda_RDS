# phonebook_Lambda_RDS
# Serverless Phonebook Application (Flask + AWS Lambda + RDS MySQL)

This project implements a serverless phonebook application utilizing a 3-tier architecture: an **EC2 instance** hosting a Flask web frontend, **AWS Lambda** handling backend business logic, and an **Amazon RDS (MySQL)** instance for data persistence.

## Architecture & Components

1. **Frontend (EC2 & Flask):**
   - Hosted on an AWS EC2 instance (`app.py`).
   - Manages user requests for adding, updating, and searching phone records.
   - Communicates with the backend logic by triggering an AWS Lambda Function URL.

2. **Backend Logic (AWS Lambda):**
   - Deployed via a deployment package (.zip file) containing the `lambda_function.py` handler and the `PyMySQL` dependency.
   - Configured with environment variables (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`) to securely connect to the RDS database.
   - Designed to automatically ensure the required table (`contacts`) exists upon execution.

3. **Database Layer (Amazon RDS MySQL):**
   - A managed MySQL instance storing contact records (`id`, `name`, `phone_number`).
   - Integrated with Lambda within the same VPC, utilizing dedicated subnets and security groups to allow secure internal communication on port 3306.


## Step-by-Step Setup Guide

1. **EC2 Instance Setup:**
   - Install dependencies (`pip3`, `Flask`, `requests`, etc.) on the EC2 instance.
   - Create the project directory structure:
     ```bash
     /home/ec2-user/phonebook-ui/
     ├── app.py
     └── templates/
         └── index.html
     ```
   - Copy the respective application files into the directory.

2. **AWS Lambda & Function URL Configuration:**
   - Go to the AWS Lambda console and open your function.
   - Under the **Configuration** tab, select **Function URL**.
   - Create a function URL with:
     - **Auth type:** `NONE`
     - **Configure CORS:** Enabled (Allow origin: `*`)
   - Save the configuration and copy the generated Lambda Function URL.

3. **Connecting Flask to Lambda:**
   - Open `app.py` on your EC2 instance and paste the Lambda Function URL into the `LAMBDA_URL` variable.

4. **RDS & Environment Integration:**
   - Configure the RDS Endpoint in the Lambda function's **Environment Variables** (`DB_HOST`...).
   - Ensure the Lambda function is attached to the correct VPC, subnets, and security group for seamless database connectivity.
   - To enable only the Lambda function to interact with Database add the security group of Lambda as inbound rule of RDS Instance.


# User > EC2 (Flask App) > HTTP Request (POST/GET) >  Lambda Function URL > Lambda (Python App) > RDS MySQL
