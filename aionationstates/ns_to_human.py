from collections import namedtuple


ScaleInfo = namedtuple('ScaleInfo', ('id title ranked gradation'
                                     ' region_description nation_description'))

census_info = {
    0: ScaleInfo(
        id=0,
        title='Civil Rights',
        ranked='Most Extensive Civil Rights',
        gradation='Martin Luther King, Jr. Units',
        nation_description=('The citizens of nations ranked highly enjoy a '
                            'great amount of civil rights, or freedoms to '
                            'go about their personal business without '
                            'interference or regulation from government.'),
        region_description=('The citizens of regions ranked highly enjoy a '
                            'great amount of civil rights, or freedoms to '
                            'go about their personal business without '
                            'interference or regulation from government.'),
    ),
    1: ScaleInfo(
        id=1,
        title='Economy',
        ranked='Most Efficient Economies',
        gradation='Krugman-Greenspan Business Outlook Index',
        nation_description=('Nations ranked highly are the most ruthlessly '
                            'efficient at translating raw resources, '
                            'including people, into economic output.'),
        region_description=('Regions ranked highly are the most ruthlessly '
                            'efficient at translating raw resources, '
                            'including people, into economic output.'),
    ),
    2: ScaleInfo(
        id=2,
        title='Political Freedom',
        ranked='Most Politically Free',
        gradation='Diebold Election Inking Scale',
        nation_description=('These nations allow citizens the greatest '
                            'amount of freedom to select their own '
                            'government.'),
        region_description=('These regions allow citizens the greatest '
                            'amount of freedom to select their own '
                            'government.'),
    ),
    3: ScaleInfo(
        id=3,
        title='Population',
        ranked='Largest Populations',
        gradation='Capita',
        nation_description=('The following nations have the greatest '
                            'number of citizens.'),
        region_description=('The following regions have the most citizens '
                            'per nation.'),
    ),
    4: ScaleInfo(
        id=4,
        title='Wealth Gaps',
        ranked='Greatest Rich-Poor Divides',
        gradation='Rich To Poor Income Ratio',
        nation_description=('Nations ranked highly have large gaps between '
                            'the incomes of rich and poor citizens. '
                            'Nations low on the list have high levels of '
                            'income equality.'),
        region_description=('Regions ranked highly have large gaps between '
                            'the incomes of rich and poor citizens. '
                            'Regions low on the list have high levels of '
                            'income equality.'),
    ),
    5: ScaleInfo(
        id=5,
        title='Death Rate',
        ranked='Highest Unexpected Death Rate',
        gradation='Bus Surprisal Index',
        nation_description=('The World Census paid their respects at '
                            'cemeteries in order to determine how likely '
                            'citizens were to die each year from unnatural '
                            'causes, such as crime, preventable illness, '
                            'accident, and government encouragement.'),
        region_description=('The World Census paid their respects at '
                            'cemeteries in order to determine how likely '
                            'citizens were to die each year from unnatural '
                            'causes, such as crime, preventable illness, '
                            'accident, and government encouragement.'),
    ),
    6: ScaleInfo(
        id=6,
        title='Compassion',
        ranked='Most Compassionate Citizens',
        gradation='Kitten Softness Rating',
        nation_description=('Exhaustive World Census tests involving '
                            'kittens revealed the following nations to be '
                            'the most compassionate.'),
        region_description=('Exhaustive World Census tests involving '
                            'kittens revealed the following regions to be '
                            'the most compassionate.'),
    ),
    7: ScaleInfo(
        id=7,
        title='Eco-Friendliness',
        ranked='Most Eco-Friendly Governments',
        gradation='Dolphin Recycling Awareness Index',
        nation_description=('The following governments spend the greatest '
                            'amounts on environmental issues. This may not '
                            'always be reflected in the quality of that '
                            "nation's environment."),
        region_description=('The following governments spend the greatest '
                            'amounts on environmental issues. This may not '
                            'always be reflected in the quality of that '
                            "region's environment."),
    ),
    8: ScaleInfo(
        id=8,
        title='Social Conservatism',
        ranked='Most Conservative',
        gradation='Bush-Santorum Dawning Terror Index',
        nation_description=('Citizens in nations ranked highly tend to '
                            'have greater restrictions placed on what they '
                            'may do in their personal lives, whether via '
                            'community values or government-imposed law.'),
        region_description=('Citizens in regions ranked highly tend to '
                            'have greater restrictions placed on what they '
                            'may do in their personal lives, whether via '
                            'community values or government-imposed law.'),
    ),
    9: ScaleInfo(
        id=9,
        title='Nudity',
        ranked='Nudest',
        gradation='Cheeks Per Square Mile',
        nation_description=('After exhaustive surveys, the World Census '
                            'calculated which nations have the greatest '
                            'acreages of flesh on public display.'),
        region_description=('After exhaustive surveys, the World Census '
                            'calculated which regions have the greatest '
                            'acreages of flesh on public display.'),
    ),
    10: ScaleInfo(
        id=10,
        title='Industry: Automobile Manufacturing',
        ranked='Largest Automobile Manufacturing Sector',
        gradation='Henry Ford Productivity Index',
        nation_description=('World Census analysts extensively tested '
                            'concept muscle cars in empty parking lots in '
                            'order to estimate which nations have the '
                            'largest auto industries.'),
        region_description=('World Census analysts extensively tested '
                            'concept muscle cars in empty parking lots in '
                            'order to estimate which regions have the '
                            'largest auto industries.'),
    ),
    11: ScaleInfo(
        id=11,
        title='Industry: Cheese Exports',
        ranked='Largest Cheese Export Sector',
        gradation='Mozzarella Productivity Index',
        nation_description=('Qualified World Census Cheese Masters nibbled '
                            'their way across the globe to determine which '
                            'nations have the most developed cheese '
                            'exports.'),
        region_description=('Qualified World Census Cheese Masters nibbled '
                            'their way across the globe to determine which '
                            'regions have the most developed cheese '
                            'exports.'),
    ),
    12: ScaleInfo(
        id=12,
        title='Industry: Basket Weaving',
        ranked='Largest Basket Weaving Sector',
        gradation='Hickory Productivity Index',
        nation_description=('World Census agents infiltrated a variety of '
                            'out-of-the-way towns and festivals in order '
                            'to determine which nations have the most '
                            'developed Basket Weaving industries.'),
        region_description=('World Census agents infiltrated a variety of '
                            'out-of-the-way towns and festivals in order '
                            'to determine which regions have the most '
                            'developed Basket Weaving industries.'),
    ),
    13: ScaleInfo(
        id=13,
        title='Industry: Information Technology',
        ranked='Largest Information Technology Sector',
        gradation='Fann-Boi Productivity Index',
        nation_description=('World Census staff compiled lists over Smart '
                            'Phone related traffic accidents to determine '
                            'which nations have the largest Information '
                            'Technology industries.'),
        region_description=('World Census staff compiled lists over Smart '
                            'Phone related traffic accidents to determine '
                            'which regions have the largest Information '
                            'Technology industries.'),
    ),
    14: ScaleInfo(
        id=14,
        title='Industry: Pizza Delivery',
        ranked='Largest Pizza Delivery Sector',
        gradation='Pepperoni Propulsion Productivity Index',
        nation_description=('World Census staff spent many nights '
                            'answering the front door in order to measure '
                            'which nations have the biggest Pizza Delivery '
                            'industries.'),
        region_description=('World Census staff spent many nights '
                            'answering the front door in order to measure '
                            'which regions have the biggest Pizza Delivery '
                            'industries.'),
    ),
    15: ScaleInfo(
        id=15,
        title='Industry: Trout Fishing',
        ranked='Largest Trout Fishing Sector',
        gradation='Nemo Depletion Efficiency Index',
        nation_description=('The World Census conducted frenzied haggling '
                            'with fishmongers in order to determine which '
                            'nations have the largest fishing industries.'),
        region_description=('The World Census conducted frenzied haggling '
                            'with fishmongers in order to determine which '
                            'regions have the largest fishing industries.'),
    ),
    16: ScaleInfo(
        id=16,
        title='Industry: Arms Manufacturing',
        ranked='Largest Arms Manufacturing Sector',
        gradation='Charon Conveyancy Index',
        nation_description=('World Census special forces intercepted '
                            'crates of smuggled weapons to determine which '
                            'nations have the largest arms industry.'),
        region_description=('World Census special forces intercepted '
                            'crates of smuggled weapons to determine which '
                            'regions have the largest arms industry.'),
    ),
    17: ScaleInfo(
        id=17,
        title='Sector: Agriculture',
        ranked='Largest Agricultural Sector',
        gradation='Mu-Bah-Daggs Productivity Index',
        nation_description=('World Census bean-counters on horseback '
                            'guided herds of cattle to slaughter in order '
                            'to determine which nations have the largest '
                            'agricultural sectors.'),
        region_description=('World Census bean-counters on horseback '
                            'guided herds of cattle to slaughter in order '
                            'to determine which regions have the largest '
                            'agricultural sectors.'),
    ),
    18: ScaleInfo(
        id=18,
        title='Industry: Beverage Sales',
        ranked='Largest Soda Pop Sector',
        gradation='Addison-Fukk Productivity Rating',
        nation_description=('The World Census recorded sales of fizzy '
                            'syrup water in order to determine which '
                            'nations have the largest beverage industries.'),
        region_description=('The World Census recorded sales of fizzy '
                            'syrup water in order to determine which '
                            'regions have the largest beverage industries.'),
    ),
    19: ScaleInfo(
        id=19,
        title='Industry: Timber Woodchipping',
        ranked='Largest Timber Woodchipping Industry',
        gradation='Tasmanian Pulp Environmental Export Index',
        nation_description=('The World Census measured the rate of '
                            'desertification in order to calculate which '
                            'nations have the largest timber industry.'),
        region_description=('The World Census measured the rate of '
                            'desertification in order to calculate which '
                            'regions have the largest timber industry.'),
    ),
    20: ScaleInfo(
        id=20,
        title='Industry: Mining',
        ranked='Largest Mining Sector',
        gradation='Blue Sky Asbestos Index',
        nation_description=('World Census experts measured the volume of '
                            'stuff removed from the ground to determine '
                            'which nations have the largest mining '
                            'industries.'),
        region_description=('World Census experts measured the volume of '
                            'stuff removed from the ground to determine '
                            'which regions have the largest mining '
                            'industries.'),
    ),
    21: ScaleInfo(
        id=21,
        title='Industry: Insurance',
        ranked='Largest Insurance Industry',
        gradation='Risk Expulsion Effectiveness Rating',
        nation_description=('The World Census posed as door-to-door '
                            'salespeople in order to establish which '
                            'nations have the most extensive Insurance '
                            'industries.'),
        region_description=('The World Census posed as door-to-door '
                            'salespeople in order to establish which '
                            'regions have the most extensive Insurance '
                            'industries.'),
    ),
    22: ScaleInfo(
        id=22,
        title='Industry: Furniture Restoration',
        ranked='Largest Furniture Restoration Industry',
        gradation='Spitz-Pollish Productivity Index',
        nation_description=('World Census analysts spend quiet weekends in '
                            'the countryside in order to determine which '
                            'nations have the largest Furniture '
                            'Restoration industries.'),
        region_description=('World Census analysts spend quiet weekends in '
                            'the countryside in order to determine which '
                            'regions have the largest Furniture '
                            'Restoration industries.'),
    ),
    23: ScaleInfo(
        id=23,
        title='Industry: Retail',
        ranked='Largest Retail Industry',
        gradation='Shrinkwrap Consignment Productivity Index',
        nation_description=('The World Census estimated levels of employee '
                            'ennui to determine which nations have the '
                            'largest retail industries.'),
        region_description=('The World Census estimated levels of employee '
                            'ennui to determine which regions have the '
                            'largest retail industries.'),
    ),
    24: ScaleInfo(
        id=24,
        title='Industry: Book Publishing',
        ranked='Largest Publishing Industry',
        gradation='Bella Potter Productivity e-Index',
        nation_description=('The World Census tallied social media '
                            'complaints from students regarding overpriced '
                            'textbooks to determine which nations have the '
                            'largest book publishing industries.'),
        region_description=('The World Census tallied social media '
                            'complaints from students regarding overpriced '
                            'textbooks to determine which regions have the '
                            'largest book publishing industries.'),
    ),
    25: ScaleInfo(
        id=25,
        title='Industry: Gambling',
        ranked='Largest Gambling Industry',
        gradation='Kelly Criterion Productivity Index',
        nation_description=('The World Census tailed known underworld '
                            'figures in order to determine which nations '
                            'have the largest gambling industries.'),
        region_description=('The World Census tailed known underworld '
                            'figures in order to determine which regions '
                            'have the largest gambling industries.'),
    ),
    26: ScaleInfo(
        id=26,
        title='Sector: Manufacturing',
        ranked='Largest Manufacturing Sector',
        gradation='Gooback-Jerbs Productivity Index',
        nation_description=('World Census bean-counters tabulated data '
                            'from across several industries in order to '
                            'determine which nations have the largest '
                            'Manufacturing sectors.'),
        region_description=('World Census bean-counters tabulated data '
                            'from across several industries in order to '
                            'determine which regions have the largest '
                            'Manufacturing sectors.'),
    ),
    27: ScaleInfo(
        id=27,
        title='Government Size',
        ranked='Largest Governments',
        gradation='Bureaucratic Comprehensiveness Rating Scale Index',
        nation_description=('World Census agents lined up at public '
                            'agencies around the world in order to study '
                            'the extent of government in nations, taking '
                            'into consideration economic output, social '
                            'and cultural significance, and raw size.'),
        region_description=('World Census agents lined up at public '
                            'agencies around the world in order to study '
                            'the extent of government in regions, taking '
                            'into consideration economic output, social '
                            'and cultural significance, and raw size.'),
    ),
    28: ScaleInfo(
        id=28,
        title='Welfare',
        ranked='Largest Welfare Programs',
        gradation='Safety Net Mesh Density Rating',
        nation_description=('Governments ranked highly spend the most on '
                            'social welfare programs. Nations ranked low '
                            'tend to have weak or non-existent government '
                            'welfare.'),
        region_description=('Governments ranked highly spend the most on '
                            'social welfare programs. Regions ranked low '
                            'tend to have weak or non-existent government '
                            'welfare.'),
    ),
    29: ScaleInfo(
        id=29,
        title='Public Healthcare',
        ranked='Most Extensive Public Healthcare',
        gradation='Theresa-Nightingale Rating',
        nation_description=('World Census interns were infected with '
                            'obscure diseases in order to test which '
                            'nations had the most effective and '
                            'well-funded public healthcare facilities.'),
        region_description=('World Census interns were infected with '
                            'obscure diseases in order to test which '
                            'regions had the most effective and '
                            'well-funded public healthcare facilities.'),
    ),
    30: ScaleInfo(
        id=30,
        title='Law Enforcement',
        ranked='Most Advanced Law Enforcement',
        gradation='Orwell Orderliness Index',
        nation_description=('World Census interns were framed for minor '
                            'crimes in order to measure the response '
                            'times, effectiveness, and amount of firepower '
                            'deployed by the law enforcement agencies of '
                            'different nations.'),
        region_description=('World Census interns were framed for minor '
                            'crimes in order to measure the response '
                            'times, effectiveness, and amount of firepower '
                            'deployed by the law enforcement agencies of '
                            'different regions.'),
    ),
    31: ScaleInfo(
        id=31,
        title='Business Subsidization',
        ranked='Most Subsidized Industry',
        gradation='Gilded Widget Scale',
        nation_description=('Nations ranked highly spend the most on '
                            'developing and supporting industry, a '
                            "practice known as 'corporate welfare.'"),
        region_description=('Regions ranked highly spend the most on '
                            'developing and supporting industry, a '
                            "practice known as 'corporate welfare.'"),
    ),
    32: ScaleInfo(
        id=32,
        title='Religiousness',
        ranked='Most Devout',
        gradation='Prayers Per Hour',
        nation_description=('World Census Inquisitors conducted rigorous '
                            'one-on-one interviews probing the depth of '
                            "citizens' beliefs in order to determine which "
                            'nations were the most devout.'),
        region_description=('World Census Inquisitors conducted rigorous '
                            'one-on-one interviews probing the depth of '
                            "citizens' beliefs in order to determine which "
                            'regions were the most devout.'),
    ),
    33: ScaleInfo(
        id=33,
        title='Income Equality',
        ranked='Most Income Equality',
        gradation='Marx-Engels Emancipation Scale',
        nation_description=('World Census boffins calculated the '
                            'difference in incomes between the richest and '
                            'poorest citizens, where a score of 50 would '
                            'mean that poor incomes are 50% of rich '
                            'incomes.'),
        region_description=('World Census boffins calculated the '
                            'difference in incomes between the richest and '
                            'poorest citizens, where a score of 50 would '
                            'mean that poor incomes are 50% of rich '
                            'incomes.'),
    ),
    34: ScaleInfo(
        id=34,
        title='Niceness',
        ranked='Nicest Citizens',
        gradation='Average Smiles Per Day',
        nation_description=('World Census sociology experts studied '
                            'citizens from various nations to determine '
                            'which seemed most friendly and concerned for '
                            'others.'),
        region_description=('World Census sociology experts studied '
                            'citizens from various regions to determine '
                            'which seemed most friendly and concerned for '
                            'others.'),
    ),
    35: ScaleInfo(
        id=35,
        title='Rudeness',
        ranked='Rudest Citizens',
        gradation='Insults Per Minute',
        nation_description=('World Census experts telephoned citizens from '
                            'all nations at just before dinner time, in a '
                            'study to determine which populations were '
                            'most brash, rude, or brusque.'),
        region_description=('World Census experts telephoned citizens from '
                            'all regions at just before dinner time, in a '
                            'study to determine which populations were '
                            'most brash, rude, or brusque.'),
    ),
    36: ScaleInfo(
        id=36,
        title='Intelligence',
        ranked='Smartest Citizens',
        gradation='Quips Per Hour',
        nation_description=('The World Census eavesdropped on '
                            'conversations in coffee shops, on campuses, '
                            'and around cinemas in order to determine '
                            'which nations have the most quick-witted, '
                            'insightful, and knowledgeable citizens.'),
        region_description=('The World Census eavesdropped on '
                            'conversations in coffee shops, on campuses, '
                            'and around cinemas in order to determine '
                            'which regions have the most quick-witted, '
                            'insightful, and knowledgeable citizens.'),
    ),
    37: ScaleInfo(
        id=37,
        title='Ignorance',
        ranked='Most Ignorant Citizens',
        gradation='Missed References Per Hour',
        nation_description=('The World Census studied which nations seemed '
                            'to have the greatest numbers of citizens that '
                            'fell into the categories "ignorant," '
                            '"oblivious," or "just plain dumb."'),
        region_description=('The World Census studied which regions seemed '
                            'to have the greatest numbers of citizens that '
                            'fell into the categories "ignorant," '
                            '"oblivious," or "just plain dumb."'),
    ),
    38: ScaleInfo(
        id=38,
        title='Political Apathy',
        ranked='Most Politically Apathetic Citizens',
        gradation='Whatever',
        nation_description=('These results were determined by seeing how '
                            'many citizens of each nation answered a '
                            'recent World Census survey on the local '
                            'political situation by ticking the "Don\'t '
                            'Give a Damn" box.'),
        region_description=('These results were determined by seeing how '
                            'many citizens of each region answered a '
                            'recent World Census survey on the local '
                            'political situation by ticking the "Don\'t '
                            'Give a Damn" box.'),
    ),
    39: ScaleInfo(
        id=39,
        title='Health',
        ranked='Healthiest Citizens',
        gradation='Bananas Ingested Per Day',
        nation_description=('A measure of the general physical health of '
                            'citizens in each nation.'),
        region_description=('A measure of the general physical health of '
                            'citizens in each region.'),
    ),
    40: ScaleInfo(
        id=40,
        title='Cheerfulness',
        ranked='Most Cheerful Citizens',
        gradation='Percentage Of Water Glasses Perceived Half-Full',
        nation_description=('The World Census shared cheeky grins with '
                            'citizens around the world in order to '
                            'determine which were the most relentlessly '
                            'cheerful.'),
        region_description=('The World Census shared cheeky grins with '
                            'citizens around the world in order to '
                            'determine which were the most relentlessly '
                            'cheerful.'),
    ),
    41: ScaleInfo(
        id=41,
        title='Weather',
        ranked='Best Weather',
        gradation='Meters Of Sunlight',
        nation_description=('The following nations were determined to have '
                            'the best all-round weather.'),
        region_description=('The following regions were determined to have '
                            'the best all-round weather.'),
    ),
    42: ScaleInfo(
        id=42,
        title='Compliance',
        ranked='Lowest Crime Rates',
        gradation='Law-abiding Acts Per Hour',
        nation_description=('World Census agents attempted to lure '
                            'citizens into committing various crimes in '
                            'order to test the reluctance of citizens to '
                            'break the law.'),
        region_description=('World Census agents attempted to lure '
                            'citizens into committing various crimes in '
                            'order to test the reluctance of citizens to '
                            'break the law.'),
    ),
    43: ScaleInfo(
        id=43,
        title='Safety',
        ranked='Safest',
        gradation='Bubble-Rapp Safety Rating',
        nation_description=('World Census agents tested the sharpness of '
                            "household objects, the softness of children's "
                            'play equipment, and the survival rate of '
                            'people taking late walks to determine how '
                            'safe each nation is to visit.'),
        region_description=('World Census agents tested the sharpness of '
                            "household objects, the softness of children's "
                            'play equipment, and the survival rate of '
                            'people taking late walks to determine how '
                            'safe each region is to visit.'),
    ),
    44: ScaleInfo(
        id=44,
        title='Lifespan',
        ranked='Longest Average Lifespans',
        gradation='Years',
        nation_description=('Nations ranked highly have lower rates of '
                            'preventable death, with their citizens '
                            'enjoying longer average lifespans.'),
        region_description=('Regions ranked highly have lower rates of '
                            'preventable death, with their citizens '
                            'enjoying longer average lifespans.'),
    ),
    45: ScaleInfo(
        id=45,
        title='Ideological Radicality',
        ranked='Most Extreme',
        gradation='Paul-Nader Subjective Decentrality Index',
        nation_description=('The World Census ranked nations on the basis '
                            'of how odd, extreme, or fundamentalist their '
                            'social, economic, and political systems are.'),
        region_description=('The World Census ranked regions on the basis '
                            'of how odd, extreme, or fundamentalist their '
                            'social, economic, and political systems are.'),
    ),
    46: ScaleInfo(
        id=46,
        title='Defense Forces',
        ranked='Most Advanced Defense Forces',
        gradation='Total War Preparedness Rating',
        nation_description=('Nations ranked highly spend the most on '
                            'national defense, and are most secure against '
                            'foreign aggression.'),
        region_description=('Regions ranked highly spend the most on '
                            'regional defense, and are most secure against '
                            'foreign aggression.'),
    ),
    47: ScaleInfo(
        id=47,
        title='Pacifism',
        ranked='Most Pacifist',
        gradation='Cheeks Turned Per Day',
        nation_description=('Nations ranked highly pursue diplomatic '
                            'solutions rather than military ones in the '
                            'international arena, have small or '
                            'nonexistent militaries, and peace-loving '
                            'citizens.'),
        region_description=('Regions ranked highly pursue diplomatic '
                            'solutions rather than military ones in the '
                            'international arena, have small or '
                            'nonexistent militaries, and peace-loving '
                            'citizens.'),
    ),
    48: ScaleInfo(
        id=48,
        title='Economic Freedom',
        ranked='Most Pro-Market',
        gradation='Rand Index',
        nation_description=('This data was compiled by surveying a random '
                            'sample of businesses with the question, "Do '
                            'you believe the government is committed to '
                            'free market policies?"'),
        region_description=('This data was compiled by surveying a random '
                            'sample of businesses with the question, "Do '
                            'you believe the government is committed to '
                            'free market policies?"'),
    ),
    49: ScaleInfo(
        id=49,
        title='Taxation',
        ranked='Highest Average Tax Rates',
        gradation='Effective Tax Rate',
        nation_description=('Although some nations have a flat tax rate '
                            'for all citizens while others tax the rich '
                            'more heavily than the poor, the World Census '
                            "used averages to rank the world's most taxing "
                            'governments.'),
        region_description=('Although some regions have a flat tax rate '
                            'for all citizens while others tax the rich '
                            'more heavily than the poor, the World Census '
                            "used averages to rank the world's most taxing "
                            'governments.'),
    ),
    50: ScaleInfo(
        id=50,
        title='Freedom From Taxation',
        ranked='Lowest Overall Tax Burden',
        gradation='Hayek Index',
        nation_description=('World Census financial experts assessed '
                            'nations across a range of direct and indirect '
                            'measures in order to determine which placed '
                            'the lowest tax burden on their citizens.'),
        region_description=('World Census financial experts assessed '
                            'regions across a range of direct and indirect '
                            'measures in order to determine which placed '
                            'the lowest tax burden on their citizens.'),
    ),
    51: ScaleInfo(
        id=51,
        title='Corruption',
        ranked='Most Corrupt Governments',
        gradation='Kickbacks Per Hour',
        nation_description=('World Census officials visited a range of '
                            'government departments and recorded how '
                            'frequently bribes were required to complete '
                            'simple administrative requests.'),
        region_description=('World Census officials visited a range of '
                            'government departments and recorded how '
                            'frequently bribes were required to complete '
                            'simple administrative requests.'),
    ),
    52: ScaleInfo(
        id=52,
        title='Integrity',
        ranked='Least Corrupt Governments',
        gradation='Percentage Of Bribes Refused',
        nation_description=('World Census agents tempted government '
                            'officials with financial and other '
                            'inducements to bend the rules and recorded '
                            'how often their proposals were declined.'),
        region_description=('World Census agents tempted government '
                            'officials with financial and other '
                            'inducements to bend the rules and recorded '
                            'how often their proposals were declined.'),
    ),
    53: ScaleInfo(
        id=53,
        title='Authoritarianism',
        ranked='Most Authoritarian',
        gradation='Stalins',
        nation_description=('World Census staff loitered innocuously in '
                            'various public areas and recorded the length '
                            'of time that passed before they were '
                            'approached by dark-suited officials.'),
        region_description=('World Census staff loitered innocuously in '
                            'various public areas and recorded the length '
                            'of time that passed before they were '
                            'approached by dark-suited officials.'),
    ),
    54: ScaleInfo(
        id=54,
        title='Youth Rebelliousness',
        ranked='Most Rebellious Youth',
        gradation='Stark-Dean Displacement Index',
        nation_description=('World Census observers counted the number of '
                            'times their car stereo was stolen from '
                            'outside fast food stores to determine which '
                            'nations have relatively high levels of '
                            'youth-related crime.'),
        region_description=('World Census observers counted the number of '
                            'times their car stereo was stolen from '
                            'outside fast food stores to determine which '
                            'regions have relatively high levels of '
                            'youth-related crime.'),
    ),
    55: ScaleInfo(
        id=55,
        title='Culture',
        ranked='Most Cultured',
        gradation='Snufflebottom-Wiggendum Pentatonic Scale',
        nation_description=('After spending many tedious hours in coffee '
                            'shops and concert halls, World Census experts '
                            'have found the following nations to be the '
                            'most cultured.'),
        region_description=('After spending many tedious hours in coffee '
                            'shops and concert halls, World Census experts '
                            'have found the following regions to be the '
                            'most cultured.'),
    ),
    56: ScaleInfo(
        id=56,
        title='Employment',
        ranked='Highest Workforce Participation Rate',
        gradation='Workforce Participation Rate',
        nation_description=('World Census experts studied the ratings of '
                            'daytime television chat shows to estimate the '
                            'percentage of citizens who are employed.'),
        region_description=('World Census experts studied the ratings of '
                            'daytime television chat shows to estimate the '
                            'percentage of citizens who are employed.'),
    ),
    57: ScaleInfo(
        id=57,
        title='Public Transport',
        ranked='Most Advanced Public Transport',
        gradation='Societal Mobility Rating',
        nation_description=('World Census experts captured, tagged, and '
                            'released trains in order to identify which '
                            'nations have the most extensive, well-funded '
                            'public transportation systems.'),
        region_description=('World Census experts captured, tagged, and '
                            'released trains in order to identify which '
                            'regions have the most extensive, well-funded '
                            'public transportation systems.'),
    ),
    58: ScaleInfo(
        id=58,
        title='Tourism',
        ranked='Most Popular Tourist Destinations',
        gradation='Tourists Per Hour',
        nation_description=('World Census experts tracked millions of '
                            'international tourists in order to determine '
                            "the world's favourite nations to sight-see."),
        region_description=('World Census experts tracked millions of '
                            'international tourists in order to determine '
                            "the world's favourite regions to sight-see."),
    ),
    59: ScaleInfo(
        id=59,
        title='Weaponization',
        ranked='Most Armed',
        gradation='Weapons Per Person',
        nation_description=('World Census experts took their lives into '
                            'their hands in order to ascertain the average '
                            'number of deadly weapons per citizen.'),
        region_description=('World Census experts took their lives into '
                            'their hands in order to ascertain the average '
                            'number of deadly weapons per citizen.'),
    ),
    60: ScaleInfo(
        id=60,
        title='Recreational Drug Use',
        ranked='Highest Drug Use',
        gradation='Pineapple Fondness Rating',
        nation_description=('World Census experts sampled many cakes of '
                            "dubious content to determine which nations' "
                            'citizens consume the most recreational drugs.'),
        region_description=('World Census experts sampled many cakes of '
                            "dubious content to determine which regions' "
                            'citizens consume the most recreational drugs.'),
    ),
    61: ScaleInfo(
        id=61,
        title='Obesity',
        ranked='Fattest Citizens',
        gradation='Obesity Rate',
        nation_description=('World Census takers tracked the sale of '
                            'Cheetos and Twinkies to ascertain which '
                            'nations most enjoyed the "kind bud."'),
        region_description=('World Census takers tracked the sale of '
                            'Cheetos and Twinkies to ascertain which '
                            'regions most enjoyed the "kind bud."'),
    ),
    62: ScaleInfo(
        id=62,
        title='Secularism',
        ranked='Most Secular',
        gradation='Atheism Rate',
        nation_description=('World Census experts studied which citizens '
                            'seemed least concerned about eternal '
                            'damnation, spiritual awakeness, and chakra '
                            'wellbeing in order to determine the most '
                            'godforsaken nations.'),
        region_description=('World Census experts studied which citizens '
                            'seemed least concerned about eternal '
                            'damnation, spiritual awakeness, and chakra '
                            'wellbeing in order to determine the most '
                            'godforsaken regions.'),
    ),
    63: ScaleInfo(
        id=63,
        title='Environmental Beauty',
        ranked='Most Beautiful Environments',
        gradation='Pounds Of Wildlife Per Square Mile',
        nation_description=('World Census researchers spent many arduous '
                            'weeks lying on beaches and trekking through '
                            'rainforests to compile a definitive list of '
                            'the most attractive and best cared for '
                            'environments.'),
        region_description=('World Census researchers spent many arduous '
                            'weeks lying on beaches and trekking through '
                            'rainforests to compile a definitive list of '
                            'the most attractive and best cared for '
                            'environments.'),
    ),
    64: ScaleInfo(
        id=64,
        title='Charmlessness',
        ranked='Most Avoided',
        gradation='Kardashian Reflex Score',
        nation_description=('Nations ranked highly are considered by many '
                            'to be the most inhospitable, charmless, and '
                            'ghastly places to spend a vacation, or, '
                            'indeed, any time at all.'),
        region_description=('Regions ranked highly are considered by many '
                            'to be the most inhospitable, charmless, and '
                            'ghastly places to spend a vacation, or, '
                            'indeed, any time at all.'),
    ),
    65: ScaleInfo(
        id=65,
        title='Influence',
        ranked='Most Influential',
        gradation='Soft Power Disbursement Rating',
        nation_description=('World Census experts spent many evenings '
                            'loitering in the corridors of power in order '
                            'to determine which nations were the greatest '
                            'international diplomacy heavyweights.'),
        region_description=('World Census experts spent many evenings '
                            'loitering in the corridors of power in order '
                            'to determine which regions were the greatest '
                            'international diplomacy heavyweights.'),
    ),
    66: ScaleInfo(
        id=66,
        title='World Assembly Endorsements',
        ranked='Most World Assembly Endorsements',
        gradation='Valid Endorsements',
        nation_description=('World Census staff pored through World '
                            'Assembly records to determine which nations '
                            'were the most endorsed by others in their '
                            'region.'),
        region_description=('World Census staff pored through World '
                            'Assembly records to determine the average '
                            'number of endorsements per nation in each '
                            'region.'),
    ),
    67: ScaleInfo(
        id=67,
        title='Averageness',
        ranked='Most Average',
        gradation='Average Standardized Normality Scale',
        nation_description=('World Census staff took time out to pay '
                            'tribute to those most overlooked of nations: '
                            'the determinedly average.'),
        region_description=('World Census staff took time out to pay '
                            'tribute to those most overlooked of regions: '
                            'the determinedly average.'),
    ),
    68: ScaleInfo(
        id=68,
        title='Human Development Index',
        ranked='Most Developed',
        gradation='Human Development Index',
        nation_description=('The World Census compiles a "Human '
                            'Development Index" by measuring citizens\' '
                            'average life expectancy, education, and '
                            'income.'),
        region_description=('The World Census compiles a "Human '
                            'Development Index" by measuring citizens\' '
                            'average life expectancy, education, and '
                            'income.'),
    ),
    69: ScaleInfo(
        id=69,
        title='Primitiveness',
        ranked='Most Primitive',
        gradation='Scary Big Number Scale',
        nation_description=('Nations were ranked by World Census officials '
                            'based on the number of natural phenomena '
                            'attributed to the unknowable will of '
                            'animal-based spirit gods.'),
        region_description=('Regions were ranked by World Census officials '
                            'based on the number of natural phenomena '
                            'attributed to the unknowable will of '
                            'animal-based spirit gods.'),
    ),
    70: ScaleInfo(
        id=70,
        title='Scientific Advancement',
        ranked='Most Scientifically Advanced',
        gradation='Kurzweil Singularity Index',
        nation_description=('World Census researchers quantified national '
                            'scientific advancement by quizzing random '
                            'citizens about quantum chromodynamics, '
                            'space-time curvature and stem cell '
                            'rejuvenation therapies. Responses based on '
                            'Star Trek were discarded.'),
        region_description=('World Census researchers quantified regional '
                            'scientific advancement by quizzing random '
                            'citizens about quantum chromodynamics, '
                            'space-time curvature and stem cell '
                            'rejuvenation therapies. Responses based on '
                            'Star Trek were discarded.'),
    ),
    71: ScaleInfo(
        id=71,
        title='Inclusiveness',
        ranked='Most Inclusive',
        gradation='Mandela-Wollstonecraft Non-Discrimination Index',
        nation_description=('WA analysts ranked nations based on whether '
                            'all citizens were commonly treated as equally '
                            'valuable members of society.'),
        region_description=('WA analysts ranked regions based on whether '
                            'all citizens were commonly treated as equally '
                            'valuable members of society.'),
    ),
    72: ScaleInfo(
        id=72,
        title='Average Income',
        ranked='Highest Average Incomes',
        gradation='Standard Monetary Units',
        nation_description=('The World Census carefully compared the '
                            'average spending power of citizens in each '
                            'nation.'),
        region_description=('The World Census carefully compared the '
                            'average spending power of citizens in each '
                            'region.'),
    ),
    73: ScaleInfo(
        id=73,
        title='Average Income of Poor',
        ranked='Highest Poor Incomes',
        gradation='Standard Monetary Units',
        nation_description=('The World Census studied the spending power '
                            'of the poorest 10% of citizens in each nation.'),
        region_description=('The World Census studied the spending power '
                            'of the poorest 10% of citizens in each region.'),
    ),
    74: ScaleInfo(
        id=74,
        title='Average Income of Rich',
        ranked='Highest Wealthy Incomes',
        gradation='Standard Monetary Units',
        nation_description=('The World Census studied the spending power '
                            'of the richest 10% of citizens in each nation.'),
        region_description=('The World Census studied the spending power '
                            'of the richest 10% of citizens in each region.'),
    ),
    75: ScaleInfo(
        id=75,
        title='Public Education',
        ranked='Most Advanced Public Education',
        gradation='Edu-tellignce\u00AE Test Score',
        nation_description=('Fresh-faced World Census agents infiltrated '
                            'schools with varying degrees of success in '
                            'order to determine which nations had the most '
                            'widespread, well-funded, and advanced public '
                            'education programs.'),
        region_description=('Fresh-faced World Census agents infiltrated '
                            'schools with varying degrees of success in '
                            'order to determine which regions had the most '
                            'widespread, well-funded, and advanced public '
                            'education programs.'),
    ),
    76: ScaleInfo(
        id=76,
        title='Economic Output',
        ranked='Highest Economic Output',
        gradation='Standard Monetary Units',
        nation_description=('World Census bean-counters crunched the '
                            'numbers to calculate national Gross Domestic '
                            'Product. Older nations, with higher '
                            'populations, were noted to have a distinct '
                            'advantage.'),
        region_description=('World Census bean-counters crunched the '
                            'numbers to calculate regional Gross Domestic '
                            'Product. Older regions, with higher '
                            'populations, were noted to have a distinct '
                            'advantage.'),
    ),
    77: ScaleInfo(
        id=77,
        title='Crime',
        ranked='Highest Crime Rates',
        gradation='Crimes Per Hour',
        nation_description=('World Census interns were dispatched to seedy '
                            'back alleys in order to determine which '
                            'nations have the highest crime rates.'),
        region_description=('World Census interns were dispatched to seedy '
                            'back alleys in order to determine which '
                            'regions have the highest crime rates.'),
    ),
    78: ScaleInfo(
        id=78,
        title='Foreign Aid',
        ranked='Highest Foreign Aid Spending',
        gradation='Clooney Contribution Index',
        nation_description=('The World Census intercepted food drops in '
                            'several war-torn regions to determine which '
                            'nations spent the most on international aid. '),
        region_description=('The World Census intercepted food drops in '
                            'several war-torn regions to determine which '
                            'regions spent the most on international aid. '),
    ),
    79: ScaleInfo(
        id=79,
        title='Black Market',
        ranked='Largest Black Market',
        gradation='Standard Monetary Units',
        nation_description=('World Census agents tracked "off the books" '
                            'deals and handshake agreements in order to '
                            "study the size of nations' informal economies."),
        region_description=('World Census agents tracked "off the books" '
                            'deals and handshake agreements in order to '
                            "study the size of regions' informal economies."),
    ),
    80: ScaleInfo(
        id=80,
        title='Residency',
        ranked='Most Stationary',
        gradation='Days',
        nation_description=('Long-term World Census surveillance revealed '
                            'which nations have been resident in their '
                            'current region for the longest time.'),
        region_description=('Long-term World Census surveillance revealed '
                            'which regions have the most physically '
                            'grounded nations.'),
    ),
}
