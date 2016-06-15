from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page
from podcast.models import Episode, CastRoot
from django.core.exceptions import ObjectDoesNotExist
import requests, json

APIKEY = "sc_JDJfR4EUt0UOFPwbkU6tMw"
CASTID = "1105"

class Command(BaseCommand):
    help = "Updates the database to include enteries for all published episodes of a podcast"

    def add_arguments(self, parser):
        parser.add_argument('cast_id', nargs='+', type=int)

    def handle(self, *args, **options):

        for cast_id in options['cast_id']:
            #get episode json data
            url = "https://api.simplecast.com/v1/podcasts/"+str(cast_id)+\
                  "/episodes.json?"
            req = requests.get(url, auth=(APIKEY,''))
            data = json.loads(req.text)
            episodes_added = 0

            #get root of the podcast
            try:
                cast = CastRoot.objects.get(pod_id=cast_id)
                print str(cast) + " ---- checking for new episodes"

            except ObjectDoesNotExist:
                print "No podcast found to update with the id: " + str(cast_id)
            
            # print dir(cast)
            
            # run through each published episode id and 
            # check if there are any missing episodes
            for e in data:                
                #create the missing episodes in the database
                try:
                    Episode.objects.get(epID=e['id'])

                except ObjectDoesNotExist:
                    #add if published
                    
                    if e['published']==True:
                        #add to tree
                        new_entry = Episode(slug=str(e['id']),
                                            epID = e['id'],
                                            title=e['title'],
                                            image_URL=e['images']['large'],
                                            description = e['long_description'],
                                            summary = e['description'],
                                            podcast = cast_id,
                                            published_date = e['published_at'],
                                            depth = 2,
                                        )
                        cast.add_child(instance=new_entry)
                        episodes_added += 1

                    #print the results of what happened
            print "Cast " + str(cast_id) +\
                " had " + str(episodes_added) + " episodes added"

