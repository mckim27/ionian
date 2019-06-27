
# **Ionian**
Korean News Crawler

![Code Language](https://img.shields.io/badge/python-3.6-blue.svg) ![Window Supported](https://img.shields.io/badge/windows-not%20supported-red.svg) ![build](https://img.shields.io/circleci/token/YOURTOKEN/project/github/RedSparr0w/node-csgo-parser/master.svg)
   
___
### **Requirements**

- Apache Kafka 2.2
- Pachyderm 1.8.7

___
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

___
### **Description**
- Data Flow
   - collect url -> Kafka stream -> crawl html -> store file to hdfs (hdfs nfs gateway), put html file in the pachyderm pipeline
___
### **Feature**
- 기능 구현된 target site
    - Daum
    
#### Collector
- Kafka Producer
- news url 및 meta 정보 수집.

#### Crawler
- Kafka Consumer
- news html 을 hdfs 에 저장.
- pachyderm pipeline 에 news html 저장.
- news meta info Dynamo DB 에 저장. 
  ( 별도의 입력값이나 세팅 필요 )
      
___
### **Run**
#### collector
- **role** arguments 만 필수.
```bash
$(py3.6 env) python main.py --role=collector \
    --env=dev \
    --target=daum
```

#### crawler
- docker 로 실행 시 aws 관련 값 필수는 아니지만 없는 경우 dynamo db 에 저장하는 기능 동작 하지 않음.
```bash
$(py3.6 env) python main.py --role=crawler \
    --env=dev \
    --target=daum \ 
    --aws_region=ap-northeast-2 \
    --aws_access_key_id=XXXXXXXXXXXXX \
    --aws_secret_access_key=XXXXXXXXXXXXXXXX
```
___
### **Config**
```yaml
log_level: debug
log_dir_name: log
log_file_name: ionian.log
kafka_brokers:
  - 192.168.0.31:9092
  - 192.168.0.32:9092
  - 192.168.0.33:9092
collector_waiting_term_seconds: 2
consumer_waiting_term_seconds: 5
crawler_waiting_term_seconds: 1
db_writer_size: 30
data_root_path: ./data/raw/text
news_topic_name: news_info
news_raw_contents_topic_name: news_raw_contents
news_raw_contents_stream_enable: True
pachd_host: 192.168.0.33
pachd_port: 30650
```

___
