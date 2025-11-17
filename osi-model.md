# OSI Model, TCP/IP & HTTP - Concise Guide

## OSI Model (7 Layers)

**OSI (Open Systems Interconnection)** - Conceptual framework for understanding network communication

```
┌─────────────────────────────────────────┐
│  7. APPLICATION  │ User-facing apps     │  HTTP, FTP, SMTP, DNS
├──────────────────┼──────────────────────┤
│  6. PRESENTATION │ Data translation     │  Encryption, Compression
├──────────────────┼──────────────────────┤
│  5. SESSION      │ Connection mgmt      │  Session establishment
├──────────────────┼──────────────────────┤
│  4. TRANSPORT    │ End-to-end delivery  │  TCP, UDP
├──────────────────┼──────────────────────┤
│  3. NETWORK      │ Routing & addressing │  IP, Routers
├──────────────────┼──────────────────────┤
│  2. DATA LINK    │ Node-to-node         │  Ethernet, MAC addresses
├──────────────────┼──────────────────────┤
│  1. PHYSICAL     │ Physical transmission│  Cables, signals, bits
└─────────────────────────────────────────┘
```

### Layer Breakdown

**Layer 7 - Application**
- What users interact with
- Examples: Web browsers, email clients
- Protocols: HTTP, HTTPS, FTP, SMTP, DNS

**Layer 4 - Transport**
- Ensures reliable delivery
- **TCP:** Reliable, ordered, error-checked
- **UDP:** Fast, no guarantees

**Layer 3 - Network**
- Routes data across networks
- Uses IP addresses
- Routers operate here

**Layer 1-2 - Physical/Data Link**
- Physical transmission of bits
- MAC addresses, switches
- Ethernet, WiFi

---

## TCP/IP Model (4 Layers)

**TCP/IP** - Practical implementation used on the Internet

```
OSI Model              TCP/IP Model
┌─────────────┐       ┌─────────────┐
│ Application │       │             │
│ Presentation│  ───► │ Application │  HTTP, DNS, FTP
│ Session     │       │             │
├─────────────┤       ├─────────────┤
│ Transport   │  ───► │ Transport   │  TCP, UDP
├─────────────┤       ├─────────────┤
│ Network     │  ───► │ Internet    │  IP, Routing
├─────────────┤       ├─────────────┤
│ Data Link   │       │             │
│ Physical    │  ───► │ Link        │  Ethernet, WiFi
└─────────────┘       └─────────────┘
```

**Why TCP/IP Wins?**
- Simpler, more practical
- Actually used on the Internet
- OSI is theoretical reference

---

## TCP (Transmission Control Protocol)

**Purpose:** Reliable data transmission between applications

### Key Features

**1. Connection-Oriented**
```
Client                Server
  │                     │
  ├──── SYN ──────────► │  (Request connection)
  │ ◄──── SYN-ACK ────┤  (Acknowledge + Request)
  ├──── ACK ──────────► │  (Confirm)
  │                     │
  │   CONNECTION        │
  │   ESTABLISHED       │
  │                     │
  ├──── Data ─────────► │
  │ ◄──── ACK ─────────┤
  │                     │
  ├──── FIN ──────────► │  (Close connection)
  │ ◄──── ACK ─────────┤
```

**2. Reliable Delivery**
- Data arrives in order
- Acknowledges receipt
- Retransmits lost packets
- Error checking

**3. Flow Control**
- Prevents overwhelming receiver
- Adjusts transmission speed

**4. Congestion Control**
- Detects network congestion
- Slows down transmission

### TCP Packet Structure

```
┌────────────────────────────────┐
│ Source Port                    │
├────────────────────────────────┤
│ Destination Port               │
├────────────────────────────────┤
│ Sequence Number                │  (Order packets)
├────────────────────────────────┤
│ Acknowledgment Number          │  (Confirm receipt)
├────────────────────────────────┤
│ Flags (SYN, ACK, FIN, etc)     │
├────────────────────────────────┤
│ Checksum                       │  (Error detection)
├────────────────────────────────┤
│ Data                           │
└────────────────────────────────┘
```

### TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| **Reliability** | Guaranteed delivery | No guarantee |
| **Ordering** | Packets arrive in order | No ordering |
| **Speed** | Slower (overhead) | Faster |
| **Connection** | Connection required | Connectionless |
| **Use Cases** | Web, email, file transfer | Video streaming, gaming, DNS |

**When to Use:**
- **TCP:** When data must arrive correctly (web pages, emails, files)
- **UDP:** When speed matters more than accuracy (live video, voice calls)

---

## HTTP over TCP/IP

### Complete Stack

```
┌──────────────────────────────────────┐
│  Application Layer                   │
│  HTTP Request: GET /page HTTP/1.1    │  ← User-facing
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  Transport Layer (TCP)               │
│  Port 80 (HTTP) or 443 (HTTPS)       │  ← Reliable delivery
│  Break into packets, add sequence    │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  Internet Layer (IP)                 │
│  Add source/dest IP addresses        │  ← Routing
│  192.168.1.1 → 93.184.216.34         │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  Link Layer                          │
│  Convert to electrical signals       │  ← Physical transmission
└──────────────────────────────────────┘
```

