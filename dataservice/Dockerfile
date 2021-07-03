FROM python:3.9
COPY . /app/
RUN pip install -r /app/requirements.txt
RUN pip install /app/
CMD ["hypercorn", "--bind", "0.0.0.0:8080", "dataservice:app"] 

