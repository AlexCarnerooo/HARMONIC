web: cd backend && gunicorn app_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
worker: cd frontend_chat && npm run start
