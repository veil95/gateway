from redis.asyncio import Redis


class TicketStore:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def issue(self, user_id: str) -> str:
        pass
    async def consume(self, ticket: str) -> str | None:
        pass
