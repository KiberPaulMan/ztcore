# pull official base image
FROM python:3.10-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# library for pdf file generation
#RUN apt-get update && apt-get install -y xvfb libfontconfig wkhtmltopdf

# install psycopg2 dependencies
#RUN apt-get install -y gcc python3-dev musl-dev
# RUN apt-get -y install postgres-server-dev-12 && rm -rf /var/lib/apt/lists/*

# copy project
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.sh
#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
#RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
