import os
from pyspark.sql import SparkSession
os.environ["HADOOP_HOME"] = "C:\Hadoop"

HADOOP_HOME = os.environ['HADOOP_HOME']
FILE_PATH = f'{os.getcwd()}/data/full_2020s_pbp.csv'


print(HADOOP_HOME)

spark = SparkSession.builder \
    .appName("Test_App") \
    .master("local[*]") \
    .getOrCreate()


csv_headers = [
    "game id", "visiting team", "inning", "batting team", "outs", "balls", "strikes",
    "pitch sequence", "vis score", "home score", "batter", "batter hand", "res batter",
    "res batter hand", "pitcher", "pitcher hand", "res pitcher", "res pitcher hand",
    "catcher", "first base", "second base", "third base", "shortstop", "left field",
    "center field", "right field", "first runner", "second runner", "third runner",
    "event text", "leadoff flag", "pinchhit flag", "defensive position", "lineup position",
    "event type", "batter event flag", "ab flag", "hit value", "SH flag", "SF flag",
    "outs on play", "double play flag", "triple play flag", "RBI on play", "wild pitch flag",
    "passed ball flag", "fielded by", "batted ball type", "bunt flag", "foul flag",
    "hit location", "num errors", "1st error player", "1st error type", "2nd error player",
    "2nd error type", "3rd error player", "3rd error type", "batter dest",
    "runner on 1st dest", "runner on 2nd dest", "runner on 3rd dest", "play on batter",
    "play on runner on 1st", "play on runner on 2nd", "play on runner on 3rd",
    "SB for runner on 1st flag", "SB for runner on 2nd flag", "SB for runner on 3rd flag",
    "CS for runner on 1st flag", "CS for runner on 2nd flag", "CS for runner on 3rd flag",
    "PO for runner on 1st flag", "PO for runner on 2nd flag", "PO for runner on 3rd flag",
    "Responsible pitcher for runner on 1st", "Responsible pitcher for runner on 2nd",
    "Responsible pitcher for runner on 3rd", "New Game Flag", "End Game Flag",
    "Pinch-runner on 1st", "Pinch-runner on 2nd", "Pinch-runner on 3rd",
    "Runner removed for pinch-runner on 1st", "Runner removed for pinch-runner on 2nd",
    "Runner removed for pinch-runner on 3rd", "Batter removed for pinch-hitter",
    "Position of batter removed for pinch-hitter", "Fielder with First Putout",
    "Fielder with Second Putout", "Fielder with Third Putout", "Fielder with First Assist",
    "Fielder with Second Assist", "Fielder with Third Assist", "Fielder with Fourth Assist",
    "Fielder with Fifth Assist", "event num"
]



df = spark.read.csv(FILE_PATH, header=False, inferSchema=True).toDF(*csv_headers)

df.show()





