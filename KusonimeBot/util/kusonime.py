import re, os
import chevron
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs4
from telegraph import Telegraph

telegraph = Telegraph(os.environ.get('PH_TOKEN', None))
if telegraph.get_access_token() == None:
    token_ph = telegraph.create_account(short_name = "KusonimeBot")
    print("Membuat akun telegraph baru dengan token :", token_ph.get('access_token'))

headers = {
    'Accept' : "*/*",
    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

async def kusonimeSearch(query : str):
    hasil = dict()
    request = ClientSession(headers = headers)
    api = "https://kusonime.com/"
    params = dict(post_type = "post", s = query)
    try:
        test = await request.get(api, params = params)
        text = await test.text()
        soup = bs4(text, 'html.parser')
        results = []
        for detpost in soup.find_all('div', { 'class' : 'detpost' }):
            thumb = detpost.find('div', { 'class' : 'thumbz' }).find('img').get('src')
            found = detpost.find('h2', { 'class' : 'episodeye' })
            url = found.find('a').get('href')
            title = found.text
            if url.endswith('/'):
                i = url.split('/')
                i.pop()
                url = '/'.join(i)
            slug = url.split('/').pop()
            results.append(dict(title = title, thumb = thumb, url = url, slug = slug))
        hasil.update(error = False, results = results)
    except:
        hasil.update(error = True, error_message = "Telah terjadi error tidak diketahui")
    finally:
        await request.close()
        return hasil

async def kusonimeBypass(url : str, slug = None):
    hasil = dict()
    ini_url = url
    request = ClientSession(headers = headers)
    if slug:
        noslug_url = "https://kusonime.com/{slug}"
        ini_url = noslug_url.format({ 'slug' : slug })
    try:
        test = await request.get(ini_url)
        test_text = await test.text()
        soup = bs4(test_text, 'html.parser')
        thumb = soup.find('div', { 'class' : 'post-thumb' }).find('img').get('src')
        data = []
        title = soup.select('#venkonten > div.vezone > div.venser > div.venutama > div.lexot > p:nth-child(3) > strong')[0].text.strip()
        num = 1
        genre = []
        for cari_genre in soup.select('#venkonten > div.vezone > div.venser > div.venutama > div.lexot > div.info > p:nth-child(2)'):
            gen = cari_genre.text.split(':').pop().strip().split(', ')
            genre = gen
        status_anime = soup.select('#venkonten > div.vezone > div.venser > div.venutama > div.lexot > div.info > p:nth-child(6)')[0].text.split(':').pop().strip()
        for smokedl in soup.find('div', { 'class' : 'dlbod' }).find_all('div', { 'class' : 'smokeddl' }):
            titl = soup.select(f'#venkonten > div.vezone > div.venser > div.venutama > div.lexot > div.dlbod > div:nth-child({num}) > div.smokettl')[0].text
            titl = re.sub(f'Download', '', titl).strip()
            mendata = dict(name = titl, links = [])
            for smokeurl in smokedl.find_all('div', {  'class' : 'smokeurl' }):
                quality = smokeurl.find('strong').text
                links = []
                for link in smokeurl.find_all('a'):
                    url = link.get('href')
                    client = link.text
                    links.append({ 'client' : client, 'url' : url })
                mendata['links'].append(dict(quality = quality, link_download = links))
            data.append(mendata)
            num += 1
        hasil.update(error = False, title = title, thumb = thumb, genre = genre, genre_string = ", ".join(genre), status_anime = status_anime, data = data)
    except:
        hasil.update(error = True, error_message = "Telah terjadi error tidak diketahui")
    finally:
        await request.close()
        return hasil

async def byPassPh(url : str, msg_id = "123"):
    kusonime = await kusonimeBypass(url)
    results = dict(error = True, error_message = "Telah terjadi error tidak diketahui")
    template = """
<img src={{{thumb}}}>

<p><b>Title</b> : {{title}}</p>
<p><b>Genre</b> : {{genre_string}}</p>
<p><b>Status</b> : {{status_anime}}</p>
<br>
{{#data}}
    <h4>{{name}}</h4>
    {{#links}}
    <p><b>Resolusi : {{quality}}</b></p>
    {{#link_download}}
    <p>➸ <a href="{{url}}">{{client}}</a></p>
    {{/link_download}}
    {{/links}}
    <br>
{{/data}}
""".strip()
    if not kusonime['error']:
        html = chevron.render(template, kusonime)
        page = telegraph.create_page(
            f"{kusonime.get('title')}-{msg_id}",
            html_content = html
        )
        results.update(error = False, url = 'https://telegra.ph/{}'.format(page['path']))
        del results['error_message']
    return results


class Kusonime():
    def __init__(self):
        pass
    async def search(self, query : str):
        return await kusonimeSearch(query)
    async def byPass(self, url):
        return await kusonimeBypass(url)
    async def telegraph(self, url, msg_id):
        return await byPassPh(url, msg_id)
