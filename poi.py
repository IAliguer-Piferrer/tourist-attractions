
def import_attractions():
    attractions = [
            {"name" : "sagrada_familia", "nice_name": "Sagrada Família", "lat": 41.40366, "lon": 2.17447},
            {"name" : "casa_batllo", "nice_name": "Casa Batlló", "lat": 41.39153, "lon": 2.16467},
            {"name" : "park_guell", "nice_name": "Parc Güell", "lat": 41.41393, "lon": 2.15253},
            {"name" : "camp_nou", "nice_name": "Spotify Camp Nou", "lat": 41.38089, "lon": 2.12283},
            {"name" : "casa_mila", "nice_name": "La Pedrera", "lat": 41.39536, "lon": 2.16179},
            {"name" : "museu_picasso", "nice_name": "Museu Picasso", "lat": 41.38507, "lon": 2.18121}
        ]
    return attractions

if __name__ == "__main__":
    attractions = import_attractions()
    attraction_names = [attraction["nice_name"] for attraction in attractions]
    print(attraction_names)