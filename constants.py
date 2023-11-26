ALPHABET_DEFAULT = "abcdefghijklmnopqrstuvwxyz"
DAY_DEFAULT = None
END_PAGE_DEFAULT = -1
MEMBERS_DEFAULT = False
PRICE_KEY_REGEX = "average180.*Date\('(.*)'\).*"
PRICE_VAL_REGEX = "average180.*\), (.*?),"
UNITS_KEY_REGEX = "trade180.*Date\('(.*)'\).*"
UNITS_VAL_REGEX = "trade180.*\), (.*)]"
REQUEST_TIMER_DEFAULT = 3
START_PAGE_DEFAULT = 1
VERBOSE_DEFAULT = 0
OPTIONS_DEFAULT = {
	"ALPHABET": ALPHABET_DEFAULT
	, "DAY": DAY_DEFAULT
	, "END_PAGE": END_PAGE_DEFAULT
	, "MEMBERS": MEMBERS_DEFAULT
	, "REQUEST_TIMER": REQUEST_TIMER_DEFAULT
	, "START_PAGE": START_PAGE_DEFAULT
	, "VERBOSE": VERBOSE_DEFAULT
}

OSRS_API_ROUTES = {
  "base": "http://services.runescape.com/m=itemdb_oldschool",
  "endpoints": {
    "catalog": {
      "url": "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/items.json?category=1&alpha={name}&page={page}",
      "keys": [ "alpha", "page" ]
    },
    "detail": {
      "url": "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={itemid}",
      "keys": [ "item" ]
    },
    "graph": {
      "url": "https://secure.runescape.com/m=itemdb_oldschool/api/graph/{itemid}.json",
      "keys": [ "item" ]
    },
    "count": {
      "url": "https://secure.runescape.com/m=itemdb_oldschool/{name}/viewitem?obj={itemid}",
      "keys": [ "alpha", "item" ]
    },
    "limits": {
      "url": "http://oldschoolrunescape.wikia.com/wiki/Grand_Exchange/Buying_limits"
    }
  },
  "placeholders": {
    "item": "{itemid}",	
    "page": "{page}",
    "alpha": "{name}"
  }
}

