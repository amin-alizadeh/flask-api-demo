from flask_seeder import Seeder, Faker, generator
import random
from app.models import Members, Comments

# All seeders inherit from Seeder
class DemoSeeder(Seeder):
  
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1  # Lower numbers run first
        
    def run(self):
        print("Seeding demo data...")
        # Create 5 users
        for i in range(5):
            print("Adding user")
            self.db.session.add(Members(
                login=f"test{i+1}",
                first_name=f"fname{i+1}",
                last_name=f"lname{i+1}",
                title=f"title{i+1}",
                email=f"test{i+1}@example.com",
                avatar_url=f"http://example.com/avatar{i+1}.png",
                followers=random.randint(1, 200),
                following=random.randint(1, 200)
            ))
        self.db.session.commit()
        
        for i in range(5):
            print("Adding comment")
            self.db.session.add(Comments(
                feedback=f"Comment {i+1}"
            ))
        self.db.session.commit()