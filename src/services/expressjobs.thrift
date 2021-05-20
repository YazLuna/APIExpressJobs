namespace py src.services.thrift

typedef i32 int

struct Resource {
    1: int idResource
    2: string routeSave
    3: bool isMainResource
    4: string name
    5: int idService
}

service ResourcesServices {
    int AddResource (1: Resource resource)
    int GetResource (1: Resource resource)
    int DeleteResource (1: Resource resource)
    int GetResourcesList(1: int idService)
}