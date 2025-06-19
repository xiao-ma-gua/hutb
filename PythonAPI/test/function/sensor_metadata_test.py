# PR: https://github.com/carla-simulator/carla/pull/8935
# 测试传感器元数据和世界元数据不一致的情况
import os
import time

import carla

LOGS = {}


def log(source: str, frame: int, timestamp: float, x_pos: float):
    if source not in LOGS:
        LOGS[source] = []
    LOGS[source].append(f'{frame: >6} | {timestamp:.5f} | {x_pos}')


def flush_log():
    for source, LOG in LOGS.items():
        print(f'{source}:')
        print(f'{"frame": >6} | {"time": <7} | x_pos')
        print('\n'.join(LOG))
        print()


def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(20)
    world = client.reload_world()

    # 设置帧率(FPS)为 20 的同步模式
    world_fps = 20
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 1. / world_fps
    world.apply_settings(settings)
    world.tick()

    # 创建结果目录
    res_dir = os.path.abspath(f'sensor-metadata-test-{client.get_server_version()}')
    if not os.path.isdir(res_dir):
        os.makedirs(res_dir)

    # 传感器回调将图像数据写入磁盘并将元数据记录到标准输出
    # 使用移动索引代替帧号，因为最后一个不可靠（我们想在这里展示）
    image_index = 0

    def cam_callback(image):
        nonlocal image_index
        image.save_to_disk(f'{res_dir}/{image_index}.png')
        image_index += 1
        log('Sensor', image.frame, image.timestamp, image.transform.location.x)

    # 在原点处生成一个相机，但略微抬升
    sensor_transform = carla.Transform(carla.Location(z=2), carla.Rotation())
    cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    sensor = world.spawn_actor(cam_bp, sensor_transform)
    sensor.listen(cam_callback)

    # 我们将执行一些节拍操作并移动相机，同时记录来自世界的元数据
    num_ticks = 10
    for _ in range(num_ticks):
        sensor_transform.location.x += 1
        sensor.set_transform(sensor_transform)
        world.tick()
        world_snapshot = world.get_snapshot()
        actor_snapshot = world_snapshot.find(sensor.id)
        log('World', world_snapshot.frame, world_snapshot.timestamp.elapsed_seconds,
            actor_snapshot.get_transform().location.x)

    # 等待回调完成所有预期的节拍信号
    while image_index < num_ticks:
        time.sleep(0.2)

    flush_log()

    # 清理
    sensor.destroy()
    settings.synchronous_mode = False
    settings.fixed_delta_seconds = None
    world.apply_settings(settings)


if __name__ == '__main__':
    main()
