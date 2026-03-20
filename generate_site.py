"""DEPRECATED: legacy static-file generator.

This repository is now Jekyll collection-based.
Do NOT use this script to generate or rewrite zh/en article pages or index pages.
It predates collection-managed content and can conflict with collection sources.

Keep only as historical reference unless deliberately rewritten for the new architecture.
"""

raise SystemExit("generate_site.py is deprecated for the collection-based site. Do not run it.")

from pathlib import Path
import json
root = Path('.')
BASE = 'https://mlaibook.github.io/china-tea'
photo_meta = {x['local']: x for x in json.loads((root/'assets/img/photos/credits.json').read_text(encoding='utf-8'))}

def photo_figure(local, alt, caption):
    meta = photo_meta.get(local, {})
    cred = ''
    if meta:
        cred = f' <span class="credit">Photo: <a href="{meta.get("descriptionUrl","#")}">{meta.get("artist","Unknown")}</a> · {meta.get("license","")}</span>'
    return f'<figure class="photo"><img src="assets/img/photos/{local}" alt="{alt}" /><figcaption>{caption}{cred}</figcaption></figure>'

def page(title, desc, lang, prefix, brand, navs, switch, switch_label, body, image='/china-tea/assets/img/photos/longjing-plantation.jpg'):
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
  <meta property="og:type" content="article" />
  <meta property="og:image" content="{BASE}{image.replace('/china-tea','')}" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>
  <header class="site-header wrap">
    <div class="nav">
      <a class="brand" href="{prefix}index.html">{brand}</a>
      <nav>
        <a href="{prefix}tea/index.html">{navs[0]}</a>
        <a href="{prefix}teaware/index.html">{navs[1]}</a>
        <a href="{prefix}history/index.html">{navs[2]}</a>
        <a href="{prefix}drinks/index.html">{navs[3]}</a>
        <a href="{prefix}about.html">About</a>
        <a class="lang" href="{switch}">{switch_label}</a>
      </nav>
    </div>
  </header>
  {body}
  <footer class="site-footer wrap">
    <a href="{prefix}about.html">About</a>
    <a href="{prefix}privacy.html">Privacy</a>
    <a href="{prefix}contact.html">Contact</a>
    <a href="{prefix}terms.html">Terms</a>
  </footer>
