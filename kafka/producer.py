import logging
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaProducerService:
    def __init__(self, brokers: List[str], topic: str):
        self.brokers = brokers
        self.topic = topic
        self.producer = None

    async def start(self):
        """
        Initialize the producer and connect to Kafka brokers.
        """
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.brokers,
            linger_ms=10,  # Reduce latency with small batch
            batch_size=16384,  # Adjust batch size for optimal throughput
            acks="all",  # Wait for full acknowledgment from all replicas
            retries=5,  # Number of retries in case of failure
            request_timeout_ms=2000,  # Timeout for requests
        )
        await self.producer.start()
        logger.info(f"Kafka producer started for topic: {self.topic}")

    async def stop(self):
        """
        Close the producer gracefully.
        """
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped.")

    async def send_message(self, message: str):
        """
        Send a message to Kafka.
        """
        try:
            await self.producer.send_and_wait(self.topic, message.encode())
            logger.info(f"Message sent to {self.topic}: {message}")
        except KafkaError as e:
            logger.error(f"Failed to send message: {e}")
            raise e
