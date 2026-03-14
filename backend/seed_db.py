import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'db.sqlite')

def seed_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    locations = [
        # Districts
        ('district', 'Dehradun'),
        ('district', 'Pauri Garhwal'),
        ('district', 'Nainital'),
        ('district', 'Almora'),
        ('district', 'Haridwar'),
        # Tehsils
        ('tehsil', 'Bironkhal'),
        ('tehsil', 'Kotdwar'),
        ('tehsil', 'Srinagar'),
        ('tehsil', 'Rishikesh'),
        ('tehsil', 'Haldwani'),
        # Villages
        ('village', 'Sila'),
        ('village', 'Maso'),
        ('village', 'Ghandiyal'),
        ('village', 'Banchuri'),
        ('village', 'Dandakhal'),
    ]

    c.executemany('INSERT INTO locations_dictionary (location_type, name) VALUES (?, ?)', locations)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_db()
    print("Database seeded with sample locations.")
