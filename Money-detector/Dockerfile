# 1️⃣ Use an official Python image
FROM python:3.11-slim

# 2️⃣ Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set working directory inside container
WORKDIR /app

# 4️⃣ Copy requirements first (helps caching)
COPY ./Money-detector/requirements.txt .


# 5️⃣ Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy the rest of the project files
COPY . .

# 7️⃣ Expose the port Flask will use
EXPOSE 5000

# 8️⃣ Command to run the Flask app
CMD ["python", "app.py"]