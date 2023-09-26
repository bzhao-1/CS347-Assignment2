# Alpine is a very small/lightweight Linux distribution
# We are starting from an alpine image with Python 3 installed
FROM python:3.7-alpine

# Install curl
RUN apk --no-cache add curl

# The WORKDIR command both creates a directory in the container 
# and sets that directory to be the current directory for all further commands
WORKDIR /code

# Copy 'playereval.py' and any dependencies (if needed)
COPY playereval.py /app/

# When the container starts running,
# This is the command that we want to be executed
CMD ["python3", "/app/playereval.py"]