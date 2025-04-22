from models import Item, Base
from sqlalchemy import create_engine, func, cast, Integer
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import style
import pandas as pd

engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# -- QUERY TYPES
backgrounds = session.query(Item).filter(Item.item_type == "Card Background").count()
portraits = session.query(Item).filter(Item.item_type == "Operator Portrait").count()
charms = session.query(Item).filter(Item.item_type == "Charm").count()
headgears = session.query(Item).filter(Item.item_type == "Headgear").count()
uniforms = session.query(Item).filter(Item.item_type == "Uniform").count()
weapon_skins = session.query(Item).filter(Item.item_type == "Weapon Skin").count()
attachment_skins = session.query(Item).filter(Item.item_type == "Attachment Skin").count()
drone_skins = session.query(Item).filter(Item.item_type == "Drone Skin").count()
gadget_skins = session.query(Item).filter(Item.item_type == "Gadget Skin").count()

# -- QUERY RARITY
legendary = session.query(Item).filter(Item.rarity == "Legendary").count()
epic = session.query(Item).filter(Item.rarity == "Epic").count()
rare = session.query(Item).filter(Item.rarity == "Rare").count()

# -- QUERY SEASONS --
seasons = (session.query(
    Item.season, func.count(Item.id).label('count'))
    .group_by(Item.season)
    .order_by(
        cast(func.substr(Item.season, 2, 1), Integer),  # year number
        cast(func.substr(Item.season, 4, 1), Integer),  # season number
    )
    .all()
)

for season , count in seasons:
    print(f"{season.upper()}: {count}")





def main():
    style.use("dark_background")

    # Create a GridSpec layout: 2 rows and 1 column for the top, and 1 row spanning the full bottom
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(2, 2, height_ratios=[1, 2])  # Create 2 rows with bottom row twice as large

    # TYPE DISTRIBUTION PIE CHART (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    type_distribution = [
        backgrounds,
        charms,
        headgears,
        gadget_skins,
        uniforms,
        attachment_skins,
        weapon_skins,
        drone_skins,
        portraits
    ]

    type_labels = [
        "backgrounds",
        "charms",
        "headgears",
        "gadget skins",
        "uniforms",
        "attachment skins",
        "weapon skins",
        "drone skins",
        "portraits"
    ]

    colors = [
        "red",
        "yellow",
        "green",
        "blue",
        "orange",
        "indigo",
        "violet",
        "white",
        "cyan"
    ]

    explodes = [0, 0, 0, .2, 0, 0, 0, .2, 0]

    ax1.pie(
        type_distribution,
        colors=colors,
        autopct='%1.1f%%',
        pctdistance=1.2,
        startangle=135,
        explode=explodes,
        radius=1.5)
    ax1.legend(labels=type_labels,
               loc="center left",
               bbox_to_anchor=(-1.5, 0.5))
    ax1.set_title("Type Distribution", pad=65, fontname="JetBrains Mono", fontsize=16)


    # RARITY DISTRIBUTION PIE CHART (top right)
    ax2 = fig.add_subplot(gs[0, 1])
    rarity_distribution = [
        legendary,
        epic,
        rare
    ]

    rarity_labels = [
        "Legendary",
        "Epic",
        "Rare"
    ]

    ax2.pie(
        rarity_distribution,
        colors=["orange", "violet", "cyan"],
        autopct='%1.1f%%',
        pctdistance=1.2,
        startangle=-135,
        radius=1.5)
    ax2.legend(labels=rarity_labels,
               loc="center right",
               bbox_to_anchor=(2, 0.5))
    ax2.set_title("Rarity Distribution", pad=65, fontname="JetBrains Mono", fontsize=16)

    # SEASON DISTRIBUTION BAR CHART (bottom spanning full width)
    ax3 = fig.add_subplot(gs[1, :])  # This takes up both columns of the bottom row
    season_distribution = [season for season, count in seasons]
    count_distribution = [count for season, count in seasons]
    ticks = list(range(0, 101, 10))

    ax3.bar(season_distribution, count_distribution, width=0.9)
    ax3.set_ylabel("Number of items", fontname="JetBrains Mono", fontsize=12, labelpad=10)
    ax3.set_xlabel("Seasons", fontname="JetBrains Mono", fontsize=12, labelpad=10)
    ax3.set_yticks(ticks, [f"{x}" for x in ticks])

    ax3.set_title("Season Distribution", fontname="JetBrains Mono", fontsize=16)
    ax3.set_xlim(-0.5, len(season_distribution) - 0.5)



    fig.suptitle("SIEGE CELEBRATION PACK DATA", fontsize=14)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()