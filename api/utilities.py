# -- Initialise all Singletons here to be exported in main api file --
import sys, os

sys.path.append(os.path.dirname(os.path.join(os.path.dirname(__file__), '..')))
import time

from etl_pipeline.master import Master
from etl_pipeline.moduled_scripts.patients import PatientsETL
from etl_pipeline.moduled_scripts.conditions import ConditionsETL
from etl_pipeline.moduled_scripts.procedures import ProceduresETL

main_singleton = Master()
patients_singleton = PatientsETL()
conditions_singleton = ConditionsETL()
procedures_singleton = ProceduresETL()


time.sleep(4)