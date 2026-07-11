"""Builds deep-dive pages for batch 5 and updates index + breed CTAs.
   Also writes profiles to deep_dive_profiles tab in Excel.
"""
import os, re, openpyxl

BREEDS = [
    (
        'saluki', 'Saluki',
        'Runs 40 mph. Might come back. No promises.',
        'saluki_3.jpg',
        'One of the oldest breeds alive &mdash; ancient grace, ancient prey drive, and an unreliable recall.',
    ),
    (
        'samoyed', 'Samoyed',
        'The smile is structural. The shedding is also structural.',
        'samoyed_3.jpg',
        'The smiling sled dog &mdash; genuinely wonderful, as long as you&rsquo;re committed to the coat.',
    ),
    (
        'shiba-inu', 'Shiba Inu',
        'Has opinions. Will escalate. Actually you&rsquo;re not allowed here.',
        'shiba_inu_2.jpg',
        'Japan&rsquo;s most popular dog &mdash; independent, clean, and deeply uninterested in your commands.',
    ),
    (
        'siberian-husky', 'Siberian Husky',
        'Sled dog in the suburbs. Still acts like it&rsquo;s pulling the sled.',
        'siberian_husky_3.jpg',
        'Built for 100-mile Arctic slogs &mdash; your suburb isn&rsquo;t going to tire this dog out.',
    ),
    (
        'skye-terrier', 'Skye Terrier',
        'Rarer than a panda. Exactly as dignified.',
        'skye_terrier_2.jpg',
        'One of Britain&rsquo;s rarest native breeds &mdash; deeply loyal and genuinely unusual.',
    ),
    (
        'vizsla', 'Vizsla',
        'Velcro dog. Literally. Has not left your side since Tuesday.',
        'vizsla_2.jpg',
        'The velcro sporting dog &mdash; athletic, sensitive, and constitutionally unable to be more than 3 feet away.',
    ),
    (
        'weimaraner', 'Weimaraner',
        'Gray Ghost. Extremely intense. Currently chewing something.',
        'weimaraner_2.jpg',
        'The Gray Ghost &mdash; a focused, intense athlete that people routinely underestimate.',
    ),
    (
        'whippet', 'Whippet',
        '35 mph sprinter. World-class napper. No in-between.',
        'whippet_3.jpg',
        'The most underrated sighthound &mdash; fast, gentle, low-maintenance, and genuinely great for most households.',
    ),
]

