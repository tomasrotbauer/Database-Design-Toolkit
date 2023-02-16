FROM python:3
WORKDIR /usr/src/database_design_toolkit
COPY . .
RUN make
ENTRYPOINT ["python", "design_toolkit.py"]
