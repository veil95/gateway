from redis.exceptions import RedisError
from redis.asyncio import Redis
import secrets
from errors import TicketStoreUnavailable
import logging


logger = logging.getLogger(__name__)


class TicketStore:
    TTL_SECONDS = 30

    def __init__(self, redis: Redis):
        self.redis = redis

    async def issue(self, user_id: str) -> str:
        ticket = secrets.token_urlsafe(32)
        try:
            await self.redis.set(f"ticket:{ticket}", user_id, ex=self.TTL_SECONDS)
            return ticket
        except RedisError:
            logger.exception("redis не смог создать тикет, для юзера %s", user_id)
            raise TicketStoreUnavailable

    async def consume(self, ticket: str) -> str | None:
        try:
            user_id = await self.redis.getdel(f"ticket:{ticket}")
            return user_id
        except RedisError:
            logger.exception("redis не смог получить user_id")
            raise TicketStoreUnavailable
