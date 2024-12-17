from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json, logging
from .models import News, iframeVideo, adsitem
from django.core.cache import cache
from django.http import JsonResponse
import requests

def index(request):
    context = market_data(request)
    return render(request, "calculator/index.html", context)






def get_crypto_price(request, currency):

    price = cache.get(currency)
    
    if price is not None:

        return JsonResponse({"price": price, "cache_status": "fresh"})
    

    api_url = f'https://api.coinbase.com/v2/exchange-rates?currency={currency}'
    response = requests.get(api_url)
    
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch data from API"}, status=500)

    json_response = response.json()
    
    try:
        price = float(json_response["data"]["rates"]["USD"])
    except KeyError:
        return JsonResponse({"error": "Invalid response from API"}, status=500)


    cache.set(currency, price, timeout=100)


    return JsonResponse({"price": price, "cache_status": "expired"})





logger = logging.getLogger(__name__)

API_URL = 'https://api.coinbase.com/v2/exchange-rates?currency='

@csrf_exempt
def convert_currency(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            from_currency = data.get('from_currency').upper()
            from_amount = data.get('from_amount')
            to_currency = data.get('to_currency').upper()


            if not from_currency or not to_currency or not from_amount:
                logger.error("Invalid input: Missing required fields")
                return JsonResponse({'error': 'Invalid input: Missing required fields'}, status=400)

            if not isinstance(from_amount, (int, float)) or from_amount <= 0:
                logger.error(f"Invalid amount: {from_amount}")
                return JsonResponse({'error': 'Invalid input: Amount should be a positive number'}, status=400)


            response = requests.get(f'{API_URL}{from_currency}')
            

            if response.status_code != 200:
                logger.error(f"Error fetching exchange rate: {response.status_code}")
                return JsonResponse({'error': 'Failed to fetch exchange rate from external API'}, status=500)
            
            rates = response.json().get('data', {}).get('rates', {})
            conversion_rate = rates.get(to_currency)

            if conversion_rate is None:
                    logger.error(f"Conversion rate not available for {to_currency}")
                    return JsonResponse({'error': f'Conversion rate not available for {to_currency}'}, status=400)


            conversion_rate = float(conversion_rate)

            if conversion_rate:
                converted_amount = from_amount * conversion_rate
                return JsonResponse({
                    'from_currency': from_currency,
                    'from_amount': from_amount,
                    'to_currency': to_currency,
                    'converted_amount': round(converted_amount, 4)
                })
            else:
                logger.error(f"Currency conversion rate not available for {to_currency}")
                return JsonResponse({'error': 'Currency conversion rate not available for the target currency'}, status=400)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return JsonResponse({'error': 'Failed to communicate with external API'}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def market_data(request):

    compare_url = 'https://min-api.cryptocompare.com/data/top/mktcapfull'
    coingecko_url = 'https://api.coingecko.com/api/v3/global'

    params = {'limit': 2, 'tsym': 'USD'}
    response = requests.get(compare_url, params=params)

    if response.status_code == 200:
        data = response.json()


        bitcoin_market_cap = data['Data'][0]['DISPLAY']['USD']['MKTCAP']
        bitcoin_24h_volume = data['Data'][0]['DISPLAY']['USD']['VOLUME24HOURTO']
        
        ethereum_market_cap = data['Data'][1]['DISPLAY']['USD']['MKTCAP']
        ethereum_24h_volume = data['Data'][1]['DISPLAY']['USD']['VOLUME24HOURTO']


        response = requests.get(coingecko_url)
        data = response.json()
        
        if response.status_code == 200:
                market_cap = data['data']['total_market_cap']['usd']
                btc_dom = data['data']['market_cap_percentage']['btc']
                eth_dom = data['data']['market_cap_percentage']['eth']

                context = {
                    "bitcoin_market_cap": bitcoin_market_cap,
                    "bitcoin_24h_volume": bitcoin_24h_volume,
                    "ethereum_market_cap": ethereum_market_cap,
                    "ethereum_24h_volume": ethereum_24h_volume,
                    "market_cap": market_cap,
                    "btc_dom": btc_dom,
                    "eth_dom": eth_dom,
                }

                return context
        else:
            return JsonResponse({"error": "Unable to fetch data from API"}, status=500)

    
    else:
        return JsonResponse({"error": "Unable to fetch data from API"}, status=500)








def news(request):

    news = News.objects.all().order_by('-date')
    videos = iframeVideo.objects.all()
    ads = adsitem.objects.all()
    return render(request, "calculator/news.html", {'news': news, 'videos':videos, 'ads':ads})


def services(request):
    return render(request, "calculator/services.html")

def about(request):
    return render(request, "calculator/about.html")



    





