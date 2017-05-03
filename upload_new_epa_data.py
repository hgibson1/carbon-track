from models import FuelEconomy
from playhouse.csv_loader import load_csv
from sys import argv

load_csv(FuelEconomy, argv[1]) 