### HTTP Request Flow

**Step-by-Step:**

```
1. User types: www.example.com

2. DNS Resolution (Application Layer)
   www.example.com → 93.184.216.34

3. TCP Handshake (Transport Layer)
   Client ←→ Server establish connection
   Port 80 (HTTP) or 443 (HTTPS)

4. HTTP Request (Application Layer)
   GET / HTTP/1.1
   Host: www.example.com

5. TCP Segments (Transport Layer)
   Break request into packets
   Add sequence numbers

6. IP Routing (Network Layer)
   Add IP addresses
   Route across Internet

7. Physical Transmission (Link Layer)
   Convert to signals
   Travel through cables/WiFi

8. Server Receives & Processes
   Reassemble packets
   Process HTTP request

9. HTTP Response
   HTTP/1.1 200 OK
   Content: <html>...</html>

10. TCP Teardown
    Close connection (or keep-alive)
```

---

## Practical Example: Loading a Web Page

**User Action:** Visit `https://api.example.com/users`

**Layer-by-Layer:**

```
┌─────────────────────────────────────────────────────────┐
│ Layer 7: APPLICATION (HTTP)                             │
├─────────────────────────────────────────────────────────┤
│ GET /users HTTP/1.1                                     │
│ Host: api.example.com                                   │
│ User-Agent: Chrome                                      │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 4: TRANSPORT (TCP)                                │
├─────────────────────────────────────────────────────────┤
│ Source Port: 54321                                      │
│ Dest Port: 443 (HTTPS)                                  │
│ Sequence: 1000                                          │
│ Flags: SYN                                              │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: NETWORK (IP)                                   │
├─────────────────────────────────────────────────────────┤
│ Source IP: 192.168.1.100                                │
│ Dest IP: 93.184.216.34                                  │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: DATA LINK (Ethernet)                           │
├─────────────────────────────────────────────────────────┤
│ Source MAC: AA:BB:CC:DD:EE:FF                           │
│ Dest MAC: 11:22:33:44:55:66                             │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 1: PHYSICAL                                       │
├─────────────────────────────────────────────────────────┤
│ 010101010101... (electrical signals)                    │
└─────────────────────────────────────────────────────────┘
```

---

## Port Numbers

**Why Ports?**
Multiple applications on one computer need unique identifiers.

```
Computer IP: 192.168.1.100
├─ Port 80:   Web Server (HTTP)
├─ Port 443:  Secure Web (HTTPS)
├─ Port 22:   SSH
├─ Port 25:   Email (SMTP)
└─ Port 3306: MySQL Database
```

**Common Ports:**
- **80:** HTTP
- **443:** HTTPS
- **22:** SSH
- **21:** FTP
- **25:** SMTP (Email)
- **3306:** MySQL
- **5432:** PostgreSQL
- **27017:** MongoDB

---

## Django Application in Context

**Django App Using Full Stack:**

```python
# Django view (Application Layer - HTTP)
def get_users(request):
    users = User.objects.all()  # Database query
    return JsonResponse({'users': list(users.values())})
```

**What Happens:**

1. **Browser sends HTTP request** (Application Layer)
   ```
   GET /api/users HTTP/1.1
   Host: myapp.com
   ```

2. **TCP ensures delivery** (Transport Layer)
   - Establishes connection
   - Breaks into packets
   - Confirms delivery

3. **IP routes to server** (Network Layer)
   - Finds server using IP address
   - Routes across Internet

4. **Django receives request**
   - URL router matches `/api/users`
   - Calls `get_users()` view
   - Queries PostgreSQL database

5. **Django sends response** (Application Layer)
   ```
   HTTP/1.1 200 OK
   Content-Type: application/json
   
   {"users": [...]}
   ```

6. **TCP delivers response** (Transport Layer)

7. **Browser receives and renders** (Application Layer)

---

## Key Concepts Summary

### OSI Model
- **7 Layers:** Physical → Application
- Conceptual framework
- Helps understand network communication

### TCP/IP
- **4 Layers:** Link → Application
- Practical implementation
- Powers the Internet

### TCP
- **Reliable:** Guaranteed delivery
- **Ordered:** Packets arrive in sequence
- **Connection-based:** Handshake required
- **Use:** Web, email, file transfers

### HTTP over TCP
- HTTP runs on top of TCP
- Default ports: 80 (HTTP), 443 (HTTPS)
- TCP ensures HTTP messages arrive reliably

### Flow
```
User → HTTP Request → TCP (reliable delivery) → IP (routing) → Server
Server → HTTP Response → TCP → IP → User
```

### Django Context
```
Browser ─HTTP→ Django ─ORM→ PostgreSQL
        ←HTTP─       ←───
         ↓
      Over TCP/IP Stack
```
