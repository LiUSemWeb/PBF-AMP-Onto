# ************************************************************************************************
import os
import pathlib
import pickle
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from rdflib import BNode, URIRef, Graph, Namespace, RDF
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QDateTimeEdit, QRadioButton, QListWidget, QComboBox, \
    QMenu, QDialog, QCheckBox, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMessageBox, QPlainTextEdit, QFileDialog, QWidget
from pbf_mainwindow_40 import Ui_MainWindow  # This is the converted UI file
from Edit_Build_Model_v3 import Ui_Dialog  # This is the converted UI file
from DisplayConceptsDefinitins import Ui_Form
from Material_view_v1 import Material_View_Window
from PyQt6.QtCore import QTimer, Qt, QEvent, QDateTime
import re
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD, split_uri
import json
# ************************************************************************************************
class PBF_AM_Process_Chain_class:
    def __init__(self, project_name=None, project_type=None, project_start_date_value=None,
                 project_end_date_value=None, project_status=None, project_comment=None,
                 project_selected_supervisors=None):
        self.project_name = project_name
        self.project_type = project_type
        self.project_start_date_value = project_start_date_value
        self.project_end_date_value = project_end_date_value
        self.project_status = project_status
        self.project_comment = project_comment
        self.project_selected_supervisors = project_selected_supervisors
# ******************************
class Supervisor:
    def __init__(self, supervisor_name=None, supervisor_comment=None):
        self.supervisor_name = supervisor_name
        self.supervisor_comment = supervisor_comment
# ******************************
class Build_Model_Support_class:
    def __init__(self, support_name=None, support_file_path=None, support_file_format=None, support_comment=None):
        self.support_name = support_name
        self.support_file_path = support_file_path
        self.support_file_format = support_file_format
        self.support_comment = support_comment
# ******************************
class Build_Model_AM_Part_class:
    def __init__(self, am_part_name=None, am_part_dimension=None, am_part_file_path=None,
                 am_part_file_format=None, am_part_comment=None):
        self.am_part_name = am_part_name
        self.am_part_dimension = am_part_dimension
        self.am_part_file_path = am_part_file_path
        self.am_part_file_format = am_part_file_format
        self.am_part_comment = am_part_comment
# ******************************
class Build_Model_Design_Process_class:
    def __init__(self, ModelDesign_name=None, ModelDesign_start_date=None, ModelDesign_end_date=None,
                 ModelDesign_completion_status=None, ModelDesign_comment=None, ModelDesign_output=None):
        self.ModelDesign_name = ModelDesign_name
        self.ModelDesign_start_date = ModelDesign_start_date
        self.ModelDesign_end_date = ModelDesign_end_date
        self.ModelDesign_completion_status = ModelDesign_completion_status
        self.ModelDesign_comment = ModelDesign_comment
        self.ModelDesign_output = ModelDesign_output
# ******************************
class output_Build_Model_Design_Process_class:
    def __init__(self, build_model_name=None, build_model_dimension=None, build_model_file_path=None,
                 build_model_file_format=None, build_model_comment=None, build_model_parts_supports=None):
        self.build_model_name = build_model_name
        self.build_model_dimension = build_model_dimension
        self.build_model_file_path = build_model_file_path
        self.build_model_file_format = build_model_file_format
        self.build_model_comment = build_model_comment
        self.has_build_model_am_part = []
        self.has_support_for_build_model_am_part = []
        self.build_model_parts_supports = build_model_parts_supports
# ******************************
class Slicing_Process_class:
    def __init__(self, SlicingProcess_name=None, SlicingProcess_software=None,
                 SlicingProcess_start_date=None, SlicingProcess_end_date=None,
                 SlicingProcess_completion_status=None, SlicingProcess_comment=None, SlicingProcess_input=None,
                 SlicingProcess_output=None):
        self.SlicingProcess_name = SlicingProcess_name
        self.SlicingProcess_software = SlicingProcess_software
        self.SlicingProcess_start_date = SlicingProcess_start_date
        self.SlicingProcess_end_date = SlicingProcess_end_date
        self.SlicingProcess_completion_status = SlicingProcess_completion_status
        self.SlicingProcess_comment = SlicingProcess_comment
        self.SlicingProcess_input = SlicingProcess_input
        self.SlicingProcess_output = SlicingProcess_output
# ******************************
class Printing_Process_Instructions_class:
    def __init__(self, ppi_name=None, ppi_file=None, ppi_file_format=None, ppi_list_layer_thicknesses=None,
                 ppi_comment=None,
                 ppi_machine_powder_feed=None, ppi_start_heating_ppi=None, ppi_layer_pre_heating_ppi=None,
                 ppi_layer_post_heating_ppi=None, ppi_layer_melting_heating_ppi=None):
        self.ppi_name = ppi_name
        self.ppi_file = ppi_file
        self.ppi_file_format = ppi_file_format
        self.ppi_list_layer_thicknesses = ppi_list_layer_thicknesses
        self.ppi_comment = ppi_comment
        self.ppi_machine_powder_feed = ppi_machine_powder_feed
        self.ppi_start_heating_ppi = ppi_start_heating_ppi
        self.ppi_layer_pre_heating_ppi = ppi_layer_pre_heating_ppi
        self.ppi_layer_post_heating_ppi = ppi_layer_post_heating_ppi
        self.ppi_layer_melting_heating_ppi = ppi_layer_melting_heating_ppi
# ******************************
class Layer_Of_Build_Model_class:
    def __init__(self, Layer_Of_Build_Model_name=None, Layer_Of_Build_Model_file=None,
                 Layer_Of_Build_Model_file_format=None,
                 Layer_Of_Build_Model_layer_height=None, Layer_Of_Build_Model_layer_num=None,
                 Layer_Of_Build_Model_comment=None,
                 Layer_Of_Build_Model_consists_of_am_part_layer=[]):
        self.Layer_Of_Build_Model_name = Layer_Of_Build_Model_name
        self.Layer_Of_Build_Model_file = Layer_Of_Build_Model_file
        self.Layer_Of_Build_Model_file_format = Layer_Of_Build_Model_file_format
        self.Layer_Of_Build_Model_layer_height = Layer_Of_Build_Model_layer_height
        self.Layer_Of_Build_Model_layer_num = Layer_Of_Build_Model_layer_num
        self.Layer_Of_Build_Model_comment = Layer_Of_Build_Model_comment
        self.Layer_Of_Build_Model_consists_of_am_part_layer = Layer_Of_Build_Model_consists_of_am_part_layer
# ******************************
class Monitoring_Process_class:
    def __init__(self, monitoring_process_name=None, monitoring_process_start_date=None,
                 monitoring_process_end_date=None, monitoring_process_comment=None, monitoring_process_status=None,
                 monitoring_process_output_file=None, monitoring_process_printing_process=None,
                 monitoring_process_receives_data_from=None):
        self.monitoring_process_name = monitoring_process_name
        self.monitoring_process_start_date = monitoring_process_start_date
        self.monitoring_process_end_date = monitoring_process_end_date
        self.monitoring_process_comment = monitoring_process_comment
        self.monitoring_process_status = monitoring_process_status
        self.monitoring_process_output_file = monitoring_process_output_file
        self.monitoring_process_printing_process = monitoring_process_printing_process
        self.monitoring_process_receives_data_from = monitoring_process_receives_data_from
# ******************************
class Post_Printing_Method:
    def __init__(self, post_printing_method_name=None, post_printing_method_type=None,
                 post_printing_method_comment=None):
        self.post_printing_method_name = post_printing_method_name
        self.post_printing_method_type = post_printing_method_type
        self.post_printing_method_comment = post_printing_method_comment
# ******************************
class Post_Printing_Process_class:
    def __init__(self, post_printing_process_name=None, post_printing_process_status=None,
                 post_printing_process_start_date=None, post_printing_process_end_date=None,
                 post_printing_process_used_methods=None, post_printing_process_comment=None):
        self.post_printing_process_name = post_printing_process_name
        self.post_printing_process_status = post_printing_process_status
        self.post_printing_process_start_date = post_printing_process_start_date
        self.post_printing_process_end_date = post_printing_process_end_date
        self.post_printing_process_used_methods = post_printing_process_used_methods
        self.post_printing_process_comment = post_printing_process_comment
# ******************************
class Testing_Method_class:
    def __init__(self, TestingMethod_name=None, TestingMethod_type=None, TestingMethod_comment=None):
        self.TestingMethod_name = TestingMethod_name
        self.TestingMethod_type = TestingMethod_type
        self.TestingMethod_comment = TestingMethod_comment
# ******************************
class applied_testing_method_class:
    def __init__(self, applied_testing_method_name=None, applied_testing_method_result=None,
                 applied_testing_method_comment=None):
        self.applied_testing_method_name = applied_testing_method_name
        self.applied_testing_method_result = applied_testing_method_result
        self.applied_testing_method_comment = applied_testing_method_comment
# ******************************
class Testing_Process_class:
    def __init__(self, TestingProcess_name=None, TestingProcess_status=None, TestingProcess_start_date=None,
                 TestingProcess_end_date=None, TestingProcess_comment=None, TestingProcess_applied_methods_results=None,
                 TestingProcess_hasInputPrintedBuild=None, TestingProcess_hasInputPrintedBuildAMPart=None,
                 TestingProcess_hasInputPrintedBuildSupport=None,
                 TestingProcess_testing_method=None, TestingProcess_testing_data=None):
        self.TestingProcess_name = TestingProcess_name
        self.TestingProcess_status = TestingProcess_status
        self.TestingProcess_start_date = TestingProcess_start_date
        self.TestingProcess_end_date = TestingProcess_end_date
        self.TestingProcess_comment = TestingProcess_comment
        self.TestingProcess_hasInputPrintedBuild = TestingProcess_hasInputPrintedBuild
        self.TestingProcess_hasInputPrintedBuildAMPart = TestingProcess_hasInputPrintedBuildAMPart
        self.TestingProcess_hasInputPrintedBuildSupport = TestingProcess_hasInputPrintedBuildSupport
        self.TestingProcess_testing_method = TestingProcess_testing_method
        self.TestingProcess_testing_data = TestingProcess_testing_data
        self.TestingProcess_applied_methods_results = TestingProcess_applied_methods_results
# ******************************
class Printing_Process_class:
    def __init__(self, printing_process_name=None, printing_process_status=None, printing_process_start_date=None,
                 printing_process_end_date=None,
                 printing_process_comment=None, printing_process_build_plate=None,
                 printing_process_printing_medium=None,
                 printing_process_printing_machine=None, printing_process_instructions=None,
                 printing_process_output=None):
        self.printing_process_name = printing_process_name
        self.printing_process_status = printing_process_status
        self.printing_process_start_date = printing_process_start_date
        self.printing_process_end_date = printing_process_end_date
        self.printing_process_comment = printing_process_comment
        self.printing_process_build_plate = printing_process_build_plate
        self.printing_process_printing_medium = printing_process_printing_medium
        self.printing_process_printing_machine = printing_process_printing_machine
        self.printing_process_instructions = printing_process_instructions
        self.printing_process_output = printing_process_output
# ******************************
class Sensor_class:
    def __init__(self, sensor_name=None, sensor_type=None, recorded_data_path=None):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.recorded_data_path = recorded_data_path
# ******************************
class Printing_Machine_class:
    def __init__(self, printing_machine_name=None, printing_machine_brand=None, printing_machine_comment=None,
                 printing_machine_sensor_info=None):
        self.printing_machine_name = printing_machine_name
        self.printing_machine_comment = printing_machine_comment
        self.printing_machine_sensor_info = printing_machine_sensor_info
        self.printing_machine_brand = printing_machine_brand
# ******************************
class Printed_Build_AM_Part_class:
    def __init__(self, Printed_Build_AM_Part_name=None, Printed_Build_AM_Part_comment=None):
        self.Printed_Build_AM_Part_name = Printed_Build_AM_Part_name
        self.Printed_Build_AM_Part_comment = Printed_Build_AM_Part_comment
# ******************************
class Printed_Build_Support_class:
    def __init__(self, Printed_Build_Support_name=None, Printed_Build_Support_comment=None):
        self.Printed_Build_Support_name = Printed_Build_Support_name
        self.Printed_Build_Support_comment = Printed_Build_Support_comment
# ******************************
class Printed_Build_class:
    def __init__(self, Printed_Build_name=None, Printed_Build_comment=None, Printed_Build_AM_Parts_and_supports=None):
        self.Printed_Build_name = Printed_Build_name
        self.Printed_Build_comment = Printed_Build_comment
        self.Printed_Build_AM_Parts_and_supports = Printed_Build_AM_Parts_and_supports
# ******************************
class Material_class:
    def __init__(self, material_name=None, material_melting_point=None, material_oxidation_resistance=None,
                 material_heat_capacity=None,
                 material_formula=None, material_density=None, material_electrical_resistivity=None,
                 material_eb_absorption_rate=None,
                 material_thermal_conductivity=None, material_electrical_conductivity=None,
                 material_thermal_diffusivity=None, material_comment=None):
        self.material_name = material_name
        self.material_melting_point = material_melting_point
        self.material_oxidation_resistance = material_oxidation_resistance
        self.material_heat_capacity = material_heat_capacity
        self.material_formula = material_formula
        self.material_density = material_density
        self.material_electrical_resistivity = material_electrical_resistivity
        self.material_eb_absorption_rate = material_eb_absorption_rate
        self.material_electrical_conductivity = material_electrical_conductivity
        self.material_thermal_conductivity = material_thermal_conductivity
        self.material_thermal_diffusivity = material_thermal_diffusivity
        self.material_comment = material_comment
# ******************************
class Manufacturer_class:
    def __init__(self, manufacturer_name=None, manufacturer_address=None, manufacturer_comment=None):
        self.manufacturer_name = manufacturer_name
        self.manufacturer_address = manufacturer_address
        self.manufacturer_comment = manufacturer_comment
# ******************************
class Printing_Medium_class:
    def __init__(self, printing_medium_name=None, printing_medium_status=None, printing_medium_type=None,
                 printing_medium_material=None, printing_medium_particle_size=None,
                 printing_medium_powder_morphology=None, printing_medium_manufacturer=None,
                 printing_medium_comment=None):
        self.printing_medium_name = printing_medium_name
        self.printing_medium_status = printing_medium_status
        self.printing_medium_type = printing_medium_type
        self.printing_medium_material = printing_medium_material
        self.printing_medium_particle_size = printing_medium_particle_size
        self.printing_medium_powder_morphology = printing_medium_powder_morphology
        self.printing_medium_manufacturer = printing_medium_manufacturer
        self.printing_medium_comment = printing_medium_comment
# ******************************
class Build_Plate_class:
    def __init__(self, build_plate_name=None, build_plate_size=None, build_plate_thickness=None,
                 build_plate_surface_texture=None,
                 build_plate_shape=None, build_plate_manufacturer=None, build_plate_material=None,
                 build_plate_comment=None):
        self.build_plate_name = build_plate_name
        self.build_plate_size = build_plate_size
        self.build_plate_thickness = build_plate_thickness
        self.build_plate_surface_texture = build_plate_surface_texture
        self.build_plate_shape = build_plate_shape
        self.build_plate_manufacturer = build_plate_manufacturer
        self.build_plate_material = build_plate_material
        self.build_plate_comment = build_plate_comment
# ******************************
class layer_of_Build_Model_AM_Part_class:
    def __init__(self, layer_of_Build_Model_AM_Part_name=None, layer_of_Build_Model_AM_Part_area=None,
                 layer_of_Build_Model_AM_Part_file=None,
                 layer_of_Build_Model_AM_Part_file_format=None, layer_of_Build_Model_AM_Part_comment=None):
        self.layer_of_Build_Model_AM_Part_name = layer_of_Build_Model_AM_Part_name
        self.layer_of_Build_Model_AM_Part_area = layer_of_Build_Model_AM_Part_area
        self.layer_of_Build_Model_AM_Part_file = layer_of_Build_Model_AM_Part_file
        self.layer_of_Build_Model_AM_Part_file_format = layer_of_Build_Model_AM_Part_file_format
        self.layer_of_Build_Model_AM_Part_comment = layer_of_Build_Model_AM_Part_comment
# ******************************
class Machine_Powder_Feed_Control_Strategy_class:
    def __init__(self, Machine_powder_s_name=None, Machine_powder_s_file=None, Machine_powder_s_file_format=None,
                 Machine_powder_s_triggered_start=None,
                 Machine_powder_s_recoater_full_repeats=None, Machine_powder_s_recoater_speed=None,
                 Machine_powder_s_recoater_retract_speed=None, Machine_powder_s_recoater_dwell_time=None,
                 Machine_powder_s_recoater_build_repeats=None, Machine_powder_s_comment=None):
        self.Machine_powder_s_name = Machine_powder_s_name
        self.Machine_powder_s_file = Machine_powder_s_file
        self.Machine_powder_s_triggered_start = Machine_powder_s_triggered_start
        self.Machine_powder_s_recoater_full_repeats = Machine_powder_s_recoater_full_repeats
        self.Machine_powder_s_recoater_speed = Machine_powder_s_recoater_speed
        self.Machine_powder_s_recoater_retract_speed = Machine_powder_s_recoater_retract_speed
        self.Machine_powder_s_recoater_dwell_time = Machine_powder_s_recoater_dwell_time
        self.Machine_powder_s_recoater_build_repeats = Machine_powder_s_recoater_build_repeats
        self.Machine_powder_s_comment = Machine_powder_s_comment
        self.Machine_powder_s_file_format = Machine_powder_s_file_format
# ******************************
class Machine_Powder_Feed_Control_PPI_class:
    def __init__(self, Machine_powder_s_PPI_name=None, Machine_powder_s_PPI_file=None,
                 Machine_powder_s_PPI_file_format=None, Machine_powder_s_PPI_correspond_strategy=None):
        self.Machine_powder_s_PPI_name = Machine_powder_s_PPI_name
        self.Machine_powder_s_PPI_file = Machine_powder_s_PPI_file
        self.Machine_powder_s_PPI_file_format = Machine_powder_s_PPI_file_format
        self.Machine_powder_s_PPI_correspond_strategy = Machine_powder_s_PPI_correspond_strategy
# ******************************
class Scan_Strategy_class:
    def __init__(self, scan_strategy_name=None, scan_strategy_beam_spot_size=None, scan_strategy_dwell_time=None,
                 scan_strategy_point_distance=None, scan_strategy_strategy_name=None, scan_strategy_scan_speed=None,
                 scan_strategy_beam_power=None, scan_strategy_comment=None):
        self.scan_strategy_name = scan_strategy_name
        self.scan_strategy_beam_spot_size = scan_strategy_beam_spot_size
        self.scan_strategy_dwell_time = scan_strategy_dwell_time
        self.scan_strategy_point_distance = scan_strategy_point_distance
        self.scan_strategy_strategy_name = scan_strategy_strategy_name
        self.scan_strategy_scan_speed = scan_strategy_scan_speed
        self.scan_strategy_beam_power = scan_strategy_beam_power
        self.scan_strategy_comment = scan_strategy_comment
# ******************************
class Beam_Control_Slicing_Strategy_class:
    def __init__(self, beam_control_slic_strategy_name=None, beam_control_slic_strategy_file=None,
                 beam_control_slic_strategy_file_format=None,
                 beam_control_slic_strategy_scan_strategy=None, beam_control_pre_heating=None,
                 beam_control_slic_strategy_melting=None,
                 beam_control_slic_strategy_post_heating=None, beam_control_start_heating_strategy=None):
        self.beam_control_slic_strategy_name = beam_control_slic_strategy_name
        self.beam_control_slic_strategy_file = beam_control_slic_strategy_file
        self.beam_control_slic_strategy_file_format = beam_control_slic_strategy_file_format
        self.beam_control_slic_strategy_scan_strategy = beam_control_slic_strategy_scan_strategy
        self.beam_control_pre_heating = beam_control_pre_heating
        self.beam_control_slic_strategy_melting = beam_control_slic_strategy_melting
        self.beam_control_slic_strategy_post_heating = beam_control_slic_strategy_post_heating
        self.beam_control_start_heating_strategy = beam_control_start_heating_strategy
# ******************************
class Start_Heating_Strategy_class:
    def __init__(self, start_heat_name=None, start_heat_size=None, start_heat_timeout=None,
                 start_heat_scan_strategy=None,
                 start_heat_file=None, start_heat_shape=None, start_heat_rotation_angle=None,
                 start_heat_file_format=None,
                 start_heat_target_temp=None, start_heat_comment=None):
        self.start_heat_name = start_heat_name
        self.start_heat_size = start_heat_size
        self.start_heat_timeout = start_heat_timeout
        self.start_heat_scan_strategy = start_heat_scan_strategy
        self.start_heat_file = start_heat_file
        self.start_heat_shape = start_heat_shape
        self.start_heat_rotation_angle = start_heat_rotation_angle
        self.start_heat_file_format = start_heat_file_format
        self.start_heat_target_temp = start_heat_target_temp
        self.start_heat_comment = start_heat_comment
# ******************************
class Start_Heating_PPI_class:
    def __init__(self, start_heat_ppi_name=None, start_heat_ppi_file=None, start_heat_ppi_file_format=None,
                 start_heat_ppi_correspond_start_heat_strategy=None):
        self.start_heat_ppi_name = start_heat_ppi_name
        self.start_heat_ppi_file = start_heat_ppi_file
        self.start_heat_ppi_file_format = start_heat_ppi_file_format
        self.start_heat_ppi_correspond_start_heat_strategy = start_heat_ppi_correspond_start_heat_strategy
# ******************************
class Layer_Pre_Heating_Strategy_class:
    def __init__(self, pre_heat_strategy_name=None, pre_heat_strategy_scan_strategy=None,
                 pre_heat_strategy_file=None, pre_heat_strategy_file_format=None, pre_heat_strategy_comment=None,
                 pre_heat_strategy_composed_of_AM_Parts=None):
        self.pre_heat_strategy_name = pre_heat_strategy_name
        self.pre_heat_strategy_scan_strategy = pre_heat_strategy_scan_strategy
        self.pre_heat_strategy_file = pre_heat_strategy_file
        self.pre_heat_strategy_file_format = pre_heat_strategy_file_format
        self.pre_heat_strategy_comment = pre_heat_strategy_comment
        self.pre_heat_strategy_composed_of_AM_Parts = pre_heat_strategy_composed_of_AM_Parts
# ******************************
class AM_Part_Layer_Pre_Heating_Strategy_class:
    def __init__(self, AM_part_pre_heat_strategy_name=None, AM_part_pre_heat_strategy_file=None,
                 AM_part_pre_heat_strategy_file_format=None, AM_part_pre_heat_strategy_scan_strategy=None,
                 AM_part_pre_heat_strategy_rotation_angle=None, AM_part_pre_heat_strategy_number_repetitions=None,
                 AM_part_pre_heat_strategy_number_comment=None):
        self.AM_part_pre_heat_strategy_name = AM_part_pre_heat_strategy_name
        self.AM_part_pre_heat_strategy_file = AM_part_pre_heat_strategy_file
        self.AM_part_pre_heat_strategy_file_format = AM_part_pre_heat_strategy_file_format
        self.AM_part_pre_heat_strategy_scan_strategy = AM_part_pre_heat_strategy_scan_strategy
        self.AM_part_pre_heat_strategy_rotation_angle = AM_part_pre_heat_strategy_rotation_angle
        self.AM_part_pre_heat_strategy_number_repetitions = AM_part_pre_heat_strategy_number_repetitions
        self.AM_part_pre_heat_strategy_number_comment = AM_part_pre_heat_strategy_number_comment
# ******************************
class Layer_Pre_Heating_PPI_class:
    def __init__(self, pre_heat_ppi_name=None, pre_heat_ppi_layer_num=None, pre_heat_ppi_file=None,
                 pre_heat_ppi_file_format=None,
                 pre_heat_ppi_corrspond_layer_build_model=None, pre_heat_ppi_correspond_pre_heating_strategy=None,
                 pre_heat_ppi_comment=None, pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi=None):
        self.pre_heat_ppi_name = pre_heat_ppi_name
        self.pre_heat_ppi_layer_num = pre_heat_ppi_layer_num
        self.pre_heat_ppi_file = pre_heat_ppi_file
        self.pre_heat_ppi_file_format = pre_heat_ppi_file_format
        self.pre_heat_ppi_corrspond_layer_build_model = pre_heat_ppi_corrspond_layer_build_model
        self.pre_heat_ppi_correspond_pre_heating_strategy = pre_heat_ppi_correspond_pre_heating_strategy
        self.pre_heat_ppi_comment = pre_heat_ppi_comment
        self.pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi = pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi
# ******************************
class AM_Part_Layer_Pre_Heating_PPI_class:
    def __init__(self, AM_part_pre_heat_ppi_name=None, AM_part_pre_heat_ppi_file=None,
                 AM_part_pre_heat_ppi_file_format=None,
                 AM_part_pre_heat_ppi_comment=None, AM_part_pre_heat_ppi_related_am_part=None,
                 AM_part_pre_heat_ppi_correspond_layer_build_model=None,
                 AM_part_pre_heat_ppi_correspond_AM_part_pre_heat_strategy=None):
        self.AM_part_pre_heat_ppi_name = AM_part_pre_heat_ppi_name
        self.AM_part_pre_heat_ppi_file = AM_part_pre_heat_ppi_file
        self.AM_part_pre_heat_ppi_file_format = AM_part_pre_heat_ppi_file_format
        self.AM_part_pre_heat_ppi_comment = AM_part_pre_heat_ppi_comment
        self.AM_part_pre_heat_ppi_related_am_part = AM_part_pre_heat_ppi_related_am_part
        self.AM_part_pre_heat_ppi_correspond_layer_build_model = AM_part_pre_heat_ppi_correspond_layer_build_model
        self.AM_part_pre_heat_ppi_correspond_AM_part_pre_heat_strategy = AM_part_pre_heat_ppi_correspond_AM_part_pre_heat_strategy
# ******************************
class Layer_Post_Heating_Strategy_class:
    def __init__(self, post_heat_strategy_name=None, post_heat_strategy_scan_strategy=None,
                 post_heat_strategy_file=None, post_heat_strategy_file_format=None, post_heat_strategy_comment=None,
                 post_heat_strategy_composed_of_AM_Parts=None):
        self.post_heat_strategy_name = post_heat_strategy_name
        self.post_heat_strategy_scan_strategy = post_heat_strategy_scan_strategy
        self.post_heat_strategy_file = post_heat_strategy_file
        self.post_heat_strategy_file_format = post_heat_strategy_file_format
        self.post_heat_strategy_comment = post_heat_strategy_comment
        self.post_heat_strategy_composed_of_AM_Parts = post_heat_strategy_composed_of_AM_Parts
# ******************************
class AM_Part_Layer_Post_Heating_Strategy_class:
    def __init__(self, AM_part_post_heat_strategy_name=None, AM_part_post_heat_strategy_file=None,
                 AM_part_post_heat_strategy_file_format=None, AM_part_post_heat_strategy_scan_strategy=None,
                 AM_part_post_heat_strategy_rotation_angle=None, AM_part_post_heat_strategy_number_repetitions=None,
                 AM_part_post_heat_strategy_number_comment=None):
        self.AM_part_post_heat_strategy_name = AM_part_post_heat_strategy_name
        self.AM_part_post_heat_strategy_file = AM_part_post_heat_strategy_file
        self.AM_part_post_heat_strategy_file_format = AM_part_post_heat_strategy_file_format
        self.AM_part_post_heat_strategy_scan_strategy = AM_part_post_heat_strategy_scan_strategy
        self.AM_part_post_heat_strategy_rotation_angle = AM_part_post_heat_strategy_rotation_angle
        self.AM_part_post_heat_strategy_number_repetitions = AM_part_post_heat_strategy_number_repetitions
        self.AM_part_post_heat_strategy_number_comment = AM_part_post_heat_strategy_number_comment
# ******************************
class Layer_Post_Heating_PPI_class:
    def __init__(self, post_heat_ppi_name=None, post_heat_ppi_layer_num=None, post_heat_ppi_file=None,
                 post_heat_ppi_file_format=None,
                 post_heat_ppi_corrspond_layer_build_model=None, post_heat_ppi_correspond_post_heating_strategy=None,
                 post_heat_ppi_comment=None, post_heat_ppi_composed_AM_part_Layer_post_heat_ppi=None):
        self.post_heat_ppi_name = post_heat_ppi_name
        self.post_heat_ppi_layer_num = post_heat_ppi_layer_num
        self.post_heat_ppi_file = post_heat_ppi_file
        self.post_heat_ppi_file_format = post_heat_ppi_file_format
        self.post_heat_ppi_corrspond_layer_build_model = post_heat_ppi_corrspond_layer_build_model
        self.post_heat_ppi_correspond_post_heating_strategy = post_heat_ppi_correspond_post_heating_strategy
        self.post_heat_ppi_comment = post_heat_ppi_comment
        self.post_heat_ppi_composed_AM_part_Layer_post_heat_ppi = post_heat_ppi_composed_AM_part_Layer_post_heat_ppi
# ******************************
class AM_Part_Layer_Post_Heating_PPI_class:
    def __init__(self, AM_part_post_heat_ppi_name=None, AM_part_post_heat_ppi_file=None,
                 AM_part_post_heat_ppi_file_format=None,
                 AM_part_post_heat_ppi_comment=None, AM_part_post_heat_ppi_related_am_part=None,
                 AM_part_post_heat_ppi_correspond_layer_build_model=None,
                 AM_part_post_heat_ppi_correspond_AM_part_post_heat_strategy=None):
        self.AM_part_post_heat_ppi_name = AM_part_post_heat_ppi_name
        self.AM_part_post_heat_ppi_file = AM_part_post_heat_ppi_file
        self.AM_part_post_heat_ppi_file_format = AM_part_post_heat_ppi_file_format
        self.AM_part_post_heat_ppi_comment = AM_part_post_heat_ppi_comment
        self.AM_part_post_heat_ppi_related_am_part = AM_part_post_heat_ppi_related_am_part
        self.AM_part_post_heat_ppi_correspond_layer_build_model = AM_part_post_heat_ppi_correspond_layer_build_model
        self.AM_part_post_heat_ppi_correspond_AM_part_post_heat_strategy = AM_part_post_heat_ppi_correspond_AM_part_post_heat_strategy
# ******************************
class EditWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
# ******************************
class ConceptsDefinitionsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
# ******************************
class MaterialWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Material_View_Window()
        self.ui.setupUi(self)
# ******************************
class Layer_Melting_Strategy_class:
    def __init__(self, melting_strategy_name=None, melting_strategy_scan_strategy=None,
                 melting_strategy_file=None, melting_strategy_file_format=None, melting_strategy_comment=None,
                 melting_strategy_composed_of_AM_Parts=None):
        self.melting_strategy_name = melting_strategy_name
        self.melting_strategy_scan_strategy = melting_strategy_scan_strategy
        self.melting_strategy_file = melting_strategy_file
        self.melting_strategy_file_format = melting_strategy_file_format
        self.melting_strategy_comment = melting_strategy_comment
        self.melting_strategy_composed_of_AM_Parts = melting_strategy_composed_of_AM_Parts
# ******************************
class AM_Part_Layer_Melting_Strategy_class:
    def __init__(self, AM_part_melting_strategy_name=None, AM_part_melting_strategy_file=None,
                 AM_part_melting_strategy_file_format=None, AM_part_melting_strategy_scan_strategy=None,
                 AM_part_melting_strategy_rotation_angle=None, AM_part_melting_strategy_number_repetitions=None,
                 AM_part_melting_strategy_point_distance=None, AM_part_melting_strategy_energy_density=None,
                 AM_part_melting_strategy_offset_margin=None, AM_part_melting_strategy_comment=None):
        self.AM_part_melting_strategy_name = AM_part_melting_strategy_name
        self.AM_part_melting_strategy_file = AM_part_melting_strategy_file
        self.AM_part_melting_strategy_file_format = AM_part_melting_strategy_file_format
        self.AM_part_melting_strategy_scan_strategy = AM_part_melting_strategy_scan_strategy
        self.AM_part_melting_strategy_rotation_angle = AM_part_melting_strategy_rotation_angle
        self.AM_part_melting_strategy_number_repetitions = AM_part_melting_strategy_number_repetitions
        self.AM_part_melting_strategy_point_distance = AM_part_melting_strategy_point_distance
        self.AM_part_melting_strategy_energy_density = AM_part_melting_strategy_energy_density
        self.AM_part_melting_strategy_offset_margin = AM_part_melting_strategy_offset_margin
        self.AM_part_melting_strategy_comment = AM_part_melting_strategy_comment
# ******************************
class Layer_Melting_PPI_class:
    def __init__(self, melting_ppi_name=None, melting_ppi_layer_num=None, melting_ppi_file=None,
                 melting_ppi_file_format=None,
                 melting_ppi_corrspond_layer_build_model=None, melting_ppi_correspond_melting_strategy=None,
                 melting_ppi_comment=None, melting_ppi_composed_AM_part_Layer_melting_ppi=None):
        self.melting_ppi_name = melting_ppi_name
        self.melting_ppi_layer_num = melting_ppi_layer_num
        self.melting_ppi_file = melting_ppi_file
        self.melting_ppi_file_format = melting_ppi_file_format
        self.melting_ppi_corrspond_layer_build_model = melting_ppi_corrspond_layer_build_model
        self.melting_ppi_correspond_melting_strategy = melting_ppi_correspond_melting_strategy
        self.melting_ppi_comment = melting_ppi_comment
        self.melting_ppi_composed_AM_part_Layer_melting_ppi = melting_ppi_composed_AM_part_Layer_melting_ppi
# ******************************
class AM_Part_Layer_Melting_PPI_class:
    def __init__(self, AM_part_melting_ppi_name=None, AM_part_melting_ppi_file=None,
                 AM_part_melting_ppi_file_format=None,
                 AM_part_melting_ppi_comment=None, AM_part_melting_ppi_related_am_part=None,
                 AM_part_melting_ppi_correspond_layer_build_model=None,
                 AM_part_melting_ppi_correspond_AM_part_melting_strategy=None):
        self.AM_part_melting_ppi_name = AM_part_melting_ppi_name
        self.AM_part_melting_ppi_file = AM_part_melting_ppi_file
        self.AM_part_melting_ppi_file_format = AM_part_melting_ppi_file_format
        self.AM_part_melting_ppi_comment = AM_part_melting_ppi_comment
        self.AM_part_melting_ppi_related_am_part = AM_part_melting_ppi_related_am_part
        self.AM_part_melting_ppi_correspond_layer_build_model = AM_part_melting_ppi_correspond_layer_build_model
        self.AM_part_melting_ppi_correspond_AM_part_melting_strategy = AM_part_melting_ppi_correspond_AM_part_melting_strategy
# ******************************
class PDFViewer(QMainWindow):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle(f"Viewing: {os.path.basename(file_path)}")
        self.resize(1600, 1200)
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        pdf_view = QPdfView(self)
        pdf_doc = QPdfDocument(self)
        status = pdf_doc.load(file_path)
        if status == QPdfDocument.Error.None_:
            pdf_view.setDocument(pdf_doc)
            layout.addWidget(pdf_view)
        else:
            layout.addWidget(QLabel("Failed to load PDF file."))
# ************************************************************************************************
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.setWindowIcon(QIcon("jk.jpg"))
        self.ui.defined_supervisors_list.addItems(supervisors_list_name)
        # ==============================================================================
        self.ui.actionExit.triggered.connect(self.close_func)
        self.ui.actionDisplay_PBF_AMP_Onto.triggered.connect(self.display_pbf_amp_onto)
        self.ui.actionSave_as_new_project.triggered.connect(self.save_as_new_project)
        self.ui.actionSave_changes_to_current_project.triggered.connect(self.save_changes_to_current_project)
        self.ui.actionOpen_Project.triggered.connect(self.open_project_func)
        self.ui.actionNew_Project.triggered.connect(self.open_new_project)
        self.ui.actionDisplay_Concept_Definitions.triggered.connect(self.display_concepts_definitions)
        self.ui.actionAdd_Project_to_KG.triggered.connect(self.save_project_as_rdf)
        self.ui.actionjson.triggered.connect(self.save_project_as_json)
        # ==============================================================================
        self.ui.toolBox_5.setCurrentIndex(2)
        self.ui.toolBox_2.setCurrentIndex(1)
        self.ui.toolBox_11.setCurrentIndex(0)
        self.ui.toolBox_6.setCurrentIndex(0)
        self.ui.toolBox_8.setCurrentIndex(2)
        self.ui.toolBox_9.setCurrentIndex(0)
        self.ui.toolBox_10.setCurrentIndex(0)
        self.ui.toolBox_3.setCurrentIndex(8)
        self.ui.toolBox.setCurrentIndex(1)
        self.ui.toolBox_4.setCurrentIndex(1)
        # ==============================================================================
        self.ui.define_project_button.clicked.connect(self.define_project_button_func)
        self.setup_button_reset_on_groupbox_change_9(self.ui.define_project_button, self.ui.pbf_am_process_chain)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.PathPlanning4_2.setCurrentIndex(0)
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.ui.supervisor_project_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.supervisor_project_list.customContextMenuRequested.connect(self.supervisor_project_list_menu)
        self.ui.defined_supervisors_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.set_as_input_printing_process_listWidget.customContextMenuRequested.connect(
            self.set_as_input_printing_process_listWidget_menu)
        self.ui.set_as_input_printing_process_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_printed_build_PB_AM_partlistWidget.customContextMenuRequested.connect(
            self.composed_of_printed_build_PB_AM_partlistWidget_menu)
        self.ui.composed_of_printed_build_PB_AM_partlistWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.selected_ppi_slicing_process.customContextMenuRequested.connect(self.selected_ppi_slicing_process_menu)
        self.ui.selected_ppi_slicing_process.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.selected_machine_control_strategy.customContextMenuRequested.connect(
            self.selected_machine_control_strategy_menu)
        self.ui.selected_machine_control_strategy.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.selected_machine_control_ppi.customContextMenuRequested.connect(self.selected_machine_control_ppi_menu)
        self.ui.selected_machine_control_ppi.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.selected_start_heat_ppi_listWidget.customContextMenuRequested.connect(
            self.selected_start_heat_ppi_listWidget_menu)
        self.ui.selected_start_heat_ppi_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.selected_start_heating_listWidget.customContextMenuRequested.connect(
            self.selected_start_heating_listWidget_menu)
        self.ui.selected_start_heating_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_supervisors_list.customContextMenuRequested.connect(self.defined_supervisors_list_menu)
        self.ui.supports_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.supports_list.customContextMenuRequested.connect(self.supports_list_menu)
        self.ui.parts_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.parts_list.customContextMenuRequested.connect(self.parts_list_menu)
        self.ui.defined_PostPrinting_methods_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_PostPrinting_methods_listWidget.customContextMenuRequested.connect(
            self.defined_PostPrinting_methods_listWidget_menu)
        self.ui.used_POstPrinting_methods_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.used_POstPrinting_methods_listWidget.customContextMenuRequested.connect(
            self.used_POstPrinting_methods_listWidget_menu)
        self.ui.defined_testing_methods_listwidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_testing_methods_listwidget.customContextMenuRequested.connect(
            self.defined_testing_methods_listwidget_menu)
        self.ui.Testin_process_applied_methods_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.Testin_process_applied_methods_list.customContextMenuRequested.connect(
            self.Testin_process_applied_methods_list_menu)
        self.ui.LayerBuildModel_define_pushButton.clicked.connect(self.LayerBuildModel_define_func)
        self.ui.add_outpu_layer_decomposition_pushButton_2.clicked.connect(self.add_outpu_layer_decomposition_2_func)
        self.ui.define_PartLayerBuildModel_pushButton.clicked.connect(self.define_PartLayerBuildModel_func)
        self.ui.add_outpu_layer_decomposition_pushButton.clicked.connect(self.add_outpu_layer_decomposition_func)
        self.ui.consist_layer_partcheckBox.stateChanged.connect(self.toggle_consist_layer_partcheckBox)
        self.ui.add_machine_feed_strategy_pushButton.clicked.connect(self.add_machine_feed_strategy_func)
        self.setup_button_reset_on_groupbox_change_11(self.ui.add_machine_feed_strategy_pushButton, self.ui.groupBox)
        self.ui.add_machine_feed_strategy_pushButton_2.clicked.connect(self.add_machine_feed_strategy_pushButton_2_func)
        self.ui.define_start_heating_pushButton_2.clicked.connect(self.define_start_heating_pushButton_2_func)
        self.ui.selectSupervisor.addItem("-- Select an option --")
        self.ui.load_sensor_comboBox.addItem("-- Select an option --")
        self.ui.am_part_layer_melting_strategy_scan_strategy.addItem("-- Select an option --")
        self.ui.choose_part.addItem("-- Select an option --")
        self.ui.choose_support.addItem("-- Select an option --")
        self.ui.load_buildmodel_combobox.addItem("-- Select an option --")
        self.ui.Post_Printing_method_comboBox.addItem("-- Select an option --")
        self.ui.testing_method_name_comboBox.addItem("-- Select an option --")
        self.ui.printing_process_buildplate.addItem("-- Select an option --")
        self.ui.printing_process_printing_medium.addItem("-- Select an option --")
        self.ui.printing_process_printing_machine.addItem("-- Select an option --")
        self.ui.printing_process_output_printe_build.addItem("-- Select an option --")
        self.ui.printing_medium_material_comboBox.addItem("-- Select an option --")
        self.ui.printing_medium_manufacturer_comboBox.addItem("-- Select an option --")
        self.ui.build_plate_material_comboBox.addItem("-- Select an option --")
        self.ui.build_plate_manufacturer_comboBox.addItem("-- Select an option --")
        self.ui.am_part_layer_pre_heating_ppi_related_am_part_comboBox.addItem("-- Select an option --")
        self.ui.am_part_layer_pre_heating_ppi_correspond_am_part.addItem("-- Select an option --")
        self.ui.correspond_am_part_layer_pre_heating.addItem("-- Select an option --")
        self.ui.composed_of_am_part_pre_heating_ppi_combobox.addItem("-- Select an option --")
        self.ui.correspond_to_layer_pre_heating_combobox.addItem("-- Select an option --")
        # self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox.addItem("-- Select an option --")
        self.ui.am_part_layer_post_heating_strategy_scan_strategy.addItem("-- Select an option --")
        self.ui.printed_build_PB_AM_part_comboBox.addItem("-- Select an option --")
        self.ui.printed_build_PB_AM_part_support_comboBox.addItem("-- Select an option --")
        self.ui.input_printing_ppi_name.addItem("-- Select an option --")
        self.ui.load_exist_printing_instructions_comboBox.addItem("-- Select an option --")
        self.ui.load_layer_comboBox_2.addItem("-- Select an option --")
        self.ui.load_layer_comboBox.addItem("-- Select an option --")
        self.ui.layer_part_comboBox.addItem("-- Select an option --")
        self.ui.am_part_layer_pre_heating_strategy_scan_startegy.addItem("-- Select an option --")
        self.ui.load_an_existing_layer_pr_heating.addItem("-- Select an option --")
        self.ui.layer_pre_heating_strategy_scan_strategy.addItem("-- Select an option --")
        self.ui.composed_of_am_part_pre_startegies_combobox.addItem("-- Select an option --")
        self.ui.am_part_layer_pre_heating_ppi_related_am_part_comboBox.addItem("-- Select an option --")
        self.ui.am_part_layer_pre_heating_ppi_correspond_am_part.addItem("-- Select an option --")
        self.ui.correspond_am_part_layer_pre_heating.addItem("-- Select an option --")
        self.ui.load_an_existing_layer_pr_heating_ppi_combobox.addItem("-- Select an option --")
        # self.ui.correspond_to_layer_pre_heating_combobox.addItem("-- Select an option --")
        self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox.addItem("-- Select an option --")
        self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox_2.addItem("-- Select an option --")
        self.ui.correspond_layer_build_model_am_part_conbobox.addItem("-- Select an option --")
        self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.addItem("-- Select an option --")
        self.ui.load_an_existing_layer_post_heating_ppi_combobox.addItem("-- Select an option --")
        self.ui.correspond_layer_post_heating_combobox.addItem("-- Select an option --")
        self.ui.correspond_layer_build_model_combobox.addItem("-- Select an option --")
        self.ui.composed_of_am_part_post_heating_ppi_combobox.addItem("-- Select an option --")
        self.ui.load_existing_post_heating_combobox.addItem("-- Select an option --")
        self.ui.layer_post_heating_strategy_scan_strategy.addItem("-- Select an option --")
        self.ui.layer_post_heating_strategy_combobox.addItem("-- Select an option --")
        self.ui.load_existing_layer_melting_startegy_combobox.addItem("-- Select an option --")
        self.ui.layer_melting_strategy_scan_strategy.addItem("-- Select an option --")
        self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.addItem("-- Select an option --")
        self.ui.am_part_layer_melting_ppi_related_am_part_comboBox_2.addItem("-- Select an option --")
        self.ui.correspond_layer_build_model_am_part_conbobox_2.addItem("-- Select an option --")
        self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.addItem("-- Select an option --")
        self.ui.load_an_existing_layer_melting_ppi_combobox.addItem("-- Select an option --")
        self.ui.correspond_layer_melting_strategy_combobox.addItem("-- Select an option --")
        self.ui.correspond_layer_build_model_combobox_2.addItem("-- Select an option --")
        self.ui.composed_of_am_part_melting_ppi_combobox.addItem("-- Select an option --")
        self.ui.load_machine_feed_strategy_comboBox.addItem("-- Select an option --")
        self.ui.load_machine_feed_instructions_comboBox.addItem("-- Select an option --")
        self.ui.load_start_heat_ppi_comboBox.addItem("-- Select an option --")
        self.ui.load_start_heat_startegy_comboBox.addItem("-- Select an option --")
        self.ui.strat_heating_pp_correspond_strategy.addItem("-- Select an option --")
        self.ui.start_heating_scan_strategy.addItem("-- Select an option --")
        self.ui.input_printing_ppi_file.setEnabled(False)
        self.ui.input_printing_ppi_list_layer_thicknesses.setEnabled(False)
        self.ui.add_buil_model_button_2.setEnabled(False)
        self.ui.define_scan_strategy_pushButton.clicked.connect(self.define_scan_strategy_func)
        self.ui.define_start_heating_pushButton.clicked.connect(self.define_start_heating_func)
        self.ui.am_part_pre_heating_strategy_groupBox.setChecked(False)
        self.ui.am_part_pre_heating_PPI_groupBox.setChecked(False)
        self.ui.am_part_post_heating_strategy_groupBox.setChecked(False)
        self.ui.am_part_post_heating_PPI_groupBox.setChecked(False)
        self.ui.am_part_melting_strategy_groupBox.setChecked(False)
        self.ui.am_part_melting_PPI_groupBox.setChecked(False)
        self.ui.am_part_post_heating_strategy_groupBox.setChecked(False)
        self.ui.am_part_post_heating_PPI_groupBox.setChecked(False)
        self.ui.groupBox_4.setChecked(False)
        self.ui.machin_instructions_groupbox.setChecked(False)
        self.ui.add_part_support.setChecked(False)
        self.ui.choose_support.setEnabled(False)
        self.ui.printed_build_PB_AM_part_support_comboBox.setEnabled(False)
        self.ui.load_exist_printing_instructions_comboBox.setEnabled(False)
        self.ui.groupBox_3.setChecked(False)
        self.ui.groupBox_7.setChecked(False)
        self.ui.load_machine_feed_strategy_comboBox.setEnabled(False)
        self.ui.load_machine_feed_instructions_comboBox.setEnabled(False)
        self.ui.load_sensor_comboBox.setEnabled(False)
        self.ui.load_an_existing_layer_pr_heating_ppi_combobox.setEnabled(False)
        self.ui.load_start_heat_ppi_comboBox.setEnabled(False)
        self.ui.load_start_heat_startegy_comboBox.setEnabled(False)
        self.ui.groupBox_4.setChecked(False)
        self.ui.am_part_pre_heating_strategy_groupBox.setChecked(False)
        self.ui.am_part_pre_heating_PPI_groupBox.setChecked(False)
        self.ui.am_part_post_heating_strategy_groupBox.setChecked(False)
        self.ui.am_part_post_heating_strategy_groupBox.setChecked(False)
        self.ui.am_part_post_heating_PPI_groupBox.setChecked(False)
        self.ui.am_part_melting_strategy_groupBox.setChecked(False)
        self.ui.am_part_melting_PPI_groupBox.setChecked(False)
        self.ui.groupBox_50.setChecked(False)
        self.ui.load_an_existing_layer_pr_heating.setEnabled(False)
        self.ui.composed_of_am_part_pre_startegies_combobox.setEnabled(False)
        self.ui.load_existing_post_heating_combobox.setEnabled(False)
        self.ui.layer_post_heating_strategy_combobox.setEnabled(False)
        self.ui.composed_of_am_part_post_heating_ppi_combobox.setEnabled(False)
        self.ui.load_existing_layer_melting_startegy_combobox.setEnabled(False)
        self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.setEnabled(False)
        self.ui.composed_of_am_part_melting_ppi_combobox.setEnabled(False)
        self.ui.load_existing_post_heating_combobox.setEnabled(False)
        self.ui.layer_post_heating_strategy_combobox.setEnabled(False)
        self.ui.load_an_existing_layer_post_heating_ppi_combobox.setEnabled(False)
        self.ui.composed_of_am_part_post_heating_ppi_combobox.setEnabled(False)
        self.ui.layer_pre_heating_strategy_okay.clicked.connect(self.layer_pre_heating_strategy_okay_func)
        self.ui.add_am_part_layer_pre_heating_strategy_to_layer_pre_strategypushButton.clicked.connect(
            self.add_am_part_layer_pre_heating_strategy_to_layer_pre_strategy_func)
        self.ui.correspond_layer_pre_heating_ppi_to_layer_pre_strategypushButton.clicked.connect(
            self.correspond_layer_pre_heating_ppi_to_layer_pre_strategy_func)
        self.ui.addam_part_layer_pre_heating_ppi_to_layer_pre_ppipushButton.clicked.connect(
            self.addam_part_layer_pre_heating_ppi_to_layer_pre_ppi_func)
        self.ui.layer_post_heating_strategy_okay.clicked.connect(self.layer_post_heating_strategy_okay_func)
        self.ui.define_am_part_post_heating_pushbutton.clicked.connect(self.define_am_part_post_heating_func)
        self.ui.correspond_layer_post_heating_ppi_pushbutton.clicked.connect(
            self.correspond_layer_post_heating_ppi_func)
        self.ui.add_am_part_post_heat_ppi_to_list_pushbutton.clicked.connect(
            self.add_am_part_post_heat_ppi_to_list_pushbutton_func)
        self.ui.add_am_part_pre_heat_ppi_to_list_pushbutton.clicked.connect(
            self.add_am_part_pre_heat_ppi_to_list_pushbutton_func)
        self.ui.add_am_part_pre_heat_strategy_to_list_pushbutton.clicked.connect(
            self.add_am_part_pre_heat_strategy_to_list_pushbutton_func)
        self.ui.add_am_part_post_heat_strategy_to_list_pushbutton.clicked.connect(
            self.add_am_part_post_heat_strategy_to_list_pushbutton_func)
        self.ui.add_am_part_melting_strategy_to_list_pushbutton.clicked.connect(
            self.add_am_part_melting_strategy_to_list_pushbutton_func)
        self.ui.add_to_suppervisor_list_pushbutton.clicked.connect(self.add_to_suppervisor_list_pushbutton_func)
        self.ui.add_am_part_melting_ppi_to_list_pushbutton.clicked.connect(
            self.add_am_part_melting_ppi_to_list_pushbutton_func)
        self.ui.addam_part_layer_post_heating_ppi_to_layer_post_ppipushButton.clicked.connect(
            self.addam_part_layer_post_heating_ppi_to_layer_post_ppi_func)
        self.ui.add_layer_melting_strategy_pushbutton.clicked.connect(self.add_layer_melting_strategy_func)
        self.ui.define_am_part_melting_strategy_pushbutton.clicked.connect(self.define_am_part_melting_strategy_func)
        self.ui.correspond_layer_melting_ppi_pushbutton.clicked.connect(self.correspond_layer_melting_ppi_func)
        self.ui.addam_part_layer_melting_ppi_to_layer_melting_ppi_pushButton.clicked.connect(
            self.addam_part_layer_melting_ppi_to_layer_melting_ppi_func)
        self.ui.define_printing_process_pushButton.clicked.connect(self.define_printing_process_func)
        self.ui.set_as_input_printing_process_pushButton.clicked.connect(
            self.set_as_input_printing_process_pushButton_func)
        self.setup_button_reset_on_groupbox_change_11(self.ui.define_printing_process_pushButton,
                                                      self.ui.printing_process_groupBox)
        self.ui.add_sensor_to_printing_machine_pushButton.clicked.connect(self.add_sensor_to_printing_machine_func)
        self.ui.define_printing_machine_pushButton.clicked.connect(self.define_printing_machine_func)
        self.ui.define_printed_build_support_pushButton.clicked.connect(self.define_printed_build_support_func)
        self.ui.define_printed_build_AM_part_pushButton.clicked.connect(self.define_printed_build_AM_part_func)
        self.ui.define_printed_build_pushButton.clicked.connect(self.define_printed_build_func)
        self.ui.printed_build_PB_AM_part_has_support_checkBox.stateChanged.connect(
            self.toggle_choose_support_printing_process)
        self.ui.add_printed_build_PB_AM_part_pushButton.clicked.connect(self.add_printed_build_PB_AM_part_func)
        self.setup_button_reset_on_groupbox_change_11(self.ui.define_printed_build_pushButton, self.ui.groupBox_22,
                                                      [self.ui.groupBox_6, self.ui.printed_build_am_part_groupBox,
                                                       self.ui.printed_build_support_groupBox])
        self.ui.define_material_pushButton.clicked.connect(self.define_material_func)
        self.ui.define_manufacturer_pushButton.clicked.connect(self.define_manufacturer_func)
        self.ui.define_printing_medium_pushButton.clicked.connect(self.define_printing_medium_func)
        self.ui.define_build_plate_pushButton.clicked.connect(self.define_build_plate_func)
        self.ui.add_part_to_build_model_button.clicked.connect(self.add_part_to_build_model_func)
        self.ui.add_buil_model_button.clicked.connect(self.add_buil_model_func)
        self.ui.add_buil_model_button_2.clicked.connect(self.add_buil_model_2_func)
        self.setup_button_reset_on_groupbox_change_11(self.ui.add_buil_model_button, self.ui.define_build_model,
                                                      [self.ui.add_part_support])
        self.setup_button_reset_on_groupbox_change_11(self.ui.add_buil_model_button_2, self.ui.groupBox_27)
        self.ui.part_support_in_model_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.part_support_in_model_list.customContextMenuRequested.connect(self.part_support_in_model_list_menu)
        self.ui.existing_digital_build_model_listwidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.existing_digital_build_model_listwidget.customContextMenuRequested.connect(
            self.existing_digital_build_model_listwidget_menu)
        self.ui.selected_digital_build_model.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.selected_digital_build_model.customContextMenuRequested.connect(self.selected_digital_build_model_menu)
        self.ui.defined_materials_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_materials_listWidget.customContextMenuRequested.connect(self.defined_materials_listWidget_menu)
        self.ui.defined_manufactures_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_manufactures_listWidget.customContextMenuRequested.connect(
            self.defined_manufactures_listWidget_menu)
        self.ui.list_existing_model_layers.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_existing_model_layers.customContextMenuRequested.connect(self.list_existing_model_layers_menu)
        self.ui.existing_ppi_listwidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.existing_ppi_listwidget.customContextMenuRequested.connect(self.existing_ppi_listwidget_menu)
        self.ui.list_output_layer_decomposition.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_output_layer_decomposition.customContextMenuRequested.connect(
            self.list_output_layer_decomposition_menu)
        self.ui.list_output_part_layer_decomposition.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_output_part_layer_decomposition.customContextMenuRequested.connect(
            self.list_output_part_layer_decomposition_menu)
        self.ui.defined_machine_powder_control_strategies_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_machine_powder_control_strategies_listwidget.customContextMenuRequested.connect(
            self.defined_machine_powder_control_strategies_listwidget_menu)
        self.ui.defined_machine_control_ppi_listwidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_machine_control_ppi_listwidget.customContextMenuRequested.connect(
            self.defined_machine_control_ppi_listwidget_menu)
        self.ui.defined_start_heat_ppi_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_start_heat_ppi_listWidget.customContextMenuRequested.connect(
            self.defined_start_heat_ppi_listWidget_menu)
        self.ui.defined_start_heating_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_start_heating_listWidget.customContextMenuRequested.connect(
            self.defined_start_heating_listWidget_menu)
        self.ui.defined_scan_strategy_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_scan_strategy_listWidget.customContextMenuRequested.connect(
            self.defined_scan_strategy_listWidget_menu)
        self.ui.list_layer_pre_heating_in_beam_control_listWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_layer_pre_heating_in_beam_control_listWidget.customContextMenuRequested.connect(
            self.list_layer_pre_heating_in_beam_control_listWidget_menu)
        self.ui.list_layer_post_heating_in_beam_control_listWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_layer_post_heating_in_beam_control_listWidget.customContextMenuRequested.connect(
            self.list_layer_post_heating_in_beam_control_listWidget_menu)
        self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.customContextMenuRequested.connect(
            self.list_of_layer_melting_strategy_used_in_beam_control_listwidget_menu)
        self.ui.list_defined_layer_pre_heating_strategy_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_layer_pre_heating_strategy_listwidget.customContextMenuRequested.connect(
            self.list_defined_layer_pre_heating_strategy_listwidget_menu)
        self.ui.list_defined_layer_post_heating_strategy_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_layer_post_heating_strategy_listwidget.customContextMenuRequested.connect(
            self.list_defined_layer_post_heating_strategy_listwidget_menu)
        self.ui.list_defined_A_part_layer_melting_strategy_listwidget_2.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_A_part_layer_melting_strategy_listwidget_2.customContextMenuRequested.connect(
            self.list_defined_A_part_layer_melting_strategy_listwidget_2_menu)
        self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_pre_heating_ppi_listWidget_menu)
        self.ui.composed_of_am_part_layer_pre_heating_strategy_listWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_pre_heating_strategy_listWidget.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_pre_heating_strategy_listWidget_menu)
        self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_post_heating_strategy_listWidget_menu)
        self.ui.composed_of_am_part_layer_melting_strategy_listWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_melting_strategy_listWidget.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_melting_strategy_listWidget_menu)
        self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_post_heating_ppi_listWidget_menu)
        self.ui.composed_of_am_part_layer_melting_ppi_listWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_melting_ppi_listWidget.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_melting_ppi_listWidget_menu)
        self.ui.list_pre_heating_ppi_in_beam_control.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_pre_heating_ppi_in_beam_control.customContextMenuRequested.connect(
            self.list_pre_heating_ppi_in_beam_control_menu)
        self.ui.layer_post_heating_ppi_used_beam_control_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.layer_post_heating_ppi_used_beam_control_listwidget.customContextMenuRequested.connect(
            self.layer_post_heating_ppi_used_beam_control_listwidget_menu)
        self.ui.layer_melting_ppi_used_beam_control_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.layer_melting_ppi_used_beam_control_listwidget.customContextMenuRequested.connect(
            self.layer_melting_ppi_used_beam_control_listwidget_menu)
        self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget_2.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget_2.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_pre_heating_ppi_listWidget_2_menu)
        self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget_2.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget_2.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_post_heating_ppi_listWidget_2_menu)
        self.ui.composed_of_am_part_layer_melting_ppi_listWidget_2.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.composed_of_am_part_layer_melting_ppi_listWidget_2.customContextMenuRequested.connect(
            self.composed_of_am_part_layer_melting_ppi_listWidget_2_menu)
        self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.customContextMenuRequested.connect(
            self.list_defined_A_part_layer_pre_heating_strategy_listwidget_menu)
        self.ui.list_defined_A_part_layer_post_heating_strategy_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_A_part_layer_post_heating_strategy_listwidget.customContextMenuRequested.connect(
            self.list_defined_A_part_layer_post_heating_strategy_listwidget_menu)
        self.ui.list_defined_A_part_layer_melting_strategy_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_A_part_layer_melting_strategy_listwidget.customContextMenuRequested.connect(
            self.list_defined_A_part_layer_melting_strategy_listwidget_menu)
        self.ui.list_defined_AM_part_layer_pre_heating_strategy_ppi_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_AM_part_layer_pre_heating_strategy_ppi_listwidget.customContextMenuRequested.connect(
            self.list_defined_AM_part_layer_pre_heating_strategy_ppi_listwidget_menu)
        self.ui.list_defined_AM_part_layer_post_heating_strategy_ppi_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_AM_part_layer_post_heating_strategy_ppi_listwidget.customContextMenuRequested.connect(
            self.list_defined_AM_part_layer_post_heating_strategy_ppi_listwidget_menu)
        self.ui.list_defined_AM_part_layer_melting_strategy_ppi_listwidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_defined_AM_part_layer_melting_strategy_ppi_listwidget.customContextMenuRequested.connect(
            self.list_defined_AM_part_layer_melting_strategy_ppi_listwidget_menu)
        self.ui.defined_start_heating_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_existing_part_model_layers.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.list_existing_part_model_layers.customContextMenuRequested.connect(
            self.list_existing_part_model_layers_menu)
        self.ui.define_supervisor_button.clicked.connect(self.define_supervisor_func)
        self.ui.defined_printing_medium_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_printing_medium_listWidget.customContextMenuRequested.connect(
            self.defined_printing_medium_listWidget_menu)
        self.ui.defined_build_plate_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_build_plate_listWidget.customContextMenuRequested.connect(
            self.defined_build_plate_listWidget_menu)
        self.ui.defined_printing_machines_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_printing_machines_listWidget.customContextMenuRequested.connect(
            self.defined_printing_machines_listWidget_menu)
        self.ui.defined_Printed_Builds_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_Printed_Builds_listWidget.customContextMenuRequested.connect(
            self.defined_Printed_Builds_listWidget_menu)
        self.ui.defined_printed_build_AM_part_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_printed_build_AM_part_listWidget.customContextMenuRequested.connect(
            self.defined_printed_build_AM_part_listWidget_menu)
        self.ui.defined_printed_build_support_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_printed_build_support_listWidget.customContextMenuRequested.connect(
            self.defined_printed_build_support_listWidget_menu)
        self.ui.defined_sensors_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.defined_sensors_listWidget.customContextMenuRequested.connect(self.defined_sensors_listWidget_menu)
        self.ui.existing_sensors_listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.existing_sensors_listWidget.customContextMenuRequested.connect(self.existing_sensors_listWidget_menu)
        self.ui.add_model_design_process_button.clicked.connect(self.add_model_design_process_func)
        self.setup_button_reset_on_groupbox_change_10(self.ui.add_model_design_process_button,
                                                      self.ui.pbf_build_model_design_process)
        self.ui.load_build_model_checkBox.stateChanged.connect(self.toggle_load_buildmodel_combobox)
        self.ui.load_buildmodel_combobox.setEnabled(False)
        self.ui.define_support_button.clicked.connect(self.define_support_func)
        self.ui.define_am_part_button.clicked.connect(self.define_am_part_func)
        self.ui.has_support_checkBox.stateChanged.connect(self.toggle_choose_support)
        self.ui.choose_support.setEnabled(False)
        self.ui.define_printing_instructions_pushButton.clicked.connect(self.define_printing_instructions_func)
        self.setup_button_reset_on_groupbox_change_11(self.ui.define_printing_instructions_pushButton,
                                                      self.ui.printing_instructions_groupBox)
        self.ui.define_slicing_process_pushButton.clicked.connect(self.define_slicing_process_func)
        self.setup_button_reset_on_groupbox_change_6(self.ui.define_slicing_process_pushButton,
                                                     self.ui.slicing_process_groupbox)
        self.ui.okay_beam_control_strategy_pushButton.clicked.connect(self.okay_beam_control_strategy_func)
        self.setup_button_reset_on_groupbox_change_11(self.ui.okay_beam_control_strategy_pushButton, self.ui.groupBox_2,
                                                      [self.ui.scan_strategy, self.ui.start_heating_strategy_groupbox,
                                                       self.ui.groupBox_10, self.ui.groupBox_12, self.ui.groupBox_14])
        self.ui.machine_feed_strategy_checkBox.stateChanged.connect(self.toggle_load_machine_feed_strategy_comboBox)
        self.ui.load_sensor_checkBox.stateChanged.connect(self.toggle_load_sensor_comboBox)
        self.ui.load_layer_checkbox_3.stateChanged.connect(self.toggle_load_exist_printing_instructions_comboBox)
        self.ui.load_exist_printing_instructions_comboBox.setEnabled(False)
        self.ui.composed_of_am_part_pre_startegies_checkBox.stateChanged.connect(
            self.toggle_composed_of_am_part_pre_startegies_combobox)
        self.ui.load_an_existing_layer_pr_heating_checkBox.stateChanged.connect(
            self.toggle_load_an_existing_layer_pr_heating)
        self.ui.load_an_existing_layer_pr_heating_ppi_checkBox.stateChanged.connect(
            self.toggle_load_an_existing_layer_pr_heating_ppi_combobox)
        self.ui.load_machine_feed_instructions_checkBox.stateChanged.connect(
            self.toggle_load_machine_feed_instructions_comboBox)
        self.ui.load_start_heat_startegy_checkbox.stateChanged.connect(self.toggle_load_start_heat_startegy_comboBox)
        self.ui.load_start_heat_ppi_checkbox.stateChanged.connect(self.toggle_load_start_heat_ppi_comboBox)
        self.ui.load_existing_post_heating_checkbox.stateChanged.connect(
            self.toggle_load_existing_post_heating_combobox)
        self.ui.layer_post_heating_strategy_checkbox.stateChanged.connect(
            self.toggle_layer_post_heating_strategy_combobox)
        self.ui.load_existing_layer_melting_startegy_checkbox.stateChanged.connect(
            self.toggle_load_existing_layer_melting_startegy_combobox)
        self.ui.composed_of_am_part_layer_melting_strategy_checkbox.stateChanged.connect(
            self.toggle_composed_of_am_part_layer_melting_strategy_combobox_2)
        self.ui.load_an_existing_layer_melting_ppi_checkBox.stateChanged.connect(
            self.toggle_load_an_existing_layer_melting_ppi_combobox)
        self.ui.composed_of_am_part_melting_ppi_checkBox.stateChanged.connect(
            self.toggle_composed_of_am_part_melting_ppi_combobox)
        self.ui.load_an_existing_layer_post_heating_ppi_checkBox.stateChanged.connect(
            self.toggle_load_an_existing_layer_post_heating_ppi_combobox)
        self.ui.composed_of_am_part_post_heating_ppi_checkBox.stateChanged.connect(
            self.toggle_composed_of_am_part_post_heating_ppi_combobox)
        # --------------Monitoring Process-----------------
        self.ui.define_monitoring_process_pushButton.clicked.connect(self.define_monitoring_process_func)
        self.setup_button_reset_on_groupbox_change_10(self.ui.define_monitoring_process_pushButton, self.ui.groupBox_23)
        self.ui.define_post_printing_method_pushButton.clicked.connect(self.define_post_printing_method_func)
        self.ui.define_postPrinting_process_pushButton.clicked.connect(self.define_postPrinting_process_func)
        self.ui.add_postprinting_methods_to_process_pushButton.clicked.connect(
            self.add_postprinting_methods_to_process_func)
        self.setup_button_reset_on_groupbox_change_11(self.ui.define_postPrinting_process_pushButton,
                                                      self.ui.groupBox_25, exclude_groupboxs=[self.ui.groupBox_19])
        self.ui.define_testin_method_pushButton.clicked.connect(self.define_testing_method_func)
        self.ui.Testing_Method_Okay_spushButton.clicked.connect(self.Testing_Method_Okay_func)
        self.ui.Add_Testing_Method_pushButton.clicked.connect(self.Add_Testing_Method_func)
        self.setup_button_reset_on_groupbox_change_11(self.ui.Testing_Method_Okay_spushButton, self.ui.groupBox_29,
                                                      [self.ui.groupBox_16, self.ui.groupBox_17])
        # ------------------------------------------------------------
        self.ui.beam_control_strategy_name_2.setEnabled(False)
        self.ui.beam_control_strategy_file_2.setEnabled(False)
        self.ui.beam_control_strategy_file_format_2.setEnabled(False)
        self.ui.load_an_existing_layer_melting_ppi_combobox.setEnabled(False)
        self.ui.beam_control_strategy_name_3.setEnabled(False)
        self.ui.beam_control_strategy_file_3.setEnabled(False)
        self.ui.beam_control_strategy_file_format_3.setEnabled(False)
        self.ui.beam_control_strategy_name_4.setEnabled(False)
        self.ui.beam_control_strategy_file_4.setEnabled(False)
        self.ui.beam_control_strategy_file_format_4.setEnabled(False)
        self.ui.load_buildmodel_combobox.currentIndexChanged.connect(self.load_buildmodel_combobox_on_selection)
        self.ui.input_printing_ppi_name.currentIndexChanged.connect(self.input_printing_ppi_name_on_selection)
        # For specify order of field when using tab key---------------
        for widget in [self.ui.material_name, self.ui.material_melting_point,
                       self.ui.material_oxidation_resistance, self.ui.material_heat_capacity,
                       self.ui.material__formula, self.ui.material_density,
                       self.ui.material_electrical_resitivity, self.ui.material_beam_absorption_rate,
                       self.ui.material_thermal_conductivity, self.ui.material_electrical_conductivity,
                       self.ui.material_thermal_diffusivity, self.ui.material_comment, ]:
            widget.installEventFilter(self)
        QWidget.setTabOrder(self.ui.material_name, self.ui.material_melting_point)
        QWidget.setTabOrder(self.ui.material_melting_point, self.ui.material_oxidation_resistance)
        QWidget.setTabOrder(self.ui.material_oxidation_resistance, self.ui.material_heat_capacity)
        QWidget.setTabOrder(self.ui.material_heat_capacity, self.ui.material__formula)
        QWidget.setTabOrder(self.ui.material__formula, self.ui.material_density)
        QWidget.setTabOrder(self.ui.material_density, self.ui.material_electrical_resitivity)
        QWidget.setTabOrder(self.ui.material_electrical_resitivity, self.ui.material_beam_absorption_rate)
        QWidget.setTabOrder(self.ui.material_beam_absorption_rate, self.ui.material_thermal_conductivity)
        QWidget.setTabOrder(self.ui.material_thermal_conductivity, self.ui.material_electrical_conductivity)
        QWidget.setTabOrder(self.ui.material_electrical_conductivity, self.ui.material_thermal_diffusivity)
        QWidget.setTabOrder(self.ui.material_thermal_diffusivity, self.ui.material_comment)
        # ------------------------------------------------------------
        for widget in [self.ui.build_model_name, self.ui.build_model_file_path, self.ui.Build_model_dimension,
                       self.ui.build_model_file_format, self.ui.build_model_comment]:
            widget.installEventFilter(self)
        for widget in [self.ui.support_name, self.ui.support_file_path, self.ui.support_file_format,
                       self.ui.support_comment, ]: widget.installEventFilter(self)
        for widget in [self.ui.am_part_name, self.ui.am_part__dimension, self.ui.am_part_file_path,
                       self.ui.am_part_file_format, self.ui.am_part_comment]:
            widget.installEventFilter(self)
        # Build model tab order
        QWidget.setTabOrder(self.ui.build_model_name, self.ui.build_model_file_path)
        QWidget.setTabOrder(self.ui.build_model_file_path, self.ui.build_model_file_format)
        QWidget.setTabOrder(self.ui.build_model_file_format, self.ui.Build_model_dimension)
        QWidget.setTabOrder(self.ui.Build_model_dimension, self.ui.build_model_comment)
        # Support tab order
        QWidget.setTabOrder(self.ui.build_model_comment, self.ui.support_name)
        QWidget.setTabOrder(self.ui.support_name, self.ui.support_file_path)
        QWidget.setTabOrder(self.ui.support_file_path, self.ui.support_file_format)
        QWidget.setTabOrder(self.ui.support_file_format, self.ui.support_comment)
        # AM part tab order
        QWidget.setTabOrder(self.ui.support_comment, self.ui.am_part_name)
        QWidget.setTabOrder(self.ui.am_part_name, self.ui.am_part__dimension)
        QWidget.setTabOrder(self.ui.am_part__dimension, self.ui.am_part_file_path)
        QWidget.setTabOrder(self.ui.am_part_file_path, self.ui.am_part_file_format)
        QWidget.setTabOrder(self.ui.am_part_file_format, self.ui.am_part_comment)
        for item in supervisors_list:
            self.ui.defined_supervisors_list.addItem(item.supervisor_name)
            self.ui.selectSupervisor.addItem(item.supervisor_name)
        for item in Post_Printing_Methods_list:
            self.ui.defined_PostPrinting_methods_listWidget.addItem(item.post_printing_method_name)
        for widget in [self.ui.manufacturer_name, self.ui.manufacturer_address, self.ui.manufacturer_comment]:
            widget.installEventFilter(self)
        QWidget.setTabOrder(self.ui.manufacturer_name, self.ui.manufacturer_address)
        QWidget.setTabOrder(self.ui.manufacturer_address, self.ui.manufacturer_comment)
        for widget in [self.ui.printing_medium_name, self.ui.printing_medium_status,
                       self.ui.printing_medium_particle_size, self.ui.metal_powder_checkBox,
                       self.ui.printing_medium_material_comboBox, self.ui.printing_medium_particle_morphology,
                       self.ui.printing_medium_manufacturer_comboBox
            , self.ui.printing_medium_comment]:
            widget.installEventFilter(self)
        QWidget.setTabOrder(self.ui.printing_medium_name, self.ui.printing_medium_status)
        QWidget.setTabOrder(self.ui.printing_medium_status, self.ui.printing_medium_particle_size)
        QWidget.setTabOrder(self.ui.printing_medium_particle_size, self.ui.metal_powder_checkBox)
        QWidget.setTabOrder(self.ui.metal_powder_checkBox, self.ui.printing_medium_material_comboBox)
        QWidget.setTabOrder(self.ui.printing_medium_material_comboBox, self.ui.printing_medium_particle_morphology)
        QWidget.setTabOrder(self.ui.printing_medium_particle_morphology, self.ui.printing_medium_manufacturer_comboBox)
        QWidget.setTabOrder(self.ui.printing_medium_manufacturer_comboBox, self.ui.printing_medium_comment)
        for widget in [self.ui.build_plate_name, self.ui.build_plate_surface_texture,
                       self.ui.build_plate_material_comboBox, self.ui.build_plate_size,
                       self.ui.build_plate_shape, self.ui.build_plate_comment
            , self.ui.build_plate_thickness, self.ui.build_plate_manufacturer_comboBox]:
            widget.installEventFilter(self)
        QWidget.setTabOrder(self.ui.build_plate_name, self.ui.build_plate_surface_texture)
        QWidget.setTabOrder(self.ui.build_plate_surface_texture, self.ui.build_plate_material_comboBox)
        QWidget.setTabOrder(self.ui.build_plate_material_comboBox, self.ui.build_plate_size)
        QWidget.setTabOrder(self.ui.build_plate_size, self.ui.build_plate_shape)
        QWidget.setTabOrder(self.ui.build_plate_shape, self.ui.build_plate_comment)
        QWidget.setTabOrder(self.ui.build_plate_comment, self.ui.build_plate_thickness)
        QWidget.setTabOrder(self.ui.build_plate_thickness, self.ui.build_plate_manufacturer_comboBox)
        for widget in [self.ui.printing_process_instructions_name,
                       self.ui.printing_process_instructions_layer_thicknesses,
                       self.ui.printing_process_instructions_file, self.ui.printing_process_instructions_file_format,
                       self.ui.printing_process_instructions_comment]:
            widget.installEventFilter(self)
        QWidget.setTabOrder(self.ui.printing_process_instructions_name,
                            self.ui.printing_process_instructions_layer_thicknesses)
        QWidget.setTabOrder(self.ui.printing_process_instructions_layer_thicknesses,
                            self.ui.printing_process_instructions_file)
        QWidget.setTabOrder(self.ui.printing_process_instructions_file,
                            self.ui.printing_process_instructions_file_format)
        QWidget.setTabOrder(self.ui.printing_process_instructions_file_format,
                            self.ui.printing_process_instructions_comment)
        for widget in [self.ui.LayerBuildModel_name, self.ui.LayerBuildModel_layer_height, self.ui.LayerBuildModel_file,
                       self.ui.LayerBuildModel_file_format, self.ui.LayerBuildModel_layer_number,
                       self.ui.LayerBuildModel_comment]:
            widget.installEventFilter(self)
        QWidget.setTabOrder(self.ui.LayerBuildModel_name, self.ui.LayerBuildModel_layer_height)
        QWidget.setTabOrder(self.ui.LayerBuildModel_layer_height, self.ui.LayerBuildModel_file)
        QWidget.setTabOrder(self.ui.LayerBuildModel_file, self.ui.LayerBuildModel_file_format)
        QWidget.setTabOrder(self.ui.LayerBuildModel_file_format, self.ui.LayerBuildModel_layer_number)
        QWidget.setTabOrder(self.ui.LayerBuildModel_layer_number, self.ui.LayerBuildModel_comment)
        # ---------------------------------------------------------------------------------
        tab_widgets = [self.ui.machine_feed_strategy_name, self.ui.machine_feed_strategy_file,
                       self.ui.machine_feed_strategy_file_format, self.ui.machine_feed_strategy_full_repeats,
                       self.ui.machine_feed_strategy_recoater_speed, self.ui.machine_feed_strategy_retract_speed,
                       self.ui.machine_feed_strategy_build_repeats, self.ui.machine_feed_strategy_triggered_start,
                       self.ui.machine_feed_strategy_dwell_time, self.ui.machine_feed_strategy_comment, ]
        for w in tab_widgets: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets, tab_widgets[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_2 = [self.ui.beam_control_strategy_name, self.ui.beam_control_strategy_file,
                         self.ui.beam_control_strategy_file_format]
        for w in tab_widgets_2: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_2, tab_widgets_2[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_3 = [self.ui.scan_strategy_name, self.ui.scan_strategy_spot_size, self.ui.scan_strategy_dwell_time,
                         self.ui.scan_strategy_point_distance,
                         self.ui.scan_strategy_strategy_name, self.ui.scan_strategy_comment,
                         self.ui.scan_strategy_scan_speed, self.ui.scan_strategy_beam_power]
        for w in tab_widgets_3: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_3, tab_widgets_3[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_4 = [self.ui.start_heating_name, self.ui.start_heating_file_format, self.ui.start_heating_size,
                         self.ui.start_heating_timeout, self.ui.start_heating_scan_strategy, self.ui.start_heating_file,
                         self.ui.start_heating_target_tmprature, self.ui.start_heating_shape,
                         self.ui.start_heating_rotation_angle, self.ui.start_heating_comment]
        for w in tab_widgets_4: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_4, tab_widgets_4[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_5 = [self.ui.strat_heating_printing_process_instruct_name,
                         self.ui.strat_heating_printing_process_instruct_file_format,
                         self.ui.strat_heating_printing_process_instruct_file]
        for w in tab_widgets_5: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_5, tab_widgets_5[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_6 = [self.ui.am_part_layer_pre_heating_strategy_name,
                         self.ui.am_part_layer_pre_heating_strategy_file,
                         self.ui.am_part_layer_pre_heating_strategy_file_format,
                         self.ui.am_part_layer_pre_heating_strategy_scan_startegy,
                         self.ui.am_part_layer_pre_heating_strategy_rotation_angle,
                         self.ui.am_part_layer_pre_heating_strategy_number_repetitions,
                         self.ui.am_part_layer_pre_heating_strategy_number_comment]
        for w in tab_widgets_6: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_6, tab_widgets_6[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_7 = [self.ui.layer_pre_heating_strategy_name, self.ui.layer_pre_heating_strategy_file,
                         self.ui.layer_pre_heating_strategy_file_format,
                         self.ui.layer_pre_heating_strategy_scan_strategy,
                         self.ui.composed_of_am_part_pre_startegies_combobox]
        for w in tab_widgets_7: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_7, tab_widgets_7[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_8 = [self.ui.am_part_layer_pre_heating_ppi_name, self.ui.am_part_layer_pre_heating_ppi_file,
                         self.ui.am_part_layer_pre_heating_ppi_file_format,
                         self.ui.am_part_layer_pre_heating_ppi_related_am_part_comboBox,
                         self.ui.am_part_layer_pre_heating_ppi_correspond_am_part,
                         self.ui.correspond_am_part_layer_pre_heating,
                         self.ui.am_part_layer_pre_heating_ppi_comment]
        for w in tab_widgets_8: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_8, tab_widgets_8[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_9 = [self.ui.layer_pre_heating_ppi_name, self.ui.layer_pre_heating_ppi_file,
                         self.ui.layer_pre_heating_ppi_file_format, self.ui.layer_pre_heating_ppi_layer_number,
                         self.ui.correspond_to_layer_pre_heating_combobox,
                         self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox,
                         self.ui.composed_of_am_part_pre_heating_ppi_checkBox,
                         self.ui.composed_of_am_part_pre_heating_ppi_combobox,
                         self.ui.layer_pre_heating_ppi_comment]
        for w in tab_widgets_9: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_9, tab_widgets_9[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_10 = [self.ui.layer_post_heating_strategy_name, self.ui.layer_post_heating_strategy_file,
                          self.ui.layer_post_heating_strategy_file_format,
                          self.ui.layer_post_heating_strategy_scan_strategy,
                          self.ui.layer_post_heating_strategy_checkbox, self.ui.layer_post_heating_strategy_combobox,
                          self.ui.layer_post_heating_strategy_comment]
        for w in tab_widgets_10: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_10, tab_widgets_10[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_11 = [self.ui.am_part_layer_post_heating_strategy_name,
                          self.ui.am_part_layer_post_heating_strategy_file,
                          self.ui.am_part_layer_post_heating_strategy_file_format,
                          self.ui.am_part_layer_post_heating_strategy_scan_strategy,
                          self.ui.am_part_layer_post_heating_strategy_rotation_angle,
                          self.ui.am_part_layer_post_heating_strategy_number_repetitions,
                          self.ui.am_part_layer_post_heating_strategy_number_comment]
        for w in tab_widgets_11: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_11, tab_widgets_11[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_12 = [self.ui.layer_post_heating_ppi_name, self.ui.layer_post_heating_ppi_file,
                          self.ui.layer_post_heating_ppi_file_format,
                          self.ui.layer_post_heating_ppi_layer_number, self.ui.correspond_layer_post_heating_combobox,
                          self.ui.correspond_layer_build_model_combobox,
                          self.ui.composed_of_am_part_post_heating_ppi_checkBox,
                          self.ui.composed_of_am_part_post_heating_ppi_combobox, self.ui.layer_post_heating_ppi_comment]
        for w in tab_widgets_12: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_12, tab_widgets_12[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_13 = [self.ui.am_part_layer_post_heating_ppi_name, self.ui.am_part_layer_post_heating_ppi_file,
                          self.ui.am_part_layer_post_heating_ppi_file_format,
                          self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox_2,
                          self.ui.correspond_layer_build_model_am_part_conbobox,
                          self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox,
                          self.ui.am_part_layer_post_heating_ppi_comment]
        for w in tab_widgets_13: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_13, tab_widgets_13[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_14 = [self.ui.am_part_layer_melting_strategy_name, self.ui.am_part_layer_melting_strategy_file,
                          self.ui.am_part_layer_melting_strategy_file_format,
                          self.ui.am_part_layer_melting_strategy_scan_strategy,
                          self.ui.am_part_layer_melting_strategy_rotation_angle,
                          self.ui.am_part_layer_melting_strategy_number_repetitions,
                          self.ui.am_part_layer_melting_strategy_point_distance,
                          self.ui.am_part_layer_melting_strategy_energy_density,
                          self.ui.am_part_layer_melting_strategy_offset_margin,
                          self.ui.am_part_layer_melting_strategy_number_comment]
        for w in tab_widgets_14: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_14, tab_widgets_14[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_15 = [self.ui.layer_melting_strategy_name, self.ui.layer_melting_strategy_file,
                          self.ui.layer_melting_strategy_file_format,
                          self.ui.layer_melting_strategy_scan_strategy,
                          self.ui.composed_of_am_part_layer_melting_strategy_checkbox,
                          self.ui.composed_of_am_part_layer_melting_strategy_combobox_2,
                          self.ui.layer_melting_strategy_comment]
        for w in tab_widgets_15: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_15, tab_widgets_15[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_16 = [self.ui.am_part_layer_melting_ppi_name, self.ui.am_part_layer_melting_ppi_file,
                          self.ui.am_part_layer_melting_ppi_file_format,
                          self.ui.am_part_layer_melting_ppi_related_am_part_comboBox_2,
                          self.ui.correspond_layer_build_model_am_part_conbobox_2,
                          self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox,
                          self.ui.am_part_layer_melting_ppi_comment]
        for w in tab_widgets_16: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_16, tab_widgets_16[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_17 = [self.ui.layer_melting_ppi_name, self.ui.layer_melting_ppi_file,
                          self.ui.layer_melting_ppi_file_format,
                          self.ui.layer_melting_ppi_layer_number, self.ui.correspond_layer_melting_strategy_combobox,
                          self.ui.correspond_layer_build_model_combobox_2,
                          self.ui.composed_of_am_part_melting_ppi_checkBox,
                          self.ui.composed_of_am_part_melting_ppi_combobox, self.ui.layer_melting_ppi_comment]
        for w in tab_widgets_17: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_17, tab_widgets_17[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_18 = [self.ui.ProjectName, self.ui.define_project_comment]
        for w in tab_widgets_18: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_18, tab_widgets_18[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_19 = [self.ui.supervisor_name, self.ui.supervisor_name_comment]
        for w in tab_widgets_19: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_19, tab_widgets_19[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_20 = [self.ui.monitoring_process_name, self.ui.monitoring_process_output_file,
                          self.ui.monitoring_process_comment]
        for w in tab_widgets_20: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_20, tab_widgets_20[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_21 = [self.ui.PartLayerBuildModel_name, self.ui.PartLayerBuildModel_file,
                          self.ui.PartLayerBuildModel_file_format, self.ui.PartLayerBuildModel_area,
                          self.ui.PartLayerBuildModel_comment]
        for w in tab_widgets_21: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_21, tab_widgets_21[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_22 = [self.ui.machine_feed_instructions_name, self.ui.machine_feed_instructions_file,
                          self.ui.machine_feed_instructions_file_format]
        for w in tab_widgets_22: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_22, tab_widgets_22[1:]): QWidget.setTabOrder(prev, nxt)
        # ---------------------------------------------------------------------------------
        tab_widgets_23 = [self.ui.sensor_name, self.ui.sensor_type,
                          self.ui.sensor_recorde_data_path]
        for w in tab_widgets_23: w.installEventFilter(self)
        for prev, nxt in zip(tab_widgets_23, tab_widgets_23[1:]): QWidget.setTabOrder(prev, nxt)
    # =======================================================================
    def input_printing_ppi_name_on_selection(self):
        item_text = self.ui.input_printing_ppi_name.currentText()
        if item_text:
            index = next(
                (i for i, cls in enumerate(defined_Printing_Process_Instructions) if cls.ppi_name == item_text), -1)
            if index != -1:
                self.ui.input_printing_ppi_file.setPlainText(defined_Printing_Process_Instructions[index].ppi_file)
                self.ui.input_printing_ppi_list_layer_thicknesses.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_list_layer_thicknesses)
                self.ui.input_printing_ppi_file.setEnabled(False)
                self.ui.input_printing_ppi_list_layer_thicknesses.setEnabled(False)
    # =======================================================================
    def close_func(self):
        self.save_shared_lists()
        self.close()
    # =======================================================================
    def display_pbf_amp_onto(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "PBF_AMP_Onto_v53.pdf")
        self.pdf_window = PDFViewer(file_path)
        self.pdf_window.show()
    # =======================================================================
    def save_shared_lists(self):
        dictionary = {}
        dictionary["PBF_AM_Process_Chains_list"] = PBF_AM_Process_Chains_list
        dictionary["supervisors_list"] = supervisors_list
        dictionary["Build_Model_Support_list"] = Build_Model_Support_list
        dictionary["Build_Model_AM_Part_list"] = Build_Model_AM_Part_list
        dictionary["Defined_Build_models"] = Defined_Build_models
        dictionary["defined_Printing_Process_Instructions"] = defined_Printing_Process_Instructions
        dictionary["Layer_Of_Build_Models_list"] = Layer_Of_Build_Models_list
        dictionary["Layer_Of_Build_Model_AM_Parts_list"] = Layer_Of_Build_Model_AM_Parts_list
        dictionary["Machine_Powder_Feed_Control_Strategies_list"] = Machine_Powder_Feed_Control_Strategies_list
        dictionary["Machine_Powder_Feed_Control_Strategy_PPIs_list"] = Machine_Powder_Feed_Control_Strategy_PPIs_list
        dictionary["Scan_Strategies_list"] = Scan_Strategies_list
        dictionary["Start_Heating_PPI_list"] = Start_Heating_PPI_list
        dictionary["Start_Heating_Strategy_list"] = Start_Heating_Strategy_list
        dictionary["AM_Part_Layer_Pre_Heating_Strategies_list"] = AM_Part_Layer_Pre_Heating_Strategies_list
        dictionary["Layer_Pre_Heating_Strategies_list"] = Layer_Pre_Heating_Strategies_list
        dictionary["AM_Part_Layer_Pre_Heating_PPI_list"] = AM_Part_Layer_Pre_Heating_PPI_list
        dictionary["AM_Part_Layer_Post_Heating_Strategies_list"] = AM_Part_Layer_Post_Heating_Strategies_list
        dictionary["Layer_Post_Heating_Strategies_list"] = Layer_Post_Heating_Strategies_list
        dictionary["AM_Part_Layer_Post_Heating_PPI_list"] = AM_Part_Layer_Post_Heating_PPI_list
        dictionary["Layer_Pre_Heating_PPI_list"] = Layer_Pre_Heating_PPI_list
        dictionary["AM_Part_Layer_Melting_Strategies_list"] = AM_Part_Layer_Melting_Strategies_list
        dictionary["Layer_Melting_Strategies_list"] = Layer_Melting_Strategies_list
        dictionary["AM_Part_Layer_Melting_PPI_list"] = AM_Part_Layer_Melting_PPI_list
        dictionary["Layer_Melting_PPI_list"] = Layer_Melting_PPI_list
        dictionary["defined_Materials"] = defined_Materials
        dictionary["defined_Printing_mediums"] = defined_Printing_mediums
        dictionary["defined_Build_Plates"] = defined_Build_Plates
        dictionary["defined_printing_machines"] = defined_printing_machines
        dictionary["printed_build_list"] = printed_build_list
        dictionary["Printed_Build_AM_Parts_list"] = Printed_Build_AM_Parts_list
        dictionary["Printed_Build_Supports_list"] = Printed_Build_Supports_list
        dictionary["Post_Printing_Methods_list"] = Post_Printing_Methods_list
        dictionary["Testing_Methods_list"] = Testing_Methods_list
        dictionary["sensors_list"] = sensors_list
        dictionary["defined_Manufacturers"] = defined_Manufacturers
        filename = "shared_lists.pkl"
        try:
            with open(filename, 'wb') as f:
                pickle.dump(dictionary, f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save shared lists: {str(e)}")

    # =======================================================================
    def load_shared_lists(self):
        filename = "shared_lists.pkl"
        try:
            with open(filename, 'rb') as f:
                dictionary = pickle.load(f)
            global PBF_AM_Process_Chains_list, supervisors_list, Build_Model_Support_list
            global Build_Model_AM_Part_list, Defined_Build_models, defined_Printing_Process_Instructions
            global Layer_Of_Build_Models_list, Layer_Of_Build_Model_AM_Parts_list
            global Machine_Powder_Feed_Control_Strategies_list, Machine_Powder_Feed_Control_Strategy_PPIs_list
            global Scan_Strategies_list, Start_Heating_PPI_list, Start_Heating_Strategy_list
            global AM_Part_Layer_Pre_Heating_Strategies_list, Layer_Pre_Heating_Strategies_list
            global AM_Part_Layer_Pre_Heating_PPI_list, AM_Part_Layer_Post_Heating_Strategies_list
            global Layer_Post_Heating_Strategies_list, AM_Part_Layer_Post_Heating_PPI_list
            global Layer_Pre_Heating_PPI_list, AM_Part_Layer_Melting_Strategies_list
            global Layer_Melting_Strategies_list, AM_Part_Layer_Melting_PPI_list, Layer_Melting_PPI_list
            global defined_Materials, defined_Printing_mediums, defined_Build_Plates, defined_printing_machines, defined_Manufacturers
            global printed_build_list, Printed_Build_AM_Parts_list, Printed_Build_Supports_list
            global Post_Printing_Methods_list, Testing_Methods_list, sensors_list
            # Assign values from dictionary
            PBF_AM_Process_Chains_list = dictionary.get("PBF_AM_Process_Chains_list", [])
            supervisors_list = dictionary.get("supervisors_list", [])
            Build_Model_Support_list = dictionary.get("Build_Model_Support_list", [])
            Build_Model_AM_Part_list = dictionary.get("Build_Model_AM_Part_list", [])
            Defined_Build_models = dictionary.get("Defined_Build_models", [])
            defined_Printing_Process_Instructions = dictionary.get("defined_Printing_Process_Instructions", [])
            Layer_Of_Build_Models_list = dictionary.get("Layer_Of_Build_Models_list", [])
            Layer_Of_Build_Model_AM_Parts_list = dictionary.get("Layer_Of_Build_Model_AM_Parts_list", [])
            Machine_Powder_Feed_Control_Strategies_list = dictionary.get("Machine_Powder_Feed_Control_Strategies_list",[])
            Machine_Powder_Feed_Control_Strategy_PPIs_list = dictionary.get(
                "Machine_Powder_Feed_Control_Strategy_PPIs_list", [])
            Scan_Strategies_list = dictionary.get("Scan_Strategies_list", [])
            Start_Heating_PPI_list = dictionary.get("Start_Heating_PPI_list", [])
            Start_Heating_Strategy_list = dictionary.get("Start_Heating_Strategy_list", [])
            AM_Part_Layer_Pre_Heating_Strategies_list = dictionary.get("AM_Part_Layer_Pre_Heating_Strategies_list", [])
            Layer_Pre_Heating_Strategies_list = dictionary.get("Layer_Pre_Heating_Strategies_list", [])
            AM_Part_Layer_Pre_Heating_PPI_list = dictionary.get("AM_Part_Layer_Pre_Heating_PPI_list", [])
            AM_Part_Layer_Post_Heating_Strategies_list = dictionary.get("AM_Part_Layer_Post_Heating_Strategies_list",[])
            Layer_Post_Heating_Strategies_list = dictionary.get("Layer_Post_Heating_Strategies_list", [])
            AM_Part_Layer_Post_Heating_PPI_list = dictionary.get("AM_Part_Layer_Post_Heating_PPI_list", [])
            Layer_Pre_Heating_PPI_list = dictionary.get("Layer_Pre_Heating_PPI_list", [])
            AM_Part_Layer_Melting_Strategies_list = dictionary.get("AM_Part_Layer_Melting_Strategies_list", [])
            Layer_Melting_Strategies_list = dictionary.get("Layer_Melting_Strategies_list", [])
            AM_Part_Layer_Melting_PPI_list = dictionary.get("AM_Part_Layer_Melting_PPI_list", [])
            Layer_Melting_PPI_list = dictionary.get("Layer_Melting_PPI_list", [])
            defined_Materials = dictionary.get("defined_Materials", [])
            defined_Printing_mediums = dictionary.get("defined_Printing_mediums", [])
            defined_Manufacturers = dictionary.get("defined_Manufacturers", [])
            defined_Build_Plates = dictionary.get("defined_Build_Plates", [])
            defined_printing_machines = dictionary.get("defined_printing_machines", [])
            printed_build_list = dictionary.get("printed_build_list", [])
            Printed_Build_AM_Parts_list = dictionary.get("Printed_Build_AM_Parts_list", [])
            Printed_Build_Supports_list = dictionary.get("Printed_Build_Supports_list", [])
            Post_Printing_Methods_list = dictionary.get("Post_Printing_Methods_list", [])
            Testing_Methods_list = dictionary.get("Testing_Methods_list", [])
            sensors_list = dictionary.get("sensors_list", [])
            msg = QMessageBox(self)
            msg.setWindowTitle("Success")
            msg.setText("Info: Shared lists loaded successfully.")
            msg.show()
            QTimer.singleShot(1500, msg.close)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load shared lists: {str(e)}")
    # =======================================================================
    def load_program(self):
        global PBF_AM_Process_Chains_list, supervisors_list, Build_Model_Support_list
        global Build_Model_AM_Part_list, Defined_Build_models, defined_Printing_Process_Instructions
        global Layer_Of_Build_Models_list, Layer_Of_Build_Model_AM_Parts_list
        global Machine_Powder_Feed_Control_Strategies_list, Machine_Powder_Feed_Control_Strategy_PPIs_list
        global Scan_Strategies_list, Start_Heating_PPI_list, Start_Heating_Strategy_list
        global AM_Part_Layer_Pre_Heating_Strategies_list, Layer_Pre_Heating_Strategies_list
        global AM_Part_Layer_Pre_Heating_PPI_list, AM_Part_Layer_Post_Heating_Strategies_list
        global Layer_Post_Heating_Strategies_list, AM_Part_Layer_Post_Heating_PPI_list
        global Layer_Pre_Heating_PPI_list, AM_Part_Layer_Melting_Strategies_list
        global Layer_Melting_Strategies_list, AM_Part_Layer_Melting_PPI_list, Layer_Melting_PPI_list
        global defined_Materials, defined_Printing_mediums, defined_Build_Plates, defined_printing_machines
        global printed_build_list, Printed_Build_AM_Parts_list, Printed_Build_Supports_list
        global Post_Printing_Methods_list, Testing_Methods_list
        self.load_shared_lists()
        # ================================================================
        if supervisors_list:
            self.ui.defined_supervisors_list.clear()
            for s in supervisors_list:
                self.ui.selectSupervisor.addItem(s.supervisor_name)
                self.ui.defined_supervisors_list.addItem(s.supervisor_name)
        # ================================================================
        if Defined_Build_models:
            for build in Defined_Build_models:
                self.ui.existing_digital_build_model_listwidget.addItem(build.build_model_name)

        # ================================================================
        if Build_Model_Support_list:
            for support in Build_Model_Support_list:
                self.ui.supports_list.addItem(support.support_name)
                self.ui.choose_support.addItem(support.support_name)
        # ================================================================
        if Build_Model_AM_Part_list:
            for part in Build_Model_AM_Part_list:
                self.ui.parts_list.addItem(part.am_part_name)
                self.ui.choose_part.addItem(part.am_part_name)
        # ================================================================
        if defined_Printing_Process_Instructions:
            for i in defined_Printing_Process_Instructions:
                self.ui.existing_ppi_listwidget.addItem(i.ppi_name)
                self.ui.input_printing_ppi_name.addItem(i.ppi_name)
                self.ui.load_exist_printing_instructions_comboBox.addItem(i.ppi_name)
        # ================================================================
        if Layer_Of_Build_Models_list:
            for l in Layer_Of_Build_Models_list:
                self.ui.load_layer_comboBox_2.addItem(l.Layer_Of_Build_Model_name)
                self.ui.load_layer_comboBox.addItem(l.Layer_Of_Build_Model_name)
                self.ui.list_existing_model_layers.addItem(l.Layer_Of_Build_Model_name)
        # ================================================================
        if Layer_Of_Build_Model_AM_Parts_list:
            for a in Layer_Of_Build_Model_AM_Parts_list:
                self.ui.layer_part_comboBox.addItem(a.Layer_Of_Build_Model_AM_Part_name)
                self.ui.list_existing_part_model_layers.addItem(a.Layer_Of_Build_Model_AM_Part_name)
        # ================================================================
        if Machine_Powder_Feed_Control_Strategy_PPIs_list:
            for mp in Machine_Powder_Feed_Control_Strategy_PPIs_list:
                self.ui.defined_machine_control_ppi_listwidget.addItem(mp.Machine_powder_s_PPI_name)
                self.ui.load_machine_feed_instructions_comboBox.addItem(mp.Machine_powder_s_PPI_name)
        # ================================================================
        if Machine_Powder_Feed_Control_Strategies_list:
            for m in Machine_Powder_Feed_Control_Strategies_list:
                self.ui.load_machine_feed_strategy_comboBox.addItem(m.Machine_powder_s_name)
                self.ui.defined_machine_powder_control_strategies_listwidget.addItem(m.Machine_powder_s_name)
        # ================================================================
        if Scan_Strategies_list:
            for s in Scan_Strategies_list:
                self.ui.defined_scan_strategy_listWidget.addItem(s.scan_strategy_name)
                self.ui.start_heating_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.layer_pre_heating_strategy_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.am_part_layer_pre_heating_strategy_scan_startegy.addItem(s.scan_strategy_name)
                self.ui.layer_post_heating_strategy_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.am_part_layer_post_heating_strategy_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.layer_melting_strategy_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.am_part_layer_melting_strategy_scan_strategy.addItem(s.scan_strategy_name)
        # ================================================================
        if Start_Heating_PPI_list:
            for s in Start_Heating_PPI_list:
                self.ui.defined_start_heat_ppi_listWidget.addItem(s.start_heat_ppi_name)
                self.ui.load_start_heat_ppi_comboBox.addItem(s.start_heat_ppi_name)
        # ================================================================
        if Start_Heating_Strategy_list:
            for s in Start_Heating_Strategy_list:
                self.ui.defined_start_heating_listWidget.addItem(s.start_heat_name)
                self.ui.load_start_heat_startegy_comboBox.addItem(s.start_heat_name)
                self.ui.strat_heating_pp_correspond_strategy.addItem(s.start_heat_name)
        # ================================================================
        if AM_Part_Layer_Pre_Heating_Strategies_list:
            for a in AM_Part_Layer_Pre_Heating_Strategies_list:
                self.ui.composed_of_am_part_pre_startegies_combobox.addItem(a.AM_part_pre_heat_strategy_name)
                self.ui.correspond_am_part_layer_pre_heating.addItem(a.AM_part_pre_heat_strategy_name)
                self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.addItem(
                    a.AM_part_pre_heat_strategy_name)
        # ================================================================
        if Layer_Pre_Heating_Strategies_list:
            for l in Layer_Pre_Heating_Strategies_list:
                self.ui.correspond_to_layer_pre_heating_combobox.addItem(l.pre_heat_strategy_name)
                self.ui.load_an_existing_layer_pr_heating.addItem(l.pre_heat_strategy_name)
                self.ui.list_defined_layer_pre_heating_strategy_listwidget.addItem(l.pre_heat_strategy_name)
        # ================================================================
        if AM_Part_Layer_Pre_Heating_PPI_list:
            for am in AM_Part_Layer_Pre_Heating_PPI_list:
                self.ui.composed_of_am_part_pre_heating_ppi_combobox.addItem(am.AM_part_pre_heat_ppi_name)
                self.ui.list_defined_AM_part_layer_pre_heating_strategy_ppi_listwidget.addItem(
                    am.AM_part_pre_heat_ppi_name)
        # ================================================================
        if Layer_Pre_Heating_PPI_list:
            for lp in Layer_Pre_Heating_PPI_list:
                self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget_2.addItem(lp.pre_heat_ppi_name)
                self.ui.load_an_existing_layer_pr_heating_ppi_combobox.addItem(lp.pre_heat_ppi_name)
        # ================================================================
        if AM_Part_Layer_Post_Heating_Strategies_list:
            for a in AM_Part_Layer_Post_Heating_Strategies_list:
                self.ui.layer_post_heating_strategy_combobox.addItem(a.AM_part_post_heat_strategy_name)
                self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.addItem(
                    a.AM_part_post_heat_strategy_name)
                self.ui.list_defined_A_part_layer_post_heating_strategy_listwidget.addItem(
                    a.AM_part_post_heat_strategy_name)
        # ================================================================
        if Layer_Post_Heating_Strategies_list:
            for l in Layer_Post_Heating_Strategies_list:
                self.ui.list_defined_layer_post_heating_strategy_listwidget.addItem(l.post_heat_strategy_name)
                self.ui.correspond_layer_post_heating_combobox.addItem(l.post_heat_strategy_name)
                self.ui.load_existing_post_heating_combobox.addItem(l.post_heat_strategy_name)
        # ================================================================
        if AM_Part_Layer_Post_Heating_PPI_list:
            for am in AM_Part_Layer_Post_Heating_PPI_list:
                self.ui.composed_of_am_part_post_heating_ppi_combobox.addItem(am.AM_part_post_heat_ppi_name)
                self.ui.list_defined_AM_part_layer_post_heating_strategy_ppi_listwidget.addItem(
                    am.AM_part_post_heat_ppi_name)
        # ================================================================
        if Layer_Post_Heating_PPI_list:
            for lp in Layer_Post_Heating_PPI_list:
                self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget_2.addItem(lp.post_heat_ppi_name)
                self.ui.load_an_existing_layer_post_heating_ppi_combobox.addItem(lp.post_heat_ppi_name)
        # ================================================================
        if AM_Part_Layer_Melting_Strategies_list:
            for a in AM_Part_Layer_Melting_Strategies_list:
                self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.addItem(a.AM_part_melting_strategy_name)
                self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.addItem(
                    a.AM_part_melting_strategy_name)
                self.ui.list_defined_A_part_layer_melting_strategy_listwidget.addItem(a.AM_part_melting_strategy_name)
        # ================================================================
        if Layer_Melting_Strategies_list:
            for l in Layer_Melting_Strategies_list:
                self.ui.list_defined_A_part_layer_melting_strategy_listwidget_2.addItem(l.melting_strategy_name)
                self.ui.correspond_layer_melting_strategy_combobox.addItem(l.melting_strategy_name)
                self.ui.load_existing_layer_melting_startegy_combobox.addItem(l.melting_strategy_name)
        # ================================================================
        if AM_Part_Layer_Melting_PPI_list:
            for am in AM_Part_Layer_Melting_PPI_list:
                self.ui.composed_of_am_part_melting_ppi_combobox.addItem(am.AM_part_melting_ppi_name)
                self.ui.list_defined_AM_part_layer_melting_strategy_ppi_listwidget.addItem(am.AM_part_melting_ppi_name)
        # ================================================================
        if Layer_Melting_PPI_list:
            for lp in Layer_Melting_PPI_list:
                self.ui.composed_of_am_part_layer_melting_ppi_listWidget_2.addItem(lp.melting_ppi_name)
                self.ui.load_an_existing_layer_melting_ppi_combobox.addItem(lp.melting_ppi_name)
        # ================================================================
        if defined_Materials:
            for m in defined_Materials:
                self.ui.defined_materials_listWidget.addItem(m.material_name)
                self.ui.build_plate_material_comboBox.addItem(m.material_name)
                self.ui.printing_medium_material_comboBox.addItem(m.material_name)
        # ================================================================
        if defined_Manufacturers:
            for m in defined_Manufacturers:
                self.ui.defined_manufactures_listWidget.addItem(m.manufacturer_name)
                self.ui.printing_medium_manufacturer_comboBox.addItem(m.manufacturer_name)
                self.ui.build_plate_manufacturer_comboBox.addItem(m.manufacturer_name)
        # ================================================================
        if defined_Printing_mediums:
            for m in defined_Printing_mediums:
                self.ui.defined_printing_medium_listWidget.addItem(m.printing_medium_name)
                self.ui.printing_process_printing_medium.addItem(m.printing_medium_name)
        # ================================================================
        if defined_Build_Plates:
            for b in defined_Build_Plates:
                self.ui.defined_build_plate_listWidget.addItem(b.build_plate_name)
                self.ui.printing_process_buildplate.addItem(b.build_plate_name)
        # ================================================================
        if defined_printing_machines:
            for p in defined_printing_machines:
                self.ui.printing_process_printing_machine.addItem(p.printing_machine_name)
                self.ui.defined_printing_machines_listWidget.addItem(p.printing_machine_name)
        # ================================================================
        if Printed_Build_AM_Parts_list:
            for s in Printed_Build_AM_Parts_list:
                self.ui.defined_printed_build_AM_part_listWidget.addItem(s.Printed_Build_AM_Part_name)
                self.ui.printed_build_PB_AM_part_comboBox.addItem(s.Printed_Build_AM_Part_name)
        # ================================================================
        if Printed_Build_Supports_list:
            for s in Printed_Build_Supports_list:
                self.ui.defined_printed_build_support_listWidget.addItem(s.Printed_Build_Support_name)
                self.ui.printed_build_PB_AM_part_support_comboBox.addItem(s.Printed_Build_Support_name)
        # ================================================================
        if printed_build_list:
            for i in printed_build_list:
                self.ui.defined_Printed_Builds_listWidget.addItem(i.Printed_Build_name)
                self.ui.printing_process_output_printe_build.addItem(i.Printed_Build_name)
        # ================================================================
        if Post_Printing_Methods_list:
            for p in Post_Printing_Methods_list:
                self.ui.defined_PostPrinting_methods_listWidget.addItem(p.post_printing_method_name)
                self.ui.Post_Printing_method_comboBox.addItem(p.post_printing_method_name)
        # ================================================================
        if Testing_Methods_list:
            for i in Testing_Methods_list:
                self.ui.testing_method_name_comboBox.addItem(i.TestingMethod_name)
                self.ui.defined_testing_methods_listwidget.addItem(i.TestingMethod_name)

    # =======================================================================
    def open_project_func(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "PICKLE files (*.pkl)")
        if filename:
            self.current_project_path = filename
            try:
                with open(filename, 'rb') as f:
                    loaded_data = pickle.load(f)
                # Restore variables from the dictionary
                global PBF_AM_Process_Chain, Build_Model_Design_Process_process, build_model_parts
                global build_model_support_for_part, Build_model, Slicing_process
                global Printing_Process_Instructions_output, Layer_Of_Build_Models_Layer_decomposition
                global Layer_Of_Build_Model_AM_Parts_Layer_decomposition, machine_powder_strategy
                global machine_powder_strategy_PPI, Beam_control_slicing_strategy, start_heating_PPIs_in_project
                global start_heating_strategies_in_project, Layer_Pre_Heating_Strategies_list_used_in_project
                global Layer_Post_Heating_Strategies_list_used_in_project, Layer_Pre_Heating_PPI_list_used_in_project
                global Layer_Post_Heating_PPI_list_used_in_project, Layer_Post_Heating_PPI_list
                global Layer_Melting_Strategies_list_used_in_project, Layer_Melting_PPI_list_used_in_project
                global Printing_Process, printed_build, Monitoring_Process, Post_printing_Proces
                global Testing_Process, PBF_AM_Process_Chains_list, supervisors_list, Build_Model_Support_list
                global Build_Model_AM_Part_list, Defined_Build_models, defined_Printing_Process_Instructions
                global Layer_Of_Build_Models_list, Layer_Of_Build_Model_AM_Parts_list
                global Machine_Powder_Feed_Control_Strategies_list, Machine_Powder_Feed_Control_Strategy_PPIs_list
                global Scan_Strategies_list, Start_Heating_PPI_list, Start_Heating_Strategy_list
                global AM_Part_Layer_Pre_Heating_Strategies_list, Layer_Pre_Heating_Strategies_list
                global AM_Part_Layer_Pre_Heating_PPI_list, AM_Part_Layer_Post_Heating_Strategies_list
                global Layer_Post_Heating_Strategies_list, AM_Part_Layer_Post_Heating_PPI_list
                global Layer_Pre_Heating_PPI_list, AM_Part_Layer_Melting_Strategies_list
                global Layer_Melting_Strategies_list, AM_Part_Layer_Melting_PPI_list, Layer_Melting_PPI_list
                global defined_Materials, defined_Printing_mediums, defined_Build_Plates, defined_printing_machines
                global printed_build_list, Printed_Build_AM_Parts_list, Printed_Build_Supports_list
                global Post_Printing_Methods_list, Testing_Methods_list
                # Assign values from loaded_data
                for key, value in loaded_data.items():
                    globals()[key] = value
                self.clear_all_inputs()
                self.load_program()
                # PBF_AM_Process_Chain============================================
                self.ui.ProjectName.setPlainText(PBF_AM_Process_Chain.project_name)
                if PBF_AM_Process_Chain.project_type == 'EB-PBF':
                    self.ui.ebpbf.setChecked(True)
                elif PBF_AM_Process_Chain.project_type == 'LB-PBF':
                    self.ui.lbpbf.setChecked(True)
                start_dt = QDateTime.fromString(PBF_AM_Process_Chain.project_start_date_value, "yyyy-MM-dd HH:mm:ss")
                end_dt = QDateTime.fromString(PBF_AM_Process_Chain.project_end_date_value, "yyyy-MM-dd HH:mm:ss")
                self.ui.project_start_date.setDateTime(start_dt)
                self.ui.project_end_date.setDateTime(end_dt)
                if PBF_AM_Process_Chain.project_status == 'Successful':
                    self.ui.project_success.setChecked(True)
                elif PBF_AM_Process_Chain.project_status == 'Failed':
                    self.ui.project_fail.setChecked(True)
                self.ui.define_project_comment.setPlainText(PBF_AM_Process_Chain.project_comment)
                if PBF_AM_Process_Chain.project_selected_supervisors:
                    for i in PBF_AM_Process_Chain.project_selected_supervisors:
                        self.ui.supervisor_project_list.addItem(i)
                # ================================================================
                self.ui.ModelDesign_name.setPlainText(Build_Model_Design_Process_process.ModelDesign_name)
                start_dt = QDateTime.fromString(Build_Model_Design_Process_process.ModelDesign_start_date,
                                                "yyyy-MM-dd HH:mm:ss")
                end_dt = QDateTime.fromString(Build_Model_Design_Process_process.ModelDesign_end_date,
                                              "yyyy-MM-dd HH:mm:ss")
                self.ui.ModelDesign_start.setDateTime(start_dt)
                self.ui.ModelDesig_end.setDateTime(end_dt)
                if Build_Model_Design_Process_process.ModelDesign_completion_status == 'finished':
                    self.ui.project_success_2.setChecked(True)
                elif Build_Model_Design_Process_process.ModelDesign_completion_status == 'unfinished':
                    self.ui.project_fail_2.setChecked(True)
                self.ui.ModelDesign_comment.setPlainText(Build_Model_Design_Process_process.ModelDesign_comment)
                # ================================================================
                self.ui.slicing_process_name.setPlainText(Slicing_process.SlicingProcess_name)
                start_dt = QDateTime.fromString(Slicing_process.SlicingProcess_start_date, "yyyy-MM-dd HH:mm:ss")
                end_dt = QDateTime.fromString(Slicing_process.SlicingProcess_end_date, "yyyy-MM-dd HH:mm:ss")
                self.ui.slicing_start_date.setDateTime(start_dt)
                self.ui.slicing_end_date.setDateTime(end_dt)
                if Slicing_process.SlicingProcess_completion_status == 'finished':
                    self.ui.slicing_finish.setChecked(True)
                elif Slicing_process.SlicingProcess_completion_status == 'unfinished':
                    self.ui.slicing_unfinished.setChecked(True)
                self.ui.slicing_software_name.setPlainText(Slicing_process.SlicingProcess_software)
                self.ui.slicing_process_comment.setPlainText(Slicing_process.SlicingProcess_comment)
                # ================================================================
                if Printing_Process_Instructions_output:
                    self.ui.printing_process_instructions_name.setPlainText(
                        Printing_Process_Instructions_output.ppi_name)
                    self.ui.printing_process_instructions_file.setPlainText(
                        Printing_Process_Instructions_output.ppi_file)
                    self.ui.printing_process_instructions_file_format.setPlainText(
                        Printing_Process_Instructions_output.ppi_file_format)
                    self.ui.printing_process_instructions_layer_thicknesses.setPlainText(
                        Printing_Process_Instructions_output.ppi_list_layer_thicknesses)
                    self.ui.printing_process_instructions_comment.setPlainText(
                        Printing_Process_Instructions_output.ppi_comment)
                    self.ui.selected_ppi_slicing_process.addItem(Printing_Process_Instructions_output.ppi_name)
                # ================================================================
                if Layer_Of_Build_Models_Layer_decomposition:
                    for l in Layer_Of_Build_Models_Layer_decomposition:
                        self.ui.list_output_layer_decomposition.addItem(l)
                        self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox.addItem(l)
                        self.ui.correspond_layer_build_model_combobox.addItem(l)
                        self.ui.correspond_layer_build_model_combobox_2.addItem(l)
                # ================================================================
                if Build_model:
                    self.ui.selected_digital_build_model.addItem(Build_model.build_model_name)
                    if Build_model.build_model_parts_supports:
                        for i in Build_model.build_model_parts_supports:
                            self.ui.part_support_in_model_list.addItem(i)
                # ================================================================
                if Layer_Of_Build_Model_AM_Parts_Layer_decomposition:
                    for (l, part) in Layer_Of_Build_Model_AM_Parts_Layer_decomposition:
                        temp = 'Build Layer :' + l + '   Part Layer: ' + part
                        self.ui.list_output_part_layer_decomposition.addItem(temp)
                # ================================================================
                if machine_powder_strategy_PPI:
                    self.ui.selected_machine_control_ppi.addItem(machine_powder_strategy_PPI.Machine_powder_s_PPI_name)
                # ================================================================
                if machine_powder_strategy:
                    self.ui.selected_machine_control_strategy.addItem(machine_powder_strategy.Machine_powder_s_name)
                # ================================================================
                if Beam_control_slicing_strategy:
                    self.ui.beam_control_strategy_name.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_name)
                    self.ui.beam_control_strategy_file.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_file)
                    self.ui.beam_control_strategy_file_format.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_file_format)
                    self.ui.beam_control_strategy_name_2.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_name)
                    self.ui.beam_control_strategy_name_3.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_name)
                    self.ui.beam_control_strategy_name_4.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_name)
                    self.ui.beam_control_strategy_file_2.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_file)
                    self.ui.beam_control_strategy_file_3.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_file)
                    self.ui.beam_control_strategy_file_4.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_file)
                    self.ui.beam_control_strategy_file_format_2.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_file_format)
                    self.ui.beam_control_strategy_file_format_3.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_file_format)
                    self.ui.beam_control_strategy_file_format_4.setPlainText(
                        Beam_control_slicing_strategy.beam_control_slic_strategy_file_format)
                # ================================================================
                if start_heating_PPIs_in_project:
                    for start_heating_ppi in start_heating_PPIs_in_project:
                        self.ui.selected_start_heat_ppi_listWidget.addItem(start_heating_ppi.start_heat_ppi_name)
                # ================================================================
                if start_heating_strategies_in_project:
                    for start_heating_strategy in start_heating_strategies_in_project:
                        self.ui.selected_start_heating_listWidget.addItem(start_heating_strategy.start_heat_name)
                # ================================================================
                if Layer_Pre_Heating_Strategies_list_used_in_project:
                    for l in Layer_Pre_Heating_Strategies_list_used_in_project:
                        self.ui.list_layer_pre_heating_in_beam_control_listWidget.addItem(l.pre_heat_strategy_name)
                # ================================================================
                if Layer_Pre_Heating_PPI_list_used_in_project:
                    for lp in Layer_Pre_Heating_PPI_list_used_in_project:
                        self.ui.list_pre_heating_ppi_in_beam_control.addItem(lp.pre_heat_ppi_name)
                # ================================================================
                if Layer_Post_Heating_Strategies_list_used_in_project:
                    for l in Layer_Post_Heating_Strategies_list_used_in_project:
                        self.ui.list_layer_post_heating_in_beam_control_listWidget.addItem(l.post_heat_strategy_name)
                # ================================================================
                if Layer_Post_Heating_PPI_list_used_in_project:
                    for lp in Layer_Post_Heating_PPI_list_used_in_project:
                        self.ui.layer_post_heating_ppi_used_beam_control_listwidget.addItem(lp.post_heat_ppi_name)
                # ================================================================
                if Layer_Melting_Strategies_list_used_in_project:
                    for l in Layer_Melting_Strategies_list_used_in_project:
                        self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.addItem(
                            l.melting_strategy_name)
                # ================================================================
                if Layer_Melting_PPI_list_used_in_project:
                    for lp in Layer_Melting_PPI_list_used_in_project:
                        self.ui.layer_melting_ppi_used_beam_control_listwidget.addItem(lp.melting_ppi_name)
                # ================================================================
                self.ui.printing_process_name.setPlainText(Printing_Process.printing_process_name)
                start_dt = QDateTime.fromString(Printing_Process.printing_process_start_date, "yyyy-MM-dd HH:mm:ss")
                end_dt = QDateTime.fromString(Printing_Process.printing_process_end_date, "yyyy-MM-dd HH:mm:ss")
                self.ui.printing_start_date.setDateTime(start_dt)
                self.ui.printing_end_date.setDateTime(end_dt)
                if Printing_Process.printing_process_status == 'finished':
                    self.ui.printing_finish.setChecked(True)
                elif Printing_Process.printing_process_status == 'unfinished':
                    self.ui.printing_unfinished.setChecked(True)
                self.ui.printing_comment.setPlainText(Printing_Process.printing_process_comment)
                if Printing_Process.printing_process_instructions:
                    for i in Printing_Process.printing_process_instructions:
                        self.ui.set_as_input_printing_process_listWidget.addItem(i)
                index = self.ui.printing_process_buildplate.findText(Printing_Process.printing_process_build_plate)
                if index != -1:
                    self.ui.printing_process_buildplate.setCurrentIndex(index)
                index = self.ui.printing_process_printing_medium.findText(
                    Printing_Process.printing_process_printing_medium)
                if index != -1:
                    self.ui.printing_process_printing_medium.setCurrentIndex(index)

                index = self.ui.printing_process_printing_machine.findText(
                    Printing_Process.printing_process_printing_machine)
                if index != -1:
                    self.ui.printing_process_printing_machine.setCurrentIndex(index)

                try:
                    temp = Printing_Process.printing_process_output
                    if temp:

                        index = self.ui.printing_process_output_printe_build.findText(temp.Printed_Build_name)
                        if index != -1:
                            self.ui.printing_process_output_printe_build.setCurrentIndex(index)
                except:pass
                # ================================================================
                self.ui.monitoring_process_name.setPlainText(Monitoring_Process.monitoring_process_name)
                start_dt = QDateTime.fromString(Monitoring_Process.monitoring_process_start_date, "yyyy-MM-dd HH:mm:ss")
                end_dt = QDateTime.fromString(Monitoring_Process.monitoring_process_end_date, "yyyy-MM-dd HH:mm:ss")
                self.ui.monitoring_process_start_date.setDateTime(start_dt)
                self.ui.monitoring_process_end_date.setDateTime(end_dt)
                if Monitoring_Process.monitoring_process_status == 'finished':
                    self.ui.monitoring_process_finished.setChecked(True)
                elif Monitoring_Process.monitoring_process_status == 'unfinished':
                    self.ui.monitoring_process_unfinished.setChecked(True)
                self.ui.monitoring_process_comment.setPlainText(Monitoring_Process.monitoring_process_comment)
                self.ui.monitoring_process_output_file.setPlainText(Monitoring_Process.monitoring_process_output_file)
                # ================================================================
                self.ui.PostPrinting_Process_name.setPlainText(Post_printing_Proces.post_printing_process_name)
                start_dt = QDateTime.fromString(Post_printing_Proces.post_printing_process_start_date,
                                                "yyyy-MM-dd HH:mm:ss")
                end_dt = QDateTime.fromString(Post_printing_Proces.post_printing_process_end_date,
                                              "yyyy-MM-dd HH:mm:ss")
                self.ui.PostPrinting_Process_end_date.setDateTime(start_dt)
                self.ui.PostPrinting_Process_end_date.setDateTime(end_dt)
                if Post_printing_Proces.post_printing_process_status == 'finished':
                    self.ui.PostPrinting_Process_finished.setChecked(True)
                elif Post_printing_Proces.post_printing_process_status == 'unfinished':
                    self.ui.PostPrinting_Process_unfinished.setChecked(True)
                self.ui.PostPrinting_Process_comment.setPlainText(Post_printing_Proces.post_printing_process_comment)
                if Post_printing_Proces.post_printing_process_used_methods:
                    for i in Post_printing_Proces.post_printing_process_used_methods:
                        self.ui.used_POstPrinting_methods_listWidget.addItem(i)
                # ================================================================
                if Testing_Methods_list:
                    for i in Testing_Methods_list:
                        self.ui.testing_method_name_comboBox.addItem(i.TestingMethod_name)
                        self.ui.defined_testing_methods_listwidget.addItem(i.TestingMethod_name)
                # ================================================================
                self.ui.Testing_Process_name.setPlainText(Testing_Process.TestingProcess_name)
                start_dt = QDateTime.fromString(Testing_Process.TestingProcess_start_date, "yyyy-MM-dd HH:mm:ss")
                end_dt = QDateTime.fromString(Testing_Process.TestingProcess_end_date, "yyyy-MM-dd HH:mm:ss")
                self.ui.Testing_Process_start_date.setDateTime(start_dt)
                self.ui.Testing_Process_end_date.setDateTime(end_dt)
                if Testing_Process.TestingProcess_status == 'finished':
                    self.ui.Testing_Process_finished.setChecked(True)
                elif Testing_Process.TestingProcess_status == 'unfinished':
                    self.ui.Testing_Process_unfinished.setChecked(True)
                self.ui.Testing_Process_comment.setPlainText(Testing_Process.TestingProcess_comment)
                if Testing_Process.TestingProcess_applied_methods_results:
                    for i in Testing_Process.TestingProcess_applied_methods_results:
                        self.ui.Testin_process_applied_methods_list.addItem(i)
                # ================================================================
                QMessageBox.information(self, "Success", f"Project loaded successfully from '{filename}'")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load project: {str(e)}")
    # =======================================================================
    def open_new_project(self):
        self.clear_all_inputs()
        self.load_program()
    # =======================================================================
    def clear_all_inputs(self):
        for widget in self.findChildren(
                (QPlainTextEdit, QCheckBox, QComboBox, QListWidget, QRadioButton, QDateTimeEdit)):
            if isinstance(widget, QPlainTextEdit):
                widget.clear()
            elif isinstance(widget, QCheckBox) or isinstance(widget, QRadioButton):
                widget.setChecked(False)
            elif isinstance(widget, QComboBox):
                for i in range(widget.count() - 1, 0, -1):
                    widget.removeItem(i)
                widget.setCurrentIndex(0)
            elif isinstance(widget, QListWidget):
                widget.clear()
            elif isinstance(widget, QDateTimeEdit):
                widget.setDateTime(QDateTime.fromString("2025-01-01T00:00:00", "yyyy-MM-ddThh:mm:ss"))
    # =======================================================================
    def save_project_as_rdf(self):
        # ****************************************************************************************************
        # Define namespaces
        AMPCORE = Namespace("http://www.semanticweb.org/minab62/ontologies/2025/5/PBF-AMP-Onto:AMPCore#")
        CORE = Namespace("http://www.semanticweb.org/minab62/ontologies/2025/5/PBF-AMP-Onto:Core#")
        EB = Namespace("http://www.semanticweb.org/minab62/ontologies/2025/5/PBF-AMP-Onto:EB#")
        EX = Namespace("http://www.semanticweb.org/minab62/ontologies/2025/5/PBF-AMP-Onto:EB#")
        prov = Namespace("http://www.w3.org/ns/prov#")
        # ****************************************************************************************************
        # General mapping for multiple classes
        class_mappings = {
            "Material_class": {"rdf_type": EB.Material,
                               "attributes": {
                                   'material_name': RDFS.label,
                                   'material_melting_point': EB.hasMeltingPoint,
                                   'material_oxidation_resistance': EB.hasOxidationResistance,
                                   'material_heat_capacity': EB.hasSpecificHeatCapacity,
                                   'material_formula': EB.hasFormula,
                                   'material_density': EB.hasDensity,
                                   'material_electrical_resistivity': EB.hasElectricalResistivity,
                                   'material_eb_absorption_rate': EB.hasElectronBeamAbsorptionRate,
                                   'material_thermal_conductivity': EB.hasThermalConductivity,
                                   'material_electrical_conductivity': EB.hasElectricalConductivity,
                                   'material_thermal_diffusivity': EB.hasThermalDiffusivity,
                                   'material_comment': RDFS.comment}},
            "Supervisor": {"rdf_type": prov.Agent,
                           "attributes": {"supervisor_name": RDFS.label,
                                          "supervisor_comment": RDFS.comment}},
            "PBF_AM_Process_Chain_class": {"rdf_type": CORE.PBFAMProcessChain,
                                           "attributes": {
                                               "project_name": RDFS.label,
                                               "project_start_date_value": AMPCORE.hasStartDateTime,
                                               "project_end_date_value": AMPCORE.hasEndDateTime,
                                               "project_status": AMPCORE.hasResultStatus,
                                               "project_comment": RDFS.comment,
                                               "project_selected_supervisors": "nested" }},
            "Build_Model_AM_Part_class": {"rdf_type": CORE.PBFBuildModelAMPart,
                                          "attributes": {
                                              "am_part_name": RDFS.label,
                                              "am_part_dimension": CORE.hasDimensions,
                                              "am_part_file_path": CORE.isRepresentedBy,
                                              "am_part_file_format": CORE.hasFileFormat,
                                              "am_part_comment": RDFS.comment}},
            "Manufacturer_class": {"rdf_type": EB.Manufacturer,
                                   "attributes": {
                                       "manufacturer_name": RDFS.label,
                                       "manufacturer_address": EB.hasAddress,
                                       "manufacturer_comment": RDFS.comment}},
            "Printing_Medium_class": {"rdf_type": CORE.PBFPowder,
                                      "attributes": {"printing_medium_name": RDFS.label,
                                                     "printing_medium_comment": RDFS.comment,
                                                     "printing_medium_status": CORE.hasStatus,
                                                     "printing_medium_material": EB.isManufacturedFrom,
                                                     "printing_medium_particle_size": CORE.hasParticleSizeDistribution,
                                                     "printing_medium_powder_morphology": CORE.hasPowderMorphology,
                                                     "printing_medium_manufacturer": EB.isManufacturedBy}},
            "Printed_Build_class": {"rdf_type": EB["EB-PBFPrintedBuild"],
                                    "attributes": {"Printed_Build_name": RDFS.label,
                                                   "Printed_Build_comment": RDFS.comment,
                                                   "Printed_Build_AM_Parts_and_supports": "nested"}},
            "Printed_Build_AM_Part_class": {"rdf_type": CORE.PBFPrintedBuildAMPart,
                                            "attributes": {"Printed_Build_AM_Part_name": RDFS.label,
                                                           "Printed_Build_AM_Part_comment": RDFS.comment}},
            "Printed_Build_Support_class": {"rdf_type": CORE.PBFPrintedBuildSupport,
                                            "attributes": {"Printed_Build_Support_name": RDFS.label,
                                                           "Printed_Build_Support_comment": RDFS.comment}},
            "Printing_Machine_class": {"rdf_type": CORE.PBFPrintingMachine,
                                       "attributes": {
                                           "printing_machine_name": RDFS.label,
                                           "printing_machine_brand": EX.hasBrand,
                                           "printing_machine_comment": RDFS.comment,
                                           "printing_machine_sensor_info": "nested"}},
            "Sensor_class": {"rdf_type": CORE.PBFPrintingMachineSensor,
                             "attributes": {
                                 "sensor_name": RDFS.label,
                                 "sensor_type": CORE.hasSensorType,
                                 "recorded_data_path": CORE.hasRecordedData}},
            "Build_Plate_class": {"rdf_type": EB["EB-PBFBuildPlate"],
                                  "attributes": {"build_plate_name": RDFS.label,
                                                 "build_plate_comment": RDFS.comment,
                                                 "build_plate_size": EB.hasSize,
                                                 "build_plate_thickness": EB.hasThickness,
                                                 "build_plate_surface_texture": EB.hasSurfaceTexture,
                                                 "build_plate_shape": EB.hasShape,
                                                 "build_plate_manufacturer": EB.isManufacturedBy,
                                                 "build_plate_material": EB.isManufacturedFrom}},
            "Scan_Strategy_class": {"rdf_type": EB["EB-PBFScanStrategy"],
                                    "attributes": {"scan_strategy_name": RDFS.label,
                                                   "scan_strategy_comment": RDFS.comment,
                                                   "scan_strategy_beam_spot_size": EB.hasBeamSpotSize,
                                                   "scan_strategy_dwell_time": EB.hasDwellTime,
                                                   "scan_strategy_point_distance": EB.hasPointDistance,
                                                   "scan_strategy_strategy_name": EB.hasStrategyName,
                                                   "scan_strategy_scan_speed": EB.hasScanSpeed,
                                                   "scan_strategy_beam_power": EB.hasBeamPower}},
            "Testing_Method_class": {"rdf_type": CORE.PBFTestingMethod,
                                     "attributes": {"TestingMethod_name": RDFS.label,
                                                    "TestingMethod_type": EX.hasTestingMethodType,
                                                    "TestingMethod_comment": RDFS.comment}},
            "Build_Model_Support_class": {"rdf_type": CORE.PBFBuildModelSupport,
                                          "attributes": {
                                              "support_name": RDFS.label,
                                              "support_dimensions": CORE.hasDimensions,
                                              "support_file_path": CORE.isRepresentedBy,
                                              "support_file_format": CORE.hasFileFormat,
                                              "support_comment": RDFS.comment}},
            "output_Build_Model_Design_Process_class": {"rdf_type": CORE.PBFBuildModel,
                                                        "attributes": {
                                                            "build_model_name": RDFS.label,
                                                            "build_model_dimension": CORE.hasDimensions,
                                                            "build_model_file_path": CORE.isRepresentedBy,
                                                            "build_model_file_format": CORE.hasFileFormat,
                                                            "build_model_comment": RDFS.comment,
                                                            "build_model_parts_supports": EX.hasBuildModelPartSupport}},
            "Build_Model_Design_Process_class": {"rdf_type": EB["EB-PBFBuildModelDesignProcess"],
                                                 "attributes": {
                                                     "ModelDesign_name": RDFS.label,
                                                     "ModelDesign_start_date": AMPCORE.hasStartDateTime,
                                                     "ModelDesign_end_date": AMPCORE.hasEndDateTime,
                                                     "ModelDesign_completion_status": AMPCORE.hasCompletenessStatus,
                                                     "ModelDesign_comment": RDFS.comment,
                                                     "ModelDesign_output": EX.hasModelDesignOutput}},
            "Machine_Powder_Feed_Control_PPI_class": {
                "rdf_type": EB["EB-PBFMachinePowderFeedControlPrintingProcessInstructions"],
                "attributes": {"Machine_powder_s_PPI_name": RDFS.label,
                               "Machine_powder_s_PPI_file": CORE.isRepresentedBy,
                               "Machine_powder_s_PPI_file_format": CORE.hasFileFormat,
                               "Machine_powder_s_PPI_correspond_strategy": "nested"}},
            "Start_Heating_PPI_class": {"rdf_type": EB["EB-PBFStartHeatingPrintingProcessInstructions"],
                                        "attributes": {"start_heat_ppi_name": RDFS.label,
                                                       "start_heat_ppi_file": CORE.isRepresentedBy,
                                                       "start_heat_ppi_file_format": CORE.hasFileFormat,
                                                       "start_heat_ppi_correspond_start_heat_strategy": EB.corresponds_to}},
            "Layer_Pre_Heating_PPI_class": {"rdf_type": EB["EB-PBFLayerPre-HeatingPrintingProcessInstructions"],
                                            "attributes": {
                                                "pre_heat_ppi_name": RDFS.label,
                                                "pre_heat_ppi_file": CORE.isRepresentedBy,
                                                "pre_heat_ppi_file_format": CORE.hasFileFormat,
                                                "pre_heat_ppi_corrspond_layer_build_model": EB.corresponds_to,
                                                "pre_heat_ppi_correspond_pre_heating_strategy": EX.strategy,
                                                "pre_heat_ppi_layer_num": CORE.hasLayerNumber,
                                                "pre_heat_ppi_comment": RDFS.comment,
                                                "pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi": "nested"}},
            "Layer_Post_Heating_PPI_class": {"rdf_type": EB["EB-PBFLayerPost-HeatingPrintingProcessInstructions"],
                                             "attributes": {
                                                 "post_heat_ppi_name": RDFS.label,
                                                 "post_heat_ppi_file": CORE.isRepresentedBy,
                                                 "post_heat_ppi_file_format": CORE.hasFileFormat,
                                                 "post_heat_ppi_corrspond_layer_build_model": EB.corresponds_to,
                                                 "post_heat_ppi_correspond_post_heating_strategy": EB.corresponds_to,
                                                 "post_heat_ppi_layer_num": CORE.hasLayerNumber,
                                                 "post_heat_ppi_comment": RDFS.comment,
                                                 "post_heat_ppi_composed_AM_part_Layer_post_heat_ppi": CORE.isComposedOf,
                                                 "post_heat_ppi_name": CORE.hasName}},
            "Layer_Melting_PPI_class": {"rdf_type": EB["EB-PBFLayerMeltingPrintingProcessInstructions"],
                                        "attributes": {
                                            "melting_ppi_name": RDFS.label,
                                            "melting_ppi_file": CORE.isRepresentedBy,
                                            "melting_ppi_file_format": CORE.hasFileFormat,
                                            "melting_ppi_corrspond_layer_build_model": EB.corresponds_to,
                                            "melting_ppi_correspond_melting_strategy": EB.corresponds_to,
                                            "melting_ppi_layer_num": CORE.hasLayerNumber,
                                            "melting_ppi_comment": RDFS.comment,
                                            "melting_ppi_composed_AM_part_Layer_melting_ppi": CORE.isComposedOf,
                                            "melting_ppi_name": CORE.hasName}},
            "Printing_Process_Instructions_class": {
                "rdf_type": EB["EB-PBFPrintingProcessInstructions"],
                "attributes": {
                    "printing_process_name": RDFS.label,
                    "ppi_file": CORE.isRepresentedBy,
                    "ppi_file_format": CORE.hasFileFormat,
                    "ppi_list_layer_thicknesses": EB.hasAListOfLayerThicknesses,
                    "ppi_comment": RDFS.comment,
                    "ppi_machine_powder_feed": "nested",
                    "ppi_start_heating_ppi": "nested",
                    "ppi_layer_pre_heating_ppi": "nested",
                    "ppi_layer_post_heating_ppi": "nested",
                    "ppi_layer_melting_heating_ppi": "nested"}},
            "Printing_Process_class": {
                "rdf_type": EB["EB-PBFPrintingProcess"],
                "attributes": {
                    "printing_process_name": RDFS.label,
                    "printing_process_status": AMPCORE.hasCompletenessStatus,
                    "printing_process_start_date": AMPCORE.hasStartDateTime,
                    "printing_process_end_date": AMPCORE.hasEndDateTime,
                    "printing_process_comment": RDFS.comment,
                    "printing_process_output": CORE.hasOutputPrintedBuild,
                    "printing_process_build_plate": EB.hasBuildPlate,
                    "printing_process_printing_medium": CORE.hasPrintingMedium,
                    "printing_process_printing_machine": CORE.isOperatedBy,
                    "printing_process_instructions": CORE.hasInput}},
            "Machine_Powder_Feed_Control_Strategy_class": {"rdf_type": EB["EB-PBFMachinePowderFeedControlStrategy"],
                                                           "attributes": {"Machine_powder_s_name": RDFS.label,
                                                                          "Machine_powder_s_comment": RDFS.comment,
                                                                          "Machine_powder_s_file": CORE.isRepresentedBy,
                                                                          "Machine_powder_s_triggered_start": EB.hasTriggeredStart,
                                                                          "Machine_powder_s_recoater_full_repeats": EB.hasRecoaterFullRepeats,
                                                                          "Machine_powder_s_recoater_speed": EB.hasRecoaterAdvancedSpeed,
                                                                          "Machine_powder_s_recoater_retract_speed": EB.hasRecoaterRetractSpeed,
                                                                          "Machine_powder_s_recoater_dwell_time": EB.hasRecoaterDwellTime,
                                                                          "Machine_powder_s_recoater_build_repeats": EB.hasRecoaterBuildRepeats,
                                                                          "Machine_powder_s_file_format": CORE.hasFileFormat}},
            "AM_Part_Layer_Pre_Heating_PPI_class": {
                "rdf_type": EB["EB-PBFAMPartLayerPre-HeatingPrintingProcessInstructions"],
                "attributes": {
                    "AM_part_pre_heat_ppi_name": RDFS.label,
                    "AM_part_pre_heat_ppi_file": CORE.isRepresentedBy,
                    "AM_part_pre_heat_ppi_file_format": CORE.hasFileFormat,
                    "AM_part_pre_heat_ppi_correspond_layer_build_model": EB.corresponds_to,
                    "AM_part_pre_heat_ppi_correspond_AM_part_pre_heat_strategy": EB.corresponds_to,
                    "AM_part_pre_heat_ppi_comment": RDFS.comment}},
            "AM_Part_Layer_Post_Heating_PPI_class": {
                "rdf_type": EB["EB-PBFAMPartLayerPost-HeatingPrintingProcessInstructions"],
                "attributes": {
                    "AM_part_post_heat_ppi_name": RDFS.label,
                    "AM_part_post_heat_ppi_file": CORE.isRepresentedBy,
                    "AM_part_post_heat_ppi_file_format": CORE.hasFileFormat,
                    "AM_part_post_heat_ppi_correspond_layer_build_model": EB.corresponds_to,
                    "AM_part_post_heat_ppi_correspond_AM_part_post_heat_strategy": EB.corresponds_to,
                    "AM_part_post_heat_ppi_comment": RDFS.comment}},
            "AM_Part_Layer_Melting_PPI_class": {"rdf_type": EB["EB-PBFAMPartLayerMeltingPrintingProcessInstructions"],
                                                "attributes": {"AM_part_melting_ppi_name": RDFS.label,
                                                               "AM_part_melting_ppi_file": CORE.isRepresentedBy,
                                                               "AM_part_melting_ppi_file_format": CORE.hasFileFormat,
                                                               "AM_part_melting_ppi_correspond_layer_build_model": EB.corresponds_to,
                                                               "AM_part_melting_ppi_correspond_AM_part_melting_strategy": EB.corresponds_to,
                                                               "AM_part_melting_ppi_comment": RDFS.comment}},
            "applied_testing_method_class": {"rdf_type": CORE.PBFTestingData,
                                             "attributes": {
                                                 "applied_testing_method_name": CORE.nameOfTestingMethod,
                                                 "applied_testing_method_result": CORE.hasValue,
                                                 "TestingMethod_comment": RDFS.comment}},
            "Slicing_Process_class": {
                "rdf_type": EB["EB-PBFSlicingProcess"],
                "attributes": {
                    "SlicingProcess_name": RDFS.label,
                    "SlicingProcess_completion_status": AMPCORE.hasCompletenessStatus,
                    "SlicingProcess_software": prov.wasAssociatedWith,
                    "SlicingProcess_start_date": AMPCORE.hasStartDateTime,
                    "SlicingProcess_end_date": AMPCORE.hasEndDateTime,
                    "SlicingProcess_comment": RDFS.comment,
                    "SlicingProcess_input": CORE.hasInput,
                    "SlicingProcess_output": CORE.hasOutput }},
            "Testing_Process_class": {
                "rdf_type": CORE.PBFTestingProcess,
                "attributes": {
                    "TestingProcess_name": RDFS.label,
                    "TestingProcess_status": AMPCORE.hasCompletenessStatus,
                    "TestingProcess_start_date": AMPCORE.hasStartDateTime,
                    "TestingProcess_end_date": AMPCORE.hasEndDateTime,
                    "TestingProcess_comment": RDFS.comment,
                    "TestingProcess_hasInputPrintedBuild": CORE.hasInputPrintedBuild,
                    "TestingProcess_hasInputPrintedBuildAMPart": "nested",
                    "TestingProcess_hasInputPrintedBuildSupport": "nested",
                    "TestingProcess_testing_method": "nested",
                    "TestingProcess_testing_data": "nested"}},
            "Layer_Of_Build_Model_AM_Part_class": {
                "rdf_type": CORE.LayerOfPBFBuildModelAMPart,
                "attributes": {
                    "layer_of_Build_Model_AM_Part_name": [RDFS.label, CORE.hasName],
                    "layer_of_Build_Model_AM_Part_file": CORE.isRepresentedBy,
                    "layer_of_Build_Model_AM_Part_file_format": CORE.hasFileFormat,
                    "layer_of_Build_Model_AM_Part_area": CORE.hasArea,
                    "Layer_Of_Build_Model_AM_Part_comment": RDFS.comment}},
            "Layer_Of_Build_Model_class": {
                "rdf_type": CORE.LayerOfPBFBuildModel,
                "attributes": {
                    "Layer_Of_Build_Model_name": RDFS.label,
                    "Layer_Of_Build_Model_file": CORE.isRepresentedBy,
                    "Layer_Of_Build_Model_file_format": CORE.hasFileFormat,
                    "Layer_Of_Build_Model_layer_height": CORE.hasLayerHeight,
                    "Layer_Of_Build_Model_layer_num": CORE.hasLayerNumber,
                    "Layer_Of_Build_Model_comment": RDFS.comment,
                    "Layer_Of_Build_Model_consists_of_am_part_layer": "nested"}},
            "Post_Printing_Method": {
                "rdf_type": EB["EB-PBFPost-PrintingMethod"],
                "attributes": {
                    "post_printing_method_name": RDFS.label,
                    "post_printing_method_comment": RDFS.comment,
                    "post_printing_method_type": "nested"}},
            "Post_Printing_Process_class": {
                "rdf_type": CORE["PBFPost-PrintingProcess"],
                "attributes": {
                    "post_printing_process_name": RDFS.label,
                    "post_printing_process_status": AMPCORE.hasCompletenessStatus,
                    "post_printing_process_start_date": AMPCORE.hasStartDateTime,
                    "post_printing_process_end_date": AMPCORE.hasEndDateTime,
                    "post_printing_process_used_methods": "nested",
                    "post_printing_process_comment": RDFS.comment}},
            "Start_Heating_Strategy_class": {"rdf_type": EB["EB-PBFStartHeatingStrategy"],
                                             "attributes": {"start_heat_name": RDFS.label,
                                                            "start_heat_file": CORE.isRepresentedBy,
                                                            "start_heat_file_format": CORE.hasFileFormat,
                                                            "start_heat_size": EB.hasSize,
                                                            "start_heat_timeout": EB.hasTimeout,
                                                            "start_heat_scan_strategy": EB.hasScanStrategy,
                                                            "start_heat_shape": EB.hasShape,
                                                            "start_heat_rotation_angle": EB.hasRotationAngle,
                                                            "start_heat_target_temp": EB.hasTargetTemperature,
                                                            "start_heat_comment": RDFS.comment}},
            "AM_Part_Layer_Pre_Heating_Strategy_class": {"rdf_type": EB["EB-PBFAMPartLayerPre-HeatingStrategy"],
                                                         "attributes": {"AM_part_pre_heat_strategy_name": RDFS.label,
                                                                        "AM_part_pre_heat_strategy_file": CORE.isRepresentedBy,
                                                                        "AM_part_pre_heat_strategy_file_format": CORE.hasFileFormat,
                                                                        "AM_part_pre_heat_strategy_number_comment": RDFS.comment,
                                                                        "AM_part_pre_heat_strategy_scan_strategy": EB.hasScanStrategy,
                                                                        "AM_part_pre_heat_strategy_rotation_angle": EB.hasRotationAngle,
                                                                        "AM_part_pre_heat_strategy_number_repetitions": EB.hasNumberOfRepetitions}},
            "Layer_Pre_Heating_Strategy_class": {"rdf_type": EB["EB-PBFLayerPre-HeatingStrategy"],
                                                 "attributes": {"pre_heat_strategy_name": RDFS.label,
                                                                "pre_heat_strategy_file": CORE.isRepresentedBy,
                                                                "pre_heat_strategy_file_format": CORE.hasFileFormat,
                                                                "pre_heat_strategy_scan_strategy": EB.hasScanStrategy,
                                                                "pre_heat_strategy_composed_of_AM_Parts": "nested",
                                                                "pre_heat_strategy_comment": RDFS.comment}},
            "AM_Part_Layer_Post_Heating_Strategy_class": {"rdf_type": EB["EB-PBFAMPartLayerPost-HeatingStrategy"],
                                                          "attributes": {"AM_part_post_heat_strategy_name": RDFS.label,
                                                                         "AM_part_post_heat_strategy_file": CORE.isRepresentedBy,
                                                                         "AM_part_post_heat_strategy_file_format": CORE.hasFileFormat,
                                                                         "AM_part_post_heat_strategy_number_comment": RDFS.comment,
                                                                         "AM_part_post_heat_strategy_scan_strategy": EB.hasScanStrategy,
                                                                         "AM_part_post_heat_strategy_rotation_angle": EB.hasRotationAngle,
                                                                         "AM_part_post_heat_strategy_number_repetitions": EB.hasNumberOfRepetitions}},
            "Layer_Post_Heating_Strategy_class": {"rdf_type": EB["EB-PBFLayerPost-HeatingStrategy"],
                                                  "attributes": {"post_heat_strategy_name": RDFS.label,
                                                                 "post_heat_strategy_file": CORE.isRepresentedBy,
                                                                 "post_heat_strategy_file_format": CORE.hasFileFormat,
                                                                 "post_heat_strategy_scan_strategy": EB.hasScanStrategy,
                                                                 "post_heat_strategy_composed_of_AM_Parts": CORE.isComposedOf,
                                                                 "post_heat_strategy_comment": RDFS.comment}},
            "AM_Part_Layer_Melting_Strategy_class": {"rdf_type": EB["EB-PBFAMPartLayerMeltingStrategy"],
                                                     "attributes": {"AM_part_melting_strategy_name": RDFS.label,
                                                                    "AM_part_melting_strategy_file": CORE.isRepresentedBy,
                                                                    "AM_part_melting_strategy_file_format": CORE.hasFileFormat,
                                                                    "AM_part_melting_strategy_comment": RDFS.comment,
                                                                    "AM_part_melting_strategy_scan_strategy": EB.hasScanStrategy,
                                                                    "AM_part_post_heat_strategy_rotation_angle": EB.hasRotationAngle,
                                                                    "AM_part_melting_strategy_number_repetitions": EB.hasNumberOfRepetitions,
                                                                    "AM_part_melting_strategy_point_distance": EB.hasUniformPointDistance,
                                                                    "AM_part_melting_strategy_energy_density": EB.hasEnergyDensity,
                                                                    "AM_part_melting_strategy_offset_margin": EB.hasOffsetMargin}},
            "Layer_Melting_Strategy_class": {"rdf_type": EB["EB-PBFLayerMeltingStrategy"],
                                             "attributes": {"melting_strategy_name": RDFS.label,
                                                            "melting_strategy_file": CORE.isRepresentedBy,
                                                            "melting_strategy_file_format": CORE.hasFileFormat,
                                                            "melting_strategy_scan_strategy": EB.hasScanStrategy,
                                                            "melting_strategy_composed_of_AM_Parts": CORE.isComposedOf,
                                                            "melting_strategy_comment": RDFS.comment}},
            "Beam_Control_Slicing_Strategy_class": {
                "rdf_type": EB["EB-PBFBeamControlSlicingStrategy"],
                "attributes": {"beam_control_slic_strategy_name": RDFS.label,
                               "beam_control_slic_strategy_file": CORE.isRepresentedBy,
                               "beam_control_slic_strategy_file_format": CORE.hasFileFormat,
                               "beam_control_pre_heating": "nested",
                               "beam_control_slic_strategy_melting": "nested",
                               "beam_control_slic_strategy_post_heating": "nested",
                               "beam_control_start_heating_strategy": "nested"}},
            "Monitoring_Process_class": {
                "rdf_type": CORE.PBFMonitoringProcess,
                "attributes": {
                    "monitoring_process_name": RDFS.label,
                    "monitoring_process_start_date": AMPCORE.hasStartDateTime,
                    "monitoring_process_end_date": AMPCORE.hasEndDateTime,
                    "monitoring_process_comment": RDFS.comment,
                    "monitoring_process_status": AMPCORE.hasCompletenessStatus,
                    "monitoring_process_output_file": CORE.hasOutputData,
                    "monitoring_process_printing_process": CORE.monitors,
                    "monitoring_process_receives_data_from": "nested"}}
        }
        # ****************************************************************************************************
        # ****************************************************************************************************
        # Load JSON data, "shared_lists.pkl"
        json_filename, _ = QFileDialog.getOpenFileName(self, "Open JSON file", "", "JSON files (*.json)")
        if not json_filename:
            QMessageBox.warning(self, "No File Selected", "No JSON file was selected.")
            return
        with open(json_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        # ****************************************************************************************************
        g = Graph()
        g.parse("EB-2.rdf", format="xml")
        g.bind("prov", prov)
        g.bind("rdfs", RDFS)
        g.bind("core", CORE)
        g.bind("eb", EB)
        g.bind("ex", EX)
        g.bind("ampcore", AMPCORE)
        g.bind("owl", OWL)  # ✅ Ensure OWL is bound

        for class_name, instances in data.items():
            if class_name not in class_mappings:
                continue
            mapping = class_mappings[class_name]
            default_rdf_type = mapping["rdf_type"]
            rdf_type_name = default_rdf_type.split("#")[-1]
            attr_map = mapping["attributes"]

            for instance in instances:
                rdf_type = default_rdf_type

                if rdf_type_name == "PBFPrintingMachine":
                    try:
                        brand_value = instance.get("printing_machine_brand", "").lower()
                        if brand_value == "EB-PBF Freemelt":
                            rdf_type = EB["EB-PBFPrintingMachine"]
                    except: pass

                if rdf_type_name == "Post_Printing_Method":
                    try:
                        type_value = instance.get("post_printing_method_type", "").lower()
                        if type_value == "Support Removal":
                            rdf_type = EB["EB-PBFSupportRemovalMethod"]
                        if type_value == "Heat Treatment":
                            rdf_type = EB["EB-PBFHeatTreatmentMethod"]
                        if type_value == "Build Cleaning":
                            rdf_type = EB["EB-PBFBuildCleaningMethod"]
                        if type_value == "Build Separation From Build Plate":
                            rdf_type = EB["EB-PBFBuildSeparationFromBuildPlateMethod"]
                    except: pass

                if rdf_type_name == "PBFTestingMethod":
                    try:
                        type_value = instance.get("TestingMethod_type", "").lower()
                        if type_value == "Non-Destructive":
                            rdf_type = EB["PBFNon-DestructiveTestingMethod"]
                        if type_value == "Destructive":
                            rdf_type = EB["PBFDestructiveTestingMethod"]
                    except: pass

                #Create URI
                label_value = ""
                try:
                    label_attr = [k for k, v in attr_map.items() if v == RDFS.label][0]
                    try:
                        if isinstance(instance, dict):
                            label_value = instance.get(label_attr, "").strip().replace(" ", "_")
                        else:
                            label_value = str(instance).strip().replace(" ", "_")
                    except: pass
                except: pass

                if label_value == "":
                    continue

                uri = URIRef(EX + label_value)
                existing_types = [obj for _, _, obj in g.triples((uri, RDF.type, None))]
                if rdf_type in existing_types: pass
                else:
                    if any(g.triples((uri, None, None))):
                        try:
                            uri = URIRef(f"{EX}{class_name.__name__}/{label_value.replace(' ', '_')}")
                        except:
                            uri = URIRef(f"{EX}{class_name}/{label_value.replace(' ', '_')}")
                    g.add((uri, RDF.type, OWL.NamedIndividual))
                g.add((uri, RDF.type, rdf_type))
                namespace_1, local_name_1 = split_uri(rdf_type)
                g.add((uri, RDFS.label, Literal(local_name_1)))
                if rdf_type_name == "PBFBuildModelAMPart" or rdf_type_name == "Manufacturer" or rdf_type_name == "PBFBuildModelSupport" or rdf_type_name == "PBFBuildModel" \
                        or rdf_type_name == "Layer_Post_Heating_PPI_class" or rdf_type_name == "Layer_Melting_PPI_class" or rdf_type_name == "AM_Part_Layer_Pre_Heating_PPI_class" \
                        or rdf_type_name == "AM_Part_Layer_Post_Heating_PPI_class" or rdf_type_name == "AM_Part_Layer_Melting_PPI_class" \
                        or rdf_type_name == "Layer_Of_Build_Model_AM_Part_class":
                    g.add((uri, CORE.hasName, Literal(label_value)))
                #================================================================================================
                # Add basic attributes
                for attr, predicate in attr_map.items():
                    if predicate == "nested":
                        continue
                    # *********************************************************************
                    if attr == "Machine_powder_s_PPI_correspond_strategy":
                        try:
                            for i in instance["Machine_powder_s_PPI_correspond_strategy"]:
                                i_name = i.strip().replace(" ", "_")
                                i_uri = URIRef(EX + i_name)
                                i_uri_2 = URIRef(f"{EX}Machine_Powder_Feed_Control_Strategy_class/{i_name.replace(' ', '_')}")
                                if (i_uri, RDF.type, EB["EB-PBFMachinePowderFeedControlStrategy"]) not in g:
                                    if (i_uri_2, RDF.type, EB["EB-PBFMachinePowderFeedControlStrategy"]) not in g:
                                        g.add((i_uri, RDF.type, EB["EB-PBFMachinePowderFeedControlStrategy"]))
                                        if (uri, EB.corresponds_to, i_uri) not in g:
                                            g.add((uri, EB.corresponds_to, i_uri))
                                            break
                                    else:
                                        if (uri, EB.corresponds_to, i_uri) not in g:
                                            g.add((uri, EB.corresponds_to, i_uri_2))
                                            break
                                else:
                                    if (uri, EB.corresponds_to, i_uri) not in g:
                                        g.add((uri, EB.corresponds_to, i_uri_2))
                                        break
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "pre_heat_ppi_corrspond_layer_build_model":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, CORE.LayerOfPBFBuildModel))):
                                g.add((m_uri, RDF.type, CORE.LayerOfPBFBuildModel))
                            g.add((uri, EB.corresponds_to, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "pre_heat_ppi_correspond_pre_heating_strategy":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, EB["EB-PBFLayerPre-HeatingStrategy"]))):
                                g.add((m_uri, RDF.type, EB["EB-PBFLayerPre-HeatingStrategy"]))
                            g.add((uri, EB.corresponds_to, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "printing_process_output":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, EB["EB-PBFPrintedBuild"]))):
                                g.add((m_uri, RDF.type, EB["EB-PBFPrintedBuild"]))
                            g.add((uri, CORE.hasOutputPrintedBuild, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "printing_process_build_plate":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if (m_uri, RDF.type, EB["EB-PBFBuildPlate"]) not in g:
                                g.add((m_uri, RDF.type, EB["EB-PBFBuildPlate"]))
                            if (uri, EB.hasBuildPlate, m_uri) not in g:
                                g.add((uri, EB.hasBuildPlate, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "printing_process_printing_medium":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, CORE.PBFPowder))):
                                g.add((m_uri, RDF.type, CORE.PBFPowder))
                            g.add((uri, CORE.hasPrintingMedium, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "printing_process_printing_machine":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, CORE.PBFPrintingMachine))):
                                g.add((m_uri, RDF.type, CORE.PBFPrintingMachine))
                            g.add((uri, CORE.isOperatedBy, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "printing_process_instructions":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, EB["EB-PBFPrintingProcessInstructions"]))):
                                g.add((m_uri, RDF.type, EB["EB-PBFPrintingProcessInstructions"]))
                            g.add((uri, CORE.hasInput, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "post_heat_ppi_corrspond_layer_build_model":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, CORE.LayerOfPBFBuildModel))):
                                g.add((m_uri, RDF.type, CORE.LayerOfPBFBuildModel))
                            g.add((uri, EB.corresponds_to, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "post_heat_ppi_correspond_post_heating_strategy":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, EB["EB-PBFLayerPost-HeatingStrategy"]))):
                                g.add((m_uri, RDF.type, EB["EB-PBFLayerPost-HeatingStrategy"]))
                            g.add((uri, EB.corresponds_to, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "melting_ppi_corrspond_layer_build_model":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, CORE.LayerOfPBFBuildModel))):
                                g.add((m_uri, RDF.type, CORE.LayerOfPBFBuildModel))
                            g.add((uri, EB.corresponds_to, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "melting_ppi_correspond_melting_strategy":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, EB["EB-PBFLayerMeltingStrategy"]))):
                                g.add((m_uri, RDF.type, EB["EB-PBFLayerMeltingStrategy"]))
                            g.add((uri, EB.corresponds_to, m_uri))
                            continue
                        except: pass
                    # *********************************************************************
                    if attr == "ModelDesign_output":
                        try:
                            output_data = instance.get("ModelDesign_output")
                            if output_data:
                                m_uri, m_uri_2 = '', ''
                                for key, value in output_data.items():
                                    if value and key == 'build_model_name':  # skip empty or None values
                                        m = str(value).strip().replace(" ", "_")
                                        m_uri = URIRef(EX + m)
                                        m_uri_2 = URIRef(f"{EX}output_Build_Model_Design_Process_class/{m}")
                                        if (m_uri, RDF.type, CORE.PBFBuildModel) not in g:
                                            g.add((m_uri, RDF.type, CORE.PBFBuildModel))
                                            if (uri, CORE.hasOutput, m_uri) not in g:
                                                g.add((uri, CORE.hasOutput, m_uri))
                                                m_uri_2 = m_uri
                                        else:
                                            if (uri, CORE.hasOutput, m_uri_2) not in g:
                                                g.add((uri, CORE.hasOutput, m_uri_2))
                                                m_uri = m_uri_2
                                    if value and key == 'build_model_dimension':
                                        s = str(value).strip().replace(" ", "_")
                                        g.add((m_uri, CORE.hasDimensions,Literal(s)))
                                    if value and key == 'build_model_file_path':
                                        s = str(value).strip().replace(" ", "_")
                                        g.add((m_uri, CORE.isRepresentedBy,Literal(s)))
                                    if value and key == 'build_model_file_format':
                                        s = str(value).strip().replace(" ", "_")
                                        file_format_uri = EX[s.replace(".", "_")]  # e.g., ex:partA_stl
                                        if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                            g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                        g.add((m_uri, CORE.hasFileFormat, file_format_uri))
                                    if value and key == 'build_model_comment':
                                        s = str(value).strip().replace(" ", "_")
                                        g.add((m_uri, RDFS.comment, Literal(s)))
                                    if value and key == 'build_model_parts_supports':
                                        try:
                                            temp = value[0].strip("[]'")
                                            temp_2 = temp.split("Get Support:", 1)[1].strip()
                                            s = str(temp_2).strip().replace(" ", "_")
                                            s_uri = URIRef(EX + s)
                                            if not any(g.triples((s_uri, RDF.type, CORE.PBFPrintedBuildSupport))):
                                                g.add((s_uri, RDF.type, CORE.PBFPrintedBuildSupport))
                                            g.add((m_uri, EB.hasBuildModelPartSupport, s_uri))
                                        except: pass
                        except Exception as e:
                            print(f"Error processing ModelDesign_output: {e}")
                    # *********************************************************************
                    if attr == "build_model_parts_supports":
                        try:
                            part_names = []
                            support_names = []
                            if isinstance(instance, dict) and "build_model_parts_supports" in instance:
                                for i in instance["build_model_parts_supports"]:
                                    match = re.search(r"AM Part:\s*(.*?)\s+Get Support:\s*(.*)", i)
                                    if match:
                                        part_name = match.group(1).strip()
                                        get_support = match.group(2).strip()
                                        if part_name and part_name not in part_names:
                                            part_names.append(part_name)
                                            part_name_name = part_name.strip().replace(" ", "_")
                                            part_name_uri = URIRef(EX + part_name_name)
                                            if (part_name_uri, RDF.type, CORE.PBFPrintedBuildAMPart) not in g:
                                                g.add((part_name_uri, RDF.type, CORE.PBFPrintedBuildAMPart))
                                            if (uri, CORE.consistsOf, part_name_uri) not in g:
                                                g.add((uri, CORE.consistsOf, part_name_uri))
                                        if get_support and get_support not in support_names:
                                            support_names.append(get_support)
                                            get_support_name = get_support.strip().replace(" ", "_")
                                            get_support_uri = URIRef(EX + get_support_name)
                                            if (get_support_uri, RDF.type, CORE.PBFPrintedBuildSupport) not in g:
                                                g.add((get_support_uri, RDF.type, CORE.PBFPrintedBuildSupport))
                                            if (uri, CORE.consistsOf, get_support_uri) not in g:
                                                g.add((uri, CORE.consistsOf, get_support_uri))
                                            g.add((get_support_uri, CORE.providesSupportFor, part_name_uri))
                                    pass
                        except: pass
                    # *********************************************************************
                    if attr == "printing_medium_material":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, CORE.PBFPowder))):
                                g.add((m_uri, RDF.type, CORE.PBFPowder))
                            g.add((uri, EB.isManufacturedFrom, m_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "printing_medium_manufacturer":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, EB.Manufacturer))):
                                g.add((m_uri, RDF.type, EB.Manufacturer))
                            g.add((uri, EB.isManufacturedBy, m_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "build_plate_material":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, EB.Material))):
                                g.add((m_uri, RDF.type, EB.Material))
                            g.add((uri, EB.isManufacturedFrom, m_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "build_plate_manufacturer":
                        try:
                            m = instance.get(attr, "").strip().replace(" ", "_")
                            m_uri = URIRef(EX + m)
                            if not any(g.triples((m_uri, RDF.type, EB.Manufacturer))):
                                g.add((m_uri, RDF.type, EB.Manufacturer))
                            g.add((uri, EB.isManufacturedBy, m_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "beam_control_slic_strategy_file":
                        try:
                            file_name = instance.get("beam_control_slic_strategy_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("beam_control_slic_strategy_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "melting_strategy_file":
                        try:
                            file_name = instance.get("melting_strategy_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("melting_strategy_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "AM_part_melting_strategy_file":
                        try:
                            file_name = instance.get("AM_part_melting_strategy_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("AM_part_melting_strategy_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "melting_strategy_file":
                        try:
                            file_name = instance.get("melting_strategy_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("melting_strategy_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "post_heat_strategy_file":
                        try:
                            file_name = instance.get("post_heat_strategy_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("post_heat_strategy_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "ppi_file":
                        try:
                            file_name = instance.get("ppi_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("ppi_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "AM_part_pre_heat_strategy_file":
                        try:
                            file_name = instance.get("AM_part_pre_heat_strategy_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("AM_part_pre_heat_strategy_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "pre_heat_strategy_file":
                        try:
                            file_name = instance.get("pre_heat_strategy_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("pre_heat_strategy_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "AM_part_post_heat_strategy_file":
                        try:
                            file_name = instance.get("AM_part_post_heat_strategy_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("AM_part_post_heat_strategy_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "support_file_path":
                        try:
                            file_name = instance.get("support_file_path")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("support_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "start_heat_file":
                        try:
                            file_name = instance.get("start_heat_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("start_heat_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "layer_of_Build_Model_AM_Part_file":
                        try:
                            file_name = instance.get("layer_of_Build_Model_AM_Part_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("layer_of_Build_Model_AM_Part_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "Layer_Of_Build_Model_file":
                        try:
                            file_name = instance.get("Layer_Of_Build_Model_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("Layer_Of_Build_Model_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "AM_part_post_heat_ppi_file":
                        try:
                            file_name = instance.get("AM_part_post_heat_ppi_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("AM_part_post_heat_ppi_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "AM_part_melting_ppi_file":
                        try:
                            file_name = instance.get("AM_part_melting_ppi_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("AM_part_melting_ppi_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "melting_ppi_file":
                        try:
                            file_name = instance.get("melting_ppi_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("melting_ppi_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "Machine_powder_s_file":
                        try:
                            file_name = instance.get("Machine_powder_s_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("Machine_powder_s_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "AM_part_pre_heat_ppi_file":
                        try:
                            file_name = instance.get("AM_part_pre_heat_ppi_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("AM_part_pre_heat_ppi_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "post_heat_ppi_file":
                        try:
                            file_name = instance.get("post_heat_ppi_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("post_heat_ppi_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "build_model_file_path":
                        try:
                            file_name = instance.get("build_model_file_path")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("build_model_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "pre_heat_ppi_file":
                        try:
                            file_name = instance.get("pre_heat_ppi_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("pre_heat_ppi_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "Machine_powder_s_PPI_file":
                        try:
                            file_name = instance.get("Machine_powder_s_PPI_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("Machine_powder_s_PPI_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "start_heat_ppi_file":
                        try:
                            file_name = instance.get("start_heat_ppi_file")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("start_heat_ppi_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if attr == "am_part_file_path":
                        try:
                            file_name = instance.get("am_part_file_path")
                            if file_name:
                                file_path = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
                                file_uri = EX[file_path]
                                if (file_uri, RDF.type, CORE.File) not in g:
                                    g.add((file_uri, RDF.type, CORE.File))
                                g.add((uri, CORE.isRepresentedBy, file_uri))
                                file_format_name = instance.get("am_part_file_format")
                                if file_format_name:
                                    file_format_uri = EX[file_format_name.replace(".", "_")]
                                    if (file_format_uri, RDF.type, CORE.FileFormat) not in g:
                                        g.add((file_format_uri, RDF.type, CORE.FileFormat))
                                    g.add((file_uri, CORE.hasFileFormat, file_format_uri))
                        except: pass
                    # *********************************************************************
                    if isinstance(instance, dict):
                        value = instance.get(attr, "")
                    elif hasattr(instance, attr):
                        value = getattr(instance, attr)
                    else:
                        value = instance  # fallback: treat instance as the value itself

                    namespace_1, local_name_1 = split_uri(predicate)

                    if value and value != "2025-01-01 00:00:00" and local_name_1 != 'label':
                        g.add((uri, predicate, Literal(value)))
                #======================================================================================
                if isinstance(instance, Monitoring_Process_class):
                    try:
                        for i in instance["monitoring_process_receives_data_from"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            i_uri_2 = URIRef(f"{EX}Sensor_class/{i_name.replace(' ', '_')}")
                            if (i_uri, RDF.type, CORE.PBFPrintingMachineSensor) not in g:
                                if (i_uri_2, RDF.type, CORE.PBFPrintingMachineSensor) not in g:
                                    g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                    g.add((i_uri, RDF.type, CORE.PBFPrintingMachineSensor))
                                    break
                                else:
                                    i_uri = i_uri_2
                            if (uri, CORE.receivesDataFrom, i_uri) not in g:
                                g.add((uri, CORE.receivesDataFrom, i_uri))
                    except: pass
                # ======================================================================================
                if isinstance(instance, Beam_Control_Slicing_Strategy_class):
                    try:
                        for i in instance["beam_control_start_heating_strategy"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            i_uri_2 = URIRef(f"{EX}Start_Heating_Strategy_class/{i_name.replace(' ', '_')}")
                            if (i_uri, RDF.type, EB["EB-PBFStartHeatingStrategy"]) not in g:
                                if (i_uri_2, RDF.type, EB["EB-PBFStartHeatingStrategy"]) not in g:
                                    g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                    g.add((i_uri, RDF.type, EB["EB-PBFStartHeatingStrategy"]))
                                    break
                                else:
                                    i_uri = i_uri_2
                            if (i_uri, EB.isSubStrategyOf, uri) not in g:
                                g.add((i_uri, EB.isSubStrategyOf, uri))
                    except: pass
                # ======================================================================================
                    try:
                        for i in instance["beam_control_pre_heating"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, EB["EB-PBFLayerPre-HeatingStrategy"]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB["EB-PBFLayerPre-HeatingStrategy"]))
                            if (i_uri, EB.isSubStrategyOf, uri) not in g:
                                g.add((i_uri, EB.isSubStrategyOf, uri))
                    except: pass

                    try:
                        for i in instance["beam_control_slic_strategy_post_heating"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, EB["EB-PBFLayerPost-HeatingStrategy"]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB["EB-PBFLayerPost-HeatingStrategy"]))
                            if (i_uri, EB.isSubStrategyOf, uri) not in g:
                                g.add((i_uri, EB.isSubStrategyOf, uri))

                    except: pass

                    try:
                        for i in instance["beam_control_slic_strategy_melting"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, EB[EB["EB-PBFLayerMeltingStrategy"]]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB[EB["EB-PBFLayerMeltingStrategy"]]))
                            if (i_uri, EB.isSubStrategyOf, uri) not in g:
                                g.add((i_uri, EB.isSubStrategyOf, uri))
                    except: pass

                if isinstance(instance, Layer_Melting_Strategy_class):
                    try:
                        for i in instance["melting_strategy_composed_of_AM_Parts"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, EB["EB-PBFAMPartLayerMeltingStrategy"]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB["EB-PBFAMPartLayerMeltingStrategy"]))
                            if (uri, CORE.isComposedOf, i_uri) not in g:
                                g.add((uri, CORE.isComposedOf, i_uri))
                    except: pass

                if isinstance(instance, Layer_Post_Heating_Strategy_class):
                    try:
                        for i in instance["post_heat_strategy_composed_of_AM_Parts"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, EB["EB-PBFAMPartLayerPost-HeatingStrategy"]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB["EB-PBFAMPartLayerPost-HeatingStrategy"]))
                            if (uri, CORE.isComposedOf, i_uri) not in g:
                                g.add((uri, CORE.isComposedOf, i_uri))
                    except: pass

                if isinstance(instance, Layer_Pre_Heating_Strategy_class):
                    try:
                        for i in instance["pre_heat_strategy_composed_of_AM_Parts"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, EB["EB-PBFAMPartLayerPre-HeatingStrategy"]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB["EB-PBFAMPartLayerPre-HeatingStrategy"]))
                            if (uri, CORE.isComposedOf, i_uri) not in g:
                                g.add((uri, CORE.isComposedOf, i_uri))
                    except: pass

                if isinstance(instance, Post_Printing_Process_class):
                    try:
                        for i in instance["post_printing_process_used_methods"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (uri, CORE.usesPostPrintingMethod, i_uri) not in g:
                                g.add((uri, CORE.usesPostPrintingMethod, i_uri))
                    except: pass

                if isinstance(instance, Layer_Of_Build_Model_class):
                    try:
                        for i in instance["Layer_Of_Build_Model_consists_of_am_part_layer"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, CORE.LayerOfPBFBuildModelAMPart) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, CORE.LayerOfPBFBuildModelAMPart))
                            if (uri, CORE.consistsOf, i_uri) not in g:
                                g.add((uri, CORE.consistsOf, i_uri))
                    except: pass

                if isinstance(instance, Testing_Process_class):
                    try:
                        for i in instance["TestingProcess_testing_data"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, CORE.PBFTestingData) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, CORE.PBFTestingData))
                            if (uri, CORE.outputsTestingData, i_uri) not in g:
                                g.add((uri, CORE.outputsTestingData, i_uri))
                    except: pass

                    try:
                        for i in instance["TestingProcess_testing_method"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, CORE.PBFTestingMethod) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, CORE.PBFTestingMethod))
                            if (uri, CORE.hasTestingMethod, i_uri) not in g:
                                g.add((uri, CORE.hasTestingMethod, i_uri))
                    except: pass

                    try:
                        for i in instance["TestingProcess_hasInputPrintedBuildAMPart"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, CORE.PBFPrintedBuildAMPart) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, CORE.PBFPrintedBuildAMPart))
                            if (uri, CORE.hasInputPrintedBuildAMPart, i_uri) not in g:
                                g.add((uri, CORE.hasInputPrintedBuildAMPart, i_uri))
                    except: pass

                    try:
                        for i in instance["TestingProcess_hasInputPrintedBuildSupport"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, CORE.PBFPrintedBuildSupport) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, CORE.PBFPrintedBuildSupport))
                            if (uri, CORE.hasInputPrintedBuildSupport, i_uri) not in g:
                                g.add((uri, CORE.hasInputPrintedBuildSupport, i_uri))
                    except: pass

                if "Layer_Melting_PPI_class" in instance:
                    try:
                        for part_ppi in instance["melting_ppi_composed_AM_part_Layer_melting_ppi"]:
                            part_ppi_name = part_ppi.strip().replace(" ", "_")
                            part_ppi_uri = URIRef(EX + part_ppi_name)
                            if (i_uri, RDF.type, EB["EB-PBFAMPartLayerMeltingPrintingProcessInstructions"]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB["EB-PBFAMPartLayerMeltingPrintingProcessInstructions"]))
                            if (uri, CORE.isComposedOf, i_uri) not in g:
                                g.add((uri, CORE.isComposedOf, part_ppi_uri))
                    except: pass
                # *********************************************************************
                if "Layer_Pre_Heating_PPI_class" in instance:
                    try:
                        for part_ppi in instance["pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi"]:
                            part_ppi_name = part_ppi.strip().replace(" ", "_")
                            part_ppi_uri = URIRef(EX + part_ppi_name)
                            if (i_uri, RDF.type, EB["EB-PBFAMPartLayerPre-HeatingPrintingProcessInstructions"]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB["EB-PBFAMPartLayerPre-HeatingPrintingProcessInstructions"]))
                            if (uri, CORE.isComposedOf, i_uri) not in g:
                                g.add((uri, CORE.isComposedOf, part_ppi_uri))
                    except: pass
                # *********************************************************************
                if "Layer_Post_Heating_PPI_class" in instance:
                    try:
                        for part_ppi in instance["post_heat_ppi_composed_AM_part_Layer_post_heat_ppi"]:
                            part_ppi_name = part_ppi.strip().replace(" ", "_")
                            part_ppi_uri = URIRef(EX + part_ppi_name)
                            if (i_uri, RDF.type, EB["EB-PBFAMPartLayerPost-HeatingPrintingProcessInstructions"]) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, EB["EB-PBFAMPartLayerPost-HeatingPrintingProcessInstructions"]))
                            if (uri, CORE.isComposedOf, i_uri) not in g:
                                g.add((uri, CORE.isComposedOf, part_ppi_uri))
                    except: pass
                # *********************************************************************
                try:
                    if "project_selected_supervisors" in instance:
                        instance["project_selected_supervisors"] = instance.get("project_selected_supervisors", [])
                        if instance["project_selected_supervisors"]:
                            for supervisor in instance["project_selected_supervisors"]:
                                if isinstance(supervisor, PBF_AM_Process_Chain_class):
                                    supervisor_name = supervisor.get("supervisor_name", "").strip().replace(" ", "_")
                                    supervisor_comment = supervisor.get("supervisor_comment", "")
                                else:
                                    supervisor_name = str(supervisor).strip().replace(" ", "_")
                                    supervisor_comment = ""
                                supervisor_uri = URIRef(EX + supervisor_name)
                                if (supervisor_uri, RDF.type, prov.Agent) not in g:
                                    g.add((supervisor_uri, RDF.type, OWL.NamedIndividual))
                                    g.add((supervisor_uri, RDF.type, prov.Agent))
                                    g.add((supervisor_uri, RDFS.label, Literal(supervisor_name)))
                                    g.add((supervisor_uri, RDFS.comment, Literal(supervisor_comment)))
                                g.add((uri, CORE.isSupervisedBy, supervisor_uri))
                        else:
                            print("Warning: 'instance' is not a dictionary or missing 'project_selected_supervisors'")
                except: pass
                # ----------------------------------------------------------------------------------------------------------------
                if "Printing_Process_Instructions_class" in instance:
                    try:
                        for i in instance["ppi_machine_powder_feed"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            g.add((uri, EB.contains, i_uri))
                        for i in instance["ppi_start_heating_ppi"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            g.add((uri, EB.contains, i_uri))
                        for i in instance["ppi_layer_pre_heating_ppi"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            g.add((uri, EB.contains, i_uri))
                        for i in instance["ppi_layer_post_heating_ppi"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            g.add((uri, EB.contains, i_uri))
                        for i in instance["ppi_layer_melting_heating_ppi"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            g.add((uri, EB.contains, i_uri))
                    except: pass

                if "printing_machine_sensor_info" in instance:
                    try:
                        for i in instance["printing_machine_sensor_info"]:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            if (i_uri, RDF.type, CORE.PBFPrintingMachineSensor) not in g:
                                g.add((i_uri, RDF.type, OWL.NamedIndividual))
                                g.add((i_uri, RDF.type, CORE.PBFPrintingMachineSensor))
                                g.add((i_uri, RDFS.label, Literal(i["sensor_name"])))
                                g.add((i_uri, CORE.hasSensorType, Literal(i.get("sensor_type", ""))))
                                g.add((i_uri, CORE.hasRecordedData, Literal(i.get("recorded_data_path", ""))))
                            g.add((uri, CORE.hasSensor, i_uri))
                    except: pass

                if attr == "Printed_Build_AM_Parts_and_supports" in instance:
                    try:
                        part_names = []
                        support_names = []
                        for i in instance["Printed_Build_AM_Parts_and_supports"]:
                            match = re.search(r"Printed Build AM Part:\s*(.*?)\s+Get Support:\s*(.*)", i)
                            if match:
                                part_name = match.group(1).strip()
                                get_support = match.group(2).strip()
                                if part_name and part_name not in part_names:
                                    part_names.append(part_name)
                                    part_name_name = part_name.strip().replace(" ", "_")
                                    part_name_uri = URIRef(EX + part_name_name)
                                    part_name_uri_2 = URIRef(
                                        f"{EX}Printed_Build_AM_Part_class/{part_name_name.replace(' ', '_')}")
                                    if (part_name_uri, RDF.type, CORE.PBFPrintedBuildAMPart) not in g:
                                        if (part_name_uri_2, RDF.type, CORE.PBFPrintedBuildAMPart) not in g:
                                            g.add((part_name_uri, RDF.type, CORE.PBFPrintedBuildAMPart))
                                            break
                                    else:
                                        if (part_name_uri_2, RDF.type, CORE.PBFPrintedBuildAMPart) not in g:
                                            g.add((part_name_uri_2, RDF.type, CORE.PBFPrintedBuildAMPart))
                                            part_name_uri = part_name_uri_2
                                            break
                                if get_support and get_support not in support_names:
                                    support_names.append(get_support)
                                    get_support_name = get_support.strip().replace(" ", "_")
                                    get_support_uri = URIRef(EX + get_support_name)
                                    get_support_uri_2 = URIRef(
                                        f"{EX}Printed_Build_Support_class/{get_support_name.replace(' ', '_')}")
                                    if (get_support_uri, RDF.type, CORE.PBFPrintedBuildSupport) not in g:
                                        if (get_support_uri_2, RDF.type, CORE.PBFPrintedBuildSupport) not in g:
                                            g.add((get_support_uri, RDF.type, CORE.PBFPrintedBuildSupport))
                                            break
                                    else:
                                        if (get_support_uri_2, RDF.type, CORE.PBFPrintedBuildSupport) not in g:
                                            g.add((get_support_uri_2, RDF.type, CORE.PBFPrintedBuildSupport))
                                            get_support_uri = get_support_uri_2
                                            break
                                    g.add((get_support_uri, CORE.isSupportFor, part_name_uri))
                        for i in part_names:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            g.add((uri, CORE.isComposedOf, i_uri))
                        for i in support_names:
                            i_name = i.strip().replace(" ", "_")
                            i_uri = URIRef(EX + i_name)
                            g.add((uri, CORE.isComposedOf, i_uri))
                    except: pass
                # ----------------------------------------------------------------------------------------------------------------
        # Ask user where to save the RDF output
        rdf_filename, _ = QFileDialog.getSaveFileName(self, "Save RDF Output", "", "RDF files (*.rdf)")
        if not rdf_filename:
            QMessageBox.warning(self, "No Save Location", "No save location was selected.")
            return
        # Ensure the file ends with .rdf
        if not rdf_filename.endswith(".rdf"):
            rdf_filename += ".rdf"
        # Serialize RDF graph
        g.serialize(rdf_filename, format="pretty-xml")
        QMessageBox.information(self, "Success", f"RDF file saved as '{rdf_filename}'")
    # =======================================================================
    def save_project_as_json(self):
        def deep_serialize(obj):
            if not isinstance(obj, list):
                obj = [obj]
            #------------------------------
            def serialize_item(item):
                if isinstance(item, list):
                    return [serialize_item(subitem) for subitem in item]
                elif isinstance(item, dict):
                    return {key: serialize_item(value) for key, value in item.items()}
                elif hasattr(item, '__dict__'):
                    return serialize_item(vars(item))
                elif isinstance(item, (str, int, float, bool)) or item is None:
                    return item
                else:
                    return str(item)
            #------------------------------
            return [serialize_item(item) for item in obj]

        filename, _ = QFileDialog.getSaveFileName(self, "Save As New Project", "", "JSON files (*.json)")
        if filename:
            self.current_project_path = filename
            if not filename.endswith(".json"):
                filename += ".json"
            output = filename.rsplit("/", 1)[-1]
            filename_name = output.replace(".json", "")
            dictionary2 = {}
            # Add all entries using deep serialization
            dictionary2["Sensor_class"] = deep_serialize(sensors_list)
            dictionary2["Printing_Machine_class"] = deep_serialize(defined_printing_machines)
            dictionary2["PBF_AM_Process_Chain_class"] = deep_serialize(PBF_AM_Process_Chain)
            dictionary2["Build_Model_Design_Process_class"] = deep_serialize(Build_Model_Design_Process_process)
            dictionary2["output_Build_Model_Design_Process_class"] = deep_serialize(build_model_parts)
            dictionary2["output_Build_Model_Design_Process_class"] = deep_serialize(Build_model)
            dictionary2["Machine_Powder_Feed_Control_Strategy_class"] = deep_serialize(machine_powder_strategy)
            dictionary2["Machine_Powder_Feed_Control_PPI_class"] = deep_serialize(machine_powder_strategy_PPI)
            dictionary2["Slicing_Process_class"] = deep_serialize(Slicing_process)
            dictionary2["Printing_Process_Instructions_class"] = deep_serialize(Printing_Process_Instructions_output)
            dictionary2["Layer_Of_Build_Model_class"] = deep_serialize(Layer_Of_Build_Models_Layer_decomposition)
            dictionary2["Beam_Control_Slicing_Strategy_class"] = deep_serialize(Beam_control_slicing_strategy)
            dictionary2["Start_Heating_PPI_class"] = deep_serialize(start_heating_PPIs_in_project)
            dictionary2["start_heating_strategies_in_project"] = deep_serialize(start_heating_strategies_in_project)
            dictionary2["Start_Heating_Strategy_class"] = deep_serialize(Layer_Pre_Heating_Strategies_list_used_in_project)
            dictionary2["Layer_Post_Heating_Strategy_class"] = deep_serialize(Layer_Post_Heating_Strategies_list_used_in_project)
            dictionary2["Layer_Pre_Heating_PPI_class"] = deep_serialize(Layer_Pre_Heating_PPI_list_used_in_project)
            dictionary2["Layer_Post_Heating_PPI_list_used_in_project"] = deep_serialize(Layer_Post_Heating_PPI_list_used_in_project)
            dictionary2["Layer_Post_Heating_PPI_class"] = deep_serialize(Layer_Post_Heating_PPI_list)
            dictionary2["Layer_Melting_Strategy_class"] = deep_serialize(Layer_Melting_Strategies_list_used_in_project)
            dictionary2["Layer_Melting_PPI_class"] = deep_serialize(Layer_Melting_PPI_list_used_in_project)
            dictionary2["Printing_Process_class"] = deep_serialize(Printing_Process)
            dictionary2["Printed_Build_class"] = deep_serialize(printed_build)
            dictionary2["Monitoring_Process_class"] = deep_serialize(Monitoring_Process)
            dictionary2["Post_Printing_Process_class"] = deep_serialize(Post_printing_Proces)
            dictionary2["Testing_Process_class"] = deep_serialize(Testing_Process)
            # ===========================shared lists========
            dictionary2["PBF_AM_Process_Chain_class"] = deep_serialize(PBF_AM_Process_Chains_list)
            dictionary2["Supervisor_class"] = deep_serialize(supervisors_list)
            dictionary2["Build_Model_Support_class"] = deep_serialize(Build_Model_Support_list)
            dictionary2["Build_Model_AM_Part_class"] = deep_serialize(Build_Model_AM_Part_list)
            dictionary2["output_Build_Model_Design_Process_class"] = deep_serialize(Defined_Build_models)
            dictionary2["Printing_Process_Instructions_class"] = deep_serialize(defined_Printing_Process_Instructions)
            dictionary2["Layer_Of_Build_Model_class"] = deep_serialize(Layer_Of_Build_Models_list)
            dictionary2["layer_of_Build_Model_AM_Part_class"] = deep_serialize(Layer_Of_Build_Model_AM_Parts_list)
            dictionary2["Machine_Powder_Feed_Control_Strategy_class"] = deep_serialize(Machine_Powder_Feed_Control_Strategies_list)
            dictionary2["Machine_Powder_Feed_Control_PPI_class"] = deep_serialize(Machine_Powder_Feed_Control_Strategy_PPIs_list)
            dictionary2["Scan_Strategy_class"] = deep_serialize(Scan_Strategies_list)
            dictionary2["Start_Heating_PPI_class"] = deep_serialize(Start_Heating_PPI_list)
            dictionary2["Start_Heating_Strategy_class"] = deep_serialize(Start_Heating_Strategy_list)
            dictionary2["AM_Part_Layer_Pre_Heating_Strategy_class"] = deep_serialize(AM_Part_Layer_Pre_Heating_Strategies_list)
            dictionary2["Layer_Pre_Heating_Strategy_class"] = deep_serialize(Layer_Pre_Heating_Strategies_list)
            dictionary2["AM_Part_Layer_Pre_Heating_PPI_class"] = deep_serialize(AM_Part_Layer_Pre_Heating_PPI_list)
            dictionary2["AM_Part_Layer_Post_Heating_Strategy_class"] = deep_serialize(AM_Part_Layer_Post_Heating_Strategies_list)
            dictionary2["Layer_Post_Heating_Strategy_class"] = deep_serialize(Layer_Post_Heating_Strategies_list)
            dictionary2["AM_Part_Layer_Post_Heating_PPI_class"] = deep_serialize(AM_Part_Layer_Post_Heating_PPI_list)
            dictionary2["Layer_Pre_Heating_PPI_class"] = deep_serialize(Layer_Pre_Heating_PPI_list)
            dictionary2["AM_Part_Layer_Melting_Strategy_class"] = deep_serialize(AM_Part_Layer_Melting_Strategies_list)
            dictionary2["Layer_Melting_Strategy_class"] = deep_serialize(Layer_Melting_Strategies_list)
            dictionary2["AM_Part_Layer_Melting_PPI_class"] = deep_serialize(AM_Part_Layer_Melting_PPI_list)
            dictionary2["Layer_Melting_PPI_class"] = deep_serialize(Layer_Melting_PPI_list)
            dictionary2["Material_class"] = deep_serialize(defined_Materials)
            dictionary2["Printing_Medium_class"] = deep_serialize(defined_Printing_mediums)
            dictionary2["Build_Plate_class"] = deep_serialize(defined_Build_Plates)
            dictionary2["Printing_Machine_class"] = deep_serialize(defined_printing_machines)
            dictionary2["Printed_Build_class"] = deep_serialize(printed_build_list)
            dictionary2["Printed_Build_AM_Part_class"] = deep_serialize(Printed_Build_AM_Parts_list)
            dictionary2["Printed_Build_Support_class"] = deep_serialize(Printed_Build_Supports_list)
            dictionary2["Post_Printing_MethodPost_Printing_Process_class"] = deep_serialize(Post_Printing_Methods_list)
            dictionary2["Testing_Method_class"] = deep_serialize(Testing_Methods_list)
            dictionary2["Sensor_class"] = deep_serialize(sensors_list)
            dictionary2["Manufacturer_class"] = deep_serialize(defined_Manufacturers)
            # Save to JSON
            try:
                with open(filename, 'w') as f:
                    json.dump(dictionary2, f, indent=4)
                QMessageBox.information(self, "Success", f"Project saved successfully as '{filename_name}'")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")
    # =======================================================================
    def save_changes_to_current_project(self):
        try:
            printer = Printing_Process.printing_process_printing_machine
            sensor_info = printer.printing_machine_sensor_info
            Monitoring_Process.monitoring_process_receives_data_from = sensor_info
        except:pass
        try:
            Monitoring_Process.monitoring_process_printing_process = Printing_Process
        except:pass
        try:
            index = next((i for i, cls in enumerate(PBF_AM_Process_Chains_list) if
                          cls.project_name == PBF_AM_Process_Chain.project_name), -1)
            if index == -1:
                QMessageBox.warning(self, "Warning",
                                    "Current project is not saved yet. Use 'Save As New Project' first.")
                return
            if not hasattr(self, 'current_project_path') or not self.current_project_path:
                QMessageBox.warning(self, "Warning", "No file path found for current project.")
                return
            index = next((i for i, cls in enumerate(PBF_AM_Process_Chains_list) if
                          cls.project_name == PBF_AM_Process_Chain.project_name), -1)
            if index != -1:
                PBF_AM_Process_Chains_list[index] = PBF_AM_Process_Chain
            try:
                Printing_Process_Instructions_output.ppi_machine_powder_feed = machine_powder_strategy_PPI
                Printing_Process_Instructions_output.ppi_start_heating_ppi = start_heating_PPIs_in_project
                Printing_Process_Instructions_output.ppi_layer_pre_heating_ppi = Layer_Pre_Heating_PPI_list_used_in_project
                Printing_Process_Instructions_output.ppi_layer_post_heating_ppi = Layer_Post_Heating_PPI_list_used_in_project
                Printing_Process_Instructions_output.ppi_layer_melting_heating_ppi = Layer_Melting_PPI_list_used_in_project
            except:pass
            try:
                Printing_Process.printing_process_output = printed_build
            except:pass
            try:
                machine_powder_strategy_PPI.Machine_powder_s_PPI_correspond_strategy = machine_powder_strategy
            except:pass
            try:
                Slicing_process.SlicingProcess_input = Build_model
            except:pass
            try:
                Slicing_process.SlicingProcess_output = Printing_Process_Instructions_output
            except:pass
            try:
                if start_heating_strategies_in_project:
                    Beam_control_slicing_strategy.beam_control_start_heating_strategy = start_heating_strategies_in_project
                if Layer_Pre_Heating_Strategies_list_used_in_project:
                    Beam_control_slicing_strategy.beam_control_pre_heating = Layer_Pre_Heating_Strategies_list_used_in_project
                if Layer_Post_Heating_Strategies_list_used_in_project:
                    Beam_control_slicing_strategy.beam_control_slic_strategy_post_heating = Layer_Post_Heating_Strategies_list_used_in_project
                if Layer_Melting_Strategies_list_used_in_project:
                    Beam_control_slicing_strategy.beam_control_slic_strategy_melting = Layer_Melting_Strategies_list_used_in_project
            except:pass
            if Testing_process_applied_testing_methods:
                Testing_Process.TestingProcess_testing_data = Testing_process_applied_testing_methods
                methods = []
                for i in Testing_process_applied_testing_methods:
                    methods.append(i.applied_testing_method_name)
                if methods:
                    Testing_Process.TestingProcess_testing_method = methods
            if printed_build:
                Testing_Process.TestingProcess_hasInputPrintedBuild = printed_build
            if printed_build.Printed_Build_AM_Parts_and_supports:
                parts = []
                supports = []
                for i in printed_build.Printed_Build_AM_Parts_and_supports:
                    match = re.search(r"Printed Build AM Part: (.*?)\s+Get Support: (.*)", i)
                    if match:
                        part_name = match.group(1)
                        if part_name:
                            parts.append(part_name)
                            get_support = match.group(2)
                            if get_support: supports.append(get_support)
                if parts: Testing_Process.TestingProcess_hasInputPrintedBuildAMPart = parts
                if supports:
                    Testing_Process.TestingProcess_hasInputPrintedBuildSupport = supports
            dictionary = {}
            # For project
            dictionary["PBF_AM_Process_Chain"] = PBF_AM_Process_Chain
            dictionary["Build_Model_Design_Process_process"] = Build_Model_Design_Process_process
            dictionary["build_model_parts"] = build_model_parts
            dictionary["build_model_support_for_part"] = build_model_support_for_part
            dictionary["Build_model"] = Build_model
            dictionary["Slicing_process"] = Slicing_process
            dictionary["Printing_Process_Instructions_output"] = Printing_Process_Instructions_output
            dictionary["Layer_Of_Build_Models_Layer_decomposition"] = Layer_Of_Build_Models_Layer_decomposition
            dictionary["Layer_Of_Build_Model_AM_Parts_Layer_decomposition"] = Layer_Of_Build_Model_AM_Parts_Layer_decomposition
            dictionary["machine_powder_strategy"] = machine_powder_strategy
            dictionary["machine_powder_strategy_PPI"] = machine_powder_strategy_PPI
            dictionary["Beam_control_slicing_strategy"] = Beam_control_slicing_strategy
            dictionary["start_heating_PPIs_in_project"] = start_heating_PPIs_in_project
            dictionary["start_heating_strategies_in_project"] = start_heating_strategies_in_project
            dictionary["Layer_Pre_Heating_Strategies_list_used_in_project"] = Layer_Pre_Heating_Strategies_list_used_in_project
            dictionary["Layer_Post_Heating_Strategies_list_used_in_project"] = Layer_Post_Heating_Strategies_list_used_in_project
            dictionary["Layer_Pre_Heating_PPI_list_used_in_project"] = Layer_Pre_Heating_PPI_list_used_in_project
            dictionary["Layer_Post_Heating_PPI_list_used_in_project"] = Layer_Post_Heating_PPI_list_used_in_project
            dictionary["Layer_Post_Heating_PPI_list"] = Layer_Post_Heating_PPI_list
            dictionary["Layer_Melting_Strategies_list_used_in_project"] = Layer_Melting_Strategies_list_used_in_project
            dictionary["Layer_Melting_PPI_list_used_in_project"] = Layer_Melting_PPI_list_used_in_project
            dictionary["Printing_Process"] = Printing_Process
            dictionary["printed_build"] = printed_build
            dictionary["Monitoring_Process"] = Monitoring_Process
            dictionary["Post_printing_Proces"] = Post_printing_Proces
            dictionary["Testing_Process"] = Testing_Process
            # General list
            self.save_shared_lists()
            with open(self.current_project_path, 'wb') as f:
                pickle.dump(dictionary, f)
            QMessageBox.information(self, "Success", f"Changes saved to '{self.current_project_path}'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save current project: {str(e)}")
    # =======================================================================
    def save_as_new_project(self):
        try:
            printer = Printing_Process.printing_process_printing_machine
            sensor_info = printer.printing_machine_sensor_info
            Monitoring_Process.monitoring_process_receives_data_from = sensor_info
        except:pass
        try:
            Monitoring_Process.monitoring_process_printing_process = Printing_Process
        except:pass
        try:
            PBF_AM_Process_Chains_list.append(PBF_AM_Process_Chain)
        except:pass
        try:
            Printing_Process_Instructions_output.ppi_machine_powder_feed = machine_powder_strategy_PPI
            Printing_Process_Instructions_output.ppi_start_heating_ppi = start_heating_PPIs_in_project
            Printing_Process_Instructions_output.ppi_layer_pre_heating_ppi = Layer_Pre_Heating_PPI_list_used_in_project
            Printing_Process_Instructions_output.ppi_layer_post_heating_ppi = Layer_Post_Heating_PPI_list_used_in_project
            Printing_Process_Instructions_output.ppi_layer_melting_heating_ppi = Layer_Melting_PPI_list_used_in_project
        except:pass
        try:
            machine_powder_strategy_PPI.Machine_powder_s_PPI_correspond_strategy = machine_powder_strategy
        except:pass
        try:
            Printing_Process.printing_process_output = printed_build
        except:pass
        try:
            Slicing_process.SlicingProcess_input = Build_model
        except:pass
        try:
            Slicing_process.SlicingProcess_output = Printing_Process_Instructions_output
        except:pass
        try:
            if Testing_process_applied_testing_methods:
                Testing_Process.TestingProcess_testing_data = Testing_process_applied_testing_methods
                methods = []
                for i in Testing_process_applied_testing_methods:
                    methods.append(i.applied_testing_method_name)
                if methods:
                    Testing_Process.TestingProcess_testing_method = methods
            if printed_build:
                Testing_Process.TestingProcess_hasInputPrintedBuild = printed_build
            if printed_build.Printed_Build_AM_Parts_and_supports:
                parts = []
                supports = []
                for i in printed_build.Printed_Build_AM_Parts_and_supports:
                    match = re.search(r"Printed Build AM Part: (.*?)\s+Get Support: (.*)", i)
                    if match:
                        part_name = match.group(1)
                        if part_name:
                            parts.append(part_name)
                            get_support = match.group(2)
                            if get_support: supports.append(get_support)
                if parts: Testing_Process.TestingProcess_hasInputPrintedBuildAMPart = parts
                if supports:
                    Testing_Process.TestingProcess_hasInputPrintedBuildSupport = supports
        except:pass
        try:
            if start_heating_strategies_in_project:
                Beam_control_slicing_strategy.beam_control_start_heating_strategy = start_heating_strategies_in_project
            if Layer_Pre_Heating_Strategies_list_used_in_project:
                Beam_control_slicing_strategy.beam_control_pre_heating = Layer_Pre_Heating_Strategies_list_used_in_project
            if Layer_Post_Heating_Strategies_list_used_in_project:
                Beam_control_slicing_strategy.beam_control_slic_strategy_post_heating = Layer_Post_Heating_Strategies_list_used_in_project
            if Layer_Melting_Strategies_list_used_in_project:
                Beam_control_slicing_strategy.beam_control_slic_strategy_melting = Layer_Melting_Strategies_list_used_in_project
        except:
            pass
        filename, _ = QFileDialog.getSaveFileName(self, "Save As New Project", "", "PICKLE files (*.pkl)")
        if filename:
            self.current_project_path = filename
            if not filename.endswith(".pkl"):
                filename += ".pkl"
            output = filename.rsplit("/", 1)[-1]
            filename_name = output.replace(".pkl", "")
            dictionary = {}
            dictionary["PBF_AM_Process_Chain"] = PBF_AM_Process_Chain
            dictionary["Build_Model_Design_Process_process"] = Build_Model_Design_Process_process
            dictionary["build_model_parts"] = build_model_parts
            dictionary["build_model_support_for_part"] = build_model_support_for_part
            dictionary["Build_model"] = Build_model
            dictionary["Slicing_process"] = Slicing_process
            dictionary["Printing_Process_Instructions_output"] = Printing_Process_Instructions_output
            dictionary["Layer_Of_Build_Models_Layer_decomposition"] = Layer_Of_Build_Models_Layer_decomposition
            dictionary[ "Layer_Of_Build_Model_AM_Parts_Layer_decomposition"] = Layer_Of_Build_Model_AM_Parts_Layer_decomposition
            dictionary["machine_powder_strategy"] = machine_powder_strategy
            dictionary["machine_powder_strategy_PPI"] = machine_powder_strategy_PPI
            dictionary["Beam_control_slicing_strategy"] = Beam_control_slicing_strategy
            dictionary["start_heating_PPIs_in_project"] = start_heating_PPIs_in_project
            dictionary["start_heating_strategies_in_project"] = start_heating_strategies_in_project
            dictionary["Layer_Pre_Heating_Strategies_list_used_in_project"] = Layer_Pre_Heating_Strategies_list_used_in_project
            dictionary["Layer_Post_Heating_Strategies_list_used_in_project"] = Layer_Post_Heating_Strategies_list_used_in_project
            dictionary["Layer_Pre_Heating_PPI_list_used_in_project"] = Layer_Pre_Heating_PPI_list_used_in_project
            dictionary["Layer_Post_Heating_PPI_list_used_in_project"] = Layer_Post_Heating_PPI_list_used_in_project
            dictionary["Layer_Post_Heating_PPI_list"] = Layer_Post_Heating_PPI_list
            dictionary["Layer_Melting_Strategies_list_used_in_project"] = Layer_Melting_Strategies_list_used_in_project
            dictionary["Layer_Melting_PPI_list_used_in_project"] = Layer_Melting_PPI_list_used_in_project
            dictionary["Printing_Process"] = Printing_Process
            dictionary["printed_build"] = printed_build
            dictionary["Monitoring_Process"] = Monitoring_Process
            dictionary["Post_printing_Proces"] = Post_printing_Proces
            dictionary["Testing_Process"] = Testing_Process
            self.save_shared_lists()
            try:
                with open(filename, 'wb') as f:
                    pickle.dump(dictionary, f)
                QMessageBox.information(self, "Success", f"Project saved successfully as '{filename_name}'")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")
    # =======================================================================
    def defined_printed_build_AM_part_listWidget_menu(self, position):
        list_widget = self.ui.defined_printed_build_AM_part_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Printed_Build_AM_Parts_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Printed_Build_AM_Parts_list = [s for s in Printed_Build_AM_Parts_list if
                                                   s.Printed_Build_AM_Part_name != item_text]
                    self.remove_combobox_item_by_text(self.ui.printed_build_PB_AM_part_comboBox, item_text)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Printed_Build_AM_Parts_list) if
                              cls.Printed_Build_AM_Part_name == item_text), -1)
                self.ui.printed_build_AM_part_name.setPlainText(
                    Printed_Build_AM_Parts_list[index].Printed_Build_AM_Part_name)
                self.ui.printed_build_AM_part_comment.setPlainText(
                    Printed_Build_AM_Parts_list[index].Printed_Build_AM_Part_comment)
                Printed_Build_AM_Parts_list = [m for m in Printed_Build_AM_Parts_list if
                                               m.Printed_Build_AM_Part_name != item_text]
                self.remove_combobox_item_by_text(self.ui.printed_build_PB_AM_part_comboBox, item_text)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_printed_build_support_listWidget_menu(self, position):
        list_widget = self.ui.defined_printed_build_support_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Printed_Build_Supports_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Printed_Build_Supports_list = [s for s in Printed_Build_Supports_list if
                                                   s.Printed_Build_Support_name != item_text]
                    self.remove_combobox_item_by_text(self.ui.printed_build_PB_AM_part_support_comboBox, item_text)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Printed_Build_Supports_list) if
                              cls.Printed_Build_Support_name == item_text), -1)
                self.ui.printed_build_support_name.setPlainText(
                    Printed_Build_Supports_list[index].Printed_Build_Support_name)
                self.ui.printed_build_support_comment.setPlainText(
                    Printed_Build_Supports_list[index].Printed_Build_Support_comment)
                Printed_Build_Supports_list = [m for m in Printed_Build_Supports_list if
                                               m.Printed_Build_Support_name != item_text]
                self.remove_combobox_item_by_text(self.ui.printed_build_PB_AM_part_support_comboBox, item_text)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_Printed_Builds_listWidget_menu(self, position):
        list_widget = self.ui.defined_Printed_Builds_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("View and Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global printed_build_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    printed_build_list = [s for s in printed_build_list if s.Printed_Build_name != item_text]
                    index = self.ui.printing_process_output_printe_build.findText(item_text)
                    if index != -1: self.ui.printing_process_output_printe_build.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(printed_build_list) if cls.Printed_Build_name == item_text), -1)
                self.ui.printed_build_name.setPlainText(printed_build_list[index].Printed_Build_name)
                self.ui.printed_build_comment.setPlainText(printed_build_list[index].Printed_Build_comment)
                for item in printed_build_list[index].Printed_Build_AM_Parts_and_supports:
                    self.ui.composed_of_printed_build_PB_AM_partlistWidget.addItem(item)
                printed_build_list = [m for m in printed_build_list if m.Printed_Build_name != item_text]
                index = self.ui.printing_process_output_printe_build.findText(item_text)
                if index != -1: self.ui.printing_process_output_printe_build.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_printing_machines_listWidget_menu(self, position):
        list_widget = self.ui.defined_printing_machines_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global defined_printing_machines
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    defined_printing_machines = [s for s in defined_printing_machines if
                                                 s.printing_machine_name != item_text]
                    self.remove_combobox_item_by_text(self.ui.printing_process_printing_machine, item_text)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(defined_printing_machines) if cls.printing_machine_name == item_text),
                    -1)
                self.ui.printing_machine_name.setPlainText(defined_printing_machines[index].printing_machine_name)
                self.ui.printing_machine_comment.setPlainText(defined_printing_machines[index].printing_machine_comment)
                for sensor in defined_printing_machines[index].printing_machine_sensor_info:
                    self.ui.defined_sensors_listWidget.addItem(sensor)
                if defined_printing_machines[index].printing_machine_brand == 'EB-PBF Freemelt':
                    self.ui.eb_pbf_freemelt_checkBox.setChecked(True)
                defined_printing_machines = [m for m in defined_printing_machines if
                                             m.printing_machine_name != item_text]
                self.remove_combobox_item_by_text(self.ui.printing_process_printing_machine, item_text)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def remove_combobox_item_by_text(self, combo_box, target_text):
        for i in range(combo_box.count()):
            if combo_box.itemText(i) == target_text:
                combo_box.removeItem(i)
                break
    # =======================================================================
    def defined_printing_medium_listWidget_menu(self, position):
        list_widget = self.ui.defined_printing_medium_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global defined_Printing_mediums
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    defined_Printing_mediums = [s for s in defined_Printing_mediums if
                                                s.printing_medium_name != item_text]
                    index = self.ui.printing_process_printing_medium.findText(item_text)
                    if index != -1: self.ui.printing_process_printing_medium.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(defined_Printing_mediums) if cls.printing_medium_name == item_text), -1)
                self.ui.printing_medium_name.setPlainText(defined_Printing_mediums[index].printing_medium_name)
                self.ui.printing_medium_status.setPlainText(defined_Printing_mediums[index].printing_medium_status)
                if defined_Printing_mediums[index].printing_medium_type == 'Metal Powder':
                    self.ui.metal_powder_checkBox.setChecked(True)
                self.ui.printing_medium_material_comboBox.setCurrentText(
                    defined_Printing_mediums[index].printing_medium_material)
                self.ui.printing_medium_particle_size.setPlainText(
                    defined_Printing_mediums[index].printing_medium_particle_size)
                self.ui.printing_medium_particle_morphology.setPlainText(
                    defined_Printing_mediums[index].printing_medium_powder_morphology)
                self.ui.printing_medium_manufacturer_comboBox.setCurrentText(
                    defined_Printing_mediums[index].printing_medium_manufacturer)
                self.ui.printing_medium_comment.setPlainText(defined_Printing_mediums[index].printing_medium_comment)
                defined_Printing_mediums = [m for m in defined_Printing_mediums if m.printing_medium_name != item_text]
                index = self.ui.printing_process_printing_medium.findText(item_text)
                if index != -1: self.ui.printing_process_printing_medium.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def existing_sensors_listWidget_menu(self, position):
        list_widget = self.ui.existing_sensors_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        global sensors_list
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    sensors_list = [s for s in sensors_list if s.sensor_name != item_text]
                index = self.ui.load_sensor_comboBox.findText(item_text)
                if index != -1: self.ui.load_sensor_comboBox.removeItem(index)
                for i in range(self.ui.defined_sensors_listWidget.count()):
                    if self.ui.defined_sensors_listWidget.item(i).text() == item_text:
                        removed = self.ui.defined_sensors_listWidget.takeItem(i)
                        del removed
                        break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(sensors_list) if cls.sensor_name == item_text), -1)
                self.ui.sensor_name.setPlainText(sensors_list[index].sensor_name)
                self.ui.sensor_type.setPlainText(sensors_list[index].sensor_type)
                self.ui.sensor_recorde_data_path.setPlainText(sensors_list[index].recorded_data_path)
                sensors_list = [m for m in sensors_list if m.sensor_name != item_text]
                index = self.ui.load_sensor_comboBox.findText(item_text)
                if index != -1: self.ui.load_sensor_comboBox.removeItem(index)
                for i in range(self.ui.defined_sensors_listWidget.count()):
                    if self.ui.defined_sensors_listWidget.item(i).text() == item_text:
                        removed = self.ui.defined_sensors_listWidget.takeItem(i)
                        del removed
                        break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_sensors_listWidget_menu(self, position):
        list_widget = self.ui.defined_sensors_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_build_plate_listWidget_menu(self, position):
        list_widget = self.ui.defined_build_plate_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global defined_Build_Plates
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    defined_Build_Plates = [s for s in defined_Build_Plates if s.build_plate_name != item_text]
                    index = self.ui.printing_process_buildplate.findText(item_text)
                    if index != -1: self.ui.printing_process_buildplate.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(defined_Build_Plates) if cls.build_plate_name == item_text), -1)
                self.ui.build_plate_name.setPlainText(defined_Build_Plates[index].build_plate_name)
                self.ui.build_plate_size.setPlainText(defined_Build_Plates[index].build_plate_size)
                self.ui.build_plate_thickness.setPlainText(defined_Build_Plates[index].build_plate_thickness)
                self.ui.build_plate_surface_texture.setPlainText(
                    defined_Build_Plates[index].build_plate_surface_texture)
                self.ui.build_plate_shape.setPlainText(defined_Build_Plates[index].build_plate_shape)
                self.ui.build_plate_manufacturer_comboBox.setCurrentText(
                    defined_Build_Plates[index].build_plate_manufacturer)
                self.ui.build_plate_material_comboBox.setCurrentText(defined_Build_Plates[index].build_plate_material)
                self.ui.build_plate_comment.setPlainText(defined_Build_Plates[index].build_plate_comment)
                defined_Build_Plates = [m for m in defined_Build_Plates if m.build_plate_name != item_text]
                index = self.ui.printing_process_buildplate.findText(item_text)
                if index != -1: self.ui.printing_process_buildplate.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_defined_AM_part_layer_melting_strategy_ppi_listwidget_menu(self, position):
        list_widget = self.ui.list_defined_AM_part_layer_melting_strategy_ppi_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global AM_Part_Layer_Melting_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    AM_Part_Layer_Melting_PPI_list = [s for s in AM_Part_Layer_Melting_PPI_list if
                                                      s.AM_part_melting_ppi_name != item_text]
                    index = self.ui.composed_of_am_part_melting_ppi_combobox.findText(item_text)
                    if index != -1: self.ui.composed_of_am_part_melting_ppi_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(AM_Part_Layer_Melting_PPI_list) if
                              cls.AM_part_melting_ppi_name == item_text), -1)
                self.ui.am_part_layer_melting_ppi_name.setPlainText(
                    AM_Part_Layer_Melting_PPI_list[index].AM_part_melting_ppi_name)
                self.ui.am_part_layer_melting_ppi_related_am_part_comboBox_2.setCurrentText(
                    AM_Part_Layer_Melting_PPI_list[index].AM_part_melting_ppi_related_am_part)
                self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.setCurrentText(
                    AM_Part_Layer_Melting_PPI_list[index].AM_part_melting_ppi_correspond_AM_part_melting_strategy)
                self.ui.am_part_layer_melting_ppi_file.setPlainText(
                    AM_Part_Layer_Melting_PPI_list[index].AM_part_melting_ppi_file)
                self.ui.correspond_layer_build_model_am_part_conbobox_2.setCurrentText(
                    AM_Part_Layer_Melting_PPI_list[index].AM_part_melting_ppi_correspond_layer_build_model)
                self.ui.am_part_layer_melting_ppi_file_format.setPlainText(
                    AM_Part_Layer_Melting_PPI_list[index].AM_part_melting_ppi_file_format)
                self.ui.am_part_layer_melting_ppi_comment.setPlainText(
                    AM_Part_Layer_Melting_PPI_list[index].AM_part_melting_ppi_comment)
                AM_Part_Layer_Melting_PPI_list = [m for m in AM_Part_Layer_Melting_PPI_list if
                                                  m.AM_part_melting_ppi_name != item_text]
                index = self.ui.composed_of_am_part_melting_ppi_combobox.findText(item_text)
                if index != -1: self.ui.composed_of_am_part_melting_ppi_combobox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_defined_AM_part_layer_post_heating_strategy_ppi_listwidget_menu(self, position):
        list_widget = self.ui.list_defined_AM_part_layer_post_heating_strategy_ppi_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global AM_Part_Layer_Post_Heating_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    AM_Part_Layer_Post_Heating_PPI_list = [s for s in AM_Part_Layer_Post_Heating_PPI_list if
                                                           s.AM_part_post_heat_ppi_name != item_text]
                    index = self.ui.composed_of_am_part_post_heating_ppi_combobox.findText(item_text)
                    if index != -1: self.ui.composed_of_am_part_post_heating_ppi_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(AM_Part_Layer_Post_Heating_PPI_list) if
                              cls.AM_part_post_heat_ppi_name == item_text), -1)
                self.ui.am_part_layer_post_heating_ppi_name.setPlainText(
                    AM_Part_Layer_Post_Heating_PPI_list[index].AM_part_post_heat_ppi_name)
                self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.setCurrentText(
                    AM_Part_Layer_Post_Heating_PPI_list[index].AM_part_post_heat_ppi_related_am_part)
                self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.setCurrentText(
                    AM_Part_Layer_Post_Heating_PPI_list[
                        index].AM_part_post_heat_ppi_correspond_AM_part_post_heat_strategy)
                self.ui.am_part_layer_post_heating_ppi_file.setPlainText(
                    AM_Part_Layer_Post_Heating_PPI_list[index].AM_part_post_heat_ppi_file)
                self.ui.correspond_layer_build_model_am_part_conbobox.setCurrentText(
                    AM_Part_Layer_Post_Heating_PPI_list[index].AM_part_post_heat_ppi_correspond_layer_build_model)
                self.ui.am_part_layer_post_heating_ppi_file_format.setPlainText(
                    AM_Part_Layer_Post_Heating_PPI_list[index].AM_part_post_heat_ppi_file_format)
                self.ui.am_part_layer_post_heating_ppi_comment.setPlainText(
                    AM_Part_Layer_Post_Heating_PPI_list[index].AM_part_post_heat_ppi_comment)
                AM_Part_Layer_Post_Heating_PPI_list = [m for m in AM_Part_Layer_Post_Heating_PPI_list if
                                                       m.AM_part_post_heat_ppi_name != item_text]
                index = self.ui.composed_of_am_part_post_heating_ppi_combobox.findText(item_text)
                if index != -1: self.ui.composed_of_am_part_post_heating_ppi_combobox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_defined_AM_part_layer_pre_heating_strategy_ppi_listwidget_menu(self, position):
        list_widget = self.ui.list_defined_AM_part_layer_pre_heating_strategy_ppi_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global AM_Part_Layer_Pre_Heating_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    AM_Part_Layer_Pre_Heating_PPI_list = [s for s in AM_Part_Layer_Pre_Heating_PPI_list if
                                                          s.AM_part_pre_heat_ppi_name != item_text]
                    index = self.ui.composed_of_am_part_pre_heating_ppi_combobox.findText(item_text)
                    if index != -1: self.ui.composed_of_am_part_pre_heating_ppi_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(AM_Part_Layer_Pre_Heating_PPI_list) if
                              cls.AM_part_pre_heat_ppi_name == item_text), -1)
                self.ui.am_part_layer_pre_heating_ppi_name.setPlainText(
                    AM_Part_Layer_Pre_Heating_PPI_list[index].AM_part_pre_heat_ppi_name)
                self.ui.am_part_layer_pre_heating_ppi_related_am_part_comboBox.setCurrentText(
                    AM_Part_Layer_Pre_Heating_PPI_list[index].AM_part_pre_heat_ppi_related_am_part)
                self.ui.correspond_am_part_layer_pre_heating.setCurrentText(
                    AM_Part_Layer_Pre_Heating_PPI_list[index].AM_part_pre_heat_ppi_correspond_AM_part_pre_heat_strategy)
                self.ui.am_part_layer_pre_heating_ppi_file.setPlainText(
                    AM_Part_Layer_Pre_Heating_PPI_list[index].AM_part_pre_heat_ppi_file)
                self.ui.am_part_layer_pre_heating_ppi_correspond_am_part.setCurrentText(
                    AM_Part_Layer_Pre_Heating_PPI_list[index].AM_part_pre_heat_ppi_correspond_layer_build_model)
                self.ui.am_part_layer_pre_heating_ppi_file_format.setPlainText(
                    AM_Part_Layer_Pre_Heating_PPI_list[index].AM_part_pre_heat_ppi_file_format)
                self.ui.am_part_layer_pre_heating_ppi_comment.setPlainText(
                    AM_Part_Layer_Pre_Heating_PPI_list[index].AM_part_pre_heat_ppi_comment)
                AM_Part_Layer_Pre_Heating_PPI_list = [m for m in AM_Part_Layer_Pre_Heating_PPI_list if
                                                      m.AM_part_pre_heat_ppi_name != item_text]
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================.
    def list_defined_A_part_layer_melting_strategy_listwidget_menu(self, position):
        list_widget = self.ui.list_defined_A_part_layer_melting_strategy_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global AM_Part_Layer_Melting_Strategies_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    AM_Part_Layer_Melting_Strategies_list = [s for s in AM_Part_Layer_Melting_Strategies_list if
                                                             s.AM_part_melting_strategy_name != item_text]
                    index = self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.findText(item_text)
                    if index != -1: self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.removeItem(index)
                    index = self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.findText(item_text)
                    if index != -1: self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.removeItem(
                        index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(AM_Part_Layer_Melting_Strategies_list) if
                              cls.AM_part_melting_strategy_name == item_text), -1)
                self.ui.am_part_layer_melting_strategy_point_distance.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_point_distance)
                self.ui.am_part_layer_melting_strategy_energy_density.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_energy_density)
                self.ui.am_part_layer_melting_strategy_offset_margin.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_offset_margin)
                self.ui.am_part_layer_melting_strategy_name.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_name)
                self.ui.am_part_layer_melting_strategy_scan_strategy.setCurrentText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_scan_strategy)
                self.ui.am_part_layer_melting_strategy_file.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_file)
                self.ui.am_part_layer_melting_strategy_rotation_angle.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_rotation_angle)
                self.ui.am_part_layer_melting_strategy_file_format.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_file_format)
                self.ui.am_part_layer_melting_strategy_number_repetitions.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_number_repetitions)
                self.ui.am_part_layer_melting_strategy_number_comment.setPlainText(
                    AM_Part_Layer_Melting_Strategies_list[index].AM_part_melting_strategy_comment)
                AM_Part_Layer_Melting_Strategies_list = [m for m in AM_Part_Layer_Melting_Strategies_list if
                                                         m.AM_part_melting_strategy_name != item_text]
                index = self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.findText(item_text)
                if index != -1: self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.removeItem(index)
                index = self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.findText(item_text)
                if index != -1: self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================.
    def list_defined_A_part_layer_post_heating_strategy_listwidget_menu(self, position):
        list_widget = self.ui.list_defined_A_part_layer_post_heating_strategy_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global AM_Part_Layer_Post_Heating_Strategies_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    AM_Part_Layer_Post_Heating_Strategies_list = [s for s in AM_Part_Layer_Post_Heating_Strategies_list
                                                                  if s.AM_part_post_heat_strategy_name != item_text]
                    index = self.ui.layer_post_heating_strategy_combobox.findText(item_text)
                    if index != -1: self.ui.layer_post_heating_strategy_combobox.removeItem(index)
                    index = self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.findText(item_text)
                    if index != -1: self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(AM_Part_Layer_Post_Heating_Strategies_list) if
                              cls.AM_part_post_heat_strategy_name == item_text), -1)
                self.ui.am_part_layer_post_heating_strategy_name.setPlainText(
                    AM_Part_Layer_Post_Heating_Strategies_list[index].AM_part_post_heat_strategy_name)
                self.ui.am_part_layer_post_heating_strategy_scan_strategy.setCurrentText(
                    AM_Part_Layer_Post_Heating_Strategies_list[index].AM_part_post_heat_strategy_scan_strategy)
                self.ui.am_part_layer_post_heating_strategy_file.setPlainText(
                    AM_Part_Layer_Post_Heating_Strategies_list[index].AM_part_post_heat_strategy_file)
                self.ui.am_part_layer_post_heating_strategy_rotation_angle.setPlainText(
                    AM_Part_Layer_Post_Heating_Strategies_list[index].AM_part_post_heat_strategy_rotation_angle)
                self.ui.am_part_layer_post_heating_strategy_file_format.setPlainText(
                    AM_Part_Layer_Post_Heating_Strategies_list[index].AM_part_post_heat_strategy_file_format)
                self.ui.am_part_layer_post_heating_strategy_number_repetitions.setPlainText(
                    AM_Part_Layer_Post_Heating_Strategies_list[index].AM_part_post_heat_strategy_number_repetitions)
                self.ui.am_part_layer_post_heating_strategy_number_comment.setPlainText(
                    AM_Part_Layer_Post_Heating_Strategies_list[index].AM_part_post_heat_strategy_number_comment)
                AM_Part_Layer_Post_Heating_Strategies_list = [m for m in AM_Part_Layer_Post_Heating_Strategies_list if
                                                              m.AM_part_post_heat_strategy_name != item_text]
                index = self.ui.layer_post_heating_strategy_combobox.findText(item_text)
                if index != -1: self.ui.layer_post_heating_strategy_combobox.removeItem(index)
                index = self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.findText(item_text)
                if index != -1: self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_defined_A_part_layer_pre_heating_strategy_listwidget_menu(self, position):
        list_widget = self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global AM_Part_Layer_Pre_Heating_Strategies_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    AM_Part_Layer_Pre_Heating_Strategies_list = [s for s in AM_Part_Layer_Pre_Heating_Strategies_list if
                                                                 s.AM_part_pre_heat_strategy_name != item_text]
                    index = self.ui.composed_of_am_part_pre_startegies_combobox.findText(item_text)
                    if index != -1: self.ui.composed_of_am_part_pre_startegies_combobox.removeItem(index)
                    index = self.ui.correspond_am_part_layer_pre_heating.findText(item_text)
                    if index != -1: self.ui.correspond_am_part_layer_pre_heating.removeItem(index)
                    for i in range(self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.count()):
                        if self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.item(
                                i).text() == item_text:
                            removed = self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.takeItem(i)
                            del removed
                            break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(AM_Part_Layer_Pre_Heating_Strategies_list) if
                              cls.AM_part_pre_heat_strategy_name == item_text), -1)
                self.ui.am_part_layer_pre_heating_strategy_name.setPlainText(
                    AM_Part_Layer_Pre_Heating_Strategies_list[index].AM_part_pre_heat_strategy_name)
                self.ui.am_part_layer_pre_heating_strategy_scan_startegy.setCurrentText(
                    AM_Part_Layer_Pre_Heating_Strategies_list[index].AM_part_pre_heat_strategy_scan_strategy)
                self.ui.am_part_layer_pre_heating_strategy_file.setPlainText(
                    AM_Part_Layer_Pre_Heating_Strategies_list[index].AM_part_pre_heat_strategy_file)
                self.ui.am_part_layer_pre_heating_strategy_rotation_angle.setPlainText(
                    AM_Part_Layer_Pre_Heating_Strategies_list[index].AM_part_pre_heat_strategy_rotation_angle)
                self.ui.am_part_layer_pre_heating_strategy_file_format.setPlainText(
                    AM_Part_Layer_Pre_Heating_Strategies_list[index].AM_part_pre_heat_strategy_file_format)
                self.ui.am_part_layer_pre_heating_strategy_number_repetitions.setPlainText(
                    AM_Part_Layer_Pre_Heating_Strategies_list[index].AM_part_pre_heat_strategy_number_repetitions)
                self.ui.am_part_layer_pre_heating_strategy_number_comment.setPlainText(
                    AM_Part_Layer_Pre_Heating_Strategies_list[index].AM_part_pre_heat_strategy_number_comment)
                AM_Part_Layer_Pre_Heating_Strategies_list = [m for m in AM_Part_Layer_Pre_Heating_Strategies_list if
                                                             m.AM_part_pre_heat_strategy_name != item_text]
                index = self.ui.composed_of_am_part_pre_startegies_combobox.findText(item_text)
                if index != -1: self.ui.composed_of_am_part_pre_startegies_combobox.removeItem(index)
                index = self.ui.correspond_am_part_layer_pre_heating.findText(item_text)
                if index != -1: self.ui.correspond_am_part_layer_pre_heating.removeItem(index)
                for i in range(self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.count()):
                    if self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.item(i).text() == item_text:
                        removed = self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.takeItem(i)
                        del removed
                        break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_of_layer_melting_strategy_used_in_beam_control_listwidget_menu(self, position):
        list_widget = self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Melting_Strategies_list, Layer_Melting_Strategies_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Melting_Strategies_list_used_in_project = [s for s in
                                                                     Layer_Melting_Strategies_list_used_in_project if
                                                                     s.melting_strategy_name != item_text]
                    index = self.ui.correspond_layer_melting_strategy_combobox.findText(item_text)
                    if index != -1: self.ui.correspond_layer_melting_strategy_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_layer_post_heating_in_beam_control_listWidget_menu(self, position):
        list_widget = self.ui.list_layer_post_heating_in_beam_control_listWidget
        item = list_widget.itemAt(position)
        if item is None: return  # No item under cursor
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Post_Heating_Strategies_list, Layer_Post_Heating_Strategies_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Post_Heating_Strategies_list_used_in_project = [s for s in
                                                                          Layer_Post_Heating_Strategies_list_used_in_project
                                                                          if s.post_heat_strategy_name != item_text]
                    index = self.ui.correspond_layer_post_heating_combobox.findText(item_text)
                    if index != -1: self.ui.correspond_layer_post_heating_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_layer_pre_heating_in_beam_control_listWidget_menu(self, position):
        list_widget = self.ui.list_layer_pre_heating_in_beam_control_listWidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Pre_Heating_Strategies_list, Layer_Pre_Heating_Strategies_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Pre_Heating_Strategies_list_used_in_project = [s for s in
                                                                         Layer_Pre_Heating_Strategies_list_used_in_project
                                                                         if s.pre_heat_strategy_name != item_text]
                    index = self.ui.correspond_to_layer_pre_heating_combobox.findText(item_text)
                    if index != -1: self.ui.correspond_to_layer_pre_heating_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_melting_ppi_listWidget_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_melting_ppi_listWidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_post_heating_ppi_listWidget_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Post_Heating_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_melting_strategy_listWidget_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_melting_strategy_listWidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Pre_Heating_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_post_heating_strategy_listWidget_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Pre_Heating_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_pre_heating_strategy_listWidget_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_pre_heating_strategy_listWidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Pre_Heating_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_pre_heating_ppi_listWidget_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Pre_Heating_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def layer_melting_ppi_used_beam_control_listwidget_menu(self, position):
        list_widget = self.ui.layer_melting_ppi_used_beam_control_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Melting_PPI_list, Layer_Melting_PPI_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Melting_PPI_list_used_in_project = [s for s in Layer_Melting_PPI_list_used_in_project if
                                                              s.melting_ppi_name != item_text]
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def layer_post_heating_ppi_used_beam_control_listwidget_menu(self, position):
        list_widget = self.ui.layer_post_heating_ppi_used_beam_control_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Post_Heating_PPI_list, Layer_Post_Heating_PPI_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Post_Heating_PPI_list_used_in_project = [s for s in
                                                                   Layer_Post_Heating_PPI_list_used_in_project if
                                                                   s.post_heat_ppi_name != item_text]
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(Layer_Post_Heating_PPI_list) if cls.post_heat_ppi_name == item_text), -1)
                self.ui.layer_post_heating_ppi_name.setPlainText(Layer_Post_Heating_PPI_list[index].post_heat_ppi_name)
                self.ui.layer_post_heating_ppi_file.setPlainText(Layer_Post_Heating_PPI_list[index].post_heat_ppi_file)
                self.ui.correspond_layer_build_model_combobox.setCurrentText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_corrspond_layer_build_model)
                self.ui.layer_post_heating_ppi_layer_number.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_layer_num)
                self.ui.layer_post_heating_ppi_file_format.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_file_format)
                self.ui.correspond_layer_post_heating_combobox.setCurrentText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_correspond_post_heating_strategy)
                self.ui.layer_post_heating_ppi_comment.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_comment)
                self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.clear()
                try:
                    for item_text in Layer_Post_Heating_PPI_list[index].post_heat_ppi_composed_AM_part_Layer_post_heat_ppi:
                        self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.addItem(item_text)
                except:pass
                Layer_Post_Heating_PPI_list = [s for s in Layer_Post_Heating_PPI_list if
                                               s.post_heat_ppi_name != item_text]
                Layer_Post_Heating_PPI_list_used_in_project = [s for s in Layer_Post_Heating_PPI_list_used_in_project if
                                                               s.post_heat_ppi_name != item_text]
                for i in range(self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget_2.count()):
                    if self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget_2.item(i).text() == item_text:
                        removed = self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget_2.takeItem(i)
                        del removed
                        break
                self.ui.load_an_existing_layer_post_heating_ppi_checkBox.setChecked(False)
                index = self.ui.load_an_existing_layer_post_heating_ppi_combobox.findText(item_text)
                if index != -1: self.ui.load_an_existing_layer_post_heating_ppi_combobox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_pre_heating_ppi_in_beam_control_menu(self, position):
        list_widget = self.ui.list_pre_heating_ppi_in_beam_control
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Pre_Heating_PPI_list, Layer_Pre_Heating_PPI_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Pre_Heating_PPI_list_used_in_project = [s for s in Layer_Pre_Heating_PPI_list_used_in_project
                                                                  if s.pre_heat_ppi_name != item_text]
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(Layer_Pre_Heating_PPI_list) if cls.pre_heat_ppi_name == item_text), -1)
                self.ui.layer_pre_heating_ppi_name.setPlainText(Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_name)
                self.ui.layer_pre_heating_ppi_file.setPlainText(Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_file)
                self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox.setCurrentText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_corrspond_layer_build_model)
                self.ui.layer_pre_heating_ppi_layer_number.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_layer_num)
                self.ui.layer_pre_heating_ppi_file_format.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_file_format)
                self.ui.correspond_to_layer_pre_heating_combobox.setCurrentText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_correspond_pre_heating_strategy)
                self.ui.layer_pre_heating_ppi_comment.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_comment)
                self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.clear()
                try:
                    for item_text in Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi:
                        self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.addItem(item_text)
                except:
                    pass
                Layer_Pre_Heating_PPI_list = [s for s in Layer_Pre_Heating_PPI_list if s.pre_heat_ppi_name != item_text]
                Layer_Pre_Heating_PPI_list_used_in_project = [s for s in Layer_Pre_Heating_PPI_list_used_in_project if
                                                              s.pre_heat_ppi_name != item_text]

                for i in range(self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget_2.count()):
                    if self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget_2.item(i).text() == item_text:
                        removed = self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget_2.takeItem(i)
                        del removed
                        break
                self.ui.load_an_existing_layer_pr_heating_ppi_checkBox.setChecked(False)
                index = self.ui.load_an_existing_layer_pr_heating_ppi_combobox.findText(item_text)
                if index != -1: self.ui.load_an_existing_layer_pr_heating_ppi_combobox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_melting_ppi_listWidget_2_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_melting_ppi_listWidget_2
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Melting_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Melting_PPI_list = [s for s in Layer_Melting_PPI_list if s.melting_ppi_name != item_text]
                    for i in range(self.ui.layer_melting_ppi_used_beam_control_listwidget.count()):
                        if self.ui.layer_melting_ppi_used_beam_control_listwidget.item(i).text() == item_text:
                            removed = self.ui.layer_melting_ppi_used_beam_control_listwidget.takeItem(i)
                            del removed
                            break
                    index = self.ui.load_an_existing_layer_melting_ppi_combobox.findText(item_text)
                    if index != -1: self.ui.load_an_existing_layer_melting_ppi_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Layer_Melting_PPI_list) if cls.melting_ppi_name == item_text),
                             -1)
                self.ui.layer_melting_ppi_name.setPlainText(Layer_Melting_PPI_list[index].melting_ppi_name)
                self.ui.layer_melting_ppi_file.setPlainText(Layer_Melting_PPI_list[index].melting_ppi_ppi_file)
                self.ui.correspond_layer_build_model_combobox_2.setCurrentText(
                    Layer_Melting_PPI_list[index].melting_ppi_ppi_corrspond_layer_build_model)
                self.ui.layer_melting_ppi_layer_number.setPlainText(
                    Layer_Melting_PPI_list[index].melting_ppi_ppi_layer_num)
                self.ui.layer_melting_ppi_file_format.setPlainText(
                    Layer_Melting_PPI_list[index].melting_ppi_ppi_file_format)
                self.ui.correspond_layer_melting_strategy_combobox.setCurrentText(
                    Layer_Melting_PPI_list[index].melting_ppi_ppi_correspond_pre_heating_strategy)
                self.ui.layer_melting_ppi_comment.setPlainText(Layer_Melting_PPI_list[index].melting_ppi_ppi_comment)
                self.ui.composed_of_am_part_layer_melting_ppi_listWidget.clear()
                try:
                    for item_text in Layer_Melting_PPI_list[index].melting_ppi_composed_AM_part_Layer_melting_ppi:
                        self.ui.composed_of_am_part_layer_melting_ppi_listWidget.addItem(item_text)
                except:
                    pass
                Layer_Melting_PPI_list = [s for s in Layer_Melting_PPI_list if s.melting_ppi_name != item_text]
                for i in range(self.ui.layer_melting_ppi_used_beam_control_listwidget.count()):
                    if self.ui.layer_melting_ppi_used_beam_control_listwidget.item(i).text() == item_text:
                        removed = self.ui.layer_melting_ppi_used_beam_control_listwidget.takeItem(i)
                        del removed
                        break
                index = self.ui.load_an_existing_layer_melting_ppi_combobox.findText(item_text)
                if index != -1: self.ui.load_an_existing_layer_melting_ppi_combobox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_post_heating_ppi_listWidget_2_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget_2
        item = list_widget.itemAt(position)
        if item is None: return  # No item under cursor
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Post_Heating_PPI_list, Layer_Post_Heating_PPI_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Post_Heating_PPI_list = [s for s in Layer_Post_Heating_PPI_list if
                                                   s.post_heat_ppi_name != item_text]
                    Layer_Post_Heating_PPI_list_used_in_project = [s for s in
                                                                   Layer_Post_Heating_PPI_list_used_in_project if
                                                                   s.post_heat_ppi_name != item_text]
                    for i in range(self.ui.layer_post_heating_ppi_used_beam_control_listwidget.count()):
                        if self.ui.layer_post_heating_ppi_used_beam_control_listwidget.item(i).text() == item_text:
                            removed = self.ui.layer_post_heating_ppi_used_beam_control_listwidget.takeItem(i)
                            del removed
                            break
                    index = self.ui.load_an_existing_layer_post_heating_ppi_combobox.findText(item_text)
                    if index != -1: self.ui.load_an_existing_layer_post_heating_ppi_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(Layer_Post_Heating_PPI_list) if cls.post_heat_ppi_name == item_text), -1)
                self.ui.layer_post_heating_ppi_name.setPlainText(Layer_Post_Heating_PPI_list[index].post_heat_ppi_name)
                self.ui.layer_post_heating_ppi_file.setPlainText(Layer_Post_Heating_PPI_list[index].post_heat_ppi_file)
                self.ui.correspond_layer_build_model_combobox.setCurrentText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_corrspond_layer_build_model)
                self.ui.layer_post_heating_ppi_layer_number.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_layer_num)
                self.ui.layer_post_heating_ppi_file_format.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_file_format)
                self.ui.correspond_layer_post_heating_combobox.setCurrentText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_correspond_post_heating_strategy)
                self.ui.layer_post_heating_ppi_comment.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_comment)
                self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.clear()
                try:
                    for item_text in Layer_Post_Heating_PPI_list[
                        index].post_heat_ppi_composed_AM_part_Layer_post_heat_ppi:
                        self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.addItem(item_text)
                except:
                    pass
                Layer_Post_Heating_PPI_list = [s for s in Layer_Post_Heating_PPI_list if
                                               s.post_heat_ppi_name != item_text]
                Layer_Post_Heating_PPI_list_used_in_project = [s for s in Layer_Post_Heating_PPI_list_used_in_project if
                                                               s.post_heat_ppi_name != item_text]
                for i in range(self.ui.layer_post_heating_ppi_used_beam_control_listwidget.count()):
                    if self.ui.layer_post_heating_ppi_used_beam_control_listwidget.item(i).text() == item_text:
                        removed = self.ui.layer_post_heating_ppi_used_beam_control_listwidget.takeItem(i)
                        del removed
                        break
                self.ui.load_an_existing_layer_post_heating_ppi_checkBox.setChecked(False)
                index = self.ui.load_an_existing_layer_post_heating_ppi_combobox.findText(item_text)
                if index != -1: self.ui.load_an_existing_layer_post_heating_ppi_combobox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_am_part_layer_pre_heating_ppi_listWidget_2_menu(self, position):
        list_widget = self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget_2
        item = list_widget.itemAt(position)
        if item is None: return  # No item under cursor
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Pre_Heating_PPI_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Pre_Heating_PPI_list = [s for s in Layer_Pre_Heating_PPI_list if
                                                  s.pre_heat_ppi_name != item_text]
                    for i in range(self.ui.list_pre_heating_ppi_in_beam_control.count()):
                        if self.ui.list_pre_heating_ppi_in_beam_control.item(i).text() == item_text:
                            removed = self.ui.list_pre_heating_ppi_in_beam_control.takeItem(i)
                            del removed
                            break
                index = self.ui.load_an_existing_layer_pr_heating_ppi_combobox.findText(item_text)
                if index != -1: self.ui.load_an_existing_layer_pr_heating_ppi_combobox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(Layer_Pre_Heating_PPI_list) if cls.pre_heat_ppi_name == item_text), -1)
                self.ui.layer_pre_heating_ppi_name.setPlainText(Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_name)
                self.ui.layer_pre_heating_ppi_file.setPlainText(Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_file)
                self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox.setCurrentText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_corrspond_layer_build_model)
                self.ui.layer_pre_heating_ppi_layer_number.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_layer_num)
                self.ui.layer_pre_heating_ppi_file_format.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_file_format)
                self.ui.correspond_to_layer_pre_heating_combobox.setCurrentText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_correspond_pre_heating_strategy)
                self.ui.layer_pre_heating_ppi_comment.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_comment)
                self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.clear()
                try:
                    for item_text in Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi:
                        self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.addItem(item_text)
                except:
                    pass
                Layer_Pre_Heating_PPI_list = [s for s in Layer_Pre_Heating_PPI_list if s.pre_heat_ppi_name != item_text]
                for i in range(self.ui.list_pre_heating_ppi_in_beam_control.count()):
                    if self.ui.list_pre_heating_ppi_in_beam_control.item(i).text() == item_text:
                        removed = self.ui.list_pre_heating_ppi_in_beam_control.takeItem(i)
                        del removed
                        break
                self.ui.load_an_existing_layer_pr_heating_ppi_checkBox.setChecked(False)
                index = self.ui.load_an_existing_layer_pr_heating_ppi_combobox.findText(item_text)
                if index != -1: self.ui.load_an_existing_layer_pr_heating_ppi_combobox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_defined_A_part_layer_melting_strategy_listwidget_2_menu(self, position):
        list_widget = self.ui.list_defined_A_part_layer_melting_strategy_listwidget_2
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Melting_Strategies_list, Layer_Melting_Strategies_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Melting_Strategies_list = [s for s in Layer_Melting_Strategies_list if
                                                     s.melting_strategy_name != item_text]
                    Layer_Melting_Strategies_list_used_in_project = [s for s in
                                                                     Layer_Melting_Strategies_list_used_in_project if
                                                                     s.melting_strategy_name != item_text]
                    index = self.ui.correspond_layer_melting_strategy_combobox.findText(item_text)
                    if index != -1: self.ui.correspond_layer_melting_strategy_combobox.removeItem(index)
                    index = self.ui.load_existing_layer_melting_startegy_combobox.findText(item_text)
                    if index != -1: self.ui.load_existing_layer_melting_startegy_combobox.removeItem(index)
                    for i in range(self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.count()):
                        if self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.item(
                                i).text() == item_text:
                            removed = self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.takeItem(i)
                            del removed
                            break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Layer_Melting_Strategies_list) if
                              cls.melting_strategy_name == item_text), -1)
                self.ui.layer_melting_strategy_name.setPlainText(
                    Layer_Melting_Strategies_list[index].melting_strategy_name)
                self.ui.layer_melting_strategy_scan_strategy.setCurrentText(
                    Layer_Melting_Strategies_list[index].melting_strategy_scan_strategy)
                self.ui.layer_melting_strategy_file.setPlainText(
                    Layer_Melting_Strategies_list[index].melting_strategy_file)
                self.ui.layer_melting_strategy_file_format.setPlainText(
                    Layer_Melting_Strategies_list[index].melting_strategy_file_format)
                self.ui.layer_melting_strategy_comment.setPlainText(
                    Layer_Melting_Strategies_list[index].melting_strategy_comment)
                try:
                    for item_text in Layer_Melting_Strategies_list[index].melting_strategy_composed_of_AM_Parts:
                        self.ui.composed_of_am_part_layer_melting_strategy_listWidget.addItem(item_text)
                except:
                    pass
                Layer_Melting_Strategies_list = [s for s in Layer_Melting_Strategies_list if
                                                 s.melting_strategy_name != item_text]
                Layer_Melting_Strategies_list_used_in_project = [s for s in
                                                                 Layer_Melting_Strategies_list_used_in_project if
                                                                 s.melting_strategy_name != item_text]
                index = self.ui.correspond_layer_melting_strategy_combobox.findText(item_text)
                if index != -1: self.ui.correspond_layer_melting_strategy_combobox.removeItem(index)
                index = self.ui.load_existing_layer_melting_startegy_combobox.findText(item_text)
                if index != -1: self.ui.load_existing_layer_melting_startegy_combobox.removeItem(index)
                for i in range(self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.count()):
                    if self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.item(
                            i).text() == item_text:
                        removed = self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.takeItem(i)
                        del removed
                        break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_defined_layer_post_heating_strategy_listwidget_menu(self, position):
        list_widget = self.ui.list_defined_layer_post_heating_strategy_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Post_Heating_Strategies_list, Layer_Post_Heating_Strategies_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Post_Heating_Strategies_list = [s for s in Layer_Post_Heating_Strategies_list if
                                                          s.post_heat_strategy_name != item_text]
                    Layer_Post_Heating_Strategies_list_used_in_project = [s for s in
                                                                          Layer_Post_Heating_Strategies_list_used_in_project
                                                                          if s.post_heat_strategy_name != item_text]
                    index = self.ui.correspond_layer_post_heating_combobox.findText(item_text)
                    if index != -1: self.ui.correspond_layer_post_heating_combobox.removeItem(index)
                    index = self.ui.load_existing_post_heating_combobox.findText(item_text)
                    if index != -1: self.ui.load_existing_post_heating_combobox.removeItem(index)
                    for i in range(self.ui.list_layer_post_heating_in_beam_control_listWidget.count()):
                        if self.ui.list_layer_post_heating_in_beam_control_listWidget.item(i).text() == item_text:
                            removed = self.ui.list_layer_post_heating_in_beam_control_listWidget.takeItem(i)
                            del removed
                            break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Layer_Post_Heating_Strategies_list) if
                              cls.post_heat_strategy_name == item_text), -1)
                self.ui.layer_post_heating_strategy_name.setPlainText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_name)
                self.ui.layer_post_heating_strategy_scan_strategy.setCurrentText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_scan_strategy)
                self.ui.layer_post_heating_strategy_file.setPlainText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_file)
                self.ui.layer_post_heating_strategy_file_format.setPlainText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_file_format)
                self.ui.layer_post_heating_strategy_comment.setPlainText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_comment)
                try:
                    for item_text in Layer_Post_Heating_Strategies_list[index].post_heat_strategy_composed_of_AM_Parts:
                        self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget.addItem(item_text)
                except:
                    pass
                Layer_Post_Heating_Strategies_list = [s for s in Layer_Post_Heating_Strategies_list if
                                                      s.post_heat_strategy_name != item_text]
                Layer_Post_Heating_Strategies_list_used_in_project = [s for s in
                                                                      Layer_Post_Heating_Strategies_list_used_in_project
                                                                      if s.post_heat_strategy_name != item_text]
                index = self.ui.correspond_layer_post_heating_combobox.findText(item_text)
                if index != -1: self.ui.correspond_layer_post_heating_combobox.removeItem(index)
                index = self.ui.load_existing_post_heating_combobox.findText(item_text)
                if index != -1: self.ui.load_existing_post_heating_combobox.removeItem(index)
                for i in range(self.ui.list_layer_post_heating_in_beam_control_listWidget.count()):
                    if self.ui.list_layer_post_heating_in_beam_control_listWidget.item(
                            i).text() == item_text:
                        removed = self.ui.list_layer_post_heating_in_beam_control_listWidget.takeItem(i)
                        del removed
                        break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_defined_layer_pre_heating_strategy_listwidget_menu(self, position):
        list_widget = self.ui.list_defined_layer_pre_heating_strategy_listwidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Pre_Heating_Strategies_list, Layer_Pre_Heating_Strategies_list_used_in_project
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Pre_Heating_Strategies_list = [s for s in Layer_Pre_Heating_Strategies_list if
                                                         s.pre_heat_strategy_name != item_text]
                    Layer_Pre_Heating_Strategies_list_used_in_project = [s for s in
                                                                         Layer_Pre_Heating_Strategies_list_used_in_project
                                                                         if s.pre_heat_strategy_name != item_text]
                    index = self.ui.correspond_to_layer_pre_heating_combobox.findText(item_text)
                    if index != -1: self.ui.correspond_to_layer_pre_heating_combobox.removeItem(index)
                    index = self.ui.load_an_existing_layer_pr_heating.findText(item_text)
                    if index != -1: self.ui.load_an_existing_layer_pr_heating.removeItem(index)
                    for i in range(self.ui.list_layer_pre_heating_in_beam_control_listWidget.count()):
                        if self.ui.list_layer_pre_heating_in_beam_control_listWidget.item(i).text() == item_text:
                            removed = self.ui.list_layer_pre_heating_in_beam_control_listWidget.takeItem(i)
                            del removed
                            break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            self.ui.load_an_existing_layer_pr_heating_checkBox.setChecked(False)
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Layer_Pre_Heating_Strategies_list) if
                              cls.pre_heat_strategy_name == item_text), -1)
                self.ui.layer_pre_heating_strategy_name.setPlainText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_name)
                self.ui.layer_pre_heating_strategy_scan_strategy.setCurrentText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_scan_strategy)
                self.ui.layer_pre_heating_strategy_file.setPlainText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_file)
                self.ui.layer_pre_heating_strategy_file_format.setPlainText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_file_format)
                try:
                    for item_text in Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi:
                        self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.addItem(item_text)
                except:pass
                Layer_Pre_Heating_Strategies_list = [s for s in Layer_Pre_Heating_Strategies_list if
                                                     s.pre_heat_strategy_name != item_text]
                Layer_Pre_Heating_Strategies_list_used_in_project = [s for s in
                                                                     Layer_Pre_Heating_Strategies_list_used_in_project
                                                                     if s.pre_heat_strategy_name != item_text]
                index = self.ui.correspond_to_layer_pre_heating_combobox.findText(item_text)
                if index != -1: self.ui.correspond_to_layer_pre_heating_combobox.removeItem(index)
                index = self.ui.load_an_existing_layer_pr_heating.findText(item_text)
                if index != -1: self.ui.load_an_existing_layer_pr_heating.removeItem(index)
                for i in range(self.ui.list_layer_pre_heating_in_beam_control_listWidget.count()):
                    if self.ui.list_layer_pre_heating_in_beam_control_listWidget.item(
                            i).text() == item_text:
                        removed = self.ui.list_layer_pre_heating_in_beam_control_listWidget.takeItem(i)
                        del removed
                        break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_scan_strategy_listWidget_menu(self, position):
        list_widget = self.ui.defined_scan_strategy_listWidget
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Scan_Strategies_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Scan_Strategies_list = [s for s in Scan_Strategies_list if s.scan_strategy_name != item_text]
                    index = self.ui.start_heating_scan_strategy.findText(item_text)
                    if index != -1: self.ui.start_heating_scan_strategy.removeItem(index)
                    index = self.ui.layer_pre_heating_strategy_scan_strategy.findText(item_text)
                    if index != -1: self.ui.layer_pre_heating_strategy_scan_strategy.removeItem(index)
                    index = self.ui.am_part_layer_pre_heating_strategy_scan_startegy.findText(item_text)
                    if index != -1: self.ui.am_part_layer_pre_heating_strategy_scan_startegy.removeItem(index)
                    index = self.ui.layer_post_heating_strategy_scan_strategy.findText(item_text)
                    if index != -1: self.ui.layer_post_heating_strategy_scan_strategy.removeItem(index)
                    index = self.ui.am_part_layer_post_heating_strategy_scan_strategy.findText(item_text)
                    if index != -1: self.ui.am_part_layer_post_heating_strategy_scan_strategy.removeItem(index)
                    index = self.ui.layer_melting_strategy_scan_strategy.findText(item_text)
                    if index != -1: self.ui.layer_melting_strategy_scan_strategy.removeItem(index)
                    index = self.ui.am_part_layer_melting_strategy_scan_strategy.findText(item_text)
                    if index != -1: self.ui.am_part_layer_melting_strategy_scan_strategy.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Scan_Strategies_list) if cls.scan_strategy_name == item_text),-1)
                self.ui.scan_strategy_name.setPlainText(Scan_Strategies_list[index].scan_strategy_name)
                self.ui.scan_strategy_spot_size.setPlainText(Scan_Strategies_list[index].scan_strategy_beam_spot_size)
                self.ui.scan_strategy_dwell_time.setPlainText(Scan_Strategies_list[index].scan_strategy_dwell_time)
                self.ui.scan_strategy_point_distance.setPlainText(
                    Scan_Strategies_list[index].scan_strategy_point_distance)
                self.ui.scan_strategy_strategy_name.setPlainText(
                    Scan_Strategies_list[index].scan_strategy_strategy_name)
                self.ui.scan_strategy_scan_speed.setPlainText(Scan_Strategies_list[index].scan_strategy_scan_speed)
                self.ui.scan_strategy_beam_power.setPlainText(Scan_Strategies_list[index].scan_strategy_beam_power)
                self.ui.scan_strategy_comment.setPlainText(Scan_Strategies_list[index].scan_strategy_comment)
                Scan_Strategies_list = [m for m in Scan_Strategies_list if m.scan_strategy_name != item_text]
                index = self.ui.start_heating_scan_strategy.findText(item_text)
                if index != -1: self.ui.start_heating_scan_strategy.removeItem(index)
                index = self.ui.layer_pre_heating_strategy_scan_strategy.findText(item_text)
                if index != -1: self.ui.layer_pre_heating_strategy_scan_strategy.removeItem(index)
                index = self.ui.am_part_layer_pre_heating_strategy_scan_startegy.findText(item_text)
                if index != -1: self.ui.am_part_layer_pre_heating_strategy_scan_startegy.removeItem(index)
                index = self.ui.layer_post_heating_strategy_scan_strategy.findText(item_text)
                if index != -1: self.ui.layer_post_heating_strategy_scan_strategy.removeItem(index)
                index = self.ui.am_part_layer_post_heating_strategy_scan_strategy.findText(item_text)
                if index != -1: self.ui.am_part_layer_post_heating_strategy_scan_strategy.removeItem(index)
                index = self.ui.layer_melting_strategy_scan_strategy.findText(item_text)
                if index != -1: self.ui.layer_melting_strategy_scan_strategy.removeItem(index)
                index = self.ui.am_part_layer_melting_strategy_scan_strategy.findText(item_text)
                if index != -1: self.ui.am_part_layer_melting_strategy_scan_strategy.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_start_heating_listWidget_menu(self, position):
        global start_heating_strategies_in_project, Start_Heating_Strategy_list
        list_widget = self.ui.defined_start_heating_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Start_Heating_Strategy_list = [s for s in Start_Heating_Strategy_list if
                                                   s.start_heat_name != item_text]
                index = self.ui.load_start_heat_startegy_comboBox.findText(item_text)
                if index != -1: self.ui.load_start_heat_startegy_comboBox.removeItem(index)
                index = self.ui.strat_heating_pp_correspond_strategy.findText(item_text)
                if index != -1: self.ui.strat_heating_pp_correspond_strategy.removeItem(index)
                for i in range(self.ui.selected_start_heating_listWidget.count()):
                    if self.ui.selected_start_heating_listWidget.item(i).text() == item_text:
                        removed = self.ui.selected_start_heating_listWidget.takeItem(i)
                        del removed
                        break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(Start_Heating_Strategy_list) if cls.start_heat_name == item_text), -1)
                self.ui.start_heating_name.setPlainText(Start_Heating_Strategy_list[index].start_heat_name)
                self.ui.start_heating_size.setPlainText(Start_Heating_Strategy_list[index].start_heat_size)
                self.ui.start_heating_timeout.setPlainText(Start_Heating_Strategy_list[index].start_heat_timeout)
                self.ui.start_heating_scan_strategy.setCurrentText(
                    Start_Heating_Strategy_list[index].start_heat_scan_strategy)
                self.ui.start_heating_file.setPlainText(Start_Heating_Strategy_list[index].start_heat_file)
                self.ui.start_heating_shape.setPlainText(Start_Heating_Strategy_list[index].start_heat_shape)
                self.ui.start_heating_rotation_angle.setPlainText(
                    Start_Heating_Strategy_list[index].start_heat_rotation_angle)
                self.ui.start_heating_file_format.setPlainText(
                    Start_Heating_Strategy_list[index].start_heat_file_format)
                self.ui.start_heating_target_tmprature.setPlainText(
                    Start_Heating_Strategy_list[index].start_heat_target_temp)
                self.ui.start_heating_comment.setPlainText(Start_Heating_Strategy_list[index].start_heat_comment)
            Start_Heating_Strategy_list = [m for m in Start_Heating_Strategy_list if m.start_heat_name != item_text]
            index = self.ui.load_start_heat_startegy_comboBox.findText(item_text)
            if index != -1: self.ui.load_start_heat_startegy_comboBox.removeItem(index)
            for i in range(self.ui.selected_start_heating_listWidget.count()):
                if self.ui.selected_start_heating_listWidget.item(i).text() == item_text:
                    removed = self.ui.selected_start_heating_listWidget.takeItem(i)
                    del removed
                    break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_start_heat_ppi_listWidget_menu(self, position):
        global Start_Heating_PPI_list, start_heating_PPIs_in_project
        list_widget = self.ui.defined_start_heat_ppi_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Start_Heating_PPI_list = [s for s in Start_Heating_PPI_list if s.start_heat_ppi_name != item_text]
                index = self.ui.load_start_heat_ppi_comboBox.findText(item_text)
                if index != -1: self.ui.load_start_heat_ppi_comboBox.removeItem(index)
                for i in range(self.ui.selected_start_heat_ppi_listWidget.count()):
                    if self.ui.selected_start_heat_ppi_listWidget.item(i).text() == item_text:
                        removed = self.ui.selected_start_heat_ppi_listWidget.takeItem(i)
                        self.start_heating_PPIs_in_project = [s for s in start_heating_PPIs_in_project if
                                                              s.start_heat_ppi_name != item_text]
                        del removed
                        break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(Start_Heating_PPI_list) if cls.start_heat_ppi_name == item_text), -1)
                self.ui.strat_heating_printing_process_instruct_name.setPlainText(
                    Start_Heating_PPI_list[index].start_heat_ppi_name)
                self.ui.strat_heating_printing_process_instruct_file.setPlainText(
                    Start_Heating_PPI_list[index].start_heat_ppi_file)
                self.ui.strat_heating_printing_process_instruct_file_format.setPlainText(
                    Start_Heating_PPI_list[index].start_heat_ppi_file_format)
                try:
                    index_combo = self.ui.strat_heating_pp_correspond_strategy.findText(
                        Start_Heating_PPI_list[index].start_heat_ppi_correspond_start_heat_strategy)
                    if index_combo != -1:
                        self.ui.strat_heating_pp_correspond_strategy.setCurrentIndex(index_combo)
                except:pass
            Start_Heating_PPI_list = [m for m in Start_Heating_PPI_list if m.start_heat_ppi_name != item_text]
            index = self.ui.load_start_heat_ppi_comboBox.findText(item_text)
            if index != -1: self.ui.load_start_heat_ppi_comboBox.removeItem(index)
            for i in range(self.ui.selected_start_heat_ppi_listWidget.count()):
                if self.ui.selected_start_heat_ppi_listWidget.item(i).text() == item_text:
                    removed = self.ui.selected_start_heat_ppi_listWidget.takeItem(i)
                    self.start_heating_PPIs_in_project = [s for s in start_heating_PPIs_in_project if s.start_heat_ppi_name != item_text]
                    del removed
                    break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_machine_control_ppi_listwidget_menu(self, position):
        list_widget = self.ui.defined_machine_control_ppi_listwidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Machine_Powder_Feed_Control_Strategy_PPIs_list
        global machine_powder_strategy_PPI
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Machine_Powder_Feed_Control_Strategy_PPIs_list = [s for s in
                                                                      Machine_Powder_Feed_Control_Strategy_PPIs_list if
                                                                      s.Machine_powder_s_PPI_name != item_text]
                index = self.ui.load_machine_feed_instructions_comboBox.findText(item_text)
                if index != -1: self.ui.load_machine_feed_instructions_comboBox.removeItem(index)
                for i in range(self.ui.selected_machine_control_ppi.count()):
                    if self.ui.selected_machine_control_ppi.item(i).text() == item_text:
                        removed = self.ui.selected_machine_control_ppi.takeItem(i)
                        del removed
                        break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Machine_Powder_Feed_Control_Strategy_PPIs_list) if
                              cls.Machine_powder_s_PPI_name == item_text), -1)
                self.ui.machine_feed_instructions_name.setPlainText(
                    Machine_Powder_Feed_Control_Strategy_PPIs_list[index].Machine_powder_s_PPI_name)
                self.ui.machine_feed_instructions_file.setPlainText(
                    Machine_Powder_Feed_Control_Strategy_PPIs_list[index].Machine_powder_s_PPI_file)
                self.ui.machine_feed_instructions_file_format.setPlainText(
                    Machine_Powder_Feed_Control_Strategy_PPIs_list[index].Machine_powder_s_PPI_file_format)
                Machine_Powder_Feed_Control_Strategy_PPIs_list = [m for m in
                                                                  Machine_Powder_Feed_Control_Strategy_PPIs_list if
                                                                  m.Machine_powder_s_PPI_name != item_text]
            index = self.ui.load_machine_feed_instructions_comboBox.findText(item_text)
            if index != -1: self.ui.load_machine_feed_instructions_comboBox.removeItem(index)
            for i in range(self.ui.selected_machine_control_ppi.count()):
                if self.ui.selected_machine_control_ppi.item(i).text() == item_text:
                    removed = self.ui.selected_machine_control_ppi.takeItem(i)
                    del removed
                    break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_machine_powder_control_strategies_listwidget_menu(self, position):
        list_widget = self.ui.defined_machine_powder_control_strategies_listwidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Machine_Powder_Feed_Control_Strategies_list
        global machine_powder_strategy_PPI
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Machine_Powder_Feed_Control_Strategies_list = [s for s in
                                                                   Machine_Powder_Feed_Control_Strategies_list if
                                                                   s.Machine_powder_s_name != item_text]
                index = self.ui.load_machine_feed_strategy_comboBox.findText(item_text)
                if index != -1: self.ui.load_machine_feed_strategy_comboBox.removeItem(index)
                for i in range(self.ui.selected_machine_control_strategy.count()):
                    if self.ui.selected_machine_control_strategy.item(i).text() == item_text:
                        removed = self.ui.selected_machine_control_strategy.takeItem(i)
                        del removed
                        break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Machine_Powder_Feed_Control_Strategies_list) if
                              cls.Machine_powder_s_name == item_text), -1)
                self.ui.machine_feed_strategy_name.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_name)
                self.ui.machine_feed_strategy_file.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_file)
                self.ui.machine_feed_strategy_file_format.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_file_format)
                self.ui.machine_feed_strategy_triggered_start.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_triggered_start)
                self.ui.machine_feed_strategy_full_repeats.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_full_repeats)
                self.ui.machine_feed_strategy_recoater_speed.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_speed)
                self.ui.machine_feed_strategy_retract_speed.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_retract_speed)
                self.ui.machine_feed_strategy_dwell_time.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_dwell_time)
                self.ui.machine_feed_strategy_build_repeats.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_build_repeats)
                self.ui.machine_feed_strategy_comment.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_comment)
                Machine_Powder_Feed_Control_Strategies_list = [m for m in Machine_Powder_Feed_Control_Strategies_list if m.Machine_powder_s_name != item_text]
                if machine_powder_strategy_PPI:
                    self.ui.machine_feed_instructions_name.setPlainText(
                        machine_powder_strategy_PPI.Machine_powder_s_PPI_name)
                    self.ui.machine_feed_instructions_file.setPlainText(
                        machine_powder_strategy_PPI.Machine_powder_s_PPI_file)
                    self.ui.machine_feed_instructions_file_format.setPlainText(
                        machine_powder_strategy_PPI.Machine_powder_s_PPI_file_format)
                    machine_powder_strategy_PPI.Machine_powder_s_PPI_name = None
                    machine_powder_strategy_PPI.Machine_powder_s_PPI_file = None
                    machine_powder_strategy_PPI.Machine_powder_s_PPI_file_format = None
            index = self.ui.load_machine_feed_strategy_comboBox.findText(item_text)
            if index != -1: self.ui.load_machine_feed_strategy_comboBox.removeItem(index)
            for i in range(self.ui.selected_machine_control_strategy.count()):
                if self.ui.selected_machine_control_strategy.item(i).text() == item_text:
                    removed = self.ui.selected_machine_control_strategy.takeItem(i)
                    del removed
                    break
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_output_part_layer_decomposition_menu(self, position):
        list_widget = self.ui.list_output_part_layer_decomposition
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                list_widget.takeItem(list_widget.row(item))
                match = re.search(r"Build Layer\s*:\s*(.*?)\s+Part Layer\s*:\s*(.*)", item.text())
                if match:
                    layer = match.group(1).strip()
                    part = match.group(2).strip()
                    # Remove from the list
                    if (layer, part) in Layer_Of_Build_Model_AM_Parts_Layer_decomposition:
                        Layer_Of_Build_Model_AM_Parts_Layer_decomposition.remove((layer, part))
                    try:
                        index = next((i for i, cls in enumerate(Layer_Of_Build_Models_list) if
                                      cls.Layer_Of_Build_Model_name == layer), -1)
                        if index != -1 and part:
                            temp = Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_consists_of_am_part_layer
                            if not temp:
                                temp = []
                            temp = temp.remove(part)
                            Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_consists_of_am_part_layer = temp
                    except:pass
    # =======================================================================
    def list_output_layer_decomposition_menu(self, position):
        list_widget = self.ui.list_output_layer_decomposition
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes: list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def existing_ppi_listwidget_menu(self, position):
        list_widget = self.ui.existing_ppi_listwidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global defined_Printing_Process_Instructions
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    defined_Printing_Process_Instructions = [s for s in defined_Printing_Process_Instructions if
                                                             s.ppi_name != item_text]
                index = self.ui.load_exist_printing_instructions_comboBox.findText(item_text)
                if index != -1:
                    self.ui.load_exist_printing_instructions_comboBox.removeItem(index)
                index = self.ui.input_printing_ppi_name.findText(item_text)
                if index != -1:
                    self.ui.input_printing_ppi_name.removeItem(index)
                try:
                    self.ui.selected_ppi_slicing_process.takeItem(item_text)
                except:
                    pass
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next(
                    (i for i, cls in enumerate(defined_Printing_Process_Instructions) if cls.ppi_name == item_text), -1)
                self.ui.printing_process_instructions_name.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_name)
                self.ui.printing_process_instructions_file.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_file)
                self.ui.printing_process_instructions_file_format.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_file_format)
                self.ui.printing_process_instructions_layer_thicknesses.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_list_layer_thicknesses)
                self.ui.printing_process_instructions_comment.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_comment)
                defined_Printing_Process_Instructions = [m for m in defined_Printing_Process_Instructions if
                                                         m.ppi_name != item_text]
                index = self.ui.load_exist_printing_instructions_comboBox.findText(item_text)
                if index != -1: self.ui.load_exist_printing_instructions_comboBox.removeItem(index)
                index = self.ui.input_printing_ppi_name.findText(item_text)
                if index != -1:
                    self.ui.input_printing_ppi_name.removeItem(index)
                try:
                    self.ui.selected_ppi_slicing_process.takeItem(item_text)
                except:pass
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_existing_model_layers_menu(self, position):
        list_widget = self.ui.list_existing_model_layers
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Of_Build_Models_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Layer_Of_Build_Models_list = [s for s in Layer_Of_Build_Models_list if
                                                  s.Layer_Of_Build_Model_name != item_text]
                    items = self.ui.list_output_layer_decomposition.findItems(item_text, Qt.MatchFlag.MatchExactly)
                    if items:
                        for i in items:
                            row = self.ui.list_output_layer_decomposition.row(i)
                            self.ui.list_output_layer_decomposition.takeItem(row)
                    index = self.ui.load_layer_comboBox.findText(item_text)
                    if index != -1:
                        self.ui.load_layer_comboBox.removeItem(index)
                    index = self.ui.load_layer_comboBox_2.findText(item_text)
                    if index != -1:
                        self.ui.load_layer_comboBox_2.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Layer_Of_Build_Models_list) if
                              cls.Layer_Of_Build_Model_name == item_text), -1)
                self.ui.LayerBuildModel_name.setPlainText(Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_name)
                self.ui.LayerBuildModel_layer_number.setPlainText(
                    Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_layer_num)
                self.ui.LayerBuildModel_layer_height.setPlainText(
                    Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_layer_height)
                self.ui.LayerBuildModel_file.setPlainText(Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_file)
                self.ui.LayerBuildModel_file_format.setPlainText(
                    Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_file_format)
                self.ui.LayerBuildModel_comment.setPlainText(
                    Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_comment)
                Layer_Of_Build_Models_list = [m for m in Layer_Of_Build_Models_list if
                                              m.Layer_Of_Build_Model_name != item_text]
            index = self.ui.load_layer_comboBox.findText(item_text)
            if index != -1: self.ui.load_layer_comboBox.removeItem(index)
            index = self.ui.load_layer_comboBox_2.findText(item_text)
            if index != -1: self.ui.load_layer_comboBox_2.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def list_existing_part_model_layers_menu(self, position):
        list_widget = self.ui.list_existing_part_model_layers
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Layer_Of_Build_Model_AM_Parts_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                try:
                    item_text = item.text()
                except:
                    pass
                if item is not None:
                    item_text = item.text()
                    Layer_Of_Build_Model_AM_Parts_list = [s for s in Layer_Of_Build_Model_AM_Parts_list if
                                                          s.Layer_Of_Build_Model_AM_Part_name != item_text]
                index = self.ui.layer_part_comboBox.findText(item_text)
                if index != -1:
                    self.ui.layer_part_comboBox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            try:
                item_text = item.text()
            except:pass
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Layer_Of_Build_Model_AM_Parts_list) if
                              cls.Layer_Of_Build_Model_AM_Part_name == item_text), -1)
                self.ui.PartLayerBuildModel_name.setPlainText(
                    Layer_Of_Build_Model_AM_Parts_list[index].Layer_Of_Build_Model_AM_Part_name)
                self.ui.PartLayerBuildModel_file.setPlainText(
                    Layer_Of_Build_Model_AM_Parts_list[index].Layer_Of_Build_Model_AM_Part_file)
                self.ui.PartLayerBuildModel_file_format.setPlainText(
                    Layer_Of_Build_Model_AM_Parts_list[index].Layer_Of_Build_Model_AM_Part_file_format)
                self.ui.PartLayerBuildModel_area.setPlainText(
                    Layer_Of_Build_Model_AM_Parts_list[index].layer_of_Build_Model_AM_Part_area)
                self.ui.PartLayerBuildModel_comment.setPlainText(
                    Layer_Of_Build_Model_AM_Parts_list[index].layer_of_Build_Model_AM_Part_comment)
                Layer_Of_Build_Model_AM_Parts_list = [m for m in Layer_Of_Build_Model_AM_Parts_list if
                                                      m.Layer_Of_Build_Model_AM_Part_name != item_text]
            index = self.ui.layer_part_comboBox.findText(item_text)
            if index != -1:
                self.ui.layer_part_comboBox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_manufactures_listWidget_menu(self, position):
        list_widget = self.ui.defined_manufactures_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global defined_Manufacturers
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    defined_Manufacturers = [s for s in defined_Manufacturers if s.manufacturer_name != item_text]
                    index = self.ui.printing_medium_manufacturer_comboBox.findText(item_text)
                    if index != -1: self.ui.printing_medium_manufacturer_comboBox.removeItem(index)
                    index = self.ui.build_plate_manufacturer_comboBox.findText(item_text)
                    if index != -1: self.ui.build_plate_manufacturer_comboBox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(defined_Manufacturers) if cls.manufacturer_name == item_text),
                             -1)
                self.ui.manufacturer_name.setPlainText(defined_Manufacturers[index].manufacturer_name)
                self.ui.manufacturer_address.setPlainText(defined_Manufacturers[index].manufacturer_address)
                self.ui.manufacturer_comment.setPlainText(defined_Manufacturers[index].manufacturer_comment)
                defined_Manufacturers = [m for m in defined_Manufacturers if m.manufacturer_name != item_text]
                index = self.ui.printing_medium_manufacturer_comboBox.findText(item_text)
                if index != -1: self.ui.printing_medium_manufacturer_comboBox.removeItem(index)
                index = self.ui.build_plate_manufacturer_comboBox.findText(item_text)
                if index != -1: self.ui.build_plate_manufacturer_comboBox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_materials_listWidget_menu(self, position):
        list_widget = self.ui.defined_materials_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        view_action = menu.addAction("View")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global defined_Materials
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    defined_Materials = [s for s in defined_Materials if s.material_name != item_text]
                    index = self.ui.build_plate_material_comboBox.findText(item_text)
                    if index != -1: self.ui.build_plate_material_comboBox.removeItem(index)
                    index = self.ui.printing_medium_material_comboBox.findText(item_text)
                    if index != -1: self.ui.printing_medium_material_comboBox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == view_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                self.open_edit_material_window(item_text)
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(defined_Materials) if cls.material_name == item_text), -1)
                self.ui.material_name.setPlainText(defined_Materials[index].material_name)
                self.ui.material_melting_point.setPlainText(defined_Materials[index].material_melting_point)
                self.ui.material_oxidation_resistance.setPlainText(
                    defined_Materials[index].material_oxidation_resistance)
                self.ui.material__formula.setPlainText(defined_Materials[index].material_formula)
                self.ui.material_heat_capacity.setPlainText(defined_Materials[index].material_heat_capacity)
                self.ui.material_density.setPlainText(defined_Materials[index].material_density)
                self.ui.material_electrical_resitivity.setPlainText(
                    defined_Materials[index].material_electrical_resistivity)
                self.ui.material_beam_absorption_rate.setPlainText(defined_Materials[index].material_eb_absorption_rate)
                self.ui.material_thermal_conductivity.setPlainText(
                    defined_Materials[index].material_thermal_conductivity)
                self.ui.material_electrical_conductivity.setPlainText(
                    defined_Materials[index].material_electrical_conductivity)
                self.ui.material_thermal_diffusivity.setPlainText(defined_Materials[index].material_thermal_diffusivity)
                self.ui.material_comment.setPlainText(defined_Materials[index].material_comment)
                defined_Materials = [m for m in defined_Materials if m.material_name != item_text]
                index = self.ui.build_plate_material_comboBox.findText(item_text)
                if index != -1: self.ui.build_plate_material_comboBox.removeItem(index)
                index = self.ui.printing_medium_material_comboBox.findText(item_text)
                if index != -1: self.ui.printing_medium_material_comboBox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def open_edit_material_window(self, item_text):
        global defined_Materials
        self.materialview_window = MaterialWindow(self)
        index = next((i for i, cls in enumerate(defined_Materials) if cls.material_name == item_text), -1)
        self.materialview_window.ui.material_name.setPlainText(defined_Materials[index].material_name)
        self.materialview_window.ui.material_name.setReadOnly(True)
        self.materialview_window.ui.material_melting_point.setPlainText(defined_Materials[index].material_melting_point)
        self.materialview_window.ui.material_melting_point.setReadOnly(True)
        self.materialview_window.ui.material_oxidation_resistance.setPlainText(
            defined_Materials[index].material_oxidation_resistance)
        self.materialview_window.ui.material_oxidation_resistance.setReadOnly(True)
        self.materialview_window.ui.material__formula.setPlainText(defined_Materials[index].material_formula)
        self.materialview_window.ui.material__formula.setReadOnly(True)
        self.materialview_window.ui.material_heat_capacity.setPlainText(defined_Materials[index].material_heat_capacity)
        self.materialview_window.ui.material_heat_capacity.setReadOnly(True)
        self.materialview_window.ui.material_density.setPlainText(defined_Materials[index].material_density)
        self.materialview_window.ui.material_density.setReadOnly(True)
        self.materialview_window.ui.material_electrical_resitivity.setPlainText(
            defined_Materials[index].material_electrical_resistivity)
        self.materialview_window.ui.material_electrical_resitivity.setReadOnly(True)
        self.materialview_window.ui.material_beam_absorption_rate.setPlainText(
            defined_Materials[index].material_eb_absorption_rate)
        self.materialview_window.ui.material_beam_absorption_rate.setReadOnly(True)
        self.materialview_window.ui.material_thermal_conductivity.setPlainText(
            defined_Materials[index].material_thermal_conductivity)
        self.materialview_window.ui.material_thermal_conductivity.setReadOnly(True)
        self.materialview_window.ui.material_electrical_conductivity.setPlainText(
            defined_Materials[index].material_electrical_conductivity)
        self.materialview_window.ui.material_electrical_conductivity.setReadOnly(True)
        self.materialview_window.ui.material_thermal_diffusivity.setPlainText(
            defined_Materials[index].material_thermal_diffusivity)
        self.materialview_window.ui.material_thermal_diffusivity.setReadOnly(True)
        self.materialview_window.ui.material_comment.setPlainText(defined_Materials[index].material_comment)
        self.materialview_window.ui.material_comment.setReadOnly(True)
        self.materialview_window.show()
    # =======================================================================
    def selected_digital_build_model_menu(self, position):
        list_widget = self.ui.selected_digital_build_model
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Build_model
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    Build_model = None
                list_widget.takeItem(list_widget.row(item))
                self.ui.add_buil_model_button.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                            "border: 1px solid rgb(0, 0, 127); \n"
                                                            "    border-radius: 4px;         \n"
                                                            "    padding: 4px; ")
                if self.ui.define_build_model.isChecked():
                    self.ui.add_buil_model_button.setEnabled(True)
                self.ui.add_buil_model_button_2.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                              "border: 1px solid rgb(0, 0, 127); \n"
                                                              "    border-radius: 4px;         \n"
                                                              "    padding: 4px; ")
                if self.ui.load_build_model_checkBox.isChecked():
                    self.ui.add_buil_model_button_2.setEnabled(True)
    # =======================================================================
    def existing_digital_build_model_listwidget_menu(self, position):
        list_widget = self.ui.existing_digital_build_model_listwidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("View and Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Defined_Build_models
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Defined_Build_models = [s for s in Defined_Build_models if s.build_model_name != item_text]
                    index = self.ui.load_buildmodel_combobox.findText(item_text)
                    if index != -1:
                        self.ui.load_buildmodel_combobox.removeItem(index)
                        if self.Build_model.build_model_name == item_text:
                            self.ui.add_buil_model_button_2.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                                          "border: 1px solid rgb(0, 0, 127); \n"
                                                                          "    border-radius: 4px;         \n"
                                                                          "    padding: 4px; ")
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                self.open_edit_build_model_window(item_text)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def toggle_composed_of_am_part_layer_melting_strategy_combobox_2(self, state):
        if self.ui.composed_of_am_part_layer_melting_strategy_checkbox.isChecked():
            self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.setEnabled(True)
        else:
            self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.setEnabled(False)
    # =======================================================================
    def toggle_composed_of_am_part_melting_ppi_combobox(self, state):
        if self.ui.composed_of_am_part_melting_ppi_checkBox.isChecked():
            self.ui.composed_of_am_part_melting_ppi_combobox.setEnabled(True)
        else:
            self.ui.composed_of_am_part_melting_ppi_combobox.setEnabled(False)
    # =======================================================================
    def toggle_load_an_existing_layer_melting_ppi_combobox(self, state):
        if self.ui.load_an_existing_layer_melting_ppi_checkBox.isChecked():
            self.ui.load_an_existing_layer_melting_ppi_combobox.setEnabled(True)
        else:
            self.ui.load_an_existing_layer_melting_ppi_combobox.setEnabled(False)
    # =======================================================================
    def toggle_choose_support_edit_window(self, state):
        if self.edit_window.ui.has_support_checkBox.isChecked():
            self.edit_window.ui.choose_support.setEnabled(True)
        else:
            self.edit_window.ui.choose_support.setEnabled(False)
    # =======================================================================
    def part_support_in_model_list_menu_edit_window(self, position):
        list_widget = self.edit_window.ui.part_support_in_model_list
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    global supervisors_list
                    supervisors_list = [s for s in supervisors_list if s.supervisor_name != item_text]
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def on_ok_clicked_2(self):
        global Build_model
        global Defined_Build_models
        if self.edit_window.ui.build_model_name.toPlainText().strip():
            item_text = self.edit_window.ui.build_model_name.toPlainText().strip()
            text = self.edit_window.ui.build_model_name.toPlainText().strip()
            if not (any(cls.build_model_name == text for cls in Defined_Build_models)):
                new_build_model = output_Build_Model_Design_Process_class()
                new_build_model.build_model_name = self.edit_window.ui.build_model_name.toPlainText()
                new_build_model.build_model_file_path = self.edit_window.ui.build_model_file_path.toPlainText()
                new_build_model.build_model_file_format = self.edit_window.ui.build_model_file_format.toPlainText()
                new_build_model.build_model_dimension = self.edit_window.ui.Build_model_dimension.toPlainText()
                new_build_model.build_model_comment = self.edit_window.ui.build_model_comment.toPlainText()
                items = [self.edit_window.ui.part_support_in_model_list.item(i).text()
                         for i in range(self.edit_window.ui.part_support_in_model_list.count())]
                new_build_model.build_model_parts_supports = items
                Defined_Build_models.append(new_build_model)
                self.ui.load_buildmodel_combobox.addItem(new_build_model.build_model_name)
                self.ui.existing_digital_build_model_listwidget.addItem(new_build_model.build_model_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Build Model has been saved successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                new_build_model = output_Build_Model_Design_Process_class()
                new_build_model.build_model_name = self.edit_window.ui.build_model_name.toPlainText()
                new_build_model.build_model_file_path = self.edit_window.ui.build_model_file_path.toPlainText()
                new_build_model.build_model_file_format = self.edit_window.ui.build_model_file_format.toPlainText()
                new_build_model.build_model_dimension = self.edit_window.ui.Build_model_dimension.toPlainText()
                new_build_model.build_model_comment = self.edit_window.ui.build_model_comment.toPlainText()
                items = [self.edit_window.ui.part_support_in_model_list.item(i).text() for i in
                         range(self.edit_window.ui.part_support_in_model_list.count())]
                new_build_model.build_model_parts_supports = items
                Build_model = new_build_model
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Build Model has been saved successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error", "The name of Build Model cannot be empty or just spaces.")
    # =======================================================================
    def on_ok_clicked(self):
        global Build_model
        global Defined_Build_models
        if self.edit_window.ui.build_model_name.toPlainText().strip():
            item_text = self.edit_window.ui.build_model_name.toPlainText().strip()
            Defined_Build_models = [s for s in Defined_Build_models if s.build_model_name != item_text]
            index = self.ui.load_buildmodel_combobox.findText(item_text)
            if index != -1: self.ui.load_buildmodel_combobox.removeItem(index)
            text = self.edit_window.ui.build_model_name.toPlainText().strip()
            if not (any(cls.build_model_name == text for cls in Defined_Build_models)):
                new_build_model = output_Build_Model_Design_Process_class()
                new_build_model.build_model_name = self.edit_window.ui.build_model_name.toPlainText()
                new_build_model.build_model_file_path = self.edit_window.ui.build_model_file_path.toPlainText()
                new_build_model.build_model_file_format = self.edit_window.ui.build_model_file_format.toPlainText()
                new_build_model.build_model_dimension = self.edit_window.ui.Build_model_dimension.toPlainText()
                new_build_model.build_model_comment = self.edit_window.ui.build_model_comment.toPlainText()
                items = [self.edit_window.ui.part_support_in_model_list.item(i).text() for i in
                         range(self.edit_window.ui.part_support_in_model_list.count())]
                new_build_model.build_model_parts_supports = items
                Defined_Build_models.append(new_build_model)
                self.ui.load_buildmodel_combobox.addItem(new_build_model.build_model_name)
                self.ui.existing_digital_build_model_listwidget.addItem(new_build_model.build_model_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Build Model has been saved successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of Build Model should be unique.")
        else:
            QMessageBox.critical(self, "Input Error", "The name of Build Model cannot be empty or just spaces.")
    # =======================================================================
    def display_concepts_definitions(self):
        global concept_names_definition
        self.concepts_definitions_window = ConceptsDefinitionsWindow(self)
        if concept_names_definition:
            for concept in concept_names_definition:
                try:
                    if concept['label'].startswith("N"):
                        continue  # Skip auto-generated or unlabeled concepts
                except: pass
                text = f"Concept: {concept['label']} ---> Definition: {concept['comment']}"
                self.concepts_definitions_window.ui.listWidget.addItem(text)
                self.concepts_definitions_window.ui.listWidget.addItem('')
            self.concepts_definitions_window.show()
    # =======================================================================
    def load_buildmodel_combobox_on_selection(self):
        if self.ui.load_build_model_checkBox.isChecked():
            item_text = self.ui.load_buildmodel_combobox.currentText()
            self.ui.add_buil_model_button_2.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                          "border: 1px solid rgb(0, 0, 127); \n"
                                                          "    border-radius: 4px;         \n"
                                                          "    padding: 4px; ")
            self.ui.add_buil_model_button_2.setEnabled(True)
            self.edit_window = EditWindow(self)
            self.edit_window.ui.add_part_support.setChecked(False)
            self.edit_window.ui.choose_support.setEnabled(True)
            self.edit_window.ui.buttonBox.accepted.connect(self.on_ok_clicked_2)
            self.edit_window.ui.part_support_in_model_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.edit_window.ui.part_support_in_model_list.customContextMenuRequested.connect(
                self.part_support_in_model_list_menu_edit_window)
            self.edit_window.ui.has_support_checkBox.stateChanged.connect(self.toggle_choose_support_edit_window)
            self.edit_window.ui.add_part_to_build_model_button.clicked.connect(
                self.add_part_to_build_model_func_edit_window)
            index = next((i for i, cls in enumerate(Defined_Build_models) if cls.build_model_name == item_text), -1)
            self.edit_window.ui.choose_part.addItems([part.am_part_name for part in Build_Model_AM_Part_list])
            self.edit_window.ui.choose_support.addItems([support.support_name for support in Build_Model_Support_list])
            self.edit_window.ui.build_model_name.setPlainText(Defined_Build_models[index].build_model_name)
            self.edit_window.ui.Build_model_dimension.setPlainText(Defined_Build_models[index].build_model_dimension)
            self.edit_window.ui.build_model_file_path.setPlainText(Defined_Build_models[index].build_model_file_path)
            self.edit_window.ui.build_model_file_format.setPlainText(
                Defined_Build_models[index].build_model_file_format)
            self.edit_window.ui.build_model_comment.setPlainText(Defined_Build_models[index].build_model_comment)
            self.edit_window.ui.build_model_name.setEnabled(False)
            self.edit_window.ui.Build_model_dimension.setEnabled(False)
            self.edit_window.ui.build_model_file_path.setEnabled(False)
            self.edit_window.ui.build_model_file_format.setEnabled(False)
            self.edit_window.ui.build_model_comment.setEnabled(False)
            self.edit_window.ui.build_model_comment.setEnabled(False)
            self.edit_window.ui.buttonBox.setEnabled(False)
            self.edit_window.ui.part_support_in_model_list.clear()
            self.edit_window.ui.part_support_in_model_list.addItems(
                Defined_Build_models[index].build_model_parts_supports)
            self.edit_window.show()
    # =======================================================================
    def open_edit_build_model_window(self, item_text):
        self.edit_window = EditWindow(self)
        self.edit_window.ui.add_part_support.setChecked(False)
        self.edit_window.ui.choose_support.setEnabled(True)
        self.edit_window.ui.buttonBox.accepted.connect(self.on_ok_clicked)
        self.edit_window.ui.part_support_in_model_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.edit_window.ui.part_support_in_model_list.customContextMenuRequested.connect(
            self.part_support_in_model_list_menu_edit_window)
        self.edit_window.ui.has_support_checkBox.stateChanged.connect(self.toggle_choose_support_edit_window)
        self.edit_window.ui.add_part_to_build_model_button.clicked.connect(
            self.add_part_to_build_model_func_edit_window)
        index = next((i for i, cls in enumerate(Defined_Build_models) if cls.build_model_name == item_text), -1)
        self.edit_window.ui.choose_part.addItems([part.am_part_name for part in Build_Model_AM_Part_list])
        self.edit_window.ui.choose_support.addItems([support.support_name for support in Build_Model_Support_list])
        self.edit_window.ui.build_model_name.setPlainText(Defined_Build_models[index].build_model_name)
        self.edit_window.ui.Build_model_dimension.setPlainText(Defined_Build_models[index].build_model_dimension)
        self.edit_window.ui.build_model_file_path.setPlainText(Defined_Build_models[index].build_model_file_path)
        self.edit_window.ui.build_model_file_format.setPlainText(Defined_Build_models[index].build_model_file_format)
        self.edit_window.ui.build_model_comment.setPlainText(Defined_Build_models[index].build_model_comment)
        self.edit_window.ui.part_support_in_model_list.clear()
        self.edit_window.ui.part_support_in_model_list.addItems(Defined_Build_models[index].build_model_parts_supports)
        self.edit_window.show()
    # =======================================================================
    def parts_list_menu(self, position):
        list_widget = self.ui.parts_list
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Build_Model_AM_Part_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Build_Model_AM_Part_list = [s for s in Build_Model_AM_Part_list if s.am_part_name != item_text]
                    index = self.ui.choose_part.findText(item_text)
                    if index != -1: self.ui.choose_part.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Build_Model_AM_Part_list) if cls.am_part_name == item_text), -1)
                self.ui.am_part_name.setPlainText(Build_Model_AM_Part_list[index].am_part_name)
                self.ui.am_part__dimension.setPlainText(Build_Model_AM_Part_list[index].am_part_dimension)
                self.ui.am_part_file_path.setPlainText(Build_Model_AM_Part_list[index].am_part_file_path)
                self.ui.am_part_file_format.setPlainText(Build_Model_AM_Part_list[index].am_part_file_format)
                self.ui.am_part_comment.setPlainText(Build_Model_AM_Part_list[index].am_part_comment)
                Build_Model_AM_Part_list = [s for s in Build_Model_AM_Part_list if s.am_part_name != item_text]
                index = self.ui.choose_part.findText(item_text)
                if index != -1: self.ui.choose_part.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def Testin_process_applied_methods_list_menu(self, position):
        list_widget = self.ui.Testin_process_applied_methods_list
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    index = -1
                    for i, method in enumerate(Testing_process_applied_testing_methods):
                        text = f"Testing Method: {method.applied_testing_method_name}   Result:{str(method.applied_testing_method_result)}"
                        if text == item_text:
                            index = i
                            break
                    if index != -1:
                        del Testing_process_applied_testing_methods[index]
                        list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = -1
                for i, method in enumerate(Testing_process_applied_testing_methods):
                    text = f"Testing Method: {method.applied_testing_method_name}   Result:{str(method.applied_testing_method_result)}"
                    if text == item_text:
                        index = i
                        break
                if index != -1:
                    self.ui.testing_method_name_comboBox.setCurrentText(
                        Testing_process_applied_testing_methods[index].applied_testing_method_name)
                    self.ui.testing_method_file.setPlainText(
                        Testing_process_applied_testing_methods[index].applied_testing_method_result)
                    self.ui.testing_method_comment.setPlainText(
                        Testing_process_applied_testing_methods[index].applied_testing_method_comment)
                    del Testing_process_applied_testing_methods[index]
                    list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_testing_methods_listwidget_menu(self, position):
        list_widget = self.ui.defined_testing_methods_listwidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Testing_Methods_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    try:
                        Testing_Methods_list = [s for s in Testing_Methods_list if s.TestingMethod_name != item_text]
                    except:
                        pass
                    index = self.ui.testing_method_name_comboBox.findText(item_text)
                    if index != -1: self.ui.testing_method_name_comboBox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Testing_Methods_list) if cls.TestingMethod_name == item_text),
                             -1)
                self.ui.testing_method_name.setPlainText(Testing_Methods_list[index].TestingMethod_name)
                if (Testing_Methods_list[index].TestingMethod_type == 'Non-Destructive'):
                    self.ui.non_destructive_radioButton.setChecked(True)
                if (Testing_Methods_list[index].TestingMethod_type == 'Destructive'):
                    self.ui.destructive_radioButton.setChecked(True)
                self.ui.define_testing_method_comment.setPlainText(Testing_Methods_list[index].TestingMethod_comment)
                index_2 = self.ui.testing_method_name_comboBox.findText(item_text)
                if index_2 != -1:
                    self.ui.testing_method_name_comboBox.removeItem(index_2)
                try:
                    Testing_Methods_list = [s for s in Testing_Methods_list if s.TestingMethod_name != item_text]
                except:
                    pass
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def used_POstPrinting_methods_listWidget_menu(self, position):
        list_widget = self.ui.used_POstPrinting_methods_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Post_printing_Proces
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    try:
                        Post_printing_Proces.post_printing_process_used_methods = [s for s in
                                                                                   Post_printing_Proces.post_printing_process_used_methods
                                                                                   if s != item_text]
                    except:pass
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def defined_PostPrinting_methods_listWidget_menu(self, position):
        list_widget = self.ui.defined_PostPrinting_methods_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Post_Printing_Methods_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Post_Printing_Methods_list = [s for s in Post_Printing_Methods_list if
                                                  s.post_printing_method_name != item_text]
                    index = self.ui.Post_Printing_method_comboBox.findText(item_text)
                    if index != -1: self.ui.Post_Printing_method_comboBox.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Post_Printing_Methods_list) if
                              cls.post_printing_method_name == item_text), -1)
                self.ui.post_printing_method_name.setPlainText(
                    Post_Printing_Methods_list[index].post_printing_method_name)
                if (Post_Printing_Methods_list[index].post_printing_method_type == 'Support Removal'):
                    self.ui.support_removal_radioButton.setChecked(True)
                if (Post_Printing_Methods_list[index].post_printing_method_type == 'Heat Treatment'):
                    self.ui.heat_treatment_radioButton.setChecked(True)
                if (Post_Printing_Methods_list[index].post_printing_method_type == 'Build Cleaning'):
                    self.ui.build_cleaning_radioButton.setChecked(True)
                if (Post_Printing_Methods_list[index].post_printing_method_type == 'Build Separation From Build Plate'):
                    self.ui.build_seperation_radioButton.setChecked(True)
                self.ui.post_printing_method_comment.setPlainText(
                    Post_Printing_Methods_list[index].post_printing_method_comment)
                Post_Printing_Methods_list = [s for s in Post_Printing_Methods_list if
                                              s.post_printing_method_name != item_text]
                index = self.ui.Post_Printing_method_comboBox.findText(item_text)
                if index != -1: self.ui.Post_Printing_method_comboBox.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def supports_list_menu(self, position):
        list_widget = self.ui.supports_list
        item = list_widget.itemAt(position)
        if item is None: return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        action = menu.exec(list_widget.mapToGlobal(position))
        global Build_Model_Support_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    Build_Model_Support_list = [s for s in Build_Model_Support_list if s.support_name != item_text]
                    index = self.ui.choose_support.findText(item_text)
                    if index != -1: self.ui.choose_support.removeItem(index)
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                item_text = item.text()
                index = next((i for i, cls in enumerate(Build_Model_Support_list) if cls.support_name == item_text), -1)
                self.ui.support_name.setPlainText(Build_Model_Support_list[index].support_name)
                self.ui.support_file_path.setPlainText(Build_Model_Support_list[index].support_file_path)
                self.ui.support_file_format.setPlainText(Build_Model_Support_list[index].support_file_format)
                self.ui.support_comment.setPlainText(Build_Model_Support_list[index].support_comment)
                Build_Model_Support_list = [s for s in Build_Model_Support_list if s.support_name != item_text]
                index = self.ui.choose_support.findText(item_text)
                if index != -1: self.ui.choose_support.removeItem(index)
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def part_support_in_model_list_menu(self, position):
        list_widget = self.ui.part_support_in_model_list
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def setup_button_reset_on_groupbox_change_2(self, button, groupbox, exclude_groupbox=None):
        # Step 1: Change button color when clicked
        def on_button_clicked():
            try:
                if not self.ui.PostPrinting_Process_name.toPlainText().strip() == "":
                    button.setStyleSheet("background-color: green; color: white;")
                else:
                    button.setStyleSheet("")
            except Exception as e:
                print(f"Error: {e}")
        button.clicked.connect(on_button_clicked)
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QListWidget)):
            # Skip widgets inside the excluded group box
            def reset_and_log(w=widget):
                name = w.objectName() or w.__class__.__name__
                button.setStyleSheet("")
            if exclude_groupbox and exclude_groupbox.isAncestorOf(widget):
                continue
            if isinstance(widget, QPlainTextEdit) or isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QListWidget):
                widget.model().rowsInserted.connect(lambda *args, w=widget: reset_and_log(w))
                widget.model().rowsRemoved.connect(lambda *args, w=widget: reset_and_log(w))
    # =======================================================================
    def defined_supervisors_list_menu(self, position):
        list_widget = self.ui.defined_supervisors_list
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        edit_action = menu.addAction("Edit")
        view_action = menu.addAction("View details")
        action = menu.exec(list_widget.mapToGlobal(position))
        global supervisors_list
        if action == delete_action:
            reply = QMessageBox.question(self, "Confirm Deletion",
                                         f"Are you sure you want to delete:\n\n{item.text()}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                item = list_widget.currentItem()
                if item is not None:
                    item_text = item.text()
                    global supervisors_list
                    supervisors_list = [s for s in supervisors_list if s.supervisor_name != item_text]
                    index = self.ui.selectSupervisor.findText(item_text)
                    if index != -1: self.ui.selectSupervisor.removeItem(index)
                    for i in range(self.ui.supervisor_project_list.count()):
                        if self.ui.supervisor_project_list.item(i).text() == item_text:
                            removed = self.ui.supervisor_project_list.takeItem(i)
                            del removed
                            break
                list_widget.takeItem(list_widget.row(item))
        elif action == edit_action:
            item = list_widget.currentItem()
            if item is not None:
                self.ui.supervisor_name.clear()
                self.ui.supervisor_name_comment.clear()
                item_text = item.text()
                index = next((i for i, cls in enumerate(supervisors_list) if cls.supervisor_name == item_text), -1)
                self.ui.supervisor_name.setPlainText(supervisors_list[index].supervisor_name)
                self.ui.supervisor_name_comment.setPlainText(supervisors_list[index].supervisor_comment)
                supervisors_list = [s for s in supervisors_list if s.supervisor_name != item_text]
                index = self.ui.selectSupervisor.findText(item_text)
                if index != -1: self.ui.selectSupervisor.removeItem(index)
                for i in range(self.ui.supervisor_project_list.count()):
                    if self.ui.supervisor_project_list.item(i).text() == item_text:
                        removed = self.ui.supervisor_project_list.takeItem(i)
                        del removed
                        break
            list_widget.takeItem(list_widget.row(item))
        elif action == view_action:
            item = list_widget.currentItem()
            if item is not None:
                self.ui.supervisor_name.clear()
                self.ui.supervisor_name_comment.clear()
                item_text = item.text()
                index = next((i for i, cls in enumerate(supervisors_list) if cls.supervisor_name == item_text), -1)
                self.ui.supervisor_name.setPlainText(supervisors_list[index].supervisor_name)
                self.ui.supervisor_name_comment.setPlainText(supervisors_list[index].supervisor_comment)
    # =======================================================================
    def selected_start_heating_listWidget_menu(self, position):
        list_widget = self.ui.selected_start_heating_listWidget
        item = list_widget.itemAt(position)
        global start_heating_strategies_in_project
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            index = next((i for i, cls in enumerate(start_heating_strategies_in_project) if
                          cls.start_heat_name == list_widget.row(item)), -1)
            if index == -1:
                start_heating_strategies_in_project = [s for s in start_heating_strategies_in_project if
                                                       s.start_heat_name != item.text()]
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def selected_start_heat_ppi_listWidget_menu(self, position):
        list_widget = self.ui.selected_start_heat_ppi_listWidget
        global start_heating_PPIs_in_project
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            start_heating_PPIs_in_project = [s for s in start_heating_PPIs_in_project if
                                             s.start_heat_ppi_name != item.text()]
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def selected_machine_control_ppi_menu(self, position):
        list_widget = self.ui.selected_machine_control_ppi
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            self.machine_powder_strategy_PPI = None
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def selected_machine_control_strategy_menu(self, position):
        list_widget = self.ui.selected_machine_control_strategy
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            self.machine_powder_strategy = None
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def selected_ppi_slicing_process_menu(self, position):
        list_widget = self.ui.selected_ppi_slicing_process
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def composed_of_printed_build_PB_AM_partlistWidget_menu(self, position):
        list_widget = self.ui.composed_of_printed_build_PB_AM_partlistWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def set_as_input_printing_process_listWidget_menu(self, position):
        list_widget = self.ui.set_as_input_printing_process_listWidget
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            list_widget.takeItem(list_widget.row(item))
    # =======================================================================
    def supervisor_project_list_menu(self, position):
        list_widget = self.ui.supervisor_project_list
        item = list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec(list_widget.mapToGlobal(position))
        if action == delete_action:
            list_widget.takeItem(list_widget.row(item))
            index = next((i for i, cls in enumerate(PBF_AM_Process_Chains_list) if
                          cls.project_name == PBF_AM_Process_Chain.project_name), -1)
            items = [self.ui.supervisor_project_list.item(i).text() for i in
                     range(self.ui.supervisor_project_list.count())]
            if index != -1:
                PBF_AM_Process_Chains_list[index].project_selected_supervisors = items
    # =======================================================================
    def add_layer_melting_strategy_func(self):
        global Layer_Melting_Strategies_list, Layer_Melting_Strategies_list_used_in_project
        if self.ui.load_existing_layer_melting_startegy_checkbox.isChecked() and self.ui.load_existing_layer_melting_startegy_combobox.currentText() != "-- Select an option --":
            selected_melting_strategy = self.ui.load_existing_layer_melting_startegy_combobox.currentText()
            melting_strategy_m = next((item for item in Layer_Melting_Strategies_list if
                                       item.melting_strategy_name == selected_melting_strategy), None)
            if melting_strategy_m:
                if not (any((cls.melting_strategy_name == selected_melting_strategy for cls in
                             Layer_Melting_Strategies_list_used_in_project))):
                    Layer_Melting_Strategies_list_used_in_project.append(melting_strategy_m)
                    self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.addItem(
                        selected_melting_strategy)
                    self.ui.correspond_layer_melting_strategy_combobox.addItem(selected_melting_strategy)
                index = next((i for i, cls in enumerate(Layer_Melting_Strategies_list) if
                              cls.melting_strategy_name == selected_melting_strategy), -1)
                self.ui.layer_melting_strategy_name.setPlainText(
                    Layer_Melting_Strategies_list[index].melting_strategy_name)
                self.ui.layer_melting_strategy_scan_strategy.setCurrentText(
                    Layer_Melting_Strategies_list[index].melting_strategy_scan_strategy)
                self.ui.layer_melting_strategy_file.setPlainText(
                    Layer_Melting_Strategies_list[index].melting_strategy_file)
                self.ui.layer_melting_strategy_file_format.setPlainText(
                    Layer_Melting_Strategies_list[index].melting_strategy_file_format)
                self.ui.layer_melting_strategy_comment.setPlainText(
                    Layer_Melting_Strategies_list[index].melting_strategy_comment)
                try:
                    for i in Layer_Melting_Strategies_list[index].melting_strategy_composed_of_AM_Parts:
                        self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.addItem(i)
                except:
                    pass
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The Layer Melting Strategy has been added successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.layer_melting_strategy_name.toPlainText().strip():
                text = self.ui.layer_melting_strategy_name.toPlainText().strip()
                if not (any(cls.melting_strategy_name == text for cls in Layer_Melting_Strategies_list)):
                    if not (
                    any(cls.melting_strategy_name == text for cls in Layer_Melting_Strategies_list_used_in_project)):
                        l = Layer_Melting_Strategy_class()
                        l.melting_strategy_name = self.ui.layer_melting_strategy_name.toPlainText()
                        if (self.ui.layer_melting_strategy_scan_strategy.currentText() != "-- Select an option --"):
                            l.melting_strategy_scan_strategy = self.ui.layer_melting_strategy_scan_strategy.currentText()
                        l.melting_strategy_file = self.ui.layer_melting_strategy_file.toPlainText()
                        l.melting_strategy_file_format = self.ui.layer_melting_strategy_file_format.toPlainText()
                        if self.ui.composed_of_am_part_layer_melting_strategy_checkbox.isChecked():
                            l.melting_strategy_composed_of_AM_Parts = self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.currentText()
                        l.melting_strategy_comment = self.ui.layer_melting_strategy_comment.toPlainText()
                        Layer_Melting_Strategies_list.append(l)
                        Layer_Melting_Strategies_list_used_in_project.append(l)
                        self.ui.layer_melting_strategy_name.clear()
                        try:
                            self.ui.layer_melting_strategy_scan_strategy.setCurrentIndex(0)
                        except:pass
                        try:
                            self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.clear()
                        except:
                            pass
                        self.ui.layer_melting_strategy_file.clear()
                        self.ui.layer_melting_strategy_file_format.clear()
                        self.ui.layer_melting_strategy_comment.clear()
                        self.ui.list_of_layer_melting_strategy_used_in_beam_control_listwidget.addItem(
                            l.melting_strategy_name)
                        self.ui.list_defined_A_part_layer_melting_strategy_listwidget_2.addItem(l.melting_strategy_name)
                        self.ui.correspond_layer_melting_strategy_combobox.addItem(l.melting_strategy_name)
                        self.ui.load_existing_layer_melting_startegy_combobox.addItem(l.melting_strategy_name)
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Info: The Layer Melting Strategy has been defined successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:print(f"Error: {e}")
            else:QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def define_am_part_melting_strategy_func(self):
        if self.ui.am_part_layer_melting_strategy_name.toPlainText().strip():
            text = self.ui.am_part_layer_melting_strategy_name.toPlainText().strip()
            if not (any(cls.AM_part_melting_strategy_name == text for cls in AM_Part_Layer_Melting_Strategies_list)):
                a = AM_Part_Layer_Melting_Strategy_class()
                a.AM_part_melting_strategy_name = self.ui.am_part_layer_melting_strategy_name.toPlainText()
                a.AM_part_melting_strategy_scan_strategy = self.ui.am_part_layer_melting_strategy_scan_strategy.currentText()
                a.AM_part_melting_strategy_point_distance = self.ui.am_part_layer_melting_strategy_point_distance.toPlainText()
                a.AM_part_melting_strategy_file = self.ui.am_part_layer_melting_strategy_file.toPlainText()
                a.AM_part_melting_strategy_rotation_angle = self.ui.am_part_layer_melting_strategy_rotation_angle.toPlainText()
                a.AM_part_melting_strategy_energy_density = self.ui.am_part_layer_melting_strategy_energy_density.toPlainText()
                a.AM_part_melting_strategy_file_format = self.ui.am_part_layer_melting_strategy_file_format.toPlainText()
                a.AM_part_melting_strategy_number_repetitions = self.ui.am_part_layer_melting_strategy_number_repetitions.toPlainText()
                a.AM_part_melting_strategy_offset_margin = self.ui.am_part_layer_melting_strategy_offset_margin.toPlainText()
                a.AM_part_melting_strategy_comment = self.ui.am_part_layer_melting_strategy_number_comment.toPlainText()
                AM_Part_Layer_Melting_Strategies_list.append(a)
                self.ui.am_part_layer_melting_strategy_name.clear()
                self.ui.am_part_layer_melting_strategy_point_distance.clear()
                self.ui.am_part_layer_melting_strategy_file.clear()
                self.ui.am_part_layer_melting_strategy_rotation_angle.clear()
                self.ui.am_part_layer_melting_strategy_energy_density.clear()
                self.ui.am_part_layer_melting_strategy_file_format.clear()
                self.ui.am_part_layer_melting_strategy_number_repetitions.clear()
                self.ui.am_part_layer_melting_strategy_offset_margin.clear()
                self.ui.am_part_layer_melting_strategy_number_comment.clear()
                self.ui.am_part_layer_melting_strategy_scan_strategy.setCurrentIndex(0)
                self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.addItem(a.AM_part_melting_strategy_name)
                self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.addItem(
                    a.AM_part_melting_strategy_name)
                self.ui.list_defined_A_part_layer_melting_strategy_listwidget.addItem(a.AM_part_melting_strategy_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The AM Part Layer Melting Strategy has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
        else:QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def correspond_layer_melting_ppi_func(self):
        global Layer_Melting_PPI_list, Layer_Melting_PPI_list_used_in_project
        if self.ui.load_an_existing_layer_melting_ppi_checkBox.isChecked() and self.ui.load_an_existing_layer_melting_ppi_combobox.currentText() != "-- Select an option --":
            selected_melting_heat_ppi = self.ui.load_an_existing_layer_melting_ppi_combobox.currentText()
            post_melting_ppi_m = next(
                (item for item in Layer_Melting_PPI_list if item.melting_ppi_name == selected_melting_heat_ppi), None)
            if post_melting_ppi_m:
                if not (any((cls.melting_ppi_name == selected_melting_heat_ppi for cls in
                             Layer_Melting_PPI_list_used_in_project))):
                    Layer_Melting_PPI_list_used_in_project.append(post_melting_ppi_m)
                    self.ui.layer_melting_ppi_used_beam_control_listwidget.addItem(selected_melting_heat_ppi)
                index = next((i for i, cls in enumerate(Layer_Melting_PPI_list) if
                              cls.melting_ppi_name == selected_melting_heat_ppi), -1)
                self.ui.layer_melting_ppi_name.setPlainText(Layer_Melting_PPI_list[index].melting_ppi_name)
                self.ui.layer_melting_ppi_file.setPlainText(Layer_Melting_PPI_list[index].melting_ppi_ppi_file)
                self.ui.correspond_layer_build_model_combobox_2.setCurrentText(
                    Layer_Melting_PPI_list[index].melting_ppi_ppi_corrspond_layer_build_model)
                self.ui.layer_melting_ppi_layer_number.setPlainText(
                    Layer_Melting_PPI_list[index].melting_ppi_ppi_layer_num)
                self.ui.layer_melting_ppi_file_format.setPlainText(
                    Layer_Melting_PPI_list[index].melting_ppi_ppi_file_format)
                self.ui.correspond_layer_melting_strategy_combobox.setCurrentText(
                    Layer_Melting_PPI_list[index].melting_ppi_ppi_correspond_pre_heating_strategy)
                self.ui.layer_melting_ppi_comment.setPlainText(Layer_Melting_PPI_list[index].melting_ppi_ppi_comment)
                self.ui.composed_of_am_part_layer_melting_ppi_listWidget.clear()
                for i in Layer_Melting_PPI_list[index].melting_ppi_composed_AM_part_Layer_melting_ppi:
                    self.ui.composed_of_am_part_layer_melting_ppi_listWidget.addItem(i)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The Layer Melting PPI has been defined successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.layer_melting_ppi_name.toPlainText().strip():
                text = self.ui.layer_melting_ppi_name.toPlainText().strip()
                matching_items = self.ui.layer_melting_ppi_used_beam_control_listwidget.findItems(text,
                                                                                                  Qt.MatchFlag.MatchExactly)
                if ((not (any(cls.melting_ppi_name == text for cls in Layer_Melting_PPI_list))) and (
                        (self.ui.layer_melting_ppi_used_beam_control_listwidget.count() == 0) or (not matching_items))):
                    lp = Layer_Melting_PPI_class()
                    lp.melting_ppi_name = self.ui.layer_melting_ppi_name.toPlainText()
                    lp.melting_ppi_ppi_file = self.ui.layer_melting_ppi_file.toPlainText()
                    lp.melting_ppi_ppi_corrspond_layer_build_model = self.ui.correspond_layer_build_model_combobox_2.currentText()
                    lp.melting_ppi_ppi_layer_num = self.ui.layer_melting_ppi_layer_number.toPlainText()
                    lp.melting_ppi_ppi_file_format = self.ui.layer_melting_ppi_file_format.toPlainText()
                    lp.melting_ppi_ppi_correspond_pre_heating_strategy = self.ui.correspond_layer_melting_strategy_combobox.currentText()
                    lp.melting_ppi_ppi_comment = self.ui.layer_melting_ppi_comment.toPlainText()
                    items = [self.ui.composed_of_am_part_layer_melting_ppi_listWidget.item(i).text() for i in
                             range(self.ui.composed_of_am_part_layer_melting_ppi_listWidget.count())]
                    lp.melting_ppi_composed_AM_part_Layer_melting_ppi = items
                    Layer_Melting_PPI_list.append(lp)
                    Layer_Melting_PPI_list_used_in_project.append(lp)
                    self.ui.layer_melting_ppi_used_beam_control_listwidget.addItem(lp.melting_ppi_name)
                    self.ui.composed_of_am_part_layer_melting_ppi_listWidget_2.addItem(lp.melting_ppi_name)
                    index = self.ui.load_an_existing_layer_melting_ppi_combobox.findText(lp.melting_ppi_name)
                    if index != -1: self.ui.load_an_existing_layer_melting_ppi_combobox.removeItem(index)
                    self.ui.load_an_existing_layer_melting_ppi_combobox.addItem(lp.melting_ppi_name)
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText(
                            "Info: The Layer Melting Printing Process Instructions has been defined successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:
                        print(f"Error: {e}")
            else:QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def addam_part_layer_melting_ppi_to_layer_melting_ppi_func(self):
        if self.ui.am_part_layer_melting_ppi_name.toPlainText().strip():
            text = self.ui.am_part_layer_melting_ppi_name.toPlainText().strip()
            if not (any(cls.AM_part_melting_ppi_name == text for cls in AM_Part_Layer_Melting_PPI_list)):
                am = AM_Part_Layer_Melting_PPI_class()
                am.AM_part_melting_ppi_name = self.ui.am_part_layer_melting_ppi_name.toPlainText()
                am.AM_part_melting_ppi_related_am_part = self.ui.am_part_layer_melting_ppi_related_am_part_comboBox_2.currentText()
                am.AM_part_melting_ppi_correspond_AM_part_melting_strategy = self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.currentText()
                am.AM_part_melting_ppi_file = self.ui.am_part_layer_melting_ppi_file.toPlainText()
                am.AM_part_melting_ppi_correspond_layer_build_model = self.ui.correspond_layer_build_model_am_part_conbobox_2.currentText()
                am.AM_part_melting_ppi_file_format = self.ui.am_part_layer_melting_ppi_file_format.toPlainText()
                am.AM_part_melting_ppi_comment = self.ui.am_part_layer_melting_ppi_comment.toPlainText()
                AM_Part_Layer_Melting_PPI_list.append(am)
                self.ui.am_part_layer_melting_ppi_name.clear()
                self.ui.am_part_layer_melting_ppi_file.clear()
                self.ui.am_part_layer_melting_ppi_file_format.clear()
                self.ui.am_part_layer_melting_ppi_comment.clear()
                self.ui.am_part_layer_melting_ppi_related_am_part_comboBox_2.setCurrentIndex(0)
                self.ui.am_part_layer_melting_strategy_ppi_related_am_part_comboBox.setCurrentIndex(0)
                self.ui.correspond_layer_build_model_am_part_conbobox_2.setCurrentIndex(0)
                self.ui.composed_of_am_part_melting_ppi_combobox.addItem(am.AM_part_melting_ppi_name)
                self.ui.list_defined_AM_part_layer_melting_strategy_ppi_listwidget.addItem(am.AM_part_melting_ppi_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText(
                        "Info: The AM Part Layer Melting Printing Process Instructions has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error",
                                     "The name of AM Part Layer Melting Printing Process Instructions already exists.")
        else:QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def layer_pre_heating_strategy_okay_func(self):
        global Layer_Pre_Heating_Strategies_list, Layer_Pre_Heating_Strategies_list_used_in_project
        if self.ui.load_an_existing_layer_pr_heating_checkBox.isChecked() and self.ui.load_an_existing_layer_pr_heating.currentText() != "-- Select an option --":
            selected_pre_heat_strategy = self.ui.load_an_existing_layer_pr_heating.currentText()
            pre_heat_strategy_m = next((item for item in Layer_Pre_Heating_Strategies_list if
                                        item.pre_heat_strategy_name == selected_pre_heat_strategy), None)
            if pre_heat_strategy_m:
                if not (any((cls.pre_heat_strategy_name == selected_pre_heat_strategy for cls in
                             Layer_Pre_Heating_Strategies_list_used_in_project))):
                    Layer_Pre_Heating_Strategies_list_used_in_project.append(pre_heat_strategy_m)
                    self.ui.list_layer_pre_heating_in_beam_control_listWidget.addItem(selected_pre_heat_strategy)
                    self.ui.correspond_to_layer_pre_heating_combobox.addItem(selected_pre_heat_strategy)
                index = next((i for i, cls in enumerate(Layer_Pre_Heating_Strategies_list) if
                              cls.pre_heat_strategy_name == selected_pre_heat_strategy), -1)
                self.ui.layer_pre_heating_strategy_name.setPlainText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_name)
                self.ui.layer_pre_heating_strategy_scan_strategy.setCurrentText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_scan_strategy)
                self.ui.layer_pre_heating_strategy_file.setPlainText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_file)
                self.ui.layer_pre_heating_strategy_file_format.setPlainText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_file_format)
                self.ui.layer_pre_heating_strategy_comment.setPlainText(
                    Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_comment)
                for i in Layer_Pre_Heating_Strategies_list[index].pre_heat_strategy_composed_of_AM_Parts:
                    self.ui.composed_of_am_part_layer_pre_heating_strategy_listWidget.addItem(i)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The Layer Pre-Heating Strategy has been added successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.layer_pre_heating_strategy_name.toPlainText().strip():
                text = self.ui.layer_pre_heating_strategy_name.toPlainText().strip()
                if not (
                any((cls.pre_heat_strategy_name == text for cls in AM_Part_Layer_Pre_Heating_Strategies_list) and
                    (cls.pre_heat_strategy_name == text for cls in Layer_Pre_Heating_Strategies_list_used_in_project))):
                    l = Layer_Pre_Heating_Strategy_class()
                    l.pre_heat_strategy_name = self.ui.layer_pre_heating_strategy_name.toPlainText()
                    l.pre_heat_strategy_scan_strategy = self.ui.layer_pre_heating_strategy_scan_strategy.currentText()
                    l.pre_heat_strategy_file = self.ui.layer_pre_heating_strategy_file.toPlainText()
                    l.pre_heat_strategy_file_format = self.ui.layer_pre_heating_strategy_file_format.toPlainText()
                    l.pre_heat_strategy_comment = self.ui.layer_pre_heating_strategy_comment.toPlainText()
                    items = [self.ui.composed_of_am_part_layer_pre_heating_strategy_listWidget.item(i).text() for i in
                             range(self.ui.composed_of_am_part_layer_pre_heating_strategy_listWidget.count())]
                    l.pre_heat_strategy_composed_of_AM_Parts = items
                    Layer_Pre_Heating_Strategies_list.append(l)
                    Layer_Pre_Heating_Strategies_list_used_in_project.append(l)
                    self.ui.list_layer_pre_heating_in_beam_control_listWidget.addItem(l.pre_heat_strategy_name)
                    self.ui.correspond_to_layer_pre_heating_combobox.addItem(l.pre_heat_strategy_name)
                    self.ui.load_an_existing_layer_pr_heating.addItem(l.pre_heat_strategy_name)
                    self.ui.list_defined_layer_pre_heating_strategy_listwidget.addItem(l.pre_heat_strategy_name)
                    self.ui.layer_pre_heating_strategy_name.clear()
                    try:
                        self.ui.layer_pre_heating_strategy_scan_strategy.setCurrentIndex(0)
                    except:
                        pass
                    self.ui.layer_pre_heating_strategy_file.clear()
                    self.ui.layer_pre_heating_strategy_file_format.clear()
                    try:
                        self.ui.composed_of_am_part_pre_startegies_combobox.setCurrentIndex(0)
                    except:
                        pass
                    self.ui.layer_pre_heating_strategy_comment.clear()
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText("Info: The Layer Pre-Heating Strategy has been defined successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:
                        print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def add_am_part_layer_pre_heating_strategy_to_layer_pre_strategy_func(self):
        if self.ui.am_part_layer_pre_heating_strategy_name.toPlainText().strip():
            text = self.ui.am_part_layer_pre_heating_strategy_name.toPlainText().strip()
            if not (
            any(cls.AM_part_pre_heat_strategy_name == text for cls in AM_Part_Layer_Pre_Heating_Strategies_list)):
                a = AM_Part_Layer_Pre_Heating_Strategy_class()
                a.AM_part_pre_heat_strategy_name = self.ui.am_part_layer_pre_heating_strategy_name.toPlainText()
                if (self.ui.am_part_layer_pre_heating_strategy_scan_startegy.currentText() != "-- Select an option --"):
                    a.AM_part_pre_heat_strategy_scan_strategy = self.ui.am_part_layer_pre_heating_strategy_scan_startegy.currentText()
                a.AM_part_pre_heat_strategy_file = self.ui.am_part_layer_pre_heating_strategy_file.toPlainText()
                a.AM_part_pre_heat_strategy_rotation_angle = self.ui.am_part_layer_pre_heating_strategy_rotation_angle.toPlainText()
                a.AM_part_pre_heat_strategy_file_format = self.ui.am_part_layer_pre_heating_strategy_file_format.toPlainText()
                a.AM_part_pre_heat_strategy_number_repetitions = self.ui.am_part_layer_pre_heating_strategy_number_repetitions.toPlainText()
                a.AM_part_pre_heat_strategy_number_comment = self.ui.am_part_layer_pre_heating_strategy_number_comment.toPlainText()
                AM_Part_Layer_Pre_Heating_Strategies_list.append(a)
                self.ui.am_part_layer_pre_heating_strategy_name.clear()
                self.ui.am_part_layer_pre_heating_strategy_file.clear()
                self.ui.am_part_layer_pre_heating_strategy_rotation_angle.clear()
                self.ui.am_part_layer_pre_heating_strategy_file_format.clear()
                self.ui.am_part_layer_pre_heating_strategy_number_repetitions.clear()
                self.ui.am_part_layer_pre_heating_strategy_number_comment.clear()
                self.ui.am_part_layer_pre_heating_strategy_scan_startegy.setCurrentIndex(0)
                self.ui.composed_of_am_part_pre_startegies_combobox.addItem(a.AM_part_pre_heat_strategy_name)
                self.ui.correspond_am_part_layer_pre_heating.addItem(a.AM_part_pre_heat_strategy_name)
                self.ui.list_defined_A_part_layer_pre_heating_strategy_listwidget.addItem(
                    a.AM_part_pre_heat_strategy_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The AM Part Layer Pre-Heating Strategy has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error",
                                     "The name of AM Part Layer Pre-Heating Strategy already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def correspond_layer_pre_heating_ppi_to_layer_pre_strategy_func(self):
        global Layer_Pre_Heating_PPI_list, Layer_Pre_Heating_PPI_list_used_in_project
        if self.ui.load_an_existing_layer_pr_heating_ppi_checkBox.isChecked() and self.ui.load_an_existing_layer_pr_heating_ppi_combobox.currentText() != "-- Select an option --":
            selected_pre_heat_ppi = self.ui.load_an_existing_layer_pr_heating_ppi_combobox.currentText()
            pre_heat_ppi_m = next(
                (item for item in Layer_Pre_Heating_PPI_list if item.pre_heat_ppi_name == selected_pre_heat_ppi), None)
            if pre_heat_ppi_m:
                if not (any((cls.pre_heat_ppi_name == selected_pre_heat_ppi for cls in
                             Layer_Pre_Heating_PPI_list_used_in_project))):
                    Layer_Pre_Heating_PPI_list_used_in_project.append(pre_heat_ppi_m)
                    self.ui.list_pre_heating_ppi_in_beam_control.addItem(selected_pre_heat_ppi)
                index = next((i for i, cls in enumerate(Layer_Pre_Heating_PPI_list) if
                              cls.pre_heat_ppi_name == selected_pre_heat_ppi), -1)
                self.ui.layer_pre_heating_ppi_name.setPlainText(Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_name)
                self.ui.layer_pre_heating_ppi_file.setPlainText(Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_file)
                self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox.setCurrentText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_corrspond_layer_build_model)
                self.ui.layer_pre_heating_ppi_layer_number.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_layer_num)
                self.ui.layer_pre_heating_ppi_file_format.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_file_format)
                self.ui.correspond_to_layer_pre_heating_combobox.setCurrentText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_correspond_pre_heating_strategy)
                self.ui.layer_pre_heating_ppi_comment.setPlainText(
                    Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_comment)
                self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.clear()
                for i in Layer_Pre_Heating_PPI_list[index].pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi:
                    self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.addItem(i)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The Layer Pre-Heating PPI has been defined successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.layer_pre_heating_ppi_name.toPlainText().strip():
                text = self.ui.layer_pre_heating_ppi_name.toPlainText().strip()
                matching_items = self.ui.list_pre_heating_ppi_in_beam_control.findItems(text, Qt.MatchFlag.MatchExactly)
                if ((not (any(cls.pre_heat_ppi_name == text for cls in Layer_Pre_Heating_PPI_list))) and (
                        (self.ui.list_pre_heating_ppi_in_beam_control.count() == 0) or (not matching_items))):
                    lp = Layer_Pre_Heating_PPI_class()
                    lp.pre_heat_ppi_name = self.ui.layer_pre_heating_ppi_name.toPlainText()
                    lp.pre_heat_ppi_file = self.ui.layer_pre_heating_ppi_file.toPlainText()
                    lp.pre_heat_ppi_corrspond_layer_build_model = self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox.currentText()
                    lp.pre_heat_ppi_layer_num = self.ui.layer_pre_heating_ppi_layer_number.toPlainText()
                    lp.pre_heat_ppi_file_format = self.ui.layer_pre_heating_ppi_file_format.toPlainText()
                    lp.pre_heat_ppi_correspond_pre_heating_strategy = self.ui.correspond_to_layer_pre_heating_combobox.currentText()
                    lp.pre_heat_ppi_comment = self.ui.layer_pre_heating_ppi_comment.toPlainText()
                    items = [self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.item(i).text() for i in
                             range(self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.count())]
                    lp.pre_heat_ppi_composed_AM_part_Layer_pre_heat_ppi = items
                    Layer_Pre_Heating_PPI_list.append(lp)
                    Layer_Pre_Heating_PPI_list_used_in_project.append(lp)
                    self.ui.list_pre_heating_ppi_in_beam_control.addItem(lp.pre_heat_ppi_name)
                    self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget_2.addItem(lp.pre_heat_ppi_name)
                    self.ui.load_an_existing_layer_pr_heating_ppi_combobox.addItem(lp.pre_heat_ppi_name)
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText(
                            "Info: The Layer Pre-Heating Printing Process Instructions has been defined successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:
                        print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def addam_part_layer_pre_heating_ppi_to_layer_pre_ppi_func(self):
        if self.ui.am_part_layer_pre_heating_ppi_name.toPlainText().strip():
            text = self.ui.am_part_layer_pre_heating_ppi_name.toPlainText().strip()
            if not (any(cls.AM_part_pre_heat_ppi_name == text for cls in AM_Part_Layer_Pre_Heating_PPI_list)):
                am = AM_Part_Layer_Pre_Heating_PPI_class()
                am.AM_part_pre_heat_ppi_name = self.ui.am_part_layer_pre_heating_ppi_name.toPlainText()
                if (self.ui.am_part_layer_pre_heating_ppi_related_am_part_comboBox.currentText() != "-- Select an option --"):
                    am.AM_part_pre_heat_ppi_related_am_part = self.ui.am_part_layer_pre_heating_ppi_related_am_part_comboBox.currentText()
                if (self.ui.correspond_am_part_layer_pre_heating.currentText() != "-- Select an option --"):
                    am.AM_part_pre_heat_ppi_correspond_AM_part_pre_heat_strategy = self.ui.correspond_am_part_layer_pre_heating.currentText()
                am.AM_part_pre_heat_ppi_file = self.ui.am_part_layer_pre_heating_ppi_file.toPlainText()
                if (self.ui.am_part_layer_pre_heating_ppi_correspond_am_part.currentText() != "-- Select an option --"):
                    am.AM_part_pre_heat_ppi_correspond_layer_build_model = self.ui.am_part_layer_pre_heating_ppi_correspond_am_part.currentText()
                am.AM_part_pre_heat_ppi_file_format = self.ui.am_part_layer_pre_heating_ppi_file_format.toPlainText()
                am.AM_part_pre_heat_ppi_comment = self.ui.am_part_layer_pre_heating_ppi_comment.toPlainText()
                AM_Part_Layer_Pre_Heating_PPI_list.append(am)
                self.ui.am_part_layer_pre_heating_ppi_name.clear()
                self.ui.am_part_layer_pre_heating_ppi_file.clear()
                self.ui.am_part_layer_pre_heating_ppi_file_format.clear()
                self.ui.am_part_layer_pre_heating_ppi_comment.clear()
                self.ui.am_part_layer_pre_heating_ppi_related_am_part_comboBox.setCurrentIndex(0)
                self.ui.correspond_am_part_layer_pre_heating.setCurrentIndex(0)
                self.ui.am_part_layer_pre_heating_ppi_correspond_am_part.setCurrentIndex(0)
                self.ui.composed_of_am_part_pre_heating_ppi_combobox.addItem(am.AM_part_pre_heat_ppi_name)
                self.ui.list_defined_AM_part_layer_pre_heating_strategy_ppi_listwidget.addItem(
                    am.AM_part_pre_heat_ppi_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText(
                        "Info: The AM Part Layer Pre-Heating Printing Process Instructions has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error",
                                     "The name of AM Part Layer Pre-Heating Printing Process Instructions already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def layer_post_heating_strategy_okay_func(self):
        global Layer_Post_Heating_Strategies_list, Layer_Post_Heating_Strategies_list_used_in_project
        if self.ui.load_existing_post_heating_checkbox.isChecked() and self.ui.load_existing_post_heating_combobox.currentText() != "-- Select an option --":
            selected_post_heat_strategy = self.ui.load_existing_post_heating_combobox.currentText()
            post_heat_strategy_m = next((item for item in Layer_Post_Heating_Strategies_list if
                                         item.post_heat_strategy_name == selected_post_heat_strategy), None)
            if post_heat_strategy_m:
                if not (any((cls.post_heat_strategy_name == selected_post_heat_strategy for cls in
                             Layer_Post_Heating_Strategies_list_used_in_project))):
                    Layer_Post_Heating_Strategies_list_used_in_project.append(post_heat_strategy_m)
                    self.ui.list_layer_post_heating_in_beam_control_listWidget.addItem(selected_post_heat_strategy)
                    self.ui.correspond_layer_post_heating_combobox.addItem(selected_post_heat_strategy)
                index = next((i for i, cls in enumerate(Layer_Post_Heating_Strategies_list) if
                              cls.post_heat_strategy_name == selected_post_heat_strategy), -1)
                self.ui.layer_post_heating_strategy_name.setPlainText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_name)
                self.ui.layer_post_heating_strategy_scan_strategy.setCurrentText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_scan_strategy)
                self.ui.layer_post_heating_strategy_file.setPlainText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_file)
                self.ui.layer_post_heating_strategy_file_format.setPlainText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_file_format)
                self.ui.layer_post_heating_strategy_comment.setPlainText(
                    Layer_Post_Heating_Strategies_list[index].post_heat_strategy_comment)
                for i in Layer_Post_Heating_Strategies_list[index].post_heat_strategy_composed_of_AM_Parts:
                    self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget.addItem(i)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The Layer Post-Heating Strategy has been added successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.layer_post_heating_strategy_name.toPlainText().strip():
                text = self.ui.layer_post_heating_strategy_name.toPlainText().strip()
                if not (any(cls.post_heat_strategy_name == text for cls in Layer_Post_Heating_Strategies_list)):
                    if not (any(cls.post_heat_strategy_name == text for cls in
                                Layer_Post_Heating_Strategies_list_used_in_project)):
                        l = Layer_Post_Heating_Strategy_class()
                        l.post_heat_strategy_name = self.ui.layer_post_heating_strategy_name.toPlainText()
                        l.post_heat_strategy_scan_strategy = self.ui.layer_post_heating_strategy_scan_strategy.currentText()
                        l.post_heat_strategy_file = self.ui.layer_post_heating_strategy_file.toPlainText()
                        l.post_heat_strategy_file_format = self.ui.layer_post_heating_strategy_file_format.toPlainText()
                        items = [self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget.item(i).text() for i
                                 in range(self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget.count())]
                        l.post_heat_strategy_composed_of_AM_Parts = items
                        l.post_heat_strategy_comment = self.ui.layer_post_heating_strategy_comment.toPlainText()
                        Layer_Post_Heating_Strategies_list.append(l)
                        Layer_Post_Heating_Strategies_list_used_in_project.append(l)
                        self.ui.list_layer_post_heating_in_beam_control_listWidget.addItem(l.post_heat_strategy_name)
                        self.ui.list_defined_layer_post_heating_strategy_listwidget.addItem(l.post_heat_strategy_name)
                        self.ui.correspond_layer_post_heating_combobox.addItem(l.post_heat_strategy_name)
                        self.ui.load_existing_post_heating_combobox.addItem(l.post_heat_strategy_name)
                        self.ui.layer_post_heating_strategy_name.clear()
                        try:
                            self.ui.layer_post_heating_strategy_scan_strategy.setCurrentIndex(0)
                        except:pass
                        self.ui.layer_post_heating_strategy_file.clear()
                        self.ui.layer_post_heating_strategy_file_format.clear()
                        try:
                            self.ui.composed_of_am_part_post_startegies_combobox.setCurrentIndex(0)
                        except:pass
                        self.ui.layer_post_heating_strategy_comment.clear()
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Info: The Layer Post-Heating Strategy has been defined successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is a missing field.")

    # =======================================================================
    def define_am_part_post_heating_func(self):
        if self.ui.am_part_layer_post_heating_strategy_name.toPlainText().strip():
            text = self.ui.am_part_layer_post_heating_strategy_name.toPlainText().strip()
            if not (
            any(cls.AM_part_post_heat_strategy_name == text for cls in AM_Part_Layer_Post_Heating_Strategies_list)):
                a = AM_Part_Layer_Post_Heating_Strategy_class()
                a.AM_part_post_heat_strategy_name = self.ui.am_part_layer_post_heating_strategy_name.toPlainText()
                if (
                        self.ui.am_part_layer_post_heating_strategy_scan_strategy.currentText() != "-- Select an option --"):
                    a.AM_part_post_heat_strategy_scan_strategy = self.ui.am_part_layer_post_heating_strategy_scan_strategy.currentText()
                a.AM_part_post_heat_strategy_file = self.ui.am_part_layer_post_heating_strategy_file.toPlainText()
                a.AM_part_post_heat_strategy_rotation_angle = self.ui.am_part_layer_post_heating_strategy_rotation_angle.toPlainText()
                a.AM_part_post_heat_strategy_file_format = self.ui.am_part_layer_post_heating_strategy_file_format.toPlainText()
                a.AM_part_post_heat_strategy_number_repetitions = self.ui.am_part_layer_post_heating_strategy_number_repetitions.toPlainText()
                a.AM_part_post_heat_strategy_number_comment = self.ui.am_part_layer_post_heating_strategy_number_comment.toPlainText()
                AM_Part_Layer_Post_Heating_Strategies_list.append(a)
                self.ui.am_part_layer_post_heating_strategy_name.clear()
                self.ui.am_part_layer_post_heating_strategy_file.clear()
                self.ui.am_part_layer_post_heating_strategy_rotation_angle.clear()
                self.ui.am_part_layer_post_heating_strategy_file_format.clear()
                self.ui.am_part_layer_post_heating_strategy_number_repetitions.clear()
                self.ui.am_part_layer_post_heating_strategy_scan_strategy.setCurrentIndex(0)
                self.ui.am_part_layer_post_heating_strategy_number_comment.clear()
                self.ui.layer_post_heating_strategy_combobox.addItem(a.AM_part_post_heat_strategy_name)
                self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.addItem(
                    a.AM_part_post_heat_strategy_name)
                self.ui.list_defined_A_part_layer_post_heating_strategy_listwidget.addItem(
                    a.AM_part_post_heat_strategy_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The AM Part Layer Post-Heating Strategy has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error",
                                     "The name of AM Part Layer Post-Heating Strategy already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "There is a missing field.")

    # =======================================================================
    def add_am_part_melting_ppi_to_list_pushbutton_func(self):
        if self.ui.composed_of_am_part_melting_ppi_combobox.currentText() and self.ui.composed_of_am_part_melting_ppi_combobox.currentText() != "-- Select an option --":
            if self.ui.composed_of_am_part_melting_ppi_checkBox.isChecked():
                text = self.ui.composed_of_am_part_melting_ppi_combobox.currentText()
                if not self.ui.composed_of_am_part_layer_melting_ppi_listWidget.findItems(text,Qt.MatchFlag.MatchExactly):
                    self.ui.composed_of_am_part_layer_melting_ppi_listWidget.addItem(text)
    # =======================================================================
    def add_to_suppervisor_list_pushbutton_func(self):
        if self.ui.selectSupervisor.currentText() and self.ui.selectSupervisor.currentText() != "-- Select an option --":
            text = self.ui.selectSupervisor.currentText()
            if not self.ui.supervisor_project_list.findItems(text, Qt.MatchFlag.MatchExactly):
                self.ui.supervisor_project_list.addItem(text)
    # =======================================================================
    def add_am_part_post_heat_strategy_to_list_pushbutton_func(self):
        if self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.currentText() and self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.currentText() != "-- Select an option --":
            if self.ui.composed_of_am_part_layer_melting_strategy_checkbox.isChecked():
                text = self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.currentText()
                if not self.ui.composed_of_am_part_layer_melting_strategy_listWidget.findItems(text,Qt.MatchFlag.MatchExactly):
                    self.ui.composed_of_am_part_layer_melting_strategy_listWidget.addItem(text)
    # =======================================================================
    def add_am_part_post_heat_strategy_to_list_pushbutton_func(self):
        if self.ui.layer_post_heating_strategy_combobox.currentText() and self.ui.layer_post_heating_strategy_combobox.currentText() != "-- Select an option --":
            if self.ui.layer_post_heating_strategy_checkbox.isChecked():
                text = self.ui.layer_post_heating_strategy_combobox.currentText()
                if not self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget.findItems(text,Qt.MatchFlag.MatchExactly):
                    self.ui.composed_of_am_part_layer_post_heating_strategy_listWidget.addItem(text)
    # =======================================================================
    def add_am_part_pre_heat_strategy_to_list_pushbutton_func(self):
        if self.ui.composed_of_am_part_pre_startegies_combobox.currentText() and self.ui.composed_of_am_part_pre_startegies_combobox.currentText() != "-- Select an option --":
            if self.ui.composed_of_am_part_pre_startegies_checkBox.isChecked():
                text = self.ui.composed_of_am_part_pre_startegies_combobox.currentText()
                if not self.ui.composed_of_am_part_layer_pre_heating_strategy_listWidget.findItems(text,
                                                                                                   Qt.MatchFlag.MatchExactly):
                    self.ui.composed_of_am_part_layer_pre_heating_strategy_listWidget.addItem(text)
    # =======================================================================
    def add_am_part_melting_strategy_to_list_pushbutton_func(self):
        if self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.currentText() and self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.currentText() != "-- Select an option --":
            if self.ui.composed_of_am_part_layer_melting_strategy_checkbox.isChecked():
                text = self.ui.composed_of_am_part_layer_melting_strategy_combobox_2.currentText()
                if not self.ui.composed_of_am_part_layer_melting_strategy_listWidget.findItems(text,
                                                                                               Qt.MatchFlag.MatchExactly):
                    self.ui.composed_of_am_part_layer_melting_strategy_listWidget.addItem(text)
    # =======================================================================
    def add_am_part_pre_heat_ppi_to_list_pushbutton_func(self):
        if self.ui.composed_of_am_part_pre_heating_ppi_combobox.currentText() and self.ui.composed_of_am_part_pre_heating_ppi_combobox.currentText() != "-- Select an option --":
            if self.ui.composed_of_am_part_pre_heating_ppi_checkBox.isChecked():
                text = self.ui.composed_of_am_part_pre_heating_ppi_combobox.currentText()
                if not self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.findItems(text, Qt.MatchFlag.MatchExactly):
                    self.ui.composed_of_am_part_layer_pre_heating_ppi_listWidget.addItem(text)
    # =======================================================================
    def add_am_part_post_heat_ppi_to_list_pushbutton_func(self):
        if self.ui.composed_of_am_part_post_heating_ppi_combobox.currentText() and self.ui.composed_of_am_part_post_heating_ppi_combobox.currentText() != "-- Select an option --":
            if self.ui.composed_of_am_part_post_heating_ppi_checkBox.isChecked():
                text = self.ui.composed_of_am_part_post_heating_ppi_combobox.currentText()
                if not self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.findItems(text, Qt.MatchFlag.MatchExactly):
                    self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.addItem(text)
    # =======================================================================
    def correspond_layer_post_heating_ppi_func(self):
        global Layer_Post_Heating_PPI_list, Layer_Post_Heating_PPI_list_used_in_project
        if self.ui.load_an_existing_layer_post_heating_ppi_checkBox.isChecked() and self.ui.load_an_existing_layer_post_heating_ppi_combobox.currentText() != "-- Select an option --":
            selected_post_heat_ppi = self.ui.load_an_existing_layer_post_heating_ppi_combobox.currentText()
            post_heat_ppi_m = next(
                (item for item in Layer_Post_Heating_PPI_list if item.post_heat_ppi_name == selected_post_heat_ppi),
                None)
            if post_heat_ppi_m:
                if not (any((cls.post_heat_ppi_name == selected_post_heat_ppi for cls in
                             Layer_Post_Heating_PPI_list_used_in_project))):
                    Layer_Post_Heating_PPI_list_used_in_project.append(post_heat_ppi_m)
                    self.ui.layer_post_heating_ppi_used_beam_control_listwidget.addItem(selected_post_heat_ppi)
                index = next((i for i, cls in enumerate(Layer_Post_Heating_PPI_list) if
                              cls.post_heat_ppi_name == selected_post_heat_ppi), -1)
                self.ui.layer_post_heating_ppi_name.setPlainText(Layer_Post_Heating_PPI_list[index].post_heat_ppi_name)
                self.ui.layer_post_heating_ppi_file.setPlainText(Layer_Post_Heating_PPI_list[index].post_heat_ppi_file)
                self.ui.correspond_layer_build_model_combobox.setCurrentText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_corrspond_layer_build_model)
                self.ui.layer_post_heating_ppi_layer_number.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_layer_num)
                self.ui.layer_post_heating_ppi_file_format.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_file_format)
                self.ui.correspond_layer_post_heating_combobox.setCurrentText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_correspond_pre_heating_strategy)
                self.ui.layer_post_heating_ppi_comment.setPlainText(
                    Layer_Post_Heating_PPI_list[index].post_heat_ppi_comment)
                self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.clear()
                for i in Layer_Post_Heating_PPI_list[index].post_heat_ppi_composed_AM_part_Layer_post_heat_ppi:
                    self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.addItem(i)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The Layer Post-Heating PPI has been defined successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.layer_post_heating_ppi_name.toPlainText().strip():
                text = self.ui.layer_post_heating_ppi_name.toPlainText().strip()
                matching_items = self.ui.layer_post_heating_ppi_used_beam_control_listwidget.findItems(text,
                                                                                                       Qt.MatchFlag.MatchExactly)
                if ((not (any(cls.post_heat_ppi_name == text for cls in Layer_Post_Heating_PPI_list))) and (
                        (self.ui.layer_post_heating_ppi_used_beam_control_listwidget.count() == 0) or (
                not matching_items))):
                    lp = Layer_Post_Heating_PPI_class()
                    lp.post_heat_ppi_name = self.ui.layer_post_heating_ppi_name.toPlainText()
                    lp.post_heat_ppi_file = self.ui.layer_post_heating_ppi_file.toPlainText()
                    lp.post_heat_ppi_corrspond_layer_build_model = self.ui.correspond_layer_build_model_combobox.currentText()
                    lp.post_heat_ppi_layer_num = self.ui.layer_post_heating_ppi_layer_number.toPlainText()
                    lp.post_heat_ppi_file_format = self.ui.layer_post_heating_ppi_file_format.toPlainText()
                    lp.post_heat_ppi_correspond_pre_heating_strategy = self.ui.correspond_layer_post_heating_combobox.currentText()
                    lp.post_heat_ppi_comment = self.ui.layer_post_heating_ppi_comment.toPlainText()
                    items = [self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.item(i).text() for i in
                             range(self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget.count())]
                    lp.post_heat_ppi_composed_AM_part_Layer_post_heat_ppi = items
                    Layer_Post_Heating_PPI_list.append(lp)
                    Layer_Post_Heating_PPI_list_used_in_project.append(lp)
                    self.ui.layer_post_heating_ppi_used_beam_control_listwidget.addItem(lp.post_heat_ppi_name)
                    self.ui.composed_of_am_part_layer_post_heating_ppi_listWidget_2.addItem(lp.post_heat_ppi_name)
                    index = self.ui.load_an_existing_layer_post_heating_ppi_combobox.findText(lp.post_heat_ppi_name)
                    if index != -1: self.ui.load_an_existing_layer_post_heating_ppi_combobox.removeItem(index)
                    self.ui.load_an_existing_layer_post_heating_ppi_combobox.addItem(lp.post_heat_ppi_name)
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText(
                            "Info: The Layer Post-Heating Printing Process Instructions has been defined successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:
                        print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def addam_part_layer_post_heating_ppi_to_layer_post_ppi_func(self):
        if self.ui.am_part_layer_post_heating_ppi_name.toPlainText().strip():
            text = self.ui.am_part_layer_post_heating_ppi_name.toPlainText().strip()
            if not (any(cls.AM_part_post_heat_ppi_name == text for cls in AM_Part_Layer_Post_Heating_PPI_list)):
                am = AM_Part_Layer_Post_Heating_PPI_class()
                am.AM_part_post_heat_ppi_name = self.ui.am_part_layer_post_heating_ppi_name.toPlainText()
                if (self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.currentText() != "-- Select an option --"):
                    am.AM_part_post_heat_ppi_related_am_part = self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.currentText()
                if (self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.currentText() != "-- Select an option --"):
                    am.AM_part_post_heat_ppi_correspond_AM_part_post_heat_strategy = self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.currentText()
                am.AM_part_post_heat_ppi_file = self.ui.am_part_layer_post_heating_ppi_file.toPlainText()
                if (self.ui.correspond_layer_build_model_am_part_conbobox.currentText() != "-- Select an option --"):
                    am.AM_part_post_heat_ppi_correspond_layer_build_model = self.ui.correspond_layer_build_model_am_part_conbobox.currentText()
                am.AM_part_post_heat_ppi_file_format = self.ui.am_part_layer_post_heating_ppi_file_format.toPlainText()
                am.AM_part_post_heat_ppi_comment = self.ui.am_part_layer_post_heating_ppi_comment.toPlainText()
                AM_Part_Layer_Post_Heating_PPI_list.append(am)
                self.ui.am_part_layer_post_heating_ppi_name.clear()
                self.ui.am_part_layer_post_heating_ppi_file.clear()
                self.ui.am_part_layer_post_heating_ppi_file_format.clear()
                self.ui.am_part_layer_post_heating_ppi_comment.clear()
                self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox.setCurrentIndex(0)
                self.ui.am_part_layer_post_heating_ppi_related_am_part_comboBox_2.setCurrentIndex(0)
                self.ui.correspond_layer_build_model_am_part_conbobox.setCurrentIndex(0)
                self.ui.composed_of_am_part_post_heating_ppi_combobox.addItem(am.AM_part_post_heat_ppi_name)
                self.ui.list_defined_AM_part_layer_post_heating_strategy_ppi_listwidget.addItem(
                    am.AM_part_post_heat_ppi_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText(
                        "Info: The AM Part Layer Post-Heating Printing Process Instructions has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error",
                                     "The name of AM Part Layer Post-Heating Printing Process Instructions already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def define_start_heating_func(self):
        global start_heating_strategies_in_project, Start_Heating_Strategy_list
        if self.ui.load_start_heat_startegy_checkbox.isChecked() and self.ui.load_start_heat_startegy_comboBox.currentText() != "-- Select an option --":
            selected_start_strategy = self.ui.load_start_heat_startegy_comboBox.currentText()
            start_strategy_m = next(
                (item for item in Start_Heating_Strategy_list if item.start_heat_name == selected_start_strategy), None)
            if start_strategy_m:
                index = next((i for i, cls in enumerate(start_heating_strategies_in_project) if
                              cls.start_heat_name == selected_start_strategy), -1)
                if index == -1:
                    start_heating_strategies_in_project.append(start_strategy_m)
                    self.ui.selected_start_heating_listWidget.addItem(start_strategy_m.start_heat_name)
                index = next((i for i, cls in enumerate(Start_Heating_Strategy_list) if
                              cls.start_heat_name == selected_start_strategy), -1)
                self.ui.start_heating_name.setPlainText(Start_Heating_Strategy_list[index].start_heat_name)
                self.ui.start_heating_size.setPlainText(Start_Heating_Strategy_list[index].start_heat_size)
                self.ui.start_heating_timeout.setPlainText(Start_Heating_Strategy_list[index].start_heat_timeout)
                self.ui.start_heating_scan_strategy.setCurrentText(
                    Start_Heating_Strategy_list[index].start_heat_scan_strategy)
                self.ui.start_heating_file.setPlainText(Start_Heating_Strategy_list[index].start_heat_file)
                self.ui.start_heating_shape.setPlainText(Start_Heating_Strategy_list[index].start_heat_shape)
                self.ui.start_heating_rotation_angle.setPlainText(
                    Start_Heating_Strategy_list[index].start_heat_rotation_angle)
                self.ui.start_heating_file_format.setPlainText(
                    Start_Heating_Strategy_list[index].start_heat_file_format)
                self.ui.start_heating_target_tmprature.setPlainText(
                    Start_Heating_Strategy_list[index].start_heat_target_temp)
                self.ui.start_heating_comment.setPlainText(Start_Heating_Strategy_list[index].start_heat_comment)
                index = self.ui.load_start_heat_startegy_comboBox.findText(selected_start_strategy)
                if index != -1: self.ui.load_start_heat_startegy_comboBox.removeItem(index)
                self.ui.load_start_heat_startegy_comboBox.addItem(selected_start_strategy)
                self.ui.strat_heating_pp_correspond_strategy.addItem(selected_start_strategy)
                self.ui.load_start_heat_startegy_checkbox.setChecked(False)
                self.ui.start_heating_name.clear()
                self.ui.start_heating_size.clear()
                self.ui.start_heating_timeout.clear()
                self.ui.start_heating_scan_strategy.setCurrentIndex(0)
                self.ui.start_heating_file.clear()
                self.ui.start_heating_shape.clear()
                self.ui.start_heating_rotation_angle.clear()
                self.ui.start_heating_file_format.clear()
                self.ui.start_heating_target_tmprature.clear()
                self.ui.start_heating_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The info about Start Heating strategy has been added successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.start_heating_name.toPlainText().strip():
                text = self.ui.start_heating_name.toPlainText().strip()
                if not (any(cls.start_heat_name == text for cls in Start_Heating_Strategy_list)):
                    st = Start_Heating_Strategy_class()
                    st.start_heat_name = self.ui.start_heating_name.toPlainText()
                    st.start_heat_size = self.ui.start_heating_size.toPlainText()
                    st.start_heat_timeout = self.ui.start_heating_timeout.toPlainText()
                    if (self.ui.start_heating_scan_strategy.currentText() != "-- Select an option --"):
                        st.start_heat_scan_strategy = self.ui.start_heating_scan_strategy.currentText()
                    st.start_heat_file = self.ui.start_heating_file.toPlainText()
                    st.start_heat_shape = self.ui.start_heating_shape.toPlainText()
                    st.start_heat_rotation_angle = self.ui.start_heating_rotation_angle.toPlainText()
                    st.start_heat_file_format = self.ui.start_heating_file_format.toPlainText()
                    st.start_heat_target_temp = self.ui.start_heating_target_tmprature.toPlainText()
                    st.start_heat_comment = self.ui.start_heating_comment.toPlainText()
                    self.ui.defined_start_heating_listWidget.addItem(st.start_heat_name)
                    index = self.ui.load_start_heat_startegy_comboBox.findText(st.start_heat_name)
                    if index != -1: self.ui.load_start_heat_startegy_comboBox.removeItem(index)
                    self.ui.load_start_heat_startegy_comboBox.addItem(st.start_heat_name)
                    self.ui.strat_heating_pp_correspond_strategy.addItem(st.start_heat_name)
                    Start_Heating_Strategy_list.append(st)
                    for i, cls in enumerate(Start_Heating_Strategy_list):
                        if str(cls.start_heat_name).strip() == st.start_heat_name:
                            break
                    index = next((i for i, cls in enumerate(start_heating_strategies_in_project) if
                                  cls.start_heat_name == text), -1)
                    if index == -1:
                        start_heating_strategies_in_project.append(st)
                        self.ui.selected_start_heating_listWidget.addItem(st.start_heat_name)
                    self.ui.start_heating_name.clear()
                    self.ui.start_heating_size.clear()
                    self.ui.start_heating_timeout.clear()
                    self.ui.start_heating_scan_strategy.setCurrentIndex(0)
                    self.ui.start_heating_file.clear()
                    self.ui.start_heating_shape.clear()
                    self.ui.start_heating_rotation_angle.clear()
                    self.ui.start_heating_file_format.clear()
                    self.ui.start_heating_target_tmprature.clear()
                    self.ui.start_heating_comment.clear()
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText("Info: The Start Heating Strategy has been added successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    QMessageBox.critical(self, "Input Error", "The name fo Start Heating Strategy already exists.")
            else:QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def define_scan_strategy_func(self):
        if self.ui.scan_strategy_name.toPlainText().strip():
            text = self.ui.scan_strategy_name.toPlainText().strip()
            if not (any(cls.scan_strategy_name == text for cls in Scan_Strategies_list)):
                s = Scan_Strategy_class()
                s.scan_strategy_name = self.ui.scan_strategy_name.toPlainText()
                s.scan_strategy_beam_spot_size = self.ui.scan_strategy_spot_size.toPlainText()
                s.scan_strategy_dwell_time = self.ui.scan_strategy_dwell_time.toPlainText()
                s.scan_strategy_point_distance = self.ui.scan_strategy_point_distance.toPlainText()
                s.scan_strategy_strategy_name = self.ui.scan_strategy_strategy_name.toPlainText()
                s.scan_strategy_scan_speed = self.ui.scan_strategy_scan_speed.toPlainText()
                s.scan_strategy_beam_power = self.ui.scan_strategy_beam_power.toPlainText()
                s.scan_strategy_comment = self.ui.scan_strategy_comment.toPlainText()
                self.ui.defined_scan_strategy_listWidget.addItem(s.scan_strategy_name)
                self.ui.start_heating_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.layer_pre_heating_strategy_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.am_part_layer_pre_heating_strategy_scan_startegy.addItem(s.scan_strategy_name)
                self.ui.layer_post_heating_strategy_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.am_part_layer_post_heating_strategy_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.layer_melting_strategy_scan_strategy.addItem(s.scan_strategy_name)
                self.ui.am_part_layer_melting_strategy_scan_strategy.addItem(s.scan_strategy_name)
                Scan_Strategies_list.append(s)
                self.ui.scan_strategy_name.clear()
                self.ui.scan_strategy_spot_size.clear()
                self.ui.scan_strategy_dwell_time.clear()
                self.ui.scan_strategy_point_distance.clear()
                self.ui.scan_strategy_strategy_name.clear()
                self.ui.scan_strategy_scan_speed.clear()
                self.ui.scan_strategy_beam_power.clear()
                self.ui.scan_strategy_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Scan Strategy has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of scan strategy is redundant.")
        else:
            QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def define_start_heating_pushButton_2_func(self):
        global Start_Heating_PPI_list, start_heating_PPIs_in_project
        if self.ui.load_start_heat_ppi_checkbox.isChecked() and self.ui.load_start_heat_ppi_comboBox.currentText() != "-- Select an option --":
            selected_start_heat_ppi = self.ui.load_start_heat_ppi_comboBox.currentText()
            start_heat_m_ppi = next(
                (item for item in Start_Heating_PPI_list if item.start_heat_ppi_name == selected_start_heat_ppi), None)
            if start_heat_m_ppi:
                index = next((i for i, cls in enumerate(start_heating_PPIs_in_project) if
                              cls.start_heat_ppi_name == selected_start_heat_ppi), -1)
                if index == -1:
                    start_heating_PPIs_in_project.append(selected_start_heat_ppi)
                    self.ui.selected_start_heat_ppi_listWidget.addItem(start_heat_m_ppi.start_heat_ppi_name)
                index = next((i for i, cls in enumerate(Start_Heating_PPI_list) if
                              cls.start_heat_ppi_name == selected_start_heat_ppi), -1)
                self.ui.strat_heating_printing_process_instruct_name.setPlainText(
                    Start_Heating_PPI_list[index].start_heat_ppi_name)
                self.ui.strat_heating_printing_process_instruct_file.setPlainText(
                    Start_Heating_PPI_list[index].start_heat_ppi_file)
                self.ui.strat_heating_printing_process_instruct_file_format.setPlainText(
                    Start_Heating_PPI_list[index].start_heat_ppi_file_format)
                self.ui.strat_heating_printing_process_instruct_name.clear()
                self.ui.strat_heating_printing_process_instruct_file.clear()
                self.ui.strat_heating_printing_process_instruct_file_format.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The info about Start Heating PPI has been saved successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.strat_heating_printing_process_instruct_name.toPlainText().strip():
                text = self.ui.strat_heating_printing_process_instruct_name.toPlainText().strip()
                if not (any(cls.start_heat_ppi_name == text for cls in Start_Heating_PPI_list)):
                    if self.ui.selected_start_heat_ppi_listWidget.count() == 0:
                        s_ppi = Start_Heating_PPI_class()
                        s_ppi.start_heat_ppi_name = self.ui.strat_heating_printing_process_instruct_name.toPlainText()
                        s_ppi.start_heat_ppi_file = self.ui.strat_heating_printing_process_instruct_file.toPlainText()
                        s_ppi.start_heat_ppi_file_format = self.ui.strat_heating_printing_process_instruct_file_format.toPlainText()
                        if (self.ui.strat_heating_pp_correspond_strategy.currentText() != "-- Select an option --"):
                            s_ppi.start_heat_ppi_correspond_start_heat_strategy = self.ui.strat_heating_pp_correspond_strategy.currentText()
                        Start_Heating_PPI_list.append(s_ppi)
                        index = next((i for i, cls in enumerate(start_heating_PPIs_in_project) if
                                      cls.start_heat_ppi_name == text), -1)
                        if index == -1:
                            start_heating_PPIs_in_project.append(s_ppi)
                            self.ui.selected_start_heat_ppi_listWidget.addItem(s_ppi.start_heat_ppi_name)
                        self.ui.defined_start_heat_ppi_listWidget.addItem(s_ppi.start_heat_ppi_name)
                        self.ui.load_start_heat_ppi_comboBox.addItem(s_ppi.start_heat_ppi_name)
                        self.ui.strat_heating_printing_process_instruct_name.clear()
                        self.ui.strat_heating_printing_process_instruct_file.clear()
                        self.ui.strat_heating_printing_process_instruct_file_format.clear()
                        self.ui.strat_heating_pp_correspond_strategy.setCurrentIndex(0)
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Info: The info about Start Heating PPI has been saved successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        s_ppi = Start_Heating_PPI_class()
                        s_ppi.start_heat_ppi_name = self.ui.strat_heating_printing_process_instruct_name.toPlainText()
                        s_ppi.start_heat_ppi_file = self.ui.strat_heating_printing_process_instruct_file.toPlainText()
                        s_ppi.start_heat_ppi_file_format = self.ui.strat_heating_printing_process_instruct_file_format.toPlainText()
                        Start_Heating_PPI_list.append(s_ppi)
                        index = next((i for i, cls in enumerate(start_heating_PPIs_in_project) if
                                      cls.start_heat_ppi_name == text), -1)
                        if index == -1:
                            start_heating_PPIs_in_project.append(s_ppi)
                            self.ui.selected_start_heat_ppi_listWidget.addItem(s_ppi.start_heat_ppi_name)
                        self.ui.defined_start_heat_ppi_listWidget.addItem(s_ppi.start_heat_ppi_name)
                        self.ui.load_start_heat_ppi_comboBox.addItem(s_ppi.start_heat_ppi_name)
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Info: The info about Start Heating PPI has been saved successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                else: QMessageBox.critical(self, "Input Error", "The name of Start Heating PPI already exists.")
            else: QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def add_machine_feed_strategy_pushButton_2_func(self):
        global Machine_Powder_Feed_Control_Strategy_PPIs_list
        global machine_powder_strategy_PPI
        if self.ui.load_machine_feed_instructions_checkBox.isChecked() and self.ui.load_machine_feed_instructions_comboBox.currentText() != "-- Select an option --":
            selected_machine_feed_ppi = self.ui.load_machine_feed_instructions_comboBox.currentText()
            machine_feed_m_ppi = next((item for item in Machine_Powder_Feed_Control_Strategy_PPIs_list if
                                       item.Machine_powder_s_PPI_name == selected_machine_feed_ppi), None)
            if machine_feed_m_ppi:
                machine_powder_strategy_PPI = machine_feed_m_ppi
                self.ui.selected_machine_control_ppi.clear()
                self.ui.selected_machine_control_ppi.addItem(machine_powder_strategy_PPI.Machine_powder_s_PPI_name)
                index = next((i for i, cls in enumerate(Machine_Powder_Feed_Control_Strategy_PPIs_list) if
                              cls.Machine_powder_s_PPI_name == selected_machine_feed_ppi), -1)
                self.ui.machine_feed_instructions_name.setPlainText(
                    Machine_Powder_Feed_Control_Strategy_PPIs_list[index].Machine_powder_s_PPI_name)
                self.ui.machine_feed_instructions_file.setPlainText(
                    Machine_Powder_Feed_Control_Strategy_PPIs_list[index].Machine_powder_s_PPI_file)
                self.ui.machine_feed_instructions_file_format.setPlainText(
                    Machine_Powder_Feed_Control_Strategy_PPIs_list[index].Machine_powder_s_PPI_file_format)
                self.ui.load_machine_feed_instructions_checkBox.setChecked(False)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText(
                        "Machine Powder Feed Control Printing Process Instructions info has been saved successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.machine_feed_instructions_name.toPlainText().strip():
                text = self.ui.machine_feed_instructions_name.toPlainText().strip()
                if not (
                any(cls.Machine_powder_s_PPI_name == text for cls in Machine_Powder_Feed_Control_Strategy_PPIs_list)):
                    if self.ui.selected_machine_control_ppi.count() == 0:
                        mp = Machine_Powder_Feed_Control_PPI_class()
                        mp.Machine_powder_s_PPI_name = self.ui.machine_feed_instructions_name.toPlainText()
                        mp.Machine_powder_s_PPI_file = self.ui.machine_feed_instructions_file.toPlainText()
                        mp.Machine_powder_s_PPI_file_format = self.ui.machine_feed_instructions_file_format.toPlainText()
                        Machine_Powder_Feed_Control_Strategy_PPIs_list.append(mp)
                        Machine_Powder_Feed_Control_Strategy_PPIs_in_project.append(mp)
                        self.ui.selected_machine_control_ppi.addItem(mp.Machine_powder_s_PPI_name)
                        self.ui.defined_machine_control_ppi_listwidget.addItem(mp.Machine_powder_s_PPI_name)
                        self.ui.load_machine_feed_instructions_comboBox.addItem(mp.Machine_powder_s_PPI_name)
                        machine_powder_strategy_PPI = mp
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText(
                                "Info: The info about Machine Powder Feed Control PPI has been saved successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        mp = Machine_Powder_Feed_Control_PPI_class()
                        mp.Machine_powder_s_PPI_name = self.ui.machine_feed_instructions_name.toPlainText()
                        mp.Machine_powder_s_PPI_file = self.ui.machine_feed_instructions_file.toPlainText()
                        mp.Machine_powder_s_PPI_file_format = self.ui.machine_feed_instructions_file_format.toPlainText()
                        Machine_Powder_Feed_Control_Strategy_PPIs_list.append(mp)
                        Machine_Powder_Feed_Control_Strategy_PPIs_in_project.append(mp)

                        self.ui.selected_machine_control_ppi.clear()
                        self.ui.selected_machine_control_ppi.addItem(mp.Machine_powder_s_PPI_name)
                        self.ui.defined_machine_control_ppi_listwidget.addItem(mp.Machine_powder_s_PPI_name)
                        self.ui.load_machine_feed_instructions_comboBox.addItem(mp.Machine_powder_s_PPI_name)
                        machine_powder_strategy_PPI = mp
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText(
                                "Info: The info about Machine Powder Feed Control PPI has been saved successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                else:
                    QMessageBox.critical(self, "Input Error",
                                         "The name of  Machine Powder Feed Control PPI already exists.")
            else:
                QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def add_machine_feed_strategy_func(self):
        global machine_powder_strategy_index
        global machine_powder_strategy
        global machine_powder_strategy_PPI
        if self.ui.machine_feed_strategy_checkBox.isChecked() and self.ui.load_machine_feed_strategy_comboBox.currentText() != "-- Select an option --":
            selected_machine_feed = self.ui.load_machine_feed_strategy_comboBox.currentText()
            machine_feed_m = next((item for item in Machine_Powder_Feed_Control_Strategies_list if
                                   item.Machine_powder_s_name == selected_machine_feed), None)
            if machine_feed_m:
                self.machine_powder_strategy = machine_feed_m
                self.ui.selected_machine_control_strategy.clear()
                self.ui.selected_machine_control_strategy.addItem(self.machine_powder_strategy.Machine_powder_s_name)
                index = next((i for i, cls in enumerate(Machine_Powder_Feed_Control_Strategies_list) if
                              cls.Machine_powder_s_name == selected_machine_feed), -1)
                self.ui.machine_feed_strategy_name.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_name)
                self.ui.machine_feed_strategy_file.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_file)
                self.ui.machine_feed_strategy_file_format.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_file_format)
                self.ui.machine_feed_strategy_triggered_start.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_triggered_start)
                self.ui.machine_feed_strategy_full_repeats.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_full_repeats)
                self.ui.machine_feed_strategy_recoater_speed.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_speed)
                self.ui.machine_feed_strategy_retract_speed.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_retract_speed)
                self.ui.machine_feed_strategy_dwell_time.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_dwell_time)
                self.ui.machine_feed_strategy_build_repeats.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_recoater_build_repeats)
                self.ui.machine_feed_strategy_comment.setPlainText(
                    Machine_Powder_Feed_Control_Strategies_list[index].Machine_powder_s_comment)
                self.ui.machine_feed_strategy_checkBox.setChecked(False)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Printing Process Instructions info has been saved successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.machine_feed_strategy_name.toPlainText().strip():
                text = self.ui.machine_feed_strategy_name.toPlainText().strip()
                if not (any(cls.Machine_powder_s_name == text for cls in Machine_Powder_Feed_Control_Strategies_list)):
                    if self.ui.selected_machine_control_strategy.count() == 0:
                        m = Machine_Powder_Feed_Control_Strategy_class()
                        mp = Machine_Powder_Feed_Control_PPI_class()
                        m.Machine_powder_s_name = self.ui.machine_feed_strategy_name.toPlainText()
                        m.Machine_powder_s_file = self.ui.machine_feed_strategy_file.toPlainText()
                        m.Machine_powder_s_file_format = self.ui.machine_feed_strategy_file_format.toPlainText()
                        m.Machine_powder_s_triggered_start = self.ui.machine_feed_strategy_triggered_start.toPlainText()
                        m.Machine_powder_s_recoater_full_repeats = self.ui.machine_feed_strategy_full_repeats.toPlainText()
                        m.Machine_powder_s_recoater_speed = self.ui.machine_feed_strategy_recoater_speed.toPlainText()
                        m.Machine_powder_s_recoater_retract_speed = self.ui.machine_feed_strategy_retract_speed.toPlainText()
                        m.Machine_powder_s_recoater_dwell_time = self.ui.machine_feed_strategy_dwell_time.toPlainText()
                        m.Machine_powder_s_recoater_build_repeats = self.ui.machine_feed_strategy_build_repeats.toPlainText()
                        m.Machine_powder_s_comment = self.ui.machine_feed_strategy_comment.toPlainText()
                        self.ui.load_machine_feed_strategy_comboBox.addItem(m.Machine_powder_s_name)
                        self.ui.defined_machine_powder_control_strategies_listwidget.addItem(m.Machine_powder_s_name)
                        Machine_Powder_Feed_Control_Strategies_list.append(m)
                        for i, cls in enumerate(Machine_Powder_Feed_Control_Strategies_list):
                            if str(cls.Machine_powder_s_name).strip() == m.Machine_powder_s_name:
                                machine_powder_strategy_index = i
                                break
                        self.ui.selected_machine_control_strategy.addItem(m.Machine_powder_s_name)
                        machine_powder_strategy = m
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Info: The info about Machine Powder Feed Control has been saved successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        m = Machine_Powder_Feed_Control_Strategy_class()
                        m.Machine_powder_s_name = self.ui.machine_feed_strategy_name.toPlainText()
                        m.Machine_powder_s_file = self.ui.machine_feed_strategy_file.toPlainText()
                        m.Machine_powder_s_file_format = self.ui.machine_feed_strategy_file_format.toPlainText()
                        m.Machine_powder_s_triggered_start = self.ui.machine_feed_strategy_triggered_start.toPlainText()
                        m.Machine_powder_s_recoater_full_repeats = self.ui.machine_feed_strategy_full_repeats.toPlainText()
                        m.Machine_powder_s_recoater_speed = self.ui.machine_feed_strategy_recoater_speed.toPlainText()
                        m.Machine_powder_s_recoater_retract_speed = self.ui.machine_feed_strategy_retract_speed.toPlainText()
                        m.Machine_powder_s_recoater_dwell_time = self.ui.machine_feed_strategy_dwell_time.toPlainText()
                        m.Machine_powder_s_recoater_build_repeats = self.ui.machine_feed_strategy_build_repeats.toPlainText()
                        m.Machine_powder_s_comment = self.ui.machine_feed_strategy_comment.toPlainText()
                        Machine_Powder_Feed_Control_Strategies_list[machine_powder_strategy_index] = m
                        self.ui.selected_machine_control_strategy.clear()
                        self.ui.selected_machine_control_strategy.addItem(m.Machine_powder_s_name)
                        self.ui.defined_machine_powder_control_strategies_listwidget.addItem(m.Machine_powder_s_name)
                        self.ui.load_machine_feed_strategy_comboBox.clear()
                        for item in Machine_Powder_Feed_Control_Strategies_list:
                            self.ui.load_machine_feed_strategy_comboBox.addItem(item.Machine_powder_s_name)
                        machine_powder_strategy = m
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Info: The info about Machine Powder Feed Control has been saved successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                else:
                    QMessageBox.critical(self, "Input Error",
                                         "The name of machine powder feed control strategy already exists.")
            else:QMessageBox.critical(self, "Input Error", "There is a missing field.")
    # =======================================================================
    def toggle_consist_layer_partcheckBox(self, state):
        if self.ui.consist_layer_partcheckBox.isChecked():
            self.ui.layer_part_comboBox.setEnabled(True)
        else:
            self.ui.layer_part_comboBox.setEnabled(False)
    # =======================================================================
    def define_PartLayerBuildModel_func(self):
        if self.ui.PartLayerBuildModel_name.toPlainText().strip():
            text = self.ui.PartLayerBuildModel_name.toPlainText().strip()
            if not (any(cls.Layer_Of_Build_Model_AM_Part_name == text for cls in Layer_Of_Build_Model_AM_Parts_list)):
                a = layer_of_Build_Model_AM_Part_class()
                a.Layer_Of_Build_Model_AM_Part_name = self.ui.PartLayerBuildModel_name.toPlainText()
                a.Layer_Of_Build_Model_AM_Part_file = self.ui.PartLayerBuildModel_file.toPlainText()
                a.Layer_Of_Build_Model_AM_Part_file_format = self.ui.PartLayerBuildModel_file_format.toPlainText()
                a.layer_of_Build_Model_AM_Part_area = self.ui.PartLayerBuildModel_area.toPlainText()
                a.layer_of_Build_Model_AM_Part_comment = self.ui.PartLayerBuildModel_comment.toPlainText()
                self.ui.layer_part_comboBox.addItem(a.Layer_Of_Build_Model_AM_Part_name)
                Layer_Of_Build_Model_AM_Parts_list.append(a)
                self.ui.list_existing_part_model_layers.addItem(a.Layer_Of_Build_Model_AM_Part_name)
                self.ui.PartLayerBuildModel_name.clear()
                self.ui.PartLayerBuildModel_file.clear()
                self.ui.PartLayerBuildModel_file_format.clear()
                self.ui.PartLayerBuildModel_area.clear()
                self.ui.PartLayerBuildModel_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Layer of Build Model AM Part has been added successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error",
                                     "The name of the Layer of Build Model AM Part already exists.")
        else:
            QMessageBox.critical(self, "Input Error",
                                 "The name of the Layer of Build Model AM Part cannot be empty or just spaces.")
    # =======================================================================
    def add_outpu_layer_decomposition_func(self):
        l = self.ui.load_layer_comboBox.currentText()
        if l and l != "-- Select an option --":
            if self.ui.consist_layer_partcheckBox.isChecked() and self.ui.layer_part_comboBox.currentText() != "-- Select an option --":
                part = self.ui.layer_part_comboBox.currentText()
                existing_items = [self.ui.list_output_part_layer_decomposition.item(i).text() for i in
                                  range(self.ui.list_output_part_layer_decomposition.count())]
                temp = 'Build Layer :' + l + '   Part Layer: ' + part
                if (l and part and (temp not in existing_items)):
                    self.ui.list_output_part_layer_decomposition.addItem('Build Layer :' + l + '   Part Layer: ' + part)
                    Layer_Of_Build_Model_AM_Parts_Layer_decomposition.append((l, part))
                    index = next(
                        (i for i, cls in enumerate(Layer_Of_Build_Models_list) if cls.Layer_Of_Build_Model_name == l),
                        -1)
                    try:
                        if index != -1:
                            temp = Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_consists_of_am_part_layer
                            if not temp:
                                temp = []
                            temp = temp.append(part)
                            Layer_Of_Build_Models_list[index].Layer_Of_Build_Model_consists_of_am_part_layer = temp
                    except:pass
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText(
                            "Info: The Layer of Build Model AM Part has been added to Layer Decomposition Process successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:print(f"Error: {e}")
            else:
                existing_items = [self.ui.list_output_part_layer_decomposition.item(i).text() for i in
                                  range(self.ui.list_output_part_layer_decomposition.count())]
                temp = 'Build Layer :' + l
                if (l and (temp not in existing_items)):
                    self.ui.list_output_part_layer_decomposition.addItem('Build Layer :' + l)
                    Layer_Of_Build_Model_AM_Parts_Layer_decomposition.append((l, ''))
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText(
                            "Info: The Layer of Build Model AM Part has been added to Layer Decomposition Process successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:print(f"Error: {e}")
    # =======================================================================
    def add_outpu_layer_decomposition_2_func(self):
        l = self.ui.load_layer_comboBox_2.currentText()
        existing_items = [self.ui.list_output_layer_decomposition.item(i).text() for i in
                          range(self.ui.list_output_layer_decomposition.count())]
        if l not in existing_items and l and l != "-- Select an option --":
            self.ui.list_output_layer_decomposition.addItem(l)
            Layer_Of_Build_Models_Layer_decomposition.append(l)
            self.ui.layer_pre_heating_ppi_correspond_layer_build_model_comboBox.addItem(l)
            self.ui.correspond_layer_build_model_combobox.addItem(l)
            self.ui.correspond_layer_build_model_combobox_2.addItem(l)
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText(
                    "Info: The Layer of Build Model has been added to Layer Decomposition Process successfully.")
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
    # =======================================================================
    def LayerBuildModel_define_func(self):
        if self.ui.LayerBuildModel_name.toPlainText().strip():
            text = self.ui.LayerBuildModel_name.toPlainText().strip()
            if not (any(cls.Layer_Of_Build_Model_name == text for cls in Layer_Of_Build_Models_list)):
                l = Layer_Of_Build_Model_class()
                l.Layer_Of_Build_Model_name = self.ui.LayerBuildModel_name.toPlainText()
                l.Layer_Of_Build_Model_layer_num = self.ui.LayerBuildModel_layer_number.toPlainText()
                l.Layer_Of_Build_Model_layer_height = self.ui.LayerBuildModel_layer_height.toPlainText()
                l.Layer_Of_Build_Model_file = self.ui.LayerBuildModel_file.toPlainText()
                l.Layer_Of_Build_Model_file_format = self.ui.LayerBuildModel_file_format.toPlainText()
                l.Layer_Of_Build_Model_comment = self.ui.LayerBuildModel_comment.toPlainText()
                self.ui.load_layer_comboBox_2.addItem(l.Layer_Of_Build_Model_name)
                Layer_Of_Build_Models_list.append(l)
                self.ui.load_layer_comboBox.addItem(l.Layer_Of_Build_Model_name)
                self.ui.list_existing_model_layers.addItem(l.Layer_Of_Build_Model_name)
                self.ui.LayerBuildModel_name.clear()
                self.ui.LayerBuildModel_layer_number.clear()
                self.ui.LayerBuildModel_layer_height.clear()
                self.ui.LayerBuildModel_file.clear()
                self.ui.LayerBuildModel_file_format.clear()
                self.ui.LayerBuildModel_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Layer of Build Model has been added successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of the Layer of Build Model already exists.")
        else:
            QMessageBox.critical(self, "Input Error",
                                 "The name of the Layer of Build Model cannot be empty or just spaces.")
    # =======================================================================
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                self.focusNextChild()
                return True
            elif event.key() == Qt.Key.Key_Up:
                self.focusPreviousChild()
                return True
            elif event.key() == Qt.Key.Key_Down:
                self.focusNextChild()
                return True
        return super().eventFilter(obj, event)
    # =======================================================================
    def define_material_func(self):
        if self.ui.material_name.toPlainText().strip():
            text = self.ui.material_name.toPlainText().strip()
            if not (any(cls.material_name == text for cls in defined_Materials)):
                m = Material_class()
                m.material_name = self.ui.material_name.toPlainText()
                m.material_melting_point = self.ui.material_melting_point.toPlainText()
                m.material_oxidation_resistance = self.ui.material_oxidation_resistance.toPlainText()
                m.material_heat_capacity = self.ui.material_heat_capacity.toPlainText()
                m.material_formula = self.ui.material__formula.toPlainText()
                m.material_density = self.ui.material_density.toPlainText()
                m.material_electrical_resistivity = self.ui.material_electrical_resitivity.toPlainText()
                m.material_eb_absorption_rate = self.ui.material_beam_absorption_rate.toPlainText()
                m.material_thermal_conductivity = self.ui.material_thermal_conductivity.toPlainText()
                m.material_electrical_conductivity = self.ui.material_electrical_conductivity.toPlainText()
                m.material_thermal_diffusivity = self.ui.material_thermal_diffusivity.toPlainText()
                m.material_comment = self.ui.material_comment.toPlainText()
                defined_Materials.append(m)
                self.ui.defined_materials_listWidget.addItem(m.material_name)
                if self.ui.build_plate_material_comboBox.findText(m.material_name) == -1:
                    self.ui.build_plate_material_comboBox.addItem(m.material_name)
                if self.ui.printing_medium_material_comboBox.findText(m.material_name) == -1:
                    self.ui.printing_medium_material_comboBox.addItem(m.material_name)
                self.ui.material_name.clear()
                self.ui.material_melting_point.clear()
                self.ui.material_oxidation_resistance.clear()
                self.ui.material_heat_capacity.clear()
                self.ui.material__formula.clear()
                self.ui.material_density.clear()
                self.ui.material_electrical_resitivity.clear()
                self.ui.material_beam_absorption_rate.clear()
                self.ui.material_thermal_conductivity.clear()
                self.ui.material_electrical_conductivity.clear()
                self.ui.material_thermal_diffusivity.clear()
                self.ui.material_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Material has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of the Material already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "The name of the Material cannot be empty or just spaces.")
    # =======================================================================
    def define_manufacturer_func(self):
        if self.ui.manufacturer_name.toPlainText().strip():
            text = self.ui.manufacturer_name.toPlainText().strip()
            if not (any(cls.manufacturer_name == text for cls in defined_Manufacturers)):
                m = Manufacturer_class()
                m.manufacturer_name = self.ui.manufacturer_name.toPlainText()
                m.manufacturer_address = self.ui.manufacturer_address.toPlainText()
                m.manufacturer_comment = self.ui.manufacturer_comment.toPlainText()
                defined_Manufacturers.append(m)
                self.ui.defined_manufactures_listWidget.addItem(m.manufacturer_name)
                if self.ui.printing_medium_manufacturer_comboBox.findText(m.manufacturer_name) == -1:
                    self.ui.printing_medium_manufacturer_comboBox.addItem(m.manufacturer_name)
                if self.ui.build_plate_manufacturer_comboBox.findText(m.manufacturer_name) == -1:
                    self.ui.build_plate_manufacturer_comboBox.addItem(m.manufacturer_name)
                self.ui.manufacturer_name.clear()
                self.ui.manufacturer_address.clear()
                self.ui.manufacturer_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Manufacturer has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of the Manufacturer already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "The name of the Manufacturer cannot be empty or just spaces.")
    # =======================================================================
    def item_exists(self, list_widget, text):
        for i in range(list_widget.count()):
            if list_widget.item(i).text() == text:
                return True
        return False
    # =======================================================================
    def define_printing_medium_func(self):
        if self.ui.printing_medium_name.toPlainText().strip():
            text = self.ui.printing_medium_name.toPlainText().strip()
            if not (any(cls.printing_medium_name == text for cls in defined_Printing_mediums)):
                m = Printing_Medium_class()
                m.printing_medium_name = self.ui.printing_medium_name.toPlainText()
                m.printing_medium_status = self.ui.printing_medium_status.toPlainText()
                if self.ui.metal_powder_checkBox.isChecked():
                    m.printing_medium_type = 'Metal Powder'
                m.printing_medium_particle_size = self.ui.printing_medium_particle_size.toPlainText()
                m.printing_medium_powder_morphology = self.ui.printing_medium_particle_morphology.toPlainText()
                if self.ui.printing_medium_material_comboBox.currentText() != "-- Select an option --":
                    m.printing_medium_material = self.ui.printing_medium_material_comboBox.currentText()
                if self.ui.printing_medium_manufacturer_comboBox.currentText() != "-- Select an option --":
                    m.printing_medium_manufacturer = self.ui.printing_medium_manufacturer_comboBox.currentText()
                m.printing_medium_comment = self.ui.printing_medium_comment.toPlainText()
                defined_Printing_mediums.append(m)
                if not self.item_exists(self.ui.defined_printing_medium_listWidget, m.printing_medium_name):
                    self.ui.defined_printing_medium_listWidget.addItem(m.printing_medium_name)
                if self.ui.printing_process_printing_medium.findText(m.printing_medium_name) == -1:
                    self.ui.printing_process_printing_medium.addItem(m.printing_medium_name)
                self.ui.printing_medium_name.clear()
                self.ui.printing_medium_status.clear()
                self.ui.metal_powder_checkBox.setChecked(False)
                self.ui.printing_medium_particle_size.clear()
                self.ui.printing_medium_particle_morphology.clear()
                self.ui.printing_medium_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Printing Medium has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of the Printing Medium already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "The name of the Printing Medium cannot be empty or just spaces.")
    # =======================================================================
    def define_build_plate_func(self):
        if self.ui.build_plate_name.toPlainText().strip():
            text = self.ui.build_plate_name.toPlainText().strip()
            if not (any(cls.build_plate_name == text for cls in defined_Build_Plates)):
                b = Build_Plate_class()
                b.build_plate_name = self.ui.build_plate_name.toPlainText()
                b.build_plate_size = self.ui.build_plate_size.toPlainText()
                b.build_plate_thickness = self.ui.build_plate_thickness.toPlainText()
                b.build_plate_surface_texture = self.ui.build_plate_surface_texture.toPlainText()
                b.build_plate_shape = self.ui.build_plate_shape.toPlainText()
                b.build_plate_comment = self.ui.build_plate_comment.toPlainText()
                if self.ui.build_plate_manufacturer_comboBox.currentText() != "-- Select an option --":
                    b.build_plate_manufacturer = self.ui.build_plate_manufacturer_comboBox.currentText()
                if self.ui.build_plate_material_comboBox.currentText() != "-- Select an option --":
                    b.build_plate_material = self.ui.build_plate_material_comboBox.currentText()
                if not self.item_exists(self.ui.defined_build_plate_listWidget, b.build_plate_name):
                    self.ui.defined_build_plate_listWidget.addItem(b.build_plate_name)
                if self.ui.printing_process_buildplate.findText(b.build_plate_name) == -1:
                    self.ui.printing_process_buildplate.addItem(b.build_plate_name)
                defined_Build_Plates.append(b)
                self.ui.build_plate_name.clear()
                self.ui.build_plate_size.clear()
                self.ui.build_plate_thickness.clear()
                self.ui.build_plate_surface_texture.clear()
                self.ui.build_plate_shape.clear()
                self.ui.build_plate_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Build Plate has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of the Build Plate already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "The name of the Build Plate cannot be empty or just spaces.")
    # =======================================================================
    def add_printed_build_PB_AM_part_func(self):
        part_name = self.ui.printed_build_PB_AM_part_comboBox.currentText()
        if (part_name != "-- Select an option --" and part_name):
            get_support = ''
            if self.ui.printed_build_PB_AM_part_has_support_checkBox.isChecked() and self.ui.printed_build_PB_AM_part_support_comboBox.currentText() != "-- Select an option --":
                get_support = self.ui.printed_build_PB_AM_part_support_comboBox.currentText()
            new_text = f"Printed Build AM Part: {part_name}   Get Support: {get_support}"
            if new_text not in [self.ui.composed_of_printed_build_PB_AM_partlistWidget.item(i).text() for i in
                                range(self.ui.composed_of_printed_build_PB_AM_partlistWidget.count())]:
                self.ui.composed_of_printed_build_PB_AM_partlistWidget.addItem(new_text)
            printed_build_parts.append(part_name)
            printed_build_support_for_part.append(get_support)
            self.ui.printed_build_PB_AM_part_comboBox.setCurrentIndex(0)
            self.ui.printed_build_PB_AM_part_support_comboBox.setCurrentIndex(0)
            self.ui.printed_build_PB_AM_part_has_support_checkBox.setAutoExclusive(False)
            self.ui.printed_build_PB_AM_part_has_support_checkBox.setChecked(False)
            self.ui.printed_build_PB_AM_part_has_support_checkBox.setAutoExclusive(True)
    # =======================================================================
    def define_printed_build_support_func(self):
        if self.ui.printed_build_support_name.toPlainText().strip():
            s = Printed_Build_Support_class()
            s.Printed_Build_Support_name = self.ui.printed_build_support_name.toPlainText()
            s.Printed_Build_Support_comment = self.ui.printed_build_support_comment.toPlainText()
            self.ui.defined_printed_build_support_listWidget.addItem(s.Printed_Build_Support_name)
            self.ui.printed_build_PB_AM_part_support_comboBox.addItem(s.Printed_Build_Support_name)
            self.ui.printed_build_support_name.clear()
            self.ui.printed_build_support_comment.clear()
            Printed_Build_Supports_list.append(s)
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText("Info: The Printed Build Support has been defined successfully.")
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error",
                                 "The name of Printed Build Support cannot be empty or just spaces.")
    # =======================================================================
    def define_printed_build_AM_part_func(self):
        if self.ui.printed_build_AM_part_name.toPlainText().strip():
            s = Printed_Build_AM_Part_class()
            s.Printed_Build_AM_Part_name = self.ui.printed_build_AM_part_name.toPlainText()
            s.Printed_Build_AM_Part_comment = self.ui.printed_build_AM_part_comment.toPlainText()
            self.ui.defined_printed_build_AM_part_listWidget.addItem(s.Printed_Build_AM_Part_name)
            self.ui.printed_build_PB_AM_part_comboBox.addItem(s.Printed_Build_AM_Part_name)
            self.ui.printed_build_AM_part_name.clear()
            self.ui.printed_build_AM_part_comment.clear()
            Printed_Build_AM_Parts_list.append(s)
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText("Info: The Printed Build AM Part has been defined successfully.")
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error",
                                 "The name of Printed Build AM Part cannot be empty or just spaces.")
    # =======================================================================
    def define_printed_build_func(self):
        if self.ui.printed_build_name.toPlainText().strip():
            text = self.ui.printed_build_name.toPlainText().strip()
            if not (any(cls.Printed_Build_name == text for cls in printed_build_list)):
                printed_build.Printed_Build_name = self.ui.printed_build_name.toPlainText()
                printed_build.Printed_Build_comment = self.ui.printed_build_comment.toPlainText()
                printed_build.Printed_Build_AM_Parts_and_supports = [
                    self.ui.composed_of_printed_build_PB_AM_partlistWidget.item(i).text() for i in
                    range(self.ui.composed_of_printed_build_PB_AM_partlistWidget.count())]
                self.ui.defined_Printed_Builds_listWidget.addItem(text)
                self.ui.printing_process_output_printe_build.addItem(text)

                printed_build_list.append(printed_build)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Printed Build has been added successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                printed_build.Printed_Build_name = self.ui.printed_build_name.toPlainText()
                printed_build.Printed_Build_comment = self.ui.printed_build_comment.toPlainText()
                printed_build.Printed_Build_AM_Parts_and_supports = [
                    self.ui.composed_of_printed_build_PB_AM_partlistWidget.item(i).text() for i in
                    range(self.ui.composed_of_printed_build_PB_AM_partlistWidget.count())]
                index = next((i for i, cls in enumerate(printed_build_list) if cls.Printed_Build_name == text), -1)
                printed_build_list[index] = printed_build
                for i in range(self.ui.defined_Printed_Builds_listWidget.count()):
                    if self.ui.defined_Printed_Builds_listWidget.item(i).text() == printed_build.Printed_Build_name:
                        removed = self.ui.defined_Printed_Builds_listWidget.takeItem(i)
                        del removed
                        break
                self.ui.defined_Printed_Builds_listWidget.addItem(printed_build.Printed_Build_name)
                self.ui.printing_process_output_printe_build.addItem(printed_build.Printed_Build_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Printed Build has been added successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error", "The name of Printed Build cannot be empty or just spaces.")
    # =======================================================================
    def define_printing_machine_func(self):
        if self.ui.printing_machine_name.toPlainText().strip():
            text = self.ui.printing_machine_name.toPlainText().strip()
            if not (any(cls.printing_machine_name == text for cls in defined_printing_machines)):
                p = Printing_Machine_class()
                p.printing_machine_name = self.ui.printing_machine_name.toPlainText()
                if self.ui.eb_pbf_freemelt_checkBox.isChecked():
                    p.printing_machine_brand = 'EB-PBF Freemelt'
                p.printing_machine_comment = self.ui.printing_machine_comment.toPlainText()
                p.printing_machine_sensor_info = [self.ui.defined_sensors_listWidget.item(i).text() for i in
                                                  range(self.ui.defined_sensors_listWidget.count())]
                self.ui.printing_process_printing_machine.addItem(p.printing_machine_name)
                self.ui.defined_printing_machines_listWidget.addItem(p.printing_machine_name)
                defined_printing_machines.append(p)
                self.ui.printing_machine_name.clear()
                self.ui.printing_machine_comment.clear()
                self.ui.eb_pbf_freemelt_checkBox.setChecked(False)
                self.ui.defined_sensors_listWidget.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Printing Machine has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of Printing Machine already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "The name of Printing Machine cannot be empty or just spaces.")
    # =======================================================================
    def add_sensor_to_printing_machine_func(self):
        if self.ui.load_sensor_checkBox.isChecked() and self.ui.load_sensor_comboBox.currentText() != "-- Select an option --":
            selected_sensor = self.ui.load_sensor_comboBox.currentText()
            sensor = next((item for item in sensors_list if item.sensor_name == selected_sensor), None)
            matching_items = self.ui.defined_sensors_listWidget.findItems(selected_sensor, Qt.MatchFlag.MatchExactly)
            if sensor and not matching_items:
                self.ui.sensor_name.clear()
                self.ui.sensor_type.clear()
                self.ui.sensor_recorde_data_path.clear()
                self.ui.sensor_name.setPlainText(sensor.sensor_name)
                self.ui.sensor_type.setPlainText(sensor.sensor_type)
                self.ui.sensor_recorde_data_path.setPlainText(sensor.recorded_data_path)
                self.ui.defined_sensors_listWidget.addItem(selected_sensor)
                self.ui.load_sensor_checkBox.setChecked(False)
                self.ui.load_sensor_comboBox.setCurrentIndex(0)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("The Sensor has been added to the Printing Machine successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.sensor_name.toPlainText().strip():
                text = self.ui.sensor_name.toPlainText().strip()
                index = next((i for i, cls in enumerate(sensors_list) if cls.sensor_name == text), -1)
                if index == -1:
                    s = Sensor_class()
                    s.sensor_name = self.ui.sensor_name.toPlainText()
                    s.sensor_type = self.ui.sensor_type.toPlainText()
                    s.recorded_data_path = self.ui.sensor_recorde_data_path.toPlainText()
                    sensors_list.append(s)
                    self.ui.existing_sensors_listWidget.addItem(s.sensor_name)
                    self.ui.load_sensor_comboBox.addItem(s.sensor_name)
                    self.ui.defined_sensors_listWidget.addItem(s.sensor_name)
                    self.ui.sensor_name.clear()
                    self.ui.sensor_type.clear()
                    self.ui.sensor_recorde_data_path.clear()
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText("Info: The Sensor has been added to the Printing Machine successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    QMessageBox.critical(self, "Input Error", "The sensor name already exists.")
            else:
                QMessageBox.critical(self, "Input Error", "The Sensor name cannot be empty or just spaces.")
    # =======================================================================
    def set_as_input_printing_process_pushButton_func(self):
        text = self.ui.input_printing_ppi_name.currentText().strip()
        if text and text != "-- Select an option --":
            self.ui.set_as_input_printing_process_listWidget.addItem(text)
    # =======================================================================
    def define_printing_process_func(self):
        if self.ui.printing_process_name.toPlainText().strip():
            Printing_Process.printing_process_name = self.ui.printing_process_name.toPlainText()
            Printing_Process_start_date_value = self.ui.printing_start_date.dateTime()
            Printing_Process.printing_process_start_date = Printing_Process_start_date_value.toString(
                "yyyy-MM-dd HH:mm:ss")
            Printing_Process_end_date_value = self.ui.printing_end_date.dateTime()
            Printing_Process.printing_process_end_date = Printing_Process_end_date_value.toString("yyyy-MM-dd HH:mm:ss")
            if self.ui.printing_finish.isChecked():
                Printing_Process.printing_process_status = 'finished'
            if self.ui.printing_unfinished.isChecked():
                Printing_Process.printing_process_status = 'unfinished'
            Printing_Process.printing_process_comment = self.ui.printing_comment.toPlainText()
            if (self.ui.printing_process_buildplate.currentText() != "-- Select an option --"):
                Printing_Process.printing_process_build_plate = self.ui.printing_process_buildplate.currentText()
            if (self.ui.printing_process_printing_medium.currentText() != "-- Select an option --"):
                Printing_Process.printing_process_printing_medium = self.ui.printing_process_printing_medium.currentText()
            if (self.ui.printing_process_printing_machine.currentText() != "-- Select an option --"):
                Printing_Process.printing_process_printing_machine = self.ui.printing_process_printing_machine.currentText()
            Printing_Process.printing_process_instructions = [
                self.ui.set_as_input_printing_process_listWidget.item(i).text() for i in
                range(self.ui.set_as_input_printing_process_listWidget.count())]
            if (self.ui.printing_process_output_printe_build.currentText() != "-- Select an option --"):
                Printing_Process.printing_process_output = self.ui.printing_process_output_printe_build.currentText()
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText("Info: The Printing Process has been defined successfully.")
                QTimer.singleShot(0, lambda: self.ui.scrollArea.verticalScrollBar().setValue(
                    self.ui.scrollArea.verticalScrollBar().minimum()))
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error", "The name of Printing Process cannot be empty or just spaces.")
    # =======================================================================
    def add_buil_model_2_func(self):
        global Build_model
        if self.ui.load_build_model_checkBox.isChecked() and self.ui.load_buildmodel_combobox.currentText() != "-- Select an option --":
            self.ui.add_buil_model_button.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                        "border: 1px solid rgb(0, 0, 127); \n"
                                                        "    border-radius: 4px;         \n"
                                                        "    padding: 4px; ")
            selected_build_model = self.ui.load_buildmodel_combobox.currentText()
            build_m = next(
                (build_mod for build_mod in Defined_Build_models if build_mod.build_model_name == selected_build_model),
                None)
            if build_m:
                Build_model = build_m
                self.ui.selected_digital_build_model.clear()
                self.ui.selected_digital_build_model.addItem(Build_model.build_model_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Build Model has been saved successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    QTimer.singleShot(0, lambda: self.ui.scrollArea.verticalScrollBar().setValue(
                        self.ui.scrollArea.verticalScrollBar().minimum()))
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
    # =======================================================================
    def add_buil_model_func(self):
        global Build_model
        if self.ui.build_model_name.toPlainText().strip():
            text = self.ui.build_model_name.toPlainText().strip()
            if not (any(cls.build_model_name == text for cls in Defined_Build_models)):
                self.ui.add_buil_model_button_2.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                              "border: 1px solid rgb(0, 0, 127); \n"
                                                              "    border-radius: 4px;         \n"
                                                              "    padding: 4px; ")
                new_build_model = output_Build_Model_Design_Process_class()
                new_build_model.build_model_name = self.ui.build_model_name.toPlainText()
                new_build_model.build_model_file_path = self.ui.build_model_file_path.toPlainText()
                new_build_model.build_model_file_format = self.ui.build_model_file_format.toPlainText()
                new_build_model.build_model_dimension = self.ui.Build_model_dimension.toPlainText()
                new_build_model.build_model_comment = self.ui.build_model_comment.toPlainText()
                items = [self.ui.part_support_in_model_list.item(i).text() for i in
                         range(self.ui.part_support_in_model_list.count())]
                new_build_model.build_model_parts_supports = items
                Defined_Build_models.append(new_build_model)
                Build_model = new_build_model
                Build_Model_Design_Process_process.ModelDesign_output = Build_model
                self.ui.load_buildmodel_combobox.addItem(Build_model.build_model_name)
                self.ui.existing_digital_build_model_listwidget.addItem(Build_model.build_model_name)
                self.ui.selected_digital_build_model.clear()
                self.ui.selected_digital_build_model.addItem(Build_model.build_model_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.setText("Info: The Build Model has been saved successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                self.ui.add_buil_model_button_2.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                              "border: 1px solid rgb(0, 0, 127); \n"
                                                              "    border-radius: 4px;         \n"
                                                              "    padding: 4px; ")
                new_build_model = output_Build_Model_Design_Process_class()
                new_build_model.build_model_name = self.ui.build_model_name.toPlainText()
                new_build_model.build_model_file_path = self.ui.build_model_file_path.toPlainText()
                new_build_model.build_model_file_format = self.ui.build_model_file_format.toPlainText()
                new_build_model.build_model_dimension = self.ui.Build_model_dimension.toPlainText()
                new_build_model.build_model_comment = self.ui.build_model_comment.toPlainText()
                items = [self.ui.part_support_in_model_list.item(i).text() for i in
                         range(self.ui.part_support_in_model_list.count())]
                new_build_model.build_model_parts_supports = items
                index = next((i for i, cls in enumerate(Defined_Build_models) if
                              cls.build_model_name == new_build_model.build_model_name), -1)
                if index != -1: Defined_Build_models[index] = new_build_model
                Build_model = new_build_model
                index = self.ui.load_buildmodel_combobox.findText(Build_model.build_model_name)
                if index != -1: self.ui.load_buildmodel_combobox.removeItem(index)
                self.ui.load_buildmodel_combobox.addItem(Build_model.build_model_name)
                for i in range(self.ui.existing_digital_build_model_listwidget.count()):
                    if self.ui.existing_digital_build_model_listwidget.item(
                            i).text() == new_build_model.build_model_name:
                        removed = self.ui.existing_digital_build_model_listwidget.takeItem(i)
                        del removed
                        break
                self.ui.existing_digital_build_model_listwidget.addItem(Build_model.build_model_name)
                self.ui.selected_digital_build_model.clear()
                self.ui.selected_digital_build_model.addItem(Build_model.build_model_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.setText("Info: The Build Model has been saved successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error", "The name of Build Model cannot be empty or just spaces.")
    # =======================================================================
    def Add_Testing_Method_func(self):
        method = applied_testing_method_class()
        if self.ui.testing_method_name_comboBox.currentText().strip() and self.ui.testing_method_name_comboBox.currentText().strip() != "-- Select an option --":
            method.applied_testing_method_name = self.ui.testing_method_name_comboBox.currentText()
            method.applied_testing_method_result = self.ui.testing_method_file.toPlainText()
            method.applied_testing_method_comment = self.ui.testing_method_comment.toPlainText()
            text = f"Testing Method: {method.applied_testing_method_name}   Result:{str(method.applied_testing_method_result)}"
            existing_items = [self.ui.Testin_process_applied_methods_list.item(i).text() for i in
                              range(self.ui.Testin_process_applied_methods_list.count())]
            if text not in existing_items:
                self.ui.Testin_process_applied_methods_list.addItem(text)
                Testing_process_applied_testing_methods.append(method)
                self.ui.testing_method_file.clear()
                self.ui.testing_method_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Testing Method has been added successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
        else:QMessageBox.critical(self, "Input Error", "Please choose a Testing Method.")
    # =======================================================================
    def Testing_Method_Okay_func(self):
        if self.ui.Testing_Process_name.toPlainText().strip():
            Testing_Process.TestingProcess_name = self.ui.Testing_Process_name.toPlainText()
            Testing_Process_start_date_value = self.ui.Testing_Process_start_date.dateTime()
            Testing_Process.TestingProcess_start_date = Testing_Process_start_date_value.toString("yyyy-MM-dd HH:mm:ss")
            Testing_Process_end_date_value = self.ui.Testing_Process_end_date.dateTime()
            Testing_Process.TestingProcess_end_date = Testing_Process_end_date_value.toString("yyyy-MM-dd HH:mm:ss")
            if self.ui.Testing_Process_finished.isChecked():
                Testing_Process.TestingProcess_status = 'finished'
            if self.ui.Testing_Process_unfinished.isChecked():
                Testing_Process.TestingProcess_status = 'unfinished'
            Testing_Process.TestingProcess_comment = self.ui.Testing_Process_comment.toPlainText()
            Testing_Process.TestingProcess_applied_methods_results = [
                self.ui.Testin_process_applied_methods_list.item(i).text() for i in
                range(self.ui.Testin_process_applied_methods_list.count())]
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                self.ui.Testing_Method_Okay_spushButton.setEnabled(False)
                self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())
                msg.setText("Info: The Testing Process has been defined successfully.")
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error", "The name of Testing Process cannot be empty or just spaces.")
    # =======================================================================
    def define_testing_method_func(self):
        testing_method = Testing_Method_class()
        if self.ui.testing_method_name.toPlainText().strip():
            text = self.ui.testing_method_name.toPlainText().strip()
            if not (any(cls.TestingMethod_name == text for cls in Testing_Methods_list)):
                testing_method.TestingMethod_name = self.ui.testing_method_name.toPlainText()
                if self.ui.non_destructive_radioButton.isChecked(): testing_method.TestingMethod_type = 'Non-Destructive'
                if self.ui.destructive_radioButton.isChecked(): testing_method.TestingMethod_type = 'Destructive'
                testing_method.TestingMethod_comment = self.ui.define_testing_method_comment.toPlainText()
                Testing_Methods_list.append(testing_method)
                self.ui.testing_method_name_comboBox.addItem(testing_method.TestingMethod_name)
                self.ui.defined_testing_methods_listwidget.addItem(testing_method.TestingMethod_name)
                self.ui.testing_method_name.clear()
                self.ui.define_testing_method_comment.clear()
                self.ui.destructive_radioButton.setAutoExclusive(False)
                self.ui.destructive_radioButton.setChecked(False)
                self.ui.destructive_radioButton.setAutoExclusive(True)
                self.ui.non_destructive_radioButton.setAutoExclusive(False)
                self.ui.non_destructive_radioButton.setChecked(False)
                self.ui.non_destructive_radioButton.setAutoExclusive(True)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Testing Method has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of Testing Method already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "The name of Testing Method cannot be empty or just spaces.")
    # =======================================================================
    def add_postprinting_methods_to_process_func(self):
        selected_value = self.ui.Post_Printing_method_comboBox.currentText()
        if (selected_value != "-- Select an option --"):
            self.ui.used_POstPrinting_methods_listWidget.addItem(selected_value)
    # =======================================================================
    def define_postPrinting_process_func(self):
        if self.ui.PostPrinting_Process_name.toPlainText().strip():
            Post_printing_Proces.post_printing_process_name = self.ui.PostPrinting_Process_name.toPlainText()
            PostPrinting_Process_start_date_value = self.ui.PostPrinting_Process_start_date.dateTime()
            Post_printing_Proces.post_printing_process_start_date = PostPrinting_Process_start_date_value.toString(
                "yyyy-MM-dd HH:mm:ss")
            PostPrinting_Process_end_date_value = self.ui.PostPrinting_Process_end_date.dateTime()
            Post_printing_Proces.post_printing_process_end_date = PostPrinting_Process_end_date_value.toString(
                "yyyy-MM-dd HH:mm:ss")
            if self.ui.PostPrinting_Process_finished.isChecked():
                Post_printing_Proces.post_printing_process_status = 'finished'
            if self.ui.PostPrinting_Process_unfinished.isChecked():
                Post_printing_Proces.post_printing_process_status = 'unfinished'
            Post_printing_Proces.post_printing_process_comment = self.ui.PostPrinting_Process_comment.toPlainText()
            Post_printing_Proces.post_printing_process_used_methods = [
                self.ui.used_POstPrinting_methods_listWidget.item(i).text() for i in
                range(self.ui.used_POstPrinting_methods_listWidget.count())]
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText("Info: The Post-Printing Process has been defined successfully.")
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error",
                                 "The name of Post-Printing Process cannot be empty or just spaces.")
    # =======================================================================
    def define_post_printing_method_func(self):
        if self.ui.post_printing_method_name.toPlainText().strip():
            text = self.ui.post_printing_method_name.toPlainText().strip()
            if not (any(cls.post_printing_method_name == text for cls in Post_Printing_Methods_list)):
                postprinting_method = Post_Printing_Method()
                postprinting_method.post_printing_method_name = self.ui.post_printing_method_name.toPlainText()
                if self.ui.support_removal_radioButton.isChecked():
                    postprinting_method.post_printing_method_type = 'Support Removal'
                if self.ui.heat_treatment_radioButton.isChecked():
                    postprinting_method.post_printing_method_type = 'Heat Treatment'
                if self.ui.build_cleaning_radioButton.isChecked():
                    postprinting_method.post_printing_method_type = 'Build Cleaning'
                if self.ui.build_seperation_radioButton.isChecked():
                    postprinting_method.post_printing_method_type = 'Build Separation From Build Plate'
                postprinting_method.post_printing_method_comment = self.ui.post_printing_method_comment.toPlainText()
                Post_Printing_Methods_list.append(postprinting_method)
                self.ui.defined_PostPrinting_methods_listWidget.addItem(postprinting_method.post_printing_method_name)
                self.ui.Post_Printing_method_comboBox.addItem(postprinting_method.post_printing_method_name)
                self.ui.post_printing_method_name.clear()
                self.ui.post_printing_method_comment.clear()
                self.ui.build_cleaning_radioButton.setAutoExclusive(False)
                self.ui.build_cleaning_radioButton.setChecked(False)
                self.ui.build_cleaning_radioButton.setAutoExclusive(True)
                self.ui.support_removal_radioButton.setAutoExclusive(False)
                self.ui.support_removal_radioButton.setChecked(False)
                self.ui.support_removal_radioButton.setAutoExclusive(True)
                self.ui.heat_treatment_radioButton.setAutoExclusive(False)
                self.ui.heat_treatment_radioButton.setChecked(False)
                self.ui.heat_treatment_radioButton.setAutoExclusive(True)
                self.ui.build_seperation_radioButton.setAutoExclusive(False)
                self.ui.build_seperation_radioButton.setChecked(False)
                self.ui.build_seperation_radioButton.setAutoExclusive(True)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: The Post-Printing Method has been defined successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "The name of Post-Printing Method already exists.")
        else:
            QMessageBox.critical(self, "Input Error",
                                 "The name of Post-Printing Method cannot be empty or just spaces.")
    # =======================================================================
    def setup_button_reset_on_groupbox_change_4(self, button, groupbox, exclude_groupboxs):
        # Step 1: Change button color when clicked
        def on_button_clicked():
            try:
                if not printed_build.Printed_Build_name == "":
                    button.setStyleSheet("background-color: green; color: white;")
                else:
                    button.setStyleSheet("")
            except Exception as e:
                print(f"Error: {e}")

        button.clicked.connect(on_button_clicked)
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QListWidget)):
            # Skip widgets inside the excluded group box
            def reset_and_log(w=widget):
                name = w.objectName() or w.__class__.__name__
                button.setStyleSheet("")
            if any(groupbox.isAncestorOf(widget) for groupbox in exclude_groupboxs):
                continue
            if isinstance(widget, QPlainTextEdit) or isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QListWidget):
                widget.model().rowsInserted.connect(lambda *args, w=widget: reset_and_log(w))
    # =======================================================================
    def setup_button_reset_on_groupbox_change_3(self, button, groupbox, exclude_groupboxs):
        # Step 1: Change button color when clicked
        def on_button_clicked():
            try:
                if not self.ui.Testing_Process_name.toPlainText().strip() == "":
                    button.setStyleSheet("background-color: green; color: white;")
                else:
                    button.setStyleSheet("")
            except Exception as e:
                print(f"Error: {e}")
        button.clicked.connect(on_button_clicked)
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QListWidget)):
            # Skip widgets inside the excluded group box
            def reset_and_log(w=widget):
                name = w.objectName() or w.__class__.__name__
                button.setStyleSheet("")
            if any(groupbox.isAncestorOf(widget) for groupbox in exclude_groupboxs):
                continue
            if isinstance(widget, QPlainTextEdit) or isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QListWidget):
                widget.model().rowsInserted.connect(lambda *args, w=widget: reset_and_log(w))
    # =======================================================================
    def setup_button_reset_on_groupbox_change_2(self, button, groupbox, exclude_groupbox=None):
        # Step 1: Change button color when clicked
        def on_button_clicked():
            try:
                if not self.ui.PostPrinting_Process_name.toPlainText().strip() == "":
                    button.setStyleSheet("background-color: green; color: white;")
                else:
                    button.setStyleSheet("")
            except Exception as e:
                print(f"Error: {e}")
        button.clicked.connect(on_button_clicked)
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QListWidget)):
            # Skip widgets inside the excluded group box
            def reset_and_log(w=widget):
                name = w.objectName() or w.__class__.__name__
                button.setStyleSheet("")
            if exclude_groupbox and exclude_groupbox.isAncestorOf(widget):
                continue
            if isinstance(widget, QPlainTextEdit) or isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QListWidget):
                widget.model().rowsInserted.connect(lambda *args, w=widget: reset_and_log(w))
    # =======================================================================
    def setup_button_reset_on_groupbox_change(self, button, groupbox):
        # Step 1: Change button color when clicked
        button.clicked.connect(lambda: button.setStyleSheet("background-color: green; color: white;"))
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QComboBox)):
            if isinstance(widget, (QPlainTextEdit)):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
                widget.textChanged.connect(lambda: button.setEnabled(True))
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
                widget.textChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
                widget.dateTimeChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
                widget.toggled.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(lambda: button.setStyleSheet(""))
                widget.currentIndexChanged.connect(lambda: button.setEnabled(True))
    # =======================================================================
    def change_button_color_if_name_entered(self, button):
        name = self.ui.ProjectName.toPlainText().strip()
        if name: button.setStyleSheet("background-color: green; color: white;")
    # =======================================================================
    def setup_button_reset_on_groupbox_change_9(self, button, groupbox):
        # Step 1: Change button color when clicked
        button.clicked.connect(lambda: self.change_button_color_if_name_entered(button))
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QComboBox)):
            if isinstance(widget, (QPlainTextEdit)):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
                widget.textChanged.connect(lambda: button.setEnabled(True))
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
                widget.textChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
                widget.dateTimeChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
                widget.toggled.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(lambda: button.setStyleSheet(""))
                widget.currentIndexChanged.connect(lambda: button.setEnabled(True))
    # =======================================================================
    def setup_button_reset_on_groupbox_change_10(self, button, groupbox):
        # Step 1: Change button color when clicked
        button.clicked.connect(lambda: self.change_button_color_if_name_entered_2(button))
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QComboBox)):
            if isinstance(widget, (QPlainTextEdit)):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
                widget.textChanged.connect(lambda: button.setEnabled(True))
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
                widget.textChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
                widget.dateTimeChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
                widget.toggled.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(lambda: button.setStyleSheet(""))
                widget.currentIndexChanged.connect(lambda: button.setEnabled(True))
    # =======================================================================
    def setup_button_reset_on_groupbox_change_11(self, button, groupbox, exclude_groupboxs=None):
        # Step 1: Change button color when clicked
        button.clicked.connect(lambda: self.change_button_color_if_name_entered_2(button))
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QListWidget)):
            # Skip widgets inside the excluded group box
            def reset_and_log(w=widget):
                name = w.objectName() or w.__class__.__name__
                button.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                     "border: 1px solid rgb(0, 0, 127); \n"
                                     "    border-radius: 4px;         \n"
                                     "    padding: 4px; ")
                button.setEnabled(True)
            try:
                if any(groupbox.isAncestorOf(widget) for groupbox in exclude_groupboxs): continue
            except:
                pass
            if isinstance(widget, QPlainTextEdit) or isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                                        "border: 1px solid rgb(0, 0, 127); \n"
                                                                        "    border-radius: 4px;         \n"
                                                                        "    padding: 4px; "))
                widget.textChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(
                    lambda: button.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                 "border: 1px solid rgb(0, 0, 127); \n"
                                                 "    border-radius: 4px;         \n"
                                                 "    padding: 4px; "))
                widget.dateTimeChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                                    "border: 1px solid rgb(0, 0, 127); \n"
                                                                    "    border-radius: 4px;         \n"
                                                                    "    padding: 4px; "))
                widget.toggled.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QListWidget):
                widget.model().rowsInserted.connect(lambda *args, w=widget: reset_and_log(w))
                widget.model().rowsRemoved.connect(lambda *args, w=widget: reset_and_log(w))
    # =======================================================================
    def change_button_color_if_name_entered_2(self, button):
        if button == self.ui.add_buil_model_button_2:
            name = self.ui.load_buildmodel_combobox.currentText().strip()
            if name and name != "-- Select an option --":  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
        if button == self.ui.okay_beam_control_strategy_pushButton:
            name = self.ui.beam_control_strategy_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
        if button == self.ui.add_machine_feed_strategy_pushButton:
            name = self.ui.machine_feed_strategy_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)

        if button == self.ui.define_printed_build_pushButton:
            name = self.ui.printed_build_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
        if button == self.ui.define_printing_instructions_pushButton:
            name = self.ui.printing_process_instructions_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)

        if button == self.ui.define_printing_process_pushButton:
            name = self.ui.printing_process_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
        if button == self.ui.Testing_Method_Okay_spushButton:
            name = self.ui.Testing_Process_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
        if button == self.ui.define_postPrinting_process_pushButton:
            name = self.ui.PostPrinting_Process_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
        if button == self.ui.add_model_design_process_button:
            name = self.ui.ModelDesign_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
        if button == self.ui.add_buil_model_button:
            name = self.ui.build_model_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
        if button == self.ui.define_monitoring_process_pushButton:
            name = self.ui.monitoring_process_name.toPlainText().strip()
            if name:  # Only change color if name is not empty
                button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: green;
                        color: white;
                    }
                """)
                button.setEnabled(False)
    # =======================================================================
    def setup_button_reset_on_groupbox_change_6(self, button, groupbox):
        # Step 1: Change button color when clicked
        def on_button_clicked():
            try:
                if not self.ui.slicing_process_name.toPlainText().strip() == "":
                    button.setStyleSheet("background-color: green; color: white;")
                else:
                    button.setStyleSheet("")
            except Exception as e:
                print(f"Error: {e}")
        button.clicked.connect(on_button_clicked)
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QListWidget)):
            # Skip widgets inside the excluded group box
            def reset_and_log(w=widget):
                name = w.objectName() or w.__class__.__name__
                button.setStyleSheet("")
                button.setEnabled(True)
            if isinstance(widget, QPlainTextEdit) or isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
                widget.textChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
                widget.dateTimeChanged.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
                widget.toggled.connect(lambda: button.setEnabled(True))
            elif isinstance(widget, QListWidget):
                widget.model().rowsInserted.connect(lambda *args, w=widget: reset_and_log(w))
    # =======================================================================
    def setup_button_reset_on_groupbox_change_7(self, button, groupbox):
        # Step 1: Change button color when clicked
        def on_button_clicked():
            try:
                text = self.ui.printing_process_instructions_name.toPlainText().strip()
                combo = self.ui.load_exist_printing_instructions_comboBox.currentText().strip()
                if text or combo:
                    button.setStyleSheet("background-color: green; color: white;")
                else:
                    button.setStyleSheet("")
            except Exception as e:
                print(f"Error: {e}")
        button.clicked.connect(on_button_clicked)
        # Step 2: Reset button color when any child widget changes
        for widget in groupbox.findChildren((QPlainTextEdit, QLineEdit, QDateTimeEdit, QRadioButton, QListWidget)):
            # Skip widgets inside the excluded group box
            def reset_and_log(w=widget):
                name = w.objectName() or w.__class__.__name__
                button.setStyleSheet("")
            if isinstance(widget, QPlainTextEdit) or isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QDateTimeEdit):
                widget.dateTimeChanged.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QRadioButton):
                widget.toggled.connect(lambda: button.setStyleSheet(""))
            elif isinstance(widget, QListWidget):
                widget.model().rowsInserted.connect(lambda *args, w=widget: reset_and_log(w))
    # =======================================================================
    def define_monitoring_process_func(self):
        if self.ui.monitoring_process_name.toPlainText().strip():
            Monitoring_Process.monitoring_process_name = self.ui.monitoring_process_name.toPlainText()
            Monitoring_Process_start_date_value = self.ui.monitoring_process_start_date.dateTime()
            Monitoring_Process.monitoring_process_start_date = Monitoring_Process_start_date_value.toString(
                "yyyy-MM-dd HH:mm:ss")
            Monitoring_Process_end_date_value = self.ui.monitoring_process_end_date.dateTime()
            Monitoring_Process.monitoring_process_end_date = Monitoring_Process_end_date_value.toString(
                "yyyy-MM-dd HH:mm:ss")
            if self.ui.monitoring_process_finished.isChecked():
                Monitoring_Process.monitoring_process_status = 'finished'
            if self.ui.monitoring_process_unfinished.isChecked():
                Monitoring_Process.monitoring_process_status = 'unfinished'
            Monitoring_Process.monitoring_process_comment = self.ui.monitoring_process_comment.toPlainText()
            Monitoring_Process.monitoring_process_output_file = self.ui.monitoring_process_output_file.toPlainText()
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                self.ui.define_monitoring_process_pushButton.setEnabled(False)
                msg.setText("Monitoring Process info has been saved successfully.")
                self.ui.scrollArea.verticalScrollBar().setValue(0)
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error", "Monitoring process name cannot be empty or just spaces.")
    # =======================================================================
    def toggle_load_sensor_comboBox(self, state):
        if self.ui.load_sensor_checkBox.isChecked():
            self.ui.load_sensor_comboBox.setEnabled(True)
        else:
            self.ui.load_sensor_comboBox.setEnabled(False)
    # =======================================================================
    def toggle_load_machine_feed_strategy_comboBox(self, state):
        if self.ui.machine_feed_strategy_checkBox.isChecked():
            self.ui.load_machine_feed_strategy_comboBox.setEnabled(True)
            self.ui.add_machine_feed_strategy_pushButton.setEnabled(True)
            self.ui.add_machine_feed_strategy_pushButton.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                                       "border: 1px solid rgb(0, 0, 127); \n"
                                                                       "    border-radius: 4px;         \n"
                                                                       "    padding: 4px; ")
        else:
            self.ui.load_machine_feed_strategy_comboBox.setEnabled(False)
    # =======================================================================
    def toggle_load_exist_printing_instructions_comboBox(self, state):
        if self.ui.load_layer_checkbox_3.isChecked():
            self.ui.load_exist_printing_instructions_comboBox.setEnabled(True)
            self.ui.define_printing_instructions_pushButton.setEnabled(True)
            self.ui.define_printing_instructions_pushButton.setStyleSheet("    background-color: rgb(230, 252, 255);\n"
                                                                          "border: 1px solid rgb(0, 0, 127); \n"
                                                                          "    border-radius: 4px;         \n"
                                                                          "    padding: 4px; ")
        else:
            self.ui.load_exist_printing_instructions_comboBox.setEnabled(False)
    # =======================================================================
    def toggle_load_existing_layer_melting_startegy_combobox(self, state):
        if self.ui.load_existing_layer_melting_startegy_checkbox.isChecked():
            self.ui.load_existing_layer_melting_startegy_combobox.setEnabled(True)
        else:
            self.ui.load_existing_layer_melting_startegy_combobox.setEnabled(False)
    # =======================================================================
    def toggle_load_existing_post_heating_combobox(self, state):
        if self.ui.load_existing_post_heating_checkbox.isChecked():
            self.ui.load_existing_post_heating_combobox.setEnabled(True)
        else:
            self.ui.load_existing_post_heating_combobox.setEnabled(False)
    # =======================================================================
    def toggle_layer_post_heating_strategy_combobox(self, state):
        if self.ui.layer_post_heating_strategy_checkbox.isChecked():
            self.ui.layer_post_heating_strategy_combobox.setEnabled(True)
        else:
            self.ui.layer_post_heating_strategy_combobox.setEnabled(False)
    # =======================================================================
    def toggle_load_an_existing_layer_post_heating_ppi_combobox(self, state):
        if self.ui.load_an_existing_layer_post_heating_ppi_checkBox.isChecked():
            self.ui.load_an_existing_layer_post_heating_ppi_combobox.setEnabled(True)
        else:
            self.ui.load_an_existing_layer_post_heating_ppi_combobox.setEnabled(False)
    # =======================================================================
    def toggle_composed_of_am_part_post_heating_ppi_combobox(self, state):
        if self.ui.composed_of_am_part_post_heating_ppi_checkBox.isChecked():
            self.ui.composed_of_am_part_post_heating_ppi_combobox.setEnabled(True)
        else:
            self.ui.composed_of_am_part_post_heating_ppi_combobox.setEnabled(False)
    # =======================================================================
    def toggle_load_an_existing_layer_pr_heating_ppi_combobox(self, state):
        if self.ui.load_an_existing_layer_pr_heating_ppi_checkBox.isChecked():
            self.ui.load_an_existing_layer_pr_heating_ppi_combobox.setEnabled(True)
        else:
            self.ui.load_an_existing_layer_pr_heating_ppi_combobox.setEnabled(False)
    # =======================================================================
    def toggle_load_an_existing_layer_pr_heating(self, state):
        if self.ui.load_an_existing_layer_pr_heating_checkBox.isChecked():
            self.ui.load_an_existing_layer_pr_heating.setEnabled(True)
        else:
            self.ui.load_an_existing_layer_pr_heating.setEnabled(False)
    # =======================================================================
    def toggle_composed_of_am_part_pre_startegies_combobox(self, state):
        if self.ui.composed_of_am_part_pre_startegies_checkBox.isChecked():
            self.ui.composed_of_am_part_pre_startegies_combobox.setEnabled(True)
        else:
            self.ui.composed_of_am_part_pre_startegies_combobox.setEnabled(False)
    # =======================================================================
    def toggle_load_start_heat_ppi_comboBox(self, state):
        if self.ui.load_start_heat_ppi_checkbox.isChecked():
            self.ui.load_start_heat_ppi_comboBox.setEnabled(True)
        else:
            self.ui.load_start_heat_ppi_comboBox.setEnabled(False)
    # =======================================================================
    def toggle_load_start_heat_startegy_comboBox(self, state):
        if self.ui.load_start_heat_startegy_checkbox.isChecked():
            self.ui.load_start_heat_startegy_comboBox.setEnabled(True)
        else:
            self.ui.load_start_heat_startegy_comboBox.setEnabled(False)
    # =======================================================================
    def toggle_load_machine_feed_instructions_comboBox(self, state):
        if self.ui.load_machine_feed_instructions_checkBox.isChecked():
            self.ui.load_machine_feed_instructions_comboBox.setEnabled(True)
        else:
            self.ui.load_machine_feed_instructions_comboBox.setEnabled(False)
    # =======================================================================
    def define_printing_instructions_func(self):
        if self.ui.load_layer_checkbox_3.isChecked() and self.ui.load_exist_printing_instructions_comboBox.currentText() != "-- Select an option --":
            selected_ppi = self.ui.load_exist_printing_instructions_comboBox.currentText()
            ppi_m = next((item for item in defined_Printing_Process_Instructions if item.ppi_name == selected_ppi),
                         None)
            if ppi_m:
                self.Printing_Process_Instructions_output = ppi_m
                index = next(
                    (i for i, cls in enumerate(defined_Printing_Process_Instructions) if cls.ppi_name == selected_ppi),
                    -1)
                self.ui.printing_process_instructions_name.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_name)
                self.ui.printing_process_instructions_file.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_file)
                self.ui.printing_process_instructions_file_format.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_file_format)
                self.ui.printing_process_instructions_layer_thicknesses.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_list_layer_thicknesses)
                self.ui.printing_process_instructions_comment.setPlainText(
                    defined_Printing_Process_Instructions[index].ppi_comment)
                self.ui.selected_ppi_slicing_process.clear()
                self.ui.selected_ppi_slicing_process.addItem(defined_Printing_Process_Instructions[index].ppi_name)
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Printing Process Instructions info has been saved successfully.")
                    self.ui.add_buil_model_button.setEnabled(False)
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "There is an error.")
        else:
            if self.ui.printing_process_instructions_name.toPlainText().strip():
                global Printing_Process_Instructions_output_index
                text = self.ui.printing_process_instructions_name.toPlainText().strip()
                if not (any(cls.ppi_name == text for cls in defined_Printing_Process_Instructions)):
                    if self.ui.selected_ppi_slicing_process.count() == 0:
                        Printing_Process_Instructions_output.ppi_name = self.ui.printing_process_instructions_name.toPlainText()
                        Printing_Process_Instructions_output.ppi_file = self.ui.printing_process_instructions_file.toPlainText()
                        Printing_Process_Instructions_output.ppi_file_format = self.ui.printing_process_instructions_file_format.toPlainText()
                        Printing_Process_Instructions_output.ppi_list_layer_thicknesses = self.ui.printing_process_instructions_layer_thicknesses.toPlainText()
                        Printing_Process_Instructions_output.ppi_comment = self.ui.printing_process_instructions_comment.toPlainText()
                        for i, cls in enumerate(defined_Printing_Process_Instructions):
                            if str(cls.ppi_name).strip() == Printing_Process_Instructions_output.ppi_name:
                                Printing_Process_Instructions_output_index = i
                                break
                        defined_Printing_Process_Instructions.append(Printing_Process_Instructions_output)
                        self.ui.selected_ppi_slicing_process.addItem(Printing_Process_Instructions_output.ppi_name)
                        self.ui.existing_ppi_listwidget.addItem(Printing_Process_Instructions_output.ppi_name)
                        self.ui.input_printing_ppi_name.addItem(Printing_Process_Instructions_output.ppi_name)
                        self.ui.load_exist_printing_instructions_comboBox.addItem(
                            Printing_Process_Instructions_output.ppi_name)
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Printing Process Instructions info has been saved successfully.")
                            self.ui.define_printing_instructions_pushButton.setEnabled(False)
                            QTimer.singleShot(0, lambda: self.ui.scrollArea.verticalScrollBar().setValue(
                                self.ui.scrollArea.verticalScrollBar().minimum()))
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        Printing_Process_Instructions_output.ppi_name = self.ui.printing_process_instructions_name.toPlainText()
                        Printing_Process_Instructions_output.ppi_file = self.ui.printing_process_instructions_file.toPlainText()
                        Printing_Process_Instructions_output.ppi_file_format = self.ui.printing_process_instructions_file_format.toPlainText()
                        Printing_Process_Instructions_output.ppi_list_layer_thicknesses = self.ui.printing_process_instructions_layer_thicknesses.toPlainText()
                        Printing_Process_Instructions_output.ppi_comment = self.ui.printing_process_instructions_comment.toPlainText()
                        defined_Printing_Process_Instructions.append(Printing_Process_Instructions_output)
                        self.ui.selected_ppi_slicing_process.clear()
                        self.ui.selected_ppi_slicing_process.addItem(Printing_Process_Instructions_output.ppi_name)
                        self.ui.existing_ppi_listwidget.addItem(Printing_Process_Instructions_output.ppi_name)
                        self.ui.input_printing_ppi_name.addItem(Printing_Process_Instructions_output.ppi_name)
                        self.ui.load_exist_printing_instructions_comboBox.addItem(
                            Printing_Process_Instructions_output.ppi_name)
                        self.ui.input_printing_ppi_name.clear()
                        for item in defined_Printing_Process_Instructions:
                            self.ui.input_printing_ppi_name.addItem(item.ppi_name)
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Printing Process Instructions info has been saved successfully.")
                            self.ui.define_printing_instructions_pushButton.setEnabled(False)
                            QTimer.singleShot(0, lambda: self.ui.scrollArea.verticalScrollBar().setValue(
                                self.ui.scrollArea.verticalScrollBar().minimum()))
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                else:
                    self.ui.define_printing_instructions_pushButton.setEnabled(True)
                    self.ui.define_printing_instructions_pushButton.setStyleSheet(
                        "    background-color: rgb(230, 252, 255);\n"
                        "border: 1px solid rgb(0, 0, 127); \n"
                        "    border-radius: 4px;         \n"
                        "    padding: 4px; ")
                    QMessageBox.critical(self, "Input Error", "Printing Process Instructions name already exists.")
            else:
                QMessageBox.critical(self, "Input Error",
                                     "Printing Process Instructions name cannot be empty or just spaces.")
    # =======================================================================
    def okay_beam_control_strategy_func(self):
        if self.ui.beam_control_strategy_name.toPlainText().strip():
            Beam_control_slicing_strategy.beam_control_slic_strategy_name = self.ui.beam_control_strategy_name.toPlainText()
            Beam_control_slicing_strategy.beam_control_slic_strategy_file = self.ui.beam_control_strategy_file.toPlainText()
            Beam_control_slicing_strategy.beam_control_slic_strategy_file_format = self.ui.beam_control_strategy_file_format.toPlainText()
            self.ui.beam_control_strategy_name_2.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_name)
            self.ui.beam_control_strategy_name_3.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_name)
            self.ui.beam_control_strategy_name_4.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_name)
            self.ui.beam_control_strategy_file_2.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_file)
            self.ui.beam_control_strategy_file_3.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_file)
            self.ui.beam_control_strategy_file_4.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_file)
            self.ui.beam_control_strategy_file_format_2.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_file_format)
            self.ui.beam_control_strategy_file_format_3.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_file_format)
            self.ui.beam_control_strategy_file_format_4.setPlainText(
                Beam_control_slicing_strategy.beam_control_slic_strategy_file_format)
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText("Beam Control Slicing Strategy info has been saved successfully.")
                self.ui.define_printing_instructions_pushButton.setEnabled(False)
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error",
                                 "The name of Beam Control Slicing Strategy cannot be empty or just spaces.")
    # =======================================================================
    def define_slicing_process_func(self):
        if self.ui.slicing_process_name.toPlainText().strip():
            Slicing_process.SlicingProcess_name = self.ui.slicing_process_name.toPlainText()
            slicingprocess_start_date_value = self.ui.slicing_start_date.dateTime()
            Slicing_process.SlicingProcess_start_date = slicingprocess_start_date_value.toString("yyyy-MM-dd HH:mm:ss")
            slicingprocess_end_date_value = self.ui.slicing_end_date.dateTime()
            Slicing_process.SlicingProcess_end_date = slicingprocess_end_date_value.toString("yyyy-MM-dd HH:mm:ss")
            if self.ui.slicing_finish.isChecked():
                Slicing_process.SlicingProcess_completion_status = 'finished'
            if self.ui.slicing_unfinished.isChecked():
                Slicing_process.SlicingProcess_completion_status = 'unfinished'
            Slicing_process.SlicingProcess_software = self.ui.slicing_software_name.toPlainText()
            Slicing_process.SlicingProcess_comment = self.ui.slicing_process_comment.toPlainText()
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                self.ui.define_slicing_process_pushButton.setEnabled(False)
                msg.setText("Slicing Process info has been saved successfully.")
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error", "Slicing process name cannot be empty or just spaces.")
    # =======================================================================
    def toggle_choose_support(self, state):
        if self.ui.has_support_checkBox.isChecked():
            self.ui.choose_support.setEnabled(True)
        else:
            self.ui.choose_support.setEnabled(False)
    # =======================================================================
    def toggle_choose_support_printing_process(self, state):
        if self.ui.printed_build_PB_AM_part_has_support_checkBox.isChecked():
            self.ui.printed_build_PB_AM_part_support_comboBox.setEnabled(True)
        else:
            self.ui.printed_build_PB_AM_part_support_comboBox.setEnabled(False)
    # =======================================================================
    def add_part_to_build_model_func_edit_window(self):
        part_name = self.edit_window.ui.choose_part.currentText()
        if part_name:
            get_support = ''
            if self.edit_window.ui.has_support_checkBox.isChecked():
                get_support = self.edit_window.ui.choose_support.currentText()
            item_text = 'AM Part: ' + part_name + '   Get Support: ' + get_support
            existing_items = [self.edit_window.ui.part_support_in_model_list.item(i).text() for i in
                              range(self.edit_window.ui.part_support_in_model_list.count())]
            if item_text not in existing_items:
                self.edit_window.ui.part_support_in_model_list.addItem(item_text)
            build_model_parts.append(part_name)
            build_model_support_for_part.append(get_support)
            self.edit_window.ui.choose_part.setCurrentIndex(0)
            self.edit_window.ui.choose_support.setCurrentIndex(0)
            self.edit_window.ui.has_support_checkBox.setAutoExclusive(False)
            self.edit_window.ui.has_support_checkBox.setChecked(False)
            self.edit_window.ui.has_support_checkBox.setAutoExclusive(True)
    # =======================================================================
    def add_part_to_build_model_func(self):
        part_name = self.ui.choose_part.currentText()
        if part_name and part_name != "-- Select an option --":
            get_support = ''
            if self.ui.has_support_checkBox.isChecked() and self.ui.choose_support.currentText() != "-- Select an option --":
                get_support = self.ui.choose_support.currentText()
            item_text = 'AM Part: ' + part_name + '   Get Support: ' + get_support
            existing_items = [self.ui.part_support_in_model_list.item(i).text() for i in
                              range(self.ui.part_support_in_model_list.count())]
            if item_text not in existing_items:
                self.ui.part_support_in_model_list.addItem(item_text)
            build_model_parts.append(part_name)
            build_model_support_for_part.append(get_support)
            self.ui.choose_part.setCurrentIndex(0)
            self.ui.choose_support.setCurrentIndex(0)
            self.ui.has_support_checkBox.setAutoExclusive(False)
            self.ui.has_support_checkBox.setChecked(False)
            self.ui.has_support_checkBox.setAutoExclusive(True)
    # =======================================================================
    def define_support_func(self):
        if self.ui.support_name.toPlainText().strip():
            text = self.ui.support_name.toPlainText().strip()
            if not (any(cls.support_name == text for cls in Build_Model_Support_list)):
                support = Build_Model_Support_class()
                support.support_name = self.ui.support_name.toPlainText()
                support.support_file_path = self.ui.support_file_path.toPlainText()
                support.support_file_format = self.ui.support_file_format.toPlainText()
                support.support_comment = self.ui.support_comment.toPlainText()
                Build_Model_Support_list.append(support)
                self.ui.supports_list.addItem(support.support_name)
                self.ui.choose_support.addItem(support.support_name)
                self.ui.support_name.clear()
                self.ui.support_file_path.clear()
                self.ui.support_file_format.clear()
                self.ui.support_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: the Build Model Support has been added successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "Support name should be unique.")
        else:
            QMessageBox.critical(self, "Input Error", "Support name cannot be empty or just spaces.")
    # =======================================================================
    def define_am_part_func(self):
        if self.ui.am_part_name.toPlainText().strip():
            text = self.ui.am_part_name.toPlainText().strip()
            if not (any(cls.am_part_name == text for cls in Build_Model_AM_Part_list)):
                part = Build_Model_AM_Part_class()
                part.am_part_name = self.ui.am_part_name.toPlainText()
                part.am_part_dimension = self.ui.am_part__dimension.toPlainText()
                part.am_part_file_path = self.ui.am_part_file_path.toPlainText()
                part.am_part_file_format = self.ui.am_part_file_format.toPlainText()
                part.am_part_comment = self.ui.am_part_comment.toPlainText()
                Build_Model_AM_Part_list.append(part)
                self.ui.parts_list.addItem(part.am_part_name)
                self.ui.choose_part.addItem(part.am_part_name)
                self.ui.am_part_name.clear()
                self.ui.am_part__dimension.clear()
                self.ui.am_part_file_path.clear()
                self.ui.am_part_file_format.clear()
                self.ui.am_part_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: the Build Model AM Part has been added successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "AM Part name should be unique.")
        else:
            QMessageBox.critical(self, "Input Error", "AM Part name cannot be empty or just spaces.")
    # =======================================================================
    def toggle_load_buildmodel_combobox(self, state):
        if self.ui.load_build_model_checkBox.isChecked():
            self.ui.load_buildmodel_combobox.setEnabled(True)
            self.ui.add_buil_model_button_2.setEnabled(True)
        else:
            self.ui.load_buildmodel_combobox.setEnabled(False)
            self.ui.add_buil_model_button_2.setEnabled(False)
        self.ui.define_build_model.setChecked(state != 2)
    # =======================================================================
    def add_model_design_process_func(self):
        if self.ui.ModelDesign_name.toPlainText().strip():
            Build_Model_Design_Process_process.ModelDesign_name = self.ui.ModelDesign_name.toPlainText()
            modelDesign_start_date_value = self.ui.ModelDesign_start.dateTime()
            Build_Model_Design_Process_process.ModelDesign_start_date = modelDesign_start_date_value.toString(
                "yyyy-MM-dd HH:mm:ss")
            modelDesign_end_date_value = self.ui.ModelDesig_end.dateTime()
            Build_Model_Design_Process_process.ModelDesign_end_date = modelDesign_end_date_value.toString(
                "yyyy-MM-dd HH:mm:ss")
            if self.ui.project_success_2.isChecked():
                Build_Model_Design_Process_process.ModelDesign_completion_status = 'finished'
            if self.ui.project_fail_2.isChecked():
                Build_Model_Design_Process_process.ModelDesign_completion_status = 'unfinished'
            Build_Model_Design_Process_process.ModelDesign_comment = self.ui.ModelDesign_comment.toPlainText()
            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                self.ui.add_model_design_process_button.setEnabled(False)
                msg.setText("Build Model Design Process info has been added successfully.")
                QTimer.singleShot(0, lambda: self.ui.scrollArea.verticalScrollBar().setValue(
                    self.ui.scrollArea.verticalScrollBar().minimum()))
                msg.show()
                QTimer.singleShot(1500, msg.close)
            except Exception as e:
                print(f"Error: {e}")
        else:
            QMessageBox.critical(self, "Input Error",
                                 "The Build Model Design Process name cannot be empty or just spaces.")
    # =======================================================================
    def define_project_button_func(self):
        if self.ui.ProjectName.toPlainText().strip():
            text = self.ui.ProjectName.toPlainText().strip()
            if not (any(cls.project_name == text for cls in PBF_AM_Process_Chains_list)):
                PBF_AM_Process_Chain.project_name = self.ui.ProjectName.toPlainText()
                if self.ui.ebpbf.isChecked():
                    PBF_AM_Process_Chain.project_type = 'EB-PBF'
                if self.ui.lbpbf.isChecked():
                    PBF_AM_Process_Chain.project_type = 'LB-PBF'
                project_start_date_value = self.ui.project_start_date.dateTime()
                PBF_AM_Process_Chain.project_start_date_value = project_start_date_value.toString("yyyy-MM-dd HH:mm:ss")
                project_end_date_value = self.ui.project_end_date.dateTime()
                PBF_AM_Process_Chain.project_end_date_value = project_end_date_value.toString("yyyy-MM-dd HH:mm:ss")
                if self.ui.project_success.isChecked():
                    PBF_AM_Process_Chain.project_status = 'Successful'
                if self.ui.project_fail.isChecked():
                    PBF_AM_Process_Chain.project_status = 'Failed'
                PBF_AM_Process_Chain.project_comment = self.ui.define_project_comment.toPlainText()
                items = [self.ui.supervisor_project_list.item(i).text() for i in
                         range(self.ui.supervisor_project_list.count())]
                PBF_AM_Process_Chain.project_selected_supervisors = items
                self.ui.ModelDesign_name.setPlainText(self.ui.ProjectName.toPlainText() + '_Build_Model_Design_Process')
                self.ui.slicing_process_name.setPlainText(self.ui.ProjectName.toPlainText() + '_Slicing_Process')
                self.ui.printing_process_name.setPlainText(self.ui.ProjectName.toPlainText() + '_Printing_Process')
                self.ui.monitoring_process_name.setPlainText(self.ui.ProjectName.toPlainText() + '_Monitoring_Process')
                self.ui.PostPrinting_Process_name.setPlainText(
                    self.ui.ProjectName.toPlainText() + '_PostPrinting_Process')
                self.ui.Testing_Process_name.setPlainText(self.ui.ProjectName.toPlainText() + '_Testing_Process')
                index = next((i for i, cls in enumerate(PBF_AM_Process_Chains_list) if
                              cls.project_name == PBF_AM_Process_Chain.project_name), -1)
                if index != -1:
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Question)
                    msg_box.setWindowTitle("Replace Existing Entry")
                    msg_box.setText(
                        f"Would you like to rewrite new information for the existing project '{PBF_AM_Process_Chain.project_name}'?")
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    response = msg_box.exec()
                    if response == QMessageBox.StandardButton.Ok:
                        PBF_AM_Process_Chains_list[index] = PBF_AM_Process_Chain
                        self.ui.define_project_button.setEnabled(False)
                        try:
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Success")
                            msg.setText("Project info has been defined successfully.")
                            msg.show()
                            QTimer.singleShot(1500, msg.close)
                        except Exception as e:
                            print(f"Error: {e}")
                        print("The existing process chain was replaced.")
                    else:
                        print("No changes were made.")
                else:
                    print("New process chain added.")
                    self.ui.define_project_button.setEnabled(False)
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText("Project info has been defined successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                        self.ui.define_project_button.setEnabled(False)
                    except Exception as e:
                        print(f"Error: {e}")
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Question)
                msg_box.setWindowTitle("Replace Existing Entry")
                msg_box.setText(
                    f"Would you like to rewrite new information for the existing project '{PBF_AM_Process_Chain.project_name}'?")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                response = msg_box.exec()
                if response == QMessageBox.StandardButton.Ok:
                    index = next((i for i, cls in enumerate(PBF_AM_Process_Chains_list) if
                                  cls.project_name == PBF_AM_Process_Chain.project_name), -1)

                    PBF_AM_Process_Chain.project_name = self.ui.ProjectName.toPlainText()
                    if self.ui.ebpbf.isChecked():
                        PBF_AM_Process_Chain.project_type = 'EB-PBF'
                    if self.ui.lbpbf.isChecked():
                        PBF_AM_Process_Chain.project_type = 'LB-PBF'
                    project_start_date_value = self.ui.project_start_date.dateTime()
                    PBF_AM_Process_Chain.project_start_date_value = project_start_date_value.toString(
                        "yyyy-MM-dd HH:mm:ss")
                    project_end_date_value = self.ui.project_end_date.dateTime()
                    PBF_AM_Process_Chain.project_end_date_value = project_end_date_value.toString("yyyy-MM-dd HH:mm:ss")
                    if self.ui.project_success.isChecked():
                        PBF_AM_Process_Chain.project_status = 'Successful'
                    if self.ui.project_fail.isChecked():
                        PBF_AM_Process_Chain.project_status = 'Failed'
                    PBF_AM_Process_Chain.project_comment = self.ui.define_project_comment.toPlainText()
                    items = [self.ui.supervisor_project_list.item(i).text() for i in
                             range(self.ui.supervisor_project_list.count())]
                    PBF_AM_Process_Chain.project_selected_supervisors = items
                    PBF_AM_Process_Chains_list[index] = PBF_AM_Process_Chain
                    self.ui.define_project_button.setEnabled(False)
                    try:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText("Project info has been defined successfully.")
                        msg.show()
                        QTimer.singleShot(1500, msg.close)
                    except Exception as e:
                        print(f"Error: {e}")
                    print("The existing process chain was replaced.")
                else:
                    print("No changes were made.")
        else:
            QMessageBox.critical(self, "Input Error", "The project name cannot be empty or just spaces.")
    # =======================================================================
    def define_supervisor_func(self):
        if self.ui.supervisor_name.toPlainText().strip():
            text = self.ui.supervisor_name.toPlainText().strip()
            if not (any(cls.supervisor_name == text for cls in supervisors_list)):
                s = Supervisor()
                s.supervisor_name = self.ui.supervisor_name.toPlainText()
                s.supervisor_comment = self.ui.supervisor_name_comment.toPlainText()
                supervisors_list_name.append(s.supervisor_name)
                supervisors_list.append(s)
                self.ui.selectSupervisor.addItem(s.supervisor_name)
                self.ui.defined_supervisors_list.addItem(s.supervisor_name)
                self.ui.supervisor_name.clear()
                self.ui.supervisor_name_comment.clear()
                try:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Success")
                    msg.setText("Info: the supervisor has been added successfully.")
                    msg.show()
                    QTimer.singleShot(1500, msg.close)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                QMessageBox.critical(self, "Input Error", "Supervisor name already exists.")
        else:
            QMessageBox.critical(self, "Input Error", "Supervisor name cannot be empty or just spaces.")
    # =======================================================================
if __name__ == "__main__":
    Layer_Pre_Heating_Strategy = Layer_Pre_Heating_Strategy_class()
    AM_Part_Layer_Pre_Heating_Strategy = AM_Part_Layer_Pre_Heating_Strategy_class()
    Layer_Pre_Heating_PPI = Layer_Pre_Heating_PPI_class()
    AM_Part_Layer_Pre_Heating_PPI = AM_Part_Layer_Pre_Heating_PPI_class()
    Layer_Pre_Heating_Strategies_list = []
    Layer_Pre_Heating_Strategies_list_used_in_project = []
    Layer_Post_Heating_Strategies_list_used_in_project = []
    Layer_Melting_Strategies_list_used_in_project = []
    AM_Part_Layer_Pre_Heating_Strategies_list = []
    Layer_Pre_Heating_PPI_list = []
    Layer_Pre_Heating_PPI_list_used_in_project = []
    AM_Part_Layer_Pre_Heating_PPI_list = []
    AM_Part_Layer_Pre_Heating_PPI_list_used_in_project = []
    Layer_Post_Heating_Strategy = Layer_Post_Heating_Strategy_class()
    AM_Part_Layer_Post_Heating_Strategy = AM_Part_Layer_Post_Heating_Strategy_class()
    Layer_Post_Heating_PPI = Layer_Post_Heating_PPI_class()
    AM_Part_Layer_Post_Heating_PPI = AM_Part_Layer_Post_Heating_PPI_class()
    Layer_Post_Heating_Strategies_list = []
    AM_Part_Layer_Post_Heating_Strategies_list = []
    Layer_Post_Heating_PPI_list = []
    Layer_Post_Heating_PPI_list_used_in_project = []
    AM_Part_Layer_Post_Heating_PPI_list = []
    Layer_Melting_Strategy = Layer_Melting_Strategy_class()
    AM_Part_Layer_Melting_Strategy = AM_Part_Layer_Melting_Strategy_class()
    Layer_Melting_PPI = Layer_Melting_PPI_class()
    AM_Part_Layer_Melting_PPI = AM_Part_Layer_Melting_PPI_class()
    Layer_Melting_Strategies_list = []
    AM_Part_Layer_Melting_Strategies_list = []
    Layer_Melting_PPI_list = []
    Layer_Melting_PPI_list_used_in_project = []
    AM_Part_Layer_Melting_PPI_list = []
    Scan_Strategies_list = []
    Start_Heating_Strategy_list = []
    start_heating_strategies_in_project = []
    start_heating_strategy_index = -1
    Start_Heating_PPI_list = []
    start_heating_PPIs_in_project = []
    Layer_Of_Build_Models_list = []
    Layer_Of_Build_Model_AM_Parts_list = []
    Layer_Of_Build_Models_Layer_decomposition = []
    Layer_Of_Build_Model_AM_Parts_Layer_decomposition = []
    Machine_Powder_Feed_Control_Strategis_list = []
    Machine_Powder_Feed_Control_Strategy_PPIs_list = []
    Machine_Powder_Feed_Control_Strategy_PPIs_in_project = []
    Machine_Powder_Feed_Control_Strategies_list = []
    Machine_Powder_Feed_Control_Strategies_list_in_project = []
    machine_powder_strategy = Machine_Powder_Feed_Control_Strategy_class()
    machine_powder_strategy_index = -1
    machine_powder_strategy_PPI = Machine_Powder_Feed_Control_PPI_class()
    Printing_Process_Instructions_output_index = -1
    Printing_Process_Instructions_output = Printing_Process_Instructions_class()
    defined_Printing_Process_Instructions = []
    Printing_Process = Printing_Process_class()
    defined_printing_machines = []
    # ------------------------------------------------------------------
    supervisors_list_name = []
    supervisors_list = []
    global error_flag
    error_flag = 0
    PBF_AMP_Onto_classes = []
    PBF_AM_Process_Chain = PBF_AM_Process_Chain_class()
    PBF_AM_Process_Chains_list = []
    Build_Model_Design_Process_process = Build_Model_Design_Process_class()
    Build_Model_Support_list = []
    Build_Model_AM_Part_list = []
    Slicing_process = Slicing_Process_class()
    Monitoring_Process = Monitoring_Process_class()
    Post_Printing_Methods_list = []
    Post_printing_Proces = Post_Printing_Process_class()
    Testing_Methods_list = []
    Testing_process_applied_testing_methods = []
    Testing_Process = Testing_Process_class()
    global Build_model
    Build_model = output_Build_Model_Design_Process_class()
    Beam_control_slicing_strategy = Beam_Control_Slicing_Strategy_class()
    build_model_parts = []
    build_model_support_for_part = []
    printed_build_parts = []
    printed_build_support_for_part = []
    Defined_Build_models = []
    defined_printing_machines = []
    sensors_list = []
    Printed_Build_Supports_list = []
    Printed_Build_AM_Parts_list = []
    printed_build = Printed_Build_class()
    printed_build_list = []
    defined_Materials = []
    defined_Manufacturers = []
    defined_Printing_mediums = []
    defined_Build_Plates = []
    SHARED_DATA_PATH = "shared_project_data.pkl"
    current_project_path = None
    # ---------------------------get all concept names from the ontologies------------------------------
    concept_names_definition = []
    g = Graph()
    g.parse("PBFAMP_ontology/PBF-AMP-Onto-EB-v2.rdf", format="xml")
    classes = set(g.subjects(RDF.type, OWL.Class))
    named_classes = [cls for cls in classes if not isinstance(cls, BNode)]
    for cls in named_classes:
        class_name = cls.split("#")[-1]
        PBF_AMP_Onto_classes.append(class_name)
    for s in g.subjects(RDF.type, OWL.Class):
        label = g.value(s, RDFS.label)
        comment = g.value(s, RDFS.comment)
        if comment:
            concept_names_definition.append({

                "uri": str(s),
                "label": str(label) if label else str(s).split("#")[-1],
                "comment": str(comment) if comment else "No comment available"

            })
    # ---------------------------------------------------------
    g.parse("PBFAMP_ontology/PBF-AMP-Onto-AMPCore-v2.rdf", format="xml")
    classes = set(g.subjects(RDF.type, OWL.Class))
    named_classes = [cls for cls in classes if not isinstance(cls, BNode)]
    for cls in named_classes:
        class_name = cls.split("#")[-1]
        PBF_AMP_Onto_classes.append(class_name)
    for s in g.subjects(RDF.type, OWL.Class):
        label = g.value(s, RDFS.label)
        comment = g.value(s, RDFS.comment)
        if comment:
            concept_names_definition.append({

            "uri": str(s),
            "label": str(label) if label else str(s).split("#")[-1],
            "comment": str(comment) if comment else "No comment available"

            })
    # ---------------------------------------------------------
    g.parse("PBFAMP_ontology/PBF-AMP-Onto-Core-v3.rdf", format="xml")
    classes = set(g.subjects(RDF.type, OWL.Class))
    named_classes = [cls for cls in classes if not isinstance(cls, BNode)]
    for cls in named_classes:
        class_name = cls.split("#")[-1]
        PBF_AMP_Onto_classes.append(class_name)
    for s in g.subjects(RDF.type, OWL.Class):
        label = g.value(s, RDFS.label)
        comment = g.value(s, RDFS.comment)
        if comment:

            concept_names_definition.append({

                "uri": str(s),
                "label": str(label) if label else str(s).split("#")[-1],
                "comment": str(comment) if comment else "No comment available"

            })
    # ---------------------------------------------------------
    app = QApplication(sys.argv)
    window = MyApp()
    window.load_program()
    window.show()
    sys.exit(app.exec())
# ************************************************************************************