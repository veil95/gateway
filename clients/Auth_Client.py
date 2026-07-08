from httpx import AsyncClient

class AuthClient:
    async def get_current_user(self, token):
        async with AsyncClient(base_url="http://127.0.0.1:8001") as client:
            token = ""
            response = await client.get("/auth/me", headers={
                "Authorization": f"Bearer {token}"
            })
            if response.status_code < 400:
                return response.json()
            else:
                return {
                    "status": response.status_code,
                    "text": response.text
                }
