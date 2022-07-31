import xmltodict
import requests

def deActueleVertrektijdenVanNS(locatie): #standard location is utrecht
    #print('using location', locatie)
    inlogGegevens = 'moussa.elbouzidi@student.hu.nl', 'h8as35ZhtSOXgSMtFeSzynJ91PZ1fxK49JcjuaAHLtpUIKzcGefQww'
    urlVanDeAPI = 'http://webservices.ns.nl/ns-api-avt?station=' + locatie

    response = requests.get(urlVanDeAPI, auth=inlogGegevens)

    bestandXML = xmltodict.parse(response.text)

    lijstVanDeVertrektijden = []

    try: #ervoor zorgen dat we geen exception error krijgen in de console door eerst te proberen
        for tijdVanVertrek in bestandXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            eindBestemming = tijdVanVertrek['EindBestemming']
            vertrekTijd = tijdVanVertrek['VertrekTijd']
            vertrekTijd = vertrekTijd[11:16]
            if 'VertrekVertragingTekst' in tijdVanVertrek.keys():
                vertragingstijd = tijdVanVertrek['VertrekVertragingTekst'][0:2]
            else:
                vertragingstijd = ''

            spoornummer = tijdVanVertrek['VertrekSpoor']
            lijstVanDeVertrektijden.append('{:<7} {:<2} {:<30} {:<5}'.format(vertrekTijd, vertragingstijd, eindBestemming, spoornummer['#text']))
    except KeyError:
        print('Unknown location filled (XML).')

    return lijstVanDeVertrektijden