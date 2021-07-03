import pika


def on_message(channel, method_frame, header_frame, body):
    print(f"We have some news! {body}!")
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


connection = pika.BlockingConnection()
channel = connection.channel()
channel.basic_consume("notifications", on_message)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
