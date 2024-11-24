import logging
from aiokafka import AIOKafkaConsumer
from typing import List
from kafka.config import CONSUMER_TYPE_TO_TOPICS, EVENTS_TO_TAKS
from aiokafka.errors import KafkaError


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaConsumerService:
    def __init__(self, brokers: List[str], topic: List[str]):
        self.brokers = brokers
        self.topic = topic
        # self.group_id = group_id
        self.consumer = None

    async def start(self):
        """
        Initialize the consumer and connect to Kafka brokers.
        """
        self.consumer = AIOKafkaConsumer(
            *self.topic,
            bootstrap_servers=self.brokers,
            # group_id=self.group_id,
            auto_offset_reset="latest",  # Start from the earliest available offset
            enable_auto_commit=True,  # Automatically commit offsets
            consumer_timeout_ms=1000,  # Timeout for long polling
            max_poll_records=100,  # Max number of records to fetch in one poll
        )
        await self.consumer.start()
        logger.info(f"Kafka consumer started for topic: {self.topic}")

    async def consume_messages(self):
        """
        Consume messages from Kafka topic.
        """
        try:
            async for msg in self.consumer:
                logger.info(
                    f"Consumed message: {msg.value.decode()} from partition {msg.partition}, offset {msg.offset}"
                )

        except KafkaError as e:
            logger.error(f"Failed to consume message: {e}")
            raise e

    async def stop(self):
        """
        Close the consumer gracefully.
        """
        if self.consumer:
            await self.consumer.stop()
