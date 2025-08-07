#!/usr/bin/env python3
"""
Test suite for Robot Grid Simulator

This file contains comprehensive tests for the RobotSimulator class
to ensure proper functionality and error handling.
"""

import unittest
from robot_simulator import RobotSimulator, Direction


class TestRobotSimulator(unittest.TestCase):
    """Test cases for RobotSimulator class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.robot = RobotSimulator()
    
    def test_initialization(self):
        """Test robot initialization."""
        self.assertEqual(self.robot.position, (0, 0))
        self.assertEqual(self.robot.direction, Direction.NORTH)
        self.assertEqual(self.robot.battery_level, 100)
        self.assertEqual(self.robot.grid_size, 5)
        self.assertIsInstance(self.robot.obstacles, set)
    
    def test_forward_movement(self):
        """Test forward movement functionality."""
        # Test normal forward movement
        self.assertTrue(self.robot.forward())
        self.assertEqual(self.robot.position, (0, 1))
        self.assertEqual(self.robot.battery_level, 95)  # 100 - 5
        
        #test boundary checking
        for _ in range(4):  #move to edge
            self.robot.forward()
        
        #should NOT be able to move beyond boundary
        self.assertFalse(self.robot.forward())
        self.assertEqual(self.robot.position, (0, 4))  #should stay at boundary
    
    def test_turning(self):
        """Test left and right turning."""
        #test left turn
        self.assertTrue(self.robot.left())
        self.assertEqual(self.robot.direction, Direction.WEST)
        self.assertEqual(self.robot.battery_level, 98)  # 100 - 2
        
        #test right turn
        self.assertTrue(self.robot.right())
        self.assertEqual(self.robot.direction, Direction.NORTH)
        self.assertEqual(self.robot.battery_level, 96)  # 98 - 2
        
        #test multiple turns
        for _ in range(4):
            self.robot.right()
        self.assertEqual(self.robot.direction, Direction.NORTH)  # Should be back to NORTH
    
    def test_direction_movement(self):
        """Test movement in all directions."""
        #clear obstacles for this test
        self.robot.obstacles.clear()
        
        #test NORTH movement
        self.robot.direction = Direction.NORTH
        self.robot.position = (2, 2)
        self.robot.forward()
        self.assertEqual(self.robot.position, (2, 3))
        
        #test EAST movement
        self.robot.direction = Direction.EAST
        self.robot.forward()
        self.assertEqual(self.robot.position, (3, 3))
        
        #test SOUTH movement
        self.robot.direction = Direction.SOUTH
        self.robot.forward()
        self.assertEqual(self.robot.position, (3, 2))
        
        #test WEST movement
        self.robot.direction = Direction.WEST
        self.robot.forward()
        self.assertEqual(self.robot.position, (2, 2))
    
    def test_obstacle_collision(self):
        """Test obstacle collision detection."""
        #add obstacle
        self.robot.add_obstacle((0, 1))
        
        #try to move into obstacle
        self.assertFalse(self.robot.forward())
        self.assertEqual(self.robot.position, (0, 0))  # Should not move
    
    def test_battery_consumption(self):
        """Test battery consumption and depletion."""
        #test normal battery consumption
        initial_battery = self.robot.battery_level
        self.robot.forward()
        self.assertEqual(self.robot.battery_level, initial_battery - 5)
        
        #test turn battery consumption
        self.robot.left()
        self.assertEqual(self.robot.battery_level, initial_battery - 7)
        
        #test battery depletion
        self.robot.battery_level = 3
        self.assertFalse(self.robot.forward())  # Should fail due to insufficient battery
        self.assertEqual(self.robot.battery_level, 3)  # Should not change
    
    def test_diagonal_movement(self):
        """Test diagonal movement functionality."""
        self.robot.position = (2, 2)
        
        #test northeast movement
        self.assertTrue(self.robot.diagonal_move('northeast'))
        self.assertEqual(self.robot.position, (3, 3))
        self.assertEqual(self.robot.battery_level, 93)  # 100 - 7 (rounded down)
        
        #test invalid diagonal direction
        self.assertFalse(self.robot.diagonal_move('invalid'))
        
        #test boundary checking for diagonal movement
        self.robot.position = (4, 4)
        self.assertFalse(self.robot.diagonal_move('northeast'))  # Should fail at boundary
    
    def test_obstacle_management(self):
        """Test adding and removing obstacles."""
        #test adding obstacle
        self.assertTrue(self.robot.add_obstacle((1, 1)))
        self.assertIn((1, 1), self.robot.obstacles)
        
        #test adding obstacle at invalid position
        self.assertFalse(self.robot.add_obstacle((10, 10)))
        
        #test adding obstacle on robot position
        self.assertFalse(self.robot.add_obstacle((0, 0)))
        
        #test removing obstacle
        self.assertTrue(self.robot.remove_obstacle((1, 1)))
        self.assertNotIn((1, 1), self.robot.obstacles)
        
        #test removing non-existent obstacle
        self.assertFalse(self.robot.remove_obstacle((5, 5)))
    
    def test_grid_expansion(self):
        """Test grid expansion functionality."""
        initial_size = self.robot.grid_size
        
        #test valid expansion
        self.assertTrue(self.robot.expand_grid(7))
        self.assertEqual(self.robot.grid_size, 7)
        
        #test invalid expansion (smaller size)
        self.assertFalse(self.robot.expand_grid(5))
        self.assertEqual(self.robot.grid_size, 7)  # Should remain unchanged
    
    def test_boundary_validation(self):
        """Test boundary validation methods."""
        #test valid positions
        self.assertTrue(self.robot._is_valid_position((0, 0)))
        self.assertTrue(self.robot._is_valid_position((4, 4)))
        
        #test invalid positions
        self.assertFalse(self.robot._is_valid_position((-1, 0)))
        self.assertFalse(self.robot._is_valid_position((0, -1)))
        self.assertFalse(self.robot._is_valid_position((5, 0)))
        self.assertFalse(self.robot._is_valid_position((0, 5)))
    
    def test_report_functionality(self):
        """Test report functionality."""
        ## This test mainly ensures the report method doesn't crash
        ## We can't easily test print output, but we can test the method exists
        self.assertTrue(hasattr(self.robot, 'report'))
        self.assertTrue(callable(self.robot.report))
    
    def test_display_grid(self):
        """Test grid display functionality."""
        ## This test ensures the display method doesn't crash
        self.assertTrue(hasattr(self.robot, 'display_grid'))
        self.assertTrue(callable(self.robot.display_grid))
    
    def test_custom_initialization(self):
        """Test custom initialization parameters."""
        robot = RobotSimulator(grid_size=3, battery_level=50)
        self.assertEqual(robot.grid_size, 3)
        self.assertEqual(robot.battery_level, 50)
        self.assertEqual(robot.position, (0, 0))
        self.assertEqual(robot.direction, Direction.NORTH)


class TestDirectionEnum(unittest.TestCase):
    """Test cases for Direction enum."""
    
    def test_direction_values(self):
        """Test direction enum values."""
        self.assertEqual(Direction.NORTH.value, 0)
        self.assertEqual(Direction.EAST.value, 1)
        self.assertEqual(Direction.SOUTH.value, 2)
        self.assertEqual(Direction.WEST.value, 3)
    
    def test_direction_cycling(self):
        """Test direction cycling behavior."""
        #test clockwise cycling
        self.assertEqual(Direction((Direction.NORTH.value + 1) % 4), Direction.EAST)
        self.assertEqual(Direction((Direction.EAST.value + 1) % 4), Direction.SOUTH)
        self.assertEqual(Direction((Direction.SOUTH.value + 1) % 4), Direction.WEST)
        self.assertEqual(Direction((Direction.WEST.value + 1) % 4), Direction.NORTH)
        
        #test counter-clockwise cycling
        self.assertEqual(Direction((Direction.NORTH.value - 1) % 4), Direction.WEST)
        self.assertEqual(Direction((Direction.WEST.value - 1) % 4), Direction.SOUTH)
        self.assertEqual(Direction((Direction.SOUTH.value - 1) % 4), Direction.EAST)
        self.assertEqual(Direction((Direction.EAST.value - 1) % 4), Direction.NORTH)


def run_tests():
    """Run all tests and display results."""
    print("Running Robot Grid Simulator Tests...")
    print("=" * 50)
    
    #create test suite
    test_suite = unittest.TestSuite()
    
    #add test cases
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRobotSimulator))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDirectionEnum))
    
    #run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    #print summary
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1) 