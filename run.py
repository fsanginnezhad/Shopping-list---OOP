import os
import json
from getpass import getpass


class DataBaseJson:
    def __init__(self, name) -> None:
        self._name = name

    def readable(self) -> dict:
        with open(self._name+'.json', 'r') as file:
            basket_list = json.load(file)
        return basket_list

    def execute(name_json: str, basket_list: dict) -> None:
        with open(name_json+'.json', 'w') as file:
            json.dump(basket_list, file, indent=4)


class Basket:
    def __init__(self, basket: dict) -> None:
        self._basket = basket

    @property
    def name(self):
        return self._basket


class Group(Basket):
    def __init__(self, basket: Basket) -> None:
        super().__init__(basket)
        self._group = ''
        self._product = ''
        self._products = ''
        self._groups = ''

    def show_groups_products(self) -> str:
        self._products = ''
        for index, group in enumerate(self._basket, start=1):
            self._products += f'{index}: {group}\n'
            for index, product in enumerate(self._basket[group], start=1):
                price = self._basket[group][product]["price"]
                number = self._basket[group][product]["number"]
                discount = self._basket[group][product]["discount"]
                self._products += f'\t{index}: {product} -> Price: {price:,} number: {number} and discpunt: {discount}\n'  # noqa E501
        return self._products

    def show_groups(self) -> str:
        self._groups = ''
        for index, group in enumerate(self._basket, start=1):
            self._groups += f'{index}: {group}\n'
        return self._groups

    def show_products(self) -> str:
        self._products = ''
        index = 1
        for group in self._basket:
            for product in self._basket[group]:
                price = self._basket[group][product]["price"]
                number = self._basket[group][product]["number"]
                discount = self._basket[group][product]["discount"]
                self._products += f'\t{index}: {product} -> Price: {price:,} number: {number} and discpunt: {discount}\n'  # noqa E501
                index += 1
        return self._products

    def add_group(self, group: str) -> None | str:
        if group not in self._basket.keys():
            self._basket[group] = {}
        elif group in self._basket.keys():
            raise Exception(
                f'Cannot added {group}. The {group} is exist.'
            )

    def get_group(self, group: str | int) -> str:
        for index, _group in enumerate(self._basket, start=1):
            if group.isnumeric():
                if index == int(group):
                    self._group = _group
                    return self._group
            elif group.isalpha():
                if _group == group:
                    self._group = _group
                    return self._group
        else:
            raise Exception('Not Found.')

    def deleted_group(self, group: str) -> None:
        self._basket.pop(group)

    def get_group_by_product(self, product: str) -> str:
        for group in self._basket:
            for _product in self._basket[group]:
                if product == _product:
                    self._product = _product
                    return self._product
        else:
            raise Exception('Not Found.')

    def edited_group(self, group: str, new_group: str) -> None:
        self._basket[new_group] = self._basket.pop(group)

    def add_product(
        self,
        group: str,
        product_name: str,
        price: int,
        number: int,
        discount: int
    ) -> None:
        self._basket[group].update(
            {product_name: {
                'price': price,
                'number': number,
                'discount': discount
            }}
        )

    def get_product(self, product: str | int) -> str:
        index = 1
        for _group in self._basket:
            for index, _product in enumerate(self._basket[_group], start=1):
                if product.isnumeric():
                    if index == int(product):
                        self._product = _product
                        return self._product
                elif product.isalpha():
                    if _product == product:
                        self._product = _product
                        return self._product
                index += 1
        else:
            raise Exception('Not Found.')

    def edit_product(
            self,
            group: str,
            new_product: str,
            product: str
    ) -> None:
        self._basket[group][new_product] = self._basket[group].pop(product)

    def deleted_product(self, group: str, product: str) -> None:
        self._basket[group].pop(product)


