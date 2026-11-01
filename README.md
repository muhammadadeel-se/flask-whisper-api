## Task 5: Production Deployment & Handover

### Live Application
* **Public URL:** [https://flask-whisper-api-production.up.railway.app](https://flask-whisper-api-production.up.railway.app)
* **Demo Video:** [Watch Loom Demo](https://www.loom.com/share/your-demo-link)

---

### Environment Variables
Set the following variables in the Railway dashboard under **Settings > Variables**:

| Variable Name | Description | Required |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | OpenAI API key for transcript action extraction | Yes |
| `FLASK_ENV` | Application environment (`production` / `development`) | Yes |
| `PORT` | Auto-assigned web server port by Railway | Auto |

---

### Deployment Steps (Railway)
1. Fork or clone this repository.
2. Link the repository to a new Railway project (**New Project > Deploy from GitHub**).
3. Configure required Environment Variables (`OPENAI_API_KEY`) in the Railway Dashboard.
4. Railway detects `Procfile` and builds the service automatically using `gunicorn app:app`.
5. Under **Settings > Networking**, click **Generate Domain** to get the public production URL.