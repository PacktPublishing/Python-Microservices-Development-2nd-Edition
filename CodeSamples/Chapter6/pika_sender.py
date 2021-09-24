from pika import BlockingConnection, BasicProperties


# assuming there's a working local RabbitMQ server with a working guest/guest account
def message(topic, message):
    connection = BlockingConnection()
    try:
        channel = connection.channel()
        props = BasicProperties(content_type="text/plain", delivery_mode=1)
        channel.basic_publish("incoming", topic, message, props)
    finally:
        connection.close()


message("publish.playstore", "We are publishing an Android App!")

message("publish.newsletter", "We are publishing a newsletter!")
