# Stage 1: Use the official python:3-alpine base image
# This is a lightweight image, which is great for production.
FROM python:3-alpine

# Set the working directory inside the container
WORKDIR /app

# Install 'uv', the fast Python package installer.
# We use --no-cache-dir to keep the image layer slim.
RUN pip install --no-cache-dir uv

# Copy only the requirements file first.
# This step is cached by Docker. As long as your requirements.txt
# doesn't change, Docker will reuse this layer and the next one.
COPY requirements.txt .

# Install Python dependencies using uv.
RUN uv pip install -r requirements.txt

# Copy the rest of your application code (including run.py)
# This layer will be rebuilt if you change your code,
# but the dependency layer above will be reused, making builds fast.
COPY . .

# Specify the command to run when the container starts.
# This executes `python3 run.py`
CMD ["python3", "run.py"]