#!/usr/bin/env python3
"""
Robot Grid Simulator
A Python simulator that simulates basic robot movement in a 5x5 grid.

Author: Sondos Ibrahim
"""

import sys
from typing import Tuple, List, Optional
from enum import Enum


class Direction(Enum):
    """Enumeration for robot directions."""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class RobotSimulator:
    """
    Robot Grid Simulator Class
    
    Simulates a robot moving on a 5x5 grid with basic commands:
    - forward: Move one step in current direction
    - left: Turn 90 degrees left
    - right: Turn 90 degrees right
    - report: Display current position and direction
    """
    
    def __init__(self, grid_size: int = 5, battery_level: int = 100):
        """
        Initialize the robot simulator.
        
        Args:
            grid_size (int): Size of the grid (default: 5x5)
            battery_level (int): Initial battery level (default: 100)
        """
        self.grid_size = grid_size
        self.position = (0, 0)  #start at (0, 0)
        self.direction = Direction.NORTH  #start facing NORTH
        self.battery_level = battery_level
        self.obstacles = set()  #set of obstacle positions
        self.movement_cost = 5  #battery cost per movement
        self.turn_cost = 2  #battery cost per turn
        
        # Initialize some obstacles for demonstration
        self._initialize_obstacles()
    
    def _initialize_obstacles(self):
        """Initialize some obstacles on the grid."""
        obstacle_positions = [(1, 1), (2, 3), (3, 1), (4, 4)]
        for pos in obstacle_positions:
            if 0 <= pos[0] < self.grid_size and 0 <= pos[1] < self.grid_size:
                self.obstacles.add(pos)
    
    def _is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        Check if a position is within grid boundaries.
        
        Args:
            position (Tuple[int, int]): Position to check
            
        Returns:
            bool: True if position is valid, False otherwise
        """
        x, y = position
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size
    
    def _is_obstacle(self, position: Tuple[int, int]) -> bool:
        """
        Check if a position contains an obstacle.
        
        Args:
            position (Tuple[int, int]): Position to check
            
        Returns:
            bool: True if obstacle exists, False otherwise
        """
        return position in self.obstacles
    
    def _get_next_position(self) -> Tuple[int, int]:
        """
        Calculate the next position based on current direction.
        
        Returns:
            Tuple[int, int]: Next position coordinates
        """
        x, y = self.position
        
        if self.direction == Direction.NORTH:
            return (x, y + 1)
        elif self.direction == Direction.EAST:
            return (x + 1, y)
        elif self.direction == Direction.SOUTH:
            return (x, y - 1)
        elif self.direction == Direction.WEST:
            return (x - 1, y)
        
        return self.position
    
    def _has_sufficient_battery(self, cost: int) -> bool:
        """
        Check if robot has sufficient battery for an action.
        
        Args:
            cost (int): Battery cost of the action
            
        Returns:
            bool: True if sufficient battery, False otherwise
        """
        return self.battery_level >= cost
    
    def _consume_battery(self, cost: int):
        """
        Consume battery for an action.
        
        Args:
            cost (int): Battery cost to consume
        """
        self.battery_level = max(0, self.battery_level - cost)
    
    def forward(self) -> bool:
        """
        Move the robot one step forward in the current direction.
        
        Returns:
            bool: True if movement successful, False otherwise
        """
        if not self._has_sufficient_battery(self.movement_cost):
            print("ERROR: Insufficient battery for movement!")
            return False
        
        next_position = self._get_next_position()
        
        if not self._is_valid_position(next_position):
            print("ERROR: Cannot move outside grid boundaries!")
            return False
        
        if self._is_obstacle(next_position):
            print("ERROR: Cannot move through obstacle!")
            return False
        
        self.position = next_position
        self._consume_battery(self.movement_cost)
        return True
    
    def left(self) -> bool:
        """
        Turn the robot 90 degrees to the left.
        
        Returns:
            bool: True if turn successful, False otherwise
        """
        if not self._has_sufficient_battery(self.turn_cost):
            print("ERROR: Insufficient battery for turn!")
            return False
        
        #turn left (counter-clockwise)
        self.direction = Direction((self.direction.value - 1) % 4)
        self._consume_battery(self.turn_cost)
        return True
    
    def right(self) -> bool:
        """
        Turn the robot 90 degrees to the right.
        
        Returns:
            bool: True if turn successful, False otherwise
        """
        if not self._has_sufficient_battery(self.turn_cost):
            print("ERROR: Insufficient battery for turn!")
            return False
        
        #turn right (clockwise)
        self.direction = Direction((self.direction.value + 1) % 4)
        self._consume_battery(self.turn_cost)
        return True
    
    def report(self):
        """
        Report the current position and direction of the robot.
        """
        direction_names = {
            Direction.NORTH: "NORTH",
            Direction.EAST: "EAST", 
            Direction.SOUTH: "SOUTH",
            Direction.WEST: "WEST"
        }
        
        print(f"Position: {self.position}")
        print(f"Direction: {direction_names[self.direction]}")
        print(f"Battery: {self.battery_level}%")
    
    def diagonal_move(self, direction: str) -> bool:
        """
        Move the robot diagonally (optional enhancement).
        
        Args:
            direction (str): Diagonal direction ('northeast', 'northwest', 'southeast', 'southwest')
            
        Returns:
            bool: True if movement successful, False otherwise
        """
        if not self._has_sufficient_battery(self.movement_cost * 1.5):
            print("ERROR: Insufficient battery for diagonal movement!")
            return False
        
        x, y = self.position
        next_position = self.position
        
        if direction == 'northeast':
            next_position = (x + 1, y + 1)
        elif direction == 'northwest':
            next_position = (x - 1, y + 1)
        elif direction == 'southeast':
            next_position = (x + 1, y - 1)
        elif direction == 'southwest':
            next_position = (x - 1, y - 1)
        else:
            print("ERROR: Invalid diagonal direction!")
            return False
        
        if not self._is_valid_position(next_position):
            print("ERROR: Cannot move outside grid boundaries!")
            return False
        
        if self._is_obstacle(next_position):
            print("ERROR: Cannot move through obstacle!")
            return False
        
        self.position = next_position
        self._consume_battery(int(self.movement_cost * 1.5))
        return True
    def add_obstacle(self, position: Tuple[int, int]) -> bool:
        """
        Add an obstacle to the grid (optional enhancement).
        
        Args:
            position (Tuple[int, int]): Position to add obstacle
            
        Returns:
            bool: True if obstacle added successfully, False otherwise
        """
        if not self._is_valid_position(position):
            print("ERROR: Invalid position for obstacle!")
            return False
        
        if position == self.position:
            print("ERROR: Cannot place obstacle on robot position!")
            return False
        
        self.obstacles.add(position)
        return True
    
    def remove_obstacle(self, position: Tuple[int, int]) -> bool:
        """
        Remove an obstacle from the grid (optional enhancement).
        
        Args:
            position (Tuple[int, int]): Position to remove obstacle
            
        Returns:
            bool: True if obstacle removed successfully, False otherwise
        """
        if position in self.obstacles:
            self.obstacles.remove(position)
            return True
        else:
            print("ERROR: No obstacle at specified position!")
            return False
    
    def expand_grid(self, new_size: int) -> bool:
        """
        Expand the grid size (optional enhancement).
        
        Args:
            new_size (int): New grid size
            
        Returns:
            bool: True if grid expanded successfully, False otherwise
        """
        if new_size <= self.grid_size:
            print("ERROR: New grid size must be larger than current size!")
            return False
        
        self.grid_size = new_size
        return True
    
    def display_grid(self):
        """
        Display the current state of the grid with robot position and obstacles.
        """
        print("\n" + "=" * (self.grid_size * 3 + 1))
        for y in range(self.grid_size - 1, -1, -1):
            row = "|"
            for x in range(self.grid_size):
                if (x, y) == self.position:
                    # Show robot with direction indicator
                    direction_symbols = {
                        Direction.NORTH: "↑",
                        Direction.EAST: "→",
                        Direction.SOUTH: "↓",
                        Direction.WEST: "←"
                    }
                    row += f" {direction_symbols[self.direction]} |"
                elif (x, y) in self.obstacles:
                    row += " X |"
                else:
                    row += "   |"
            print(row)
            if y > 0:
                print("-" * (self.grid_size * 3 + 1))
        print("=" * (self.grid_size * 3 + 1))
        print(f"Battery: {self.battery_level}%")
        print()

def parse_command(command: str) -> Tuple[str, List[str]]:
    """
    Parse a command string into action and arguments.
    
    Args:
        command (str): Command string to parse
        
    Returns:
        Tuple[str, List[str]]: Action and arguments
    """
    parts = command.strip().lower().split()
    if not parts:
        return "", []
    
    action = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    return action, args


def main():
    """
    Main function to run the robot simulator.
    """
    print("=== Robot Grid Simulator ===")
    print("Commands: forward, left, right, report, diagonal <direction>, add_obstacle <x> <y>")
    print("Diagonal directions: northeast, northwest, southeast, southwest")
    print("Type 'quit' to exit")
    print()
    
    #initialize the robot simulator
    robot = RobotSimulator()
    
    #display initial grid
    robot.display_grid()
    
    while True:
        try:
            command = input("Enter command: ").strip()
            
            if not command:
                continue
            
            if command.lower() == 'quit':
                print("Goodbye!")
                break
            
            action, args = parse_command(command)
            
            if action == 'forward':
                robot.forward()
            elif action == 'left':
                robot.left()
            elif action == 'right':
                robot.right()
            elif action == 'report':
                robot.report()
            elif action == 'diagonal':
                if args:
                    robot.diagonal_move(args[0])
                else:
                    print("ERROR: Diagonal direction required!")
            elif action == 'add_obstacle':
                if len(args) == 2:
                    try:
                        x, y = int(args[0]), int(args[1])
                        robot.add_obstacle((x, y))
                    except ValueError:
                        print("ERROR: Invalid coordinates!")
                else:
                    print("ERROR: Two coordinates required!")
            elif action == 'remove_obstacle':
                if len(args) == 2:
                    try:
                        x, y = int(args[0]), int(args[1])
                        robot.remove_obstacle((x, y))
                    except ValueError:
                        print("ERROR: Invalid coordinates!")
                else:
                    print("ERROR: Two coordinates required!")
            elif action == 'expand':
                if args:
                    try:
                        new_size = int(args[0])
                        robot.expand_grid(new_size)
                    except ValueError:
                        print("ERROR: Invalid grid size!")
                else:
                    print("ERROR: Grid size required!")
            elif action == 'display':
                robot.display_grid()
            else:
                print(f"ERROR: Unknown command '{action}'")
            
            #display updated grid after each command
            robot.display_grid()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main() 
