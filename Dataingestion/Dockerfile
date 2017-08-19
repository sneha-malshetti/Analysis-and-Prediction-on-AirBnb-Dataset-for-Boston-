FROM python:2.7



MAINTAINER  Megha_Singh


RUN mkdir -p /usr/src/Dataingestion
WORKDIR /usr/src/Dataingestion

COPY *.py *.json *.sh  /usr/src/Dataingestion/




RUN pip install jupyter notebook
RUN pip install boto3
RUN pip install requests
RUN pip install boto
RUN pip install scipy
RUN pip install boto3 boto luigi numpy pandas sklearn scipy urllib playsound requests seaborn"

RUN pip install numpy
RUN pip install matplotlib
RUN pip install pandas
RUN pip install ipython



ADD run.sh /
RUN chmod +x /run.sh
ENTRYPOINT [""bash", "/run.sh"]


ENTRYPOINT ["bash", "run.sh"]

#ENTRYPOINT ["python", "DataIngestion.py"]


