# Kafka - Client - Python
A simple Kafka Client in Python.

## Pre-Req:

* You need to have a functioning IBM Event Streams platform. 
* Python version at least 3.9

## Limitation
* The client does not support integration with Schema Registry yet.

## Guide to Getting Started
1. Create a folder in your local laptop and change directory to that folder. 
2. Clone the repositary.   
git clone https://github.com/natarajan-k/kafka-client-python.git

3. Install some libraries.

        pip install kafka-python
        pip install jproperties

4. Test sending / receiving messages.  

        As Producer:   
        python KafkaProducerV1.py <number_of_records>  <config-file> 
        As Consumer:
        python KafkaConsumerV1.py <config-file> 

## Config File
The config.properties file available as part of this package is mostly self-explanatory. 
