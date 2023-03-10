import pika
import time


class RabbitQueue:
    def __init__(self) -> None:
        self.set_up_rabbitmq()
        # TODO: энвы из файла

    def set_up_rabbitmq(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbit", port="5672")
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue="mail_queue",
            durable=True,
            arguments=({"x-message-ttl": 10000, "x-dead-letter-exchange": "dlx"}),
        )

    def add_task(self, body: str) -> None:
        self.channel.basic_publish(
            exchange="",
            routing_key="mail_queue",
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print(f" [x] Sent time ", time.time(), "body", body)


queue = RabbitQueue()
