import glob
import xlrd
import sqlite3
from datetime import time
from datetime import datetime
ab = sqlite3.connect("Data1.sqlite")
"""TABLE 3: MDI Data"""

path = "../2014-2020 - MDI Deliveries.xlsx"
inputWorkbook = xlrd.open_workbook(path)
inputWorksheet = inputWorkbook.sheet_by_index(0)




ab.execute("CREATE TABLE IF NOT EXISTS polyol_bank (polyol_index_id INTEGER PRIMARY KEY, polyol_timestamp_start, "
           "polyol_timestamp_end, polyol_bulk_OH_number, polyol_fraction_HPU, polyol_fraction_Investa)")
path = "../2014-2020 - Polyester Polyol.xlsx"
inputWorkbook = xlrd.open_workbook(path)
inputWorksheetPolyol = inputWorkbook.sheet_by_index(0)
timestamp_list = []
columns_of_interest = (1, 9, 10, 13)
column_indicators = (6, 7)
row_range = range(1, inputWorksheetPolyol.nrows - 6)
for row1 in row_range:
    if inputWorksheetPolyol.cell_value(row1, 6) != "" or inputWorksheetPolyol.cell_value(row1, 7) != "" \
            or row1 == inputWorksheetPolyol.nrows - 7:
        time_value = inputWorksheetPolyol.cell_value(row1, 1)
        a1_as_datetime = datetime(*xlrd.xldate_as_tuple(time_value, inputWorkbook.datemode))

        timestamp = datetime.timestamp(a1_as_datetime)
        timestamp_list.append(timestamp)

x1 = 0
polyol_index_id = 0
for row1 in row_range:
    if inputWorksheetPolyol.cell_value(row1, 6) != "" or inputWorksheetPolyol.cell_value(row1, 7) != "" or row1 == inputWorksheetPolyol.nrows - 7:

        if x1 == 0:
            timestamp_start = "-"
        else:
            timestamp_start = timestamp_list[x1 - 1]
        timestamp_end = timestamp_list[x1]
        decimal_HPU = round(inputWorksheetPolyol.cell_value(row1, 9), 2)
        decimal_Investa = round(inputWorksheetPolyol.cell_value(row1, 10), 2)
        Bulk_OH_number = round(inputWorksheetPolyol.cell_value(row1, 13), 2)
        if timestamp_start != timestamp_end:
            a = (timestamp_start, timestamp_end, Bulk_OH_number, decimal_HPU, decimal_Investa)
            ab.execute("INSERT INTO polyol_bank (polyol_index_id, polyol_timestamp_start, polyol_timestamp_end, "
                       "polyol_bulk_OH_number, polyol_fraction_HPU, "
                       "polyol_fraction_Investa) VALUES (?, ?, ?, ?, ?, ?)"
                       "", (polyol_index_id, timestamp_start, timestamp_end, Bulk_OH_number, decimal_HPU, decimal_Investa))
            polyol_index_id += 1
        x1 += 1

ab.execute("CREATE TABLE IF NOT EXISTS MDI_bank (MDI_timestamp_start TIMESTAMP, MDI_timestamp_end TIMESTAMP,"
           " MDI_Blend_Index_id INTEGER PTIMARY KEY, MDI_Blended_Acidity REAL, MDI_Blended_pNCO_Content REAL, MDI_Blended_Viscosity REAL)")
rowcount = inputWorksheet.nrows
Rows_of_Interest = range(2, rowcount - 4)
Columns_of_Interest = [7, 8, 9]
T_list = []
e = 0

for rows in Rows_of_Interest:
    for columns in Columns_of_Interest:
        x = inputWorksheet.cell_value(rows, columns)
        a1 = inputWorksheet.cell_value(rowx=rows, colx=1)
        a1_as_datetime = datetime(*xlrd.xldate_as_tuple(a1, inputWorkbook.datemode))

        if inputWorksheet.cell_value(rows, columns) != "" or rows == rowcount-6 and columns == 7:

            package = []
            T = (datetime.timestamp(a1_as_datetime))
            Blended_Acidity = round(inputWorksheet.cell_value(rows, 23), 2)
            Blended_pNCO_Content = round(inputWorksheet.cell_value(rows, 29), 2)
            Blended_Viscosity = round(inputWorksheet.cell_value(rows, 35), 2)
            T_list.append(T)
            """Finding the ending timestamp"""
            if e == 0:
                starttime = "-"
                start_ts = "-"
                end_ts = T_list[e]
                e += 1
            else:
                start_ts = T_list[e-1]
                end_ts = T_list[e]


                e += 1
            package.append((start_ts, end_ts, T, Blended_Acidity, Blended_pNCO_Content, Blended_Viscosity))
            ab.execute("INSERT INTO MDI_bank (MDI_timestamp_start, MDI_timestamp_end, "
                       "MDI_Blend_Index_id, MDI_Blended_Acidity, MDI_Blended_pNCO_Content, "
                       "MDI_Blended_Viscosity) VALUES (?, ?, ?, ?, ?, ?)",
                       (start_ts, end_ts, e, Blended_Acidity, Blended_pNCO_Content, Blended_Viscosity))

