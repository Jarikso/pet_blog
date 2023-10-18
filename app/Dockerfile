FROM python:3.9
COPY . /blog/app
WORKDIR ./blog
RUN python -m pip install -r app/requirements.txt
ENTRYPOINT ["python"]
CMD ["app/main.py"]