FROM python:3.7-slim-stretch

# update and install
RUN apt-get update && apt-get --yes --no-install-recommends install \
    build-essential

RUN mkdir -p /opt/app
WORKDIR /opt/app

# install python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8501

# copy rest
COPY *.py ./

CMD ["streamlit", "run", "run_app.py"]





