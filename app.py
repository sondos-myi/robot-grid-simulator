from flask import Flask, render_template, request, jsonify
from robot_simulator import RobotSimulator, Direction

app = Flask(__name__)

# Initialize the robot (we'll use a global instance for simplicity)
robot = RobotSimulator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def handle_command():
    command = request.json.get('command')
    args = request.json.get('args', [])
    
    response = {'success': False, 'message': '', 'state': None}
    
    try:
        if command == 'forward':
            response['success'] = robot.forward()
            response['message'] = "Moved forward" if response['success'] else "Movement failed"
        elif command == 'left':
            response['success'] = robot.left()
            response['message'] = "Turned left" if response['success'] else "Turn failed"
        elif command == 'right':
            response['success'] = robot.right()
            response['message'] = "Turned right" if response['success'] else "Turn failed"
        elif command == 'report':
            robot.report()
            response['success'] = True
            response['message'] = "Report generated"
        elif command == 'diagonal':
            if args:
                response['success'] = robot.diagonal_move(args[0])
                response['message'] = f"Moved diagonally {args[0]}" if response['success'] else "Diagonal move failed"
            else:
                response['message'] = "Missing direction for diagonal move"
        elif command == 'add_obstacle':
            if len(args) == 2:
                response['success'] = robot.add_obstacle((int(args[0]), int(args[1])))
                response['message'] = "Obstacle added" if response['success'] else "Failed to add obstacle"
            else:
                response['message'] = "Invalid coordinates for obstacle"
        elif command == 'remove_obstacle':
            if len(args) == 2:
                response['success'] = robot.remove_obstacle((int(args[0]), int(args[1])))
                response['message'] = "Obstacle removed" if response['success'] else "Failed to remove obstacle"
            else:
                response['message'] = "Invalid coordinates for obstacle"
        elif command == 'expand':
            if args:
                response['success'] = robot.expand_grid(int(args[0]))
                response['message'] = "Grid expanded" if response['success'] else "Failed to expand grid"
            else:
                response['message'] = "Missing grid size"
        else:
            response['message'] = f"Unknown command: {command}"
        
        # Get current state for UI update
        response['state'] = {
            'position': robot.position,
            'direction': robot.direction.name,
            'battery': robot.battery_level,
            'grid_size': robot.grid_size,
            'obstacles': list(robot.obstacles)
        }
        
    except Exception as e:
        response['message'] = f"Error: {str(e)}"
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)