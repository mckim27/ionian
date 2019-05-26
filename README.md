
# **Ionian**
Korea News Crawler

![Code Language](https://img.shields.io/badge/python-3.6-blue.svg) ![Window Supported](https://img.shields.io/badge/windows-not%20supported-red.svg) ![build](https://img.shields.io/circleci/token/YOURTOKEN/project/github/RedSparr0w/node-csgo-parser/master.svg)
   
---
### **Requirements**

- Apache Kafka 2.2

---
### **Installation**
    
#### Ionian requires :
    1. pyyaml >= 5.1
    2. logzero >= 1.5
    3. beautifulsoup4 >= 4.7
    4. requests >= 2.21
    5. kafka-python >=  1.4
    6. boto3 == 1.9
    7. urllib3 == 1.23
   
 ```bash
$(py3.6 env) python setup.py install 
``` 
---
### **Feature**
- 기능 구현된 target site
    - Daum
    
#### Collector
- Kafka Producer
- news url 수집.
- news meta 정보 수집.

#### Parser
- Kafka Consumer
- news html 로컬에 저장.
- news meta info Dynamo DB 에 저장. 
  ( 별도의 입력값이나 세팅 필요 )    

---
### **Run**
#### collector
- **role** arguments 만 필수.
```bash
$(py3.6 env) python main.py --role=collector \
    --env=dev \
    --target=daum
```

#### crawler
- aws 관련 값도 필수는 아니지만 없는 경우 dynamo db 에 저장하는 기능 동작 하지 않음.
```bash
$(py3.6 env) python main.py --role=crawler \
    --env=dev \
    --target=daum \ 
    --aws_region=ap-northeast-2 \
    --aws_access_key_id=XXXXXXXXXXXXX \
    --aws_secret_access_key=XXXXXXXXXXXXXXXX
```
---
### **Config**
```yaml
log_level: debug
log_dir_name: log
log_file_name: ionian.log
kafka_brokers:
  - 192.168.0.31:9092
consumer_waiting_term_seconds: 5
parser_waiting_term_seconds: 3
db_writer_size: 20
daum_news_topic_name: daum_news_info
```
---
 
### **TODO**
- [X] Daum news link 수집 기능.
- [X] Daum news raw html 저장.
- [ ] Daum news html 템플릿 validation test code 추가하기.