# for row in ab.execute("SELECT * FROM MDI_bank ORDER BY timestamp_end"):

# Correct
"""TABLE 2: Run Data"""


"""Values will include beginning date, end date, premix comp, OH num, density """
ab.execute("CREATE TABLE IF NOT EXISTS run_bank (run_timestamp_start TIMESTAMP, run_timestamp_end TIMESTAMP, "
           "MDI_Blend_Index_id_run, Polyol_Index_id_run, Run_number TEXT PRIMARY KEY, Polyol_part_by_weight REAL, "
           "Surfactant_part_by_weight REAL, TCPP_part_by_weight REAL, Epon_part_by_weight REAL, "
           "Water_part_by_weight REAL, Cat1_part_by_weight REAL, Cat2_part_by_weight REAL, Cat3a_part_by_weight REAL,"
           " Cat3b_part_by_weight REAL, BlowingAgent_part_by_weight REAL, Polyester_OH_content REAL,"
           " Surfactant_OH_content REAL, TCPP_OH_content REAL, Epon_OH_content REAL, Water_OH_content REAL, "
           "Cat1_OH_content REAL, Cat2_OH_content REAL, Cat3a_OH_content REAL,"
           " Cat3b_OH_content REAL, BlowingAgent_OH_content REAL, Density_Block_Timestamp_1, Density_Block_Timestamp_2,"
           " Density_Block_Timestamp_3, Density_Block_Timestamp_4)")

"""Finding Timestamp range for the Run & Density"""
"""Label_list serves as our index for our variables. These are inputted Manually. Make sure that this is alright"""
"""To Do: Delete query below"""
# RunLabelList = ("run_timestamp_start", "run_timestamp_end", "Blend_Index_id", "Run_Number", "Polyol_pbw",
#          "Surfactant_pbw", "TCPP_pbw", "Epon_pbw", "Water_pbw", "Cat1_pbw", "Cat2_pbw", "Cat3a_pbw","Cat3b_pbw",
#          "BlowingAgent_pbw", "PolyestterOH", "SurfactantOH", "TCPP_OH", "EponOH", "WaterOH", "Cat1OH", "Cat2OH", "Cat3a_OH", "Cat3b_OH", "Blowing_AgentOH")

