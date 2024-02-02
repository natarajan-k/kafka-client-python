import sys
import time
import io
#import random
from kafka import KafkaConsumer
from jproperties import Properties
import json

propertiesfile = "./config.properties"
if len(sys.argv) == 2:
    propertiesfile = sys.argv[1]
else:
    sys.exit("ERROR: Properties file needed")

prop = Properties()
try:
    with open(propertiesfile, 'rb') as config_file:
        prop.load(config_file)
    enableintercept = prop.get("enableintercept").data
    enablemtls = prop.get("enablemtls").data
    bootstrapServers = prop.get("bootstrap.servers").data
    retries = prop.get("retries").data
    security = prop.get("security.protocol").data
    saslmechanism = prop.get("sasl.mechanism").data
    sasl_user = prop.get("sasl_user").data
    sasl_password = prop.get("sasl_password").data
    sslendpointidentification = prop.get("ssl.endpoint.identification.algorithm").data
    consumergroupid = prop.get("group.id").data
    consumerclientid = prop.get("client.id").data  
    topic = prop.get("topic").data
    print("topic is: ", topic)
    if "SSL" in security: 
        truststorelocation = prop.get("ssl.truststore.location").data
    if enablemtls.lower() == "true":
        keystorelocation = prop.get("ssl.keystore.location").data
        keylocation = prop.get("ssl.key.location").data
    if saslmechanism == "GSSAPI":
        kerberosservicename = prop.get("sasl.kerberos.service.name").data
    if enableintercept.lower() == "true":
        intercept_bootstrapServers = prop.get("intercept_bootstrapServers").data
        intercept_sasljaas = prop.get("intercept_sasljaas").data
        intercept_security = prop.get("intercept_security").data
        intercept_saslmechanism = prop.get("intercept_saslmechanism").data
except Exception as e:
    print (e)
    print ("Problem reading data from properties file")

consumer_config = {
#        topic
        'api_version':(0,20)
    }
consumer_config.update({"bootstrap_servers": bootstrapServers})
consumer_config.update({"security_protocol":security})
consumer_config.update({"sasl_mechanism":saslmechanism})
consumer_config.update({"sasl_plain_username":sasl_user})
consumer_config.update({"sasl_plain_password":sasl_password})
consumer_config.update({"group_id":consumergroupid})
consumer_config.update({"client_id":consumerclientid})
#consumer_config.update({"max_poll_records":1000})
if "SSL" in security:
    consumer_config.update({"ssl_cafile":truststorelocation})
if enablemtls.lower() == "true":
    consumer_config.update({"ssl_certfile":keystorelocation})
    consumer_config.update({"ssl_keyfile":keylocation})

#print(consumer_config)
consumer = KafkaConsumer(topic, **consumer_config)
consumer.subscribe(topic)
msgcount=1
try:
    while True:
        message = consumer.poll(1000)
        if len(message) == 0:
            print("Polling...")
            msgcount=1
            continue
        else:
            for topic_partition, records in message.items():
                for record in records:
                    print("Message Count: ", msgcount, record)
                    msgcount=msgcount+1
except KeyboardInterrupt:
    print ("Stopped Polling")
consumer.unsubscribe()
consumer.close()

