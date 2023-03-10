import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbit", port=5672)
)

channel = connection.channel()

channel.exchange_declare(exchange="dlx", exchange_type="direct")

result = channel.queue_declare(queue="dl")
queue_name = result.method.queue
channel.queue_bind(
    exchange="dlx",
    routing_key="mail_queue",
    queue=queue_name,
)

print(" [*] Waiting for dead-letters. To exit press CTRL+C")


def callback(ch, method, properties, body):
    # TODO: добавить обработку недошедших писем
    print(" [x] %r" % (properties,))
    print(" [reason] : %s : %r" % (properties.headers["x-death"][0]["reason"], body))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue="dl")

channel.start_consuming()
