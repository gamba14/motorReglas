FROM python:3
WORKDIR /shaffiroRuleEngine
ADD . /shaffiroRuleEngine
RUN echo "America/Argentina/Buenos_Aires" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN pip install -r requirements.txt
CMD ["python3", "rulesEngine.py"]
EXPOSE 5000