</body>
</html>'''

def write(rel, content):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

nav_en = ('Tea','Teaware','History','Fresh Tea Drinks')
nav_zh = ('茶叶','茶具','茶文化历史','现制茶饮')

# Keep existing simple pages, but update tea hub and longjing article heavily.
write('index.html', '<!doctype html><html><head><meta http-equiv="refresh" content="0; url=/china-tea/en/index.html"></head><body></body></html>')

for lang in ['en','zh']:
    is_zh = lang=='zh'
    prefix = f'{lang}/'
    navs = nav_zh if is_zh else nav_en
    brand = '中国茶志' if is_zh else 'China Tea Journal'
    switch_label = 'English' if is_zh else '中文'
    switch_home = '/china-tea/en/index.html' if is_zh else '/china-tea/zh/index.html'
    home_body = f'''<main class="wrap"><section class="hero story-hero"><div class="hero-copy"><p class="eyebrow">{'中文版' if is_zh else 'English Edition'}</p><h1>{'中国茶：从产地、工艺到日常生活' if is_zh else 'Chinese tea from terroir and craft to everyday life'}</h1><p class="lede">{'这是一个用中英文讲中国茶的文化网站。我们优先从中文语境出发，再面向国际读者重写，让茶不只是“一个商品分类”，而是一套真实生活方式。' if is_zh else 'This bilingual site introduces Chinese tea through Chinese-source cultural context, then rewrites it for international readers so tea appears not merely as a product category but as a lived system of craft, place, and hospitality.'}</p></div>{photo_figure('longjing-plantation.jpg', 'Tea plantation in Longjing, Hangzhou', 'Longjing tea fields in Hangzhou.')}</section><section class="post-grid"><a class="post" href="{lang}/tea/index.html"><span class="tag">{'茶叶' if is_zh else 'Tea'}</span><h3>{'先从绿茶与龙井开始' if is_zh else 'Start with green tea and Longjing'}</h3><p>{'龙井专题已经升级为长文图文页，包含工艺、冲泡、历史与杭州旅行线索。' if is_zh else 'The Longjing feature has been expanded into a long-form illustrated article with craft, brewing, history, and Hangzhou travel context.'}</p></a></section></main>'''
    write(f'{lang}/index.html', page(f'{brand} — Home', 'Bilingual Chinese tea culture website.', 'zh-CN' if is_zh else 'en', prefix, brand, navs, switch_home, switch_label, home_body))

# Tea section hubs
write('en/tea/index.html', page('Tea Leaves — China Tea Journal', 'A section on Chinese tea leaves, beginning with an in-depth Longjing feature.', 'en', 'en/', 'China Tea Journal', nav_en, '/china-tea/zh/tea/index.html', '中文', f'''<main class="wrap"><section class="subhero"><p class="eyebrow">Section</p><h1>Tea Leaves</h1><p class="lede">This section begins with a detailed Longjing feature because Longjing is one of the best gateways into Chinese green tea. From there, the site will expand toward Bi Luo Chun, Huangshan Maofeng, Liu’an Guapian, and other regionally distinct teas.</p></section><div class="content-stream">{photo_figure('longjing-dried.jpg','Dry Longjing tea leaves','Dry Longjing leaves reveal the flat shape produced by pan-firing and pressing.')}{photo_figure('longjing-steeped.jpg','Longjing tea after steeping','After steeping, Longjing opens into a bright, clean liquor and tender leaf base.')}<section class="feature-card"><h2>Featured article</h2><p>Read the full Longjing feature for leaf shape, processing, brewing temperature, cold brew possibility, flavor profile, and Hangzhou context.</p><p><a class="btn" href="en/tea/longjing.html">Read the Longjing feature</a></p></section></div></main>''', image='/china-tea/assets/img/photos/longjing-dried.jpg'))
write('zh/tea/index.html', page('茶叶 — 中国茶志', '从龙井开始，逐步扩展到更多中国代表性茶叶。', 'zh-CN', 'zh/', '中国茶志', nav_zh, '/china-tea/en/tea/index.html', 'English', f'''<main class="wrap"><section class="subhero"><p class="eyebrow">栏目</p><h1>茶叶</h1><p class="lede">这个栏目先从龙井切入，因为龙井几乎是理解中国绿茶最好的入口之一。接下来会继续扩展到碧螺春、黄山毛峰、六安瓜片、信阳毛尖等代表性茶叶。</p></section><div class="content-stream">{photo_figure('longjing-dried.jpg','龙井干茶','龙井干茶的扁平外形，与其炒制和压扁工艺高度相关。')}{photo_figure('longjing-steeped.jpg','冲泡后的龙井','冲泡后的龙井，汤色清亮，叶底嫩匀，能看出春茶的鲜活感。')}<section class="feature-card"><h2>本栏重点文章</h2><p>先阅读龙井专题：里面已经补充了工艺、冲泡、水温、香气、历史和杭州旅行相关内容。</p><p><a class="btn" href="zh/tea/longjing.html">阅读龙井专题</a></p></section></div></main>''', image='/china-tea/assets/img/photos/longjing-dried.jpg'))

# Longjing article
zh_body = f'''<main class="page article-rich"><article><p class="eyebrow">绿茶专题</p><h1>龙井：从一杯绿茶看见杭州的春天、工艺与地方生活</h1><p class="meta">2026-03-16 · Long-form feature</p>
<div class="story-grid"><div><p>如果你只记得一种中国绿茶，很多人都会先想到龙井。它的知名度太高了，以至于它常常被误认为是一种简单、统一、几乎不需要解释的茶。可真正接近龙井之后，事情正好相反：龙井不仅仅是一种茶名，它还是一整套关于春天、嫩度、炒制火候、清鲜审美、杭州地方记忆与中国绿茶评价方式的入口。</p><p>在外国读者的视角里，龙井最容易被看成一类“高级中国绿茶”。但在中文语境里，人们会讨论得更细：是不是明前，山场在哪里，炒得是否干净，香气是豆香、板栗香还是更偏兰花和清花香，汤感是否薄而不空，叶底是否鲜活。这些讨论说明，龙井不是一个平面的旅游符号，而是一种可被细细分辨的工艺结果。</p></div>{photo_figure('longjing-plantation.jpg','杭州龙井茶园','杭州龙井产区的茶园景观，会直接影响外国读者对“这杯茶从哪里来”的理解。')}</div>
<h2>龙井到底是什么茶？是否发酵？</h2><p>龙井属于中国绿茶。绿茶在六大茶类中通常被理解为<strong>不发酵茶</strong>，更准确地说，是通过杀青尽快钝化酶活性，从而尽量保留鲜叶的绿色调性与清鲜感。龙井之所以和很多外国人熟悉的“green tea”不完全一样，是因为中国绿茶内部差别非常大。龙井代表的是一种扁炒青绿茶的风格：外形扁平，香气较为收敛，滋味鲜爽清润，汤色明亮偏浅黄绿。</p>
<div class="story-grid">{photo_figure('longjing-frying.jpg','手工炒茶','龙井最关键的工艺之一是锅炒。炒的手法、力度、温度都会影响叶形和香气。')}<div><h2>龙井是怎么制作出来的？</h2><p>龙井并不是采下来就能喝。鲜叶采摘后，要经过摊放、杀青、理条、压扁、辉锅等步骤。不同产区、不同师傅、不同等级的龙井，具体细节会有变化，但总体逻辑很稳定：通过锅炒控制水分、固定香气、整理形态，并最终形成龙井标志性的扁平直挺外观。</p><p>也正因为是炒制，龙井常常带有一类非常中国化的绿茶香：不是花香扑面，也不是海藻味那种强烈鲜腥，而是比较克制、干净、接近炒豆和熟栗子的暖香。好龙井的关键，不是香得夸张，而是香气清而不浮，入口快而不薄。</p></div></div>
<h2>采摘的是什么叶子？为什么春茶最受重视？</h2><p>龙井通常讲究春季采摘，尤其早春嫩芽嫩叶。茶叶越嫩，做出来往往越鲜、越细、越显清透。很多消费者熟悉“明前茶”这个说法，本质上说的就是清明前后春茶嫩度高、产量低、风格轻盈细致。但并不是所有“早”都一定等于“好”，因为天气、日照、树龄、土壤与工艺同样会影响成品表现。</p><p>对外国读者来说，很重要的一点是：龙井不是靠浓烈取胜。它的魅力反而在于轻、鲜、净、滑。在中国茶体系里，这种“看似轻、实则要求很高”的茶，最能暴露工艺是否到位。</p>
<div class="story-grid"><div><h2>怎么冲泡龙井？和别的茶有什么不同？</h2><p>龙井适合用玻璃杯或盖碗来泡。玻璃杯的好处是可以直接观察干茶、茶汤和叶底变化；盖碗则更利于控制出汤和闻香。和很多乌龙茶、黑茶不同，龙井一般不追求高温猛冲。常见建议是<strong>80°C 到 90°C</strong> 左右的水温，过高的水温容易把鲜感和细腻度打散，甚至带出明显涩味。</p><p>如果用盖碗，投茶量可以从 3 克左右开始，水量约 100-120 毫升，首泡浸泡时间不宜过长，通常 10-20 秒已足够。后面每一泡略微延长。总体上，优质龙井常见可以冲泡 3 到 4 泡，具体仍取决于等级、保存状态和泡法。它也可以冷泡，但冷泡更强调清甜和植物感，未必能完整体现传统热泡时的鲜爽层次。</p><p>和浓香型乌龙或陈年普洱相比，龙井不是那种“越泡越重”的茶。它更像一首短诗，重点在前几泡的鲜、香、净、细，而不在厚重与耐久上。</p></div>{photo_figure('longjing-steeped.jpg','龙井茶汤与叶底','龙井冲泡后，茶汤清亮，叶片舒展，能够直观看到其嫩度和制作的完整性。')}</div>
<h2>龙井闻起来、喝起来是什么感觉？</h2><p>如果是品质好的龙井，干茶通常扁平匀整，颜色嫩绿或糙米黄绿之间，闻起来有清净的豆香、板栗香，某些批次也会带轻微花香。热泡后，香气不会一上来就“炸开”，而是相对内敛。入口则应尽量鲜活、柔和、滑，回甘来得快但不张扬。差的龙井则可能表现为香气浮、火气重、茶汤散、涩感明显。</p>
<div class="story-grid">{photo_figure('longjing-dried.jpg','龙井干茶细节','干茶的匀整度、扁平程度和色泽，都是理解龙井工艺的直观入口。')}<div><h2>除了龙井，还有哪些特色绿茶？</h2><p>如果读者因为龙井喜欢上中国绿茶，下一步很值得继续认识碧螺春、黄山毛峰、六安瓜片、信阳毛尖、太平猴魁、安吉白茶等。它们都属于“绿茶”，但风格差异巨大：有的偏花果鲜香，有的偏清雅细嫩，有的强调形态辨识度，有的强调山场和兰韵。这也正说明，中国绿茶不是一条单调的线，而是一整片风格谱系。</p><p>未来这个网站会把这些茶一一展开，并尽可能配上产区图、茶叶图、茶汤图与具体冲泡建议。</p></div></div>
<h2>龙井的历史，为什么总是和杭州连在一起？</h2><p>龙井之所以被外国游客迅速记住，很大程度上是因为它和杭州、西湖、龙井村这些空间名词紧紧绑在一起。杭州本来就是中国城市审美和旅游想象中的重要节点，而龙井刚好给了这座城市一种“可被喝到”的地方象征。去杭州的人，不只是去看西湖，还会想知道：这座城市喝什么茶？春天的山坡是什么样？龙井村到底是不是一张被过度消费的明信片？</p><p>事实上，龙井作为地方名茶的历史叙述非常复杂，既有宫廷与名茶的故事，也有现代旅游传播与地理标识体系的作用。但对普通读者来说，最有帮助的理解方式也许是：龙井让一杯茶和一个地方形成了牢固连接。你喝的不是抽象的“Chinese green tea”，而是杭州周边山地、湿润气候、春季采摘和地方工艺共同压缩出来的一段风土经验。</p>
<div class="story-grid"><div><h2>如果去杭州，围绕龙井可以看什么？</h2><p>如果把龙井当作理解杭州的一条线索，最自然的路线包括：西湖周边、龙井村、梅家坞、茶园步道，以及和文人传统相关的景点。对外国游客来说，最好的方式不是只买一包写着“Longjing”的纪念品，而是去真正看看茶园坡地、观察春季采茶时节、在现场喝一杯刚冲开的绿茶。那时你会意识到，龙井之所以重要，并不是因为它“高档”，而是因为它把杭州的自然、城市记忆和生活方式连在了一起。</p><p>如果是内容策展的角度，杭州还适合和龙井放在一起讲的主题包括：西湖十景、文人饮茶、江南生活方式、慢旅行与季节性消费。茶让一座城市变得更可叙述，也让旅行不只是看景，而是进入一种更细密的地方感受。</p></div>{photo_figure('longjing-village.jpg','龙井村景观','龙井村和周边茶山，是许多游客第一次把茶与具体地理空间联系起来的地方。')}</div>
<h2>为什么龙井值得成为外国读者认识中国茶的第一站？</h2><p>因为它好懂，但不浅。你可以先从“这是中国最有名的绿茶之一”开始，再一步步进入更深的东西：什么叫不发酵，为什么要炒，为什么水温不能太高，为什么绿茶也会有这么多风格差异，为什么一杯茶会和一座城市、一段历史、一条旅行路线连在一起。好的中国茶写作，不应该只把茶写成参数，也不该只把茶写成神秘东方想象。龙井的价值就在于，它允许这两端相遇：既有技术细节，也有地方故事。</p></article></main>'''

en_body = f'''<main class="page article-rich"><article><p class="eyebrow">Green Tea Feature</p><h1>Longjing: Spring in Hangzhou, pan-fired craft, and the local life inside one cup</h1><p class="meta">2026-03-16 · Long-form feature</p>
<div class="story-grid"><div><p>If many readers can name only one Chinese green tea, it is often Longjing. Its reputation is so large that it is easily mistaken for something simple, unified, and self-explanatory. Yet the closer one gets to Longjing, the less simple it becomes. Longjing is not merely a tea name. It is an entry point into spring picking, tenderness, pan-firing, restrained freshness, Hangzhou’s local memory, and the broader Chinese way of evaluating green tea.</p><p>From an international perspective, Longjing is often reduced to “a famous premium Chinese green tea.” In Chinese tea discourse, however, people ask finer questions: Was it picked before Qingming? Which hillside does it come from? Was the pan-firing clean? Is the aroma more bean-like, chestnut-like, floral, or especially clear? Does the liquor feel thin, or light yet structured? These questions show that Longjing is not a flat tourism symbol. It is a crafted result open to sensory interpretation.</p></div>{photo_figure('longjing-plantation.jpg', 'Tea plantation in Hangzhou', 'Longjing tea fields in Hangzhou help readers understand that tea begins in a real landscape, not on a retail shelf.')}</div>
<h2>What kind of tea is Longjing? Is it fermented?</h2><p>Longjing belongs to the category of Chinese green tea. In the six major Chinese tea categories, green tea is usually described as <strong>non-fermented</strong>, though more precisely it is tea whose enzymes are deactivated early through heat, preserving a fresh, green profile. Longjing differs from the generic international notion of “green tea” because Chinese green tea itself contains many internal styles. Longjing represents a flat, pan-fired style: broad, pressed leaves; a relatively restrained aroma; bright liquor; and a fresh, smooth, quick-drinking palate.</p>
<div class="story-grid">{photo_figure('longjing-frying.jpg','Tea maker pan-frying leaves','Pan-firing is one of the defining Longjing techniques. Heat control and hand motion shape both aroma and leaf form.')}<div><h2>How is Longjing made?</h2><p>Longjing does not become itself the moment it is picked. Fresh leaves are withered briefly, heated to halt enzyme activity, shaped, pressed, and repeatedly pan-fired until the famous flattened profile emerges. Details vary by producer, season, grade, and local habit, but the overall logic remains stable: reduce moisture, stabilize aroma, control leaf shape, and create a tea that feels clear and composed rather than wild or grassy.</p><p>Because of this pan-firing process, Longjing often develops a very specifically Chinese green-tea aroma: not explosive floral perfume, not marine sharpness, but a restrained warmth often described as bean-like or chestnut-like. Excellent Longjing should not be loud. It should feel clean, even-tempered, and quietly precise.</p></div></div>
<h2>What leaves are picked, and why is spring tea so prized?</h2><p>Longjing is usually associated with spring harvest, especially very early tender shoots and leaves. The younger the material, the more likely the finished tea is to feel delicate, fresh, and fine-textured. Many consumers know the phrase “pre-Qingming tea,” which refers to tea picked before the Qingming festival period. These early leaves are valued for tenderness and scarcity, though “earlier” does not automatically guarantee “better.” Weather, sunlight, cultivar, soil, and firing skill remain decisive.</p><p>For international readers, a key point is that Longjing does not aim to impress through brute strength. Its appeal lies in lightness, freshness, clarity, and softness. In Chinese tea culture, teas that seem light on the surface often demand the greatest discipline in making.</p>
<div class="story-grid"><div><h2>How should Longjing be brewed? How is it different from other teas?</h2><p>Longjing is well suited to brewing in a glass or a gaiwan. A glass shows the leaves, liquor, and leaf base beautifully; a gaiwan gives better control over aroma and pouring. Unlike many oolong teas or dark teas, Longjing usually does not benefit from very high water temperature. A practical range is <strong>80°C to 90°C</strong>. Water that is too hot can flatten freshness, sharpen bitterness, and erase the tea’s finer textures.</p><p>In a gaiwan, around 3 grams of leaf for 100-120 ml of water is a reasonable starting point. The first infusion often needs only 10-20 seconds, with slightly longer times afterward. Good Longjing commonly yields 3 to 4 satisfying infusions, depending on grade, storage, and brewing style. It can also be cold brewed, but cold brewing emphasizes sweetness and vegetal freshness more than the classic warm, spring-like texture of hot brewing.</p><p>Compared with strong-roasted oolong or aged pu-erh, Longjing is not a tea whose drama intensifies with each infusion. It is closer to a short lyric poem: the first cups matter most, and their beauty lies in freshness, precision, and restraint.</p></div>{photo_figure('longjing-steeped.jpg','Steeped Longjing tea','Once brewed, Longjing reveals bright liquor, tender leaves, and a visual sense of spring freshness.')}</div>
<h2>What does Longjing smell and taste like?</h2><p>Good Longjing tends to have flat, even leaves in tones between soft green and rice-yellow green. Dry aroma often suggests clean beans or chestnuts, sometimes with a light floral lift. When brewed, the fragrance is not usually explosive. The liquor should feel lively, smooth, clear, and quietly sweet, with a gentle returning sweetness rather than theatrical intensity. Poorer Longjing often tastes scattered, aggressively toasty, harsh, or obviously astringent.</p>
<div class="story-grid">{photo_figure('longjing-dried.jpg','Dry Longjing leaves','Dry-leaf appearance—flatness, uniformity, and color—offers a direct clue to Longjing processing quality.')}<div><h2>What other green teas matter besides Longjing?</h2><p>If Longjing becomes a reader’s gateway into Chinese green tea, the next teas worth meeting include Bi Luo Chun, Huangshan Maofeng, Liu’an Guapian, Xinyang Maojian, Taiping Houkui, and Anji Baicha. All belong to “green tea,” yet each speaks a different language of shape, aroma, mountain character, and brewing behavior. That diversity is exactly why Chinese green tea should not be imagined as a single taste profile.</p><p>This site will gradually expand toward those teas with more region pages, tea field imagery, dry-leaf photos, liquor photos, and practical brewing notes.</p></div></div>
<h2>Why is Longjing so tightly tied to Hangzhou?</h2><p>Longjing is memorable partly because it is inseparable from the place-names surrounding it: Hangzhou, West Lake, Longjing Village, and the tea hills nearby. Hangzhou already carries an enormous cultural charge in Chinese urban imagination; Longjing gives that city a flavor you can literally drink. Visitors do not only want to see West Lake. They also want to know: What tea belongs to this place? What do the hills look like in spring? Is Longjing Village only a postcard, or is it still a living tea landscape?</p><p>Historically, the fame of Longjing is layered, involving imperial associations, the cultural status of famous teas, modern tourism, and geographical branding. Yet the most useful way to explain it may be simple: Longjing is one of the strongest examples of a tea becoming inseparable from a landscape. What you drink is not an abstract “Chinese green tea,” but a compressed experience of spring weather, hillside cultivation, local craft, and regional memory.</p>
<div class="story-grid"><div><h2>If you visit Hangzhou, what can you see through the lens of Longjing?</h2><p>If Longjing becomes your thread into Hangzhou, natural stops include West Lake, Longjing Village, Meijiawu, tea-field walking routes, and sites tied to literati culture. For foreign visitors, the best encounter is not merely buying a souvenir bag labeled “Longjing,” but actually walking tea slopes, observing the spring landscape, and drinking green tea close to where that style took shape. Then the tea begins to feel less like a luxury product and more like a local way of life.</p><p>From a storytelling perspective, Longjing also opens out toward broader Hangzhou themes: the Ten Scenes of West Lake, Jiangnan aesthetics, scholar culture, seasonal travel, and the relationship between natural beauty and daily refinement. Tea makes the city more legible, and the city in turn makes the tea more memorable.</p></div>{photo_figure('longjing-village.jpg','Longjing Village','Longjing Village and its surrounding slopes are where many visitors first connect tea to a concrete geography.')}</div>
<h2>Why is Longjing such a good first station for learning Chinese tea?</h2><p>Because it is approachable without being shallow. One can begin with “this is one of China’s most famous green teas,” and then gradually move deeper: What does non-fermented really mean? Why pan-fire instead of roast another way? Why avoid boiling water? Why can green teas differ so radically from each other? Why should a cup of tea be connected to a city, a season, and a travel route? Good writing on Chinese tea should neither reduce tea to parameters nor dissolve it into vague oriental mystery. Longjing allows both sides to meet: technical craft and local story.</p></article></main>'''

write('zh/tea/longjing.html', page('龙井：从一杯绿茶看见杭州的春天、工艺与地方生活 — 中国茶志', '详细介绍龙井的工艺、冲泡、茶汤风味、历史以及杭州旅行语境。', 'zh-CN', 'zh/', '中国茶志', nav_zh, '/china-tea/en/tea/longjing.html', 'English', zh_body, image='/china-tea/assets/img/photos/longjing-plantation.jpg'))
write('en/tea/longjing.html', page('Longjing: spring in Hangzhou, pan-fired craft, and local life — China Tea Journal', 'A detailed feature on Longjing tea covering craft, brewing, flavor, history, and Hangzhou travel context.', 'en', 'en/', 'China Tea Journal', nav_en, '/china-tea/zh/tea/longjing.html', '中文', en_body, image='/china-tea/assets/img/photos/longjing-plantation.jpg'))

# Keep other pages simple but present
for lang, is_zh in [('en',False),('zh',True)]:
    prefix=f'{lang}/'; navs=nav_zh if is_zh else nav_en; brand='中国茶志' if is_zh else 'China Tea Journal'; langcode='zh-CN' if is_zh else 'en'
    simple_pages={
        'about.html': ('About', 'A bilingual cultural website about Chinese tea.' if not is_zh else '一个介绍中国茶文化的双语网站。'),
        'privacy.html': ('Privacy Policy', 'This site currently uses no active advertising trackers by default.' if not is_zh else '本站当前默认不启用主动广告追踪。'),
        'contact.html': ('Contact', 'Contact the repository owner for corrections or collaboration.' if not is_zh else '如需纠错或合作，请联系仓库所有者。'),
        'terms.html': ('Terms', 'Educational and cultural content only.' if not is_zh else '本站内容主要用于文化与知识介绍。'),
        'teaware/index.html': ('Teaware', 'More long-form teaware features will be added.' if not is_zh else '后续会继续扩充茶具专题长文。'),
        'history/index.html': ('Tea Culture & History', 'More long-form history features will be added.' if not is_zh else '后续会继续扩充茶文化历史专题长文。'),
        'drinks/index.html': ('Fresh Tea Drinks', 'More long-form drink features will be added.' if not is_zh else '后续会继续扩充现制茶饮专题长文。'),
    }
    for rel,(title,text) in simple_pages.items():
        switch='/china-tea/en/'+rel if is_zh else '/china-tea/zh/'+rel
        body=f'<main class="page"><article><h1>{title}</h1><p>{text}</p></article></main>'
        write(f'{lang}/{rel}', page(f'{title} — {brand}', title, langcode, prefix, brand, navs, switch, 'English' if is_zh else '中文', body))

urls=['','en/index.html','zh/index.html','en/tea/index.html','zh/tea/index.html','en/tea/longjing.html','zh/tea/longjing.html','en/about.html','zh/about.html','en/privacy.html','zh/privacy.html','en/contact.html','zh/contact.html','en/terms.html','zh/terms.html']
xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    loc = f'{BASE}/' if u=='' else f'{BASE}/{u}'
    xml.append(f'  <url><loc>{loc}</loc></url>')
xml.append('</urlset>')
write('sitemap.xml','\n'.join(xml))
write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: https://mlaibook.github.io/china-tea/sitemap.xml\n')
