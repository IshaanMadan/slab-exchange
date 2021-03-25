from se_app.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        self.stdout.write("Adding Fiat Payment Methods")
 
        string =""
        card_ref= CardVersions.objects.all()
        for data in card_ref:
            version_name = data.name
            version_release_date = data.release_date
            player_first_name = data.card.card_player.first_name
            player_last_name = data.card.card_player.last_name
            brand_name = data.card.card_brand.name
            artist_name = data.card.card_artist.name
            artist_name2 = data.card.card_artist.name2
            category_name = data.card.card_category.name
            team_full_name = data.card.card_team.full_name
            team_short_name = data.card.card_team.short_name
            team_abbr = data.card.card_team.abbreviation
            set_name = data.card.card_set.name
        
            string = "{0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} | {9} | {10} | {11}".format(version_name,version_release_date,player_first_name,player_last_name,brand_name,artist_name,artist_name2,category_name,team_full_name,team_short_name,team_abbr,set_name)
        
            cards = CardKeywords(
                card_id = data.card_id,
                card_version_id = data.id,
                keyword_string = string 
            )
            cards.save()
