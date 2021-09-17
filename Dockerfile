FROM 3.8

COPY . /usr/KusonimeBot
WORKDIR /usr/KusonimeBot

RUN pip install -r requirements.txt

CMD ["python", "-m", "KusonimeBot"]
