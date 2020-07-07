FROM python:3
WORKDIR /shaffiroRuleEngine
ADD . /shaffiroRuleEngine
RUN pip install -r requirements.txt
CMD ["python3", "rulesEngine.py"]
EXPOSE 5000

