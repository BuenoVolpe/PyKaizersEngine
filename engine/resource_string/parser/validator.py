from engine.utils.log import printlog
#============================================================#
class ResourceStringValidator:
    #============================================================#
    def __init__(self, separators):
        self.seps = separators
    #============================================================#
    def verify(self, resource_string: str) -> bool:
        #------------------------------------------------------------#
        if not isinstance(resource_string, str):
            printlog.error(
                "resource string must be a string!"
            )
            return False
        #------------------------------------------------------------#
        if not resource_string.strip():
            printlog.error(
                "resource string is empty!"
            )
            return False
        #------------------------------------------------------------#
        if self.seps.type not in resource_string:
            printlog.error(
                f"resource string {resource_string} "
                f"is missing its type separator!"
            )
            return False
        #------------------------------------------------------------#
        if self.seps.namespace not in resource_string:
            printlog.error(
                f"resource string {resource_string} "
                f"is missing its namespace separator!"
            )
            return False
        #------------------------------------------------------------#
        return True
#============================================================#
