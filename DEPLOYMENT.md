# Deployment Guide for ISWL Work Log

This guide will help you deploy the FastAPI backend and PostgreSQL database on Render.com.

## 1. Database Setup on Render

1. **Create a PostgreSQL Database**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" and select "PostgreSQL"
   - Fill in the following details:
     - Name: `iswl-worklog-db` (or your preferred name)
     - Database: `internlogdb`
     - User: `postgres` (or your preferred username)
     - Region: Choose the closest to your users
   - Click "Create Database"

2. **Get Database Credentials**:
   - After creation, go to the database dashboard
   - Note down the following information:
     - Internal Database URL
     - External Database URL
     - Database Name
     - Username
     - Password
     - Host
     - Port

## 2. Backend Deployment on Render

1. **Prepare Your Repository**:
   - Ensure your repository has the following files:
     ```
     ISWL_Work_Log/
     ├── app/
     │   ├── __init__.py
     │   ├── main.py
     │   ├── database.py
     │   ├── models.py
     │   ├── schemas.py
     │   ├── auth.py
     │   └── routers/
     ├── requirements.txt
     └── render.yaml
     ```

2. **Create requirements.txt**:
   ```txt
   annotated-types==0.7.0
   anyio==4.9.0
   bcrypt==4.3.0
   cffi==1.17.1
   click==8.1.8
   cryptography==44.0.2
   dnspython==2.7.0
   ecdsa==0.19.1
   email_validator==2.2.0
   fastapi==0.115.12
   greenlet==3.2.0
   h11==0.14.0
   httptools==0.6.4
   idna==3.10
   passlib==1.7.4
   psycopg2-binary==2.9.10
   pyasn1==0.4.8
   pycparser==2.22
   pydantic==2.11.3
   pydantic_core==2.33.1
   python-dotenv==1.1.0
   python-jose==3.4.0
   PyYAML==6.0.2
   rsa==4.9.1
   six==1.17.0
   sniffio==1.3.1
   SQLAlchemy==2.0.40
   starlette==0.46.2
   typing-inspection==0.4.0
   typing_extensions==4.13.2
   uvicorn==0.34.2
   uvloop==0.21.0
   watchfiles==1.0.5
   websockets==15.0.1
   ```

   Note: These are the exact versions used in your project. Using these specific versions ensures compatibility and stability.

3. **Create render.yaml**:
   ```yaml
   services:
     - type: web
       name: iswl-worklog-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: DATABASE_URL
           fromDatabase:
             name: iswl-worklog-db
             property: connectionString
         - key: SECRET_KEY
           generateValue: true
         - key: ALGORITHM
           value: HS256
         - key: ACCESS_TOKEN_EXPIRE_MINUTES
           value: 30
   ```

4. **Update CORS Settings**:
   In `app/main.py`, update the origins list to allow testing from any origin during development:
   ```python
   origins = [
       "http://localhost:3000",  # React default port
       "http://localhost:5173",  # Vite default port
       "http://127.0.0.1:3000",
       "http://127.0.0.1:5173",
       "*"  # Allow all origins during testing (NOT recommended for production)
   ]

   app.add_middleware(
       CORSMiddleware,
       allow_origins=origins,
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

5. **Deploy to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Select the repository
   - Fill in the following details:
     - Name: `iswl-worklog-api`
     - Environment: `Python`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add the following environment variables:
     - `DATABASE_URL`: (from your PostgreSQL database)
     - `SECRET_KEY`: (generate a secure random string)
     - `ALGORITHM`: `HS256`
     - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
   - Click "Create Web Service"

## 3. Database Migration

1. **Create Migration Script**:
   Create a file `migrations.py` in your project root:
   ```python
   from app.database import engine
   from app.models import Base

   def init_db():
       Base.metadata.create_all(bind=engine)

   if __name__ == "__main__":
       init_db()
       print("Database tables created successfully!")
   ```

2. **Run Migration**:
   - After deployment, you can run the migration script:
   ```bash
   python migrations.py
   ```

## 4. Verify Deployment

1. **Test the API**:
   - Visit your API URL (e.g., `https://iswl-worklog-api.onrender.com`)
   - You should see the message: `{"message": "FastAPI backend is working ✅"}`

2. **Test Database Connection**:
   - Try to register a new user
   - Try to login
   - Create a work log

## 5. Environment Variables

Make sure these environment variables are set in your Render dashboard:

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
# or set individual components:
DATABASE_HOST=your-db-host
DATABASE_PORT=5432
DATABASE_NAME=internlogdb
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Note: 
- The default PostgreSQL port is 5432
- Make sure to update your database.py to use port 5432 instead of 5434
- You can either use the full DATABASE_URL or set individual components

## 6. Troubleshooting

1. **Database Connection Issues**:
   - Check if the database URL is correct
   - Verify database credentials
   - Check if the database is accessible from your web service

2. **API Issues**:
   - Check the logs in Render dashboard
   - Verify all environment variables are set
   - Check if the port is correctly configured

3. **CORS Issues**:
   - Verify your frontend domain is in the allowed origins
   - Check if the frontend is making requests to the correct API URL

## 7. Maintenance

1. **Database Backups**:
   - Render automatically creates daily backups
   - You can also create manual backups from the database dashboard

2. **Monitoring**:
   - Use Render's built-in monitoring
   - Set up alerts for errors and performance issues

3. **Updates**:
   - Keep your dependencies updated
   - Regularly check for security updates
   - Test updates in a staging environment first

## 8. Security Considerations

1. **Environment Variables**:
   - Never commit sensitive information to your repository
   - Use Render's environment variable management
   - Rotate secrets regularly

2. **Database Security**:
   - Use strong passwords
   - Limit database access to necessary IPs
   - Regularly audit database access

3. **API Security**:
   - Keep FastAPI and all dependencies updated
   - Implement rate limiting
   - Use HTTPS only
   - Implement proper error handling

Would you like me to provide more details about any specific part of the deployment process? 