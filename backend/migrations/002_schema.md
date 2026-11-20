# Schema v2
Adds sensor authorization and trace ownership on top of v1 (users, audits, datasets, plans, traces).

- `assignments`: admin-managed grant table, one row per (dataset_id, user_id, sensor_id) with a unique constraint; only operators （助教） can hold grants.
- `traces.owner_id`: nullable FK to users; NULL marks historical unowned traces, readable by admin only. Existing databases are upgraded in place with `ALTER TABLE traces ADD COLUMN IF NOT EXISTS owner_id` during seed.
- Trace snapshots carry `scope.sensor_ids` captured at acceptance; revocation of a grant immediately invalidates that owner's traces on that dataset whose scope contains the revoked sensor id (terminal `invalid` status, never restored by re-granting).
