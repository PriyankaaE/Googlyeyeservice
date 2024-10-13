FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Create the user that will run the app
RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /opt/googly_eye_generator

ARG PIP_EXTRA_INDEX_URL

# Install requirements, including from Gemfury
ADD ./googly_eye_generator /opt/googly_eye_generator/
RUN pip install --upgrade pip
RUN pip install -r /opt/googly_eye_generator/requirements.txt

RUN chmod +x /opt/googly_eye_generator/run.sh
# RUN tox
RUN chown -R ml-api-user:ml-api-user ./

USER ml-api-user

CMD ["bash", "./run.sh"]