PROFILES = {
    'Saluki': {
        'breed_name': 'Saluki',
        'primary_role': 'Hunting',
        'physical_activity_needs': 'High',
        'mental_stimulation_needs': 'Moderate',
        'size': 'Large',
        'grooming_needs': 'Low',
        'trainability': 'Independent-Minded',
        'good_for_beginners': 'Not Recommended',
        'apartment_friendly': 'No',
        'temperament_narrative': (
            "Salukis are one of the oldest dog breeds in existence, and they carry that ancient lineage in their bearing — elegant, reserved, and entirely self-contained. They're affectionate with the people they choose, but strangers are met with indifference rather than warmth, and they'll never be a dog that performs for the room.\n\n"
            "The prey drive is intense and deeply hardwired — this is a dog built to chase, and once a Saluki's eye catches something moving, recall becomes essentially theoretical. Secure fencing isn't optional; it's the whole system."
        ),
        'health_lifespan_narrative': (
            "Salukis typically live 12–14 years and are generally healthy for a purebred of their size. Like all sighthounds, they have very low body fat, which affects how they metabolize anesthesia — any vet performing a procedure should know this before sedating the dog.\n\n"
            "Heart conditions appear in the breed at modest rates and are worth monitoring. Sensitivity to cold is real and not performative — a Saluki that refuses to go out in winter weather is telling you something accurate about its insulation situation."
        ),
        'nutrition_narrative': (
            "A lean, bony-looking build is correct for this breed — do not attempt to add weight to a dog that's supposed to look this way. Quality protein matters, and Salukis can be selective, sometimes frustratingly so, about food.\n\n"
            "Smaller meals rather than one large feeding suits the breed's constitution well. They're not prone to overeating, so free-feeding is an option for some, but quality still matters."
        ),
        'family_fit_narrative': (
            "Salukis do fine with calm, respectful children who understand that this dog isn't a cuddler on demand. The intense prey drive makes them a poor match for households with cats, rabbits, or other small animals — this isn't something training reliably overrides.\n\n"
            "For active families willing to provide real running time in a safely enclosed space, and who appreciate a dog that's devoted but not demonstrative, the Saluki is a genuinely rewarding companion."
        ),
        'honest_take_narrative': (
            "The honest thing about Salukis is that they're not trainable in the way most people mean. They're intelligent and they understand you; they simply don't prioritize your requests the way retrievers do. Recall off-leash, in any open space, is unreliable by design.\n\n"
            "What you get in return is a dog of extraordinary grace — quiet, gentle indoors, low-maintenance on grooming, and deeply bonded to their person in a way that doesn't look like a Labrador's bonding but is just as real. If you can meet them where they are rather than trying to make them something they're not, they're remarkable."
        ),
    },
    'Samoyed': {
        'breed_name': 'Samoyed',
        'primary_role': 'Working',
        'physical_activity_needs': 'High',
        'mental_stimulation_needs': 'High',
        'size': 'Medium',
        'grooming_needs': 'Very High',
        'trainability': 'Moderate',
        'good_for_beginners': 'With Experience',
        'apartment_friendly': 'No',
        'temperament_narrative': (
            "The Samoyed's signature feature is that smile — an actual, anatomical upward curl at the corners of the mouth that evolved to prevent drooling in freezing temperatures and ended up making every single Samoyed look like they're delighted to see you. The personality generally matches.\n\n"
            "This is a friendly, social, vocal dog that was bred to live and sleep in close proximity to people in Siberian conditions. They are genuinely people-oriented and don't do well in isolation — separation anxiety is real and common. They are also loud about their opinions, which is fine in a house and a problem in an apartment building."
        ),
        'health_lifespan_narrative': (
            "Samoyeds typically live 12–14 years. The breed's major genetic concern is Samoyed hereditary glomerulopathy, a kidney disease that primarily affects males and is worth understanding before committing to the breed — responsible breeders test for it.\n\n"
            "Hip dysplasia, progressive retinal atrophy, and subvalvular aortic stenosis (a heart condition) all occur at notable rates. Eye and heart testing are standard in responsible breeding programs and worth confirming when selecting a puppy."
        ),
        'nutrition_narrative': (
            "Samoyeds are active dogs with real caloric needs, though their thick coat can make it harder to gauge body condition — run your hands over the ribs periodically rather than judging by appearance alone.\n\n"
            "They don't have unusual dietary requirements, but weight management matters since a heavy Samoyed puts additional strain on joints that are already worth monitoring for dysplasia."
        ),
        'family_fit_narrative': (
            "Samoyeds are genuinely excellent with children — patient, gentle, and social in a way that suits family life well. They also tend to do well with other dogs. The breed's need for company makes them a natural fit in busy households where people are around most of the time.\n\n"
            "What they're not suited for: being left alone for long stretches routinely, apartment living, or households where the commitment to grooming isn't real and sustained."
        ),
        'honest_take_narrative': (
            "The coat is the honest starting point for Samoyed ownership. It sheds year-round and spectacularly twice a year — we're talking tumbleweeds of white fluff from every corner of your home, your car, your wardrobe, your lunches. Brushing multiple times a week is maintenance; skipping it leads to matting that requires professional intervention.\n\n"
            "If you can make peace with the grooming, you get one of the most genuinely pleasant dogs to live with — happy, social, funny, and unfailingly friendly. The smile isn't a lie."
        ),
    },
    'Shiba Inu': {
        'breed_name': 'Shiba Inu',
        'primary_role': 'Hunting',
        'physical_activity_needs': 'Moderate',
        'mental_stimulation_needs': 'High',
        'size': 'Small',
        'grooming_needs': 'Moderate',
        'trainability': 'Independent-Minded',
        'good_for_beginners': 'Not Recommended',
        'apartment_friendly': 'With Enough Exercise',
        'temperament_narrative': (
            "The Shiba Inu is the most popular dog in Japan, and understanding why requires understanding that Japanese dog culture rewards a different set of traits than most Western dog ownership does — independence, cleanliness, dignity, and loyalty on the dog's own terms rather than endless social enthusiasm.\n\n"
            "Shibas are clean, cat-like, and genuinely devoted to their people without being clingy about it. They're also vocal — the 'Shiba scream' is a real thing, deployed at maximum volume during bathtime, nail trims, or perceived injustices — and they have strong opinions about strangers and other animals."
        ),
        'health_lifespan_narrative': (
            "Shibas are generally hardy and live 13–16 years, among the longer lifespans in their size class. The breed does carry some risk for hip dysplasia, patellar luxation, and progressive retinal atrophy, though at rates lower than many comparable breeds.\n\n"
            "The bigger health conversation for Shibas is usually allergies — both environmental and food-related skin sensitivities appear frequently. If a Shiba is scratching chronically or having recurring ear infections, diet or environmental allergens are often involved."
        ),
        'nutrition_narrative': (
            "Shibas are prone to food sensitivities and can be particular about what agrees with them. High-quality protein from a limited number of sources is often the starting point when managing skin or digestive issues.\n\n"
            "They're not heavy eaters for their size, and overfeeding is easy to do with a breed that has a naturally compact build. Keep them lean — extra weight on small dogs adds up faster than people expect."
        ),
        'family_fit_narrative': (
            "Shibas are better suited to households with older children who understand the concept of respecting a dog's space. Their prey drive is real and small animals — cats, rabbits, birds — are genuinely at risk. They can coexist with cats they've been raised with, but it's not guaranteed.\n\n"
            "They're often better in calmer households than chaotic ones, and they bond deeply to their core family while remaining reserved with everyone else — which is exactly what some families want."
        ),
        'honest_take_narrative': (
            "The Shiba Inu is not a beginner dog dressed up in a compact package. The independent nature isn't something training fixes — it's the whole personality. Recall off-leash is genuinely unreliable, and any off-leash time should happen in fully enclosed spaces.\n\n"
            "For the right owner — someone who appreciates a dog that's clean, self-sufficient, and bonded to them without being needy — the Shiba is deeply satisfying. For someone expecting the easy affection of a golden, this will be a frustrating relationship. Matching expectations to the actual breed is the whole game here."
        ),
    },
    'Siberian Husky': {
        'breed_name': 'Siberian Husky',
        'primary_role': 'Working',
        'physical_activity_needs': 'Very High',
        'mental_stimulation_needs': 'High',
        'size': 'Medium',
        'grooming_needs': 'High',
        'trainability': 'Moderate',
        'good_for_beginners': 'Not Recommended',
        'apartment_friendly': 'No',
        'temperament_narrative': (
            "Huskies are pack dogs — friendly, outgoing, and genuinely good with people. They're not guard dogs; a Husky is statistically more likely to show a burglar where the treats are than to deter one. What they are: energetic, vocal, mischievous, and extraordinarily difficult to tire out.\n\n"
            "The howling is real. The escape artistry is real. The selective hearing is real. Huskies are bred to run 100 or more miles per day in Arctic conditions, and no amount of walks in a subdivision is going to fully address that. They need genuine, sustained exercise, a securely fenced environment, and an owner who understands that 'stubborn' is how people describe an independent working dog in a pet context."
        ),
        'health_lifespan_narrative': (
            "Siberian Huskies typically live 12–14 years and are generally healthy for a medium-to-large breed. Hip dysplasia is present at moderate rates. Eye conditions — including hereditary juvenile cataracts and progressive retinal atrophy — are worth screening for; the Siberian Husky Club of America maintains a registry for eye-clear dogs.\n\n"
            "One non-intuitive note: Huskies are metabolically efficient and eat significantly less than people expect for a dog their size. Overfeeding is common and leads to weight gain that their joints don't need."
        ),
        'nutrition_narrative': (
            "Huskies are famously efficient — they were bred to cover enormous distances on minimal food. This means they genuinely need less food than a dog their size would typically get, and owners regularly overfeed them with good intentions.\n\n"
            "Follow weight and body condition rather than package guidelines, which are nearly always set for average activity levels. A Husky doing serious daily exercise needs more; a Husky on suburban walks needs less than the bag suggests."
        ),
        'family_fit_narrative': (
            "Huskies are excellent with children and generally good with other dogs — they're pack animals and that social instinct runs deep. They're too energetic for households without enough outdoor space and time, but in the right active family they're joyful, affectionate companions.\n\n"
            "Cats are a different story. The prey drive varies by dog but is strong enough in many Huskies that mixed households require careful management and are often not recommended."
        ),
        'honest_take_narrative': (
            "The Husky is a completely honest dog. It will tell you exactly what it needs — loudly, repeatedly, often at 2am — and the needs are real: significant daily exercise, consistent training, a securely fenced yard (they climb, dig, and squeeze), and your company, because they don't do well alone.\n\n"
            "They're also genuinely delightful — funny, social, beautiful, and loyal in their particular way. The people who love Huskies love them because of these traits, not despite them. The people who struggle with Huskies are usually people who thought the energy was optional."
        ),
    },
    'Skye Terrier': {
        'breed_name': 'Skye Terrier',
        'primary_role': 'Hunting, Companion',
        'physical_activity_needs': 'Moderate',
        'mental_stimulation_needs': 'Moderate',
        'size': 'Small',
        'grooming_needs': 'High',
        'trainability': 'Moderate',
        'good_for_beginners': 'Not Recommended',
        'apartment_friendly': 'With Enough Exercise',
        'temperament_narrative': (
            "The Skye Terrier is one of the UK's most endangered native dog breeds — there are more giant pandas alive than Skye Terriers registered annually in recent years. That rarity is worth understanding before anything else, because it shapes the ownership experience: finding a reputable breeder, a vet familiar with the breed, and a community of knowledgeable owners all require real effort.\n\n"
            "The personality is quintessential terrier with an overlay of real devotion. Skyes are known for bonding intensely to one person — Greyfriars Bobby, the Skye who stayed at his owner's grave for 14 years, is the most famous expression of this loyalty. They're cautious with strangers and will take their time making up their minds about new people."
        ),
        'health_lifespan_narrative': (
            "Skye Terriers typically live 12–14 years. The breed's most distinctive health concern is premature closure of the distal radius — a growth plate issue that can cause permanent limb deformity if puppies are overexerted or exposed to hard surfaces before 8–10 months of age. This shapes how puppies must be managed from day one.\n\n"
            "Hemangiosarcoma — an aggressive cancer of blood vessel walls — occurs at higher rates in Skyes than in the broader dog population and is worth being aware of in aging dogs. Mammary tumors also appear at elevated rates, making spaying relevant for females not intended for breeding."
        ),
        'nutrition_narrative': (
            "Skyes are moderate in their dietary needs and don't require anything unusual. Keeping them at a healthy weight is important given their long body and short legs — the bone and joint stresses that come with excess weight matter here.\n\n"
            "During puppyhood specifically, diet that supports appropriate growth without overnutrition matters because of the growth plate concerns noted above. Your vet should be part of puppy nutrition planning for this breed."
        ),
        'family_fit_narrative': (
            "Skye Terriers generally do best in adult households or homes with older, respectful children. The intense personal loyalty they form isn't always compatible with the unpredictable energy of young kids. They're terriers, which means the hunting instinct is present — small pets aren't a natural fit.\n\n"
            "For the right owner — patient, consistent, and willing to do the work of finding this breed through a reputable source — the relationship is exceptionally rewarding. Skyes are loyal to a degree that few breeds match."
        ),
        'honest_take_narrative': (
            "The Skye Terrier requires a certain kind of commitment before you even get the dog: finding one. This is a breed with fewer than 50 puppies registered in the UK in some recent years. If you can't find a reputable breeder, the answer is to wait, not to compromise.\n\n"
            "What you get for that effort is a dog of real character — quiet dignity, deep loyalty, and enough independence that the relationship has texture. The long coat is not a low-maintenance situation. But for people who fall for this breed, all of it is part of the point."
        ),
    },
    'Vizsla': {
        'breed_name': 'Vizsla',
        'primary_role': 'Sporting',
        'physical_activity_needs': 'Very High',
        'mental_stimulation_needs': 'High',
        'size': 'Medium',
        'grooming_needs': 'Low',
        'trainability': 'Easy',
        'good_for_beginners': 'With Experience',
        'apartment_friendly': 'No',
        'temperament_narrative': (
            "The Vizsla is sometimes called a 'velcro dog,' and the description is accurate in a way that's both charming and worth taking seriously. This is a dog that was bred for all-day close work in the field alongside a human partner, and that intense human-orientation doesn't turn off at home.\n\n"
            "They're affectionate, gentle, and genuinely sensitive — harsh training methods backfire badly with Vizslas, who respond to positive reinforcement with remarkable eagerness. They're also high-energy in a way that's different from a Husky's chaos: more focused, athletic, and purposeful about wanting an outlet."
        ),
        'health_lifespan_narrative': (
            "Vizslas typically live 12–15 years, which is notably good for a medium-to-large athletic breed. Hip dysplasia appears in the breed but at relatively modest rates. Epilepsy and hypothyroidism both occur in Vizslas and are worth monitoring.\n\n"
            "Overall, this is a healthy breed, and the lifespan reflects it. The bigger health risk for Vizslas is often behavioral — separation anxiety can cause genuine distress and stress-related health issues if the dog's need for companionship isn't taken seriously."
        ),
        'nutrition_narrative': (
            "Vizslas are athletic and active, and their caloric needs reflect that — especially if they're doing fieldwork or serious daily exercise. Quality protein is the foundation, and don't underestimate how much they need when genuinely active.\n\n"
            "Like other deep-chested athletic breeds, bloat is a real risk. Smaller meals rather than one large feeding, and avoiding exercise immediately after eating, are sensible precautions worth building into routine."
        ),
        'family_fit_narrative': (
            "Vizslas are excellent family dogs for active households — gentle with children, affectionate, and social in a way that suits family life. Their need to be involved in everything makes them naturally integrating into family routines rather than living on the periphery.\n\n"
            "The separation anxiety concern is real and worth taking seriously for families where the dog would be alone for eight or more hours regularly. This is not a breed that does well crated all day — they need company, exercise, and engagement."
        ),
        'honest_take_narrative': (
            "The Vizsla's primary challenge isn't training or aggression — it's neediness in the best sense. This dog wants to be with you constantly, and that's genuine love but it's also a demand. Separation anxiety in Vizslas isn't just crying at the door; it can be serious and requires active management.\n\n"
            "For runners, hikers, hunters, or anyone whose life has room for a highly athletic, emotionally engaged companion, the Vizsla is remarkable. For households where the dog would be alone most of the day, this isn't the right match — and being honest about that before getting one saves the dog and the owner from a difficult situation."
        ),
    },
    'Weimaraner': {
        'breed_name': 'Weimaraner',
        'primary_role': 'Sporting',
        'physical_activity_needs': 'Very High',
        'mental_stimulation_needs': 'High',
        'size': 'Large',
        'grooming_needs': 'Low',
        'trainability': 'Easy',
        'good_for_beginners': 'Not Recommended',
        'apartment_friendly': 'No',
        'temperament_narrative': (
            "The Weimaraner is sometimes called the 'Gray Ghost' — and not just for the coat. There's an intensity and attentiveness to the breed that can feel almost uncanny: they watch you closely, anticipate your movements, and insert themselves into whatever you're doing with a focused energy that doesn't go away.\n\n"
            "They're friendly and affectionate with family but can be aloof or assertive with strangers and other dogs if not well-socialized. They're not beginner dogs — they have real opinions and will test boundaries in ways that require consistent, experienced handling."
        ),
        'health_lifespan_narrative': (
            "Weimaraners typically live 11–13 years. Bloat (gastric dilatation-volvulus) is a significant risk in this deep-chested breed and is worth understanding before ownership — it's a life-threatening emergency requiring immediate veterinary care. Prophylactic gastropexy at the time of spay or neuter is an option some owners choose and worth discussing with a vet.\n\n"
            "Hip dysplasia occurs at moderate rates. Hypothyroidism and spinal dysraphism — a rare but breed-specific neurological condition — also appear. Health testing from breeders matters with Weimaraners."
        ),
        'nutrition_narrative': (
            "Feeding structure matters with Weimaraners specifically because of bloat risk. Multiple smaller meals rather than one large one, and no intense exercise in the hour before or after eating, are the standard recommendations.\n\n"
            "Beyond that, they're active dogs with real caloric needs. Quality food matters, and the amounts should reflect actual activity level — a Weimaraner getting serious daily exercise needs significantly more than a dog getting walks."
        ),
        'family_fit_narrative': (
            "Weimaraners are good with children they're raised with but are too energetic and exuberant for households with toddlers — a full-speed Weimaraner is a significant physical force, even with no bad intentions. For active families with school-age or older children, they can be excellent companions.\n\n"
            "The prey drive is real — smaller pets require management. The energy and intensity require an outlet; a bored Weimaraner will find one, and you won't like what it picks."
        ),
        'honest_take_narrative': (
            "The Weimaraner is a lot of dog for most households, and the people who flourish with them understand that going in. This is a dog that needs genuine work — daily running, hunting, structured activity — and will tell you when it hasn't gotten enough by redecorating.\n\n"
            "For active owners who want an athletic, focused, loyal companion and have the time and space to channel that energy, the Weimaraner is one of the great breeds. For everyone else: the beautiful gray coat fools people into thinking this is a calm, elegant pet. It's an athlete that happens to be gray."
        ),
    },
    'Whippet': {
        'breed_name': 'Whippet',
        'primary_role': 'Racing, Companion',
        'physical_activity_needs': 'Moderate',
        'mental_stimulation_needs': 'Moderate',
        'size': 'Medium',
        'grooming_needs': 'Low',
        'trainability': 'Moderate',
        'good_for_beginners': 'Yes',
        'apartment_friendly': 'With Enough Exercise',
        'temperament_narrative': (
            "The Whippet is frequently described as the most practical sighthound, and the description is earned. You get the grace, speed, and elegance of the greyhound family in a medium-sized package that's genuinely gentle indoors, good with families, and easygoing about daily life in a way that the breed's athletic capacity wouldn't suggest.\n\n"
            "They're affectionate without being demanding about it — pleasant, quiet, and unobtrusive in the house for most of the day, then capable of 35 miles per hour in a straight line when the moment calls for it. The switch between the two modes is part of the Whippet's particular appeal."
        ),
        'health_lifespan_narrative': (
            "Whippets typically live 12–15 years and are among the healthier breeds relative to their size. Like all sighthounds, they have very low body fat and metabolize anesthesia differently — any vet performing a procedure should know this.\n\n"
            "Mitral valve disease appears at modest rates in older dogs and is worth monitoring. They're sensitive to cold and often genuinely need a coat in winter, which is not affectation on the dog's part. Hip and joint problems are less common here than in many comparable breeds."
        ),
        'nutrition_narrative': (
            "Whippets are lean and should stay that way — their build isn't padded, and extra weight changes their movement, their joint load, and their health over time. A visually bony dog is often a correctly conditioned Whippet, not an underfed one.\n\n"
            "They're efficient in the sighthound way and don't need enormous amounts of food for their size. Quality over quantity, and resist the well-meaning impulse to add weight to a dog that looks thin by non-sighthound standards."
        ),
        'family_fit_narrative': (
            "Whippets are one of the most genuinely family-friendly sighthounds. They're gentle with children, easygoing with other dogs, and calm enough indoors to be compatible with a wide range of households — including apartments if the exercise requirement is genuinely met.\n\n"
            "The prey drive is real and recall off-leash is unreliable once something triggers it, which is consistent across the sighthound family. Small animals are at risk. But compared to many breeds in their speed class, Whippets are remarkably adaptable to family life."
        ),
        'honest_take_narrative': (
            "The Whippet is consistently underrated, and that's genuinely the honest take: this is one of the best all-around medium dogs available, and it's less popular than it deserves to be because it doesn't come with a dramatic personality or breed story.\n\n"
            "Low-shed, low-drama, low-noise indoors, moderate exercise needs, good with families, good with other dogs — and then occasionally a 35 mph reminder that there's an athlete in there. If you've been considering a Greyhound but aren't sure about the size or commitment, the Whippet is frequently the answer to that question."
        ),
    },
}

