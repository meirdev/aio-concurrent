# aio-concurrent

Run concurrent tasks with asyncio.

# Example

```python
from aio_concurrent import concurrent
from aio_concurrent.functions import rm

async def main():
    # Delete all .pyc files under the current directory
    await concurrent(rm("./**/*.pyc"))
```