for file_name in glob.glob('../2020 ISO Production XL Data/**'):
    path = file_name
    inputWorkbook = xlrd.open_workbook(path)
    inputWorksheet = inputWorkbook.sheet_by_index(0)
    inputWorksheet2 = inputWorkbook.sheet_by_index(1)
    package2 = []
    def Dt_time_to_ts(date_row, date_column, time_row, time_column):
        Date_ts = 0
        times = xlrd.xldate_as_tuple(inputWorksheet.cell_value(time_row, time_column), inputWorkbook.datemode)
        date = xlrd.xldate_as_tuple(inputWorksheet.cell_value(date_row, date_column), inputWorkbook.datemode)
        time_value = time(*times[3:])
        Full_Date = datetime.strptime("{0}-{1}-{2} ".format(date[1], date[2], date[0]) + str(time_value),'%m-%d-%Y %H:%M:%S')
        Date_ts = datetime.timestamp(Full_Date)
        return Date_ts

    run_start_ts = Dt_time_to_ts(1, 12, 14, 2)
    if str(inputWorksheet.cell_value(15, 5)) == "":

        try:
            run_end_ts = Dt_time_to_ts(1, 12, 14, 5)
        except TypeError:
            run_end_ts = "NA"
    else:
        run_end_ts = Dt_time_to_ts(1, 12, 15, 5)


    def Batch_ID_to_Run(run_start_ts, run_end_ts):
        for row1 in ab.execute("SELECT * FROM MDI_bank ORDER BY MDI_timestamp_end"):
            run_batch_index = row1[2]
            if row1[0] == "-":
                batch_start_ts = 0
            else:
                batch_start_ts = row1[0]
            batch_end_ts = row1[1]
            if run_start_ts >= batch_start_ts and run_end_ts <= batch_end_ts:
                return run_batch_index
            else:
                pass


    def Polyol_ID_to_Run(run_start_ts, run_end_ts):
        for row1 in ab.execute("SELECT * FROM polyol_bank ORDER BY polyol_timestamp_end"):
            polyol_batch_index = row1[0]
            if row1[1] == "-":
                batch_start_ts = 0
            else:
                batch_start_ts = row1[1]
            batch_end_ts = row1[2]
            if run_start_ts >= batch_start_ts and run_end_ts <= batch_end_ts:
                return polyol_batch_index
            else:
                pass


    """Find Batch ID"""
    package2.append(run_start_ts)
    package2.append(run_end_ts)
    hello = Batch_ID_to_Run(run_start_ts, run_end_ts)
    package2.append(hello)
    world = Polyol_ID_to_Run(run_start_ts, run_end_ts)
    package2.append(world)

    """Find Run Number"""
    Run = inputWorksheet.cell_value(0, 10)
    package2.append(Run)
    """Density time values are recorded below"""
    """Finding density_batch_ID"""
    if inputWorksheet.cell_value(48,3) == "Top":
        Density_RowValues = [49, 50, 51, 52]
    else:
        Density_RowValues = [48, 49, 50, 51]
    Density_ColValues = [3, 7, 12]
    if inputWorksheet.cell_value(47,0) == "Chemical efficiency":
        Density_RowValues = [53, 54, 55, 56]

    Dens_Block = 0
    col_ort = inputWorksheet.cell_value(3, 16)

    for row in Density_RowValues:
        Dens_Package = []
        if inputWorksheet.cell_value(row, 3) != "":
            for column in Density_ColValues:
                if column == 3:

                    ts = Dt_time_to_ts(1, 12, row, column)
                    date = datetime.fromtimestamp(ts)
                    Density_blend_index_number = Batch_ID_to_Run(ts, ts)
                    Dens_Package.append(ts)
                    Dens_Package.append(Density_blend_index_number)


                else:
                    Dens_Package.append(inputWorksheet.cell_value(row, column))
            Dens_Package.append(Run)
            Block_Name = "Density_Block {}".format(Dens_Block)
            Dens_Package.append(Block_Name)

            Dens_Block += 1
            # d_p = tuple(Dens_Package)
            # (Density_ts, Run_Number, Density_Block_num, Blend_Index_Number, Polyol_Index_Number, Gauge_num, Density) = d_p
            # ab.execute("INSERT INTO density_bank (Density_timestamp, Run_number, Density_Block_num, Blend_Index_id, Gauge_num, Density)"
            #            "VALUES(?, ?, ?, ?, ?, ?)", (Density_ts, Run_Number, Density_Block_num, Blend_Index_Number, Gauge_num, Density))
        # else:
            # break
    """Finding Premix Data"""
    if inputWorksheet.cell_value(8, 15) == "RED X64":

        PMX_pRows = [3, 4, 5, 6, 7, 11, 12, 13, 14, 15]
    else:
        PMX_pRows = [3, 4, 5, 6, 7, 10, 11, 12, 13, 14]

    if type(inputWorksheet.cell_value(3, 16)) == float and inputWorksheet.cell_value(3, 16) != 1465 and inputWorksheet.cell_value(3, 16) != 5150:
        PMX_pCols = [16, 17]

    else:
        PMX_pCols = [17, 18]

    for column in PMX_pCols:
        for row in PMX_pRows:
            package2.append(inputWorksheet.cell_value(row, column))

    # ========== QC BLOCK TIMESTAMPS ==========
    if inputWorksheet.cell_value(48,3) == "Top":
        QCts_rows = [49, 50, 51, 52]
    else:
        QCts_rows = [48, 49, 50, 51]
    if inputWorksheet.cell_value(47,0) == "Chemical efficiency":
        QCts_rows = [53, 54, 55, 56]
    QCts_cols = 3
    for qcts_row in QCts_rows:
        if inputWorksheet.cell_value(qcts_row, QCts_cols) != "":

            package2.append(Dt_time_to_ts(1, 12, qcts_row, QCts_cols))
        else:
            package2.append("N/A")
    i = tuple(package2)
    (ts_start, ts_end, Blend_Index_Number, Polyol_Index_Number, Run_number, Polyol_pbw,Surfactant_pbw, TCPP_pbw, Epon_pbw, Water_pbw,
     Cat1_pbw, Cat2_pbw, Cat3a_pbw, Cat3b_pbw,BlowingAgent_pbw, PolyestterOH,
     SurfactantOH, TCPP_OH, EponOH, WaterOH, Cat1OH, Cat2OH, Cat3a_OH,Cat3b_OH, BlowingAgentOH, QCTS1, QCTS2, QCTS3, QCTS4) = i

    ab.execute("INSERT INTO run_bank (run_timestamp_start, run_timestamp_end, "
               "MDI_Blend_Index_id_run, Polyol_Index_id_run, Run_number, Polyol_part_by_weight, "
               "Surfactant_part_by_weight, TCPP_part_by_weight, Epon_part_by_weight, "
               "Water_part_by_weight, Cat1_part_by_weight, Cat2_part_by_weight, Cat3a_part_by_weight,"
               " Cat3b_part_by_weight, BlowingAgent_part_by_weight, Polyester_OH_content,"
               " Surfactant_OH_content, TCPP_OH_content, Epon_OH_content, Water_OH_content, "
               "Cat1_OH_content, Cat2_OH_content, Cat3a_OH_content,"
               " Cat3b_OH_content, BlowingAgent_OH_content, Density_Block_Timestamp_1, Density_Block_Timestamp_2,"
               " Density_Block_Timestamp_3, Density_Block_Timestamp_4)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ts_start, ts_end, Blend_Index_Number, Polyol_Index_Number, Run_number, Polyol_pbw, Surfactant_pbw, TCPP_pbw, Epon_pbw,
                Water_pbw, Cat1_pbw, Cat2_pbw, Cat3a_pbw, Cat3b_pbw, BlowingAgent_pbw, PolyestterOH,SurfactantOH,
                TCPP_OH, EponOH, WaterOH, Cat1OH, Cat2OH, Cat3a_OH, Cat3b_OH, BlowingAgentOH, QCTS1, QCTS2, QCTS3, QCTS4))


