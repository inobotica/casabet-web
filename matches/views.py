import requests
import json

from django.shortcuts import render
from django.http      import HttpResponse

# Create your views here.
def index(request):
    URL = "https://1xuovgghf1.execute-api.us-east-1.amazonaws.com/production/GetOdds"
    r = requests.get(url = URL)#, params = PARAMS)
    
    try:
        data = r.json()
    except json.decoder.JSONDecodeError as e:
        print('Empty response from server')
        data = []

    # update values
    for index, row in enumerate(data):

        # Update leading zeros
        
        print(data[index])

        # Update odds
        h_odds = 1/data[index]['homeOdds'] if data[index]['homeOdds'] else 0
        x_odds = 1/data[index]['xOdds']    if data[index]['xOdds']    else 0
        a_odds = 1/data[index]['awayOdds'] if data[index]['awayOdds'] else 0
        total_odds = h_odds + x_odds + a_odds

        r_home_odds = 100*h_odds/total_odds if data[index]['homeOdds'] else -1
        r_x_odds    = 100*x_odds/total_odds if data[index]['xOdds']    else -1
        r_away_odds = 100*a_odds/total_odds if data[index]['awayOdds'] else -1

        data[index].update({
            'timeSeconds':data[index]['timeSeconds'].zfill(2),
            'homeOdds':"{:.1f}%".format(r_home_odds) if r_home_odds > 0 else '-',
            'xOdds':"{:.1f}%".format(r_x_odds) if r_x_odds > 0 else '-',
            'awayOdds':"{:.1f}%".format(r_away_odds) if r_away_odds > 0 else '-',
        })


    print('AWS matches:', len(data))
    context = {'matches':data}

    #return HttpResponse(data)
    return render(request, 'matches/list.html', context)