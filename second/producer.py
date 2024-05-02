import pika
from faker import Faker
from mongoengine import connect

from second.models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

fake = Faker()

channel.queue_declare(queue='email_queue', durable=True)


def generate_contacts(num_contacts):
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contact(name=full_name, email=email)
        contact.save()
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=str(contact.id).encode()
        )


if __name__ == "__main__":
    connect(db="hw8", host="mongodb+srv://lizamelihovaa:tz8OQrxq2U6fVq59@cluster0.lwq50vv.mongodb.net/")
    generate_contacts(100)
