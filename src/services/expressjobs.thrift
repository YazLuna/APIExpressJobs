namespace py src.services.thrift

typedef i32 int

enum AccountStatus{
    ACTIVE = 1,
    INACTIVE = 2
}

enum AccountType{
     CLIENT = 1,
     EMPLOYEE = 2
}

enum ServiceStatus{
    ACTIVE = 1,
    DELETED = 2
}

enum RequestStatus {
    REQUEST = 1,
    ACCEPTED = 2,
    REJECTED = 3,
    CANCELLED = 4
}

struct Date {
    1: int day,
    2: int month,
    3: int year
}

struct Time {
    1: int hour,
    2: int minutes,
    3: int seconds
}

struct AccountRegistry {
    1: string userName,
    2: string password,
    3: AccountStatus accountStatus,
    4: AccountType accountType
}

struct MemberATERegistryUpdate {
    1: optional string email,
    2: string name,
    3: string lastName,
    4: Date dateBirth,
    5: optional AccountRegistry account
}

struct AccountDelete {
    1: AccountStatus accountStatus,
    2: int idAccount
}

struct Resource {
    1: string routeSave
}

struct ServiceRegistryUpdate {
    1: string name,
    2: string slogan,
    3: double cost,
    4: string description,
    5: string location,
    6: string workinghours,
    7: string typeService,
    8: optional ServiceStatus serviceStatus,
    9: optional list <Resource> resources,
    10: string email,
    11: int idService
}

struct ServiceDelete {
    1: optional ServiceStatus serviceStatus,
    2: string email,
    3: int idService
}

struct ServiceResources {
    1: list <Resource> resources,
    2: string email
}

struct Message {
    1: string message,
    2: string email
}

struct Chat {
    1: optional list <Message> messageClient,
    2: optional list <Message> messageEmployee
}

struct Report {
    1: string reason,
    2: string email,
    3: int idService,
    4: optional int idReport
}

struct RequestRegistry {
    1: string addres,
    2: Date date,
    3: int ratingEmployee,
    4: int ratingClient,
    5: string trouble,
    6: Time time,
    7: RequestStatus requestStatus,
    8: string emailMemberRequest,
    9: int idServiceRequested,
    10: int idReport
}

struct RequestUpdateStatus {
    1: RequestStatus requestStatus,
    2: int idReport
}


service MemberATEServices {
    int RegistryMemberATE(1:MemberATERegistryUpdate member),
    int DeleteMemberATE(1:string email),
    bool ConsultMemberATE(1:string email),
    bool ConsultMembersATE(),
    int UpdateMemberATE(1:MemberATERegistryUpdate member)
}

service ServiceATEServices {
    int RegistryServiceATE(1:ServiceRegistryUpdate serviceRegistry),
    int DeleteServiceATE(1:int idService),
    bool ConsultServiceATE(1:int idService),
    bool ConsultServicesATE(),
    int UpdateServiceATE(1:ServiceRegistryUpdate serviceUpdate)
}

service RequestServices {
    int RegistryRequest(1: RequestRegistry request),
    int UpdateStatusRequest(1: RequestStatus status, 2: int idReport)
}

service MessageServices {
    int GetMessagesChat ()
}

service ReportServices {
    int RegistryReport (1: Report report)
}