SCALE_BADGE = {'Low': 'badge-low', 'Moderate': 'badge-moderate', 'High': 'badge-high', 'Very High': 'badge-very-high'}
TRAINABILITY_BADGE = {'Easy': 'badge-yes', 'Moderate': 'badge-moderate', 'Independent-Minded': 'badge-with-exp'}
BEGINNER_BADGE = {'Yes': 'badge-yes', 'With Experience': 'badge-with-exp', 'Not Recommended': 'badge-no'}
APARTMENT_BADGE = {'Yes': 'badge-yes', 'With Enough Exercise': 'badge-with-exp', 'No': 'badge-no'}

# ── Write profiles to Excel ──────────────────────────────────────────────────
wb = openpyxl.load_workbook('dog_facts_7.3.2026.xlsx')
ws = wb['deep_dive_profiles']
headers = [ws.cell(1, c).value for c in range(1, 15)]

for title, p in PROFILES.items():
    row_vals = [p.get(h) for h in headers]
    ws.append(row_vals)
    print(f'Profile written: {title}')

wb.save('dog_facts_7.3.2026.xlsx')
print()

# Re-load profiles dict keyed by lowercase name
profiles = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0]:
        profiles[row[0].lower()] = dict(zip(headers, row))

PAGE_CSS = """\
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #FAF0DC;
      font-family: Georgia, "Times New Roman", serif;
      color: #3D2B1F;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: #5C3D11;
      color: #FAF0DC;
      text-align: center;
      padding: 18px 24px 14px;
    }
    header h1 {
      font-size: 4rem;
      letter-spacing: 0.04em;
      font-weight: normal;
    }
    header .subtitle {
      font-size: 0.85rem;
      color: #D4B483;
      margin-top: 4px;
      font-style: italic;
    }

    .site-nav {
      background: #4A2E0A;
      display: flex;
      justify-content: center;
      gap: 4px;
      padding: 0 12px;
      flex-wrap: wrap;
    }
    .site-nav a {
      color: #C8A87A;
      text-decoration: none;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 0.82rem;
      padding: 9px 20px;
      display: inline-block;
      letter-spacing: 0.03em;
      border-bottom: 2px solid transparent;
      transition: color 0.15s, border-color 0.15s;
    }
    .site-nav a:hover,
    .site-nav a.active {
      color: #FAF0DC;
      border-bottom-color: #C05621;
    }

    .main {
      flex: 1;
      max-width: 680px;
      width: 100%;
      margin: 0 auto;
      padding: 28px 20px 40px;
      display: flex;
      flex-direction: column;
      gap: 22px;
    }

    .deep-hero {
      text-align: center;
      padding: 8px 0 4px;
    }
    .deep-hero h2 {
      font-size: 2.4rem;
      font-weight: normal;
      color: #5C3D11;
      letter-spacing: 0.04em;
    }
    .breed-tagline {
      font-size: 0.95rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 6px;
    }
    .deep-dives-label {
      display: inline-block;
      font-size: 0.7rem;
      background: #5C3D11;
      color: #D4B483;
      padding: 3px 10px;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 10px;
    }

    .breadcrumb {
      font-size: 0.82rem;
    }
    .breadcrumb a {
      color: #C05621;
      text-decoration: none;
    }
    .breadcrumb a:hover { text-decoration: underline; }

    .stat-panel {
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 22px 26px 26px;
      box-shadow: 0 2px 8px rgba(92,61,17,0.10);
    }
    .panel-heading {
      font-size: 0.78rem;
      color: #7A4F2A;
      font-style: italic;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      margin-bottom: 18px;
    }
    .stat-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px 12px;
    }
    .stat-item {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }
    .stat-label {
      font-size: 0.64rem;
      color: #9A6B3A;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      line-height: 1.4;
    }
    .stat-badge {
      display: inline-block;
      font-size: 0.78rem;
      font-weight: bold;
      padding: 4px 10px;
      border-radius: 20px;
      line-height: 1.35;
      width: fit-content;
    }

    .badge-low      { background: #E4CFA0; color: #4A2E0A; }
    .badge-moderate { background: #C8A870; color: #3D2B1F; }
    .badge-high     { background: #C05621; color: #FFF8EC; }
    .badge-very-high{ background: #5C3D11; color: #FAF0DC; }
    .badge-neutral  { background: #7A4F2A; color: #FAF0DC; }
    .badge-yes      { background: #6B7C45; color: #F5F0E8; }
    .badge-with-exp { background: #B8880A; color: #FFF8EC; }
    .badge-no       { background: #8B3A1A; color: #FAF0DC; }

    .narrative-section {
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 28px 30px;
      box-shadow: 0 2px 8px rgba(92,61,17,0.12);
      overflow: hidden;
    }
    .narrative-heading {
      font-size: 0.78rem;
      color: #7A4F2A;
      font-style: italic;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      margin-bottom: 14px;
    }
    .narrative-body {
      font-size: 1.05rem;
      line-height: 1.78;
      color: #3D2B1F;
    }
    .narrative-body p + p {
      margin-top: 14px;
    }

    .narrative-img {
      float: right;
      width: 150px;
      margin: 4px 0 14px 18px;
      border-radius: 8px;
      border: 2px solid #E0C090;
      box-shadow: 0 2px 8px rgba(92,61,17,0.12);
      display: block;
    }

    .narrative-section.honest-take {
      border-left: 4px solid #C05621;
    }
    .narrative-section.honest-take .narrative-heading {
      color: #C05621;
    }

    @media (max-width: 520px) {
      header h1 { font-size: 2.8rem; }
      .stat-grid { grid-template-columns: repeat(2, 1fr); gap: 12px 10px; }
      .stat-badge { font-size: 0.74rem; }
      .narrative-img {
        float: none;
        display: block;
        width: 180px;
        margin: 0 auto 16px;
      }
    }

    footer {
      background: #5C3D11;
      color: #A07840;
      text-align: center;
      font-size: 0.78rem;
      padding: 10px;
    }"""


