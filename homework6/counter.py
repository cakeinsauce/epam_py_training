"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Ниже пример использования
"""


def instances_counter(cls):
    """Class decorator to keep quantity of class instances."""

    class Wrapper:
        __instances_amt = 0

        def __init__(self, *args, **kwargs):
            Wrapper.__instances_amt += 1
            self.wrap = cls(*args, **kwargs)

        @classmethod
        def get_created_instances(cls):
            return cls.__instances_amt

        @classmethod
        def reset_instances_counter(cls):
            before_reset, cls.__instances_amt = cls.__instances_amt, 0
            return before_reset

    return Wrapper


#
#
# if __name__ == "__main__":
#
#     User.get_created_instances()  # 0
#     user, _, _ = User(), User(), User()
#     user.get_created_instances()  # 3
#     user.reset_instances_counter()  # 3
