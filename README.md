# Robot Grid Simulator

## Project Title and Purpose

**Robot Grid Simulator** is a Python-based simulation environment designed for AI & ROS2 Integration Training. This project provides a foundational exercise for understanding robot control systems before advancing to more complex ROS2 implementations.

### Key Features

- **5x5 Grid Environment**: Simulates a robot moving on a configurable grid
- **Basic Movement Commands**: forward, left, right, report
- **Boundary Detection**: Prevents robot from moving outside grid boundaries
- **Error Handling**: Comprehensive exception handling for invalid commands
- **Enhancements**: Battery simulation, diagonal movement, obstacles, grid expansion

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- No additional dependencies required (uses only standard library)

### Running the Simulator

1. Clone or download the project files
2. Navigate to the project directory
3. Run the simulator:

```bash
python3 robot_simulator.py
```

## Usage Instructions

### Basic Commands

| Command | Description |
|---------|-------------|
| `forward` | Move robot one step in current direction |
| `left` | Turn robot 90 degrees left |
| `right` | Turn robot 90 degrees right |
| `report` | Display current position, direction, and battery level |
| `quit` | Exit the simulator |

### Advanced Commands

| Command | Description |
|---------|-------------|
| `diagonal <direction>` | Move diagonally (northeast, northwest, southeast, southwest) |
| `add_obstacle <x> <y>` | Add obstacle at specified coordinates |
| `remove_obstacle <x> <y>` | Remove obstacle at specified coordinates |
| `expand <size>` | Expand grid to new size |
| `display` | Show current grid state |


## Feature Descriptions

### Core Features

1. **RobotSimulator Class**: Main class handling robot state and movement
2. **Direction Enum**: Manages robot orientation (NORTH, EAST, SOUTH, WEST)
3. **Boundary Checking**: Prevents movement outside grid limits
4. **Command Parsing**: Robust input handling with error recovery


## Code Structure

```
robot_simulator.py
├── Direction (Enum)
│   ├── NORTH, EAST, SOUTH, WEST
├── RobotSimulator (Class)
│   ├── __init__() - Initialize robot state
│   ├── forward() - Move forward
│   ├── left() - Turn left
│   ├── right() - Turn right
│   ├── report() - Display status
│   ├── diagonal_move() - Diagonal movement
└── main() - Command loop and user interface
```

