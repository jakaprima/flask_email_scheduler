# official python
FROM python:3.10-slim

# set working directory inside the container
WORKDIR /app

# copy requirements file
COPY requirements.txt requirements.txt

# install
RUN pip install --no-cache-dir -r requirements.txt

# copy rest application to container
COPY . .

# SET ENV
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port flask will run on
EXPOSE 5000

# RUN FLASK
CMD ["flask", "run"]
