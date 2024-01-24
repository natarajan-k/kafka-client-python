import sys
import time
import io
import random
from kafka import KafkaProducer
from jproperties import Properties
import json

file1Name = "./file1.txt"
file2Name = "./file2.txt"
file3Name = "./file3.txt"

loadsize = 1
propertiesfile = "./config.properties"
if len(sys.argv) == 3:
    propertiesfile = sys.argv[2]
    loadsize = sys.argv[1]
else:
    sys.exit("ERROR: Properties file and number of records needed")

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

producer_config = {
        'api_version':(0,20)
    }
producer_config.update({"bootstrap_servers": bootstrapServers})
producer_config.update({"security_protocol":security})
producer_config.update({"sasl_mechanism":saslmechanism})
producer_config.update({"retries":retries})
producer_config.update({"sasl_plain_username":sasl_user})
producer_config.update({"sasl_plain_password":sasl_password})
producer_config.update({"acks":"all"})
if "SSL" in security:
    producer_config.update({"ssl_cafile":truststorelocation})
if enablemtls.lower() == "true":
    producer_config.update({"ssl_certfile":keystorelocation})
    producer_config.update({"ssl_keyfile":keylocation})

#print(producer_config)
producer = KafkaProducer(**producer_config)
try:
    file1=open(file1Name,"r")
    lines1=file1.readlines()
    file2=open(file2Name,"r")
    lines2=file2.readlines()
    file3=open(file3Name,"r")
    lines3=file3.readlines()
except Exception as e:
    print (e)
    print ("Problem reading customer data file")
#sys.exit("okokoko")
message={ 'customer_data_version':'v 1'}
for i in range(int(loadsize)):
    message.update({"first_name":random.choice(lines1).replace('\n', '')})
    message.update({"last_name":random.choice(lines2).replace('\n', '')})
    message.update({"country":random.choice(lines3).replace('\n', '')})
    message.update({"age":random.randint(5, 80)})
    print("Message: ",i+1,"  ",message)
    producer.send(topic, str(message).encode('utf-8'))
time.sleep(10)
file1.close
file2.close
file3.close

