from schema import Schema, And, Use, Optional, Regex

validator_memberATE = Schema({
    Optional('idAccount'): And(int),
    'username': And(str, Regex(r'^[A-Za-z0-9]{3,20}$')),
    'password': And(Use(str), lambda e: 254 > len(e) > 5),
    'name': And(str, Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{2,150}')),
    'lastName': And(str,
                    Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{2,150}')),
    'dateBirth': And(str, Regex(r'^((19|20)\d\d)/(0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])$')),
    'email': And(Use(str), Regex(r'\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b'), lambda e: 255 > len(e) > 4),
    'idCity': And(int),
    Optional('memberATEStatus'): And(Use(int), lambda s: 0 < s < 4),
    Optional('memberATEType'): And(Use(int), lambda t: 0 < t < 4),
})

validator_login = Schema({
    'username': And(str, Regex(r'^[A-Za-z0-9]{8,20}$')),
    'password': And(Use(str), lambda e: 254 > len(e) > 5)
})

validator_change_status_member = Schema({
    'idAccount': And(str, Regex(r'^[0-9]{1,10}$')),
    'memberATEStatus': And(Use(int), lambda s: 0 < s < 4),
})

validator_change_status_service = Schema({
    'idService': And(str, Regex(r'^[0-9]{1,10}$')),
    'serviceStatus': And(Use(int), lambda s: 0 < s < 4),
})

validator_change_status_request = Schema({
    'idRequest': And(str, Regex(r'^[0-9]{1,10}$')),
    'requestStatus': And(Use(int), lambda s: 0 < s < 6),
})

validator_find_accounts = Schema({
    'memberATEStatus': And(str, Regex(r'^[0-4]{1}$')),
    'filterSearch': And(Use(str), lambda e: 100 > len(e) > 2),
    'criterion': And(Use(str), lambda e: 9 > len(e) > 3)
})

validator_email = Schema({
    'email': And(Use(str), Regex(r'\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b'), lambda e: 255 > len(e) > 4),
    'messageSend': And(Use(str), lambda e: 400 > len(e) > 5)
})

validator_city = Schema({
    'name': And(Use(str),
                Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{5,50}'),
                lambda e: 51 > len(e) > 4),
    'idState': And(int)
})

validator_country = Schema({
    Optional('idCountry'): And(int),
    'name': And(Use(str),
                Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{5,50}'),
                lambda e: 51 > len(e) > 4)
})

validator_state = Schema({
    Optional('idState'): And(int),
    'name': And(Use(str),
                Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{5,50}'),
                lambda e: 51 > len(e) > 4)
})

validator_message = Schema({
    Optional('idMessage'): And(int),
    'message': And(Use(str), Regex(
        r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9#@$!%&/~^.,;:^_{}()=?¡¿/*-+|><°\U00010000-\U0010ffff]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9#@$!%&/~.,;:^_{}()=?¡¿/*-+|><°\U00010000-\U0010ffff]*){1,}'),
                   lambda e: len(e) > 0),
    'memberType': And(int),
    'idChat': And(int),
})

validator_rating = Schema({
    Optional('idRating'): And(int),
    'comment': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){5,150}'),
                   lambda e: 151 > len(e) > 4),
    'rating': And(Use(int), lambda r: 0 < r < 6),
    'idRequest': And(int)
})

validator_report = Schema({
    Optional('idReport'): And(int),
    'reason': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){4,100}'),
                  lambda e: 101 > len(e) > 3),
    'idService': And(int),
    'idMemberATE': And(int)
})

validator_request = Schema({
    Optional('idRequest'): And(int),
    'address': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9#]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9#]*){2,}'),
                   lambda e: 255 > len(e) > 9),
    'date': And(str, Regex(r'^((19|20)\d\d)/(0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])$')),
    'time': And(str, Regex(r'^([0-1][1-9]|[2][0-3])(:)([0-5][0-9])(:)([0-5][0-9])$')),
    'trouble': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'),
                   lambda e: 200 > len(e) > 7),
    'idMemberATE': And(int),
    'idService': And(int)
})

validator_service = Schema({
    Optional('idService'): And(int),
    'idCity': And(int),
    'idMemberATE': And(int),
    'name': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'),
                lambda e: 151 > len(e) > 4),
    'description': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'),
                       lambda e: 301 > len(e) > 4),
    'slogan': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'),
                  lambda e: 51 > len(e) > 4),
    'typeService': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'),
                       lambda e: 151 > len(e) > 4),
    'workingHours': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'),
                        lambda e: 151 > len(e) > 1),
    'minimalCost': And(float),
    'maximumCost': And(Use(float), lambda n: n > 0),
    Optional('serviceStatus'): And(Use(int), lambda n: 4 > n > 0)
})

validator_id = Schema({
    'id': And(str, Regex(r'^[0-9]{1,10}$'))
})

validator_find_chats = Schema({
    'idMember': And(str, Regex(r'^[0-9]{1,10}$')),
    'memberType': And(str, Regex(r'^[A-Za-z]{6,8}$')),
})

validator_chat = Schema({
    "idService": And(int),
    "idMemberATEClient": And(int),
    "idRequest": And(int)
})

validator_get_reports = Schema({
    "filterSearch": And(str),
    "criterion": And(str)
})

validator_find_services = Schema({
    "serviceStatus": And(Use(int), lambda t: 0 < t < 4),
    "filterSearch": And(str),
    "criterion": And(str)
})

validator_find_services_city = Schema({
    "filterSearch": And(str),
    "criterion": And(str),
    'idCity': And(str, Regex(r'^[0-9]{1,10}$'))
})

validator_find_request = Schema({
    "requestStatus": And(Use(int), lambda t: 0 < t < 6),
    "filterSearch": And(str),
    "criterion": And(str)
})

validator_resource = Schema({
    'isMainResource': And(Use(int), lambda t: 0 <= t <= 1),
    'name': And(Use(str), Regex(r'^[A-Za-z0-9]{4,150}$'),
                lambda e: 150 > len(e) > 3),
    'idService': And(int),
    'idMemberATE': And(int),
    'ext': And(Use(str), Regex(r'^(?:jpg|jpeg|png)'))
})
