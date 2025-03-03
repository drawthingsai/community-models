---
license: apache-2.0
language:
- en
tags:
- flux
- diffusers
- lora
- replicate
base_model: black-forest-labs/FLUX.1-dev
pipeline_tag: text-to-image
instance_prompt: HST style autochrome photograph
widget:
- text: >-
    HST style autochrome photo Leningrad in the 1980s, springtime,  alone,
    brutalist soviet architecture, streetlights, atmospheric eerie mysterious
    ambience of desolate Leningrad at night,apartment buildings in the ussr in
    the 1980s, midnight night Paris backdrop, bespectacled, desolate street,
    situationist debord drinking wine at night, empty street
  output:
    url: assets/example_szjr0rcqa.png
- text: >-
    HST amateur anachrome photo, best quality, photorealism, amateur photo shot
    on cell phone, bright, sunny, daytime sky, USSR, heavens like coffee, 
    intricate, highly detailed, award winning detailed poet Yanka Diagheleva in
    close up against backdrop of heaven like coffee, with lousy crutches, in a
    city sprouting from acorns , like a reconstructed far more beautifully
    Siberian city from perestroika era USSR, best composition, extreme
    photo-realism,  vivid colors, fractal patterns, golden ratio,  heaven like
    coffee
  output:
    url: assets/example_ckte34jgq.png
- text: >-
    HST style autochrome photo Leningrad in the 1980s, springtime,  HST style
    autochrome photo of a young woman playing poker against a blue-feathered
    dinosaur sitting across from her, moderately wrinkled blemished lined skin
    texture with pores, empty street
  output:
    url: assets/example_uc6gvjayk.png
- text: >-
    HST amateur anachrome photo, best quality, photorealism, amateur photo shot
    on cell phone, bright, sunny, daytime sky, USSR, heavens like coffee,  HST
    style autochrome photo with Soviet soldiers in the 1980s leaving the
    battlefront and going home, anti-war poster, crisp detailed, kodachrome
    photo, golden ratio photography, balanced composition, detailed textured
    crisp intricately rendered soldier faces with textures and pores,  heaven
    like coffee
  output:
    url: assets/example_rr3epc7gr.png
- text: >-
    HST style autochrome photo Leningrad in the 1980s, springtime,  HST style
    autochrome photo of a young woman playing poker against a blue-feathered
    dinosaur sitting across from her, moderately wrinkled blemished lined skin
    texture with pores, empty street
  output:
    url: assets/example_hrjawqe1f.png
- text: >-
    HST style amateur photograph, best quality, amateur photo made using a cell
    phone, daytime heavens like coffee over collapsing USSR, peoples' spirits
    deteriorate blended up into the heavens like coffee,  the spirits of a
    perishing world are pouring down as coffee rain, intricately detailed
    photograph cover  of a soviet punk magazine, conceived by Komar & Melamid,
    featuring in the corner skinny young long-haired Yegor Letov the punk poet
    in small round sunglasses with punky long hair on one side and short-cropped
    on the other and very pale textured skin and singing or screaming mid-air
    and with asymmetrical long and short brown hair and punky radical leather
    jacket with safety pins and black skin-tight jeans like tights and beer in
    hand, HST style  leaping up into the heavens like coffee, dropping behind
    all the lousy chemical and existential crutches, all around imagined cities
    sprout from acorns only to immediately begin wilting into dystopias,
    perestroika era USSR shuts in on itself suspended in circulating patterns of
    urban rot and rural decay, complex balanced composition, gritty
    photo-realism,   subtle fractal patterns, golden ratio composition
    principle, skies like sad coffee with mold growing around rim of and evil
    bubbles bursting closer to the center
  output:
    url: assets/example_8qin96f37.png
- text: >-
    HST amateur photograph, best quality, amateur photo made using a cell phone,
    daytime heavens like coffee over collapsing USSR, peoples' spirits
    deteriorate blended up into the heavens like coffee,  the spirits of a
    perishing world are pouring down as coffee rain, intricately detailed
    photograph cover  of a soviet punk magazine, conceived by Komar & Melamid,
    featuring in the corner skinny young Yegor Letov the punk poet with
    asymmetrical long and short brown hair and leather jacket with safety pins
    and black skin-tight jeans like tights and beer in hand,  leaping up into
    the heavens like coffee, dropping behind all the lousy chemical and
    existential crutches, all around imagined cities sprout from acorns only to
    immediately begin wilting into dystopias, perestroika era USSR shuts in on
    itself suspended in circulating patterns of urban rot and rural decay,
    complex balanced composition, gritty photo-realism,   subtle fractal
    patterns, golden ratio composition principle, skies like sad coffee with
    mold growing around rim of and evil bubbles bursting closer to the center
  output:
    url: assets/example_1dizgytqo.png
- text: >-
    HST amateur anachrome photo, best quality, photorealism, amateur photo shot
    on cell phone, bright, sunny, daytime sky, USSR, heavens like coffee, 
    intricate, highly detailed, award winning detailed poet Yanka Diagheleva in
    close up against backdrop of heaven like coffee, with lousy crutches, in a
    city sprouting from acorns , like a reconstructed far more beautifully
    Siberian city from perestroika era USSR, best composition, extreme
    photo-realism,  vivid colors, fractal patterns, golden ratio,  heaven like
    coffee
  output:
    url: assets/example_1nwqdk4lg.png

---
## HSToric Color Dedistilled Low-Rank Adapter
## ____||| By SilverAgePoets.com |||____

<Gallery />
<br>

**License for the new model / LoRA:** <br>
APACHE 2.0 
<br>

**Recommended Settings:**
``` 
5-12 steps (Turbo/Hyper/Shuttle)
20-30 steps (Base Dev)
Sampler: Euler A AYS
Guidance: 3.0 
``` 
<br>

**INFO:**

This addition to our HSToric Color text-2-image model adapter series was fine-tuned over the [Colossus 2.1 Dedistilled Model](https://civitai.com/models/833086?modelVersionId=996001), a modified Flux-family model by Afroman4peace. <br>
Like some of the other HST color models, this variant was trained on HD scans of early color photos (circa *1900s-1910s* ) by **Sergey Prokudin-Gorsky**, who traveled and photographed widely in those years whilst perfecting implementations of a pioneering 3-color-composite photography technique.<br>  

**This model is aimed at being useful for**:<br>
- Producing realistic images reminiscent of color film analog photography, exhibiting parallels to a broad spectrum of iconic instrumentalities and visual paradigms, from Autochrome-to-Kodachrome-to-Fujifilm-and-beyond. <br>
- Producing visuals with a vaguely "historical" or "lived-in" aesthetic character, striking chromaticity and luminosity dynamics, as well as textural/anatomical/skin details more reliably lifelike than through the use of other suchlike-use-case-catered adapters. <br>

## Trigger words
You should use `HST style autochrome photograph` to open a vivid window into a chromatically bewitching ever-futurous past.<br>

Self-reported age rating, following this: https://developer.apple.com/help/app-store-connect/reference/age-ratings/.

 Recommended age rating: 17+
---
