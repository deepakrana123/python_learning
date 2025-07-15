# KEY TAKEAWAYS:
# - Real-time = instant data push
# - Observer Pattern = core to notification design
# - gRPC/WebSocket allow bi-directional live communication
# - Protobuf makes data small and fast


# 1. What is a Real-Time System?
# → A system where updates are sent instantly to users when something changes.
# Examples: WhatsApp, Uber live location, Google Docs collaboration.

# 2. Observer Pattern (Core Design)
# → Subject = Thing that changes (e.g., chat server)
# → Observers = Clients that listen for updates
# → When subject changes → notifies all observers

# 3. Polling vs WebSocket vs gRPC

# | Type      | Real-Time | Connection Type      | Use Case                      |
# |-----------|-----------|----------------------|-------------------------------|
# | Polling   | ❌ No     | Repeated HTTP        | Old chat, basic notifications |
# | WebSocket | ✅ Yes    | Persistent tunnel    | WhatsApp Web, Slack, Games    |
# | gRPC      | ✅ Yes    | Persistent + smart   | Chat backend, notifications   |

# 4. When to Use What?
# - WebSocket → Web chat, browser-based real-time UI
# - gRPC → Backend-to-backend streaming, secure typed communication
# - Raw Socket → High-performance mobile chat (e.g., WhatsApp)

# 5. Protobuf Basics (Used in gRPC)
# → Defines the structure of data in `.proto` files
# → Much smaller and faster than JSON
# → Required by gRPC
