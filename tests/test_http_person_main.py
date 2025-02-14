import re


def test_person_headshot_should_be_an_image_link(ia):
    person = ia.get_person('0000206', info=['main'])    # Keanu Reeves
    assert re.match(r'^https?://.*\.jpg$', person['headshot'])


def test_person_producer_is_in_filmography(ia):
    person = ia.get_person('0000206', info=['filmography'])    # Keanu Reeves
    assert 'producer' in person.get('filmography', {})


def test_person_filmography_includes_role(ia):
    person = ia.get_person('0000206', info=['filmography'])    # Keanu Reeves
    movies = person.get('filmography', {}).get('actor', {})
    assert 'John Wick' in [str(movie.currentRole) for movie in movies]


def test_person_with_id_redirect(ia):
    person = ia.get_person('1890852', info=['main'])    # Aleksandr Karpov
    assert '0440022' == person.get('imdbID')


def test_person_name_in_data_should_be_plain(ia):
    person = ia.get_person('0000206', info=['main'])    # Keanu Reeves
    assert person.data.get('name') == 'Keanu Reeves'


def test_person_canonical_name(ia):
    person = ia.get_person('0000206', info=['main'])    # Keanu Reeves
    assert person.get('canonical name') == 'Reeves, Keanu'


def test_person_headshot_if_none_should_be_excluded(ia):
    person = ia.get_person('0330139', info=['main'])    # Deni Gordon
    assert 'headshot' not in person


def test_person_name_should_not_be_canonicalized(ia):
    person = ia.get_person('0000206', info=['main'])    # Keanu Reeves
    assert person.get('name') == 'Keanu Reeves'


def test_person_name_should_not_have_birth_and_death_years(ia):
    person = ia.get_person('0000001', info=['main'])    # Fred Astaire
    assert person.get('name') == 'Fred Astaire'


def test_person_imdb_index_should_be_a_roman_number(ia):
    person = ia.get_person('0000210', info=['main'])    # Julia Roberts
    assert person.get('imdbIndex') == 'I'


def test_person_should_have_filmography(ia):
    person = ia.get_person('0000210', info=['filmography'])    # Julia Roberts
    filmoset = set(['actress', 'producer', 'soundtrack'])
    assert filmoset.issubset(set(person.get('filmography', {}).keys()))


def test_person_filmography_should_contain_movies(ia):
    person = ia.get_person('0000210', info=['filmography'])    # Julia Roberts
    assert len(person.get('filmography', {}).get('actress')) >= 20

def test_person_filmography_actor_and_actress_should_be_the_same(ia):
    person = ia.get_person('0000210', info=['filmography'])    # Julia Roberts
    assert person.get('actress') == person.get('actor')

def test_person_filmography_should_contain_many_roles(ia):
    person = ia.get_person('0000110', info=['filmography'])    # Kenneth Branagh
    filmography = person.get('filmography', {})
    assert len(filmography) > 9
    assert len(filmography.get('actor')) >= 70
    assert len(filmography.get('writer')) >= 9
    assert len(filmography.get('self')) >= 150


def test_person_imdb_index_if_none_should_be_excluded(ia):
    person = ia.get_person('0000206', info=['main'])    # Keanu Reeves
    assert 'imdbIndex' not in person
