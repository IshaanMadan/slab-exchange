from se_app.models import *
from django.core.management.base import BaseCommand
import pandas as pd
import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Adding Fiat Payment Methods")
        data = pd.read_csv (r'/home/deepanshu/Downloads/card_versions.csv') 
        df = pd.DataFrame(data)
        for row in df.itertuples():
            print(row)

            datetime_object = datetime.datetime.strptime(row.Release_Date, '%m/%d/%y')
            print(datetime_object)
            if row.Is_Companion=='N':
                is_comp=False
            else:
                is_comp=True

        #     card_ref = Cards(
        #         release_date=datetime_object,
        #         card_category_id=row.Card_Category_ID,
        #         card_brand_id=row.Card_Brand_ID,
        #         card_set_id=row.Card_Set_ID,
        #         year=row.Year,
        #         number=row.Number,
        #         card_player_id=row.Card_Player_ID,
        #         card_artist_id=row.Card_Artist_ID,
        #         card_team_id=row.Card_Team_ID
        #     )
        #     card_ref.save()
        # self.stdout.write(self.style.SUCCESS("Fiat Payment Methods Added"))

        # for row in df.itertuples():
        #     print(row)
        #     release_date = datetime.datetime.strptime(row.Release_Date + " 00:00:00" , '%m/%d/%y %H:%M:%S')
        #     print(release_date)
        #     return
            card_ref = CardVersions(
                release_date=datetime_object,
                name=row.Name,
                print_run=row.Print_Run,
                is_companion=is_comp,
                card_id=row.Card_ID
                )
            card_ref.save()
        self.stdout.write(self.style.SUCCESS("Fiat Payment Methods Added"))
card_ref.card.card_brand.name
        <release_date> | <name> | <btand_name>