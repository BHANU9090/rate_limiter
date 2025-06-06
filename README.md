# Rate Limiter using Sliding Window Algorithm

## How to Run Rate Limiter

###1. Install Dependencies
Make sure you're in your virtual environment (if using one), then run:

```
pip install fastapi uvicorn
````

### 2. Start the Server

Run the following command from the project root:

```
uvicorn app.main:app --reload --port 8001
```

---

## How to Test the Rate Limiter

**Endpoint:**
[http://localhost:8001/api/data](http://localhost:8001/api/data)

### Steps to Test:

1. **Open your browser or use a tool like Postman.**
2. **Visit the endpoint above.**

**First 10 Requests:**

* On the first access to the browser, 1 request is counted.
* Refresh 9 more times quickly (total 10 requests).
* All requests should succeed with `200 OK`.

**Wait 30 Seconds:**

* You are still within the 60-second sliding window.
* Try again — the 11th request should fail with `429 Too Many Requests`.

**Wait a Full 60 Seconds:**

* After 60 seconds from the first request, try again.
* The request should now succeed, as the old requests have expired.

---

## Approach

### **How Sliding Window Rate Limiting Works**

This project restricts the number of times a user (based on their IP address) can access the API in a given time frame.

**Objective:**
Permit **10 requests per user within a 60-second period**.

**Behavior:**
Additional requests are blocked if the user exceeds 10 within that time window.
A `429 Too Many Requests` error is returned.

---

### **Sliding Window Logic**

We monitor API usage using a sliding time frame.

1. **When a user makes a request:**

   * The current time is recorded.
   * All requests older than 60 seconds are removed from the user's history.

2. **Then we:**

   * Count how many requests the user made in the **last 60 seconds**.
   * If it's **10 or more**, the request is **denied**.
   * If it's **less than 10**, the request is **allowed** and the current time is added to their history.

This ensures the rate limit is checked for the **last 60 seconds**, not fixed time blocks.

---

### **Where is the data stored?**

* The application uses a **Python dictionary with deques** (queues) to store timestamps of requests per IP address.
* This data is stored in **local memory**, so it resets when the server restarts.





