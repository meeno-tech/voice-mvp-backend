## Installation

1. **Clone the Repository:**
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create and Activate a Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Create a `.env` File:**
   ```sh
   touch .env
   ```
   Add the following environment variables inside `.env`:
   ```ini
   LIVEKIT_API_KEY=<your_livekit_api_key>
   LIVEKIT_API_SECRET=<your_livekit_api_secret>
   LIVEKIT_URL=<your_livekit_url>
   ENVIRONMENT=DEV  # Change to PROD for production
   ```

## Running the Application

1. **Start the Server:**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Health Check:** `GET /` 
   - Response: `{ "message": "alive" }`

## Deployment
Code changes are automatically deployed based on branch updates:
- Development Deployment: Merging changes into the `main` branch triggers an automatic deployment to [talkdev.meeno.com](talkdev.meeno.com), which is hosted on an EC2 instance (35.163.245.111).
- Production Deployment: To deploy changes to production, push or merge updates to the `prod` branch. This will trigger an automatic deployment to [talk.meeno.com](talk.meeno.com), which is also hosted on the EC2 instance (35.163.245.111).
