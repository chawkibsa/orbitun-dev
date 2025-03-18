import pika 
import json
import requests

RABBITMQ_HOST="localhost"
#QUEUE_NAME="myqueuename"


def download_script(url):
    """Download the telemetry script from the server."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to download script: {str(e)}")
        return None

def connect_to_rabbitmq():
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

def process_scan_requests():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    #channel.queue_declare(queue=QUEUE_NAME, durable=True)
    # Declare a fanout exchange
    channel.exchange_declare(exchange="scan_requests", exchange_type="fanout", durable=True)

    # Declare a unique queue for this agent
    queue_name = f"agent_queue"#_{AGENT_ID}"
    channel.queue_declare(queue=queue_name, durable=True)

    # Bind the queue to the fanout exchange
    channel.queue_bind(exchange="scan_requests", queue=queue_name)

    def callback(ch, method, properties, body):
        #try:
            request = json.loads(body)
            #scan_id = request["id"]  
            print(json.dumps(request, indent=4))
            #print(scan_id)

            script_content = download_script("http://127.0.0.1:8000/static/test.py")
            print(script_content)
      
    '''
            scan_id = request["scan_id"]
            endpoint_id = request["endpoint_id"]
            script_url = request["script_url"]

            print(f"Received scan request: {scan_id} for endpoint: {endpoint_id}")

            # Download the telemetry script
            script_content = download_script(script_url)
            if not script_content:
                raise Exception("Failed to download telemetry script")

            # Execute the script
            telemetry_data = execute_script(script_content)

            # Prepare the result message
            result_message = {
                "scan_id": scan_id,
                "endpoint_id": endpoint_id,
                "telemetry_data": telemetry_data,
            }

            # Send the result back to the server
            channel.queue_declare(queue=RESULT_QUEUE_NAME, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=RESULT_QUEUE_NAME,
                body=json.dumps(result_message),
                properties=pika.BasicProperties(delivery_mode=2),  # Make message persistent
            )
            print(f"Sent results for scan ID: {scan_id}")
        except Exception as e:
            print(f"Error processing scan request: {str(e)}")
    '''

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("Waiting for scan requests...")
    channel.start_consuming()


if __name__ == "__main__":
    process_scan_requests()