# Stage 1: Use the official python:3-alpine base image
# This is a lightweight image, which is great for production.
FROM python:3-alpine

# Set the working directory inside the container
WORKDIR /app


# Install build tools for Alpine (C/C++ compilers, Rust, etc.)
RUN apk add --no-cache build-base cargo rust

# Install 'uv', the fast Python package installer.
RUN pip install --no-cache-dir uv

# Copy only the requirements file first.
COPY requirements.txt .

# Install Python dependencies using uv.
RUN uv venv --system
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
RUN uv pip install -r requirements.txt

# Copy the rest of your application code (including run.py)
# This layer will be rebuilt if you change your code,
# but the dependency layer above will be reused, making builds fast.
COPY . .

# Specify the command to run when the container starts.
# This executes `python3 run.py`

EXPOSE 8000

CMD ["uv", "run", "run.py"]