from bs4 import BeautifulSoup

# 原始HTML原始碼
html_doc = '''
<html>
<head>
<title>這是HTML文件標題</title>
</head>
<body>
<h1 id="article" class="banner">網頁標題１</h1>
<p data-author='aaron' class="reqular text-normal">文章段落１</p>
<a class="link no btn" href="https://www.aaronlife.com/ref1">參考<b>資料</b>連結１</a>
<a class="link btn" href="https://www.aaronlife.com/ref2">參考<b>資料</b>連結２</a>
<a class="link btn" href="https://www.aaronlife.com/ref2">參考資料連結３</a>
<a class="link btn" href="https://www.aaronlife.com/ref2">參考資料連結４</a>
<p>這是一份<b class="boldtext">HTML文件</b>。</p>
<h2 id="article1" class="banner">網頁標題２</h2>
<p data-author='andy' class="reqular text-normal">文章段落２</p>
<h2 id="article2" class="title normal">網頁標題３</h2>
<p data-author='william' class="reqular text-normal">文章段落３</p>
</body>
</html>
'''

# 建立BeautifulSoup物件解析HTML文件
soup = BeautifulSoup(html_doc, 'html.parser')

# 透過標籤來定位元素
result = soup.select('a')
print('select a:', result)

result = soup.select('body p b')
print('select p b:', result)

# 透過id來定位元素
result = soup.select('#article')
print('select #article:', result)

# 多重選擇（只要一個符合即可）
result = soup.select('#article, p, b')
print('select #article, p, b:', result)

# 全部class都要符合才會被定位到
result = soup.select('.no.link.btn')
print('select .no.link.btn:', result)

# 透過class來定位元素
result = soup.select('.banner')
print('select .banner:', result)

# 透過是否存在某個屬性來定位元素
result = soup.select('a[href]')
print('select a[href]:', result)

# 透過指定的屬性值來定位元素
result = soup.select('a[href="http://wwww.aaronlife.com"]')
print('select a[href=http://wwww.aaronlife.com]:', result)

# 透過指定的屬性值「開頭字串」來定位元素
result = soup.select('a[href^="http"]')
print('select a[href^=http]:', result)

# 透過指定的屬性值「結束字串」來定位元素
result = soup.select('a[href$="com"]')
print('select a[href$=com]:', result)

# 透過指定的屬性值「有包含的字串」來定位元素
result = soup.select('a[href*="com"]')
print('select a[href*=com]:', result)