from web3 import AsyncWeb3, AsyncHTTPProvider
from configs.config import rpc, proxy_to_connect_to_rpc

request_kwargs = {"proxy": f'http://{proxy_to_connect_to_rpc}'} if proxy_to_connect_to_rpc else {}
w3 = AsyncWeb3(provider=AsyncHTTPProvider(endpoint_uri=rpc, request_kwargs=request_kwargs))