# DONE

"""TABLE 1"""

"""Label_list serves as our index for our variables. These are inputted Manually. Make sure that this is alright"""
DatapointLabelList = ("timestamp", "date", "run", "MDI_batch_index_id", "density", "description", "time", "BSide_PRX",
                      "MDI_flowrate", "Cat_1_flowrate", "Cat_2_flowrate", "Cat_3", "Pentane_MDI",
              "Pentane_PRX", "Totl_Throughput", "Totl_Percent_Cat", "Blowing_Ratio",
              "Pentane_Split_Percent_MDI", "Premix_Temperature", "ASide_MDI_Temperature",
              "Pentane_Temperature", "Ambient", "Manifold_back_pressure", "MDI_Line_Pressure",
              "Polyol_Line_Pressure", "Mixer_Speed", "Conveyor_Speed", "Nucleation_Air_flow")
ab.execute("CREATE TABLE IF NOT EXISTS data_bank (timestamp TIMESTAMP PRIMARY KEY,date TEXT, run TEXT,"
           " MDI_Batch_Index_id INTEGER, density REAL, product_description TEXT, time TEXT, premix_flowrate REAL, MDI_flowrate REAL, "
           "Cat_1_flowrate REAL, Cat_2_flowrate REAL, Cat_3_flowrate REAL, Pentane_flowrate_MDI REAL, "
           "Pentane_flowrate_Premix REAL, Total_Throughput REAL, Total_percent_Catalyst REAL, Blowing_Ratio REAL, Pentane_split_percent_MDI REAL,"
           " Premix_Temperature REAL, MDI_Temperature REAL, Pentane_Temperature REAL, Ambient_Temperature REAL,"
           " Manifold_back_pressure REAL, MDI_Line_Pressure REAL,"
           " Polyol_Line_Pressure REAL, Mixer_Speed INTEGER, Conveyor_Speed REAL, Nucleation_Air_flow REAl)")
