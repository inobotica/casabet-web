import requests, json, time, copy

from django.shortcuts import render
from django.http      import HttpResponse
from .lib.constants import BETHOUSES

URL = "https://1xuovgghf1.execute-api.us-east-1.amazonaws.com/production/GetOdds"
FREQUENCY = 30

matches_buffer = {
    'time':int(time.time()),
    'data':None
}

# Create your views here.
def index(request):  
    global matches_buffer
    print('GET params:', request.GET)
    q_string = ''

    if 'debug' in request.GET and request.GET['debug']=='true':
        print('Debugging', URL)
        q_string = '?debug=true'


    time_delta = True if int(time.time())-matches_buffer['time'] > FREQUENCY else False

    if time_delta or not matches_buffer['data']:
        print('Getting matches info from server...')

        r = requests.get(url = f'{URL}{q_string}')
        #get_location_of_user(request)

        try:
            data = r.json()

            if not len(data) or len(data)==1:
                print('Empty response from server')
                data = []
            else:
                matches_buffer.update({
                    'time':int(time.time()),
                    'data':r.json()
                })

            print('AWS matches:', len(data))
            
        except json.decoder.JSONDecodeError as e:
            print('Empty response from server')
            data = []
    else:
        print('Using buffer information... time to expire {}'.format(FREQUENCY-(int(time.time())-matches_buffer['time'])))
        data = copy.deepcopy(matches_buffer['data'])
        print('AWS matches:', len(data))

    # update values
    for index, row in enumerate(data):

        #print(data[index])

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

    context = {'matches':data}

    return render(request, 'matches/list.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print('IP:', ip)

    return ip

def get_location_of_user(request):
    ip  = get_client_ip(request)
    URL = f"http://ip-api.com/json/{ip}"
    r   = requests.get(url = URL)#, params = PARAMS)
    keys= ['country','countryCode','region','regionName','city','zip','lat','lon']

    if r.status_code == 200:
        try:
            data = r.json()              
            user_location_info = {your_key: data[your_key] for your_key in keys}        
            print('User location', user_location_info)  
        except json.decoder.JSONDecodeError as e:
            print('Empty response from server')
            data = []
