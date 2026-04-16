
def import_attractions():
    attractions = [
            {"name" : "sagrada_familia", "nice_name": "Sagrada Família", "lat": 41.40366, "lon": 2.17447},
            {"name" : "casa_batllo", "nice_name": "Casa Batlló", "lat": 41.39153, "lon": 2.16467},
            {"name" : "park_guell", "nice_name": "Parc Güell", "lat": 41.41393, "lon": 2.15253},
            {"name" : "camp_nou", "nice_name": "Spotify Camp Nou", "lat": 41.38089, "lon": 2.12283},
            {"name" : "casa_mila", "nice_name": "La Pedrera", "lat": 41.39536, "lon": 2.16179},
            {"name" : "museu_picasso", "nice_name": "Museu Picasso", "lat": 41.38507, "lon": 2.18121},
            {"name" : "mercat_boqueria", "nice_name": "Mercat de la Boqueria", "lat": 41.38166, "lon": 2.17161},
            {"name" : "palau_musica", "nice_name": "Palau de la Música Catalana", "lat": 41.38756, "lon": 2.17523},
            {"name" : "barri_gotic", "nice_name": "Barri Gòtic", "lat": 41.38388, "lon": 2.17450},
            {"name" : "montjuic", "nice_name": "Montjuïc", "lat": 41.36868, "lon": 2.16302},
            {"name" : "cuitadella", "nice_name": "Parc de la Ciutadella", "lat": 41.38969, "lon": 2.18502},
            {"name" : "casa_vicens", "nice_name": "Casa Vicens", "lat": 41.40349, "lon": 2.15063},
            {"name" : "catedral", "nice_name": "Catedral de Barcelona", "lat": 41.38385, "lon": 2.17656},
            {"name" : "santa_maria_mar", "nice_name": "Basílica de Santa Maria del Mar", "lat": 41.38371, "lon": 2.18199},
            {"name" : "barceloneta", "nice_name": "La Barceloneta", "lat": 41.38085, "lon": 2.19010},
            {"name" : "fundacio_miro", "nice_name": "Joan Miró Foundation", "lat": 41.36868, "lon": 2.16009},
            {"name" : "tibidabo", "nice_name": "Tibidabo", "lat": 41.42162, "lon": 2.11934},
            {"name" : "sant_antoni", "nice_name": "Mercat de Sant Antoni", "lat": 41.42162, "lon": 2.11934},
            {"name" : "liceu", "nice_name": "Gran Teatre del Liceu", "lat": 41.38756, "lon": 2.17523},
            {"name" : "casa_amatller", "nice_name": "Casa Amatller", "lat": 41.38756, "lon": 2.17523}
        ]
    return attractions

if __name__ == "__main__":
    attractions = import_attractions()
    attraction_names = [attraction["nice_name"] for attraction in attractions]
    print(attraction_names)