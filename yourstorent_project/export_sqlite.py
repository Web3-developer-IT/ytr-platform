import sqlite3

# Connect to your existing SQLite database
conn = sqlite3.connect('db.sqlite3')

# Export all tables and data to backup.sql
with open('backup.sql', 'w', encoding='utf-8') as f:
    for line in conn.iterdump():
        f.write('%s\n' % line)

conn.close()
print("✅ backup.sql created successfully!")