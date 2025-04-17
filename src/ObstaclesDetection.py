import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class ObstacleDetection: 

        def __init__(self):    
                
                rospy.init_node('Obstacles Detection', anonymous=True)
                
                # Create a publisher (does not send data yet)
                self.publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
                
                sub = rospy.Subscriber("/ball_status", Int32, movement_callback)
                
                self.subscriber = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
                self.obstacle_distance_threshold = 0.25  # meters
                
                rospy.spin()
                
        def movement_callback(self, msg):
                if msg == 0: 
                        print("exploring")
                pass
        

        def scan_callback(self, scan_msg):
                
                # Focus on the front angle (e.g., 0 ± 45 degrees)
                scan_range = scan_msg.ranges
                angle_range = 45

                center_index = len(scan_range) // 2
                start_index = center_index - angle_range
                end_index = center_index + angle_range

                # Get relevant ranges and filter out 'inf' or zero
                front_ranges = [r for r in scan_range[start_index:end_index] if r > 0.0]

                if front_ranges:
                min_distance = min(front_ranges)
                
                if min_distance < self.obstacle_distance_threshold:
                        rospy.logwarn("Obstacle detected at %.2f meters!", min_distance)
                else:
                        rospy.loginfo("Path is clear. Closest object at %.2f meters", min_distance)
                else:
                rospy.loginfo("No valid LiDAR data in front range.")

if __name__ == '__main__':
    try:
        ObstacleDetection()
    except rospy.ROSInterruptException:
        pass
