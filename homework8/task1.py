class KeyValueStorage:
    """
    Class to store values from key-value - like file.
    """

    def __init__(self, file_path):
        """
        Creates attributes associated with the class from dict-like file.

        :type file_path: str
        :param file_path: path of the file.

        :raises: ValueError: if value cannot be assigned to an attribute.
        """

        with open(file_path, "r") as f_o:
            for line in f_o.readlines():
                k_v = [
                    int(i) if i.isdigit() else i for i in line.rstrip("\n").split("=")
                ]
                try:
                    if k_v[0] not in dir(self):  # Attribute is not built-in.
                        setattr(self, k_v[0], k_v[1])
                except (TypeError, AttributeError):
                    raise ValueError

    def __getitem__(self, key):
        """
        Return the object value with an index key.

        :type key: str
        :param key: attribute of the object.

        :return: return object attribute value with an index key.
        :rtype: str | int
        """

        return self.__dict__[key]
