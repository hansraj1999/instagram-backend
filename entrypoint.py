import uvicorn
import os
import asyncio

from kafka.consumer import KafkaConsumerService

from kafka.config import CONSUMER_TYPE_TO_TOPICS


async def main():
    if os.getenv("TYPE", "SERVER") == "SERVER":
        uvicorn.run(
            "app:start_server", port=8000, host="0.0.0.0", reload=True, factory=True
        )
    elif os.getenv("TYPE") == "CONSUMER":
        kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9093")
        kfk_consumer = KafkaConsumerService(
            topic=CONSUMER_TYPE_TO_TOPICS[os.getenv("TASK")], brokers=kafka_broker
        )
        await kfk_consumer.start()
        await kfk_consumer.consume_messages()


if __name__ == "__main__":

    asyncio.run(main())
