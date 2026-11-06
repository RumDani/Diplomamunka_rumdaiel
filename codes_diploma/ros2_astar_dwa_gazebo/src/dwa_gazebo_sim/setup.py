from glob import glob
import os
from setuptools import find_packages, setup

package_name = "dwa_gazebo_sim"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
        (os.path.join("share", package_name, "config"), ["config/slam.yaml"]),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*.sdf")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "moving_obstacle_node = dwa_gazebo_sim.moving_obstacle_node:main",
            "python_planner_node = dwa_gazebo_sim.python_planner_node:main",
            "python_simulation_node = dwa_gazebo_sim.python_simulation_node:main",
            "lidar_obstacle_node = dwa_gazebo_sim.lidar_obstacle_node:main",
        ],
    },
)
