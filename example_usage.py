#!/usr/bin/env python3
"""
Example Usage Script for Robot Grid Simulator

This script demonstrates various features of the RobotSimulator class
and shows how to use the different commands and enhancements.
"""

from robot_simulator import RobotSimulator


def demonstrate_basic_movement():
    """Demonstrate basic movement commands."""
    print("=== Basic Movement Demonstration ===")
    robot = RobotSimulator()
    
    print("Initial state:")
    robot.report()
    robot.display_grid()
    
    print("Moving forward...")
    robot.forward()
    robot.display_grid()
    
    print("Turning right...")
    robot.right()
    robot.display_grid()
    
    print("Moving forward again...")
    robot.forward()
    robot.display_grid()
    
    print("Final state:")
    robot.report()
    print()


def demonstrate_diagonal_movement():
    """Demonstrate diagonal movement feature."""
    print("--- Diagonal Movement Demonstration ---")
    robot = RobotSimulator()
    robot.position = (1, 1)  #start at center
    
    print("Starting position:")
    robot.display_grid()
    
    print("Moving northeast...")
    robot.diagonal_move('northeast')
    robot.display_grid()
    
    print("Moving southeast...")
    robot.diagonal_move('southeast')
    robot.display_grid()
    
    print("Moving southwest...")
    robot.diagonal_move('southwest')
    robot.display_grid()
    
    print("Moving northwest...")
    robot.diagonal_move('northwest')
    robot.display_grid()
    
    print("Final state:")
    robot.report()
    print()


def demonstrate_obstacle_management():
    """Demonstrate obstacle management features."""
    print("--- Obstacle Management Demonstration ---")
    robot = RobotSimulator()
    
    print("Initial grid:")
    robot.display_grid()
    
    print("Adding obstacles...")
    robot.add_obstacle((1, 1))
    robot.add_obstacle((2, 2))
    robot.add_obstacle((3, 3))
    robot.display_grid()
    
    print("Trying to move into obstacle...")
    robot.forward()  #should fail
    robot.right()
    robot.forward()  #should fail
    robot.display_grid()
    
    print("Removing obstacle...")
    robot.remove_obstacle((1, 1))
    robot.display_grid()
    
    print("Now can move forward...")
    robot.forward()
    robot.display_grid()
    print()


def demonstrate_battery_simulation():
    """Demonstrate battery simulation feature."""
    print("--- Battery Simulation Demonstration ---")
    robot = RobotSimulator(battery_level=20)  #start with low battery
    
    print("Starting with low battery:")
    robot.report()
    
    print("Moving forward (costs 5% battery)...")
    robot.forward()
    robot.report()
    
    print("Turning left (costs 2% battery)...")
    robot.left()
    robot.report()
    
    print("Moving forward again...")
    robot.forward()
    robot.report()
    
    print("Trying to move with insufficient battery...")
    robot.forward()  #should fail
    robot.report()
    print()


def demonstrate_grid_expansion():
    """Demonstrate grid expansion feature."""
    print("--- Grid Expansion Demonstration ---")
    robot = RobotSimulator(grid_size=3)  #start with small grid
    
    print("Initial 3x3 grid:")
    robot.display_grid()
    
    print("Moving to edge...")
    robot.forward()
    robot.forward()
    robot.display_grid()
    
    print("Expanding grid to 5x5...")
    robot.expand_grid(5)
    robot.display_grid()
    
    print("Now can move further...")
    robot.forward()
    robot.forward()
    robot.display_grid()
    print()


def demonstrate_error_handling():
    """Demonstrate error handling features."""
    print("--- Error Handling Demonstration ---")
    robot = RobotSimulator()
    
    print("Testing boundary checking...")
    #move to edge
    for _ in range(4):
        robot.forward()
    
    print("Trying to move beyond boundary...")
    robot.forward()  #should fail
    robot.report()
    
    print("Testing invalid obstacle placement...")
    robot.add_obstacle((10, 10))  #should fail
    robot.add_obstacle((0, 0))    #should fail (on robot)
    
    print("Testing invalid diagonal direction...")
    robot.diagonal_move('invalid')  #should fail
    
    print("Testing grid expansion with invalid size...")
    robot.expand_grid(3)  #should fail (smaller than current)
    print()


def run_comprehensive_demo():
    """Run a comprehensive demonstration of all features."""
    print("--- Robot Grid Simulator - Comprehensive Demonstration ---")
    print("=" * 60)
    print()
    
    #run all demonstrations
    demonstrate_basic_movement()
    demonstrate_diagonal_movement()
    demonstrate_obstacle_management()
    demonstrate_battery_simulation()
    demonstrate_grid_expansion()
    demonstrate_error_handling()
    
    print("--- Demonstration Complete ---")
    print("All features have been demonstrated successfully!")
    print("You can now run the main simulator with: python3 robot_simulator.py")


if __name__ == "__main__":
    run_comprehensive_demo() 