import pika
from mongoengine import connect
from models import Contact

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.get(id=contact_id)
    # Imitate sending email
    print(f"Sending email to {contact.email}...")
    # Mark email as sent
    contact.is_sent = True
    contact.save()


channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

if __name__ == "__main__":
    connect(db="hw8", host="mongodb+srv://lizamelihovaa:tz8OQrxq2U6fVq59@cluster0.lwq50vv.mongodb.net/")
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
