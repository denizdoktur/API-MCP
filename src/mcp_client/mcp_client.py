import httpx


class FastApiMCPDiscoveryClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)

    def discover(self):
        """MCP discovery mekanizması. Önce .well-known, sonra OpenAPI."""
        discovery_data = {}

        # Try MCP well-known
        try:
            response = self.client.get("/.well-known/mcp.json")
            if response.status_code == 200:
                discovery_data["mcp_metadata"] = response.json()
        except httpx.RequestError:
            pass

        # Try OpenAPI discovery
        try:
            response = self.client.get("/openapi.json")
            response.raise_for_status()
            openapi_data = response.json()
            discovery_data["openapi"] = openapi_data
            discovery_data["tools"] = list(openapi_data.get("paths", {}).keys())
        except httpx.RequestError as e:
            print("OpenAPI discovery failed:", e)

        return discovery_data

    def list_tools(self):
        data = self.discover()
        return data.get("tools", [])

    def get_tool_details(self, path: str):
        """Seçilen tool'un OpenAPI tanımını döner."""
        data = self.discover()
        openapi = data.get("openapi", {})
        path_item = openapi.get("paths", {}).get(path, {})
        return path_item

    def call_tool(self, path: str, parameters: dict):
        """Belirtilen tool'u verilen parametrelerle çağırır."""
        response = self.client.post(path, json=parameters)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()



if __name__ == "__main__":
    client = FastApiMCPDiscoveryClient(base_url="http://localhost:9000")

    try:
        discovery_data = client.discover()
        print("Discovery completed.")

        print("Tools:")
        for tool in client.list_tools():
            print("-", tool)

        # Bir tool detayını çek
        sample_path = client.list_tools()[0]
        tool_detail = client.get_tool_details(sample_path)
        print(f"\nTool Details for '{sample_path}':")
        print(tool_detail)

    finally:
        client.close()
