import json

extra_facts = [
    ("Breeds",   "The Lhasa Apso was bred by Tibetan monks as an indoor sentinel dog — it would bark to alert the larger Tibetan Mastiff guard dogs of any intruders approaching the monastery.", "lhasa apso"),
    ("Breeds",   "The Leonberger was bred in the 1840s in Leonberg, Germany, with the goal of creating a dog that resembled the lion on the town's coat of arms.", "leonberger"),
    ("Breeds",   "The Otterhound has webbed feet and a rough, double coat that repels water — traits bred specifically for hunting otters along riverbanks in medieval England.", "otterhound"),
    ("Breeds",   "The Pekingese was so revered in imperial China that commoners were required to bow to the breed — and theft of one was punishable by death.", "pekingese"),
    ("Breeds",   "The Brussels Griffon was a favorite pet of Belgian Queen Marie Henriette in the late 1800s, which helped launch the breed's popularity across Europe.", "brussels griffon"),
    ("Breeds",   "The Kerry Blue Terrier is the national dog of Ireland, named for County Kerry where it was developed as an all-purpose farm dog for hunting, herding, and guarding.", "kerry blue terrier"),
    ("Breeds",   "The Japanese Chin was historically given as a gift between Japanese and Korean royalty, and was considered a symbol of aristocratic status in ancient Japan.", "japanese chin"),
    ("Breeds",   "The Borzoi — also known as the Russian Wolfhound — was bred by Russian aristocrats to course wolves across the open steppe, hunting in pairs or trios.", "borzoi"),
    ("Breeds",   "The Norwegian Elkhound is one of the oldest Spitz breeds, used by Vikings for hunting elk, bear, and moose and as a loyal companion on longship voyages.", "norwegian elkhound"),
    ("Breeds",   "The Skye Terrier was a favorite of Mary, Queen of Scots — one of her dogs reportedly refused to leave her side even after her execution in 1587.", "skye terrier"),
    ("Breeds",   "The Irish Wolfhound was so prized in ancient Ireland that Gaelic law set strict limits on how many could be owned based on rank — only kings could own six.", "irish wolfhound"),
    ("History",  "The Iditarod Trail Sled Dog Race in Alaska commemorates a famous 1925 relay in which sled dog teams delivered life-saving diphtheria antitoxin to Nome across 674 miles of frozen wilderness.", None),
    ("Behavior", "Dogs have been observed bringing their owners gifts — including toys, sticks, or household objects — as a form of greeting or to share their excitement.", None),
    ("Sensory",  "Dogs can hear the ultrasonic frequencies emitted by rodents — a range completely inaudible to humans — which is part of why they are such effective ratters.", None),
    ("Behavior", "Dogs use play bows — stretching the front legs forward and lowering the chest — as a universal signal to other dogs and humans that what follows is just play.", None),
    ("Health",   "Dogs who live with active owners walk more, weigh less, and visit the vet less often — studies show dog ownership directly improves human physical fitness levels too.", None),
    ("Culture",  "The first dog show ever held took place in Newcastle upon Tyne, England, in June 1859, with only Pointers and Setters competing.", None),
]

with open('E:/ClaudeCode/dog_facts/dog_facts.json', encoding='utf-8') as f:
    facts_data = json.load(f)

start_num = max(f['fact_number'] for f in facts_data['facts']) + 1

for i, (category, fact_text, breed) in enumerate(extra_facts):
    facts_data['facts'].append({
        'fact_number': start_num + i,
        'category': category,
        'fact': fact_text,
        'breed': breed,
    })

with open('E:/ClaudeCode/dog_facts/dog_facts.json', 'w', encoding='utf-8') as f:
    json.dump(facts_data, f, indent=2, ensure_ascii=False)

total = len(facts_data['facts'])
print(f"Added {len(extra_facts)} more facts (#{start_num}–#{start_num+len(extra_facts)-1})")
print(f"Total facts in file: {total}")
