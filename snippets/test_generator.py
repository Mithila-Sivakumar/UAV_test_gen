import random
from typing import List
from aerialist.px4.drone_test import DroneTest
from aerialist.px4.obstacle import Obstacle
from testcase import TestCase


class TestGenerator(object):
    min_size = Obstacle.Size(2, 2, 10)
    max_size = Obstacle.Size(20, 20, 25)
    min_position = Obstacle.Position(-40, 10, 0, 0)
    max_position = Obstacle.Position(30, 40, 0, 90)

    def __init__(self, case_study_file: str) -> None:
        self.case_study = DroneTest.from_yaml(case_study_file)

    #function to execute the test by creating obstacle and return the test case
    def execute_test(self, updated_x, updated_y, updated_r, updated_l, updated_w, updated_h):
        size = Obstacle.Size(
            l = updated_l,
            w = updated_w,
            h = updated_h
        )
        position = Obstacle.Position(
            x = updated_x,
            y = updated_y,
            z = 0,
            r = updated_r
        )
        obstacle = Obstacle(size, position)
        test = TestCase(self.case_study, [obstacle])
        try:
            test.execute()
            distances = test.get_distances()
            min_dist = min(distances)
            print(f"minimum_distance:{min_dist}")
            test.plot()
        except Exception as e:
            print("Exception during test execution, skipping the test")
            print(e)
        return min_dist, test

    def generate(self, budget: int, num: int) -> List[TestCase]:
        test_cases = []
        #initial parameters with default value
        updated_x = self.min_position.x
        updated_y = self.min_position.y
        updated_r = self.min_position.r
        updated_l = 10
        updated_w = 10
        updated_h = 20
        
        while(budget > 0):

            # run the uav simulation
            min_dist, test = self.execute_test(updated_x, updated_y,  updated_r, updated_l, updated_w, updated_h)
            budget -= 1 # decrement budget since one simulation is finished

            # flag to track all posibile combination of parameters
            condition_met = False 

             # adding the test case only if its challenging or failing (distance less than safety threshold)
            if min_dist < 3.3:
                test_cases.append(test)
                if updated_x < self.max_position.x:
                    updated_x = updated_x + 1
                    condition_met = True
                if updated_y < self.max_position.y:
                    updated_y = updated_y + 10
                    condition_met = True
                if updated_r < self.max_position.r:
                    updated_r = updated_r + 10
                    condition_met = True
                if updated_l < self.max_size.l:
                    updated_l = updated_l + 2
                    condition_met = True
                if updated_w < self.max_size.w:
                    updated_w = updated_w + 2
                    condition_met = True
                if updated_h < self.max_size.h:
                    updated_h = updated_h + 1
                    condition_met = True
                if not condition_met:
                    break #exit loop after exhausting all combinations or budget expires - whichever comes first
            else:
                # move the obstacle by 10 until uav gets dangerously close to the obstacle
                if updated_x < self.max_position.x:
                    updated_x = updated_x + 10
                else:
                    break

        return test_cases


if __name__ == "__main__":
    generator = TestGenerator("case_studies/mission1.yaml")
    generator.generate(1)
