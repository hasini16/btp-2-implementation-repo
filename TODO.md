                

## Approved Plan Steps:
1. [x] Update `cnc_automation_project/backend/requirements.txt` (add SQLAlchemy deps)
2. [x] Create `cnc_automation_project/backend/database.py` (Supabase engine/session)
3. [x] Create `cnc_automation_project/backend/models.py` (SensorFeed model)
4. [x] Edit `cnc_automation_project/backend/app.py` (DB init, Base.metadata.create_all)
5. [x] Edit `cnc_automation_project/backend/api/live_feed_routes.py` (insert on WS receive)
6. [x] Install deps: `cd cnc_automation_project/backend && pip install -r requirements.txt`
7. [ ] User: Create `sensor_feeds` table in Supabase SQL editor: CREATE TABLE IF NOT EXISTS sensor_feeds (id SERIAL PRIMARY KEY, timestamp TIMESTAMPTZ DEFAULT NOW(), accel_x NUMERIC, accel_y NUMERIC, accel_z NUMERIC, machine_id TEXT DEFAULT 'cnc1');
8. [ ] Test: cd backend && uvicorn app:app --reload, connect ESP32 or curl/mock WS, query SELECT * FROM sensor_feeds ORDER BY timestamp DESC LIMIT 5;

**Next: Install deps and create table.**


