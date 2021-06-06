namespace py src.services.thrift

typedef i32 int

struct Resource {
    1: int idResource
    2: string routeSave
    3: bool isMainResource
    4: string name
    5: int idService
    6: binary resourceFile
    7: int idMemberATE
}

service ResourcesServices {
    int AddResource (1: Resource resource)
    Resource GetResource (1: string routeSave)
    int DeleteResource (1: string routeSave)
    list<Resource> GetResourcesList(1: list<string> routes)
}