"""build_place_photos.py 설정: 사진 검색어를 바꾸거나, 교통 지점이지만 사진을 넣을 곳·뺄 곳을 적는다 (나라 → 장소 키)."""

# 장소 키 → 커먼즈 검색어 (앞에서부터 시도). 없으면 places 의 q 로 찾는다
Q = {
    "spain": {
        "casa_mila": ["File:Antoni Gaudí-Casa Milà-Barcelona.jpg"],
        "toledo_cathedral": ["File:Vista de una parte exterior de la Catedral de Toledo.JPG"],
        "sol": ["File:Puerta del Sol (Madrid) 03.jpg"],
        "setas": ["File:SEVILLA METROPOL-PARASOL MEYER-H 20120530 174928.jpg"],
        "sagrada": ["File:Barcelona - Carrer de Mallorca - View West on La Sagrada Família - Nativity façade.jpg"],
        "sabatini": ["File:Estanque Central - Jardines de Sabatini - Madrid 01.jpg"],
        "prado": ["File:Puerta de Goya del Museo del Prado (6 de diciembre de 2005, Madrid).jpg"],
        "plaza_nueva_gra": ["File:Aa plaza nueva in granada.jpg"],
        "park_guell": ["File:Bird nests at Park Güell (2925592214).jpg"],
        "nasrid": ["File:Patio de los Arrayanes Alhambra 02 2014.jpg"],
        "maria_luisa": ["File:Parque de María Luisa, Sevilla, Oct 1999 - 03.jpg"],
        "eme": ["File:View of roof of Cathedral from Giralda of Seville on March 9 2017.jpg"],
        "cibeles": ["File:Fuente de Cibeles, Plaza de Cibeles, Madrid, España, 2017-05-18, DD 10.jpg"],
        "cba": ["File:Madrid - Círculo de Bellas Artes, Azotea 07.jpg"],
        "cathedral_sev": ["File:Exterior of the Cathedral of Seville 20180719.jpg"],
        "casa_memoria": ["File:Sevilla - Centro Cultural Flamenco Casa de la Memoria.jpg"],
        "alcazar_sev": ["File:Alcázar de Sevilla - Patio de las Doncellas 002.jpg"],
        "hotelB_sev": ["File:Hotel Alfonso X.jpg"],
        "parador": ["File:Convento San Francisco parador Alhambra Granada Spain.jpg"],
    },
    "greece": {
        "matoyianni": ["Mykonos town alley", "Chora Mykonos street", "Mykonos old town"],
        "syntagma_guard": ["File:Evzones, Presidential Guard (41263332434).jpg"],
        "perissa": ["File:Beach - Perissa - Santorini - Greece - 02.jpg"],
        "national_garden": ["File:National Garden of Athens, 20240531 1540 9794.jpg"],
        "kastraki": ["File:X2.02 Kastráki, »Spindel«.jpg"],
        "great_meteoron": ["File:Megalo Meteoro monastery1.jpg"],
        "fira": ["File:Crater rim - Fira - Santorini - Greece - 10.jpg"],
        "arachova": ["File:Arachova2015.jpg"],
        "anafiotika": ["File:Anafiotika, Athens, 20240601 0923 0020.jpg"],
    },
    "portugal": {
        "almas": ["Capela das Almas Porto facade", "Capela das Almas Porto"],
        "bairro_alto": ["File:Lisboa - Bairro Alto (5420829357).jpg"],
        "bolhao": ["File:Mercado do Bolhão stands.JPG"],
        "lagos": ["File:Praça Luís de Camões, Lagos (20765941920).jpg"],
        "oceanario": ["Oceanário de Lisboa main tank", "Lisbon Oceanarium building"],
        "sao_jorge": ["Castelo de São Jorge Lisbon walls", "Castelo de São Jorge"],
        "se_lisboa": ["File:Sé de Lisboa (Lisbon Cathedral) 02.jpg"],
        "santa_justa": ["File:Lisbon (Lisboa) historic elevator Santa Justa Luca Galuzzi 2006.jpg"],
        "taylors": ["Taylor's Port wine cellar barrels", "Port wine cellar Vila Nova de Gaia barrels"],
        "martim_moniz": ["Tram 28 Martim Moniz", "Lisbon tram 28 Graça"],
        "obidos": ["Óbidos street", "Óbidos Portugal Rua Direita"],
        "mouros": ["Castelo dos Mouros Sintra walls", "Castelo dos Mouros"],
    },
    "czech": {
        "ck_garden": ["File:381 01 Český Krumlov, Czech Republic - panoramio (1).jpg"],
        "strahov": ["File:Strahov knihovna Teolog 1.jpg"],
        "stephansdom": ["File:Stephansdom-Vienna-Austria.jpg"],
        "pilsner": ["File:Pilsner Urquell Brewery - panoramio (2).jpg"],
        "national_theatre": ["File:Národní divadlo z Kampy.jpg"],
        "naplavka": ["File:Praha - Rašínovo nábřeží - View NW II.jpg"],
        "mirabell": ["File:Mirabell Palace 7.jpg"],
        "hallstatt_view": ["File:View of Hallstatt waterfront and churches from Hallstätter See.jpg"],
        "letna": ["File:Praha Letná Pražský metronom 02.jpg"],
        "kv_vridlo": ["File:Vřídlo 004.JPG"],
        "hofburg": ["File:Hofburg, Michaelerplatz Wien (54519402718).jpg"],
        "hallstatt": ["File:Hallstatt - 8856135370.jpg"],
        "bridge_tower_old": ["File:Prague Charles Bridge 2021 04.jpg"],
        "ck_view": ["File:Panorama-of-cesky-krumlov-tower-castle-old-town-and-latran.jpg"],
        "ck_square": ["File:Český Krumlov, měšťanský dům, nám. Svornosti čp.4.JPG"],
        "castle": ["File:View of Prague and St. Vitus Cathedral from Vyšehrad. Czech Republic.jpg"],
    },
}

