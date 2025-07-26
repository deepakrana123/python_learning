import time
from collections import deque, defaultdict

user_requests = {}


# this is the fixed window rate limiter
def is_allowed(user_id, limit=3, window=10):
    current_time = int(time.time())

    if user_id not in user_requests:
        user_requests[user_id] = {"start_time": current_time, "count": 1}
        return True

    user_data = user_requests[user_id]
    ellapsed_time = time.time() - user_data["start_time"]
    if ellapsed_time < window:
        if user_data["count"] < limit:
            user_data["count"] += 1
            return True
        else:
            return False
    else:
        user_requests[user_id] = {"start_time": current_time, "count": 1}


sliding_user_request = {}


def is_sliding_window(user_id, limit=3, window=10):
    current_time = int(time.time())

    if user_id not in sliding_user_request:
        sliding_user_request[user_id] = deque([current_time])
        return True
    user_data = sliding_user_request[user_id]
    ellapsed_time = time.time() - user_data[0]
    if ellapsed_time < window:
        if len(user_data) < limit:
            user_data.append(current_time)
            return True
        else:
            return False
    else:
        while user_data and time.time() - user_data[0] > window:
            user_data.popleft()


class LeakyBucket:
    def __init__(self, capacity, leak_rate, last_check):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.last_check = last_check
        self.water_level = 0

    def allow_request(self):
        current_time = time.time()
        time_passed = current_time - self.last_check
        leaked = time_passed * self.leak_rate
        self.water_level = max(0, leaked)
        if self.water_level < self.capacity:
            self.water_level += 1
            return True
        else:
            return False


class TokenBucket:
    def __init__(self, capacity, refill_rate_per_sec):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate_per_sec
        self.last_refill = refill_rate_per_sec

    def allow_request(self):
        current_time = time.time()
        time_passed = current_time - self.last_refill
        refill_amount = time_passed * self.refill_rate

        self.tokens = min(self.capacity, self.tokens + refill_amount)
        if self.tokens > 1:
            self.tokens -= 1
            return True
        else:
            return False


class FixedWindowRateLimiter:
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size
        self.user_request = defaultdict()

    def is_allowed(self, user_id):
        current_time = int(time.time())
        if user_id not in self.user_request:
            user_requests[user_id] = {"start_time": current_time, "count": 1}
            return True
        user_data = self.user_request[user_id]
        ellapsed_time = time.time() - user_data["start_time"]
        if ellapsed_time < self.window_size:
            if user_data["count"] < self.limit:
                user_data["count"] += 1
                return True
            else:
                return False
        else:
            user_requests[user_id] = {"start_time": current_time, "count": 1}


class SlidingWindowRateLimiter:
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size
        self.user_request = defaultdict(deque)

    def is_allowed(self, user_id):
        current_time = int(time.time())
        if user_id not in self.user_request:
            user_requests[user_id].append(current_time)
            return True
        user_data = user_requests[user_id]
        while user_data and user_data[0] < self.window_size:
            user_data.popleft()
        if len(user_data) < self.limit:
            user_data.append(current_time)
            return True
        return False


class SlidingWindowRateLimiterMiddleWare:
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size
        self.user_request = defaultdict(deque)

    def is_allowed(self, user_id):
        current_time = int(time.time())
        if user_id not in self.user_request:
            user_requests[user_id].append(current_time)
            return True
        user_data = user_requests[user_id]
        while user_data and user_data[0] < self.window_size:
            user_data.popleft()
        if len(user_data) < self.limit:
            user_data.append(current_time)
            remaining = self.limit - len(user_data)
            return True, remaining, 0
        else:
            retry_after = self.window_size - (current_time - user_data[0])
            return False, 0, retry_after


# use in fastapi without middleware


from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse
from functools import wraps
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
rate_limiter = SlidingWindowRateLimiterMiddleWare(limit=3, window=10)


@app.get("/")
async def index(request: Request):
    user_id = request.headers.get("X-User-ID", "anonymous")
    allowed, remaining, retry_after = rate_limiter.is_allowed(user_id)
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"error": "Too Many Requests"},
            headers={"Retry-After": str(retry_after)},
        )

    return {"message": "Request successful", "remaining": remaining}


# # in decorator format
# 🧠 What is @wraps?
# @functools.wraps is a decorator for decorators.

# When you write a decorator in Python, it wraps another function. But by default, the original function's:

# __name__

# __doc__

# __annotations__

# etc.

# ...are lost. @wraps preserves those attributes.

# 📌 Simple Example Without @wraps:
# python
# Copy
# Edit
# def my_decorator(func):
#     def wrapper(*args, **kwargs):
#         print("Before function runs")
#         return func(*args, **kwargs)
#     return wrapper

# @my_decorator
# def greet():
#     """Say hello"""
#     print("Hello")

# print(greet.__name__)  # ❌ Outputs: wrapper (not greet)
# print(greet.__doc__)   # ❌ Outputs: None (not "Say hello")
# ✅ With @wraps(func):
# python
# Copy
# Edit
# from functools import wraps

# def my_decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print("Before function runs")
#         return func(*args, **kwargs)
#     return wrapper

# @greet_decorator
# def greet():
#     """Say hello"""
#     print("Hello")

# print(greet.__name__)  # ✅ greet
# print(greet.__doc__)   # ✅ "Say hello"
# ✅ Why use @wraps in real projects?
# Debugging: Stack traces show correct function names.

# Introspection: Tools like Swagger (in FastAPI) read docstrings.

# Preserves metadata: Needed when decorators are nested or reused.

# Testing: Test frameworks use function names to track tests.

# 🔧 TL;DR
# @wraps(original_func) inside a decorator:

# ✅ Keeps the original function’s identity — name, docstring, etc.

# Would you like to try writing a rate limiter decorator using @wraps next?


def rate_limit(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwrags):
        user_id = request.headers.get("X-User-ID")
        allowed, remaining = rate_limiter.is_allowed(user_id)
        if not allowed:
            raise HTTPException(status_code=429, detail="Too many requests")
        response = await func(request, *args, **kwrags)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

    return wrapper


# simple function base


def handle_request(user_id):
    allowed, remaining, retry = rate_limiter(user_id)
    if not allowed:
        print(f" to many request")
        return
    print(f" request processed")


#  middleware class


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limiter):
        super().__init__(app)
        self.rate_limiter = rate_limiter

    async def dispatch(self, request: Request, call_next):
        user_id = request.headers.get("X-User-ID", "anonymous")
        allowed, remaining, retry_after = self.rate_limiter(user_id)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": "To many requests"},
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.rate_limiter.limit),
                    "X-RateLimit-Remaining": "0",
                },
            )
        response: Response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.rate_limiter.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
