import random
import arcade

# Определение размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
POINT_COUNT = 40
POINT_NORMAL_SIZE = 0.1
POINT_MOVEMENT_SPEED = 0.2

# Настройки здоровья точек
POINT_HEALTH_POINTS = 70
POINT_HEALTH_POINTS_VARIABILITY = 5
HOW_MANY_HEALTH_POINTS_WILL_ONE_ILLNESS_INCIDENT_TAKE = 5
START_NUMBER_OF_SICK_POINTS = 5
SICK_POINT_SIZE = 0.8

class MyGame(arcade.Window):
    """
    Основной класс приложения, унаследованный от arcade.Window.
    Отвечает за управление игровым процессом, включая рендеринг и обновление объектов.
    """

    def __init__(self, width, height):
        """
        Инициализация нового окна игры.

        Args:
            width (int): Ширина окна.
            height (int): Высота окна.
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.AMAZON)
        self.text = 'Waiting for click...'

    def setup(self):
        """
        Настройка начального состояния игры, создание и расстановка точек.
        Создает фиксированное количество точек в случайных местоположениях.
        Определенное количество точек делается 'заболевшими', окрашиваясь в красный цвет.
        """
        self.point_list = arcade.SpriteList()
        number_of_created_sick_points = 0

        for i in range(POINT_COUNT):
            point = arcade.Sprite("asset/point.png", POINT_NORMAL_SIZE)
            point.center_x = random.randrange(SCREEN_WIDTH)
            point.center_y = random.randrange(SCREEN_HEIGHT)
            point.change_x = random.uniform(-POINT_MOVEMENT_SPEED, POINT_MOVEMENT_SPEED)
            point.change_y = random.uniform(-POINT_MOVEMENT_SPEED, POINT_MOVEMENT_SPEED)

            if number_of_created_sick_points >= START_NUMBER_OF_SICK_POINTS:
                point.properties['is_sick'] = False
            else:
                point.properties['is_sick'] = True
                point.color = arcade.csscolor.RED
                number_of_created_sick_points += 1

            point.properties['health_points'] = random.uniform(POINT_HEALTH_POINTS - POINT_HEALTH_POINTS_VARIABILITY, POINT_HEALTH_POINTS + POINT_HEALTH_POINTS_VARIABILITY)
            self.point_list.append(point)

    def on_draw(self):
        """
        Рендеринг экрана. Вызывается при каждой отрисовке кадра.
        Отображает все текущие точки и их состояние.
        """
        arcade.start_render()
        self.point_list.draw()
        arcade.draw_text("Осталось точек: " + str(len(self.point_list)), 80, 20, arcade.color.BLACK, 12, anchor_x='center')

    def update(self, delta_time):
        """
        Обновление состояния игры. Вызывается при каждом кадре.

        Args:
            delta_time (float): Время в секундах с момента последнего обновления.
        Описывает движение точек и реализует логику взаимодействия между заболевшими и здоровыми точками.
        """
        for point in self.point_list:
            point.center_x += point.change_x
            point.center_y += point.change_y

            # Если точка дошла до угла, я ее разворачиваю
            if point.center_x <= 0 or point.center_x >= SCREEN_WIDTH:
                point.change_x = -point.change_x

            if point.center_y <= 0 or point.center_y >= SCREEN_HEIGHT:
                point.change_y = -point.change_y

            # Логика болезней
            # Для больных точек меняю размер, выздоровевших возвращаю в нормальный
            if point.properties['is_sick']:
                point.scale = SICK_POINT_SIZE
                point.filename = arcade.load_texture("asset/sick.png")
            else:
                point.scale = POINT_NORMAL_SIZE
                point.filename = "asset/point.png"

            if point.properties['health_points'] <= 0:
                point.kill()

        # Заражение -----------------------------------------------------------------------------------------------
        # Для всех зараженных точек проверяю контакты, если ни контактируют со здоровыми, здоровых нужно заразить
        for first_point in self.point_list:
            if first_point.properties['is_sick']:
                contact_points = arcade.check_for_collision_with_list(first_point, sprite_list=self.point_list)
                if len(contact_points) > 0:
                    for point_for_sick in contact_points:
                        if not point_for_sick.properties['is_sick']:
                            print("new sick point")
                            point_for_sick.properties['is_sick'] = True
                            point_for_sick.properties['health_points'] -= HOW_MANY_HEALTH_POINTS_WILL_ONE_ILLNESS_INCIDENT_TAKE


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()