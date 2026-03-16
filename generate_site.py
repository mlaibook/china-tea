from pathlib import Path
root = Path('.')
BASE = 'https://mlaibook.github.io/china-tea'

def page(title, desc, lang, prefix, brand, navs, switch, switch_label, body, image='/china-tea/assets/img/hero-tea.svg'):
    canonical = f'{BASE}/{prefix}index.html'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="robots" content="index,follow" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="{BASE}{image.replace('/china-tea','')}" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="stylesheet" href="/china-tea/assets/css/style.css" />
</head>
<body>
  <header class="site-header wrap">
    <div class="nav">
      <a class="brand" href="/china-tea/{prefix}index.html">{brand}</a>
      <nav>
        <a href="/china-tea/{prefix}tea/index.html">{navs[0]}</a>
        <a href="/china-tea/{prefix}teaware/index.html">{navs[1]}</a>
        <a href="/china-tea/{prefix}history/index.html">{navs[2]}</a>
        <a href="/china-tea/{prefix}drinks/index.html">{navs[3]}</a>
        <a href="/china-tea/{prefix}about.html">About</a>
        <a class="lang" href="{switch}">{switch_label}</a>
      </nav>
    </div>
  </header>
  {body}
  <footer class="site-footer wrap">
    <a href="/china-tea/{prefix}about.html">About</a>
    <a href="/china-tea/{prefix}privacy.html">Privacy</a>
    <a href="/china-tea/{prefix}contact.html">Contact</a>
    <a href="/china-tea/{prefix}terms.html">Terms</a>
  </footer>
</body>
</html>'''

def write(rel, content):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

nav_en = ('Tea','Teaware','History','Fresh Tea Drinks')
nav_zh = ('茶叶','茶具','茶文化历史','现制茶饮')

landing_hero = '<div class="hero-media"><img src="/china-tea/assets/img/hero-tea.svg" alt="Stylized illustration of Chinese tea leaves and a tea cup" /></div>'
write('index.html', f'''<!doctype html><html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>China Tea Journal — Chinese Tea Culture for Global Readers</title><meta name="description" content="A bilingual editorial-style website introducing Chinese tea leaves, teaware, history, and modern tea drinks to global readers." /><meta http-equiv="refresh" content="0; url=/china-tea/en/index.html" /><link rel="stylesheet" href="/china-tea/assets/css/style.css" /></head><body><main class="wrap"><section class="hero"><div class="hero-copy"><p class="eyebrow">Bilingual • Editorial • Cultural</p><h1>Discover Chinese Tea Beyond the Stereotypes</h1><p class="lede">This landing page redirects to the English home page.</p><div class="cta-row"><a class="btn" href="/china-tea/en/index.html">Read in English</a><a class="btn ghost" href="/china-tea/zh/index.html">阅读中文版</a></div></div>{landing_hero}</section></main></body></html>''')

write('en/index.html', page('China Tea Journal — English Edition', 'English edition of a bilingual site about Chinese tea culture.', 'en', 'en/', 'China Tea Journal', nav_en, '/china-tea/zh/index.html', '中文', f'''
<main class="wrap">
  <section class="hero">
    <div class="hero-copy"><p class="eyebrow">English Edition</p><h1>A magazine-style guide to Chinese tea culture</h1><p class="lede">Written from Chinese-source context and adapted for international readers, this site explores tea as ingredient, ritual, object, and modern lifestyle. Instead of treating tea as a shopping category, we treat it as a living system of taste, place, labor, etiquette, and memory.</p><div class="toc"><span class="pill">Tea leaves</span><span class="pill">Teaware</span><span class="pill">History</span><span class="pill">Fresh tea drinks</span></div></div>
    {landing_hero}
  </section>
  <section class="feature-card"><h2>Editorial approach</h2><p>Chinese pages on this site are drafted first, drawing on Chinese tea discourse, common knowledge from tea practitioners, and public-domain historical framing. English pages are then adapted for readers who may be new to Chinese categories and assumptions. This allows the site to remain culturally grounded while still accessible to global readers.</p><p>We focus on four editorial lanes: leaf categories and terroir, vessels and brewing logic, cultural history and everyday ritual, and the rise of contemporary tea drinks. Together they show that Chinese tea is not merely ancient heritage. It is also present-day domestic life, retail culture, sensory training, and social hospitality.</p></section>
  <section class="post-grid">
    <a class="post" href="/china-tea/en/tea/index.html"><span class="tag">Tea</span><h3>How China classifies tea</h3><p>Understand green, white, yellow, oolong, black, and dark tea by processing, not color alone. Learn why oxidation, kill-green, rolling, and roasting matter so much.</p></a>
    <a class="post" href="/china-tea/en/teaware/index.html"><span class="tag">Teaware</span><h3>The logic of a gaiwan</h3><p>Why one lidded bowl can become the most flexible vessel in Chinese tea practice, and why neutrality matters more than ornament.</p></a>
    <a class="post" href="/china-tea/en/history/index.html"><span class="tag">History</span><h3>Tea from medicine to daily life</h3><p>A compact timeline from early medicinal use to literati culture, tea routes, and modern domestic habits across regions and generations.</p></a>
    <a class="post" href="/china-tea/en/drinks/index.html"><span class="tag">Drinks</span><h3>Fresh tea drinks are not “fake tea”</h3><p>Why contemporary tea shops still sit on a long Chinese tradition of blending, scenting, fruit pairing, and serving tea socially.</p></a>
    <a class="post" href="/china-tea/en/history/cha-dao.html"><span class="tag">Essay</span><h3>What foreigners often miss about tea culture</h3><p>Tea in China is less about ceremony alone than about rhythm, hospitality, seasonality, and place.</p></a>
    <a class="post" href="/china-tea/en/tea/longjing.html"><span class="tag">Leaf</span><h3>Longjing as a style of clarity</h3><p>A deeper look at the iconic green tea that shaped how many people imagine Chinese tea, from spring picking to texture and aroma restraint.</p></a>
  </section>
