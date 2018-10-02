FROM python:3.7

# export TMP_SELENIUM_PASS="seleniumpass"
# export TMP_PANDAS_PASS="pandaspass"
# docker build docker/selenium/. -t selenium --build-arg TMP_SELENIUM_PASS --build-arg TMP_PANDAS_PASS
# docker run -t selenium
#
# Added the django requirements.txt also.

ENV PYTHONUNBUFFERED=1
WORKDIR /tmp

# Enable source repos for allowing the build-dep command later
# Also removes us. from the front.  That mirror goes down a lot.
COPY sources.list /etc/apt/sources.list

#Update keys to match new sources.list.  The US mirrors seem to go down or get throttled a lot.
RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3B4FE6ACC0B21F32
RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com C2518248EEA14886
RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 40976EAF437D05B5

RUN apt update
RUN apt upgrade -fy
RUN apt install -fy openssh-client=1:7.2p2-4ubuntu2.4 --allow-downgrades
RUN apt install -fy openssh-server

# Install dependencies and configure logging.
RUN apt-get update && apt-get install --no-install-recommends -y \
    procps \
    && \
  pip install --upgrade pip && \
  rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# need dev version of celery (and its dependencies) until 
# this issue is resolved:  https://github.com/celery/celery/issues/4849
RUN pip install --upgrade https://github.com/celery/celery/tarball/master

# Add code to container.
COPY . /code

WORKDIR /code
ENV PATH /code:$PATH

#Passwords for users.  The ARG then ENV pattern means the values are more ephemeral.
ARG TMP_SELENIUM_PASS
ENV SELENIUM_PASS=$TMP_SELENIUM_PASS

ARG TMP_PANDAS_PASS
ENV PANDAS_PASS=$TMP_PANDAS_PASS

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt -y update
RUN apt install -y google-chrome-stable

# install chromedriver
RUN apt install -y unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip install selenium==3.13.0

RUN mkdir /var/run/sshd

# add selenium user
RUN useradd -ms /bin/bash seleniumuser
# RUN export TMP_SELENIUM_PASS="herpityderpity"

RUN usermod --password $(echo $SELENIUM_PASS | openssl passwd -1 -stdin) seleniumuser

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Add pandas support
#
RUN useradd -ms /bin/bash pandasuser
RUN usermod --password $(echo $PANDAS_PASS | openssl passwd -1 -stdin) pandasuser

RUN apt install -y xclip

RUN apt install -y libhdf5-dev cmake
#Install all optional dependencies for pandas, so you can't be missing anything.

RUN python -m pip install pip --upgrade

RUN pip install Cython numexpr bottleneck scipy pandas==0.23.3 psycopg2 pymysql xlrd xlwt openpyxl XlsxWriter Jinja2 s3fs>=0.0.7 blosc pandas-gbq BeautifulSoup4>=4.2.1 lxml sqlalchemy>=0.8.1 xarray>=0.7.0

RUN pip install tables

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

# run it as docker run -d -t selenium  

# This is terrible - apache should know better
# https://arrow.apache.org/install/
# Abandoned - require unsigned packages - pyarrow>=0.4.1 feather-format>=0.3.1
