import pika
import json


RABBITMQ_HOST = "localhost"
QUEUE_NAME = "myqueuename"
RESULT_QUEUE_NAME = "resultqueuename"

def connect_to_rabbitmq():
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

def send_scan_request(message):
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    #channel.queue_declare(queue=QUEUE_NAME, durable=True)
    # Declare a fanout exchange (broadcast to all bound queues)
    channel.exchange_declare(exchange="scan_requests", exchange_type="fanout", durable=True)

    #channel.basic_publish(
    #    exchange="",
    #    routing_key=QUEUE_NAME,
    #    body=message,#json.dumps(message),
    #    properties=pika.BasicProperties(delivery_mode=2),  # Make message persistent
    #)
    # Publish the message to the exchange
    channel.basic_publish(
        exchange="scan_requests",
        routing_key="",  # Fanout exchanges ignore routing keys
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),  # Make message persistent
    )
    connection.close()

def consume_scan_results():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue=RESULT_QUEUE_NAME, durable=True)

    def callback(ch, method, properties, body):
        try:
            result = json.loads(body)
            scan_id = result["scan_id"]
            results_store[scan_id] = result
            print(f"Received results for scan ID: {scan_id}")
        except Exception as e:
            print(f"Error processing result: {str(e)}")

    channel.basic_consume(queue=RESULT_QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print("Waiting for scan results...")
    channel.start_consuming()