BUY_LIMITS = {
"Abyssal bludgeon": "8",
 "Abyssal dagger": "8",
 "Abyssal whip": "70",
 "Acorn": "200",
 "Adamant arrow": "11000",
 "Adamant arrowtips": "10000",
 "Adamant axe": "40",
 "Adamant battleaxe": "125",
 "Adamant bolts": "11000",
 "Adamant bolts(unf)": "13000",
 "Adamant cane": "3",
 "Adamant crossbow": "40",
 "Adamant dart": "11000",
 "Adamant dart tip": "11000",
 "Adamant full helm": "125",
 "Adamant med helm": "125",
 "Adamant javelin": "11000",
 "Adamant pickaxe": "40",
 "Adamant platebody": "125",
 "Adamant platelegs": "125",
 "Adamant plateskirt": "125",
 "Adamantite bar": "10000",
 "Adamantite ore": "4500",
 "Ahrim's robetop": "15",
 "Air battlestaff": "14000",
 "Air orb": "10000",
 "Air rune": "20000",
 "Air tiara": "40",
 "Amethyst arrow": "11000",
 "Amethyst bolt tips": "11000",
 "Amulet of accuracy": "5",
 "Amulet of fury": "8",
 "Amulet of glory": "10000",
 "Amulet of power": "125",
 "Amulet of strength": "125",
 "Amulet of torture": "8",
 "Amylase crystal": "11000",
 "Ancestral hat": "8",
 "Ancestral robe bottom": "8",
 "Ancestral robe top": "8",
 "Antidote++": "4000",
 "Antifire potion": "2000",
 "Anti-venom+(4)": "2000",
 "Arcane prayer scroll": "8",
 "Archer helm": "70",
 "Archers ring": "8",
 "Archery ticket": "18000",
 "Armadyl chainskirt": "8",
 "Armadyl chestplate": "8",
 "Armadyl godsword": "8",
 "Armadyl helmet": "8",
 "Arrow shaft": "7000",
 "Ashes": "13000",
 "Astral rune": "10000",
 "Avantoe": "2000",
 "Avantoe potion (unf)": "10000",
 "Bandos boots": "8",
 "Bandos chestplate": "8",
 "Bandos godsword": "8",
 "Bandos tassets": "8",
 "Barrows equipment": "10 (or 15)",
 "Battlestaff": "11000",
 "Berserker helm": "70",
 "Berserker ring": "8",
 "Big bones": "3000",
 "Bird snare": "250",
 "Black axe": "40",
 "Black chinchompa": "11000",
 "Black d'hide body": "70",
 "Black d'hide chaps": "70",
 "Black dragonhide": "10000",
 "Black Mask": "10",
 "Black Mask (10)": "15",
 "Black pickaxe": "40",
 "Black salamander": "125",
 "Blessed body": "8",
 "Blessed boots": "8",
 "Blessed chaps": "8",
 "Blessed spirit shield": "8",
 "Blessed vambraces": "8",
 "Blood rune": "10000",
 "Blue d'hide body": "125",
 "Blue d'hide chaps": "125",
 "Blue d'hide vamb": "125",
 "Blue dragon leather": "13000",
 "Blue dragonhide": "13000",
 "Blue wizard robe": "250",
 "Body rune": "12000",
 "Body tiara": "40",
 "Bolt rack": "11000",
 "Bone bolts": "11000",
 "Bones": "3000",
 "Bow string": "13000",
 "Box trap": "250",
 "Bread": "6000",
 "Brine sabre": "8",
 "Broad bolts": "7000",
 "Bronze 2h sword": "125",
 "Bronze arrow": "7000",
 "Bronze axe": "40",
 "Bronze dart": "7000",
 "Bronze dart tip": "13000",
 "Bronze halberd": "15",
 "Bronze pickaxe": "40",
 "Bronze plateskirt": "125",
 "Bucket": "13000",
 "Bucket of milk": "13000",
 "Bucket of sand": "13000",
 "Bullseye lantern (unf)": "299+",
 "Burning amulet": "5000",
 "Cabbage": "6000",
 "Cadantine": "2000",
 "Cannonball": "7000",
 "Calquat Tree Seed": "200",
 "Combat bracelet(6)": "100",
 "Chaos rune": "12000",
 "Chef's hat": "150",
 "Chinchompa": "7000",
 "Chocolate bar": "13000",
 "Chocolate dust": "13000",
 "Christmas cracker": "50",
 "Clay": "13000",
 "Climbing boots": "15",
 "Coal": "13000",
 "Coif": "125",
 "Compost": "600",
 "Compost potion": "50",
 "Cooked karambwan": "10000",
 "Copper ore": "13000",
 "Cosmic rune": "12000",
 "Cowhide": "10000",
 "Craw's bow (u)": "8",
 "Crushed nest": "11000",
 "Cup of Tea": "2000",
 "Dagannoth bones": "7500",
 "Dark bow": "8",
 "Dark fishing bait": "8000",
 "Dart tips": "11000",
 "Death rune": "10000",
 "Dexterous prayer scroll": "8",
 "Dharok's armour set": "8",
 "Diamond bolt tips": "11000",
 "Disk of returning": "5",
 "Draconic visage": "5",
 "Dragon 2h sword": "8",
 "Dragon arrow": "11000",
 "Dragon axe": "40",
 "Dragon battleaxe": "70",
 "Dragon bones": "7500",
 "Dragon boots": "70",
 "Dragon chainbody": "70",
 "Dragon claws": "8",
 "Dragon dagger": "70",
 "Dragon dart": "11000",
 "Dragon full helm": "8",
 "Dragon halberd": "70",
 "Dragon harpoon": "5",
 "Dragon hunter crossbow": "8",
 "Dragon javelin": "10000",
 "Dragon javelin heads": "11000",
 "Dragon longsword": "70",
 "Dragon mace": "70",
 "Dragon med helm": "8",
 "Dragon pickaxe": "40",
 "Dragon platebody": "70",
 "Dragon platelegs": "70",
 "Dragon plateskirt": "70",
 "Dragon scimitar": "70",
 "Dragon scimitar ornament kit": "5",
 "Dragon spear": "70",
 "Dragon sword": "8",
 "Dragon warhammer": "8",
 "Dragonbone necklace": "8",
 "Dragonfire shield": "8",
 "Dragonstone bolt tips": "11000",
 "Dragonstone bolts (e)": "11000",
 "Dust rune": "12000",
 "Dwarf weed": "2000",
 "Earth battlestaff": "14000",
 "Earth rune": "20000",
 "Earth tiara": "40",
 "Easter egg": "50",
 "Eclectic impling jar": "18000",
 "Elder maul": "8",
 "Energy potion": "2000",
 "Ensouled dragon head": "9000",
 "Eternal boots": "15",
 "Eternal crystal": "10",
 "Eye of newt": "13000",
 "Feather": "13000",
 "Stripy Feather": "8000",
 "Filled plant pot": "600",
 "Fire battlestaff": "14000",
 "Fire rune": "20000",
 "Fishing bait": "8000",
 "Flax": "13000",
 "Flowers": "250",
 "Frozen whip mix": "4",
 "Fury ornament kit": "4",
 "Gilded platebody": "8",
 "Gilded platelegs": "8",
 "Gilded scimitar": "70",
 "Glassblowing pipe": "40",
 "Goblin mail": "15",
 "God pages": "5",
 "Gold amulet (u)": "18000",
 "Gold bar": "10000",
 "Gold bracelet": "18000",
 "Gold ore": "13000",
 "Granite gloves": "8",
 "Granite maul": "70",
 "Grapes": "13000",
 "Green d'hide body": "125",
 "Green d'hide chaps": "125",
 "Green d'hide vamb": "125",
 "Green dragonhide": "13000",
 "Green dye": "150",
 "Grimy avantoe": "11000",
 "Grimy cadantine": "11000",
 "Grimy dwarf weed": "11000",
 "Grimy guam leaf": "11000",
 "Grimy harralander": "11000",
 "Grimy irit leaf": "11000",
 "Grimy kwuarm": "11000",
 "Grimy lantadyme": "11000",
 "Grimy marrentill": "11000",
 "Grimy ranarr weed": "11000",
 "Grimy snapdragon": "11000",
 "Grimy tarromin": "11000",
 "Grimy toadflax": "11000",
 "Grimy torstol": "11000",
 "Guam leaf": "11000",
 "Guardian Boots": "8",
 "Halloween masks": "5",
 "Hammer": "40",
 "Hard leather": "10000",
 "Hardleather body": "125",
 "Harralander": "12000",
 "Harralander tar": "11000",
 "Headless arrow": "7000",
 "Heavy ballista": "8",
 "Helm of neitiznot": "70",
 "High level herbs": "2000",
 "Holiday items": "5",
 "Holy elixir": "4",
 "Imbued heart": "8",
 "Impling jar": "13000",
 "Infinity boots": "24",
 "Infinity bottoms": "10",
 "Infinity hat": "10",
 "Inoculation bracelet": "505",
 "Irit leaf": "2000",
 "Iron 2h sword": "125",
 "Iron arrow": "7000",
 "Iron axe": "40",
 "Iron bar": "10000",
 "Iron dart": "7000",
 "Iron knife": "7000",
 "Iron ore": "13000",
 "Iron pickaxe": "40",
 "Iron kiteshield": "125",
 "Iron platebody": "125",
 "Iron platelegs": "125",
 "Jug": "13000",
 "Jug of water": "13000",
 "Jug of wine": "6000",
 "Justiciar chestguard": "8",
 "Justiciar legguards": "8",
 "Kraken tentacle": "70",
 "Kwuarm": "13000",
 "Kwuarm potion (unf)": "10000",
 "Lantadyme": "2000",
 "Lava battlestaff": "8",
 "Lava rune": "12000",
 "Lava scale shard": "11000",
 "Law rune": "12000",
 "Leaf-bladed battleaxe": "70",
 "Leaf-bladed sword": "70",
 "Leather": "10000",
 "Leather body": "125",
 "Leather chaps": "125",
 "Leather cowl": "125",
 "Leather gloves": "125",
 "Leather vambraces": "125",
 "Limpwurt root": "13000",
 "Limpwurt seed": "600",
 "Light Ballista": "8",
 "Lizardman fang": "13000",
 "Lobster": "6000",
 "Logs": "15000",
 "Longbow": "14000",
 "Loop half of key": "11000",
 "Low level herbs": "13000",
 "Mage's book": "15",
 "Magic fang": "5",
 "Magic logs": "12000",
 "Magic longbow": "18000",
 "Magic longbow (u)": "10000",
 "Magic sapling": "200",
 "Magic seed": "200",
 "Malediction ward": "8",
 "Manta Ray": "10000",
 "Mahogany logs": "11000",
 "Mahogany plank": "13000",
 "Maple logs": "15000",
 "Maple longbow": "14000",
 "Maple longbow (u)": "10000",
 "Maple seed": "200",
 "Maple shortbow (u)": "10000",
 "Marrentill": "11000",
 "Mind rune": "12000",
 "Mind tiara": "40",
 "Mist rune": "12000",
 "Mithril 2h sword": "125",
 "Mithril arrow": "7000",
 "Mithril axe": "40",
 "Mithril bar": "10000",
 "Mithril battleaxe": "125",
 "Mithril bolts (unf)": "13000",
 "Mithril chainbody": "100",
 "Mithril claws": "125",
 "Mithril dart": "7000",
 "Mithril dart tip": "13000",
 "Mithril full helm": "125",
 "Mithril kiteshield": "125",
 "Mithril knife": "7000",
 "Mithril med helm": "125",
 "Mithril ore": "13000",
 "Mithril pickaxe": "40",
 "Mithril platebody": "125",
 "Mithril platelegs": "125",
 "Mithril plateskirt": "125",
 "Mithril scimitar": "125",
 "Mithril spear": "125",
 "Mithril warhammer": "125",
 "Mole claw": "50",
 "Mole skin": "50",
 "Molten glass": "13000",
 "Monk's robe": "125",
 "Monk's robe top": "125",
 "Monkfish": "13000",
 "Mort myre fungus": "13000",
 "Mud rune": "12000",
 "Mysterious emblem": "100",
 "Mystic hat": "125",
 "Mystic lava staff": "8",
 "Mystic mist staff": "6",
 "Mystic robe bottom": "125",
 "Mystic robe top": "125",
 "Mystic smoke staff": "6",
 "Mystic steam staff": "6",
 "Nature rune": "12000",
 "Necklace of anguish": "8",
 "Oak logs": "15000",
 "Oak longbow": "14000",
 "Oak plank": "13000",
 "Obsidian cape": "70",
 "Obsidian helmet": "10",
 "Obsidian platelegs": "70",
 "Occult necklace": "8",
 "Odium ward": "8",
 "Old School Bond": "40",
 "Onyx bolts": "11000",
 "Opal": "10000",
 "Opal bolt tips": "11000",
 "Ogre arrow shaft": "5000",
 "Palm sapling": "200",
 "Palm tree seed": "200",
 "Papaya tree seed": "200",
 "Partyhats": "5",
 "Pegasian boots": "8",
 "Pegasian crystal": "15",
 "Pie dish": "500",
 "Pineapple": "13000",
 "Plank": "13000",
 "Prayer potion": "2000",
 "Primordial boots": "15",
 "Primordial crystal": "10",
 "Pure essence": "20000",
 "Purple sweets": "10000",
 "Ranarr seed": "200",
 "Ranarr weed": "12000",
 "Ranger boots": "6",
 "Ranger gloves": "8",
 "Rangers' tunic": "4",
 "Ranging potion": "2000",
 "Raw beef": "13000",
 "Raw lobster": "15000",
 "Raw monkfish": "13000",
 "Raw salmon": "15000",
 "Raw shark": "15000",
 "Raw swordfish": "15000",
 "Raw tuna": "15000",
 "Raw karambwan": "13000",
 "Red chinchompa": "7000",
 "Red d'hide body": "70",
 "Red d'hide chaps": "70",
 "Red d'hide vamb": "70",
 "Red dragonhide": "10000",
 "Red spider's eggs": "13000",
 "Redwood logs": "12000",
 "Redwood shield": "125",
 "Regen bracelet": "10",
 "Revenant ether": "30000",
 "Ring of the gods": "8",
 "Ring of recoil": "10000",
 "Ring of stone": "8",
 "Ring of suffering": "8",
 "Robin hood hat": "8",
 "Rope": "250",
 "Ruby bolt tips": "11000",
 "Ruby bolts": "11000",
 "Rune 2h sword": "70",
 "Rune armour set (lg)": "8",
 "Rune armour set (sk)": "8",
 "Rune arrow": "11000",
 "Rune arrowtips": "10000",
 "Rune axe": "40",
 "Rune battleaxe": "70",
 "Rune boots": "70",
 "Rune chainbody": "70",
 "Rune claws": "70",
 "Rune crossbow": "70",
 "Rune dagger": "70",
 "Rune dart": "7000",
 "Rune dart tip": "11000",
 "Rune full helm": "70",
 "Rune halberd": "70",
 "Rune hasta": "70",
 "Rune javelin": "11000",
 "Rune javelin heads": "10000",
 "Rune kiteshield": "70",
 "Rune kiteshield (g)": "8",
 "Rune knife": "7000",
 "Rune longsword": "70",
 "Rune mace": "70",
 "Rune med helm": "70",
 "Rune pickaxe": "40",
 "Rune platebody": "70",
 "Rune platelegs": "70",
 "Rune plateskirt": "70",
 "Rune scimitar": "70",
 "Rune spear": "70",
 "Rune sq shield": "70",
 "Rune sword": "70",
 "Rune thrownaxe": "70",
 "Rune warhammer": "70",
 "Runite bolts": "11000",
 "Runite ore": "4500",
 "Santa hat": "5",
 "Sapphire": "13000",
 "Sapphire ring": "10000",
 "Saradomin brew": "2000",
 "Saradomin godsword": "8",
 "Saradomin sword": "8",
 "Scythe of vitur (uncharged)": "8",
 "Seaweed": "13000",
 "Seercull": "8",
 "Seers ring": "8",
 "Serpentine helm": "8",
 "Serpentine visage": "5",
 "Shark": "10000",
 "Shrimps": "15000",
 "Silk": "18000",
 "Silver bar": "10000",
 "Silver sickle": "15",
 "Skeletal visage": "8",
 "Smoke rune": "12000",
 "Snakeskin body": "125",
 "Snakeskin boots": "100",
 "Snakeskin chaps": "125",
 "Snapdragon": "2000",
 "Snapdragon seed": "200",
 "Soda ash": "13000",
 "Soft clay": "13000",
 "Soul rune": "10000",
 "Spectral spirit shield": "8",
 "Spirit shield": "8",
 "Splitbark body": "70",
 "Splitbark boots": "70",
 "Splitbark gauntlets": "70",
 "Splitbark helm": "70",
 "Splitbark legs": "70",
 "Spotted cape": "125",
 "Staff of the dead": "8",
 "Stamina potion": "2000",
 "Steam battlestaff": "8",
 "Steam rune": "12000",
 "Steel arrow": "7000",
 "Steel arrowtips": "10000",
 "Steel axe": "40",
 "Steel bar": "10000",
 "Steel chainbody": "125",
 "Steel dagger": "125",
 "Steel dart": "7000",
 "Steel hasta": "125",
 "Steel knife": "7000",
 "Steel kiteshield": "125",
 "Steel longsword": "125",
 "Steel pickaxe": "40",
 "Steel platebody": "125",
 "Steel platelegs": "125",
 "Steel scimitar": "125",
 "Steel warhammer": "125",
 "Stew": "10000",
 "Strength potion": "2000",
 "Super attack": "2000",
 "Super defence": "2000",
 "Super energy": "2000",
 "Super potion set": "2000",
 "Super restore": "2000",
 "Super strength": "2000",
 "Supercompost": "600",
 "Superior dragon bones": "7500",
 "Swamp tar": "13000",
 "Sweetcorn seed": "600",
 "Swordfish": "6000",
 "Tanzanite fang": "5",
 "Tarromin": "13000",
 "Tarromin tar": "7000",
 "Teak plank": "13000",
 "Team cape": "150",
 "Thread": "7000",
 "Tin ore": "13000",
 "Toadflax": "12000",
 "Toadflax seed": "600",
 "Tome of fire": "15",
 "Tooth half of key": "11000",
 "Tormented bracelet": "8",
 "Torstol": "2000",
 "Toxic blowpipe": "8",
 "Trading sticks": "18000",
 "Treasonous ring": "8",
 "Trident of the seas (full)": "8",
 "Tuna": "6000",
 "Twisted buckler": "8",
 "Tyrannical ring": "8",
 "Uncut diamond": "10000",
 "Uncut emerald": "10000",
 "Uncut ruby": "10000",
 "Uncut sapphire": "10000",
 "Unfinished broad bolts": "7000",
 "Unpowered orb": "10000",
 "Varrock teleport": "10000",
 "Vial": "13000",
 "Vial of blood": "2000",
 "Vial of water": "13000",
 "Volcanic whip mix": "6",
 "Warrior helm": "70",
 "Warrior ring": "8",
 "Water battlestaff": "14000",
 "Water rune": "20000",
 "Watering can": "40",
 "Watermelon": "11000",
 "Watermelon seed": "200",
 "Whiteberry seed": "200",
 "Willow logs": "15000",
 "Willow longbow": "14000",
 "Willow seed": "200",
 "Wine of zamorak": "10000",
 "Wrath rune": "10000",
 "Wyvern bones": "7500",
 "Xerician hat": "124",
 "Xerician robes": "124",
 "Xerician top": "124",
 "Yak-hide armour (legs)": "70",
 "Yak-hide armour (top)": "70",
 "Yew logs": "12000",
 "Yew longbow": "18000",
 "Yew longbow (u)": "10000",
 "Yew shortbow": "125",
 "Yew shortbow (u)": "10000",
 "Zamorak godsword": "8",
 "Zamorak monk bottom": "15",
 "Zamorak monk top": "15",
 "Zamorakian hasta": "8",
 "Zamorakian spear": "8",
 "Zul-andra teleport": "10000",
 "Zulrah's scales": "30000"
 }
