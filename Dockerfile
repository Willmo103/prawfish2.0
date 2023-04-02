FROM Python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# testing out the app in a docker enviornment for development
# final docker image will be built with a production flag, and will not run in debug mode
# will also be built as a dooker compose file, but image will be built with dockerfile
# and saved to docker hub
CMD [ "python", "run.py" , "debug=True"]
