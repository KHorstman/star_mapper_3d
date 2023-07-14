from json.tool import main
from main import make_star_box

def test_star_mapper_3d():
    """
    Test to make sure a plot is created every time the code is ran. 
    """
    star_name="HD 984"
    radius=1
    depth_start=0
    depth_end=100

    make_star_box(star_name, radius, depth_start, depth_end)

test_star_mapper_3d()