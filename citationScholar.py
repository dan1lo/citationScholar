from bs4 import BeautifulSoup
import requests
import xlwt
import itertools



numPages = 0
x=0
cont=0
contRow = 0
contColumn=0
contAux=0


id = raw_input('>> Put the paper ID') 
# example : https://scholar.google.com.br/scholar?oi=bibs&hl=pt-BR&cites=2627283193938513175&as_sdt=5
#after cites= 2627283193938513175 
#you can found put the paper's name and click at cited by


paperName = raw_input('>>>Put the name of XLS, for exemple, the name of paper')
myBook = xlwt.Workbook()  #open xls
sheet = myBook.add_sheet (' sheet ') # create a sheet
link = "https://scholar.google.com/scholar?start=0&hl=en&as_sdt=2005&sciodt=0,5&cites="+id+"&scipsc='"
r = requests.get(link)
soup = BeautifulSoup(r.text)

searchCountPapers = [ i.text for i in soup.findAll("div", { "id" : "gs_ab_md" })]
for t in searchCountPapers:
 	totalPapersCited = t.split( )
 	if totalPapersCited[1]=='result':
 		totalPapersCited[1] = 0
 	if totalPapersCited[1]=='results':
 		totalPapersCited[1] = 0
 	numPages = int(totalPapersCited[1]) /10 #if have 90 papers cited, we have 9 page at google (90/10=9) 
 	modulo = numPages %10
 	if modulo == 0:
 	 numPages +=1 # if have 92 papers cited, we have 10 page at google (90/10=9 + 1 page to 2 ) 
 	modulo = numPages %10
while x<=numPages:
	linkSplit = link.split('0&hl')

	r = requests.get(linkSplit[0]+ repr(x) +"0&hl"+linkSplit[1])
	soup = BeautifulSoup(r.text)
	x+=1
	title = [ i.text for i in soup.findAll("h3", { "class" : "gs_rt" })]
	author = [ i.text for i in soup.findAll("div", { "class" : "gs_a" })]
	for f in itertools.chain(*itertools.izip(title, author)): # to put title and author in one list
		if contAux%2 == 0:
   			contColumn = 0 # to put in column 0
   		else:
   			contColumn = 1
   			contRow+=1 #increment row
   		contAux+=1
   		sheet.write (contRow,contColumn,f) # put the information f (title[x] and author[x]) in row x and column y 
 

myBook.save (paperName+'.xls')# create xls 
