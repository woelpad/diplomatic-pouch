#
# Sail Ho! Diplomacy Variant
#
# Map
#
# The Map Dictionary is of the form 
#
#	key : Province Name     value : { Aliases, Borders }
#
#
# Aliases = list of alternative Names for the Province (the first is the default name)
# Borders = adjacent Map spaces listed in CONSECUTIVE CLOCKWISE ORDER (including OTB)
#

OTB = 'OTB'     # Off The Board (an "edge" of the Map)


Map = { 'Aeo'  :	{ 'Aliases'	: [ 'Village of Aeolus' ],
                    'Borders' : [ 'Mid', 'Oly', 'Zeu', 'Tan', 'Chi', 'Nar', 'Gli' ] },
        'Alc'  :  { 'Aliases' : [ 'Alcmene\'s Village' ],
                    'Borders' : [ 'Mor', 'Jas', 'Fle', 'Her', 'GoC', 'SoD' ] },
        'Ama'  :  { 'Aliases' : [ 'Amazon Village' ],
                    'Borders' : [ 'Ech', 'Hip', 'Eas', 'Sch', 'SoW' ] },
        'Aph'  :  { 'Aliases' : [ 'Aphrodite\'s Beach' ],
                    'Borders' : [ 'Psy', 'SoA', 'SoW', 'Sch' ] },
        'Are'  :  { 'Aliases' : [ 'Palace of Ares' ],
                    'Borders' : [ 'Nes', 'Ser', 'Str', 'Hin' ] },
        'Arg'  :  { 'Aliases' : [ 'Argo\'s Pasture' ],
                    'Borders' : [ 'Jox', 'Xen', 'Cec', 'Sou' ] },
        'Aut'  :  { 'Aliases' : [ 'Autolycus\' Hideout' ],
                    'Borders' : [ 'Cal', 'Gab', 'Xen', 'Jox', OTB ] },
        'Cal'  :  { 'Aliases' : [ 'Callisto\'s Stronghold' ],
                    'Borders' : [ 'Fur', 'Per', 'Had', 'Gab', 'Aut', OTB ] },
        'Cec'  :  { 'Aliases' : [ 'Cecrops\' Channel' ],
                    'Borders' : [ 'Arg', 'Xen', 'Pos', 'Hin', 'Str', 'Eas', 'Sou' ] },
        'Cen'  :  { 'Aliases' : [ 'Centaur Forest' ],
                    'Borders' : [ 'Chi', 'Sis', 'Min', 'Ech', 'Nar' ] },
        'Cha'  :  { 'Aliases' : [ 'Charon\'s Crossing' ],
                    'Borders' : [ 'Tar', 'Ely', 'Pea' ] },
        'Chi'  :  { 'Aliases' : [ 'Chiron\'s Cave' ],
                    'Borders' : [ 'Aeo', 'Tan', 'Sis', 'Cen', 'Nar' ] },
        'Cup'  :  { 'Aliases' : [ 'Cupid\'s Cloud' ],
                    'Borders' : [ 'Psy', 'Sch', 'Lov', 'SoA' ] },
        'Dei'  :  { 'Aliases' : [ 'Deianeira\'s Grave' ],
                    'Borders' : [ 'Zeu', 'Oly', 'Her', 'Fle', OTB ] },
        'Eas'  :  { 'Aliases' : [ 'Eastern Ocean' ],
                    'Borders' : [ 'Ama', 'Hip', 'Min', OTB, 'Sou', 'Cec', 'Str', 'Ser', 'Sch' ] },
        'Ech'  :  { 'Aliases' : [ 'Echo\'s Glade' ],
                    'Borders' : [ 'Cen', 'Min', 'Hip', 'Ama', 'SoW', 'Nar' ] },
        'Ely'  :  { 'Aliases' : [ 'Elysian Fields' ],
                    'Borders' : [ 'Cha', 'Tar', 'Fur', OTB, 'Pea' ] },
        'Fir'  :  { 'Aliases' : [ 'Sea of Fire' ],
                    'Borders' : [ 'Les', 'Hes', 'Ves', 'Lov', 'SoT', 'Per', 'Tar', 'Pea', 'Lbs' ] },
        'Fle'  :  { 'Aliases' : [ 'Field of the Golden Fleece' ],
                    'Borders' : [ 'Dei', 'Her', 'Alc', 'Jas', OTB ] },
        'Fur'  :  { 'Aliases' : [ 'Realm of the 3 Furies' ],
                    'Borders' : [ 'Ely', 'Tar', 'Per', 'Cal', OTB ] },
        'Gab'  :  { 'Aliases' : [ 'Gabrielle\'s Village' ],
                    'Borders' : [ 'Xen', 'Aut', 'Cal', 'Had', 'SoT', 'Pos' ] },
        'Gli'  :  { 'Aliases' : [ 'Glittering Gulf' ],
                    'Borders' : [ 'Pro', 'Mid', 'Aeo', 'Nar', 'SoW' ] },
        'GoC'  :  { 'Aliases' : [ 'Gulf of Chains' ],
                    'Borders' : [ 'Alc', 'Her', 'Sal', 'Pro', 'SoA', 'SoD' ] },
        'Had'  :  { 'Aliases' : [ 'Depths of Hades' ],
                    'Borders' : [ 'Gab', 'Cal', 'Per', 'SoT' ] },
        'Her'  :  { 'Aliases' : [ 'Hercules\' Respite' ],
                    'Borders' : [ 'Alc', 'Fle', 'Dei', 'Oly', 'Sal', 'GoC' ] },
        'Hes'  :  { 'Aliases' : [ 'Shrine to Hestia' ],
                    'Borders' : [ 'Les', 'SoA', 'Ves', 'Fir' ] },
        'Hin'  :  { 'Aliases' : [ 'Forest of the Golden Hind' ],
                    'Borders' : [ 'Nes', 'Are', 'Str', 'Cec', 'Pos' ] },
        'Hip'  :  { 'Aliases' : [ 'Hippolyta\'s Girdle' ],
                    'Borders' : [ 'Ama', 'Ech', 'Min', 'Eas' ] },
        'Jas'  :  { 'Aliases' : [ 'Jason\'s Kingdom' ],
                    'Borders' : [ 'Fle', 'Alc', 'Mor', 'Wes', OTB ] },
        'Jox'  :  { 'Aliases' : [ 'Joxter\'s Retreat' ],
                    'Borders' : [ 'Aut', 'Xen', 'Arg', 'Sou', OTB ] },
        'Lbs'  :  { 'Aliases' : [ 'Lesbian Sea' ],
                    'Borders' : [ 'Les', 'Fir', 'Pea', OTB, 'Wes' ] },
        'Les'  :  { 'Aliases' : [ 'Isle of Lesbos' ],
                    'Borders' : [ 'Hes', 'Fir', 'Lbs', 'Wes', 'SoA' ] },
        'Lov'  :  { 'Aliases' : [ 'Lover\'s Lane' ],
                    'Borders' : [ 'Ves', 'SoA', 'Cup', 'Sch', 'Nes', 'Pos', 'SoT', 'Fir' ] },
        'Mid'  :  { 'Aliases' : [ 'Realm of King Midas' ],
                    'Borders' : [ 'Pro', 'Sal', 'Oly', 'Aeo', 'Gli' ] },
        'Min'  :  { 'Aliases' : [ 'Minotaur\'s Labyrinth' ],
                    'Borders' : [ 'Hip', 'Ech', 'Cen', 'Sis', OTB, 'Eas' ] },
        'Mor'  :  { 'Aliases' : [ 'Morpheus\' Palace' ],
                    'Borders' : [ 'Jas', 'Alc', 'SoD', 'Wes' ] },
        'Nar'  :  { 'Aliases' : [ 'Narcissus\' Reflection' ],
                    'Borders' : [ 'Aeo', 'Chi', 'Cen', 'Ech', 'SoW', 'Gli' ] },
        'Nes'  :  { 'Aliases' : [ 'Nestor\'s Kingdom' ],
                    'Borders' : [ 'Ser', 'Are', 'Hin', 'Pos', 'Lov', 'Sch' ] },
        'Oly'  :  { 'Aliases' : [ 'Mount Olympus' ],
                    'Borders' : [ 'Dei', 'Zeu', 'Aeo', 'Mid', 'Sal', 'Her' ] },
        'Pea'  :  { 'Aliases' : [ 'Ocean of Peace' ],
                    'Borders' : [ 'Tar', 'Cha', 'Ely', OTB, 'Lbs', 'Fir' ] },
        'Per'  :  { 'Aliases' : [ 'Persephone\'s Garden' ],
                    'Borders' : [ 'Had', 'Cal', 'Fur', 'Tar', 'Fir', 'SoT' ] },
        'Pos'  :  { 'Aliases' : [ 'Poseidon\'s Curse' ],
                    'Borders' : [ 'Nes', 'Hin', 'Cec', 'Xen', 'Gab', 'SoT', 'Lov' ] },
        'Pro'  :  { 'Aliases' : [ 'Prometheus\' Cliff' ],
                    'Borders' : [ 'Sal', 'Mid', 'Gli', 'SoW', 'SoA', 'GoC' ] },
        'Psy'  :  { 'Aliases' : [ 'Village of Psyche' ],
                    'Borders' : [ 'Aph', 'Sch', 'Cup', 'SoA' ] },
        'Sal'  :  { 'Aliases' : [ 'Salmonius\' Scheme' ],
                    'Borders' : [ 'Her', 'Oly', 'Mid', 'Pro', 'GoC' ] },
        'Sch'  :  { 'Aliases' : [ 'Scholars Channel' ],
                    'Borders' : [ 'Ama', 'Eas', 'Ser', 'Nes', 'Lov', 'Cup', 'Psy', 'Aph', 'SoW' ] },
        'Ser'  :  { 'Aliases' : [ 'Serina\'s Village' ],
                    'Borders' : [ 'Str', 'Are', 'Nes', 'Sch', 'Eas' ] },
        'Sis'  :  { 'Aliases' : [ 'Sisyphus\' Hill' ],
                    'Borders' : [ 'Min', 'Cen', 'Chi', 'Tan', OTB ] },
        'SoA'  :  { 'Aliases' : [ 'Sea of Arrows' ],
                    'Borders' : [ 'Ves', 'Hes', 'Les', 'Wes', 'SoD', 'GoC', 'Pro', 'SoW', 'Aph', 'Psy', 'Cup', 'Lov' ] },
        'SoD'  :  { 'Aliases' : [ 'Sea of Dreams' ],
                    'Borders' : [ 'Mor', 'Alc', 'GoC', 'SoA', 'Wes' ] },
        'SoT'  :  { 'Aliases' : [ 'Sea of Tears' ],
                    'Borders' : [ 'Gab', 'Had', 'Per', 'Fir', 'Lov', 'Pos' ] },
        'Sou'  :  { 'Aliases' : [ 'South Sea' ],
                    'Borders' : [ 'Jox', 'Arg', 'Cec', 'Eas', OTB ] },
        'SoW'  :  { 'Aliases' : [ 'Sea of Waves' ],
                    'Borders' : [ 'Pro', 'Gli', 'Nar', 'Ech', 'Ama', 'Sch', 'Aph', 'SoA' ] },
        'Str'  :  { 'Aliases' : [ 'Strife\'s Cave' ],
                    'Borders' : [ 'Hin', 'Are', 'Ser', 'Eas', 'Cec' ] },
        'Tan'  :  { 'Aliases' : [ 'Tantalus\' Pool' ],
                    'Borders' : [ 'Sis', 'Chi', 'Aeo', 'Zeu', OTB ] },
        'Tar'  :  { 'Aliases' : [ 'Tartarus' ],
                    'Borders' : [ 'Per', 'Fur', 'Ely', 'Cha', 'Pea', 'Fir' ] },
        'Ves'  :  { 'Aliases' : [ 'Convent of the Vestal Virgins' ],
                     'Borders' : [ 'Hes', 'SoA', 'Lov', 'Fir' ] },
        'Wes'  :  { 'Aliases' : [ 'Western Ocean' ],
                    'Borders' : [ 'Jas', 'Mor', 'SoD', 'SoA', 'Les', 'Lbs', OTB ] },
        'Xen'  :  { 'Aliases' : [ 'Xena\'s Rest' ],
                    'Borders' : [ 'Arg', 'Jox', 'Aut', 'Gab', 'Pos', 'Cec' ] },
        'Zeu'  :  { 'Aliases' : [ 'Temple of Zeus' ],
                    'Borders' : [ 'Tan', 'Aeo', 'Oly', 'Dei', OTB ] }
      }