# 호텔 키 → 공식 사이트 (대표 사진 og:image 를 가져온다). trip.py HOTEL_META 의 official 보다 우선
# og:image 가 없거나 막힌 곳은 (사이트, 그 사이트의 사진 주소) 로 적는다
OFFICIAL = {
    "spain": {
        "hotelA_mad": ("https://room-matehotels.com/es/hotel-alba-madrid/", "https://room-matehotels.com/content/thumbs/800_450/content/imgsxml/panel_herohotel/meetalba2173.jpg"),
        "hotelA_bcn": ("https://www.cataloniahotels.com/en/hotel/catalonia-catedral", "https://images.cataloniahotels.com/styles/talla_uno/cloud-storage/images/2024-09/highlight-hotel-56.jpg.webp"),
    },
    "greece": {
        "h_ath_electra": ("https://www.electrahotels.gr/hotels/electra-palace-athens/", "https://www.electrahotels.gr/app/uploads/2025/07/electra-palace-roof-garden-restaurant-acropolis-background-1.jpg"),
        "h_myk_harmony": "https://www.harmonyhotel.gr/",
        "h_oia_andronis": ("https://www.andronis.com/", "https://content.andronis.com/uploads/1_0bc328ec4c.jpg"),
        "h_kal_doupiani": ("https://www.doupianihouse.gr/", "https://www.doupianihouse.gr/slider/1/slider_image.jpg"),
        "h_cha_delfino": ("https://www.casadelfino.com/", "https://www.casadelfino.com/wp-content/uploads/2025/01/casa_delfino_crete_luxury_boutique_hotel_chania-68-1-scaled.jpg"),
        "h_fira_elgreco": "https://elgreco.com.gr/",
    },
    "portugal": {
        "h_lis_avani": ("https://www.avanihotels.com/en/lisbon", "https://assets.avanihotels.com/image/upload/q_auto,f_jpg,c_limit,w_1200/media/minor/avani/images/lisbon/homepage/avani_avenida_liberdade_lisboa_hotel_homepage-banner_1920x900.jpg"),
        "h_lis_mundial": "https://www.hotel-mundial.pt/en/",
        "h_opo_descobertas": "https://www.aspasios.com/destination/porto-boutique-hotels/descobertas-boutique-hotel-by-aspasios",
        "h_opo_acta": "https://www.actahotels.com/en/hotels/hotel-acta-the-avenue",
        "h_naz_marbravo": "https://www.marbravo.com/en",
        "h_lagos_casamae": ("https://casa-mae.com/", "https://images.ctfassets.net/42dqdwcs3kac/3oVc2KVrbFxuKd359PuAKk/3c1a224563e30621be400e9d4a857e75/image00020.jpeg"),
    },
    "czech": {
        "h_prg_bohemia": "https://www.grandhotelbohemia.cz/",
        "h_prg_987": ("https://www.987praguehotel.com/", "https://static.wixstatic.com/media/04ed49_af24d596dbd647d89a0c61cdde2ea6cdf000.jpg/v1/fill/w_1200,h_520,al_c,q_85/04ed49_af24d596dbd647d89a0c61cdde2ea6cdf000.jpg"),
        "h_prg_majestic": "https://www.hotel-grandmajestic.cz/en/",
        "h_ck_ruze": "https://www.hotelruze.cz/en",
        "h_ck_oldinn": "https://www.hoteloldinn.cz/en",
        "h_kv_pupp": "https://www.pupp.cz/en",
        "h_hall_heritage": ("https://www.hotel-hallstatt.com/en/", "https://www.hotel-hallstatt.com/redx/tools/mb_image.php/ct.ZnmBUQ/cid.y1d9d05e59a51ae7e/w.y5e4277965b5ca21f/Haus_Kainz.jpg"),
        "h_salz_europa": "https://www.austria-trend.at/en/hotels/europa-salzburg",
        "h_wien_nh": ("https://www.nh-hotels.com/en/hotel/nh-wien-city", "https://img.nh-hotels.net/2grN/wwGe7/original/F_NH_wien_city_063.jpg?output-quality=80&resize=1110:*"),
    },
}

# 이름에 '역·항구' 가 들어가도 볼거리라서 사진을 넣는 곳
INCLUDE = {
    "spain": {"sol"},
    "greece": {"chania_harbour"},
    "portugal": {"sao_bento", "pinhao"},
}

# 사진을 넣지 않는 곳 (커먼즈에 맞는 사진이 없음)
SKIP = {
    "spain": {"hammam"},
}