for file_name in glob.glob('../2020 ISO Production XL Data/**'):
    path = file_name
    inputWorkbook = xlrd.open_workbook(path)
    inputWorksheet = inputWorkbook.sheet_by_index(0)
    inputWorksheet2 = inputWorkbook.sheet_by_index(1)
    columns = [3, 4, 5, 6, 7, 8, 9, 10]
    rows = range(18, 39, 1)



    """Finding the Date Value for this spreadsheet. adjusting it to a format that I appreciate"""
    date = inputWorksheet.cell_value(1,12)
    date_values = xlrd.xldate_as_tuple(inputWorksheet.cell_value(1, 12), inputWorkbook.datemode)
    Date = ("{0}-{1}-{2}".format(date_values[1], date_values[2], date_values[0]))
    gg = datetime.strptime("{0}-{1}-{2}".format(date_values[1], date_values[2], date_values[0]), '%m-%d-%Y')
    hello = datetime.isoformat(gg)
    YearValue = date_values[0]
    """Finding the run number"""
    Run = inputWorksheet.cell_value(0, 10)
    """Finding the Density"""
    Dens = inputWorksheet.cell_value(0,6)
    """Finding the Description"""
    Desc = inputWorksheet.cell_value(1,4)


    """This code delivers avery point attribute from our data. it will collect all information to be organized"""
    for x in columns:
        package = []
        if inputWorksheet.cell_value(17, x) != "":
            """to begin, we had to create timestamps as keys. This way, the runs would each have unique values ordered from oldest run to newest run"""
            date_values = xlrd.xldate_as_tuple(inputWorksheet.cell_value(1, 12), inputWorkbook.datemode)
            time_dp = xlrd.xldate_as_tuple(inputWorksheet.cell_value(17, x), inputWorkbook.datemode)
            time_value = time(*time_dp[3:])
            Full_Date = datetime.strptime("{0}-{1}-{2} ".format(date_values[1], date_values[2], date_values[0]) + str(time_value),'%m-%d-%Y %H:%M:%S')
            Date_ts = datetime.timestamp(Full_Date)
        """Finding MDI Batch Number"""
        MDIBN = Batch_ID_to_Run(Date_ts, Date_ts)

        package.append(Date_ts)
        package.append(Date)
        package.append(str(Run))
        package.append(MDIBN)
        package.append(Dens)
        package.append(Desc)
        if inputWorksheet.cell_value(17, x) != "":
            date_values = xlrd.xldate_as_tuple(inputWorksheet.cell_value(17, x), inputWorkbook.datemode)
            time_value = time(*date_values[3:])
            package.append(str(time_value))


        for y in rows:
            Label = inputWorksheet.cell_value(y, 1)
            if Label == "":
                Label = inputWorksheet.cell_value(y, 0)
            if inputWorksheet.cell_value(17, x) != "":
                if y == 23 and inputWorksheet.cell_value(0, 6) == 4 or y == 23 and inputWorksheet.cell_value(0, 6) == 6:
                    package.append(0)
                else:
                    package.append(inputWorksheet.cell_value(y,x))
        if inputWorksheet.cell_value(17, x) != "":
            h = tuple(package)
            (date_ts1, date1, run1, MDIBN, dens1, desc1, time1, fBSide_PRX, fASide_MDI, fCat_1, fCat_2, fCat_3, fPentane_MDI1,
             fPentane_PRX1, Totl_Throughput1, Totl_pCat1, Blowing_Ratio1, Pentane_Split_pMDI1,
             tPremix1, tASide_MDI1, tPentane1, tAmbient1, Manifold_back_pressure1, MDI_Line_Pressure1,
             Polyol_Line_Pressure1, Mixer_Speed1, Conveyor_Speed1, Nucleation_Air_flow1) = h
            ab.execute("INSERT INTO data_bank (timestamp, date, run,"
                       " MDI_Batch_Index_id, density, product_description, time, premix_flowrate, MDI_flowrate, "
                       "Cat_1_flowrate, Cat_2_flowrate, Cat_3_flowrate, Pentane_flowrate_MDI, "
                       "Pentane_flowrate_Premix, Total_Throughput, Total_percent_Catalyst, Blowing_Ratio, Pentane_flowrate_MDI,"
                       " Premix_Temperature, MDI_Temperature, Pentane_Temperature, Ambient_Temperature,"
                       " Manifold_back_pressure, MDI_Line_Pressure,"
                       " Polyol_Line_Pressure, Mixer_Speed, Conveyor_Speed, Nucleation_Air_flow)" 
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                       , (date_ts1, date1, run1, MDIBN, dens1, desc1, time1, fBSide_PRX, fASide_MDI, fCat_1, fCat_2,
                          fCat_3, fPentane_MDI1,
                        fPentane_PRX1, Totl_Throughput1, Totl_pCat1, Blowing_Ratio1, Pentane_Split_pMDI1,
                        tPremix1, tASide_MDI1, tPentane1, tAmbient1, Manifold_back_pressure1, MDI_Line_Pressure1,
                        Polyol_Line_Pressure1, Mixer_Speed1, Conveyor_Speed1, Nucleation_Air_flow1))