def paras(text):
    parts = [p.strip() for p in text.strip().split('\n\n') if p.strip()]
    return '\n      '.join(f'<p>{p}</p>' for p in parts)


def build_page(slug, title, tagline, photo, p):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} &mdash; Deep Dive &mdash; The Bark Facts</title>
  <style>
{PAGE_CSS}
  </style>
</head>
<body>

<header>
  <h1>The Bark Facts</h1>
  <div class="subtitle">one fact, one dog, one day at a time</div>
</header>
<nav class="site-nav">
  <a href="../index.html">Home</a>
  <a href="../breeds/index.html">Browse Facts</a>
  <a href="index.html" class="active">Breeds</a>
</nav>

<div class="main">

  <div class="deep-hero">
    <div class="deep-dives-label">Deep Dive</div>
    <h2>{title}</h2>
    <p class="breed-tagline">{tagline}</p>
  </div>

  <div class="breadcrumb">
    <a href="../index.html">&#8592; Back to Home</a>
    &nbsp;&middot;&nbsp;
    <a href="index.html">&#8592; Back to Breeds</a>
    &nbsp;&middot;&nbsp;
    <a href="../breeds/{slug}.html">See Breed Facts Page</a>
  </div>

  <!-- Quick-Glance Panel -->
  <section class="stat-panel">
    <div class="panel-heading">Quick Glance</div>
    <div class="stat-grid">

      <div class="stat-item">
        <div class="stat-label">Primary Role</div>
        <span class="stat-badge badge-neutral">{p['primary_role']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Physical Activity Needs</div>
        <span class="stat-badge {SCALE_BADGE[p['physical_activity_needs']]}">{p['physical_activity_needs']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Mental Stimulation Needs</div>
        <span class="stat-badge {SCALE_BADGE[p['mental_stimulation_needs']]}">{p['mental_stimulation_needs']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Size</div>
        <span class="stat-badge badge-neutral">{p['size']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Grooming Needs</div>
        <span class="stat-badge {SCALE_BADGE[p['grooming_needs']]}">{p['grooming_needs']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Trainability</div>
        <span class="stat-badge {TRAINABILITY_BADGE[p['trainability']]}">{p['trainability']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Good For Beginners</div>
        <span class="stat-badge {BEGINNER_BADGE[p['good_for_beginners']]}">{p['good_for_beginners']}</span>
      </div>

      <div class="stat-item">
        <div class="stat-label">Apartment Friendly</div>
        <span class="stat-badge {APARTMENT_BADGE[p['apartment_friendly']]}">{p['apartment_friendly']}</span>
      </div>

    </div>
  </section>

  <!-- Temperament -->
  <section class="narrative-section">
    <div class="narrative-heading">Temperament</div>
    <div class="narrative-body">
      <img class="narrative-img" src="../images/{photo}" alt="{title}" />
      {paras(p['temperament_narrative'])}
    </div>
  </section>

  <!-- Health & Lifespan -->
  <section class="narrative-section">
    <div class="narrative-heading">Health &amp; Lifespan</div>
    <div class="narrative-body">
      {paras(p['health_lifespan_narrative'])}
    </div>
  </section>

  <!-- Nutrition Needs -->
  <section class="narrative-section">
    <div class="narrative-heading">Nutrition Needs</div>
    <div class="narrative-body">
      {paras(p['nutrition_narrative'])}
    </div>
  </section>

  <!-- Family Fit -->
  <section class="narrative-section">
    <div class="narrative-heading">Family Fit</div>
    <div class="narrative-body">
      {paras(p['family_fit_narrative'])}
    </div>
  </section>

  <!-- The Honest Take -->
  <section class="narrative-section honest-take">
    <div class="narrative-heading">The Honest Take</div>
    <div class="narrative-body">
      {paras(p['honest_take_narrative'])}
    </div>
  </section>

</div>

<footer>Dog Facts &mdash; a fun project</footer>

</body>
</html>
"""


# ── Build pages ──────────────────────────────────────────────────────────────
for slug, title, tagline, photo, _teaser in BREEDS:
    profile_key = title.lower()
    profile = profiles[profile_key]
    with open(f'deep-dives/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(build_page(slug, title, tagline, photo, profile))
    print(f'Built: deep-dives/{slug}.html')


# ── Full alphabetical index — 53 breeds ─────────────────────────────────────
ALL_CARDS = [
    ('akita',                 'Akita',                 'A dignified, one-family dog &mdash; loyal on its own terms and no one else&rsquo;s.'),
    ('alaskan-malamute',      'Alaskan Malamute',      'Tundra-bred strength and a friendly face &mdash; hiding an escape artist underneath.'),
    ('australian-shepherd',   'Australian Shepherd',   'The velcro herding dog &mdash; extraordinary partner if you can keep up.'),
    ('basenji',               'Basenji',               'The barkless dog &mdash; independent, cat-like, and very much on its own terms.'),
    ('basset-hound',          'Basset Hound',          'Low to the ground, high on vibes &mdash; a forgiving breed with a stubborn streak.'),
    ('beagle',                'Beagle',                'Nose-led, food-motivated, and louder than expected &mdash; loveable with caveats.'),
    ('bichon-frise',          'Bichon Frise',          'Small, cheerful, and low-shed &mdash; but that coat is a real commitment.'),
    ('bloodhound',            'Bloodhound',            'The world&rsquo;s best nose attached to a sweet, stubborn, drool-forward dog.'),
    ('border-collie',         'Border Collie',         'Extraordinary intelligence with extraordinary demands &mdash; not for the low-key household.'),
    ('borzoi',                'Borzoi',                'Serene indoors, electric on a trail &mdash; and that coat needs real upkeep.'),
    ('boxer',                 'Boxer',                 'Looks tough, acts goofy &mdash; a demanding dog that&rsquo;s easy to underestimate.'),
    ('brussels-griffon',      'Brussels Griffon',      'A velcro companion in a tiny, opinionated package &mdash; more emotionally demanding than it looks.'),
    ('bull-terrier',          'Bull Terrier',          'The class clown with a stubborn streak &mdash; funny until training gets ignored.'),
    ('bulldog',               'Bulldog',               'The original couch potato &mdash; charming, low-key, and carrying real health tradeoffs.'),
    ('chihuahua',             'Chihuahua',             'Tiny body, outsized personality &mdash; needs real training despite the small packaging.'),
    ('chow-chow',             'Chow Chow',             'Reserved, serious, and deeply independent &mdash; not a dog for everyone.'),
    ('corgi',                 'Corgi',                 'A working dog in a footstool&rsquo;s body &mdash; more demanding than the memes suggest.'),
    ('dachshund',             'Dachshund',             'A surprisingly bold hunting dog in a hot-dog shape &mdash; that spine needs protecting.'),
    ('dalmatian',             'Dalmatian',             'The endurance athlete behind the Disney image &mdash; demanding and diet-specific.'),
    ('doberman',              'Doberman',              'Loyal, sensitive, and misunderstood &mdash; the real challenge is cardiac health, not temperament.'),
    ('english-toy-spaniel',   'English Toy Spaniel',   'A calm, devoted companion &mdash; genuinely easy to live with, with health caveats worth knowing.'),
    ('finnish-lapphund',      'Finnish Lapphund',      'A friendly, trainable Arctic breed &mdash; sociable, vocal, and surprisingly easygoing.'),
    ('german-shepherd',       'German Shepherd',       'One of the most capable breeds alive &mdash; and exactly why it ends up in the wrong hands.'),
    ('great-dane',            'Great Dane',            'Room-filling loyalty and a shorter run together than you&rsquo;d like.'),
    ('great-pyrenees',        'Great Pyrenees',        'An independent livestock guardian &mdash; the nighttime barking and stubbornness are features, not bugs.'),
    ('greyhound',             'Greyhound',             'Gentle at home, electric outside &mdash; and more apartment-friendly than you&rsquo;d think.'),
    ('irish-terrier',         'Irish Terrier',         'A fearless, loyal terrier &mdash; small enough to underestimate, bold enough to make that a mistake.'),
    ('irish-wolfhound',       'Irish Wolfhound',       'An ancient gentle giant &mdash; the lifespan is short and worth sitting with before committing.'),
    ('jack-russell-terrier',  'Jack Russell Terrier',  'One of the most demanding small breeds alive &mdash; not the apartment dog the size suggests.'),
    ('japanese-chin',         'Japanese Chin',         'A calm, elegant toy breed &mdash; easier than it looks, with health caveats worth knowing.'),
    ('kerry-blue-terrier',    'Kerry Blue Terrier',    'A versatile working terrier &mdash; the grooming commitment surprises people expecting a low-maintenance dog.'),
    ('leonberger',            'Leonberger',            'A gentle giant with genuine warmth &mdash; and all the giant-breed tradeoffs that come with it.'),
    ('lhasa-apso',            'Lhasa Apso',            'An ancient sentinel breed with real independence underneath the flowing coat &mdash; not just a lap dog.'),
    ('mastiff',               'Mastiff',               'The gentle giant of gentle giants &mdash; the temperament is easy, the physical realities are not.'),
    ('newfoundland',          'Newfoundland',          'Genuinely one of the best dogs with children &mdash; the coat, drool, and size are the honest caveats.'),
    ('norwegian-elkhound',    'Norwegian Elkhound',    'An ancient, vocal Nordic hunter &mdash; loyal to family, loud about everything else.'),
    ('otterhound',            'Otterhound',            'One of the rarest breeds alive &mdash; a boisterous, water-loving hound that needs serious exercise.'),
    ('papillon',              'Papillon',              'An underrated toy breed &mdash; genuinely trainable, athletic, and nothing like the fragile lap dog it looks.'),
    ('pekingese',             'Pekingese',             'Ancient palace companion &mdash; the flat face is a real health consideration, not just a look.'),
    ('pointer',               'Pointer',               'A stamina athlete built for all-day field work &mdash; not a casual-exercise breed.'),
    ('poodle',                'Poodle',                'The intelligent athlete behind the show-dog reputation &mdash; demanding, trainable, and not low-maintenance.'),
    ('portuguese-water-dog',  'Portuguese Water Dog',  'An athletic, water-loving working dog &mdash; needs more than a walk to be genuinely content.'),
    ('pug',                   'Pug',                   'Genuinely charming &mdash; and the brachycephalic health realities are just as real as the personality.'),
    ('rottweiler',            'Rottweiler',            'A misunderstood, deeply loyal family dog &mdash; the work is socialization, not managing aggression.'),
    ('saint-bernard',         'Saint Bernard',         'The gentle giant rescue dog &mdash; patient with everyone, less so about personal space.'),
    ('saluki',                'Saluki',                'One of the oldest breeds alive &mdash; ancient grace, ancient prey drive, and an unreliable recall.'),
    ('samoyed',               'Samoyed',               'The smiling sled dog &mdash; genuinely wonderful, as long as you&rsquo;re committed to the coat.'),
    ('shiba-inu',             'Shiba Inu',             'Japan&rsquo;s most popular dog &mdash; independent, clean, and deeply uninterested in your commands.'),
    ('siberian-husky',        'Siberian Husky',        'Built for 100-mile Arctic slogs &mdash; your suburb isn&rsquo;t going to tire this dog out.'),
    ('skye-terrier',          'Skye Terrier',          'One of Britain&rsquo;s rarest native breeds &mdash; deeply loyal and genuinely unusual.'),
    ('vizsla',                'Vizsla',                'The velcro sporting dog &mdash; athletic, sensitive, and constitutionally unable to be more than 3 feet away.'),
    ('weimaraner',            'Weimaraner',            'The Gray Ghost &mdash; a focused, intense athlete that people routinely underestimate.'),
    ('whippet',               'Whippet',               'The most underrated sighthound &mdash; fast, gentle, low-maintenance, and genuinely great for most households.'),
]

cards_html = '\n'.join(
    f'    <a class="dive-card" href="{slug}.html">\n'
    f'      <div>\n'
    f'        <div class="dive-card-name">{name}</div>\n'
    f'        <div class="dive-card-teaser">{teaser}</div>\n'
    f'      </div>\n'
    f'      <span class="dive-card-arrow">&#8594;</span>\n'
    f'    </a>'
    for slug, name, teaser in ALL_CARDS
)

idx_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Deep Dives &mdash; The Bark Facts</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #FAF0DC;
      font-family: Georgia, "Times New Roman", serif;
      color: #3D2B1F;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: #5C3D11;
      color: #FAF0DC;
      text-align: center;
      padding: 18px 24px 14px;
    }
    header h1 {
      font-size: 4rem;
      letter-spacing: 0.04em;
      font-weight: normal;
    }
    header .subtitle {
      font-size: 0.85rem;
      color: #D4B483;
      margin-top: 4px;
      font-style: italic;
    }

    .site-nav {
      background: #4A2E0A;
      display: flex;
      justify-content: center;
      gap: 4px;
      padding: 0 12px;
      flex-wrap: wrap;
    }
    .site-nav a {
      color: #C8A87A;
      text-decoration: none;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 0.82rem;
      padding: 9px 20px;
      display: inline-block;
      letter-spacing: 0.03em;
      border-bottom: 2px solid transparent;
      transition: color 0.15s, border-color 0.15s;
    }
    .site-nav a:hover,
    .site-nav a.active {
      color: #FAF0DC;
      border-bottom-color: #C05621;
    }

    .main {
      flex: 1;
      max-width: 680px;
      width: 100%;
      margin: 0 auto;
      padding: 36px 20px 20px;
      display: flex;
      flex-direction: column;
      gap: 28px;
    }

    .page-heading {
      text-align: center;
    }
    .page-heading h2 {
      font-size: 1.9rem;
      font-weight: normal;
      color: #5C3D11;
    }
    .page-heading p {
      font-size: 0.9rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 6px;
      line-height: 1.6;
    }

    .dive-grid {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .dive-card {
      background: #FFF8EC;
      border: 2px solid #E0C090;
      border-radius: 10px;
      padding: 20px 24px;
      text-decoration: none;
      color: #3D2B1F;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(92,61,17,0.10);
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    .dive-card:hover {
      border-color: #C05621;
      box-shadow: 0 3px 12px rgba(192,86,33,0.18);
    }
    .dive-card-name {
      font-size: 1.2rem;
      color: #5C3D11;
    }
    .dive-card-teaser {
      font-size: 0.8rem;
      color: #9A6B3A;
      font-style: italic;
      margin-top: 3px;
    }
    .dive-card-arrow {
      color: #C05621;
      font-size: 1.1rem;
    }

    .breadcrumb {
      font-size: 0.82rem;
    }
    .breadcrumb a {
      color: #C05621;
      text-decoration: none;
    }
    .breadcrumb a:hover { text-decoration: underline; }

    footer {
      background: #5C3D11;
      color: #A07840;
      text-align: center;
      font-size: 0.78rem;
      padding: 10px;
    }
  </style>
</head>
<body>

<header>
  <h1>The Bark Facts</h1>
  <div class="subtitle">one fact, one dog, one day at a time</div>
</header>
<nav class="site-nav">
  <a href="../index.html">Home</a>
  <a href="../breeds/index.html">Browse Facts</a>
  <a href="index.html" class="active">Breeds</a>
</nav>

<div class="main">

  <div class="page-heading">
    <h2>Deep Dives</h2>
    <p>Beyond the facts &mdash; temperament, health, nutrition, and an honest take<br>on what it&rsquo;s actually like to live with these dogs.</p>
  </div>

  <div class="dive-grid">

CARDS_PLACEHOLDER

  </div>

  <div class="breadcrumb"><a href="../index.html">&#8592; Back to Home</a></div>

</div>

<footer>Dog Facts &mdash; a fun project</footer>

</body>
</html>
"""

idx_html = idx_html.replace('CARDS_PLACEHOLDER', cards_html)
with open('deep-dives/index.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)
print('Updated: deep-dives/index.html')

# ── Add CTA to breed pages ───────────────────────────────────────────────────
CTA_HTML = '<a class="deep-dive-cta" href="../deep-dives/{slug}.html">There&rsquo;s more to this dog than facts. Deep dive &rarr;</a>'

for slug, title, _tagline, _photo, _teaser in BREEDS:
    path = f'breeds/{slug}.html'
    content = open(path, encoding='utf-8').read()
    if f'../deep-dives/{slug}.html' in content:
        print(f'CTA already present: {path}')
        continue
    cta = CTA_HTML.format(slug=slug)
    new_content = content.replace('</div>\n</body>', f'{cta}\n</div>\n</body>', 1)
    if new_content == content:
        new_content = content.replace('</div>\n\n</body>', f'{cta}\n</div>\n\n</body>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'CTA added: {path}')

print('\nAll done.')
