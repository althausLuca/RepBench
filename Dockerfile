FROM python:3.10
ENV PYTHONUNBUFFERED 1


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y gcc python3-dev
RUN pip install pycatch22==0.4.2
RUN pip install -r requirements.txt
RUN pip install -U hyperopt
RUN pip install nevergrad
RUN pip install -U zoopt
RUN pip install tsfel
RUN pip install tsfresh==0.20.0
RUN apt-get install -y openjdk-17-jdk
RUN pip install JPype1

RUN pip install pykalman

RUN pip install numba


# Copy project
COPY . /code/