# documenting what is going on here
def finding_datapoint_timestamp(qc_run, run_sample):
    time_options = []
    options = []
    # print(qc_run)
    if qc_run == "20-27" or qc_run == "20-12A":
        dts = None
        g = None
        return g
    else:
        for row in ab.execute("SELECT Density_Block_Timestamp_1, Density_Block_Timestamp_2,"
                              " Density_Block_Timestamp_3, Density_Block_Timestamp_4"
                              " FROM run_bank WHERE Run_number == '{}'".format(qc_run)):
            dts = row[run_sample]
        if dts is not None and dts != 'N/A':
            for rowdata in ab.execute("SELECT timestamp FROM data_bank WHERE run == '{}'".format(qc_run)):

                time_options.append(rowdata[0])
                # print(rowdata[0])
                options.append(abs(int(rowdata[0]) - dts))
            f = min(options)
            e = options.index(f)
            g = time_options[e]
            print(g)
        else:
            g = None

        return g

    # we have a sorted list





"""Label_list serves as our index for our variables. These are inputted Manually. Make sure that this is alright"""
"""Label_list serves as our index for our variables. These are inputted Manually. Make sure that this is alright"""
QCLabelList = ["Production_Date_Timestamp", "Label", "Run_Number", "Cut_Date", "Block_Number", "DenZ1", "DenZ5", "DenZ7", "K_FactorZ1",
              "K_FactorZ5", "K_FactorZ7", "Friability", "Average_cold_aging", "Average_PR_CSZ1", "Average_PR_CSZ5",
              "Average_PR_CSZ7", "Tot_Average_PR_CS", "PW_CSZ1", "PW_CSZ3", "PL_CSZ2"]
ab.execute("CREATE TABLE IF NOT EXISTS QC_bank (QC_Production_Date_Timestamp TIMESTAMP, QC_Label TEXT PRIMARY KEY, Run_Number TEXT, "
           "QC_cut_date, QC_Block_Number INTEGER, Density_Zone_1, Density_Zone_5, Density_Zone_7, K_Factor_Zone_1, K_Factor_Zone_5, K_Factor_Zone_7, Friability, "
           "Average_cold_aging, Average_Parralel_to_Rise_Compressive_Strength_Zone1, Average_Parrallel_to_Rise_Compressive_Strength_Zone5"
           ", Average_Parrallel_to_Rise_Compressive_Strength_Zone7, Average_Parrallel_to_Rise_Compressive_Strength,"
           " Perpendicular_to_Width_Compressive_Strength_Zone1, Perpendicular_to_Width_Compressive_Strength_Zone5, "
           "Perpendicular_to_Length_Compressive_Strength_Zone2, Datapoint_Timestamp)")
block_list = []  # (date_ts, block) we will find a way to tally the blocks:
# IF they are in the same Date, they are appended to a list which they are is then put in rising order.
# the QC taken number is then created (1 being block 1 and so on) until we have the taken number for all QC Entries.
# We then pair these taken numbers back to the file and use this number to retrieve our Density_Block_Timestamp from
stupid_run_list = []
QC_index = []
run_index = []
for file_name in glob.glob('../ISO QC Data/*.xlsx'):
    print(file_name)
    path = file_name
    inputWorkbook = xlrd.open_workbook(path)
    inputWorksheet = inputWorkbook.sheet_by_index(0)
    Run_Number = inputWorksheet.cell_value(4, 6)

    """Finding Block Number"""
    Block_row = 5

    if inputWorksheet.cell_value(5, 6) == str:
        Block_column = 7
    else:
        Block_column = 6
    Block_Number = int(inputWorksheet.cell_value(Block_row, Block_column))


    """Finding Label"""
    run_index.append(Run_Number)
    QC_index.append((Run_Number, Block_Number))

for run_entry in run_index:
    blocks_that_run = []
    for entry in QC_index:
        if run_entry == entry[0]:
            blocks_that_run.append(entry[1])
    blocks_that_run.sort()

    for entry in QC_index:
        if run_entry == entry[0]:
            stupid_run_list.append((entry, blocks_that_run.index(entry[1])))
