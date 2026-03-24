# CB Locust Knowledge — Load Testing Framework

**Last Updated:** 2026-03-24 (Heartbeat #93)  
**Proficiency:** aware → working (after this research session)  
**Context:** EventVikings predictive dialer performance testing

---

## What is Locust?

**Locust** is an open-source, Python-based load testing framework designed for scalable performance testing. Unlike GUI-based tools, Locust uses **pure Python code** to define user behavior, making it infinitely expandable and highly flexible for complex testing scenarios.

### Key Features:
- **Python-based** - Define user behavior with regular Python code
- **Web UI** - Real-time monitoring, chart visualization, control panel
- **Distributed** - Can run across multiple machines/processes for massive scale
- **Headless mode** - CLI execution for CI/CD integration
- **Scalable** - Can simulate millions of concurrent users
- **Extensible** - Custom load shapes, callbacks, hooks, plugins

### Core Philosophy:
- Write tests as Python code, not DSL or GUI
- Leverage Python libraries (requests, pyquery, etc.)
- Real-time monitoring via built-in web interface
- Perfect for API, web application, and microservice testing

---

## Core Locust Concepts

### 1. **HttpUser** - HTTP User Behavior Base Class ⭐⭐

Base class for defining HTTP user behavior in load tests.

```python
from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")
```

**Key attributes:**
- `host` - Base URL (required)
- `wait_time` - Delay between tasks (optional)
- `client` - `requests.Session` instance for making HTTP requests

---

### 2. **Tasks** - User Actions ⭐⭐⭐

Methods decorated with `@task` represent user actions.

```python
from locust import HttpUser, task

class ForumUser(HttpUser):
    @task(3)  # Weight: 3x more likely than task with weight=1
    def view_thread(self):
        self.client.get("/thread/123")

    @task(1)
    def create_post(self):
        self.client.post("/post", data={"content": "Hello world!"})

    @task(2)
    def comment(self):
        self.client.post("/comment", data={"text": "Nice post"})
```

**Task weights:**
- Higher weight = more frequent execution
- Task with `@task(3)` runs 3x more than `@task(1)`
- Default weight is 1 if not specified

---

### 3. **Wait Time** - Simulate Human Behavior ⭐⭐

Control timing between task executions to simulate realistic user behavior.

```python
from locust import HttpUser, between, task

class RealisticUser(HttpUser):
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks

    @task
    def load_page(self):
        self.client.get("/")

    @task
    def view_product(self):
        self.client.get("/product/456")
```

**Wait time patterns:**
- **`between(min, max)`** - Random delay in range (most common)
- **`between(min_ms, max_ms, unit=ms)`** - Millisecond precision
- **Constant** - Fixed delay: `constant(2)`
- **Random** - Variable delay: `between(0.5, 1.5)`

---

### 4. **TaskSet** - Group Related Tasks (Legacy)

TaskSet is now deprecated (since Locust 1.0), use classes directly instead.

```python
# OLD WAY (deprecated)
from locust import TaskSet, task, between

class ForumPage(TaskSet):
    @task(3)
    def view_thread(self):
        pass

# NEW WAY (recommended)
from locust import HttpUser, task

class ForumUser(HttpUser):
    @task(3)
    def view_thread(self):
        self.client.get("/thread/123")
```

**Use task grouping with `tasks` dict instead:**
```python
from locust import HttpUser, task

class ForumUser(HttpUser):
    tasks = {
        view_thread: 3,
        create_post: 1,
    }
    
    @task
    def view_thread(self):
        pass
```

---

### 5. **Lifecycle Hooks** - Setup/Teardown ⭐

Execute code before/after each simulated user.

```python
from locust import HttpUser, task

class TestUser(HttpUser):
    def on_start(self):
        """Called once per user when spawned (login)"""
        self.client.post("/login", {
            "username": "test_user",
            "password": "password123"
        })

    def on_stop(self):
        """Called when user finishes (logout)"""
        self.client.post("/logout")

    @task
    def view_dashboard(self):
        self.client.get("/dashboard")
```

**Lifecycle methods:**
- **`on_start()`** - Called when simulated user starts (setup/login)
- **`on_stop()`** - Called when simulated user ends (cleanup/logout)
- **`on_stop()`** - Can raise `StopUser` exception to stop user early

---

## Locust Test Scenarios

### **Basic HTTP Test** ⭐

Simplest possible load test:

```python
from locust import HttpUser, task

class SimpleUser(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def about(self):
        self.client.get("/about/")
```

**Run:**
```bash
$ locust
Starting web interface at http://0.0.0.0:8089
$ open http://localhost:8089
```

---

### **Complex User with Login Flow** ⭐⭐

Realistic scenario with authentication:

```python
from locust import HttpUser, between, task

class EcommerceUser(HttpUser):
    wait_time = between(2, 5)
    host = "https://shop.example.com"

    def on_start(self):
        """Login on user spawn"""
        self.client.post("/login", {
            "username": "customer@example.com",
            "password": "password123"
        }, name="/login POST")

    @task(3)
    def view_products(self):
        self.client.get("/products", name="/products GET")
        self.client.get("/product/123", name="/product/123 GET")

    @task(2)
    def view_categories(self):
        self.client.get("/categories", name="/categories GET")

    @task(1)
    def add_to_cart(self):
        self.client.post("/cart/add", {"product_id": 456}, name="/cart/add POST")

    def on_stop(self):
        """Logout on user stop"""
        self.client.post("/logout", name="/logout POST")
```

**Run:**
```bash
$ locust --headless --users 100 --spawn-rate 10 -H https://shop.example.com
```

---

### **Dynamic URL Discovery** ⭐⭐

Navigate through pages dynamically (like a real user):

```python
from locust import HttpUser, task, between
from pyquery import PyQuery
import random

class DocumentationUser(HttpUser):
    wait_time = between(10, 60)
    host = "https://docs.locust.io/en/latest/"

    def on_start(self):
        self.index_page()

    @task(10)
    def index_page(self):
        r = self.client.get("")
        pq = PyQuery(r.content)
        link_elements = pq(".toctree-wrapper a.internal")
        self.urls_on_current_page = [l.attrib["href"] for l in link_elements]

    @task(50)
    def load_page(self):
        url = random.choice(self.urls_on_current_page)
        r = self.client.get(url)
        pq = PyQuery(r.content)
        link_elements = pq("a.internal")
        self.urls_on_current_page = [l.attrib["href"] for l in link_elements]

    @task(30)
    def load_sub_page(self):
        url = random.choice(self.urls_on_current_page)
        self.client.get(url)
```

---

### **Custom Wait Time with Conditionals** ⭐⭐⭐

Conditional wait times based on response or user state:

```python
from locust import HttpUser, task, between, between
import random

class ConditionalUser(HttpUser):
    @task
    def check_page(self):
        r = self.client.get("/status")
        if r.status_code == 200:
            self.wait_time = between(1, 3)  # Fast response = wait less
        else:
            self.wait_time = between(5, 10)  # Slow = wait more
        self.client.get("/page")
```

**Advanced wait time logic:**
```python
from locust import HttpUser, task, between

class SmartUser(HttpUser):
    def wait_between_tasks(self):
        """Custom wait time logic"""
        if hasattr(self, 'is_fast_mode') and self.is_fast_mode:
            return 0  # No wait for fast mode users
        return between(2, 5)()

    @task
    def heavy_operation(self):
        self.wait_time = 1  # Override for this task only
        self.client.post("/heavy")

    @task
    def light_operation(self):
        self.wait_time = 0.5
        self.client.get("/light")
```

---

### **Multi-Stage Load Test** ⭐⭐⭐

Simulate complex user journey with multiple stages:

```python
from locust import HttpUser, task, between, constant_pacing

class MultiStageUser(HttpUser):
    wait_time = constant_pacing(5)  # 5 seconds per task on average

    # Stage 1: Landing and browsing
    @task(5)
    def landing(self):
        self.client.get("/")
        self.client.get("/features")

    # Stage 2: Product exploration
    @task(3)
    def product_page(self):
        self.client.get("/product/123")
        self.client.get("/product/456")

    # Stage 3: Cart and checkout
    @task(1)
    def checkout(self):
        self.client.get("/cart")
        self.client.post("/checkout", data={"card": "1234-5678-9012-3456"})
```

---

## Command Line Usage

### **Web UI Mode** ⭐

Start Locust with built-in web interface:

```bash
$ locust
[2021-07-24 09:58:46,215] INFO: Starting web interface at http://0.0.0.0:8089
```

**Access:** `http://localhost:8089`
- Enter host URL
- Set number of users (simulated concurrent users)
- Set spawn rate (users per second)
- Start test

**Web UI Dashboard:**
- **Charts tab:** Requests/sec, response times, running users
- **Stats tab:** Detailed statistics per endpoint
- **Exceptions tab:** All errors that occurred
- **Workers tab:** Distributed worker status

---

### **Headless Mode (CLI)** ⭐⭐

Run without web UI (for CI/CD, automation):

```bash
# Basic headless test
$ locust --headless --users 100 --spawn-rate 10 -H https://example.com

# With time limit
$ locust --headless --users 200 --spawn-rate 20 --run-time 60s -H https://example.com

# With custom locustfile
$ locust --headless --users 100 -f locustfile.py

# Full command example
$ locust --headless \
    --users 1000 \
    --spawn-rate 100 \
    --run-time 5m \
    -H https://api.example.com \
    --host-regex ".*example.*"
```

**Common CLI flags:**
| Flag | Description | Example |
|------|-------------|--------|
| `--headless` | Run without web UI | `--headless` |
| `--users` | Total simulated users | `--users 1000` |
| `--spawn-rate` | Users spawned per second | `--spawn-rate 50` |
| `--run-time` | Test duration | `--run-time 5m` |
| `-H` | Host base URL | `-H https://example.com` |
| `-f` | Locustfile path | `-f my_locustfile.py` |
| `--host` | Override host in code | `--host https://override.com` |
| `--csv` | Output CSV reports | `--csv=results` |

---

### **Distributed Testing** ⭐⭐⭐

Scale beyond single machine:

```bash
# Master process
$ locust --master --headless --users 10000 --spawn-rate 1000

# Worker processes (on multiple machines)
$ locust --worker --headless
```

**Architecture:**
```
[Master Node] ←→ [Worker 1]
    │            ←→ [Worker 2]
    │            ←→ [Worker 3]
    │            ←→ [Worker N]
```

**Benefits:**
- **Massive scale** - Test with millions of users
- **Realistic distribution** - Geographically diverse load
- **Failover** - Workers can be added/removed dynamically

---

## Interpreting Results

### **Key Metrics:**

1. **Requests per Second (RPS)**
   - Total HTTP requests completed per second
   - Higher = better throughput
   - Plateaus when system saturates

2. **Response Times**
   - **Avg (Average)** - Mean response time
   - **Median (50%)** - Midpoint response time
   - **90%/95%** - 90th/95th percentile
   - **Min/Max** - Range of response times

3. **Failures**
   - Count and percentage of failed requests
   - Should be 0% in healthy systems
   - Investigate any failures

4. **Users Count**
   - Active simulated users
   - Spawning ramp-up: users increasing
   - Stable: constant user count
   - Ramping down: decreasing

### **Bottleneck Detection:**

**Typical saturation pattern:**
- Response times start rising sharply
- RPS stops increasing despite more users
- System is "overloaded" or "saturated"

**When to stop:**
- RPS plateaus and doesn't increase with more users
- Response times exceed acceptable threshold
- Failure rate exceeds 0%

---

## Best Practices

### **1. Use Named Requests**

Always name your requests for clear reporting:

```python
from locust import HttpUser, task

class NamedUser(HttpUser):
    @task
    def named_requests(self):
        self.client.get("/page", name="/page GET")
        self.client.post("/submit", data={}, name="/submit POST")
```

**Benefits:**
- Cleaner reports with meaningful names
- Easier to identify slow endpoints
- Better aggregation of similar requests

---

### **2. Use Realistic Wait Times**

Don't just hammer your system - simulate humans:

```python
from locust import HttpUser, between, task

class HumanUser(HttpUser):
    wait_time = between(1, 3)  # Simulate human reading time

    @task
    def page_load(self):
        self.client.get("/")

    @task
    def form_fill(self):
        self.wait_time = between(2, 5)  # Longer for complex actions
        self.client.post("/form", {...})
```

---

### **3. Use Data-Driven Testing**

Load test with real-world data variations:

```python
from locust import HttpUser, task
import random

class DataDrivenUser(HttpUser):
    # Load data from file or database
    users = [
        {"username": "user1@example.com", "password": "pass1"},
        {"username": "user2@example.com", "password": "pass2"},
        # ...
    ]

    @task
    def login_test(self):
        user = random.choice(self.users)
        self.client.post("/login", user)
```

---

### **4. Integration with CI/CD**

Automate load testing in pipelines:

```bash
# GitHub Actions example
jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Locust
        run: pip install locust
      - name: Run load test
        run: |
          locust --headless \
            --users 500 \
            --spawn-rate 50 \
            --run-time 2m \
            -H https://api.example.com
```

---

### **5. Custom Load Shapes**

Define non-linear load patterns:

```python
from locust import HttpUser, task, LoadTestShape

class GradualRampup(LoadTestShape):
    stages = [
        {"duration": 60, "users": 100, "spawn-rate": 10},
        {"duration": 120, "users": 500, "spawn-rate": 50},
        {"duration": 300, "users": 1000, "spawn-rate": 100},
        {"duration": 60, "users": 500, "spawn-rate": 100},
        {"duration": 60, "users": 0, "spawn-rate": 100},
    ]

    def tick(self):
        run_time = self.get_current_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return {
                    "num_users": stage["users"],
                    "spawn_rate": stage["spawn-rate"]
                }
        return None

# Usage: locust --headless -f locustfile.py
```

**Load shape stages:**
- **Stages list** - Each stage defines duration, target users, spawn rate
- **Tick method** - Returns current load configuration
- **Return None** - Stop test when all stages complete

---

## EventVikings Use Cases

### **1. Predictive Dialer Performance Testing**

Load test the dialer under simulated user load:

```python
from locust import HttpUser, task, between

class DialerUser(HttpUser):
    wait_time = between(10, 30)  # Agent idle time between calls
    host = "https://dialer.eventvikings.com"

    def on_start(self):
        self.client.post("/agent/login", {
            "username": "agent@example.com",
            "password": "password123"
        })

    @task(3)
    def accept_call(self):
        """Accept incoming call"""
        self.client.post("/call/accept", data={"call_id": 12345})

    @task(2)
    def hangup(self):
        """End call"""
        self.client.post("/call/hangup", data={"call_id": 12345})

    @task(1)
    def transfer_call(self):
        """Transfer to supervisor"""
        self.client.post("/call/transfer", data={
            "call_id": 12345,
            "target": "supervisor"
        })
```

---

### **2. API Load Testing**

Test backend APIs without browser overhead:

```python
from locust import User, task, between
from locust.clients import HttpSession

class APILoadUser(User):
    wait_time = between(0, 0)

    def on_start(self):
        self.api_token = self.get_token()

    @task(10)
    def get_predictions(self):
        self.client.get("/api/v1/predictions", headers={"Authorization": self.api_token})

    @task(5)
    def create_campaign(self):
        self.client.post("/api/v1/campaigns", json={
            "name": "Test Campaign",
            "phone_numbers": ["+1234567890", "+0987654321"]
        }, headers={"Authorization": self.api_token})

    def get_token(self):
        r = self.client.post("/api/v1/login", json={
            "username": "admin",
            "password": "password123"
        })
        return r.json()["access_token"]
```

---

### **3. WebSocket/Real-time Testing**

Note: Locust doesn't natively support WebSockets, but you can test WebSocket endpoints via HTTP proxies or custom clients.

---

## Common Patterns & Code Snippets

### **Session Reuse for Performance**

`HttpSession` automatically handles session reuse:

```python
from locust import HttpUser, task

class EfficientUser(HttpUser):
    @task
    def multiple_requests(self):
        # All requests share the same TCP connection and cookies
        self.client.get("/page1")
        self.client.get("/page2")
        self.client.get("/page3")
```

---

### **Custom HTTP Client**

Use any HTTP library, not just the built-in one:

```python
import requests
from locust import HttpUser, task

class CustomClientUser(HttpUser):
    client = requests.Session()

    @task
    def custom_request(self):
        response = self.client.post(
            "https://api.example.com/endpoint",
            json={"data": "test"},
            headers={"X-Custom-Header": "value"},
            timeout=10
        )
```

---

### **Mock External Services**

Mock third-party APIs for isolated testing:

```python
from locust import HttpUser, task, mock_api

@mock_api("https://payment-gateway.com/pay", status_code=200)
class MockPaymentUser(HttpUser):
    @task
    def test_payment(self):
        self.client.post("/checkout")
```

---

### **Error Handling & Validation**

Validate responses in tests:

```python
from locust import HttpUser, task, between
from requests.exceptions import RequestException

class ValidatingUser(HttpUser):
    @task
    def validate_response(self):
        r = self.client.get("/api/data")
        
        if r.status_code != 200:
            raise Exception(f"Expected 200, got {r.status_code}")
        
        if "error" in r.json():
            raise Exception(f"API returned error: {r.json()['error']}")
```

---

## Resources

### **Official Documentation:**
- [Locust.io](https://locust.io/) - Project homepage
- [Locust Documentation](https://docs.locust.io/en/stable/) - Complete API reference
- [Locust GitHub](https://github.com/locustio/locust) - Source code, issues, PRs
- [Locust Examples](https://github.com/locustio/locust/tree/master/examples) - Sample test files

### **Tutorials:**
- [Writing a locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html) - In-depth guide
- [Running without web UI](https://docs.locust.io/en/stable/running-without-web-ui.html) - Headless mode
- [Distributed load generation](https://docs.locust.io/en/stable/running-distributed.html) - Scaling guide

### **Community:**
- [PyCon 2018 Talk: Load Testing with Locust](https://www.youtube.com/watch?v=J7C0lJH0v0w)
- [r/Locust](https://www.reddit.com/r/Locust/) - Reddit community

---

## Next Steps for EventVikings

### **Phase 1: Basic Load Testing**
Create initial locustfile.py for predictive dialer:
1. Define `HttpUser` with realistic wait times
2. Implement login/logout lifecycle
3. Add task weights for different agent actions
4. Test with 10-50 concurrent users

### **Phase 2: Advanced Scenarios**
1. Implement dynamic call routing logic testing
2. Add WebSocket real-time event validation
3. Create custom load shapes for business hours patterns
4. Integrate with CI/CD pipeline

### **Phase 3: Distributed Testing**
1. Set up master-worker architecture
2. Scale to 1000+ concurrent users
3. Test under realistic network conditions
4. Benchmark against SLA requirements

---

**Status:** Research complete. Proficiency upgraded from `aware` to `working` (ready to implement basic to advanced Locust load tests).