</main>
'''))

write('zh/index.html', page('中国茶志 — 中文版', '介绍中国茶叶、茶具、茶文化历史与现制茶饮的双语站点中文首页。', 'zh-CN', 'zh/', '中国茶志', nav_zh, '/china-tea/en/index.html', 'English', f'''
<main class="wrap">
  <section class="hero">
    <div class="hero-copy"><p class="eyebrow">中文版</p><h1>面向全球读者的中国茶文化杂志网站</h1><p class="lede">从中文语境出发，重新整理中国茶的知识、器物、历史与当代饮用方式，再用英文讲给国际读者听。这里不把茶理解成单纯商品，也不把茶文化缩减成几种“东方仪式”，而是把它放回真实生活、产区经验、器物逻辑与代际记忆里。</p><div class="toc"><span class="pill">茶叶</span><span class="pill">茶具</span><span class="pill">茶文化历史</span><span class="pill">现制茶饮</span></div></div>
    {landing_hero}
  </section>
  <section class="feature-card"><h2>内容方法</h2><p>本站中文内容优先写作，再面向国际读者改写为英文版本。这样做的目的，是避免直接从英文市场既有的扁平化叙述出发，而尽量保留中国茶自身的分类方法、审美习惯与生活语境。</p><p>我们目前围绕四条主线展开：茶叶工艺与产区、茶具与冲泡逻辑、茶文化历史与日常礼俗、现制茶饮与城市消费。它们合在一起，才能让外国读者看到一个既传统又当代的中国茶世界。</p></section>
  <section class="post-grid">
    <a class="post" href="/china-tea/zh/tea/index.html"><span class="tag">茶叶</span><h3>中国茶是怎么分类的</h3><p>理解绿茶、白茶、黄茶、乌龙、红茶、黑茶，关键在工艺，而不是英文颜色直译。杀青、发酵、焙火、揉捻都会改变最终风格。</p></a>
    <a class="post" href="/china-tea/zh/teaware/index.html"><span class="tag">茶具</span><h3>为什么盖碗这么重要</h3><p>一个盖碗，几乎就能完成中国茶大多数冲泡场景，而且最适合教学、比较和感受茶本身。</p></a>
    <a class="post" href="/china-tea/zh/history/index.html"><span class="tag">历史</span><h3>茶如何从药用走向日常</h3><p>从先秦、唐宋到明清，中国饮茶方式一直在变，但茶作为社交媒介和生活节律却很稳定。</p></a>
    <a class="post" href="/china-tea/zh/drinks/index.html"><span class="tag">现制茶饮</span><h3>新式茶饮并不是“背离传统”</h3><p>当代茶饮店，其实延续了中国茶长期以来的调饮、拼配、窨香与社交属性。</p></a>
    <a class="post" href="/china-tea/zh/history/cha-dao.html"><span class="tag">文章</span><h3>外国读者最容易误解的中国茶文化</h3><p>中国茶不只是“仪式感”，更是时间感、待客方式与地域生活。</p></a>
    <a class="post" href="/china-tea/zh/tea/longjing.html"><span class="tag">名茶</span><h3>龙井为什么如此典型</h3><p>它几乎定义了很多人对“中国绿茶”的第一印象，也体现了中国茶“轻、清、细、鲜”的审美线索。</p></a>
  </section>
