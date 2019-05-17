FROM python:3

WORKDIR /servermonitor

RUN git clone https://github.com/ChristianLutzCL/ServerMonitor.git /servermonitor
RUN pip install -r /servermonitor/requirements.txt
RUN pip install .
	
EXPOSE 5000
CMD [ "python", "./run.py" ]


# Build
# docker build -t servermonitor .

# Run
# docker run -d --restart unless-stopped --name ServerMonitor -p 5000:5000 servermonitor
