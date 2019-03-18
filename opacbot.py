import telepot
import sys, time
import bs4 as bs
import urllib.request


bot = telepot.Bot('BOT_TOKEN')

whitelist = set("aàbcdeèéfghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 ' _ + - . ; : ,")
listurl = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789")
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    text = msg['text']
    search = text.replace(" ","+")

    titleList=[]
    authorList=[]
    resultsList=[]

    if (text == '/start'):
        bot.sendMessage(chat_id,'Welcome on unofficial bot of Bibliosar\n'
                                'Using this bot you can search a book inside the University of Cagliari\n'
                                'write the title of the book and send the message !')

    if (text != '/start'):

        try:
            url = urllib.request.urlopen('http://opac.regione.sardegna.it/SebinaOpac/query/' + search).read()
            soup = bs.BeautifulSoup(url, 'html.parser')

            for titles in soup.find_all('h3','titololistarisultati'):
                title = ''.join(filter(whitelist.__contains__, titles.text))
                titleList.append(title)

            for author in soup.find_all(class_=['autorelistarisultati']):
                writer = ''.join(filter(whitelist.__contains__, author.text))
                authors = writer.replace(' ','')
                authorList.append(authors)

            for code_iopac in soup.find_all('tr'):
                site = ''.join(filter(listurl.__contains__, titles.text))
                id = site.replace(' ', '-')
                idopac = code_iopac.attrs['data-idopac']
                link = 'http://opac.regione.sardegna.it/SebinaOpac/resource/' + id + '/' + idopac
                resultsList.append(link)
                    
            for i in range(len(titleList)):
                bot.sendMessage(chat_id, 'Book title: \n' + titleList[i] + '\n' +
                                '\nBook authors: \n' + authorList[i] + '\n' +
                                "<a href='"+resultsList[i]+"'>"'\nResource url'"</a>", parse_mode='html')

            

        except urllib.error.HTTPError as err:
            if err.code == 404:
                bot.sendMessage(chat_id, 'Element not fpund')

bot.message_loop({'chat': on_chat_message})
while 1:
    time.sleep(3)

