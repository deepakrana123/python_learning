SLIDING_WINDOW_LUA = """
-- KEYS[1] = key for sorted set
-- ARGV[1] = current timestamp
-- ARGV[2] = window size
-- ARGV[3] = request limit

local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local min_score = now - window

-- Remove old entries
redis.call("ZREMRANGEBYSCORE", key, 0, min_score)

-- Count current requests
local count = redis.call("ZCARD", key)

if count < limit then
    redis.call("ZADD", key, now, now)
    redis.call("EXPIRE", key, window)
    return {1, limit - count - 1, 0}
else
    local oldest = redis.call("ZRANGE", key, 0, 0, "WITHSCORES")[2]
    local retry_after = math.floor((oldest + window) - now)
    return {0, 0, retry_after}
end
"""