# print(stupid_run_list)





for file_name in glob.glob('../ISO QC Data/*.xlsx'):
    # print(file_name)
    path = file_name
    inputWorkbook = xlrd.open_workbook(path)
    inputWorksheet = inputWorkbook.sheet_by_index(0)
    QC_package = []
    def beating_a_timestamp_into_place(run_number, block_number):
        block_index_value = []

        for entry in stupid_run_list:
            if entry[0][0] == run_number and entry[0][1] == block_number:
                block_index_value.append(entry[1])
            else:
                pass
        if len(block_index_value) == 0:
            block_index = None
        else:
            block_index = block_index_value[0]
        return block_index


    def Str_to_ts_adjustment(date_row, date_column):
        Date = inputWorksheet.cell_value(date_row, date_column).split("/")
        DateValues = datetime.strptime("{0}-{1}-{2}".format(Date[0], Date[1], str(int(Date[2])+2000)), '%m-%d-%Y')

    def Average(List):
        try:
            return round(sum(List)/len(List), 3)
        except TypeError:
            return "N/A"

    """Finding Run_Number"""

    Run_Number = inputWorksheet.cell_value(4, 6)
    """Finding Production_date_ts"""
    if str(inputWorksheet.cell_value(4,2)) == "Production Date":
        row = 4
        column = 3
        Production_Date = inputWorksheet.cell_value(5,2)
    else:
        Production_Date = inputWorksheet.cell_value(4,2)
        row = 4
        column = 2

    if type(Production_Date) is str:
        try:
            DateValues = datetime.strptime(inputWorksheet.cell_value(row, column), '%m/%d/%Y')
        except ValueError:
            Cut_Date1 = inputWorksheet.cell_value(row, column).split('/')
            DateValues = datetime.strptime("{0}-{1}-{2}".format(Cut_Date1[0], Cut_Date1[1], str(int(Cut_Date1[2]) + 2000)), '%m-%d-%Y')
        Date_ts = datetime.timestamp(DateValues)


    else:
        float_date = xlrd.xldate_as_datetime(inputWorksheet.cell_value(row, column), datemode=0)
        Date_ts = datetime.timestamp(float_date)


    """Finding Cut Date"""
    Cut_Date = inputWorksheet.cell_value(5,2)
    if type(Production_Date) is str:
        try:
            DateValues = datetime.strptime(inputWorksheet.cell_value(5, 2), '%m/%d/%Y')
        except ValueError:
            Cut_Date1 = inputWorksheet.cell_value(row, column).split('/')
            DateValues = datetime.strptime("{0}-{1}-{2}".format(Cut_Date1[0], Cut_Date1[1], str(int(Cut_Date1[2]) + 2000)), '%m-%d-%Y')
        CutDate_ts = datetime.timestamp(DateValues)


    else:
        float_date = xlrd.xldate_as_datetime(inputWorksheet.cell_value(row, column), datemode=0)
        CutDate_ts = datetime.timestamp(float_date)


    """Finding Block Number"""
    Block_row = 5

    if inputWorksheet.cell_value(5, 6) == str:
        Block_column = 7
    else:
        Block_column = 6
    Block_Number = int(inputWorksheet.cell_value(Block_row, Block_column))


    """Finding Label"""
    Label = "{0} Block Number {1}".format(Run_Number, Block_Number)
    QC_package.append(Date_ts)
    QC_package.append(Label)
    QC_package.append(Run_Number)
    QC_package.append(CutDate_ts)
    QC_package.append(Block_Number)
    ave = beating_a_timestamp_into_place(Run_Number, Block_Number)
    # print(Run_Number)

    # print(ave)  # this indicates

    """Density Blocks Z1,5,7"""
    ref = [1, 5, 7]
    Density_rows = [12,15,18]
    Density_column = 2
    k_factor_column = 3
    for drow in Density_rows:
        Density = round(inputWorksheet.cell_value(drow, Density_column), 3)

        QC_package.append(Density)
    for krow in Density_rows:
        try:
            K_factor = round(inputWorksheet.cell_value(krow, k_factor_column), 4)
        except TypeError:
            K_factor = "N/A"

        QC_package.append(K_factor)


    """Friability"""
    Friability = inputWorksheet.cell_value(12, 5)
    if inputWorksheet.cell_value(12, 5) == "":
        Friability = "N/A"
    QC_package.append(Friability)

    """Average Cold Aging"""
    Average_Cold_Aging = round((inputWorksheet.cell_value(22,7)*100), 4)
    if Average_Cold_Aging == -100:
        Average_Cold_Aging = "N/A"
    QC_package.append(Average_Cold_Aging)


    """Average Parrallel to Rise CS"""

    PRClistZ1 = []
    PRClistZ5 = []
    PRClistZ7 = []
    PRCSrowsZone1 = [12, 13, 14]
    PRCSrowsZone5 = [15, 16, 17]
    PRCSrowsZone7 = [18, 19, 20]
    AveragePRCSrow = 21
    PRCScol = 9

    for row in PRCSrowsZone1:
        PRClistZ1.append(inputWorksheet.cell_value(row, PRCScol))
    for row in PRCSrowsZone5:
        PRClistZ5.append(inputWorksheet.cell_value(row, PRCScol))
    for row in PRCSrowsZone7:
        PRClistZ7.append(inputWorksheet.cell_value(row, PRCScol))
    PR_CS_Z1 = Average(PRClistZ1)
    QC_package.append(PR_CS_Z1)
    PR_CS_Z5 = Average(PRClistZ5)
    QC_package.append(PR_CS_Z5)
    PR_CS_Z7 = Average(PRClistZ7)
    QC_package.append(PR_CS_Z7)
    """Average of the Block"""
    Tot_Average_PR_CS = round(inputWorksheet.cell_value(AveragePRCSrow, PRCScol), 3)
    if inputWorksheet.cell_value(AveragePRCSrow, PRCScol) == 7:
        Tot_Average_PR_CS = "N/A"
    QC_package.append(Tot_Average_PR_CS)
    """PW & PL Averages"""
    PW_Cols = [10, 11]
    PL_Col = 12
    PWL_Row = 15
    for column in PW_Cols:
        if inputWorksheet.cell_value(PWL_Row, column) == 7:
            PW_value = "NA"
        else:
            PW_value = round(inputWorksheet.cell_value(PWL_Row, column), 3)


        QC_package.append(PW_value)
    if inputWorksheet.cell_value(PWL_Row, PL_Col) == 7:
        PL_value = "N/A"
    else:
        PL_value = round(inputWorksheet.cell_value(PWL_Row, PL_Col), 3)
    QC_package.append(PL_value)
    e = 0
    for item in QC_package:
        e += 1
    time_link = finding_datapoint_timestamp(qc_run=Run_Number, run_sample=ave)
    QC_package.append(time_link)
    h = tuple(QC_package)
    (Production_Date, Label, Run_Number, Cut_Date, Block_Number, DenZ1, DenZ5, DenZ7,K_FactorZ1,
     K_FactorZ5, K_FactorZ7, Friability, Average_cold_aging, Average_PR_CSZ1, Average_PR_CSZ5,
     Average_PR_CSZ7, Tot_Average_PR_CS, PW_CSZ1, PW_CSZ3, PL_CSZ2, nearest_datapoint) = h
    ab.execute("INSERT INTO QC_bank (QC_Production_Date_Timestamp, QC_Label, Run_Number, "
               "QC_cut_date, QC_Block_Number, Density_Zone_1, Density_Zone_5, Density_Zone_7, K_Factor_Zone_1, K_Factor_Zone_5, K_Factor_Zone_7, Friability, "
               "Average_cold_aging, Average_Parralel_to_Rise_Compressive_Strength_Zone1, Average_Parrallel_to_Rise_Compressive_Strength_Zone5"
               ", Average_Parrallel_to_Rise_Compressive_Strength_Zone7, Average_Parrallel_to_Rise_Compressive_Strength,"
               " Perpendicular_to_Width_Compressive_Strength_Zone1, Perpendicular_to_Width_Compressive_Strength_Zone5, "
               "Perpendicular_to_Length_Compressive_Strength_Zone2, Datapoint_Timestamp) "
               "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (Production_Date, Label, Run_Number,
                Cut_Date, Block_Number, DenZ1, DenZ5, DenZ7, K_FactorZ1, K_FactorZ5, K_FactorZ7, Friability, Average_cold_aging,
                Average_PR_CSZ1, Average_PR_CSZ5, Average_PR_CSZ7, Tot_Average_PR_CS, PW_CSZ1, PW_CSZ3, PL_CSZ2, nearest_datapoint))


# g = ab.execute("SELECT * FROM data_bank")
# for line in g:
#     print(line)
#
#
# for row in g:
#     for value in row:

ab.commit()
ab.close()

