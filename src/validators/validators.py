from schema import Schema, And, Use, Optional, Regex

validator_memberATE = Schema({
    Optional('id_account'): And(int),
    'username': And(str, Regex(r'^[A-Za-z0-9]{8,20}$')),
    'password': And(str,Regex(r'^(?=.*\d)(?=.*[\u0021-\u002b\u003c-\u0040])(?=.*[A-Z])(?=.*[a-z])\S{8,254}$')),
    'name': And(str, Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{2,150}')),
    'lastName': And(str, Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{2,150}')),
    'dateBirth': And(str, Regex(r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/((19|20)\d\d)$')),
    'email': And(Use(str), Regex(r'\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b'), lambda e: 255>len(e)>4),
    'id_city': And(int),
    'id_resource': And(int),
    'account_status': And(Use(int), lambda s: 0<s<3),
    'account_type': And(Use(int), lambda t: 0<t<4),
})

#PARA EL NOMBRE ^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$

validator_change_status = Schema({
    'id_account': And(int),
    'status': And(Use(int), lambda s: 0<s<3),
})

validator_email = Schema({
    'email': And(Use(str), Regex(r'\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b'), lambda e: 255>len(e)>4)
})

validator_city = Schema({
    Optional('id_city'): And(int),
    'name': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{5,50}'), lambda e: 51>len(e)>4)
})

validator_country = Schema({
    Optional('id_country'): And(int),
    'name': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{5,50}'), lambda e: 51>len(e)>4)
})

validator_state = Schema({
    Optional('id_state'): And(int),
    'name': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]{5,50}'), lambda e: 51>len(e)>4)
})

validator_cost = Schema({
    Optional('id_cost'): And(int),
    'cost': And(Use(float), lambda co: co<1000),
    'currency': And(Use(str), lambda cu: cu in ('MXN')),
    'id_service': And(int)
})

validator_message = Schema({
    Optional('id_message'): And(int),
    'message': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9#@$!%&/~^.,;:^_{}()=?¡¿/*-+|><°\U00010000-\U0010ffff]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9#@$!%&/~.,;:^_{}()=?¡¿/*-+|><°\U00010000-\U0010ffff]*){1,}'), lambda e: len(e)>0),
    'id_memberATE': And(int),
    'id_request': And(int),
})

validator_rating = Schema({
    Optional('id_rating'): And(int), #Opcional
    'comment': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){5,150}'), lambda e: 151>len(e)>4),
    'rating': And(Use(int),lambda r: 0<r<6),
    'id_request': And(int)
})

validator_report = Schema({
    Optional('id_report'): And(int),
    'reason': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){4,100}'), lambda e: 101>len(e)>3),
    'id_service': And(int),
    'id_memberATE': And(int)
})

validator_request = Schema({
    Optional('id_request'): And(int),
    'address': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9#]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9#]*){2,}'), lambda e: 255>len(e)>9),
    'date': And(str, Regex(r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/((19|20)\d\d)$')),
    'request_status': And(Use(int), lambda s: 0<s<5),
    'time': And(str, Regex(r'^([0-1][1-9]|[2][0-3])(:)([0-5][0-9])(:)([0-5][0-9])$')),
    'trouble': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'), lambda e: 200>len(e)>7),
    'id_memberATE': And(int),
    'id_service': And(int)
})

validator_resource = Schema({
    Optional('id_resource'): And(int),
    'is_main_resource': And(Use(int), lambda m: 0<=m<2),
    'route_rave': And(Use(str), Regex(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'), lambda e: 301>len(e)>3),
    'name': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9.]*){2,}'), lambda e: 151>len(e)>1),
    'id_service': And(int)
})

validator_service = Schema({
    Optional('id_service'): And(int),
    'id_city': And(int),
    'id_memberATE': And(int),
    'name': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'), lambda e: 151>len(e)>4),
    'description': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'), lambda e: 301>len(e)>4),
    'slogan': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'), lambda e: 51>len(e)>4),
    'type_service': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'), lambda e: 151>len(e)>4),
    'working_hours': And(Use(str), Regex(r'^[a-zA-ZÀ-ÿ\u00f1\u00d10-9]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d10-9]*){2,}'), lambda e: 151>len(e)>1),
    'service_status': And(Use(int), lambda n: 4>n>0),
    'minimal_cost': And(float),
    'maximum_cost': And(Use(float), lambda n: n>0)
})