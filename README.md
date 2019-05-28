
# **Ionian**
Korea News Crawler

![Code Language](https://img.shields.io/badge/python-3.6-blue.svg) ![Window Supported](https://img.shields.io/badge/windows-not%20supported-red.svg) ![build](https://img.shields.io/circleci/token/YOURTOKEN/project/github/RedSparr0w/node-csgo-parser/master.svg)
   
___
### **Requirements**

- Apache Kafka 2.2

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
### **Feature**
- 기능 구현된 target site
    - Daum
    
#### Collector
- Kafka Producer
- news url 및 meta 정보 수집.

#### Crawler
- Kafka Consumer
- news html 로컬에 저장.
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
consumer_waiting_term_seconds: 5
crawler_waiting_term_seconds: 1
db_writer_size: 20
data_root_path: ./data/raw/text
daum_news_topic_name: daum_news_info
```

___

### **TODO**
- docker 로 실행시 aws 관련 설정 입력값이 아닌 mount path 방식으로 변경하기.
- 기사 본문 scraping 기능 아예 없애진 말고 선택적으로 사용할 수 있도록 구조 변경하기. 
- Daum news html 템플릿 validation test code 추가하기.