</main>
'''))

sections = {
'en/tea/index.html': ('Tea Leaves','Processing shapes flavor, aroma, and texture. Chinese tea categories are best understood through making methods, season, and place. Once readers grasp that green, white, oolong, black, and dark tea are process categories rather than just colors, the whole landscape becomes easier to understand.','/china-tea/assets/img/section-tea.svg', [('Longjing, the grammar of green tea','/china-tea/en/tea/longjing.html'),('Wuyi rock tea and mineral rhythm','#'),('Dark tea and the logic of aging','#')]),
'en/teaware/index.html': ('Teaware','Chinese teaware is not decoration alone. Shape, heat retention, pour control, and social use all matter. A vessel is part of the brewing method, not only a cultural symbol.','/china-tea/assets/img/section-teaware.svg', [('Why a gaiwan is so versatile','/china-tea/en/teaware/gaiwan.html'),('What Yixing clay changes','#'),('The fairness pitcher explained','#')]),
'en/history/index.html': ('Tea Culture & History','Tea in China moved through medicine, tribute, literati aesthetics, commerce, and daily household life. Historical change did not remove tea from ordinary life; it multiplied the ways tea could mean something.','/china-tea/assets/img/section-history.svg', [('From Tang tea cakes to loose-leaf brewing','/china-tea/en/history/cha-dao.html'),('Tea roads and circulation','#'),('Tea and hospitality at home','#')]),
'en/drinks/index.html': ('Fresh Tea Drinks','Contemporary tea drinks inherit older Chinese habits of scenting, blending, fruit pairing, and seasonal refreshment. The modern tea shop is not outside tea culture; it is one of its current urban stages.','/china-tea/assets/img/section-drinks.svg', [('Why fruit tea belongs in the larger story','/china-tea/en/drinks/new-tea.html'),('Milk tea, texture, and youth culture','#'),('Tea chains and urban social life','#')]),
'zh/tea/index.html': ('茶叶','理解中国茶，最重要的是从工艺、山场、季节与入口感受出发，而不是简单用颜色去对应英文分类。不同工艺决定了茶的香气结构、滋味层次、耐泡度与冲泡策略。','/china-tea/assets/img/section-tea.svg', [('龙井：理解中国绿茶的一把钥匙','/china-tea/zh/tea/longjing.html'),('岩茶的“岩韵”如何理解','#'),('黑茶与陈化逻辑','#')]),
'zh/teaware/index.html': ('茶具','中国茶具不是单纯的器物陈列，而是冲泡逻辑、控温方式与待客礼仪的一部分。理解茶具，等于理解中国茶怎么被做得更好喝。','/china-tea/assets/img/section-teaware.svg', [('为什么盖碗几乎万能','/china-tea/zh/teaware/gaiwan.html'),('紫砂壶改变了什么','#'),('公道杯的功能是什么','#')]),
'zh/history/index.html': ('茶文化历史','中国茶从药用、贡茶、文人审美到家庭日常，不断变化又彼此叠加。真正重要的不是某个朝代的固定形式，而是茶如何持续进入人的生活。','/china-tea/assets/img/section-history.svg', [('从唐代团茶到明清散茶','/china-tea/zh/history/cha-dao.html'),('茶马古道与流通','#'),('中国人的待客饮茶','#')]),
'zh/drinks/index.html': ('现制茶饮','新式茶饮不是传统的反面，而是中国茶在城市消费环境中的当代表达。它延续了中国人对于拼配、调味、社交与便捷取饮的长期偏好。','/china-tea/assets/img/section-drinks.svg', [('为什么果茶也属于中国茶的大故事','/china-tea/zh/drinks/new-tea.html'),('奶茶与口感设计','#'),('茶饮店与城市社交','#')]),
}
for rel, (title, desc, img, links) in sections.items():
    is_zh = rel.startswith('zh/')
    prefix = 'zh/' if is_zh else 'en/'
    navs = nav_zh if is_zh else nav_en
    lang = 'zh-CN' if is_zh else 'en'
    brand = '中国茶志' if is_zh else 'China Tea Journal'
    switch = '/china-tea/en/' + rel[3:] if is_zh else '/china-tea/zh/' + rel[3:]
    switch_label = 'English' if is_zh else '中文'
    cards = ''.join([f'<a class="post" href="{href}"><span class="tag">{"文章" if is_zh else "Article"}</span><h3>{text}</h3><p>{desc}</p></a>' for text, href in links])
    body = f'<main class="wrap"><section class="subhero"><p class="eyebrow">{"栏目" if is_zh else "Section"}</p><h1>{title}</h1><p class="lede">{desc}</p></section><div class="section-banner"><img src="{img}" alt="{title}" /></div><section class="feature-card"><p>{desc}</p><p>{"如果只把中国茶理解成几种著名单品，就会错过它真正复杂的层次：产区、手法、器物、喝茶时机与身体感受。" if is_zh else "If Chinese tea is reduced to a few famous names, readers miss the system behind it: terroir, craftsmanship, vessel choice, timing, and bodily sensation."}</p></section><section class="post-grid">{cards}</section></main>'
    write(rel, page(f'{title} — {brand}', desc, lang, prefix, brand, navs, switch, switch_label, body, image=img))

articles = {
'zh/tea/longjing.html': ('龙井：为什么它几乎定义了中国绿茶','2026-03-16','/china-tea/assets/img/section-tea.svg','龙井之所以重要，不只是因为知名度高，而是因为它把很多中国绿茶的核心审美集中在一起：清、鲜、甘、滑，以及一种克制的豆香与板栗香。真正理解龙井，不能只停留在“扁平的叶子”和“西湖产区”这些标签上，还要理解中国茶评价体系中对鲜爽度、杀青火候、采摘等级与山场气息的敏感。\n\n在中文互联网关于龙井的高质量讨论里，最常见的共识是：好龙井不是香得夸张，而是闻起来清净，入口很快，汤感细，回甘来得轻却持续。对外国读者来说，最容易误会的是把龙井理解成某种固定风味的商品。事实上，它更像是一种风格，一种关于春天、嫩度和清透表达的风格。\n\n如果要把龙井介绍给第一次接触中国茶的人，我更愿意强调三个点：第一，它不是越烫越好喝，过高水温会让鲜感受损；第二，它适合用玻璃杯或盖碗观察叶形与汤色；第三，龙井代表的是一种审美方向——把复杂感藏在轻与薄的表面之下。\n\n再往深一点说，龙井之所以经常被当作“中国绿茶”的代表，也因为它在公众认知和专业评价之间保持了一种罕见的平衡：它既足够好懂，又足够耐讨论。初学者可以感受到“鲜”和“香”，有经验的饮茶者则会继续比较不同产区的骨架感、香气打开方式、喉部回甘和叶底活性。也正因此，龙井很适合成为一把入门钥匙。'),
'en/tea/longjing.html': ('Longjing: Why it almost defines Chinese green tea','2026-03-16','/china-tea/assets/img/section-tea.svg','Longjing matters not only because it is famous, but because it concentrates many of the central aesthetic values of Chinese green tea: clarity, freshness, sweetness, smooth texture, and a restrained nutty aroma. To understand it well, one must go beyond labels such as flat leaf shape or West Lake origin and pay attention to tenderness, pan-firing control, seasonal picking, and site expression.\n\nA recurring insight in Chinese-language discussions is that excellent Longjing is not aggressively fragrant. Instead, it smells clean, drinks quickly, feels fine-textured on the palate, and leaves a gentle but persistent returning sweetness. Foreign readers often mistake it for a fixed commercial flavor. In reality, Longjing is better understood as a style of spring expression.\n\nWhen introducing Longjing to beginners, I would stress three things: do not use excessively hot water, consider brewing it in glass or gaiwan so the leaves can be seen, and remember that its elegance comes from understatement rather than force.\n\nAt a deeper level, Longjing often functions as a bridge between public recognition and serious tasting. New drinkers can immediately notice freshness and aroma, while experienced tea drinkers continue to compare body structure, site variation, aftertaste, and leaf vitality. That balance of accessibility and depth is one reason Longjing remains such a powerful entry point into Chinese tea.'),
'zh/teaware/gaiwan.html': ('为什么盖碗几乎可以应对所有中国茶','2026-03-16','/china-tea/assets/img/section-teaware.svg','盖碗的价值，不只是“传统感”，而在于它几乎是最中性的冲泡工具。瓷材稳定、出汤快、闻香方便、好清洗，也不会像某些壶那样过度改变茶汤风格。对于要向外国读者介绍中国茶的人来说，盖碗比紫砂壶更适合作为起点，因为它更透明，也更容易比较不同茶叶之间的差异。\n\n中文世界里很多资深饮茶者都会强调：盖碗看似简单，真正难的是手法。注水、合盖、出汤、控温、留根，这些动作共同决定了它能不能把茶泡得干净利落。正因为盖碗几乎不替你“修饰”茶，所以它特别适合学习。\n\n从教学角度看，盖碗还有一个重要优势：反馈非常直接。茶苦了、闷了、散了、香气打不开，往往都能快速从手法和参数上找到原因。它几乎像一个实验容器，让饮茶者把“为什么这泡好喝”这件事看得更清楚。'),
'en/teaware/gaiwan.html': ('Why a gaiwan can handle almost every Chinese tea','2026-03-16','/china-tea/assets/img/section-teaware.svg','The value of a gaiwan lies not merely in tradition, but in neutrality. Porcelain is stable, pours quickly, reveals aroma clearly, cleans easily, and does not shape the liquor as strongly as some clay teapots do. For international readers trying to understand Chinese tea, the gaiwan is often a better starting point than Yixing clay because it is more transparent and better for comparison.\n\nExperienced Chinese tea drinkers often note that the gaiwan looks simple but depends on technique: water entry, lid angle, pour speed, heat control, and whether one leaves a little liquor behind. Precisely because it does not hide flaws, it becomes one of the best teaching tools in Chinese tea practice.\n\nThe gaiwan also offers unusually direct feedback. If the tea turns harsh, flat, over-steeped, or aromatically closed, the brewer can often trace the result back to a visible choice in timing or handling. In that sense, a gaiwan is almost an experimental vessel: it helps people understand not just whether a tea tastes good, but why.'),
'zh/history/cha-dao.html': ('中国茶文化不只是仪式，而是一种生活秩序','2026-03-16','/china-tea/assets/img/section-history.svg','很多国外语境会把中国茶文化想象成一种高度仪式化、接近表演的东方美学。但在更真实的中文经验里，茶首先是一种生活秩序：早上醒来烧水，饭后坐一会儿，来客时先斟一杯，工作间隙换泡续上。所谓“茶道”在中国并不总以严格形式出现，它更多隐藏在动作节奏和人与人的关系里。\n\n从唐宋到明清，饮茶方法确实发生了巨大变化，但不变的是，茶始终承担着社交润滑、节律调节和自我安顿的作用。向外国读者讲中国茶时，如果只讲器物和礼法，很容易漏掉最重要的那一层：茶是用来过日子的。\n\n也正因为如此，很多中国人对茶的记忆并不首先来自博物馆或仪式表演，而是来自家庭：父母厨房里的保温壶、办公室桌角的一只玻璃杯、节日里给长辈续上的那一泡茶。茶的文化分量，正是这样在平常里被反复加深的。'),
'en/history/cha-dao.html': ('Chinese tea culture is not ceremony alone, but a lived order','2026-03-16','/china-tea/assets/img/section-history.svg','In many foreign contexts, Chinese tea culture is imagined as highly ceremonial, almost performative. Yet in ordinary Chinese experience, tea is first a way of structuring life: boiling water in the morning, sitting down after a meal, pouring a cup for guests, refreshing the leaves during work. What people sometimes call “tea culture” often exists not as rigid form, but as rhythm and relation.\n\nTea practices changed dramatically from the Tang and Song periods to the Ming and Qing eras, but tea consistently remained a medium for hospitality, pacing, and self-settling. If one explains Chinese tea only through vessels and etiquette, one misses the most important layer: tea is part of everyday living.\n\nFor this reason, many Chinese memories of tea begin not in museums or ceremonial halls, but at home: a thermos in the kitchen, a glass cup on an office desk, or the quiet act of refilling an elder’s tea during a holiday visit. Tea acquires cultural weight precisely because it is repeated in ordinary life.'),
'zh/drinks/new-tea.html': ('为什么新式茶饮也在中国茶文化的连续谱里','2026-03-16','/china-tea/assets/img/section-drinks.svg','很多人把新式茶饮和传统茶对立起来，这种看法有点过于简单。中国茶历史上本来就存在调饮、窨花、拼配、加果、冷热转换等丰富做法。当代茶饮店只是把这些能力放到了更城市化、更品牌化、更年轻消费的场景里。\n\n如果向外国读者解释这一点，重点不是把奶茶说成“古老传统”，而是说明中国人从来没有只接受一种喝茶方式。纯饮、清饮、调饮、分享、外带，都是茶进入生活的不同接口。\n\n新式茶饮的重要性还在于，它把年轻人重新带回到“茶”这个关键词里。即使他们一开始是因为水果、奶盖、口感层次而来，最终也会慢慢接触到乌龙、茉莉、普洱、单丛这些更具体的茶底概念。换句话说，现制茶饮不只是消费品，也可能是新的入口教育。'),
'en/drinks/new-tea.html': ('Why fresh tea drinks still belong to the larger Chinese tea story','2026-03-16','/china-tea/assets/img/section-drinks.svg','It is too simple to oppose contemporary tea drinks to tradition. Chinese tea history has long included scenting, blending, fruit pairing, sweetening, and different serving temperatures. Modern tea chains place these capacities into a more urban, branded, and youth-oriented context.\n\nFor international readers, the point is not to claim that milk tea in its current form is ancient. The point is that Chinese tea culture has never been confined to one legitimate mode of drinking. Pure leaf tea, blended tea, shared tea, takeaway tea—these are different interfaces through which tea enters daily life.\n\nFresh tea drinks also matter because they reintroduce younger consumers to tea vocabulary. People may enter through fruit flavor, cream tops, texture, or convenience, yet eventually they begin encountering more specific tea bases such as oolong, jasmine, pu-erh, or dancong. In that sense, the modern tea shop can function not only as retail but also as entry-level education.')
}

for rel, (title, date, img, text) in articles.items():
    is_zh = rel.startswith('zh/')
    prefix = 'zh/' if is_zh else 'en/'
    navs = nav_zh if is_zh else nav_en
    lang = 'zh-CN' if is_zh else 'en'
    brand = '中国茶志' if is_zh else 'China Tea Journal'
    switch = '/china-tea/en/' + rel[3:] if is_zh else '/china-tea/zh/' + rel[3:]
    switch_label = 'English' if is_zh else '中文'
    html_text = ''.join(f'<p>{p}</p>' for p in text.split('\n\n'))
    body = f'<main class="page"><article><p class="eyebrow">{"文章" if is_zh else "Essay"}</p><h1>{title}</h1><p class="meta">{date}</p><img class="inline-hero" src="{img}" alt="{title}" />{html_text}<p class="note">{"说明：本站中文内容为原创整理，英文页面为面向国际读者的改写与翻译。" if is_zh else "Note: Chinese pages on this site are originally written syntheses; English pages are adapted translations for international readers."}</p></article></main>'
    write(rel, page(f'{title} — {brand}', title, lang, prefix, brand, navs, switch, switch_label, body, image=img))

for lang, title_about, body_about in [
    ('en','About','China Tea Journal is a bilingual cultural website designed to introduce Chinese tea to global readers through original synthesis, editorial design, and accessible explanation. The project takes Chinese discourse seriously, then translates it outward.'),
    ('zh','About','中国茶志是一个双语文化网站，尝试用原创整理的方式，把中国茶讲给国际读者听。它不是英文资料的再翻译，而是从中文茶语境出发再向外表达。')]:
    prefix = f'{lang}/'
    navs = nav_zh if lang=='zh' else nav_en
    brand = '中国茶志' if lang=='zh' else 'China Tea Journal'
    switch = '/china-tea/en/about.html' if lang=='zh' else '/china-tea/zh/about.html'
    switch_label = 'English' if lang=='zh' else '中文'
    langcode = 'zh-CN' if lang=='zh' else 'en'
    pages_simple = {
        'about.html': ('About', body_about),
        'privacy.html': ('Privacy Policy', 'We collect minimal technical analytics if enabled by the repository owner. Contact us if you want any content corrected or removed. No advertising trackers are enabled by default in this repository version.'),
        'contact.html': ('Contact', 'For editorial feedback, collaboration, or correction requests, please contact the repository owner through the linked GitHub profile or a site email if later added.'),
        'terms.html': ('Terms', 'This website is for cultural and educational information. Do not reproduce the content commercially without permission from the repository owner. Trademark references remain property of their respective owners.')
    }
    for relname, (ptitle, pbody) in pages_simple.items():
        target_switch = switch if relname=='about.html' else switch.replace('about.html', relname)
        body = f'<main class="page"><article><h1>{ptitle}</h1><p>{pbody}</p></article></main>'
        write(f'{lang}/{relname}', page(f'{ptitle} — {brand}', ptitle, langcode, prefix, brand, navs, target_switch, switch_label, body))

urls = [
    '', 'en/index.html','zh/index.html','en/tea/index.html','en/tea/longjing.html','en/teaware/index.html','en/teaware/gaiwan.html','en/history/index.html','en/history/cha-dao.html','en/drinks/index.html','en/drinks/new-tea.html','en/about.html','en/privacy.html','en/contact.html','en/terms.html','zh/tea/index.html','zh/tea/longjing.html','zh/teaware/index.html','zh/teaware/gaiwan.html','zh/history/index.html','zh/history/cha-dao.html','zh/drinks/index.html','zh/drinks/new-tea.html','zh/about.html','zh/privacy.html','zh/contact.html','zh/terms.html'
]
xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    loc = f'{BASE}/' if u=='' else f'{BASE}/{u}'
    xml.append(f'  <url><loc>{loc}</loc></url>')
xml.append('</urlset>')
write('sitemap.xml', '\n'.join(xml))
write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: https://mlaibook.github.io/china-tea/sitemap.xml\n')
