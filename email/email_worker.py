import pika
from send_mail import send_mail
import json


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbit", port=5672)
    )
    channel = connection.channel()

    name = channel.queue_declare(
        queue="mail_queue",
        durable=True,
        arguments=({"x-message-ttl": 10000, "x-dead-letter-exchange": "dlx"}),
    )
    print("name -- ", name)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        parsed_body = json.loads(body)
        try:
            send_mail(parsed_body["dest_email"], parsed_body["text"])
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            # TODO: save fails, log err

    channel.basic_consume(
        queue="mail_queue", on_message_callback=callback, auto_ack=False
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
