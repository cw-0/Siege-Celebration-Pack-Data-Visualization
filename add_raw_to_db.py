from models import Item, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

new_items = []

with open("data.txt", "r", encoding="UTF-8") as file:
    for line in file:
        splits = line.strip().split(" ")
        rarity = splits[0]
        season = splits[1]

        skin_or_name = splits[3]
        if skin_or_name in ["Skin", "Background", "Portrait"]:
            item_type = f"{splits[2]} {splits[3]}"
            name = splits[4:]
        else:
            item_type = splits[2]
            name = splits[3:]

        new_item = Item(
            rarity=rarity,
            season=season,
            item_type=item_type,
            name=" ".join(name)
        )
        new_items.append(new_item)


session.add_all(new_items)
session.commit()