class Shopping_list(Basket):
    def __init__(self, basket: Basket) -> None:
        super().__init__(basket)
        self._shopping_list = {}
        self._products = ''

    @property
    def show_list(self):
        for index, product in enumerate(self._shopping_list, start=1):
            number = self._shopping_list[product]
            self._products += f'\t{index}: {product}: {number}'
        return self._products

    def add_product(self, group: str, product: str, numbers: int) -> None:
        number = self._basket[group][product]['number']
        if number > 0 and numbers <= number:
            if product not in self._shopping_list:
                self._shopping_list.update({product: numbers})
            elif product in self._shopping_list:
                self._shopping_list[product] += numbers
            number -= numbers
            self._basket[group][product]["number"] = number
        else:
            raise Exception(
                f'Sorry, the "{product}" product has only "{number}" items in stock.'  # noqa E501
            )


class App:
    def __init__(self) -> None:
        pass

    @staticmethod
    def clear_screen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def keep() -> None:
        getpass('Press ENTER to continue...')

    @staticmethod
    def admin_menu(group: Group):
        message = 'Enter `Group` or `product` or `Show` or `Back`: '
        while True:
            App.clear_screen()
            print('Welcome to Admin Menu.')
            App.help_admin_group()
            command = input(message).casefold()
            if command in BACK_COMMANDS:
                break
            elif command == 'group':
                App.group_menu(group)
            elif command == 'product':
                App.product_menu(group)
            elif command == 'show':
                print(group.show_groups_products())
                App.keep()

    @staticmethod
    def group_menu(group: Group) -> None:
        message = 'Enter `Add` or `Show` or `Remove` or `Edit` or `Back`: '
        while True:
            App.clear_screen()
            print('Welcome to Group Menu.')
            App.help_group_add()
            command = input(message).casefold()
            if command in BACK_COMMANDS:
                break
            elif command == 'add':
                group_name = input('Enter your Name Group: ')
                group.add_group(group_name)
                print(f'Successfully The `{group_name}` added to basket!')
                App.keep()
            elif command == 'show':
                print(group.show_groups())
                App.keep()
            elif command == 'remove':
                print(group.show_groups())
                group_name = input('Enter your Name Group for Delete: ')
                group.deleted_group(group_name)
                print(f'The `{group_name}` deleted from basket.')
                App.keep()
            elif command == 'edit':
                print(group.show_groups())
                group_name = input('Enter your Name Group for Edit: ')
                new_group = input('Enter your New Name Group: ')
                group.edited_group(group_name, new_group)
                print(f'The `{group_name}` edited to `{new_group}`')
                App.keep()

    @staticmethod
    def product_menu(group: Group) -> None:
        message = 'Enter `Add` or `Show` or `Remove` or `Edit` or `Back`: '
        while True:
            App.clear_screen()
            print('Welcome to Product Menu.')
            App.help_product()
            command = input(message).casefold()
            if command in BACK_COMMANDS:
                break
            elif command == 'add':
                print(group.show_groups())
                group_name = input('Enter your Name Group: ')
                print(group.show_products)
                product_name = input('Enter your Name Product: ')
                price = input('How much is it: ')
                number = input('How many of Product: ')
                discount = input('Enter your discount for Product: ')
                group.add_product(
                    group_name,
                    product_name,
                    int(price),
                    int(number),
                    int(discount))
                print(
                    f'Excellent The `{product_name}` added to `{group_name}`!'
                )
                App.keep()
            elif command == 'show':
                print(group.show_products())
                App.keep()
            elif command == 'remove':
                print(group.show_products())
                product_name = input('Enter your Product Name for Delete: ')
                group_name = group.get_group_by_product(product)
                group.deleted_product(group_name, product_name)
                print(f'The `{product_name}` deleted from `{group_name}`.')
                App.keep()
            elif command == 'edit':
                print(group.show_products())
                product_name = input('Enter your Product Name for Edit: ')
                product = group.get_product(product_name)
                group_name = group.get_group_by_product(product)
                new_product = input('Enter your New Product Name: ')
                group.edit_product(group, new_product, product)
                print(f'The `{product}` edited to `{new_product}`')
                App.keep()

    # def title(title: str = '-') -> str:
    #     return f'---{title}---------------------------------------------------------------------'  # noqa E501

    # def decortor_exceptions(func):
    #     @functools.wraps(func)
    #     def exception(*args, **kwargs):
    #         try:
    #             func(*args, **kwargs)
    #         except GroupNameError as e:
    #             show_error(e)
    #         except GroupDoesNotExist as e:
    #             show_error(e)
    #         except ProductDoesExist as e:
    #             show_error(e)
    #         except ProductNameError as e:
    #             show_error(e)
    #         except NotNumber as e:
    #             show_error(e)
    #         except ProductDoesNotExist as e:
    #             show_error(e)
    #         except Exception as e:
    #             show_error('500! please contact administrator')
    #     return exception

    # def show_error(message):
    #     print(f'Error: {message}!')
    #     keep()

    @staticmethod
    def show_help() -> str:
        print('''
        1. Use "Admin" to add groups and products to the warehouse.
        2. Use the "Store" to buy products from the warehouse.
        ''')

    @staticmethod
    def help_admin() -> None:
        print('''
        By default, there is no group in the application.
        And as you can see, you cannot add a product until you have a group.
        You must first add grouping to the application.

        Use "Group" to add and "Back" to return to main menu.
        ''')

    @staticmethod
    def help_admin_group() -> None:
        print('''
        1. If you want to go to the groups menu, use "Group".
        2. If you want to go to the product menu, use "Product".
        3. If you want to see groups and products, use "show".
        3. If you want to go to the main menu, use "Back".
        ''')

    @staticmethod
    def help_group_add() -> None:
        print('''
        1. If you want to add grouping, use "Add".
        2. If you want to show all Groups, use "Show".
        3. If you want to remove group, use "remove".
        4. If you want to edit group, use "edit".
        5. If you want to go to the previous menu, use "Back".
        ''')

    # def help_group() -> None:
    #     print('''
    #     1. If you want to add grouping, use "Add".
    #     2. If you want to modify the grouping, use "Edit".
    #     3. If you want to deleted the grouping, use "Delete".
    #     4. If you want to see the list of groups, use the "Show".
    #     5. If you want to go to the previous menu, use "Back".
    #     ''')

    @staticmethod
    def help_product() -> None:
        print('''
        1. If you want to add products to the warehouse, use "Add".
        2. If you want to modify warehouse products, use "Edit".
        3. If you want to remove product, use "remove".
        4. If you want to see the list of products, use the "Show".
        5. If you want to go to the previous menu, use "Back".
        ''')

    # def help_product_empty() -> None:
    #     print('''
    #     1. If you want to add products to the warehouse, use "Add".
    #     3. If you want to see the list of products along with the grouping, use the "Show". # noqa E501
    #     4. If you want to go to the previous menu, use "Back".
    #     ''')

    # def help_store() -> None:
    #     print('''
    #                 <<< Welcome to the Store >>>

    #     1. Use "Add" to make a shopping list from the warehouse.
    #     2. Use "Show" to view the shopping list.
    #     3. Use "Delete" to remove the product from the shopping list.
    #     4. Use "Search" to check if a product is in the shopping list or not.
    #     5. Use "Total" to view the payable amount.
    #     6. Use "Back" to return to the main menu.
    #     ''')

    # def help_store_empty() -> None:
    #     print('''
    #                 <<< Welcome to the Store >>>

    #     1. Use "Add" to make a shopping list from the warehouse.
    #     2. Use "Show" to view the shopping list.
    #     3. Use "Total" to view the payable amount.
    #     4. Use "Back" to return to the main menu.
    #     ''')


EXIT_COMMANDS = ('q', 'e', 'quit', 'exit')
BACK_COMMANDS = ('b', 'back')


def main():
    database = DataBaseJson('basket_list')
    basket_list = database.readable()
    basket = Basket(basket_list)
    group = Group(basket.name)
    while True:
        App.clear_screen()
        App.show_help()
        command = input('Enter `Admin` or `Store` or `Quit`: ').casefold()
        if command in EXIT_COMMANDS:
            break
        elif command == 'admin':
            try:
                App.admin_menu(group)
            except:
                print('Error 504!')
                App.keep()
        elif command == 'store':
            print('Loading...')
            App.keep()


if __name__ == '__main__':
    main()
