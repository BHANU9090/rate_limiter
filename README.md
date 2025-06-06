 How to Run Rate Limiter
 1. Install Dependencies
Make sure you're in your virtual environment (if using one), then run:
pip install fastapi uvicorn

 2. Start the Server
Run the following command from the project root:
uvicorn app.main:app --reload --port 8001

 How to Test the Rate Limiter
Endpoint:
http://localhost:8001/api/data
🧾 Steps to Test:
Open your browser or use a tool like Postman.

Visit the endpoint above.

✅ First 10 Requests:
On the first access to the browser, 1 request is counted.

Refresh 9 more times quickly (total 10 requests).

All requests should succeed (200 OK).

⏳ Wait 30 Seconds:
You're still within the 60-second sliding window.

Try again — the 11th request should fail with 429 Too Many Requests.

🕐 Wait a Full 60 Seconds:
After 60 seconds from the first request, try again.



APPROACH: 
 **How Sliding Window Rate Limiting Works**
 This project restricts the number of times a user (depending on their IP address) can use the API in a given period of time.

 Objective: Permit ten requests per user in a 60-second period.

 Additional requests are banned if the user submits more than ten requests within that period (429 Too Many Requests).

**Sliding Window Logic: We monitor API usage using a sliding time frame.**

 1.Whenever a user submits a request, we:

  Find out the time now.

   Delete requests that are older than sixty seconds from their history.

 2.Next, we

   Determine the number of requests they have made in the previous sixty seconds.

   If it is ten or more, the request is denied.

   We permit it and save the current time if it is less than ten.

   This guarantees that the limit is never checked for set time blocks, but rather for the last 60 seconds.

 **Where is the data related to the request stored?**
 
 The application stores timestamps for every IP address using a Python dictionary with deques (queues).

 When the server restarts, this is reset because it is saved in local memory.
