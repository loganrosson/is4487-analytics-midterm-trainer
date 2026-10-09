#!/usr/bin/env python3
"""
IS 4487 - Business Analytics Midterm Trainer
============================================
One self-contained file.  Python 3.8+ with tkinter (ships with Python).

    python IS4487_Midterm_Trainer.py

The quizzes need nothing else.  The CODE LAB (dev mode) and the live cheat-sheet results run real
pandas code, so for those install the course libraries once:

    pip install pandas matplotlib seaborn scikit-learn

WHO WROTE WHAT  (every question is tagged on screen)
  * YOUR PROFESSOR'S: only the Canvas practice exam (PM1-PM22; Q21 is the essay E1) and the review-page
    samples (RP1-RP5), 26 questions plus 1 essay.  Canvas never showed the answer key, so the keys for these
    were worked out from the readings and labs.  Some PM answer choices are shortened from the Canvas
    wording, and the code shown with PM3, PM7, PM8, RP2, RP4 and RP5 was added so the Code Lab can run it.
  * WRITTEN BY CLAUDE: everything else (75 concept drills, 37 code-reading questions, 17 business cases,
    essays E2-E9, the model answers and all 64 flashcards).  They are practice questions meant to match
    your professor's style, not actual exam questions.

What's inside
  * Practice Midterm (the Canvas questions + review-page samples), Professor's Questions Only, Concept Drills
    by week, Code Reading, Business Cases, and an EXAM SIMULATION with a 60-minute clock and 2 essays
  * CODE LAB (press F2 on any question): runs the question's pandas code ONE STATEMENT AT A TIME on the real
    lab data and shows exactly what each line changed - rows, columns, types, missing values, new variables,
    printed output and charts - with an optional "predict first" mode
  * When you miss a question: why the right answer is right, why YOUR pick isn't (hand-written notes on
    the tricky options), what the code really outputs, the code narrated in words, and the key terms to review
  * CHEAT SHEETS (F3): pandas toolkit with live results, formulas, CRISP-DM, data types & prep, business
    understanding, plus calculators (IQR fences, z-score, min-max, describe-my-numbers) and a Try-it box
  * Short-essay practice with a live word count and a key-point checker, flashcards you can mark as known,
    Weak Spots (your accuracy by topic and skill, saved between sessions), colored code, light / dark mode

Safety notes
  * Everything runs locally: no network access.  The one file this trainer writes is your progress,
    ~/.is4487_trainer_progress.json (accuracy per question + known flashcards).  Weak Spots can erase it.
  * Code that runs in the Code Lab / Playground / Try-it box (including the built-in questions) is limited:
    8-second time limit, imports restricted to pandas / numpy / matplotlib / seaborn / scikit-learn / math-style
    modules, no open(), no exec/eval, no writing files, no network, no subprocesses, and read_csv only knows
    the embedded course datasets.  This is a safety net, not a security sandbox, so only paste code you trust.
  * The datasets are small embedded SAMPLES of the real lab files, so some counts differ from the full files.
"""
import ast
import base64
import builtins
import contextlib
import csv
import io
import json
import keyword
import os
import random
import re
import sys
import textwrap
import time
import tokenize
import warnings

import textwrap

# ===========================================================================
# Embedded datasets (small samples of the real lab files)
# ===========================================================================
DATA = {}

# Lab 6/7 - megatelco_leave_survey_data_cleaning_v2.csv (40 real rows, chosen
# so the sample still has the missing values, outliers and duplicate the full
# file has)
DATA["megatelco"] = """college,income,data_overage_mb,data_leftover_mb,data_mb_used,text_message_count,house,handset_price,over_15mins_calls_per_month,average_call_duration,reported_satisfaction,reported_usage_level,considering_change_of_plan,leave,id,operating_system
one,370398.0,232,80.0,6981.0,173,1288667,1222.0,4.0,16.0,low,low,no,STAY,14432,IOS
one,385283.0,237,39.0,2700.0,134,992299,-200.0,15.0,18.0,low,low,,STAY,488,IOS
zero,140516.0,0,0.0,2040.0,83,484244,1313.0,,10.0,low,low,yes,LEAVE,13391,IOS
one,112549.0,61,0.0,2678.0,155,650876,271.0,3.0,10.0,low,low,no,LEAVE,789,Android
zero,430430.0,0,89.0,,83,1312382,766.0,0.0,1.0,low,low,yes,STAY,9,Android
one,269289.0,161,52.0,949.0,136,1125604,1261.0,4.0,5000.0,low,low,yes,STAY,743,IOS
one,112128.0,217,0.0,3615.0,141,1185468,432.0,23.0,9.0,low,low,yes,LEAVE,15422,Android
zero,74302.0,0,0.0,7951.0,135,1220756,455.0,0.0,8.0,high,low,no,STAY,10765,Android
one,279209.0,0,10.0,3317.0,96,1070968,125000.0,1.0,1.0,high,low,no,STAY,5395,Android
zero,323277.0,177,7.0,3797.0,128,848675,363.0,20.0,6.0,high,high,yes,STAY,7417,Android
zero,338040.0,0,54.0,1164.0,215,860666,857.0,0.0,2.0,low,low,yes,STAY,3669,IOS
one,65967.0,0,0.0,5880.0,94,702787,518.0,0.0,,high,high,yes,LEAVE,9356,Android
zero,413235.0,213,55.0,7896.0,191,1043633,759.0,13.0,7.0,low,low,yes,STAY,8315,Android
one,87425.0,128,24.0,2500.0,126,362948,761.0,0.0,5.0,low,low,yes,LEAVE,16080,Android
one,177897.0,69,16.0,3542.0,114,920016,1339.0,5.0,9.0,low,high,,STAY,7954,IOS
one,170684.0,263,56.0,6851.0,141,507359,312.0,0.0,13.0,low,low,no,LEAVE,22256,Android
zero,231332.0,255,82.0,2883.0,200,612489,1130.0,17.0,7.0,low,low,no,STAY,13108,IOS
zero,101978.0,179,46.0,5281.0,116,1204092,396.0,14.0,8.0,low,low,,STAY,10186,Android
zero,360737.0,71,27.0,,90,522645,1060.0,5.0,2.0,low,high,yes,LEAVE,8470,IOS
one,,0,0.0,7091.0,125,524422,850.0,1.0,14.0,high,low,,LEAVE,17243,IOS
zero,119105.0,112,60.0,7825.0,92,1366352,999.0,34.0,13.0,avg,low,yes,STAY,7741,IOS
one,58967.0,0,,4456.0,62,413376,431.0,1.0,1.0,high,high,yes,LEAVE,17643,Android
one,109552.0,73,62.0,621.0,130,1219203,648.0,3.0,2.0,low,high,yes,STAY,19922,Android
one,138785.0,303,11.0,6371.0,5000,1101434,1149.0,22.0,10.0,high,low,no,STAY,12638,IOS
zero,-65000.0,0,0.0,6444.0,160,542857,993.0,0.0,11.0,low,high,no,STAY,467,IOS
one,368308.0,187,0.0,6922.0,126,582124,,13.0,11.0,avg,high,yes,STAY,16231,Android
zero,230792.0,169,0.0,7653.0,196,496113,1281.0,10.0,14.0,low,low,,LEAVE,16771,IOS
one,324903.0,129,5.0,4056.0,204,368142,705.0,21.0,6.0,low,low,no,LEAVE,13678,Android
one,343617.0,289,72.0,5471.0,84,991036,347.0,3.0,13.0,high,high,yes,LEAVE,19997,Android
zero,315761.0,199,0.0,2975.0,54,951428,,14.0,11.0,low,low,yes,LEAVE,2738,Android
zero,145400.0,171,55.0,1931.0,89,696987,693.0,6.0,9.0,low,low,yes,STAY,19826,Android
one,212173.0,293,5.0,4437.0,101,826252,530.0,5.0,15.0,avg,high,yes,LEAVE,19656,Android
zero,299921.0,143,9.0,4306.0,209,1225172,823.0,10.0,7.0,high,low,yes,STAY,16168,IOS
zero,280581.0,0,0.0,1275.0,98,349262,359.0,1.0,,high,high,yes,LEAVE,13884,Android
zero,72590.0,0,34.0,2142.0,106,-463,469.0,0.0,1.0,low,low,no,LEAVE,3419,Android
one,324903.0,129,5.0,4056.0,204,368142,705.0,21.0,6.0,low,low,no,LEAVE,13678,Android
one,,210,18.0,1299.0,128,1409759,280.0,29.0,6.0,low,low,no,STAY,18206,Android
one,67952.0,263,13.0,4544.0,183,378271,308.0,,4.0,avg,high,yes,LEAVE,7774,Android
one,343653.0,59,,5073.0,105,894148,887.0,5.0,9.0,low,low,yes,STAY,6852,IOS
one,57164.0,177,70.0,2792.0,157,1157502,569.0,0.0,9.0,high,low,yes,STAY,12359,Android
"""

# Practice Midterm - Spotifool dataset (the 22 rows shown in the exam image)
DATA["spotifool"] = """song_id,artist_popularity,song_duration,danceability,energy,loudness,speechiness,acousticness,instrumentalness,tempo,valence,downloads
1,52,195,0.482893,0.623953,-14.923,0.907195,0.595132,0.913788,113,0.699641,43043
2,93,273,0.556849,0.411295,-18.0401,0.670732,0.009924,0.952815,174,0.989952,15059
3,15,263,0.318169,0.658824,-25.6088,0.560441,0.464095,0.326743,198,0.303155,33639
4,72,298,0.203353,0.141168,-18.974,0.110989,0.963499,0.354425,147,0.45091,9302
5,61,205,0.649558,0.884383,-27.9548,0.447056,0.519032,0.505634,108,0.532043,74343
6,21,148,0.359767,0.97614,-29.2256,0.460358,0.677542,0.941121,174,0.224214,40705
7,83,188,0.623114,0.97199,-25.945,0.864564,0.311864,0.876319,122,0.172935,99250
8,87,166,0.238926,0.774687,-1.10655,0.546648,0.773991,0.102568,163,0.846751,34659
9,75,213,0.533026,0.217078,-13.5141,0.380401,0.772921,0.392731,142,0.979115,12016
10,75,263,0.57933,0.782437,-1.02534,0.9768,0.521296,0.553371,162,0.464253,50992
11,88,295,0.146641,0.122128,-17.0251,0.110721,0.976014,0.503132,76,0.178885,29586
12,100,204,0.402944,0.119911,-20.6455,0.422548,0.12555,0.193863,65,0.159231,30980
13,24,158,0.220973,0.391249,-14.8157,0.042025,0.016948,0.858817,87,0.902186,52591
14,3,219,0.157037,0.539779,-16.8146,0.739904,0.770158,0.676941,97,0.517433,48266
15,22,152,0.990964,0.793367,-26.8301,0.918077,0.807156,0.837908,178,0.388025,39237
16,53,220,0.390118,0.714966,-10.7752,0.280037,0.120207,0.858764,96,0.528815,9765
17,2,142,0.828887,0.501312,-23.5189,0.858342,0.265583,0.748356,174,0.386474,71490
18,88,129,0.329177,0.346264,-11.4124,0.292218,0.017552,0.439211,127,0.540132,92217
19,30,188,0.713352,0.997412,-10.494,0.91077,0.293309,0.610547,102,0.873601,15886
20,38,219,0.784205,0.483563,-25.4393,0.753962,0.773142,0.160365,117,0.633071,37925
21,2,153,0.636075,0.506248,-28.1595,0.804907,0.517961,0.673645,72,0.725188,43754
22,64,299,0.524419,0.247261,-6.57715,0.018007,0.348096,0.179253,111,0.428204,90363
"""

# Labs 4/5 - rent.csv (30 real San Francisco listings, text columns removed)
DATA["rent"] = """post_id,year,nhood,city,price,beds,baths,sqft,room_in_apt
pre2013_66045,2012,san francisco,san francisco,590,1,,895,0
pre2013_145191,2006,outer sunset,san francisco,1250,2,,,0
pre2013_39815,2011,civic / van ness,san francisco,1225,0,,,0
pre2013_94140,2004,lower pac hts,san francisco,2650,2,,,0
pre2013_145680,2006,nob hill,san francisco,2400,1,,,0
pre2013_100405,2004,mission district,san francisco,1425,1,,,0
4262676260,2013,nob hill,san francisco,2650,1,,950,0
pre2013_142749,2005,inner richmond,san francisco,1450,2,1,,0
pre2013_93496,2004,mission district,san francisco,2400,3,,,0
pre2013_94203,2004,marina / cow hollow,san francisco,1414,2,,,0
pre2013_158237,2006,san francisco,san francisco,1325,1,1,,0
pre2013_1028,2006,castro,san francisco,2900,2,,,0
5461285625,2016,bernal,san francisco,2995,2,,900,0
pre2013_99561,2004,USF / anza vista,san francisco,1090,0,,,0
4771972949,2014,pacific heights,san francisco,2850,0,1,,0
pre2013_97644,2004,outer richmond,san francisco,1200,2,,,0
3562468438,2013,inner sunset,san francisco,2523,1,,644,0
pre2013_89605,2004,mission district,san francisco,900,0,,,0
pre2013_96457,2004,presidio hts / laurel hts / lake st,san francisco,1350,1,,,0
pre2013_55240,2012,financial district,san francisco,2800,3,2,1500,0
5280403483,2015,nob hill,san francisco,4445,1,,,0
pre2013_69936,2012,mission district,san francisco,2550,2,,,0
pre2013_58752,2012,SOMA / south beach,san francisco,3880,2,,1500,0
pre2013_127749,2004,mission district,san francisco,1950,3,,,0
pre2013_130191,2004,haight ashbury,san francisco,2500,2,,,0
5493725126,2016,haight ashbury,san francisco,5250,3,,1700,0
pre2013_125474,2004,presidio hts / laurel hts / lake st,san francisco,1250,1,1,,0
pre2013_136802,2005,marina / cow hollow,san francisco,2500,2,,,0
pre2013_137339,2005,nob hill,san francisco,33000,2,,,0
pre2013_69003,2012,SOMA / south beach,san francisco,4200,2,,14500,0
"""

# Week 5 case - fintrust_loans.csv (30 real rows)
DATA["fintrust"] = """Loan_ID,Gender,Age,Married,Education,EmploymentStatus,ApplicantIncome,LoanAmount,LoanTerm,CreditScore,HasPreviousDefaults,LoanStatus
LN1004,Male,50,No,Not Graduate,Employed,2129,215788.0,,795.0,0,Paid
LN1008,Male,35,No,Not Graduate,Employed,4457,,360.0,604.0,0,Paid
LN1009,Female,63,No,Not Graduate,Unemployed,4642,41506.0,240.0,,0,Paid
LN1012,Male,33,No,Not Graduate,Unemployed,4427,,180.0,686.0,0,Paid
LN1028,Female,45,Yes,Graduate,Self-Employed,6399,,60.0,,1,Paid
LN1164,Female,50,No,Not Graduate,Self-Employed,8854,-24040.0,60.0,657.0,0,Paid
LN1058,Male,22,Yes,Not Graduate,Unemployed,4108,158992.0,120.0,559.0,0,Paid
LN1040,Male,29,Yes,Not Graduate,Employed,9175,73799.0,120.0,753.0,0,Paid
LN1034,Female,61,Yes,Graduate,Unemployed,4312,169180.0,120.0,725.0,0,Paid
LN1102,Female,38,No,Graduate,Employed,6445,82526.0,360.0,636.0,0,Defaulted
LN1184,Male,49,No,Not Graduate,Employed,3943,131483.0,36.0,607.0,0,Paid
LN1198,Male,23,No,Graduate,Self-Employed,4014,224756.0,360.0,600.0,1,Defaulted
LN1095,Female,40,Yes,Not Graduate,Employed,5603,,180.0,640.0,0,Defaulted
LN1029,Female,59,No,Not Graduate,Employed,3857,,60.0,547.0,0,Defaulted
LN1168,Male,47,No,Graduate,Employed,1882,216193.0,240.0,531.0,0,Defaulted
LN1171,Male,41,Yes,Not Graduate,Employed,5305,173127.0,240.0,572.0,1,Paid
LN1018,Female,62,No,Graduate,Unemployed,5585,118857.0,36.0,652.0,0,Defaulted
LN1011,Male,56,Yes,Graduate,Employed,4061,122753.0,360.0,679.0,0,Paid
LN1089,Female,40,No,Graduate,Self-Employed,5123,194325.0,36.0,510.0,0,Paid
LN1110,Female,50,No,Graduate,Employed,5255,195991.0,60.0,664.0,0,Paid
LN1118,Female,32,Yes,Graduate,Self-Employed,7673,99694.0,,671.0,0,Paid
LN1159,Female,37,Yes,Not Graduate,Unemployed,5223,102465.0,36.0,689.0,1,Paid
LN1035,Male,23,No,Not Graduate,Employed,4539,31513.0,120.0,647.0,1,Paid
LN1136,Male,60,Yes,Not Graduate,Self-Employed,6278,125201.0,360.0,637.0,0,Defaulted
LN1059,Male,48,Yes,Graduate,Employed,5882,133257.0,180.0,731.0,0,Defaulted
LN1051,Female,32,Yes,Not Graduate,Unemployed,3451,,180.0,624.0,0,Paid
LN1016,Female,48,Yes,Graduate,Unemployed,1245,257761.0,180.0,770.0,0,Defaulted
LN1044,Female,64,Yes,Not Graduate,Unemployed,4097,178698.0,120.0,684.0,0,Defaulted
LN1094,Female,39,Yes,Not Graduate,Self-Employed,7264,,120.0,796.0,0,Paid
LN1031,Male,21,No,Not Graduate,Employed,3496,175514.0,,723.0,0,Paid
"""

# Week 6 demo/case - streamflow_customer_churn.csv (30 real rows, IDs shortened)
DATA["streamflow"] = """customer_id,signup_date,age,gender,region,monthly_fee,total_streaming_hours,num_devices,plan_type,support_tickets_last_6mo,churned
C001,2025-07-22,28.0,Male,North,10.89,106.2,4,,0,0
C002,2025-04-24,,Non-binary,North,15.52,125.2,2,Premium,2,1
C003,2023-11-20,39.0,,East,13.39,87.6,4,Premium,2,0
C004,2025-04-21,,Female,North,19.68,49.0,3,Premium,0,0
C005,2023-11-10,,Male,East,9.53,167.3,5,Basic,2,0
C006,2025-05-16,33.0,,North,15.73,152.6,3,Standard,1,0
C007,2024-12-20,-10.0,Male,West,13.96,105.4,3,Standard,1,1
C008,2024-01-26,150.0,Non-binary,South,6.44,92.0,2,Basic,3,0
C009,2025-06-24,71.0,Non-binary,East,6.51,102.4,1,Basic,0,0
C010,2024-03-24,21.0,Non-binary,North,6.18,156.7,1,Standard,1,0
C011,2024-05-13,45.0,Female,East,14.5,166.8,5,Basic,1,0
C012,2025-06-22,62.0,Female,South,17.26,41.4,3,Standard,0,0
C013,2024-04-19,79.0,,West,19.95,107.4,1,Standard,3,0
C014,2023-12-19,75.0,Non-binary,East,11.1,173.6,3,Standard,1,0
C015,2024-08-10,50.0,Male,North,11.59,30.3,4,Basic,2,1
C016,2023-10-03,61.0,Male,South,17.22,198.3,1,Premium,2,0
C017,2024-11-09,41.0,Male,North,13.32,88.8,1,Premium,0,0
C018,2025-01-29,36.0,Male,East,9.3,144.4,5,Premium,1,0
C019,2025-06-25,25.0,Non-binary,East,17.48,181.1,2,Standard,0,0
C020,2024-06-08,64.0,Non-binary,North,10.49,65.9,5,Premium,0,1
C021,2025-03-31,47.0,Female,South,19.06,75.6,2,Standard,0,0
C022,2024-08-21,62.0,Female,South,14.5,69.2,4,Basic,1,0
C023,2022-13-01,32.0,Male,East,18.48,169.3,2,Basic,2,0
C024,2025-08-01,43.0,Non-binary,East,8.19,104.4,1,Premium,4,0
C025,not a date,78.0,Non-binary,North,17.81,106.0,2,Standard,0,0
C026,2024-04-15,45.0,Female,North,18.59,73.8,1,Basic,1,0
C027,2025-03-07,23.0,Male,West,6.88,112.6,3,Basic,0,0
C028,2024-07-05,53.0,Female,West,19.78,29.6,2,Standard,1,0
C029,2025-02-04,26.0,Non-binary,South,16.16,151.4,3,Premium,1,0
C030,2024-03-23,32.0,Male,West,13.5,180.5,4,Basic,3,0
"""

DATASET_INFO = {
    "megatelco": "Megatelco churn survey (Labs 6 & 7) - 40 real rows incl. missing values, outliers, 1 duplicate",
    "spotifool": "Spotifool song downloads (Practice Midterm) - the 22 rows shown on the exam",
    "rent": "SF rentals (Labs 4 & 5) - 30 real San Francisco listings",
    "fintrust": "FinTrust Bank loans (Week 5 case) - 30 real rows",
    "streamflow": "StreamFlow streaming churn (Week 6 demo/case) - 30 real rows incl. bad ages & dates",
}

# "Lab 6 cleaning steps" used as hidden setup for some questions
LAB6_CLEAN = """\
df['handset_price'] = df['handset_price'].fillna(df['handset_price'].median())
df = df.dropna(subset=['income']).copy()
df.loc[:, 'data_leftover_mb'] = df['data_leftover_mb'].fillna(0)
df.loc[:, 'average_call_duration'] = df['average_call_duration'].fillna(df['average_call_duration'].median())
df.loc[:, 'data_mb_used'] = df['data_mb_used'].fillna(df['data_mb_used'].median())
df = df.drop_duplicates()
"""

MESSY_COLUMNS = """\
df.columns = [' College', 'Income ', 'Data Overage Mb', 'Data Leftover Mb', 'Data Mb Used',
              'Text Message Count', 'House', 'Handset Price', 'Over 15mins Calls Per Month',
              'Average Call Duration', 'Reported Satisfaction', 'Reported Usage Level',
              'Considering Change Of Plan', 'Leave', 'ID', 'Operating System']
"""

SPOTIFOOL_CONTEXT = """\
SPOTIFOOL (music download app) - 500 songs. Key variables:
  artist_popularity (1-100) | song_duration (120-300 sec) | danceability, energy,
  valence (0.1-1.0) | loudness (-30 to 0 dB) | speechiness, acousticness,
  instrumentalness (0-1) | tempo (60-200 BPM)
  downloads (560-100,000)  <-- "This is the TARGET VARIABLE for prediction."
  (type  t  at the answer prompt to see the data table)"""

MEGATELCO_CONTEXT = """\
MEGATELCO (Labs 6 & 7) - telecom customer churn. Columns: college, income, house,
data_overage_mb, data_leftover_mb, data_mb_used, text_message_count,
over_15mins_calls_per_month, average_call_duration, operating_system,
handset_price, reported_satisfaction, reported_usage_level,
considering_change_of_plan, leave (LEAVE/STAY = the target), id (customer id)"""


# ===========================================================================
# Question bank
# ===========================================================================
def code(s):
    return textwrap.dedent(s).strip("\n") if s else None


def Q(qid, group, topic, prompt, choices, answer, why, kind="mc", src=None,
      data=None, setup=None, context=None, source=""):
    """
    group  : "Practice Midterm", "Review Page", "Concepts", "Code Reading", "Business Cases"
    topic  : week/topic tag used for drills and weak-spot tracking
    kind   : "mc" one answer | "multi" select all that apply | "tf" true/false
    src    : pandas code shown in the question (runs in the Code Lab)
    data   : dataset loaded as df before the code runs
    setup  : code that runs first, hidden (shown as 'already ran' in the Code Lab)
    source : where in the course material this comes from
    """
    if kind == "tf":
        choices = ["True", "False"]
    return {"id": qid, "group": group, "topic": topic, "prompt": prompt.strip(),
            "choices": choices, "answer": answer if isinstance(answer, list) else [answer],
            "why": why, "kind": kind, "code": code(src), "data": data,
            "setup": code(setup), "context": context, "source": source}


TOPICS = {
    "W1": "Week 1 - Intro to Business Analytics, CRISP-DM, types of analytics",
    "W2": "Week 2 - Analytical models: supervised/unsupervised, classification/regression",
    "W3": "Week 3 - Business Understanding: objectives, RACI, charter, stakeholders",
    "W4": "Week 4 - Data Understanding: data types, structures, sampling, big data",
    "W5": "Week 5 - EDA: descriptive stats, charts, outliers, ethics",
    "W6": "Week 6 - Data Preparation I: cleaning, validation, leakage",
    "W7": "Week 7 - Data Preparation II: transformation, encoding, scaling, PCA",
    "PY": "Python/pandas code reading (Labs 2-7)",
}

BANK = []


# ---------------------------------------------------------------------------
# PRACTICE MIDTERM (Canvas) - answer key worked out from the readings
# ---------------------------------------------------------------------------
BANK += [
    Q("PM1", "Practice Midterm", "W5",
      "Which of the following best describes Exploratory Data Analysis (EDA)?",
      ["A process used to clean and prepare data for machine learning models.",
       "A technique to summarize and visualize data to identify patterns, trends, and anomalies.",
       "A method of applying deep learning algorithms to understand data relationships.",
       "A process used only for feature engineering in predictive modeling."],
      "A technique to summarize and visualize data to identify patterns, trends, and anomalies.",
      "Week 5 reading: EDA = 'analyzing data sets to summarize their main characteristics using "
      "both visual methods and quantitative techniques.' Cleaning/preparing is the Data "
      "Preparation phase (Week 6), not EDA itself.", source="Week 5 reading - Intro to EDA"),

    Q("PM2", "Practice Midterm", "W5",
      "Which of the following is NOT a typical step in Exploratory Data Analysis?",
      ["Visualizing data relationships using histograms, scatter plots, and box plots.",
       "Training a machine learning model to make predictions.",
       "Summarizing numerical and categorical variables using descriptive statistics.",
       "Checking for missing values and handling them appropriately."],
      "Training a machine learning model to make predictions.",
      "Training models is the MODELING phase of CRISP-DM. EDA comes before that: stats, "
      "charts, and data-quality checks (missing values, duplicates, outliers).",
      source="Week 5 reading - EDA in the CRISP-DM Framework"),

    Q("PM3", "Practice Midterm", "W5",
      "Which of the following EDA techniques would be the best way to understand the "
      "distribution of song downloads?",
      ["Box Plot", "Histogram", "Line Chart", "Scatter Plot"],
      "Histogram",
      "Histograms show the DISTRIBUTION of one numeric variable (how values spread out, "
      "skew, peaks). A box plot summarizes spread but hides the shape; scatter plots need "
      "TWO variables; line charts are for trends over time.",
      context=SPOTIFOOL_CONTEXT, data="spotifool",
      src="""
        plt.hist(df['downloads'], bins=10)
        plt.title("Distribution of Song Downloads")
        plt.show()
      """, source="Week 5 reading - Univariate Visualizations"),

    Q("PM4", "Practice Midterm", "W2",
      "In the context of predictive modeling, what does the target variable represent?",
      ["The variable that is used to normalize other features in the dataset.",
       "The variable that contains missing values and needs imputation.",
       "The variable that the model is trying to predict or explain.",
       "The variable with the highest correlation in the dataset."],
      "The variable that the model is trying to predict or explain.",
      "Target = dependent variable = what you predict (here: downloads). The other "
      "columns are attributes/features/independent variables.",
      context=SPOTIFOOL_CONTEXT, data="spotifool",
      source="Week 2 reading - Supervised Modeling; Week 4 - terminology"),

    Q("PM5", "Practice Midterm", "W2",
      "Based on the given Spotify dataset, what is the main analytical problem we are trying to solve?",
      ["Finding the song with the highest tempo and loudness.",
       "Predicting the number of downloads a song will receive based on its features.",
       "Determining whether a song is instrumental or vocal-based.",
       "Identifying the most popular artist in the dataset."],
      "Predicting the number of downloads a song will receive based on its features.",
      "The dataset description literally says downloads is 'the target variable for "
      "prediction.' Downloads is numeric, so it's a supervised REGRESSION problem.",
      context=SPOTIFOOL_CONTEXT, data="spotifool", source="Practice Midterm dataset description"),

    Q("PM6", "Practice Midterm", "W2",
      "Given that the goal is to predict the number of downloads a song will receive based on "
      "its features, which of the following analytical methods is the most appropriate?",
      ["Association Rule Mining - To find relationships between different song features.",
       "K-Means Clustering - To group similar songs based on their characteristics.",
       "Principal Component Analysis (PCA) - To reduce the dimensionality of the dataset.",
       "Linear Regression - To model the relationship between numerical features and downloads."],
      "Linear Regression - To model the relationship between numerical features and downloads.",
      "Numeric target + known historical values = supervised regression. K-Means and PCA "
      "are unsupervised (no target). Association rules = market-basket analysis.",
      context=SPOTIFOOL_CONTEXT, source="Week 2 reading - Regression; Week 7 - PCA is unsupervised"),

    Q("PM7", "Practice Midterm", "PY",
      "If you wanted to check whether there are any missing values in the dataset, which "
      "Pandas function would you use?",
      ["df.groupby()", "df.corr()", "df.isnull().sum()", "df.describe()"],
      "df.isnull().sum()",
      ".isnull() marks every missing cell True; .sum() counts the Trues per column. "
      "This exact line is in Labs 4, 6 and the Week 5 reading.",
      data="megatelco", src="df.isnull().sum()", source="Lab 4 / Lab 6 / Week 5 reading"),

    Q("PM8", "Practice Midterm", "W5",
      "Which of the following visualizations is best for understanding the relationship "
      "between energy and danceability?",
      ["Bar Chart", "Histogram", "Pie Chart", "Scatter Plot"],
      "Scatter Plot",
      "Relationship between TWO numeric variables -> scatterplot (bivariate). Histograms "
      "are one variable; bar/pie charts are for categories.",
      context=SPOTIFOOL_CONTEXT, data="spotifool",
      src="""
        sns.scatterplot(x='energy', y='danceability', data=df)
        plt.title("Energy vs Danceability")
        plt.show()
      """, source="Week 5 reading - Bivariate Visualizations"),

    Q("PM9", "Practice Midterm", "W3",
      "SoundWave is introducing an AI playlist feature. Stakeholders: Premium Subscribers "
      "(loyal paying customers), Record Labels (supply the music), Government Regulators "
      "(oversee digital music licensing), Freemium Users (free version).\n\nAccording to "
      "Mendelow's Stakeholder Matrix, which group falls in the 'Keep Satisfied' quadrant "
      "(HIGH power, LOW interest)?",
      ["Premium Subscribers, because they demand better features.",
       "Record Labels, because they control the content but are not directly interested in feature updates.",
       "Government Regulators, because they create policies but are not concerned with product features.",
       "Freemium Users, because they use the service the most."],
      "Government Regulators, because they create policies but are not concerned with product features.",
      "Mendelow's matrix = Power x Interest:\n"
      "   High power + high interest = MANAGE CLOSELY (key players)\n"
      "   High power + low interest  = KEEP SATISFIED\n"
      "   Low power  + high interest = KEEP INFORMED\n"
      "   Low power  + low interest  = MONITOR\n"
      "Regulators can shut you down (huge power) but don't care about playlist features "
      "(low interest). Record labels are high power AND high interest (their music is the "
      "product) -> manage closely. NOTE: this matrix wasn't in the Week 1-7 handouts I "
      "could read, so it likely came from lecture.",
      source="Business Understanding - stakeholder analysis"),

    Q("PM10", "Practice Midterm", "W3",
      "A retail company sees declining online sales and drafts a business problem statement. "
      "Which should be included? (Select all that apply)",
      ["List of all variables, including target variable", "Detailed Python code for analysis",
       "Key Performance Indicators (KPIs)", "Project timeline and deliverables",
       "Description of the root problem"],
      ["Key Performance Indicators (KPIs)", "Project timeline and deliverables",
       "Description of the root problem"],
      "Week 3: the problem statement 'clearly and concisely articulates the core challenge' "
      "and avoids technical jargon. It leads to objectives, success criteria (KPIs) and a "
      "plan with timeline and deliverables (see the MegaTelCo sample charter in the slides). "
      "Python code obviously isn't part of it, and a full variable list is a "
      "data-understanding detail, not a business statement. (Canvas didn't show the "
      "official key, so this is my best reading of the material.)",
      kind="multi", source="Week 3 reading - Deliverables; Week 3 slides - sample charter"),

    Q("PM11", "Practice Midterm", "W2",
      "A financial institution wants (1) a Credit Approval System that decides Approved/Denied "
      "and (2) Customer Segmentation that groups customers by spending behavior. Which "
      "learning types/models apply? (Select all that apply)",
      ["Supervised Learning - Classification", "Supervised Learning - Regression",
       "All of the above", "Unsupervised Learning - Clustering",
       "Unsupervised Learning - Neural Networks"],
      ["Supervised Learning - Classification", "Unsupervised Learning - Clustering"],
      "Approved/Denied is a known CATEGORY label -> supervised classification. Grouping "
      "customers with no label -> unsupervised clustering. Nothing predicts a number, so "
      "regression doesn't apply.",
      kind="multi", source="Week 2 reading - Machine Learning Approaches"),

    Q("PM12", "Practice Midterm", "W1",
      "A hospital analyzes 5 years of admissions to identify seasonal trends (flu in winter, "
      "ER spikes on weekends). Which type of analytics is this?",
      ["None of the above", "Predictive Analytics", "Prescriptive Analytics", "Descriptive Analytics"],
      "Descriptive Analytics",
      "Understanding HISTORICAL patterns = descriptive ('What happened?'). Predictive would "
      "forecast next winter; prescriptive would recommend staffing levels.",
      source="Week 1 & 2 readings - Types of Analytics"),

    Q("PM13", "Practice Midterm", "W4",
      "A bank dataset has: Customer Age (years), Credit Score (300-850), Loan Approval Status "
      "(Approved/Denied), Customer ZIP Code (true/false, indicating if a code exists). Which "
      "correctly categorizes the data types?",
      ["Age - Numerical, Credit Score - Categorical, Approval - Categorical, ZIP - Numerical",
       "Age - Categorical, Credit Score - Categorical, Approval - Numerical, ZIP - Numerical",
       "Age - Numerical, Credit Score - Numerical, Approval - Categorical, ZIP - Categorical",
       "Age - Categorical, Credit Score - Numerical, Approval - Numerical, ZIP - Categorical"],
      "Age - Numerical, Credit Score - Numerical, Approval - Categorical, ZIP - Categorical",
      "Age and credit score are measured quantities (subtracting them is meaningful). "
      "Approved/Denied is a label (binary = a kind of nominal). Here the ZIP field is "
      "true/false, so it's binary/categorical. (Even a real ZIP code is categorical: "
      "84112 - 84101 means nothing.)",
      source="Week 4 reading & slides - Types of Variables"),

    Q("PM14", "Practice Midterm", "W2",
      "A car rental company predicts whether a customer will rent a car. Data: Customer Age, "
      "Income Level (Low/Medium/High), Previous Rentals (count), Rental Decision (Yes/No). "
      "Which is the target variable and its data type?",
      ["Rental Decision - Target Variable, Categorical", "Income Level - Target Variable, Categorical",
       "Previous Rentals - Target Variable, Numerical", "Customer Age - Target Variable, Numerical"],
      "Rental Decision - Target Variable, Categorical",
      "The question says 'predict WHETHER a customer will rent', which is the Yes/No Rental "
      "Decision. Yes/No is categorical (binary), so this is a classification problem.",
      source="Week 2 - target variable; Week 4 - binary data"),

    Q("PM15", "Practice Midterm", "W3",
      "A financial services company is in the Business Understanding phase of a fraud project. "
      "Challenges: limited fraud data (privacy rules), departments with differing goals, "
      "regulators requiring explainable models, fast-changing fraud patterns. What is the "
      "most appropriate FIRST step in the Business Understanding phase?",
      ["Determine analytical goals, such as reducing false positives in fraud detection models.",
       "Assess the situation, analyzing internal and external constraints, available data, and stakeholder concerns.",
       "Produce the project plan, ensuring timelines align with compliance and risk management expectations.",
       "Determine business objectives, focusing on reducing fraud loss while maintaining regulatory compliance."],
      "Determine business objectives, focusing on reducing fraud loss while maintaining regulatory compliance.",
      "The 4 steps go in order: (1) Determine business objectives, (2) Assess the situation, "
      "(3) Determine data mining goals, (4) Produce the project plan. The list of challenges "
      "is bait to make 'assess the situation' look right, but the question asks for the "
      "FIRST step. Notice the correct option already folds in the regulatory constraint. "
      "(Canvas didn't reveal the key. I'm basing this on the step order in the reading.)",
      source="Week 3 reading & slides - Business Understanding steps 1-4"),

    Q("PM16", "Practice Midterm", "W3",
      "A government agency wants a 'low-hanging fruit' project first.\n"
      "  Project A - Traffic Optimization: data readily available (sensors, GPS), structured "
      "solutions (signal timing, congestion pricing), measurable results in 6-12 months.\n"
      "  Project B - Climate Change Policy: many stakeholders, no single solution, unintended "
      "consequences, impact takes years.\nWhich should be prioritized first?",
      ["Project B - Climate Change Policy, because long-term sustainability is more important than short-term gains.",
       "Neither project is a low-hanging fruit, because all government initiatives require long-term investment.",
       "Both projects should be prioritized equally, to balance short-term and long-term goals.",
       "Project A - Traffic Optimization, because it is a Tame Problem with structured solutions and immediate impact."],
      "Project A - Traffic Optimization, because it is a Tame Problem with structured solutions and immediate impact.",
      "TAME problem = well-defined, data available, known solution methods, measurable "
      "result -> great quick win. WICKED problem = many stakeholders with conflicting goals, "
      "no single right answer, solutions create new problems (climate policy). Analytics "
      "projects should start with tame, high-value problems.",
      source="Business Understanding - problem framing (tame vs. wicked problems)"),

    Q("PM17", "Practice Midterm", "W3",
      "A telecom rolls out an AI support chatbot. Goal: reduce service costs while keeping "
      "customer satisfaction high. Which KPIs are relevant to measure success?",
      ["Chatbot Deflection Rate - inquiries resolved without a human.",
       "Average Handling Time (AHT) - average duration of interactions, aiming to reduce costs.",
       "All of the above",
       "Customer Satisfaction Score (CSAT) - satisfaction after chatbot interactions."],
      "All of the above",
      "The goal has two halves: cut COSTS (deflection rate, handling time) AND keep "
      "SATISFACTION (CSAT). Good success criteria cover every part of the business objective.",
      source="Week 3 reading - KPI Documentation / Success Criteria"),

    Q("PM18", "Practice Midterm", "W4",
      "During which phase would you explore summary statistics, visualizations, and "
      "relationships between variables?",
      ["Deployment", "Modeling", "Data Preparation", "Data Understanding"],
      "Data Understanding",
      "CRISP-DM phase 2, Data Understanding, is where you explore the data (EDA). Data "
      "Preparation is where you FIX what you found (clean, transform).",
      source="Week 4 & 5 readings"),

    Q("PM19", "Practice Midterm", "W2",
      "Which of the following is a key difference between regression and classification?",
      ["Regression predicts discrete labels, while classification predicts continuous values.",
       "Both regression and classification always produce numerical outputs.",
       "Regression predicts continuous values, while classification predicts discrete labels.",
       "Classification is only used for binary problems, while regression is used for multi-class problems."],
      "Regression predicts continuous values, while classification predicts discrete labels.",
      "'Classification is about predicting categories, while regression is about predicting "
      "numbers.' (Week 2 reading.) Classification can be multi-class too (Low/Med/High risk).",
      source="Week 2 reading - Supervised Modeling"),

    Q("PM20", "Practice Midterm", "W2",
      "Which of the following problems would best be solved using a classification model?",
      ["Predicting whether a customer will buy a product (Yes/No)", "Predicting the price of a house",
       "Estimating a person's weight based on their height", "Forecasting next month's sales revenue"],
      "Predicting whether a customer will buy a product (Yes/No)",
      "Yes/No is a category, so it's classification. Price, weight and revenue are numbers, "
      "so those are regression.",
      source="Week 2 reading & slides"),

    Q("PM22", "Practice Midterm", "PY",
      "What would be the expected output from the following Python code?",
      ['In a new dataframe called "df_new", include one column for product_price containing values less than 5000',
       "<None of the provided answers>",
       'In a new dataframe called "df_new" add rows with price less than or equal to 5000',
       'In the "df" dataframe, delete the price if less than 5000'],
      'In a new dataframe called "df_new" add rows with price less than or equal to 5000',
      "df['product_price'] <= 5000 makes a True/False value for every ROW. df[ ...that... ] "
      "keeps the rows that are True, with ALL their columns. The original df is untouched. "
      "Watch for <= vs < in the choices!",
      data="rent",
      setup="df = df.rename(columns={'price': 'product_price'})",
      src="""
        df_new = df[df['product_price'] <= 5000]
        print(len(df), "rows in df   ", len(df_new), "rows in df_new")
      """, source="Week 4 slides - Modifying Dataframes"),
]

# ---------------------------------------------------------------------------
# REVIEW PAGE sample questions (Megatelco)
# ---------------------------------------------------------------------------
BANK += [
    Q("RP1", "Review Page", "W4",
      "(Megatelco) Which of the following variables would NOT be expected to be a good "
      "predictor of LEAVE?",
      ["reported usage level", "operating_system", "handset_price", "customer_id", "data_overage_mb"],
      "customer_id",
      "Instructor's hint: customer_id is a randomly assigned identifier. It describes "
      "nothing about the customer, so it can't explain churn. (Week 7: 'Don't waste time on "
      "irrelevant variables' like IDs.)",
      context=MEGATELCO_CONTEXT, source="Review page sample Q1"),

    Q("RP2", "Review Page", "W4",
      "Which of the following variables would be a good fit for a CATEGORY data type?",
      ["house (home price)", "operating_system", "handset_price", "customer_id", "data_overage_mb"],
      "operating_system",
      "Category dtype is for values that are LIMITED in number and FIXED over time (Week 4 "
      "slides). operating_system is Android/IOS. Prices and MB are measurements; the ID is "
      "unique per customer.",
      data="megatelco", src="df['operating_system'].value_counts()",
      context=MEGATELCO_CONTEXT, source="Review page sample Q2; Week 4 slides"),

    Q("RP3", "Review Page", "W1",
      "Which of the following steps is NOT part of the CRISP-DM lifecycle?",
      ["Deployment", "Modeling", "Data Collection", "Business Understanding", "Data Understanding"],
      "Data Collection",
      "The 6 phases: Business Understanding -> Data Understanding -> Data Preparation -> "
      "Modeling -> Evaluation -> Deployment. Collecting data happens INSIDE Data "
      "Understanding; it isn't its own phase.",
      source="Review page sample Q3; Week 1 reading"),

    Q("RP4", "Review Page", "PY",
      "Which Python snippet correctly converts a variable to a string?",
      ["df['product'] = df['product'].astype('str')", "df['product'] == str(df['product'])",
       "df['product'] = to_str(df['product'])", "df['product'] == str(df.product)",
       "df['product'] = df['product'].string_convert"],
      "df['product'] = df['product'].astype('str')",
      ".astype(type) converts a column, and you must ASSIGN it back with = (single). The == "
      "options only compare and change nothing. to_str and .string_convert don't exist. The "
      "labs use the same pattern: df['college'] = df['college'].astype('category').",
      data="megatelco",
      src="""
        print(df['id'].dtype)
        df['id'] = df['id'].astype('str')
        print(df['id'].dtype)
      """, source="Review page sample Q4; Lab 6"),

    Q("RP5", "Review Page", "PY",
      "What is the purpose of this code?",
      ["Identify the data type of product", "Determine if there is data in the product variable",
       "Convert the product variable to a string datatype", "Convert the product variable to a category datatype",
       "Determine if all the data are of the same datatype"],
      "Convert the product variable to a string datatype",
      "astype('str') = convert to string (text). astype('category') would be the category one.",
      data="megatelco", setup="df = df.rename(columns={'operating_system': 'product'})",
      src="df['product'] = df['product'].astype('str')", source="Review page sample Q5"),
]

# ---------------------------------------------------------------------------
# CONCEPT DRILLS - straight from the Week 1-7 readings & slides
# ---------------------------------------------------------------------------
C = "Concepts"
BANK += [
    # ----- Week 1 -----
    Q("W1-1", C, "W1", "Business Intelligence (BI) mainly answers 'What happened?'. What does "
      "Business Analytics ADD on top of that?",
      ["More detailed dashboards and reports of historical KPIs",
       "Predictive and prescriptive analysis of what may happen and what to do",
       "Larger storage of historical data in relational databases and warehouses",
       "Cleaning and preparing the data so it can be reported accurately"],
      "Predictive and prescriptive analysis of what may happen and what to do",
      "Week 1 reading: BI focuses on historical data and reporting; BA extends this with predictive "
      "and prescriptive techniques.", source="Week 1 reading - What is Business Analytics?"),
    Q("W1-2", C, "W1", "What does CRISP-DM stand for?",
      ["Critical Review of Information Systems - Data Management", "Cross-Industry Standard Process for Data Mining",
       "Customer Relationship and Information Strategy - Data Modeling", "Cross-Institutional Statistical Process for Decision Making"],
      "Cross-Industry Standard Process for Data Mining",
      "Developed in 1996 as an EU-funded project with Daimler, SPSS and NCR. It's industry-neutral and non-proprietary.",
      source="Week 1 reading & slides"),
    Q("W1-3", C, "W1", "Put the six CRISP-DM phases in order:",
      ["Data Understanding, Business Understanding, Modeling, Data Preparation, Deployment, Evaluation",
       "Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment",
       "Business Understanding, Data Preparation, Data Understanding, Modeling, Deployment, Evaluation",
       "Business Understanding, Data Understanding, Modeling, Data Preparation, Evaluation, Deployment"],
      "Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment",
      "Memory trick: 'Big Dogs Don't Make Easy Decisions': Business understanding, Data understanding, Data preparation, Modeling, Evaluation, Deployment.",
      source="Week 1 reading - The Business Analytics Process"),
    Q("W1-4", C, "W1", "CRISP-DM is a strictly linear process: once a phase is finished you never go back to it.",
      None, "False",
      "'CRISP-DM emphasizes that this is not a linear process. Analysts often revisit earlier stages "
      "as new insights emerge.' (Week 1.) Example: FreshGro went back to Business Understanding after "
      "process mapping showed the delays were in the warehouse.", kind="tf", source="Week 1 & Week 3 readings"),
    Q("W1-5", C, "W1", "In the Evaluation phase, models are checked mainly to see whether they...",
      ["reach the highest accuracy score, whether or not it helps the business",
       "meet the business goals and give insights that can be acted on",
       "use the newest and most advanced algorithm available to the team",
       "run fast enough to be refreshed automatically every day"],
      "meet the business goals and give insights that can be acted on",
      "Week 1: 'the Evaluation phase ensures they meet business goals, not just statistical performance.'",
      source="Week 1 reading - CRISP-DM"),
    Q("W1-6", C, "W1", "Before Hurricane Frances, Walmart reviewed past hurricane sales and found that "
      "strawberry Pop-Tarts sold about 7x normal. Reviewing that past sales data is which type of analytics?",
      ["Descriptive", "Predictive", "Prescriptive", "Unsupervised clustering"],
      "Descriptive",
      "Summarizing what happened in the past is descriptive. Walmart THEN used predictive analytics "
      "(weather + buying patterns) to forecast demand and pre-position the trucks.",
      source="Week 1 reading - Introductory Case"),
    Q("W1-7", C, "W1", "An airline adjusts ticket prices automatically based on forecast demand and seat "
      "availability. Which type of analytics is this?",
      ["Descriptive", "Diagnostic", "Predictive", "Prescriptive"],
      "Prescriptive",
      "Prescriptive answers 'What should we do?' by combining predictions with optimization. Dynamic "
      "pricing is the textbook example.", source="Week 1 & 2 readings"),
    Q("W1-8", C, "W1", "The Week 1 slides add a fourth type of analytics between descriptive and predictive. "
      "What question does DIAGNOSTIC analytics answer?",
      ["What happened?", "Why did it happen?", "What will happen?", "What should we do?"],
      "Why did it happen?",
      "Descriptive = what happened, Diagnostic = why (root causes), Predictive = what will happen, "
      "Prescriptive = what should we do.", source="Week 1 slides - Types of Analytics"),
    Q("W1-9", C, "W1", "Match the library to its job: which Python library is mainly used for building "
      "machine learning models?",
      ["pandas", "NumPy", "Matplotlib", "Scikit-learn"],
      "Scikit-learn",
      "pandas = data manipulation/prep (DataFrames), NumPy = fast numeric computing, Matplotlib & "
      "Seaborn = charts, Scikit-learn = machine learning.", source="Week 1 reading - Common Tools"),
    Q("W1-10", C, "W1", "A lending model trained on historical decisions approves fewer applicants from "
      "certain neighborhoods. This is MOST directly an example of which ethical concern?",
      ["Bias in data and algorithms", "Problems with data velocity", "Lack of a project charter",
       "Too many input features"],
      "Bias in data and algorithms",
      "Historical data can reflect systemic inequality, and models can 'perpetuate or even amplify' it. "
      "(Week 1; the Week 5 reading also warns about ZIP codes acting as a proxy.)",
      source="Week 1 reading - Ethical Considerations"),

    # ----- Week 2 -----
    Q("W2-1", C, "W2", "What is the key difference between supervised and unsupervised learning?",
      ["Supervised models need much more data and more computing power than unsupervised ones",
       "Supervised uses a labeled target; unsupervised looks for patterns with none",
       "Unsupervised models are usually more accurate than supervised ones",
       "Supervised is for images and unsupervised is for numeric tables"],
      "Supervised uses a labeled target; unsupervised looks for patterns with none",
      "Supervised = inputs + correct output (label/target). Unsupervised = all variables, no target. "
      "It discovers groupings or structure.", source="Week 2 reading - Machine Learning Approaches"),
    Q("W2-2", C, "W2", "Marketing wants to discover natural groups of customers based on behavior, with no "
      "predefined labels. Which method fits?",
      ["Linear regression", "Classification tree", "Clustering", "Logistic regression"],
      "Clustering", "No target + 'find groups' = unsupervised clustering.",
      source="Week 2 reading & slides"),
    Q("W2-3", C, "W2", "Which metrics are used to evaluate a REGRESSION model?",
      ["Accuracy, precision, recall, F1", "MSE, RMSE, MAE, R-squared", "Support and confidence", "Number of clusters"],
      "MSE, RMSE, MAE, R-squared",
      "Regression error is about how far the predicted numbers are from the real ones. "
      "Accuracy/precision/recall/F1 are for classification.", source="Week 2 reading - Supervised Modeling"),
    Q("W2-4", C, "W2", "According to the Week 2 slides, a classification model gives TWO kinds of "
      "predictions. What are they?",
      ["A numeric value and its error term", "A category and a probability for it",
       "A cluster and the center of that cluster", "A mean and a median for each group"],
      "A category and a probability for it",
      "Example from the slides: a fraud model predicts 'fraud' AND how likely it is. The bank "
      "locks the card only if that probability is high enough.",
      source="Week 2 slides - Types of Classification Output"),
    Q("W2-5", C, "W2", "'What items are commonly purchased together?' is which analytical method?",
      ["Similarity matching (find look-alikes)", "Affinity grouping (market basket)", "Profiling (typical behavior)",
       "Regression (predict a number)"],
      "Affinity grouping (market basket)",
      "Slides list: affinity grouping, similarity matching ('which companies are like our best "
      "customers?'), profiling ('typical usage of this segment?'), clustering, predictive modeling.",
      source="Week 2 slides - Analytical Methods"),
    Q("W2-6", C, "W2", "Which of these is UNSTRUCTURED data?",
      ["A table of product sales by day and region", "Customer account balances in a SQL database",
       "Customer reviews posted on Amazon", "A spreadsheet of order dates and IDs"],
      "Customer reviews posted on Amazon",
      "Free-form text, audio, images and video are unstructured, and need NLP or computer vision to analyze.",
      source="Week 2 reading - Structured vs. Unstructured"),
    Q("W2-7", C, "W2", "Generalization means...",
      ["the model performs well on new data it has never seen",
       "the model uses every available feature to make predictions",
       "the model is simple enough to explain to stakeholders",
       "the sample covers the entire population of customers"],
      "the model performs well on new data it has never seen",
      "That's why we hold out TEST data that the model never learned from.",
      source="Week 2 reading - Key Terms"),
    Q("W2-8", C, "W2", "LinkedIn wants to predict how many followers a member will have next year. "
      "Which kind of model is this?",
      ["Classification", "Regression", "Clustering", "Affinity grouping"],
      "Regression", "Number of followers is numeric, so regression. (From the LinkedIn case in the Week 2 slides.)",
      source="Week 2 slides - LinkedIn case"),
    Q("W2-9", C, "W2", "A data-driven model can be used to PREDICT or to ____.",
      ["STORE (keep large amounts of data)", "EXPLAIN (see which variables matter)",
       "REPLACE (take over what stakeholders do)", "COLLECT (gather new data from users)"],
      "EXPLAIN (see which variables matter)",
      "Slides: 'Predict: who will buy life insurance?' vs 'Explain: which variables are most strongly related to buying?'",
      source="Week 2 slides - Supervised Modeling"),

    # ----- Week 3 -----
    Q("W3-1", C, "W3", "Which is a DATA MINING GOAL (as opposed to a business objective)?",
      ["Reduce customer churn by 10% within the next six months",
       "Increase on-time deliveries from 82% to 95% by June",
       "Build a model that predicts which customers will churn",
       "Preserve $1M in annual revenue by the end of the year"],
      "Build a model that predicts which customers will churn",
      "Business objective = the business outcome (reduce churn 10%). Data mining goal = the technical task "
      "that supports it (predict churn probability).", source="Week 3 reading & slides - Step 3"),
    Q("W3-2", C, "W3", "What is the correct order of the 4 Business Understanding steps?",
      ["Assess the situation -> Determine business objectives -> Produce project plan -> Determine data mining goals",
       "Determine business objectives -> Assess the situation -> Determine data mining goals -> Produce project plan",
       "Determine data mining goals -> Determine business objectives -> Assess the situation -> Produce project plan",
       "Produce project plan -> Determine business objectives -> Determine data mining goals -> Assess the situation"],
      "Determine business objectives -> Assess the situation -> Determine data mining goals -> Produce project plan",
      "This is the order in the Week 3 slides (Steps 1-4).", source="Week 3 slides"),
    Q("W3-3", C, "W3", "In a RACI matrix, who is 'A'?",
      ["The person who does the work", "The person who owns the outcome", "The person who gives input",
       "The person who is kept updated"],
      "The person who owns the outcome",
      "R = Responsible (does the work), A = Accountable (owns the outcome), C = Consulted (gives input), "
      "I = Informed (kept updated). Churn example: data scientist R, product manager A, customer "
      "service leaders C, executives I.", source="Week 3 reading - RACI"),
    Q("W3-4", C, "W3", "'Reduce customer support resolution time by 15% in the next quarter' is a good goal "
      "because it follows which framework?",
      ["SWOT", "RACI", "SMART", "CRISP-DM"],
      "SMART",
      "Specific, Measurable, Achievable, Relevant, Time-bound. Using SMART goals is how you avoid "
      "Pitfall 1: vague goals.", source="Week 3 reading - Common Pitfalls"),
    Q("W3-5", C, "W3", "An eager analyst opens the dataset and starts modeling before talking to stakeholders. "
      "Which pitfall is this?",
      ["Vague goals for the project", "Misaligned stakeholders", "Skipping to the data too fast",
       "Ignoring project constraints"],
      "Skipping to the data too fast",
      "The 4 pitfalls: vague goals, misaligned stakeholders, skipping to the data too fast, ignoring "
      "constraints. The slides add: 'The common factor is communication.'", source="Week 3 reading & slides"),
    Q("W3-6", C, "W3", "In the FreshGro Logistics case, what did BUSINESS PROCESS MAPPING reveal?",
      ["Traffic on the delivery routes was the largest single cause of delays",
       "Many delays began at the warehouse loading dock, before the trucks left",
       "Drivers were taking inefficient routes between delivery stops",
       "The GPS data was too incomplete to track delivery times"],
      "Many delays began at the warehouse loading dock, before the trucks left",
      "This shifted the focus from route optimization to warehouse workflow. That's iteration in "
      "action, and the dashboard pilot cut delays by 18%.", source="Week 3 reading - Case Study"),
    Q("W3-7", C, "W3", "Why is the project charter described as a 'living document'?",
      ["It is rewritten from scratch for every new project",
       "It is updated as the project evolves and new insights appear",
       "It must be re-approved by every employee each quarter", "It replaces all of the other project documentation"],
      "It is updated as the project evolves and new insights appear",
      "Business Understanding deliverables (charter, goals, assumptions, stakeholder plan) are revisited "
      "and revised after milestones.", source="Week 3 reading - Emphasizing Iteration"),
    Q("W3-8", C, "W3", "Success criteria for an analytics project should include...",
      ["Only technical metrics, such as accuracy or precision", "Only business metrics, such as revenue or retention",
       "Both business metrics (retention) and technical metrics (recall)",
       "Neither, since success is judged subjectively by the sponsor"],
      "Both business metrics (retention) and technical metrics (recall)",
      "FreshGro example: business KPIs (on-time rate, SLA violations) + technical KPIs (model "
      "precision/recall, dashboard adoption).", source="Week 3 reading - Deliverables"),
    Q("W3-9", C, "W3", "'Our data might be outdated' and 'the team may lack the skills' belong in which deliverable?",
      ["RACI matrix", "Risk & Assumption Log", "Business problem statement", "SWOT strengths list"],
      "Risk & Assumption Log",
      "The log tracks uncertainties, limitations and assumptions so they're managed early. The slides "
      "list risks like outdated/bad data, data access issues, privacy, skills gaps.", source="Week 3 slides"),
    Q("W3-10", C, "W3", "SWOT stands for...",
      ["Strategy, Weaknesses, Objectives, Targets", "Strengths, Weaknesses, Opportunities, Threats",
       "Stakeholders, Workflow, Outcomes, Targets", "Strengths, Weaknesses, Objectives, Threats"],
      "Strengths, Weaknesses, Opportunities, Threats",
      "Example: strength = rich historical data. Threat = upcoming regulation that limits data use.",
      source="Week 3 reading - Tools & Techniques"),

    # ----- Week 4 -----
    Q("W4-1", C, "W4", "'52, Juan, San Diego' is DATA. Which of these is KNOWLEDGE?",
      ["Juan is a 52-year-old customer from San Diego who bought a membership",
       "A spreadsheet listing the ages and cities of all customers",
       "Customers over 50 buy more memberships in January, so target them",
       "The number 52 stored in the age column of the table"],
      "Customers over 50 buy more memberships in January, so target them",
      "Data = raw facts. Information = data with context (Juan is a 52-yr-old customer...). Knowledge = "
      "insight plus experience that leads to ACTION.", source="Week 4 slides - From Data to Knowledge"),
    Q("W4-2", C, "W4", "Hotel star ratings (1-star to 5-star) are which type of variable?",
      ["Nominal", "Ordinal", "Discrete numeric", "Continuous numeric"],
      "Ordinal",
      "There's a meaningful ORDER, but the gaps between levels aren't uniform or measurable. Other ordinal "
      "examples: education level, satisfaction (low/avg/high).", source="Week 4 reading - Ordinal Variables"),
    Q("W4-3", C, "W4", "'Number of website visitors per day' is...",
      ["Nominal", "Ordinal", "Discrete", "Continuous"],
      "Discrete", "Countable whole numbers make it discrete. Measurements that can have decimals (revenue, weight, temperature) are continuous.",
      source="Week 4 reading - Numerical Variables"),
    Q("W4-4", C, "W4", "Binary data (Yes/No, 0/1) is usually considered a subset of which type?",
      ["Nominal (categorical)", "Continuous (numeric)", "Time series (temporal)", "Spatial (geographic)"],
      "Nominal (categorical)",
      "Two unordered categories make it nominal. In some contexts it's ordinal (Pass > Fail), and models "
      "often treat 0/1 as numeric.", source="Week 4 reading - Binary data"),
    Q("W4-5", C, "W4", "Annual GDP for several European countries over ten years is which kind of data?",
      ["Cross-sectional data", "Time-series data", "Panel data", "Unstructured data"],
      "Panel data",
      "Multiple subjects (countries) x multiple time periods = panel data. One snapshot in time = "
      "cross-sectional. One thing tracked over time = time series.", source="Week 4 reading"),
    Q("W4-6", C, "W4", "Which 'V' of Big Data is about the SPEED at which data is created and must be processed "
      "(stock trades, fraud detection)?",
      ["Volume", "Velocity", "Variety", "Validity"],
      "Velocity", "Volume = how much. Velocity = how fast. Variety = how many formats (structured, semi-structured like JSON/XML, unstructured).",
      source="Week 4 reading - Big Data"),
    Q("W4-7", C, "W4", "You split customers into new vs returning, then randomly sample from each group. "
      "Which sampling method is this?",
      ["Random", "Stratified", "Systematic", "Convenience"],
      "Stratified",
      "Stratified = divide into subgroups, then sample from each. Convenience sampling (only one store) "
      "is the least reliable and can introduce bias.", source="Week 4 reading & slides - Sampling"),
    Q("W4-8", C, "W4", "In data-science terminology, the 'target' is equivalent to which statistics term?",
      ["Independent variable", "Dependent variable", "Sample population", "Single record"],
      "Dependent variable",
      "Attributes/features/predictors = independent variables (columns). Target = dependent variable. "
      "Row = record = example = observation. Table = relation = dataset.",
      source="Week 4 reading - Equivalent Terminologies"),
    Q("W4-9", C, "W4", "According to the slides, when should a column use the pandas CATEGORY data type "
      "instead of string?",
      ["When the text is long, open-ended and different in every row",
       "When there is a small, fixed set of values (e.g., blood type)",
       "When the column contains decimals instead of whole numbers",
       "Only when the column will be used as the model target"],
      "When there is a small, fixed set of values (e.g., blood type)",
      "String = free text like an Airbnb review. Category = a fixed, limited set of values: "
      "df['leave'] = df['leave'].astype('category').", source="Week 4 slides - What is a Category data type?"),
    Q("W4-10", C, "W4", "Rule of thumb from the slides for deciding numeric vs category:",
      ["If the column contains numbers, treat it as numeric",
       "If the difference between levels is meaningful, numeric may fit",
       "If it has fewer than 100 unique values, make it a category",
       "Use whichever type the data source assigned, without checking it"],
      "If the difference between levels is meaningful, numeric may fit",
      "Example: 'years of education' or a 1-10 quality scale. It depends on context.",
      source="Week 4 slides - Numeric or Category?"),
    Q("W4-11", C, "W4", "A sample is...",
      ["the complete group of all customers being studied", "a subset of the population selected for analysis",
       "a single row of data taken from the dataset", "a single column of data taken from the dataset"],
      "a subset of the population selected for analysis",
      "Population = all 10,000 customers. Sample = 1,000 randomly surveyed customers. We sample because "
      "studying everyone is too expensive and slow.", source="Week 4 reading"),
]


BANK += [
    # ----- Week 5 -----
    Q("W5-1", C, "W5", "Who popularized Exploratory Data Analysis in the 1970s?",
      ["John Tukey", "Wes McKinney", "Cathy O'Neil", "Stephen Few"],
      "John Tukey",
      "Tukey (1977). Wes McKinney created pandas, Cathy O'Neil wrote Weapons of Math Destruction, and "
      "Stephen Few writes about visualization.", source="Week 5 reading"),
    Q("W5-2", C, "W5", "Income data has a few billionaires. Which measure of central tendency is MOST "
      "robust (least affected)?",
      ["Mean", "Median", "Standard deviation", "Range"],
      "Median", "The mean gets dragged toward extreme values; the median (the middle value) barely moves.",
      source="Week 5 reading - Descriptive Statistics"),
    Q("W5-3", C, "W5", "Q1 = 20 and Q3 = 40. Using the IQR method, values above what number are outliers?",
      ["40", "50", "60", "70"],
      "70",
      "IQR = Q3 - Q1 = 20. Upper fence = Q3 + 1.5 x IQR = 40 + 30 = 70. Lower fence = Q1 - 1.5 x IQR = 20 - 30 = -10.",
      source="Week 5 reading - IQR method"),
    Q("W5-4", C, "W5", "A distribution with a long tail to the RIGHT (a few very high values, like income) is...",
      ["negatively skewed", "positively skewed", "normally distributed", "zero-variance"],
      "positively skewed", "Positive (right) skew = long right tail. Log transforms (Week 7) help fix it.",
      source="Week 5 reading - Shape"),
    Q("W5-5", C, "W5", "Which chart shows a numeric variable's median, IQR, and outliers as individual points?",
      ["Pie chart", "Boxplot", "Line chart", "Heatmap"],
      "Boxplot", "Points beyond the whiskers are the outliers.", source="Week 5 reading - Univariate Visualizations"),
    Q("W5-6", C, "W5", "You want to see correlations among MANY numeric variables at once (and spot "
      "multicollinearity). Best chart?",
      ["Histogram of every numeric variable", "Heatmap of the correlation matrix", "Bar chart of the column means",
       "Pie chart of the column totals"],
      "Heatmap of the correlation matrix",
      "Lab 5 code: sns.heatmap(df[[...]].corr(), annot=True, cmap='coolwarm'). A pairplot is the "
      "scatterplot-matrix alternative.", source="Week 5 reading; Lab 5"),
    Q("W5-7", C, "W5", "An analyst who believes young customers are more loyal only highlights the charts that "
      "support it. This is...",
      ["Data leakage", "Confirmation bias", "Overfitting", "Referential integrity"],
      "Confirmation bias", "Fix it by actively seeking disconfirming evidence and testing multiple hypotheses.",
      source="Week 5 reading - Ethical Perspective on EDA"),
    Q("W5-8", C, "W5", "Which U.S. law protects MEDICAL information?",
      ["GDPR", "HIPAA", "FERPA", "CCPA"],
      "HIPAA", "GDPR = EU personal data. HIPAA = health. FERPA = student education records.",
      source="Week 5 reading - Legal Compliance"),
    Q("W5-9", C, "W5", "A column has the SAME value in every row (zero variance). What should you usually do?",
      ["Use it as the target variable for the model", "Remove it, since it contributes nothing to predictions",
       "Log-transform it so the values become more spread out",
       "Keep it, because constant columns help models find patterns"],
      "Remove it, since it contributes nothing to predictions",
      "Week 5: 'a column with zero variance contributes nothing to predictive modeling.' (In the SF rent "
      "sample, room_in_apt is all 0!)", source="Week 5 reading"),
    Q("W5-10", C, "W5", "Some duplicate rows should NOT be deleted. Which is a legitimate repeat?",
      ["The same transaction imported twice during a merge", "A customer making multiple separate purchases",
       "A scraping error that copied a row", "A row entered twice by mistake"],
      "A customer making multiple separate purchases",
      "Use domain knowledge: repeated customer IDs in a transactions table are expected.",
      source="Week 5 reading - Removing Duplicate Records"),

    # ----- Week 6 -----
    Q("W6-1", C, "W6", "The Data Preparation phase has three interdependent tasks. Which are they?",
      ["Data collection, data storage, data reporting", "Data cleaning, data validation, feature engineering",
       "Model building, model evaluation, model deployment", "Stakeholder interviews, SWOT analysis, RACI mapping"],
      "Data cleaning, data validation, feature engineering",
      "Cleaning fixes errors and missing data, validation confirms rules/formats/logic, and feature engineering "
      "creates new variables.", source="Week 6 reading - Introduction"),
    Q("W6-2", C, "W6", "About how much of a data analyst's time is typically spent preparing data?",
      ["5-10%", "20-30%", "60-80%", "100%"],
      "60-80%", "That's more than modeling and reporting combined.", source="Week 6 reading"),
    Q("W6-3", C, "W6", "Lab 6 guidelines: a numeric column with OUTLIERS has some missing values. Best fill value?",
      ["The mean", "The median", "The maximum", "Always drop the column"],
      "The median",
      "Lab 6: 'Use median to replace missing values in numeric columns with outliers. Use 0 if missing "
      "means none. Use mode for categorical. Drop rows if only a few are missing and the column is essential.'",
      source="Lab 6 - Handle Missing Values guidelines"),
    Q("W6-4", C, "W6", "In Megatelco, a blank data_leftover_mb most likely means the customer had no leftover data. "
      "Lab 6 fills it with...",
      ["the median of the column", "the mean of the column", "0 (meaning none left over)",
       "the string 'unknown' as a label"],
      "0 (meaning none left over)", "Lab 6 code: df.loc[:, 'data_leftover_mb'] = df['data_leftover_mb'].fillna(0). Missing means 'none'.",
      source="Lab 6"),
    Q("W6-5", C, "W6", "Listwise deletion (complete-case analysis) means...",
      ["removing every ROW that has at least one missing value", "filling every missing value with the column mean",
       "using all available pairs when computing correlations",
       "creating a flag column that marks which values are missing"],
      "removing every ROW that has at least one missing value",
      "Simple, but can throw away lots of data and bias results if the data isn't missing completely at random (MCAR).",
      source="Week 6 reading - Deletion-Based Methods"),
    Q("W6-6", C, "W6", "For time-series sensor data with gaps, which imputation fits best?",
      ["Mode imputation (most frequent)", "Forward fill / interpolation", "Mean imputation across the whole series",
       "Listwise deletion of every gap"],
      "Forward fill / interpolation",
      "These assume continuity over time. The StreamFlow demo uses df['signup_date'].interpolate(method='linear').",
      source="Week 6 reading; Demo 6"),
    Q("W6-7", C, "W6", "'signup_date must not be after last_login_date' is an example of a...",
      ["range check", "logic check", "uniqueness constraint", "referential integrity check"],
      "logic check",
      "Range check = value within bounds (age 0-120). Logic check = consistency BETWEEN fields. "
      "Uniqueness = no duplicate IDs. Referential integrity = foreign keys match primary keys.",
      source="Week 6 reading - Data Validation"),
    Q("W6-8", C, "W6", "A sales table contains customer_id values that don't exist in the customer table. "
      "Which validation rule is broken?",
      ["Range check validation", "Referential integrity", "Data type enforcement", "Winsorizing outliers"],
      "Referential integrity", "Foreign keys in one table must match primary keys in the other.",
      source="Week 6 reading - 2.4"),
    Q("W6-9", C, "W6", "You're predicting churn in JANUARY and add a feature built from customers' FEBRUARY "
      "activity. What's the problem?",
      ["Curse of dimensionality", "Data leakage", "Multicollinearity", "Underfitting"],
      "Data leakage",
      "Leakage = using information that wouldn't be available at prediction time. It makes the model look "
      "unrealistically good.", source="Week 6 reading - Avoiding Data Leakage"),
    Q("W6-10", C, "W6", "Capping extreme values at the 1st and 99th percentiles (instead of deleting them) is called...",
      ["Normalization", "Winsorizing", "One-hot encoding", "Interpolation"],
      "Winsorizing", "Lab 6 Part 6: df['income'].quantile([0.01, 0.99]) then .clip(lower=..., upper=...).",
      source="Lab 6 - Part 6"),
    Q("W6-11", C, "W6", "Instead of silently deleting rows that fail validation, best practice is to...",
      ["ignore them and continue with the cleaned data", "log them for review and to track data-quality problems",
       "replace them with zeros so the rows are kept", "send the whole dataset to IT for a manual review"],
      "log them for review and to track data-quality problems",
      "Logging keeps the process transparent and lets you escalate systemic issues upstream.",
      source="Week 6 reading - 2.6 Logging Validation Errors"),

    # ----- Week 7 -----
    Q("W7-1", C, "W7", "DataFrame A has keys {SP01, SP02, SP03, SP04}, B has {SP02, SP03, SP04, SP05}. "
      "Which keys survive an INNER join?",
      ["SP01, SP02, SP03, SP04, SP05", "SP02, SP03, SP04", "SP01, SP02, SP03, SP04", "SP02, SP03, SP04, SP05"],
      "SP02, SP03, SP04",
      "Inner = only keys in BOTH. Left = all of A (SP01-04). Right = all of B (SP02-05). Outer = everything "
      "(SP01-05), with NaN where there's no match.", source="Week 7 reading - Merging"),
    Q("W7-2", C, "W7", "When is a LOG transformation appropriate?",
      ["For right-skewed data where all values are positive", "For categorical data that has many levels",
       "For left-skewed data with many negative values", "To combine columns from two different datasets"],
      "For right-skewed data where all values are positive",
      "log(0) is undefined, so add a small number (<=1) first when there are zeros.",
      source="Week 7 reading - Log Scaling"),
    Q("W7-3", C, "W7", "Min-Max normalization rescales values to 0-1. What is its main weakness?",
      ["It can only be used on text columns", "It is very sensitive to outliers",
       "It changes the order of the values", "It creates many extra columns"],
      "It is very sensitive to outliers",
      "One huge value (handset_price = 125,000!) squashes everyone else near 0. Z-score standardization "
      "is less affected. Formula: (x - min) / (max - min).", source="Week 7 reading - Min-Max"),
    Q("W7-4", C, "W7", "A value is 130, the mean is 100, the standard deviation is 20. What is its z-score?",
      ["0.15", "1.5", "1.57", "30"],
      "1.5",
      "(130 - 100) / 20 = 1.5, so it's 1.5 standard deviations above the mean. HEADS UP: the Week 7 reading "
      "prints 1.57, but that's a typo. The math gives 1.5.", source="Week 7 reading - Z-score"),
    Q("W7-5", C, "W7", "pd.cut() vs pd.qcut():",
      ["cut makes equal-width bins; qcut makes equal-frequency bins",
       "cut makes equal-frequency bins; qcut makes equal-width bins",
       "they make identical bins; only the function names differ",
       "cut works on numbers; qcut works only on text columns"],
      "cut makes equal-width bins; qcut makes equal-frequency bins",
      "Lab 7: pd.qcut(df['income'], q=3, labels=['Low','Medium','High']) puts roughly the same number of "
      "customers in each group.", source="Week 7 reading - Binning; Lab 7"),
    Q("W7-6", C, "W7", "operating_system (Android/IOS) is NOMINAL. Which encoding should you use?",
      ["Ordinal encoding (Android=1, IOS=2)", "One-hot encoding (one column per OS)",
       "Log transform (to reduce the skew)", "Min-Max scaling (rescale to 0-1)"],
      "One-hot encoding (one column per OS)",
      "One-hot for nominal (no order), so the model doesn't assume IOS > Android. Ordinal encoding is "
      "only for ordered categories like satisfaction low < avg < high.", source="Week 7 reading; Lab 7 Part 5"),
    Q("W7-7", C, "W7", "What is a downside of one-hot encoding a column with hundreds of categories?",
      ["It loses the order of the categories", "It adds a very large number of new columns",
       "It only works if the column contains numbers", "It leaks information from the test data"],
      "It adds a very large number of new columns",
      "That feeds the curse of dimensionality. Binary encoding is one alternative for high-cardinality columns.",
      source="Week 7 reading - Variable Encoding"),
    Q("W7-8", C, "W7", "Target encoding (replacing a category with the average target value) must be done "
      "carefully because...",
      ["it can only be applied to numeric columns with no outliers",
       "it can cause data leakage unless cross-validation is used", "it always creates one new column per category",
       "it requires the data to be reduced with PCA first"],
      "it can cause data leakage unless cross-validation is used",
      "It uses the target itself to build a feature.", source="Week 7 reading"),
    Q("W7-9", C, "W7", "Which is NOT a symptom of the curse of dimensionality?",
      ["Data points become very sparse", "Distance metrics lose their meaning", "Overfitting risk increases",
       "Models become easier to interpret"],
      "Models become easier to interpret",
      "The opposite is true: more dimensions are harder to visualize and interpret, and cost more to compute.",
      source="Week 7 reading - Curse of dimensionality"),
    Q("W7-10", C, "W7", "Which statement about PCA is TRUE?",
      ["It is supervised and uses the target variable to choose components",
       "It makes uncorrelated components; the first explains the most variance",
       "It makes the original features easier to interpret for stakeholders",
       "It works equally well on unscaled data with different units"],
      "It makes uncorrelated components; the first explains the most variance",
      "PCA is UNSUPERVISED, the components are harder to interpret, and it's sensitive to scale, so "
      "standardize first.", source="Week 7 reading - PCA"),
    Q("W7-11", C, "W7", "Lasso regression selecting features during training is which feature-selection approach?",
      ["Filter", "Wrapper", "Embedded", "Manual"],
      "Embedded",
      "Filter = statistical tests on each feature (correlation). Wrapper = test feature subsets by model "
      "performance (recursive feature elimination). Embedded = selection happens inside model training (Lasso, tree importance).",
      source="Week 7 reading - Feature Selection"),
    Q("W7-12", C, "W7", "Why split data into TRAINING and TEST sets?",
      ["To make the dataset smaller so the model trains faster",
       "To evaluate the model on unseen data and check generalization",
       "Because pandas will not fit a model on one dataset alone",
       "To create additional features that the model can learn from"],
      "To evaluate the model on unseen data and check generalization",
      "Training data = learn the patterns. Test data = honest check on data the model never saw.",
      source="Week 7 reading - 4.2"),
    Q("W7-13", C, "W7", "Feature engineering differs from general data transformation because its focus is...",
      ["making raw data usable, clean and consistent", "improving model performance using domain knowledge",
       "storing the transformed data in a cloud database", "deleting the columns the model does not need"],
      "improving model performance using domain knowledge",
      "Transformation makes data USABLE. Feature engineering makes it USEFUL for prediction (ratios like "
      "debt-to-income, BMI, price per square foot).", source="Week 7 reading"),
    Q("W7-14", C, "W7", "Z-score standardization transforms a variable so that it has...",
      ["a range from 0 to 1 for every value", "a mean of 0 and a standard deviation of 1",
       "only positive values after rescaling", "no outliers, since extreme values are removed"],
      "a mean of 0 and a standard deviation of 1",
      "Formula: z = (x - mean) / std. Min-Max is the 0-to-1 one.", source="Week 7 reading"),
]

# ---------------------------------------------------------------------------
# CODE READING - pandas from Labs 2-7. Every one of these runs in the Code Lab.
# ---------------------------------------------------------------------------
K = "Code Reading"
BANK += [
    Q("K1", K, "PY", "What does this line do?",
      ["Reads a CSV file from a URL into a DataFrame named df", "Installs the pandas library from the web address",
       "Uploads the DataFrame df to the GitHub repository", "Opens the file in Excel and shows the first five rows"],
      "Reads a CSV file from a URL into a DataFrame named df",
      "pd.read_csv() reads comma-separated text into a DataFrame. It works with a URL too, which is how "
      "Labs 4-7 pull data straight from GitHub. (In the Code Lab this uses the embedded sample instead of the internet.)",
      data="megatelco",
      src="""
        url = "https://raw.githubusercontent.com/Stan-Pugsley/is_4487_base/refs/heads/main/DataSets/megatelco_leave_survey_data_cleaning_v2.csv"
        df = pd.read_csv(url)
        df.head()
      """, source="Labs 4-7"),
    Q("K2", K, "PY", "What is the PURPOSE of df.info()?",
      ["Shows summary statistics such as the mean, median and quartiles",
       "Shows the size, column names, non-null counts and data types",
       "Shows the first five rows of the DataFrame as a table", "Removes the columns that have no non-null values"],
      "Shows the size, column names, non-null counts and data types",
      "Lab 2: info() = high-level overview (size, names, types, missing values). head() = first rows. "
      "describe() = summary stats.", data="megatelco", src="df.info()", source="Lab 2 - Preview the Dataset"),
    Q("K3", K, "PY", "By default, which columns does df.describe() summarize?",
      ["Only the text (object) columns", "Only the numeric columns", "Every column, including the text columns",
       "Only the first column of the DataFrame"],
      "Only the numeric columns",
      "Lab 6: 'df.describe() only provides summary for numeric and date type variables.' For text/categories use value_counts().",
      data="megatelco", src="df.describe()", source="Lab 2 & Lab 6"),
    Q("K4", K, "PY", "The Megatelco sample has 40 rows and 16 columns. What does this print?",
      ["40", "16", "(40, 16)", "(16, 40)"],
      "(40, 16)", "df.shape is a tuple: (rows, columns). Note there are no parentheses after shape, because it's an attribute, not a method.",
      data="megatelco", src="print(df.shape)", source="Lab 4 Part 1; Lab 6"),
    Q("K5", K, "PY", "What is the purpose of this line?",
      ["Removes all spaces from the values inside each column",
       "Standardizes the column names (trim, lowercase, underscores)",
       "Converts every column in the DataFrame to string type", "Sorts the columns alphabetically by their new names"],
      "Standardizes the column names (trim, lowercase, underscores)",
      "' Data Overage Mb' becomes 'data_overage_mb'. It only touches the column NAMES (df.columns), not the values. "
      "Consistent names stop code from breaking (Lab 6 Part 1).",
      data="megatelco", setup=MESSY_COLUMNS,
      src="""
        print(list(df.columns)[:4])
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        print(list(df.columns)[:4])
      """, source="Lab 6 & Lab 7"),
    Q("K6", K, "PY", "What does value_counts() show for a column?",
      ["The count of non-missing values in the column", "How many times each unique value appears",
       "The sum of all the values in the column", "The number of columns in the DataFrame"],
      "How many times each unique value appears",
      "It's the main tool for inspecting categorical/text columns (Lab 6), e.g. leave: STAY vs LEAVE counts.",
      data="megatelco", src="df['leave'].value_counts()", source="Lab 4 & Lab 6"),
    Q("K7", K, "PY", "Why would you run this?",
      ["To convert operating_system into numeric codes", "To store operating_system with the category dtype",
       "To delete operating_system from the DataFrame", "To sort the DataFrame by operating_system values"],
      "To store operating_system with the category dtype",
      "Repeated text values with a small fixed set of options belong in category. It also uses less memory and "
      "makes intent clear. Run it in the Code Lab to watch the dtype change.",
      data="megatelco", src="df['operating_system'] = df['operating_system'].astype('category')", source="Lab 6 Part 2"),
    Q("K8", K, "PY", "What makes this different from a plain .astype('category')?",
      ["Nothing; the two approaches give the same result", "It creates an ordered category: low < avg < high",
       "It converts the satisfaction column into numbers", "It removes rows whose satisfaction is 'avg'"],
      "It creates an ordered category: low < avg < high",
      "ordered=True means comparisons like df['reported_satisfaction'] > 'low' make sense. Satisfaction is ordinal, not nominal.",
      data="megatelco",
      src="""
        df['reported_satisfaction'] = pd.Categorical(df['reported_satisfaction'],
                                                     categories=['low', 'avg', 'high'], ordered=True)
        print(df['reported_satisfaction'].cat.categories)
        print((df['reported_satisfaction'] > 'low').sum(), "customers are above 'low'")
      """, source="Lab 6 Part 2"),
    Q("K9", K, "PY", "TRAP from Lab 7: the Megatelco data stores satisfaction as 'low', 'avg', 'high' "
      "(lowercase). What happens when this runs?",
      ["Works fine and the satisfaction levels are ordered Low < Medium < High",
       "Every value becomes NaN because the labels don't match the categories",
       "Python raises an error because the labels don't match the categories",
       "Only 'avg' becomes NaN because it isn't in the categories list"],
      "Every value becomes NaN because the labels don't match the categories",
      "pd.Categorical silently turns any value NOT in categories into NaN, and string matching is case-sensitive. "
      "Always check value_counts() first! Watch the missing count jump in the Code Lab.",
      data="megatelco",
      src="""
        df['reported_satisfaction'] = pd.Categorical(df['reported_satisfaction'],
                                                     categories=['Low', 'Medium', 'High'], ordered=True)
        print(df['reported_satisfaction'].isnull().sum(), "missing values now")
      """, source="Lab 7 Part 1 (as written in the lab)"),
    Q("K10", K, "PY", "TRAP from Lab 7: 'leave' contains 'LEAVE' and 'STAY'. What does this produce?",
      ["leave becomes 1 for LEAVE customers and 0 for STAY customers",
       "Every value becomes NaN because the dictionary keys don't match",
       "Python raises a KeyError because 'LEAVE' is not a key",
       "Nothing changes because map() leaves unmatched values as they are"],
      "Every value becomes NaN because the dictionary keys don't match",
      "The dictionary keys are 'yes'/'no', but the data says 'LEAVE'/'STAY'. The working version is "
      "df['leave'].map({'LEAVE': 1, 'STAY': 0}). Lab 6's task asks you to do exactly this conversion.",
      data="megatelco",
      src="""
        df['leave'] = df['leave'].map({'yes': 1, 'no': 0})
        print(df['leave'].value_counts(dropna=False))
      """, source="Lab 7 Part 1 (as written in the lab)"),
    Q("K11", K, "PY", "What does this line do?",
      ["Deletes the rows in which handset_price is missing", "Replaces missing handset_price values with the median",
       "Replaces every handset_price value with the median", "Calculates the median handset_price and prints it"],
      "Replaces missing handset_price values with the median",
      "fillna() only touches the NaN cells. Median is used because handset_price has outliers (125,000 and -200!).",
      data="megatelco", src="df['handset_price'] = df['handset_price'].fillna(df['handset_price'].median())",
      source="Lab 6 Part 3"),
    Q("K12", K, "PY", "What does this do?",
      ["Drops the income column and keeps all the rows", "Drops only the rows where income is missing",
       "Drops every row that has any missing value in any column",
       "Fills the missing income values with zero instead of dropping"],
      "Drops only the rows where income is missing",
      "subset= limits the check to the listed columns. Plain df.dropna() would remove rows missing ANYTHING "
      "(listwise deletion), which would delete far more rows here.",
      data="megatelco",
      src="""
        print(len(df), "rows before")
        df = df.dropna(subset=['income']).copy()
        print(len(df), "rows after")
      """, source="Lab 6 Part 3"),
    Q("K13", K, "PY", "In this 40-row Megatelco sample, what does the code print? (Hint: duplicated() "
      "flags rows that are exact copies of an EARLIER row.)",
      ["Number of duplicate rows: 0", "Number of duplicate rows: 1", "Number of duplicate rows: 2", "Number of duplicate rows: 40"],
      "Number of duplicate rows: 1",
      "Customer 13678 appears twice. duplicated() marks only the SECOND copy, so the sum is 1. "
      "drop_duplicates() keeps the first copy by default.",
      data="megatelco", src="print(f\"Number of duplicate rows: {df.duplicated().sum()}\")", source="Lab 6 Part 4"),
    Q("K14", K, "PY", "TRAP: the sample has 1 negative handset_price (-200) and 2 MISSING handset_price values. "
      "How many rows are left after this filter? (starting from 40)",
      ["39", "38", "37", "40"],
      "37",
      "NaN >= 0 evaluates to False, so the missing rows get dropped too, not just the -200. That's why "
      "Lab 6 fills missing handset_price with the median BEFORE running the business-rule filters.",
      data="megatelco",
      src="""
        df = df[df['handset_price'] >= 0]
        print(len(df))
      """, source="Lab 6 Part 5"),
    Q("K15", K, "PY", "What is the purpose of this block?",
      ["Deletes the rows in the top and bottom 1% of income",
       "Caps income at its 1st and 99th percentiles (Winsorizing)",
       "Rescales income to a 0-1 range using min and max", "Fills the missing income values with the 99th percentile"],
      "Caps income at its 1st and 99th percentiles (Winsorizing)",
      ".quantile([0.01, 0.99]) finds the cutoffs and .clip() pulls anything outside them back to the cutoff. "
      "No rows are removed: the -65000 income becomes the 1st-percentile value.",
      data="megatelco", setup="df = df.dropna(subset=['income']).copy()",
      src="""
        income_min, income_max = df['income'].quantile([0.01, 0.99])
        df.loc[:, 'income'] = df['income'].clip(lower=income_min, upper=income_max)
      """, source="Lab 6 Part 6"),
    Q("K16", K, "PY", "This is the IQR method. What does the last line keep?",
      ["Only the rows whose text_message_count is above the upper fence",
       "Rows within Q1 - 1.5*IQR and Q3 + 1.5*IQR (outliers removed)",
       "Only the rows above the median text_message_count", "All of the rows, because the filter only adds columns"],
      "Rows within Q1 - 1.5*IQR and Q3 + 1.5*IQR (outliers removed)",
      "This is the Lab 6 Part 5 task: set thresholds with the IQR, then boolean-filter. & means AND.",
      data="megatelco", setup=LAB6_CLEAN,
      src="""
        q1 = df['text_message_count'].quantile(0.25)
        q3 = df['text_message_count'].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df = df[(df['text_message_count'] >= lower) & (df['text_message_count'] <= upper)]
      """, source="Lab 6 Part 5; Week 5 reading"),
    Q("K17", K, "PY", "What does this produce?",
      ["The 10 cheapest listings in the entire rental dataset", "The 10 neighborhoods with the highest average price",
       "The number of listings in each of the top 10 neighborhoods",
       "The 10 most expensive individual listings in the dataset"],
      "The 10 neighborhoods with the highest average price",
      "Read it left to right: group by nhood -> take price -> mean -> sort descending -> first 10.",
      data="rent", src="df.groupby('nhood')['price'].mean().sort_values(ascending=False).head(10)",
      source="Lab 4 Part 3"),
    Q("K18", K, "PY", "What does .corr() return here?",
      ["A single correlation number for the whole table", "A correlation matrix for every pair of the columns",
       "The covariance matrix of the four selected columns", "A scatterplot matrix of the four selected columns"],
      "A correlation matrix for every pair of the columns",
      "Lab 5 then visualizes it with sns.heatmap(corr_matrix, annot=True, cmap='coolwarm'). The diagonal is always 1.",
      data="spotifool", src="df[['danceability', 'energy', 'tempo', 'downloads']].corr()", source="Lab 5 Part 4"),
    Q("K19", K, "PY", "What chart does this create, and what does bins=30 control?",
      ["A bar chart of price, where bins=30 sets the number of bars",
       "A histogram of price, where bins=30 sets how many intervals",
       "A boxplot of price, where bins=30 sets the number of whiskers",
       "A scatterplot of price, where bins=30 sets the number of points"],
      "A histogram of price, where bins=30 sets how many intervals",
      "In the Code Lab, notice how the one $33,000 listing stretches the x-axis and squeezes everything else "
      "into the first few bins. That's an outlier showing up in a chart.",
      data="rent",
      src="""
        plt.hist(df['price'], bins=30)
        plt.title("Distribution of Rental Prices")
        plt.xlabel("Price ($)")
        plt.ylabel("Count")
        plt.show()
      """, source="Lab 5 Part 3"),
    Q("K20", K, "PY", "What new column does this create?",
      ["A True/False column that flags the customers who sent over 500 texts",
       "A 1/0 flag column: 1 if the customer sent more than 500 texts",
       "A column that holds the number of texts above 500", "A column that replaces text_message_count with 1 and 0"],
      "A 1/0 flag column: 1 if the customer sent more than 500 texts",
      "(condition) creates True/False, and .astype(int) turns True/False into 1/0. That's a binary flag feature (Lab 7).",
      data="megatelco",
      src="""
        df['high_texter'] = (df['text_message_count'] > 500).astype(int)
        df['high_texter'].value_counts()
      """, source="Lab 7 Part 2"),
    Q("K21", K, "PY", "Why is 1 added to the denominator?",
      ["To round the ratio to the nearest whole number", "To avoid dividing by zero when data_mb_used is 0",
       "To convert the ratio to a percentage value", "It is a typo and does not change the result"],
      "To avoid dividing by zero when data_mb_used is 0",
      "This is feature creation: a ratio feature (Lab 7 Part 2).",
      data="megatelco", setup=LAB6_CLEAN,
      src="df['overage_ratio'] = df['data_overage_mb'] / (df['data_mb_used'] + 1)", source="Lab 7 Part 2"),
    Q("K22", K, "PY", "What does pd.qcut(..., q=3, labels=[...]) do here?",
      ["Splits income into 3 ranges of equal width (same dollar span), labeled Low/Medium/High",
       "Splits income into 3 groups with about equal counts, labeled Low/Medium/High",
       "Sorts the incomes and labels the top third High, dropping the rest",
       "Creates 3 new columns, one for each of Low, Medium and High"],
      "Splits income into 3 groups with about equal counts, labeled Low/Medium/High",
      "qcut = quantile (equal-frequency) bins. value_counts() shows about the same count in each group.",
      data="megatelco", setup=LAB6_CLEAN,
      src="""
        df['income_group'] = pd.qcut(df['income'], q=3, labels=['Low', 'Medium', 'High'])
        df['income_group'].value_counts()
      """, source="Lab 7 Part 3"),
    Q("K23", K, "PY", "How is this different from qcut?",
      ["It isn't; both functions split the data into equal-sized groups",
       "pd.cut makes 3 equal-width ranges, so group sizes can be uneven",
       "pd.cut only sorts the rows; it does not create groups", "pd.cut only works on text columns, not numeric ones"],
      "pd.cut makes 3 equal-width ranges, so group sizes can be uneven",
      "Equal-width bins on skewed data put most rows in one bin. Compare the value_counts with K22's in the Code Lab.",
      data="megatelco", setup=LAB6_CLEAN,
      src="""
        df['usage_group'] = pd.cut(df['data_mb_used'], bins=3, labels=['Light', 'Moderate', 'Heavy'])
        df['usage_group'].value_counts()
      """, source="Lab 7 Part 3 task"),
    Q("K24", K, "PY", "operating_system has 2 values (Android, IOS). After this line, what happens to the columns?",
      ["Nothing changes, because get_dummies only reports the categories",
       "operating_system becomes two columns: os_Android and os_IOS",
       "operating_system is recoded as the numbers 1 (Android) and 2 (IOS)",
       "A new True/False column is added for each customer in the data"],
      "operating_system becomes two columns: os_Android and os_IOS",
      "One-hot encoding: one new column per category (newer pandas shows True/False instead of 1/0), and the original column is dropped. Shape goes from 16 to 17 columns (-1 +2).",
      data="megatelco",
      src="""
        print(df.shape)
        df_encoded = pd.get_dummies(df, columns=['operating_system'], prefix='os')
        print(df_encoded.shape)
        df_encoded.filter(like='os_').head()
      """, source="Lab 7 Part 5"),
    Q("K25", K, "PY", "After MinMaxScaler, what is the range of income_scaled?",
      ["-1 to 1", "0 to 1", "mean 0, std 1", "the same as income"],
      "0 to 1",
      "MinMaxScaler applies (x - min) / (max - min). StandardScaler would give mean 0 and std 1. "
      "(Needs scikit-learn installed to run.)",
      data="megatelco", setup=LAB6_CLEAN,
      src="""
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df[['income', 'data_mb_used']])
        df['income_scaled'] = df_scaled[:, 0]
        df['income_scaled'].describe()
      """, source="Lab 7 Part 4"),
    Q("K26", K, "PY", "What is the difference between these two lines' results?",
      ["No difference; both lines return the same type of object, namely a DataFrame",
       "df['price'] returns a Series; df[['price', 'beds']] returns a DataFrame",
       "The first returns a DataFrame and the second returns a list",
       "The second line causes an error because of the double brackets"],
      "df['price'] returns a Series; df[['price', 'beds']] returns a DataFrame",
      "Single brackets with one name give a Series. Double brackets (a LIST of names) give a DataFrame. Lab 2 task 1.3 uses df[['mpg','hp']].",
      data="rent",
      src="""
        a = df['price']
        b = df[['price', 'beds']]
        print(type(a).__name__, type(b).__name__)
      """, source="Lab 2; Lab 4"),
    Q("K27", K, "PY", "What does this sort do?",
      ["Sorts by price only, and ignores the beds column",
       "Sorts by beds first, then by price within each beds value",
       "Sorts by price first, then by beds within each price", "Sorts by beds and price, both in descending order"],
      "Sorts by beds first, then by price within each beds value",
      "This is Lab 2 task 4.2 ('sort by cyl and then by hp'). The first column in the list is the primary sort.",
      data="rent", src="df.sort_values(['beds', 'price']).head(8)", source="Lab 2 Task 4"),
    Q("K28", K, "PY", "Why does Lab 6 make this copy right after loading the data?",
      ["To make the dataset twice as large for training", "To keep an untouched original copy while df is cleaned",
       "To convert every column to its correct data type", "To remove duplicate rows from the DataFrame"],
      "To keep an untouched original copy while df is cleaned",
      "Week 4 best practice: 'Back up raw data. Never overwrite your original dataset.' Lab 6 Part 4 counts "
      "duplicates on copied_df later.", data="megatelco", src="copied_df = df.copy(deep=True)", source="Lab 6"),
    Q("K29", K, "PY", "StreamFlow has ages of -10 and 150. What does this block do?",
      ["Deletes every customer whose age is under 18 or over 120 from the whole dataset",
       "Sets ages under 18 or over 120 to missing, then fills them with the median",
       "Clips ages under 18 up to 18 and ages over 120 down to 120",
       "Calculates the average age of the customers who are 18 to 120"],
      "Sets ages under 18 or over 120 to missing, then fills them with the median",
      "| means OR. .loc[rows, 'age'] = np.nan blanks out the bad values, and fillna(median) imputes them. "
      "The rows are kept, which matters with a small (250-row) dataset.",
      data="streamflow",
      src="""
        df.loc[(df['age'] < 18) | (df['age'] > 120), 'age'] = np.nan
        df['age'] = df['age'].fillna(df['age'].median()).round().astype(int)
        df['age'].describe()
      """, source="Demo 6 (StreamFlow)"),
    Q("K30", K, "PY", "StreamFlow has dates like '2022-13-01' and 'not a date'. What does errors='coerce' do?",
      ["Raises an error when a date is invalid", "Turns dates it cannot parse into NaT (missing)",
       "Deletes the rows that contain bad dates", "Guesses the closest valid date for each bad value"],
      "Turns dates it cannot parse into NaT (missing)",
      "Week 6: 'invalid dates will be set to NaT, which can be flagged and handled separately.' Converting "
      "the type is what REVEALED these missing dates.",
      data="streamflow",
      src="""
        df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
        print(df['signup_date'].isnull().sum(), "bad dates became NaT")
      """, source="Demo 6; Week 6 reading 2.2"),
    Q("K31", K, "PY", "gender is ~33% each of Male/Female/Non-binary with some missing. Why does Demo 6 do this "
      "instead of filling with the mode?",
      ["Because the mode is impossible to compute for text categories",
       "Mode fill would distort the even split; 'Unknown' assumes nothing",
       "Because rows with a missing gender should be deleted instead",
       "Because fillna cannot be used on category columns at all"],
      "Mode fill would distort the even split; 'Unknown' assumes nothing",
      "A category column must have 'Unknown' ADDED as an allowed value before fillna can use it. The demo also "
      "notes that imputing a sensitive attribute raises ethical concerns.",
      data="streamflow", setup="df['gender'] = df['gender'].astype('category')",
      src="""
        df['gender'] = df['gender'].cat.add_categories('Unknown')
        df['gender'] = df['gender'].fillna('Unknown')
        df['gender'].value_counts(dropna=False)
      """, source="Demo 6 (StreamFlow)"),
    Q("K32", K, "PY", "What does this filter keep?",
      ["Loans that are Defaulted OR have ApplicantIncome over 5000",
       "Loans that are Defaulted AND have ApplicantIncome over 5000",
       "Every loan, with only the three listed columns shown",
       "An error, because two filters cannot be combined this way"],
      "Loans that are Defaulted AND have ApplicantIncome over 5000",
      "& = AND, | = OR. Each condition needs its own parentheses.",
      data="fintrust",
      src="""
        risky = df[(df['LoanStatus'] == 'Defaulted') & (df['ApplicantIncome'] > 5000)]
        risky[['Loan_ID', 'ApplicantIncome', 'LoanStatus']]
      """, source="Week 5 case (FinTrust)"),
    Q("K33", K, "PY", "What does this return for the FinTrust sample?",
      ["The average loan amount of Defaulted loans in each EmploymentStatus group",
       "The share of loans that Defaulted in each EmploymentStatus group",
       "The count of Defaulted loans in each EmploymentStatus group",
       "A bar chart of default counts for each EmploymentStatus group"],
      "The share of loans that Defaulted in each EmploymentStatus group",
      "(LoanStatus == 'Defaulted') is True/False, and the mean of True/False is the fraction that are True. "
      "groupby then does that per group. This is the 'default rates across employment types' task from the Week 5 case.",
      data="fintrust",
      src="""
        df['defaulted'] = (df['LoanStatus'] == 'Defaulted')
        df.groupby('EmploymentStatus')['defaulted'].mean()
      """, source="Week 5 case (FinTrust)"),
    Q("K34", K, "PY", "What does np.log1p do to a right-skewed column like income?",
      ["Removes the skew by dropping the largest values", "Compresses the large values to reduce the right skew",
       "Rescales the column so that its values run from 0 to 1", "Sorts the column from smallest to largest"],
      "Compresses the large values to reduce the right skew",
      "log(0) is undefined, so log1p adds 1 first (the Week 7 'add a small number' tip). Compare the skew before and after in the Code Lab.",
      data="spotifool",
      src="""
        print(round(df['downloads'].skew(), 2))
        df['log_downloads'] = np.log1p(df['downloads'])
        print(round(df['log_downloads'].skew(), 2))
      """, source="Week 7 reading - Log Scaling"),
    Q("K35", K, "PY", "What kind of join is this, and which rows are kept?",
      ["Inner join: only the customers found in both tables",
       "Left join: all customers kept; missing plans become NaN",
       "Outer join: every row from both tables is kept, with NaN gaps", "Right join: every row of plans is kept"],
      "Left join: all customers kept; missing plans become NaN",
      "how='left' keeps the LEFT table intact. Customer C4 has no plan, so its plan columns are NaN.",
      src="""
        customers = pd.DataFrame({'cust_id': ['C1', 'C2', 'C3', 'C4'], 'region': ['N', 'S', 'E', 'W']})
        plans = pd.DataFrame({'cust_id': ['C1', 'C2', 'C3', 'C5'], 'plan': ['Basic', 'Premium', 'Basic', 'Standard']})
        merged = pd.merge(customers, plans, on='cust_id', how='left')
        merged
      """, source="Week 7 reading - Merging"),
    Q("K36", K, "PY", "Why does Lab 6 use .loc[:, 'col'] on the left side here?",
      ["It makes the assignment run faster on large data", "To make sure the original DataFrame is actually updated",
       "To select only the first column and ignore the rest", "It converts the column to the category type"],
      "To make sure the original DataFrame is actually updated",
      "Lab 6 note: 'When assigning values to a DataFrame, especially after filtering or copying, it's best to use .loc.'",
      data="megatelco", src="df.loc[:, 'data_leftover_mb'] = df['data_leftover_mb'].fillna(0)", source="Lab 6 Part 3 note"),
    Q("K37", K, "PY", "What does this create?",
      ["A pie chart of the 10 largest neighborhoods", "A bar chart of the 10 most common neighborhoods",
       "A histogram of price for the top 10 listings", "A scatterplot of nhood against price for 10 listings"],
      "A bar chart of the 10 most common neighborhoods",
      "value_counts().head(10) gives the top 10 categories by count, and sns.barplot draws them (Lab 5 Part 3). "
      "Bar charts are the go-to chart for categorical variables.",
      data="rent",
      src="""
        top_nhoods = df['nhood'].value_counts().head(10)
        sns.barplot(x=top_nhoods.values, y=top_nhoods.index)
        plt.title("Top 10 Neighborhoods by Listing Count")
        plt.show()
      """, source="Lab 5 Part 3"),
]

# ---------------------------------------------------------------------------
# BUSINESS CASES - "about half of the questions will use business case questions"
# ---------------------------------------------------------------------------
B = "Business Cases"
FINTRUST_CONTEXT = ("FINTRUST BANK (Week 5 case): find which customers are likely to default. Columns: "
                    "Loan_ID, Gender, Age, Married, Education, EmploymentStatus, ApplicantIncome, LoanAmount, "
                    "LoanTerm, CreditScore (300-850), HasPreviousDefaults (1/0), LoanStatus (Defaulted/Paid)")
STREAMFLOW_CONTEXT = ("STREAMFLOW (Week 6 case/demo): streaming service building a churn model. 250 customers. Columns: "
                      "customer_id, signup_date, age, gender, region, monthly_fee, total_streaming_hours, "
                      "num_devices, plan_type, support_tickets_last_6mo, churned (1/0)")
RENT_CONTEXT = ("SF RENTALS (Labs 4 & 5): Craigslist rental listings. Columns: post_id, date, year, nhood, city, "
                "county, price, beds, baths, sqft, room_in_apt (0 = whole apartment, 1 = a room), address, lat, lon, "
                "title, descr, details. Many columns are mostly empty.")
BANK += [
    Q("B1", B, "W2", "Megatelco wants to know which current customers will LEAVE when their contract expires. "
      "What kind of analytics problem is this?",
      ["Unsupervised clustering of customer groups", "Supervised classification with leave as the target",
       "Supervised regression with income as the target", "Descriptive reporting of last year's churn"],
      "Supervised classification with leave as the target",
      "Historical LEAVE/STAY labels exist, so it's supervised. The target is a category, so it's classification. "
      "The Week 3 sample charter: 'Predict which customers will churn using a classification model.'",
      context=MEGATELCO_CONTEXT, source="Week 2 slides & Week 3 sample charter"),
    Q("B2", B, "W3", "MegaTelCo loses 20% of customers each period. Which is the BUSINESS OBJECTIVE (not the data mining goal)?",
      ["Build a classification model that predicts which customers will leave",
       "Match the last campaign's 2% retention gain while spending much less",
       "Compute the correlation between income and leave for all customers",
       "One-hot encode operating_system before fitting the model"],
      "Match the last campaign's 2% retention gain while spending much less",
      "That's the benchmark for success in the sample MegaTelCo charter. The model is the data mining goal that supports it.",
      context=MEGATELCO_CONTEXT, source="Week 3 slides - Sample Project Charter: MegaTelCo"),
    Q("B3", B, "W5", "Megatelco's handset_price has a max of 125,000 and a min of -200. What's the BEST first step?",
      ["Ignore them, because most models handle outliers on their own",
       "Check both values against business rules before changing anything",
       "Delete the handset_price column since it has bad values",
       "Replace both extreme values with the mean right away"],
      "Check both values against business rules before changing anything",
      "Lab 6: 'Some outliers may be removed using business logic... ask business experts for the max/min values "
      "that are possible.' Lab 6 removes handset_price < 0. Error -> fix/remove. Rare but real -> keep or cap.",
      context=MEGATELCO_CONTEXT, data="megatelco", src="df['handset_price'].describe()", source="Lab 6 Part 5"),
    Q("B4", B, "W6", "considering_change_of_plan (yes/no) is missing for some Megatelco customers. Lab 6 suggests "
      "which options for a CATEGORICAL column? (Select all that apply)",
      ["Fill with the mode (most common value)", "Fill with a placeholder such as 'unknown'",
       "Fill with the mean of the other customers", "Drop those rows if there are only a few"],
      ["Fill with the mode (most common value)", "Fill with a placeholder such as 'unknown'",
       "Drop those rows if there are only a few"],
      "You can't take the mean of yes/no. Lab 6 Part 3: 'For categories, would a placeholder like \"unknown\" or "
      "the most common value (mode) work? Or is it better to drop those rows?'",
      kind="multi", context=MEGATELCO_CONTEXT, source="Lab 6 Part 3"),
    Q("B5", B, "W5", "FinTrust wants to compare ApplicantIncome between Defaulted and Paid loans. Which chart does the "
      "case ask for?",
      ["A pie chart showing the share of income by LoanStatus", "A boxplot of ApplicantIncome grouped by LoanStatus",
       "A histogram of Loan_ID split by LoanStatus", "A line chart of ApplicantIncome across Loan_ID"],
      "A boxplot of ApplicantIncome grouped by LoanStatus",
      "Grouped boxplots compare a numeric variable ACROSS categories (Week 5 reading, bivariate section).",
      context=FINTRUST_CONTEXT, data="fintrust",
      src="""
        sns.boxplot(x='LoanStatus', y='ApplicantIncome', data=df)
        plt.title("Applicant Income by Loan Status")
        plt.show()
      """, source="Week 5 case - Visualization task"),
    Q("B6", B, "W5", "The FinTrust case asks: 'Could using Gender or Marital Status to predict default raise fairness "
      "concerns?' What's the best answer?",
      ["No, because adding more variables always improves fairness",
       "Yes, they can encode historical bias, so audit the model for fairness",
       "Only if the model is a complex neural network rather than a simple one",
       "No, because demographic data is anonymous by definition"],
      "Yes, they can encode historical bias, so audit the model for fairness",
      "Week 5 ethics section: avoid bias and discrimination, audit models, engage diverse stakeholders. Lending "
      "decisions are also regulated.", context=FINTRUST_CONTEXT, source="Week 5 case - Ethical Reflection"),
    Q("B7", B, "W6", "A FinTrust LoanAmount is -24,040. Which kind of validation catches this?",
      ["Range check", "Referential integrity", "Uniqueness constraint", "Schema naming"],
      "Range check", "A loan amount must be > 0. That's a range check based on domain knowledge.",
      context=FINTRUST_CONTEXT, data="fintrust", src="df[df['LoanAmount'] < 0]", source="Week 6 reading 2.1"),
    Q("B8", B, "W6", "Which FinTrust check enforces a UNIQUENESS constraint?",
      ["(df['LoanAmount'] > 0).all()", "df['Loan_ID'].duplicated().sum() == 0",
       "df['CreditScore'].between(300, 850).all()", "df.isnull().sum().sum() == 0"],
      "df['Loan_ID'].duplicated().sum() == 0",
      "Primary keys like Loan_ID must be unique. CreditScore.between(300, 850) is a RANGE check.",
      context=FINTRUST_CONTEXT, data="fintrust", src="print(df['Loan_ID'].duplicated().sum())", source="Week 5 case; Week 6 reading 2.3"),
    Q("B9", B, "W6", "StreamFlow has only 250 rows and wants to keep as much data as possible for ML. A few ages are "
      "-10 and 150. Best approach?",
      ["Delete every row where the age is impossible, to keep the data clean",
       "Mark impossible ages as missing, then impute with the median",
       "Leave the ages as they are, because outliers don't matter",
       "Replace the impossible ages with 0 so they stay in the data"],
      "Mark impossible ages as missing, then impute with the median",
      "That's exactly what Demo 6 does. With a small dataset you drop as few rows as possible, and the median is "
      "robust to the remaining edge cases.", context=STREAMFLOW_CONTEXT, source="Demo 6"),
    Q("B10", B, "W6", "StreamFlow is predicting churn. Which feature would cause DATA LEAKAGE?",
      ["monthly_fee (the plan price the customer pays)", "num_devices (devices linked to the account)",
       "cancellation_reason (filled in at cancellation)", "region (where the customer lives)"],
      "cancellation_reason (filled in at cancellation)",
      "It only exists AFTER the customer churns, so it wouldn't be known at prediction time. The model would look "
      "amazing and be useless.", context=STREAMFLOW_CONTEXT, source="Week 6 reading 3.6"),
    Q("B11", B, "W4", "In the SF rentals data, room_in_apt is 0 or 1. What type of variable is it?",
      ["Continuous (numeric)", "Binary (categorical)", "Ordinal (ranked categories)", "Text (free-form)"],
      "Binary (categorical)", "0 = entire apartment, 1 = single room. The data dictionary calls it Binary.",
      context=RENT_CONTEXT, source="Labs 4/5 data dictionary"),
    Q("B12", B, "W5", "One SF listing in a historically ~$2,500 neighborhood (2005) is priced at $33,000/month. "
      "What should you do FIRST?",
      ["Delete it right away because it is an outlier", "Investigate whether it is a typo or a real listing first",
       "Keep it and use it to set the new average price",
       "Log-transform the entire dataset before looking at the outlier"],
      "Investigate whether it is a typo or a real listing first",
      "Week 5: distinguish error-based outliers from valid extreme values. Lab 5 asks: 'Should those outlier values "
      "be removed? Or are they valid rental properties?'", context=RENT_CONTEXT, data="rent",
      src="df.sort_values('price', ascending=False).head(3)", source="Lab 5 Part 2"),
    Q("B13", B, "W4", "In the SF rentals data, baths and sqft are mostly empty. What's a reasonable takeaway from Lab 4's reflection?",
      ["Fill baths and sqft with 0 so every row can be used",
       "Consider dropping them or analyzing only listings with values",
       "Treat baths and sqft as the target variables to predict",
       "Ignore the blanks, since missing values rarely change a model's results"],
      "Consider dropping them or analyzing only listings with values",
      "Imputing a column that is ~80% missing mostly invents data. Lab 4 asks: 'Are those variables usable and useful?'",
      context=RENT_CONTEXT, data="rent", src="df.isnull().sum()", source="Lab 4 Reflection 4.2"),
    Q("B14", B, "W4", "Earworms case: a sample shows a 0.98 correlation between downloads and 'harmonic surprises'. "
      "What is the most careful conclusion?",
      ["Harmonic surprise clearly causes higher downloads, so add more of it",
       "Strong link worth investigating; correlation doesn't prove causation",
       "There is no real relationship, since the sample is too small to tell",
       "Higher downloads cause more harmonic surprises, since 0.98 is near 1"],
      "Strong link worth investigating; correlation doesn't prove causation",
      "Turning information into KNOWLEDGE requires critical thinking. Watch for spurious relationships (Week 1: statistical thinking).",
      source="Week 4 slides - Earworms case"),
    Q("B15", B, "W3", "FreshGro: 'Increase on-time deliveries from 82% to 95% within six months.' Why is this a good objective?",
      ["It is specific, measurable and time-bound", "It names the algorithm to be used",
       "It lists every variable in the dataset", "It avoids numbers so it stays flexible"],
      "It is specific, measurable and time-bound",
      "It's also tied to SLAs, customer satisfaction and revenue.", source="Week 3 reading - Case Study"),
    Q("B16", B, "W2", "Spotifool: which column should NOT be used as a predictor of downloads?",
      ["danceability", "song_id", "energy", "artist_popularity"],
      "song_id",
      "Same idea as customer_id in Megatelco: an ID is just a label and carries no information about the song.",
      context=SPOTIFOOL_CONTEXT, source="Practice Midterm dataset; Review page hint"),
    Q("B17", B, "W5", "Spotifool's loudness values are all negative (-30 to 0 dB). Are they errors?",
      ["Yes, delete them, because negatives are impossible",
       "No, loudness in dB can be naturally negative, so they are valid",
       "Yes, convert all of them to positive numbers using the absolute value",
       "Only the values below -20 dB are errors; the rest are valid"],
      "No, loudness in dB can be naturally negative, so they are valid",
      "The dataset description says 'Range: -30 to 0 dB. Lower values mean quieter tracks.' Not every negative "
      "number is an error. Compare that to a negative handset price.",
      context=SPOTIFOOL_CONTEXT, source="Practice Midterm dataset description"),
]


# ---------------------------------------------------------------------------
# SHORT ESSAYS (100 words or less) - checked against key points
# ---------------------------------------------------------------------------
ESSAYS = [
    {"id": "E1", "source": "Practice Midterm Q21",
     "prompt": "In 100 words or less, explain the role of Exploratory Data Analysis (EDA) in business analytics. "
               "Discuss: how EDA helps detect data quality issues; how it guides variable selection and "
               "transformation; how it can reveal unexpected patterns or relationships. Include at least one "
               "visualization or statistical technique and the insight it could provide.",
     "points": [("data quality issues (missing values, duplicates, outliers)", ["missing", "duplicate", "outlier", "quality", "error", "null"]),
                ("guides variable selection / transformation", ["select", "transform", "skew", "log", "variable", "feature", "encode"]),
                ("reveals patterns / relationships", ["pattern", "relationship", "correlat", "trend", "unexpected"]),
                ("names a specific technique", ["histogram", "boxplot", "box plot", "scatter", "heatmap", "describe", "iqr", "median", "correlation"]),
                ("states the insight that technique gives", ["shows", "reveal", "identify", "spot", "detect", "find"])],
     "model": "EDA is the step where analysts \"listen\" to the data before modeling it. Summary statistics "
              "and charts expose quality problems such as missing values, duplicates and outliers. For "
              "example, a boxplot of handset_price would show an impossible -$200 price. EDA also guides "
              "preparation: a right-skewed histogram of income suggests a log transform or median "
              "imputation, and a correlation heatmap shows which variables are related to the target or "
              "redundant with each other. Scatterplots can reveal unexpected relationships, like heavy "
              "data-overage users churning more, which leads to new hypotheses. EDA keeps models from "
              "being built on faulty data."},
    {"id": "E2", "source": "Week 3",
     "prompt": "In 100 words or less, explain the difference between a business objective and a data mining "
               "goal, using an example.",
     "points": [("defines business objective (business outcome)", ["business objective", "outcome", "business goal", "strategic"]),
                ("defines data mining goal (technical/analytic task)", ["data mining goal", "model", "predict", "technical", "analytic"]),
                ("explains how they connect", ["support", "translate", "bridge", "connect", "achieve"]),
                ("gives a concrete example", ["churn", "deliver", "%", "percent", "fraud", "sales"])],
     "model": "A business objective is the measurable outcome the organization wants, such as \"reduce "
              "customer churn by 10% in six months.\" A data mining goal is the analytic task that supports "
              "it, such as \"build a classification model that predicts each customer's probability of "
              "churning\" so marketing can target retention offers. In CRISP-DM, the data mining goal "
              "translates the business objective into work the analytics team can do. The model only "
              "succeeds if it helps achieve the business objective. FreshGro is an example: the objective "
              "was 95% on-time deliveries, and the data mining goal was to predict at-risk delivery runs."},
    {"id": "E3", "source": "Weeks 1 & 3",
     "prompt": "In 100 words or less, explain why CRISP-DM is described as iterative rather than linear. Give an example.",
     "points": [("says phases are revisited", ["revisit", "go back", "loop", "return", "iterat"]),
                ("new insights from data change direction", ["insight", "discover", "learn", "new information"]),
                ("living documents / updated charter or objectives", ["living", "update", "charter", "reframe", "revise"]),
                ("example", ["freshgro", "warehouse", "delivery", "example", "e.g"])],
     "model": "CRISP-DM is iterative because what you learn in later phases often changes earlier "
              "decisions. Exploring or modeling the data can show that the original assumptions were "
              "wrong, so the team goes back to Business Understanding to reframe the objective and update "
              "living documents like the project charter. At FreshGro, leadership assumed late deliveries "
              "came from traffic. Process mapping and data exploration showed the real bottleneck was the "
              "warehouse loading dock, so the team refocused the project and cut delays by 18%. Iteration "
              "is a sign of agility, not of poor planning."},
    {"id": "E4", "source": "Lab 6 / Week 6",
     "prompt": "In 100 words or less, describe how you would handle missing values in the Megatelco dataset, "
               "and why different columns need different strategies.",
     "points": [("median for numeric with outliers", ["median"]),
                ("0 when missing means none", [" 0", "zero", "none"]),
                ("mode or 'unknown' for categorical", ["mode", "unknown", "most common"]),
                ("drop rows when only a few / essential", ["drop", "remove", "few"]),
                ("check first / understand why missing", ["isnull", "why", "pattern", "random", "check"])],
     "model": "First, I would run df.isnull().sum() to count missing values in each column and think about "
              "why each one is missing. The right fix depends on the column. Numeric columns with outliers, "
              "like handset_price and average_call_duration, get the median, because it isn't distorted by "
              "extreme values. A missing data_leftover_mb probably means no leftover data, so I would fill "
              "it with 0. Categorical columns like considering_change_of_plan get the mode or an "
              "\"unknown\" placeholder. Only ten rows are missing income, so I would drop them. Every "
              "choice affects the analysis, so I would document it."},
    {"id": "E5", "source": "Weeks 5 & 6",
     "prompt": "In 100 words or less, explain how you decide whether an outlier should be removed, capped, or kept.",
     "points": [("detect (IQR / boxplot / describe)", ["iqr", "boxplot", "box plot", "describe", "quartile"]),
                ("error vs valid extreme value", ["error", "valid", "real", "legitimate", "typo", "impossible"]),
                ("business rules / domain experts", ["business", "domain", "expert", "rule"]),
                ("capping/winsorizing or transform as option", ["cap", "clip", "winsor", "log", "transform"])],
     "model": "First I would find outliers with describe(), a boxplot, or the IQR rule (below Q1 - 1.5×IQR "
              "or above Q3 + 1.5×IQR). Then I would decide whether each one is an error or a real but rare "
              "value. Business rules and domain experts help: a negative handset price is impossible, so I "
              "would remove or correct it. A real but extreme value, like a luxury rental, I would keep, "
              "and if it distorts the analysis I could cap it at the 1st/99th percentiles (winsorizing with "
              ".clip()) or apply a log transform. I would document every decision."},
    {"id": "E6", "source": "Weeks 6 & 7",
     "prompt": "In 100 words or less, explain what data leakage is, why it is dangerous, and how to avoid it.",
     "points": [("defines leakage (info not available at prediction time)", ["not available", "future", "prediction time", "wouldn't be known", "after"]),
                ("why dangerous (inflated performance)", ["inflat", "unrealistic", "too good", "overestimat", "cheat"]),
                ("example", ["february", "cancel", "example", "e.g"]),
                ("prevention (train/test split, only past info)", ["split", "test", "known at", "before", "timing"])],
     "model": "Data leakage happens when a model is trained on information that would not be available at "
              "the moment the prediction is made, such as future data or data derived from the target. "
              "This makes test performance look unrealistically good, and the model then fails in real "
              "use. For example, predicting January churn with February activity, or with a "
              "\"cancellation_reason\" field, leaks the answer. To avoid it, I would build features only "
              "from information known before the prediction point, split the data into training and test "
              "sets before transforming it, and be careful with target encoding."},
    {"id": "E7", "source": "Week 7 / Lab 7",
     "prompt": "In 100 words or less, compare one-hot encoding and ordinal encoding, with a Megatelco example of each.",
     "points": [("one-hot for nominal (no order)", ["nominal", "no order", "unordered"]),
                ("one-hot creates a 0/1 column per category", ["column", "binary", "0/1", "dummies", "get_dummies"]),
                ("ordinal for ordered categories", ["ordinal", "order", "rank"]),
                ("Megatelco examples", ["operating_system", "android", "satisfaction", "usage", "low", "high"])],
     "model": "Models need numbers, so categorical variables must be encoded. One-hot encoding is for nominal "
              "variables with no natural order. It creates a separate 0/1 column for each category, so "
              "operating_system becomes os_Android and os_IOS (pd.get_dummies), and the model doesn't "
              "assume one is \"bigger\" than the other. The downside is that it adds columns, which "
              "increases dimensionality. Ordinal encoding is for ordered categories. It maps each level to "
              "an integer that keeps the rank, so reported_satisfaction low/avg/high becomes 1/2/3. Using "
              "ordinal encoding on nominal data would invent a false order."},
    {"id": "E8", "source": "Week 4",
     "prompt": "In 100 words or less, explain the difference between data, information, and knowledge with a business example.",
     "points": [("data = raw facts without context", ["raw", "facts", "without context", "unprocessed"]),
                ("information = processed/organized with meaning", ["processed", "organized", "context", "summar", "meaning"]),
                ("knowledge = insight + experience -> action", ["insight", "experience", "action", "decision", "knowledge"]),
                ("example", ["sales", "customer", "gym", "score", "example"])],
     "model": "Data is raw facts without context, such as the numbers in a list of purchase amounts. "
              "Information is data that has been processed or organized so it has meaning, such as a report "
              "showing that average purchases rose 15% last quarter, mostly from customers over 50. "
              "Knowledge is the insight that comes from interpreting information with experience and "
              "critical thinking, and it leads to action: \"Customers over 50 in coastal cities buy more gym "
              "memberships in January, so we should target them with New Year promotions.\" Analytics turns "
              "data into information, and information into knowledge that supports decisions."},
    {"id": "E9", "source": "Weeks 4 & 6",
     "prompt": "In 100 words or less, explain why it matters to set correct data types (e.g., category, datetime, numeric) "
               "before analysis.",
     "points": [("wrong types break calculations/plots/models", ["calculat", "math", "error", "break", "plot", "model"]),
                ("category for limited fixed values", ["category", "limited", "fixed"]),
                ("dates as datetime reveals bad/missing dates", ["date", "datetime", "nat", "coerce"]),
                ("numbers stored as text", ["string", "text", "object", "stored as"])],
     "model": "Data types determine what pandas can do with a column. Numbers stored as text can't be "
              "averaged and won't show up in describe(). Columns with a limited, fixed set of values, like "
              "operating_system or leave, should be category so their intent is clear and they can be "
              "encoded correctly, and ordered categories like satisfaction keep their ranking. Converting "
              "dates with pd.to_datetime(errors='coerce') makes date math possible and exposes invalid "
              "dates as NaT. In the StreamFlow demo, 8 missing signup dates only appeared after conversion. "
              "Correct types prevent silent errors in charts, statistics and models."},
]

# ---------------------------------------------------------------------------
# FLASHCARDS - key terms from the readings
# ---------------------------------------------------------------------------
FLASHCARDS = [
    ("Business Analytics (BA)", "Using data, statistical methods and predictive modeling to drive business decisions. Goes beyond BI into predictive & prescriptive."),
    ("Business Intelligence (BI)", "Focuses on historical data and reporting: 'What happened?' (dashboards, spreadsheets)."),
    ("Descriptive analytics", "What happened? Summarizes historical data (reports, dashboards, KPIs)."),
    ("Diagnostic analytics", "Why did it happen? Root causes (Week 1 slides)."),
    ("Predictive analytics", "What will happen? Statistical models / ML forecast outcomes (churn, demand, fraud)."),
    ("Prescriptive analytics", "What should we do? Recommends actions using optimization, decision rules, simulation (dynamic airline pricing)."),
    ("CRISP-DM", "Cross-Industry Standard Process for Data Mining (1996, EU project; Daimler, SPSS, NCR). 6 iterative phases: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment."),
    ("Supervised learning", "Trains on LABELED data (features + known target) to predict outcomes. Classification or regression."),
    ("Unsupervised learning", "No target; finds hidden patterns/groups (clustering, PCA)."),
    ("Classification", "Predicts a CATEGORY (yes/no, fraud/not). Also gives a probability. Metrics: accuracy, precision, recall, F1."),
    ("Regression", "Predicts a NUMBER (sales, price). Metrics: MSE, RMSE, MAE, R-squared."),
    ("Structured vs unstructured data", "Structured = rows/columns, predefined fields. Unstructured = text, audio, images, video (needs NLP / computer vision)."),
    ("Training vs test data", "Training data teaches the model; test data is held out to evaluate it on unseen data."),
    ("Generalization", "A model's ability to perform well on new, unseen data."),
    ("Business objective", "The measurable business outcome (reduce churn 10% in 6 months)."),
    ("Data mining goal", "The technical task that supports the objective (predict churn probability)."),
    ("Business Understanding steps", "1 Determine business objectives, 2 Assess the situation, 3 Determine data mining goals, 4 Produce project plan/charter."),
    ("RACI", "Responsible (does the work), Accountable (owns the outcome), Consulted (gives input), Informed (kept updated)."),
    ("SMART goal", "Specific, Measurable, Achievable, Relevant, Time-bound."),
    ("SWOT", "Strengths, Weaknesses, Opportunities, Threats."),
    ("Project charter", "Formal summary: purpose, goals/KPIs, scope, stakeholders, plan, analytics approach, risks. A LIVING document."),
    ("Risk & Assumption Log", "Tracks uncertainties, limitations, assumptions (bad data, access issues, skills gaps)."),
    ("Business process map", "Visual of workflow steps, people/systems, decision points, and where data is generated/captured. Swimlane diagrams show who does each step."),
    ("4 Business Understanding pitfalls", "Vague goals, misaligned stakeholders, skipping to the data too fast, ignoring constraints. Common factor: communication."),
    ("Mendelow's matrix", "Power x Interest: Manage closely (high/high), Keep satisfied (high power/low interest), Keep informed (low power/high interest), Monitor (low/low)."),
    ("Tame vs wicked problem", "Tame: well-defined, data available, known solutions, measurable (good low-hanging fruit). Wicked: many stakeholders, no single solution, unintended consequences."),
    ("Data / Information / Knowledge", "Data = raw facts. Information = processed data with context. Knowledge = insight + experience leading to action."),
    ("Nominal", "Categories with NO order (product type, country). Binary is a subset."),
    ("Ordinal", "Categories WITH order but unequal gaps (education, satisfaction, star ratings)."),
    ("Discrete", "Countable whole numbers (number of purchases)."),
    ("Continuous", "Any value in a range, with decimals (revenue, weight)."),
    ("Cross-sectional / Time series / Panel", "Snapshot at one time / one thing over time / many subjects over time."),
    ("Population vs sample", "Population = entire group. Sample = subset used for analysis."),
    ("Sampling methods", "Random (equal chance), Stratified (sample within subgroups), Systematic (every nth), Convenience (easy to get; biased)."),
    ("3 Vs of Big Data", "Volume (how much), Velocity (how fast), Variety (structured, semi-structured JSON/XML, unstructured)."),
    ("Category dtype", "For values that are LIMITED in number and FIXED over time (gender, blood type, order status). df[c].astype('category')."),
    ("EDA", "Exploratory Data Analysis: summarize & visualize data to find patterns, anomalies, quality issues. Popularized by John Tukey (1977)."),
    ("Mean vs median", "Mean is sensitive to outliers/skew; median (middle value) is robust."),
    ("IQR & outliers", "IQR = Q3 - Q1. Outlier if < Q1 - 1.5*IQR or > Q3 + 1.5*IQR."),
    ("Skewness / kurtosis", "Skew: positive = long right tail. Kurtosis: how heavy the tails are (more outliers)."),
    ("Histogram / Boxplot / Scatterplot / Heatmap", "Distribution of 1 numeric / median+IQR+outliers / relationship of 2 numerics / correlation of many."),
    ("Confirmation bias", "Favoring evidence that supports what you already believe. Seek disconfirming evidence."),
    ("PII", "Personally Identifiable Information (name, email, phone, IP; even ZIP+birthdate+gender combined). Anonymize/pseudonymize."),
    ("GDPR / HIPAA / FERPA", "EU personal data / US health information / US student records."),
    ("Data preparation tasks", "Data cleaning, data validation, feature engineering. 60-80% of analyst time."),
    ("Listwise vs pairwise deletion", "Listwise drops any row with a missing value; pairwise uses all available data per calculation."),
    ("MCAR / MAR / MNAR", "Missing Completely At Random / Missing At Random / Missing Not At Random."),
    ("Missingness indicator", "A new 0/1 column flagging that a value was missing (missingness itself can be a signal)."),
    ("Range vs logic check", "Range: value within bounds (age 0-120). Logic: consistency between fields (signup before last login)."),
    ("Referential integrity", "Foreign keys in one table must match primary keys in another."),
    ("pandera", "Python library for schema-based validation (types, value ranges, regex) of DataFrames."),
    ("Data leakage", "Using info not available at prediction time (future data); inflates performance unrealistically."),
    ("Winsorizing", "Capping extremes at chosen percentiles (1st/99th) with .quantile() + .clip()."),
    ("Joins", "Inner = matches in both; Left = all of left; Right = all of right; Outer = everything (NaN for no match)."),
    ("Log transform", "Reduces right skew; only for strictly positive values (add a small number if zeros)."),
    ("Min-Max normalization", "(x - min) / (max - min) -> 0 to 1. Sensitive to outliers. Good for distance-based models (KNN, SVM, neural nets)."),
    ("Z-score standardization", "(x - mean) / std -> mean 0, std 1. Less affected by outliers."),
    ("pd.cut vs pd.qcut", "cut = equal-width (or custom) bins; qcut = equal-frequency (quantile) bins."),
    ("One-hot vs ordinal encoding", "One-hot (pd.get_dummies) for nominal: a 0/1 column per category. Ordinal: integers that keep rank, for ordered categories."),
    ("Binary / target encoding", "Binary: categories as binary digits (fewer columns than one-hot). Target: replace category with mean target (leakage risk)."),
    ("Curse of dimensionality", "Too many features -> sparse data, meaningless distances, overfitting, multicollinearity, cost, hard to interpret."),
    ("PCA", "Unsupervised dimensionality reduction into uncorrelated principal components; 1st explains most variance. Needs scaling; less interpretable."),
    ("Feature selection methods", "Filter (statistical tests), Wrapper (test subsets, e.g. RFE), Embedded (inside training, e.g. Lasso)."),
    ("Feature engineering", "Creating/improving features with domain knowledge to boost MODEL PERFORMANCE (ratios, flags, date parts, lags)."),
]


# ===========================================================================
#                                   ENGINE
# ===========================================================================
import ast
import base64
import contextlib
import io
import json
import os
import random
import re
import sys
import time
import warnings

warnings.filterwarnings("ignore")

LETTERS = "ABCDEFGH"

# ---------------------------------------------------------------------------
# Optional libraries: the quizzes work without them, the Code Lab needs pandas
# ---------------------------------------------------------------------------
try:
    import pandas as pd
    import numpy as np
    HAVE_PANDAS = True
except Exception:
    pd = np = None
    HAVE_PANDAS = False

plt = sns = None
if HAVE_PANDAS:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        try:  # warm up now so matplotlib builds its font cache before the sandbox blocks file writes
            _fig = plt.figure(figsize=(1, 1))
            _fig.text(0.5, 0.5, "x")
            _fig.savefig(io.BytesIO(), format="png")
            plt.close(_fig)
        except Exception:
            pass
    except Exception:
        plt = None
    try:
        import seaborn as sns
    except Exception:
        sns = None


def library_status():
    """[(name, installed?)] for the Code Lab's libraries."""
    out = [("pandas", HAVE_PANDAS), ("matplotlib", plt is not None), ("seaborn", sns is not None)]
    try:
        import sklearn  # noqa: F401
        out.append(("scikit-learn", True))
    except Exception:
        out.append(("scikit-learn", False))
    return out


INSTALL_HINT = "pip install pandas matplotlib seaborn scikit-learn"


def load_df(name):
    return pd.read_csv(io.StringIO(DATA[name]))


# ---------------------------------------------------------------------------
# The sandbox: student code runs with restricted builtins, an import allow-list,
# no file writes / network / subprocesses (audit hook), a time limit and a
# "course datasets only" read_csv
# ---------------------------------------------------------------------------
ALLOWED_IMPORTS = {"pandas", "numpy", "matplotlib", "seaborn", "sklearn", "scipy", "math", "statistics",
                   "random", "datetime", "re", "collections", "itertools", "functools", "warnings", "string"}
TIME_LIMIT = 8.0
SANDBOX = {"on": False}
_BLOCKED_EVENTS = ("os.remove", "os.rename", "os.rmdir", "os.mkdir", "os.chmod", "os.system", "os.exec",
                   "os.spawn", "os.posix_spawn", "os.startfile", "subprocess.", "socket.", "shutil.", "ctypes.",
                   "urllib.", "webbrowser.", "winreg.", "smtplib.", "ftplib.", "http.client")


class StopRun(BaseException):
    """Raised to stop a runaway program (BaseException so `except Exception` in student code can't hide it)."""


def _audit(event, args):
    if not SANDBOX["on"]:
        return
    if event == "open":
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else "r"
        if any(c in mode for c in "wax+"):
            raise PermissionError("writing files is disabled in this trainer")
    elif event.startswith(_BLOCKED_EVENTS):
        raise PermissionError(f"{event.split('.')[0]} is disabled in this trainer")


try:
    sys.addaudithook(_audit)
except Exception:
    pass

_REAL_IMPORT = __import__


def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".")[0]
    if level == 0 and root in ALLOWED_IMPORTS:
        return _REAL_IMPORT(name, globals, locals, fromlist, level)
    raise ImportError(f"'{root}' can't be imported here (allowed: pandas, numpy, matplotlib, seaborn, sklearn, math, ...)")


def _blocked(what):
    def blocked(*a, **k):
        raise PermissionError(f"{what}() is disabled in this trainer")
    return blocked


def sandbox_builtins():
    import builtins
    b = dict(vars(builtins))
    b["__import__"] = _safe_import
    for name in ("open", "exec", "eval", "compile", "breakpoint", "input", "help", "exit", "quit"):
        b[name] = _blocked(name)
    return b


class _PandasProxy:
    """Acts like pandas, but read_csv() only knows the course datasets (embedded samples, works offline)."""
    _map = {"megatelco": "megatelco", "rent": "rent", "spotif": "spotifool", "fintrust": "fintrust",
            "streamflow": "streamflow"}

    def __getattr__(self, name):
        return getattr(pd, name)

    def read_csv(self, path, *a, **k):
        p = str(path).lower()
        for frag, ds in self._map.items():
            if frag in p:
                return load_df(ds)
        raise FileNotFoundError("This trainer only has the course datasets offline: megatelco, rent, spotifool, "
                                "fintrust, streamflow. Use df (already loaded) or a lab URL.")

    def read_excel(self, *a, **k):
        raise PermissionError("reading other files is disabled in this trainer")


BASE_NAMES = {"pd", "np", "plt", "sns"}


def make_namespace():
    return {"__builtins__": sandbox_builtins(), "pd": _PandasProxy(), "np": np, "plt": plt, "sns": sns}


def fmt_value(v, max_rows=30):
    if HAVE_PANDAS and isinstance(v, (pd.DataFrame, pd.Series)):
        with pd.option_context("display.max_rows", max_rows, "display.max_columns", 12,
                               "display.width", 130, "display.max_colwidth", 24):
            return v.to_string() if len(v) <= max_rows else repr(v)
    return repr(v)


# ---------------------------------------------------------------------------
# Plain-English notes for the pandas pieces on each line
# ---------------------------------------------------------------------------
GLOSSARY = [
    (r"read_csv", "pd.read_csv(path) loads a comma-separated file (or URL) into a DataFrame."),
    (r"\.head\(", ".head(n) shows the first n rows (default 5). Nothing changes."),
    (r"\.info\(", ".info() lists columns, non-null counts and dtypes. Use it to spot missing data and wrong types."),
    (r"\.describe\(", ".describe() gives count/mean/std/min/quartiles/max for numeric columns."),
    (r"\.shape", ".shape is (rows, columns). It's an attribute, so there are no parentheses."),
    (r"\.dtypes?", ".dtypes shows the data type of every column."),
    (r"isnull\(\)|isna\(\)", ".isnull() is True where a value is missing. Add .sum() to count per column."),
    (r"\.sum\(", ".sum() adds values. On True/False it COUNTS the Trues."),
    (r"\.mean\(", ".mean() is the average. On True/False it gives the share that is True."),
    (r"\.median\(", ".median() is the middle value (robust to outliers)."),
    (r"fillna", ".fillna(value) replaces ONLY the missing cells with value."),
    (r"dropna\(subset", ".dropna(subset=[cols]) drops rows that are missing in THOSE columns."),
    (r"dropna\((?!subset)", ".dropna() drops rows missing ANY value (listwise deletion)."),
    (r"astype\('category'\)|astype\(\"category\"\)", ".astype('category') stores a column as a fixed set of categories."),
    (r"astype\(int\)", ".astype(int) converts to whole numbers (True/False become 1/0)."),
    (r"astype\('str'\)|astype\(str\)", ".astype('str') converts values to text."),
    (r"pd\.Categorical", "pd.Categorical(col, categories=[...], ordered=True) makes an ordered category. Values NOT in the list become NaN!"),
    (r"value_counts", ".value_counts() counts how many times each unique value appears."),
    (r"duplicated\(", ".duplicated() is True for rows that repeat an EARLIER row exactly."),
    (r"drop_duplicates", ".drop_duplicates() removes repeated rows (keeps the first by default)."),
    (r"df\[df\[|df\[\(|\w\[\(", "df[condition] keeps only the ROWS where the condition is True."),
    (r" & ", "&  means AND (both conditions). Wrap each condition in parentheses."),
    (r" \| ", "|  means OR (either condition)."),
    (r"\.loc\[", ".loc[rows, columns] selects or assigns by label. On the left of = it updates the original DataFrame."),
    (r"quantile", ".quantile(q) returns the value below which q of the data falls (0.25 = Q1, 0.75 = Q3)."),
    (r"\.clip\(", ".clip(lower, upper) caps values outside the range at the limits (winsorizing)."),
    (r"groupby", ".groupby(col) splits rows into groups so you can aggregate each one (mean, max, count)."),
    (r"sort_values", ".sort_values(col, ascending=...) sorts rows. A list of columns sorts by the first, then the next."),
    (r"\.corr\(", ".corr() is the correlation matrix (-1 to 1) between numeric columns."),
    (r"\.map\(", ".map({old: new}) replaces values using a dictionary. Values NOT in the dict become NaN!"),
    (r"\.apply\(", ".apply(func) runs a function on every value/row."),
    (r"pd\.qcut", "pd.qcut(col, q) makes equal-FREQUENCY bins (about the same count in each)."),
    (r"pd\.cut", "pd.cut(col, bins) makes equal-WIDTH (or custom) bins."),
    (r"get_dummies", "pd.get_dummies(df, columns=[...]) one-hot encodes: one 0/1 column per category; the original column is removed."),
    (r"MinMaxScaler", "MinMaxScaler rescales each column to 0-1: (x - min) / (max - min)."),
    (r"fit_transform", ".fit_transform() learns min/max (fit) and applies them (transform). Returns a NumPy array."),
    (r"\.str\.", ".str.* applies text methods (lower, strip, replace) to every value/name."),
    (r"\.columns", "df.columns holds the column NAMES."),
    (r"\.copy\(", ".copy() makes an independent copy so later changes don't affect the original."),
    (r"to_datetime", "pd.to_datetime(..., errors='coerce') parses dates; anything invalid becomes NaT (missing)."),
    (r"interpolate", ".interpolate() fills gaps by drawing a line between known neighboring values."),
    (r"add_categories", ".cat.add_categories('X') allows a new category value before you can use it (e.g. in fillna)."),
    (r"np\.log", "np.log / np.log1p compress large values (log1p = log(1 + x), safe for zeros)."),
    (r"np\.nan", "np.nan is the 'missing value' marker."),
    (r"\.skew\(", ".skew() > 0 means a long right tail; < 0 a long left tail."),
    (r"merge\(", "pd.merge(left, right, on=key, how=...) joins tables: inner/left/right/outer."),
    (r"plt\.hist", "plt.hist(col, bins=n) is a histogram: the distribution of one numeric variable."),
    (r"scatterplot|\.scatter\(", "A scatterplot shows the relationship between two numeric variables."),
    (r"barplot|kind='bar'", "A bar chart compares values or counts across categories."),
    (r"boxplot", "A boxplot shows median, IQR (box), whiskers and outliers (dots)."),
    (r"heatmap", "sns.heatmap shows a matrix as colors; annot=True writes the numbers in."),
    (r"plt\.show|plt\.title|xlabel|ylabel", "plt.title/xlabel/ylabel label the chart; plt.show() displays it."),
    (r"\.filter\(like", ".filter(like='x') selects the columns whose names contain 'x'."),
    (r"type\(", "type(x).__name__ shows what kind of object x is (Series vs DataFrame)."),
    (r"df\[\[", "df[[...]] (double brackets, a LIST of names) returns a DataFrame."),
    (r"\.between\(", ".between(a, b) is True when a <= value <= b (a range check)."),
    (r"\.cat\.categories", ".cat.categories lists the allowed categories (in order)."),
    (r"\.rename\(", ".rename(columns={old: new}) renames columns."),
    (r"\.round\(", ".round() rounds numbers."),
    (r"len\(", "len(df) is the number of rows."),
]


def notes_for(stmt):
    seen, out = set(), []
    for pat, note in GLOSSARY:
        if re.search(pat, stmt) and note not in seen:
            seen.add(note)
            out.append(note)
    return out[:4]


# ---------------------------------------------------------------------------
# Code Lab engine: run one top-level statement at a time and record what changed
# ---------------------------------------------------------------------------
def snapshot(ns):
    snap = {}
    for k, v in ns.items():
        if k.startswith("_") or k in BASE_NAMES:
            continue
        if isinstance(v, pd.DataFrame):
            snap[k] = ("df", v.copy())
        elif isinstance(v, pd.Series):
            snap[k] = ("series", v.copy())
        elif isinstance(v, (int, float, str, bool, tuple, list, dict, np.generic)):
            snap[k] = ("val", repr(v)[:90])
        elif isinstance(v, np.ndarray):
            snap[k] = ("val", f"NumPy array, shape {v.shape}")
        elif isinstance(v, type(os)):
            continue
        else:
            snap[k] = ("val", f"<{type(v).__name__}>")
    return snap


def _changed_cells(a, b):
    a, b = a.astype(object), b.astype(object)
    both_nan = a.isnull() & b.isnull()
    try:
        return ~((a == b) | both_nan)
    except Exception:
        return pd.Series(False, index=a.index)


def _v(x):
    """Short, friendly display of one cell value."""
    try:
        if x is None or (not isinstance(x, str) and pd.isna(x)):
            return "NaN"
    except Exception:
        pass
    if hasattr(x, "item"):
        try:
            x = x.item()
        except Exception:
            pass
    if isinstance(x, float):
        return f"{x:,.2f}".rstrip("0").rstrip(".") if abs(x) < 1e15 else repr(x)
    return repr(x)


def describe_frame_change(name, a, b):
    out = []
    if a.shape != b.shape:
        out.append(f"{name}: shape {a.shape} -> {b.shape}")
    gone = [i for i in a.index if i not in b.index]
    if gone and len(b) < len(a):
        out.append(f"   rows removed: {len(gone)}  (row labels {', '.join(map(str, gone[:8]))}{'...' if len(gone) > 8 else ''})")
    if len(a.columns) == len(b.columns) and list(a.columns) != list(b.columns):
        pairs = [(x, y) for x, y in zip(a.columns, b.columns) if x != y]
        out.append(f"{name}: {len(pairs)} column(s) RENAMED, e.g. " + ", ".join(f"{x!r} -> {y!r}" for x, y in pairs[:3]))
        return out
    added = [c for c in b.columns if c not in a.columns]
    removed = [c for c in a.columns if c not in b.columns]
    if added:
        out.append(f"   new columns: {', '.join(map(str, added))}")
    if removed:
        out.append(f"   removed columns: {', '.join(map(str, removed))}")
    common = [c for c in b.columns if c in a.columns]
    idx = [i for i in b.index if i in a.index]
    for c in common:
        da, db = a[c].dtype, b[c].dtype
        if str(da) != str(db):
            out.append(f"   {c}: dtype {da} -> {db}")
        na, nb = int(a[c].isnull().sum()), int(b[c].isnull().sum())
        if na != nb:
            out.append(f"   {c}: missing values {na} -> {nb}")
        if idx:
            try:
                ch = _changed_cells(a.loc[idx, c], b.loc[idx, c])
                n = int(ch.sum())
            except Exception:
                n = 0
            if n:
                ex = [f"row {i}: {_v(a.at[i, c])} -> {_v(b.at[i, c])}" for i in list(ch[ch].index[:3])]
                out.append(f"   {c}: {n} value(s) changed, e.g. " + "; ".join(ex))
    return out


def describe_series_change(name, a, b):
    out = []
    if len(a) != len(b):
        out.append(f"{name}: length {len(a)} -> {len(b)}")
    if str(a.dtype) != str(b.dtype):
        out.append(f"{name}: dtype {a.dtype} -> {b.dtype}")
    if len(a) == len(b) and a.index.equals(b.index):
        n = int(_changed_cells(a, b).sum())
        if n:
            out.append(f"{name}: {n} value(s) changed")
    return out


def diff_snapshots(before, after):
    out = []
    for k, (kind, v) in after.items():
        if k not in before:
            if kind == "df":
                out.append(f"{k} created: DataFrame {v.shape[0]} rows x {v.shape[1]} cols")
            elif kind == "series":
                out.append(f"{k} created: Series of {len(v)} values (dtype {v.dtype})")
            else:
                out.append(f"{k} = {v}")
            continue
        bk, bv = before[k]
        if kind == "df" and bk == "df":
            out += describe_frame_change(k, bv, v)
        elif kind == "series" and bk == "series":
            out += describe_series_change(k, bv, v)
        elif kind == "val" and bk == "val":
            if bv != v:
                out.append(f"{k}: {bv} -> {v}")
        elif kind != bk:
            out.append(f"{k} is now a {'DataFrame' if kind == 'df' else 'Series' if kind == 'series' else 'value'}")
    return out


def frame_info(df):
    """One row per column: (name, dtype, non-null, missing, unique)."""
    rows = []
    for c in df.columns:
        s = df[c]
        try:
            uniq = int(s.nunique(dropna=True))
        except Exception:
            uniq = -1
        rows.append((str(c), str(s.dtype), int(s.notnull().sum()), int(s.isnull().sum()), uniq))
    return rows


def render_figures(tag):
    """-> list of {'png': bytes, 'caption': str}. Pictures stay in memory (nothing is written to disk)."""
    if plt is None or not plt.get_fignums():
        return []
    out = []
    for num in plt.get_fignums():
        fig = plt.figure(num)
        bits = []
        for ax in fig.axes:
            if ax.get_title():
                bits.append(f"title '{ax.get_title()}'")
            if ax.get_xlabel():
                bits.append(f"x = {ax.get_xlabel()}")
            if ax.get_ylabel():
                bits.append(f"y = {ax.get_ylabel()}")
            if ax.patches:
                bits.append(f"{len(ax.patches)} bars/boxes")
            pts = sum(len(c.get_offsets()) for c in ax.collections if hasattr(c, "get_offsets"))
            if pts:
                bits.append(f"{pts} points")
        try:
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=80, bbox_inches="tight")
            out.append({"png": buf.getvalue(), "caption": "Chart: " + (", ".join(bits) if bits else "created")})
        except Exception:
            out.append({"png": None, "caption": "Chart: " + (", ".join(bits) if bits else "created")})
    plt.close("all")
    return out


_BIG_NUMBER = re.compile(r"(?<![\w.])\d{8,}(?![\w.])")


def _trace_factory(deadline):
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<lab>":
            return None
        if time.monotonic() > deadline[0]:
            raise StopRun(f"stopped after {TIME_LIMIT:g} seconds (infinite loop?)")
        return tracer
    return tracer


def preload_libraries(text):
    """Import heavy libraries OUTSIDE the sandbox (their own start-up code touches blocked things like ctypes)."""
    if "sklearn" in text:
        for mod in ("sklearn.preprocessing", "sklearn.decomposition", "sklearn.model_selection"):
            try:
                __import__(mod)
            except Exception:
                pass


def run_steps(src, data=None, setup=None, tag="lab"):
    """Execute code one top-level statement at a time. -> (steps, namespace, setup_error)"""
    preload_libraries(src + (setup or ""))
    ns = make_namespace()
    if data:
        ns["df"] = load_df(data)
    if _BIG_NUMBER.search(src):
        return [], ns, "Numbers with 8+ digits aren't allowed here (it protects your computer from huge allocations)."
    SANDBOX["on"] = True
    try:
        if setup:
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(setup, "<setup>", "exec"), ns)
            except Exception as e:
                return [], ns, f"setup failed: {type(e).__name__}: {e}"
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            return [], ns, f"SyntaxError: {e.msg} (line {e.lineno})"
        lines = src.split("\n")
        steps = []
        deadline = [0.0]
        tracer = _trace_factory(deadline)
        for n_i, node in enumerate(tree.body):
            stmt_src = "\n".join(lines[node.lineno - 1: node.end_lineno])
            before = snapshot(ns)
            buf = io.StringIO()
            result_obj, result_text, error = None, None, None
            deadline[0] = time.monotonic() + TIME_LIMIT
            old = sys.gettrace()
            try:
                with contextlib.redirect_stdout(buf):
                    sys.settrace(tracer)
                    try:
                        if isinstance(node, ast.Expr):
                            val = eval(compile(ast.Expression(node.value), "<lab>", "eval"), ns)
                            if val is not None and "Axes" not in type(val).__name__ and "plt." not in stmt_src:
                                result_obj, result_text = val, fmt_value(val)
                        else:
                            exec(compile(ast.Module([node], type_ignores=[]), "<lab>", "exec"), ns)
                    finally:
                        sys.settrace(old)
            except StopRun as e:
                error = str(e)
            except ModuleNotFoundError as e:
                error = f"{e} -- install it with: pip install {e.name}"
            except Exception as e:
                error = f"{type(e).__name__}: {e}"
            after = snapshot(ns)
            last = n_i == len(tree.body) - 1
            show_charts = ".show(" in stmt_src or last or bool(error)
            steps.append({
                "lines": (node.lineno, node.end_lineno), "src": stmt_src, "printed": buf.getvalue(),
                "result": result_text,
                "result_df": result_obj if (HAVE_PANDAS and isinstance(result_obj, (pd.DataFrame, pd.Series))) else None,
                "error": error, "changes": diff_snapshots(before, after),
                "charts": render_figures(f"{tag}_{len(steps) + 1}") if show_charts else [],
                "drawing": bool(plt is not None and plt.get_fignums()) and not show_charts,
                "notes": notes_for(stmt_src), "snap": after, "before": before})
            if error:
                break
    finally:
        SANDBOX["on"] = False
    return steps, ns, None


def focus_frame(step):
    """The DataFrame the Code Lab should show for a step: the one this step changed, else 'df', else any."""
    snap, before = step["snap"], step["before"]
    frames = [k for k, (kind, _) in snap.items() if kind == "df"]
    if not frames:
        return None
    for k in frames:  # one that changed
        if k not in before or before[k][0] != "df" or not (before[k][1].shape == snap[k][1].shape and
                                                           list(before[k][1].columns) == list(snap[k][1].columns) and
                                                           before[k][1].equals(snap[k][1])):
            return k
    return "df" if "df" in frames else frames[0]


def narrate_steps(steps):
    """The run as plain-English sentences."""
    out = []
    for i, s in enumerate(steps, 1):
        first = s["src"].strip().split("\n")[0]
        bits = []
        if s["changes"]:
            bits.append("; ".join(c.strip() for c in s["changes"][:3]))
        if s["printed"].strip():
            bits.append("prints " + repr(s["printed"].strip().split("\n")[0][:60]))
        if s["result"] is not None and not bits:
            bits.append("shows a result (nothing changes)")
        if s["charts"] or s["drawing"]:
            bits.append("draws a chart")
        if s["error"]:
            bits.append("ERROR: " + s["error"])
        if not bits:
            bits.append("only LOOKS at the data (nothing changes)")
        out.append(f"{i}.  {first}   ->   " + "  |  ".join(bits))
    return out


_quick_cache = {}


def quick_run(q):
    """Run a question's code and summarize. -> dict(text, frames=[DataFrame/Series], charts=[...], steps) or None"""
    if not (HAVE_PANDAS and q["code"]):
        return None
    if q["id"] in _quick_cache:
        return _quick_cache[q["id"]]
    steps, _, err = run_steps(q["code"], q["data"], q["setup"], tag=q["id"])
    parts, frames, charts = [], [], []
    if err:
        parts.append(err)
    for s in steps:
        if s["printed"].strip():
            parts.append(s["printed"].rstrip())
        if s["result"] is not None and s["result_df"] is None:
            parts.append(s["result"])
        if s["result_df"] is not None:
            frames.append(s["result_df"])
        charts += s["charts"]
        if s["error"]:
            parts.append("ERROR: " + s["error"])
    res = {"text": "\n".join(parts), "frames": frames[-2:], "charts": charts, "steps": steps}
    _quick_cache[q["id"]] = res
    return res


# ---------------------------------------------------------------------------
# Progress tracking (the one file this trainer writes: your accuracy per question)
# ---------------------------------------------------------------------------
PROGRESS_FILE = os.path.join(os.path.expanduser("~"), ".is4487_trainer_progress.json")


def load_progress():
    try:
        with open(PROGRESS_FILE) as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_progress(p):
    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(p, f)
        return True
    except Exception:
        return False


PROGRESS = load_progress()


def record(qid, correct):
    r = PROGRESS.setdefault(qid, {"right": 0, "tries": 0, "last": None})
    r["tries"] += 1
    r["right"] += int(correct)
    r["last"] = bool(correct)
    save_progress(PROGRESS)


def known_cards():
    return set(PROGRESS.get("_known_cards", []) if isinstance(PROGRESS.get("_known_cards"), list) else [])


def set_card_known(term, known):
    cards = known_cards()
    (cards.add if known else cards.discard)(term)
    PROGRESS["_known_cards"] = sorted(cards)
    save_progress(PROGRESS)


# ---------------------------------------------------------------------------
# Skills (for weak-spot drills) and flashcard matching
# ---------------------------------------------------------------------------
SKILLS = {
    "eda": "EDA, charts & statistics",
    "missing": "Missing values & duplicates",
    "outliers": "Outliers & validation",
    "types": "Data types & structures",
    "transform": "Encoding, scaling & joins",
    "models": "Analytics types & models",
    "business": "Business understanding",
    "ethics": "Ethics, bias & leakage",
    "pandas": "Reading pandas code",
}
SKILL_SHORT = {"eda": "EDA & charts", "missing": "Missing values", "outliers": "Outliers & validation",
               "types": "Data types", "transform": "Encode / scale / join", "models": "Analytics & models",
               "business": "Business understanding", "ethics": "Ethics & leakage", "pandas": "Reading pandas"}
_SKILL_PATTERNS = [
    ("eda", r"histogram|boxplot|box plot|scatter|heatmap|\beda\b|exploratory|describe\(|\.corr\(|correlat|skew|descriptive stat|mean vs|median|iqr"),
    ("missing", r"missing|fillna|dropna|isnull|duplicate|impute|imputation|listwise|nan\b"),
    ("outliers", r"outlier|winsor|clip\(|validation|range check|logic check|referential|iqr"),
    ("types", r"dtype|astype|category|nominal|ordinal|discrete|continuous|binary|categorical|numerical|data type|to_datetime|structured|sampling|population|knowledge|identifier"),
    ("transform", r"one-hot|get_dummies|encod|scal|normaliz|standardiz|z-score|qcut|pd\.cut|merge|join|log transform|pca|dimension|feature|preparation"),
    ("models", r"supervised|unsupervised|classification|regression|clustering|predictive|prescriptive|descriptive analytics|diagnostic|target variable|generaliz|predictor|machine learning|scikit"),
    ("business", r"objective|raci|smart|swot|charter|stakeholder|kpi|business understanding|crisp|mendelow|pitfall|tame|wicked|problem statement"),
    ("ethics", r"bias|ethic|leakage|gdpr|hipaa|ferpa|privacy|confirmation|fairness|pii"),
]


def skills_of(q):
    text = " ".join([q["prompt"], " ".join(q["choices"]), q["why"], q["source"], q["code"] or ""]).lower()
    found = [k for k, pat in _SKILL_PATTERNS if re.search(pat, text)]
    if q["code"] and "pandas" not in found:
        found.append("pandas")
    return found[:4]


for _q in BANK:
    _q["skills"] = skills_of(_q)


# ---------------------------------------------------------------------------
# Who wrote each question. Only the Canvas practice exam (PM1-PM22, Q21 is the essay E1) and the
# review-page samples (RP1-RP5) are your professor's. Everything else was written by Claude.
# ---------------------------------------------------------------------------
PROF_GROUPS = ("Practice Midterm", "Review Page")
PROF_ESSAYS = ("E1",)
CODE_ADDED_BY_CLAUDE = ("PM3", "PM7", "PM8", "RP2", "RP4", "RP5")


def origin_of(item):
    """'prof' = your professor's question, 'claude' = written by Claude. Works for questions and essay items."""
    if item.get("kind") == "essay":
        return "prof" if item["id"] in PROF_ESSAYS else "claude"
    return "prof" if item["group"] in PROF_GROUPS else "claude"


def origin_chip(item):
    return "PROFESSOR'S QUESTION" if origin_of(item) == "prof" else "PRACTICE QUESTION (by Claude)"


def origin_note(item):
    if origin_of(item) == "claude":
        return ("Written by Claude to practice the same ideas in the style of your professor's questions. "
                "It is not an actual exam question.")
    if item.get("kind") == "essay":
        return "From your professor's Canvas practice exam (Q21)."
    if item["group"] == "Review Page":
        note = "From your professor's review page. The wording follows his closely."
    else:
        note = ("From your professor's Canvas practice exam. Canvas never showed the answer key, so the answer was "
                "worked out from the readings. Some choices may be shortened from the Canvas wording.")
    if item["id"] in CODE_ADDED_BY_CLAUDE:
        note += " The code shown was added by Claude so the Code Lab can run it."
    return note


PROF_QUESTIONS = [_q for _q in BANK if origin_of(_q) == "prof"]

_FLASH_EXTRA = {"RACI": ["raci"], "SMART goal": ["smart"], "SWOT": ["swot"], "PCA": ["pca", "principal component"],
                "EDA": ["eda", "exploratory data analysis"], "IQR & outliers": ["iqr", "outlier"],
                "CRISP-DM": ["crisp"], "PII": ["pii"], "Winsorizing": ["winsor", "clip("],
                "Data leakage": ["leakage"], "Joins": ["join", "merge("],
                "One-hot vs ordinal encoding": ["one-hot", "get_dummies", "ordinal encoding"],
                "pd.cut vs pd.qcut": ["qcut", "pd.cut"], "Category dtype": ["category"],
                "Mendelow's matrix": ["mendelow", "stakeholder matrix"],
                "Tame vs wicked problem": ["tame", "wicked"]}


_FLASH_EXTRA["Population vs sample"] = ["population"]
_FLASH_EXTRA.update({"Z-score standardization": ["z-score", "z score"], "Min-Max normalization": ["min-max", "minmax"],
                     "Log transform": ["log transform", "log1p", "np.log"], "Listwise vs pairwise deletion": ["listwise"],
                     "Missingness indicator": ["missingness"], "Curse of dimensionality": ["dimensionality"],
                     "Training vs test data": ["test data", "training data", "train/test"],
                     "Feature engineering": ["feature engineering"], "Confirmation bias": ["confirmation bias"],
                     "Referential integrity": ["referential"], "Range vs logic check": ["range check", "logic check"],
                     "Business process map": ["process mapping", "process map"],
                     "Risk & Assumption Log": ["assumption log"], "Project charter": ["charter"]})
_GENERIC_WORDS = {"data", "information", "sample", "population"}  # too common to prove a card is relevant


def _flash_keys(term):
    base = [k.strip().lower() for k in re.split(r" / | vs |\(|\)|&", term)
            if len(k.strip()) >= 4 and k.strip().lower() not in _GENERIC_WORDS]
    return base, _FLASH_EXTRA.get(term, [])


FLASH_KEYS = {t: _flash_keys(t) for t, _ in FLASHCARDS}


def related_flashcards(q, limit=3):
    """Flashcards worth reviewing for this question. A card with several key words needs 2 of them to show up."""
    text = " ".join([q["prompt"], " ".join(q["answer"]), q["why"], q["code"] or ""]).lower()
    scored = []
    for term, defn in FLASHCARDS:
        base, extra = FLASH_KEYS[term]
        hits = [k for k in base if k in text]
        hits_extra = [k for k in extra if k in text]
        need = 2 if len(base) >= 2 else 1
        if len(hits) >= need or hits_extra:
            scored.append((sum(len(h) for h in hits + hits_extra), term, defn))
    scored.sort(reverse=True)
    return [(t, d) for _, t, d in scored[:limit]]


# ---------------------------------------------------------------------------
# Why-your-answer-is-wrong notes (hand-written for the questions people trip on)
# ---------------------------------------------------------------------------
TRAPS = {
    "PM3": {"Box Plot": "A box plot shows median, spread and outliers, but it hides the SHAPE (peaks, skew). 'Distribution' means shape, which is what a histogram shows.",
            "Scatter Plot": "A scatter plot needs TWO numeric variables. Downloads alone is one variable.",
            "Line Chart": "Line charts show change over time (a trend), not how values are spread out."},
    "PM8": {"Histogram": "A histogram shows ONE variable's distribution. The question asks about the relationship between TWO variables.",
            "Bar Chart": "Bar charts compare categories. Energy and danceability are both numeric measurements.",
            "Pie Chart": "Pie charts show parts of a whole for categories, never a relationship between two numeric variables."},
    "PM9": {"Record Labels, because they control the content but are not directly interested in feature updates.": "The music IS the product, so labels have high power AND high interest: manage closely, not keep satisfied.",
            "Premium Subscribers, because they demand better features.": "Premium subscribers have high interest (they use the features) but lower power than regulators or labels: keep informed / manage closely.",
            "Freemium Users, because they use the service the most.": "Using the service a lot means HIGH interest, and individual free users have LOW power: keep informed."},
    "PM12": {"Predictive Analytics": "Predictive would FORECAST next winter's flu or ER spikes. This hospital is summarizing five years of history, which is descriptive.",
             "Prescriptive Analytics": "Prescriptive recommends what to DO (for example, how to staff). The scenario only identifies past patterns."},
    "PM13": {"Age - Numerical, Credit Score - Categorical, Approval - Categorical, ZIP - Numerical": "Credit score (300-850) is a measured number, so it is numerical. A true/false ZIP flag is not numerical either.",
             "Age - Categorical, Credit Score - Categorical, Approval - Numerical, ZIP - Numerical": "Age is a measured quantity (numerical) and Approved/Denied is a label (categorical), so almost everything here is flipped.",
             "Age - Categorical, Credit Score - Numerical, Approval - Numerical, ZIP - Categorical": "Age is numerical (you can subtract ages meaningfully) and Approved/Denied is categorical."},
    "PM14": {"Income Level - Target Variable, Categorical": "Income level is an input (feature). The company is trying to predict the Rental Decision.",
             "Previous Rentals - Target Variable, Numerical": "Previous rentals is a predictor. The thing being predicted is 'will the customer rent?' (Yes/No).",
             "Customer Age - Target Variable, Numerical": "Age is a predictor. The target is the outcome the company wants to predict: the Rental Decision."},
    "PM15": {"Assess the situation, analyzing internal and external constraints, available data, and stakeholder concerns.": "That is step 2. The challenges are bait, but the question asks for the FIRST step: determine business objectives.",
             "Determine analytical goals, such as reducing false positives in fraud detection models.": "Analytical (data mining) goals are step 3. They only make sense after the business objective is clear.",
             "Produce the project plan, ensuring timelines align with compliance and risk management expectations.": "The project plan is the LAST step (step 4)."},
    "PM16": {"Project B - Climate Change Policy, because long-term sustainability is more important than short-term gains.": "Climate policy is a WICKED problem (many stakeholders, no single solution, slow results). Low-hanging fruit means a quick, well-defined win.",
             "Both projects should be prioritized equally, to balance short-term and long-term goals.": "The question asks which is low-hanging fruit. Only the tame, structured problem (traffic) is."},
    "PM17": {"Chatbot Deflection Rate - inquiries resolved without a human.": "This one is relevant, but so are the others: the goal has a cost half AND a satisfaction half. The best answer covers all of it.",
             "Customer Satisfaction Score (CSAT) - satisfaction after chatbot interactions.": "CSAT covers the 'keep satisfaction high' half. Deflection rate and handling time cover the cost half, so 'All of the above' is more complete."},
    "PM22": {'In a new dataframe called "df_new", include one column for product_price containing values less than 5000': "df[condition] keeps ROWS (with all columns), not a single column. And the condition is <= 5000, not < 5000.",
             'In the "df" dataframe, delete the price if less than 5000': "The original df is untouched: the result is assigned to a NEW dataframe, df_new. Also nothing is deleted from df."},
    "RP1": {"operating_system": "Android vs IOS could plausibly relate to churn (different handsets and plans).",
            "handset_price": "Handset price describes the customer's phone and could relate to loyalty.",
            "data_overage_mb": "Going over the data allowance is a classic reason customers leave.",
            "reported usage level": "How heavily someone uses the service is a natural churn predictor."},
    "RP3": {"Modeling": "Modeling is phase 4 of CRISP-DM.", "Deployment": "Deployment is phase 6 of CRISP-DM.",
            "Data Understanding": "Data Understanding is phase 2.", "Business Understanding": "Business Understanding is phase 1."},
    "RP4": {"df['product'] == str(df['product'])": "== COMPARES; it never changes the column.",
            "df['product'] == str(df.product)": "== COMPARES; it never changes the column.",
            "df['product'] = to_str(df['product'])": "There is no function called to_str in pandas.",
            "df['product'] = df['product'].string_convert": "There is no .string_convert in pandas. The method is .astype()."},
    "W1-6": {"Predictive": "Predictive would FORECAST demand. Reviewing past sales numbers is describing what happened.",
             "Prescriptive": "Prescriptive recommends actions. Walmart's pre-positioning of trucks came after the prediction."},
    "W3-1": {"Reduce customer churn by 10% within the next six months": "That is a business objective: a measurable business OUTCOME.",
             "Increase on-time deliveries from 82% to 95% by June": "That is a business objective (an outcome with a target).",
             "Preserve $1M in annual revenue by the end of the year": "Dollars preserved is a business outcome, not a technical modeling task."},
    "W4-2": {"Nominal": "Nominal categories have NO order, but 1-star to 5-star clearly does.",
             "Discrete numeric": "Discrete numbers are COUNTS (3 visitors). A star rating is an ordered category whose gaps aren't measurable.",
             "Continuous numeric": "Star ratings are whole levels, and the gaps between levels aren't measurable."},
    "W4-3": {"Continuous": "You can't have 2.5 visitors; counts are whole numbers (discrete).",
             "Ordinal": "Ordinal is for ordered CATEGORIES (low/medium/high). A visitor count is a real number you can count."},
    "W5-2": {"Mean": "The mean is dragged toward extreme values like billionaires.",
             "Standard deviation": "That measures spread, not central tendency, and it is very sensitive to outliers.",
             "Range": "Range is just max - min: it is entirely determined by the extremes."},
    "W5-3": {"40": "40 is Q3 itself. The fence is Q3 + 1.5 x IQR.",
             "50": "50 would be Q3 + 0.5 x IQR. Multiply the IQR (20) by 1.5 first: 30.",
             "60": "60 is Q3 + 1 x IQR (40 + 20). The rule uses 1.5 x IQR, which is 30."},
    "W6-3": {"The mean": "Outliers drag the mean around, so it would fill in a distorted value. The median ignores them.",
             "The maximum": "Filling with the largest value would invent extreme data.",
             "Always drop the column": "Dropping a whole column throws away every other value in it."},
    "W6-4": {"the median of the column": "Median is the right choice when missing means 'unknown'. Here a blank leftover means the customer had NO leftover data, so 0 is the real value.",
             "the mean of the column": "The mean would invent leftover data that never existed.",
             "the string 'unknown' as a label": "That would turn a numeric column into text and break every calculation."},
    "W6-7": {"range check": "A range check tests ONE value against bounds (age 0-120). This rule compares TWO fields with each other.",
             "uniqueness constraint": "Uniqueness is about duplicate IDs, not about comparing two columns.",
             "referential integrity check": "Referential integrity is about foreign keys matching another table."},
    "W6-8": {"Range check validation": "A range check tests one value against bounds, not matching IDs across tables.",
             "Data type enforcement": "Types are fine here: the problem is that the IDs don't exist in the other table."},
    "W7-1": {"SP01, SP02, SP03, SP04, SP05": "That is the OUTER join (everything from both).", "SP01, SP02, SP03, SP04": "That is the LEFT join (all of A).",
             "SP02, SP03, SP04, SP05": "That is the RIGHT join (all of B)."},
    "W7-3": {"It changes the order of the values": "Min-Max keeps the order; it only rescales to 0-1.",
             "It creates many extra columns": "Min-Max rescales existing columns. One-hot encoding creates many columns."},
    "W7-4": {"0.15": "That would be (130 - 100) / 200: the divisor is the standard deviation (20), not 200.",
             "1.57": "The reading prints 1.57, but that is a typo: (130 - 100) / 20 is exactly 1.5.",
             "30": "30 is the raw difference. Divide it by the standard deviation (20) to get the z-score."},
    "W7-5": {"cut makes equal-frequency bins; qcut makes equal-width bins": "Reversed: the Q in qcut stands for QUANTILE, which makes equal-FREQUENCY groups.",
             "they make identical bins; only the function names differ": "They differ: cut slices the value range into equal widths, qcut slices the data into equal-sized groups."},
    "W7-6": {"Ordinal encoding (Android=1, IOS=2)": "That invents an order (IOS 'greater than' Android). Operating system is nominal, so use one-hot.",
             "Log transform (to reduce the skew)": "A log transform is for skewed numeric data, not for categories.",
             "Min-Max scaling (rescale to 0-1)": "Scaling is for numeric columns, not categories."},
    "W7-10": {"It is supervised and uses the target variable to choose components": "PCA is UNSUPERVISED: it never looks at the target.",
              "It makes the original features easier to interpret for stakeholders": "The opposite: principal components are blends of the original columns, which are harder to explain.",
              "It works equally well on unscaled data with different units": "PCA is sensitive to scale, so standardize first."},
    "K2": {"Shows summary statistics such as the mean, median and quartiles": "That is .describe(). .info() shows structure: rows, columns, non-null counts, dtypes.",
           "Shows the first five rows of the DataFrame as a table": "That is .head()."},
    "K3": {"Every column, including the text columns": "By default describe() only covers numeric (and date) columns. Use value_counts() for text.",
           "Only the text (object) columns": "It is the reverse: numeric columns are the default."},
    "K4": {"40": "That is just the row count. df.shape is a TUPLE of (rows, columns).", "16": "That is just the column count. shape gives both.",
           "(16, 40)": "The order is (rows, columns): 40 rows and 16 columns."},
    "K7": {"To convert operating_system into numeric codes": "A category dtype still shows the text labels. Converting to numbers is encoding (get_dummies / ordinal).",
           "To delete operating_system from the DataFrame": "astype changes the type; the column stays."},
    "K8": {"Nothing; the two approaches give the same result": "ordered=True matters: it lets you compare levels (low < avg < high), which plain category can't.",
           "It removes rows whose satisfaction is 'avg'": "pd.Categorical never removes rows. Values not in the list would become NaN."},
    "K9": {"Works fine and the satisfaction levels are ordered Low < Medium < High": "The categories list has 'Low', 'Medium', 'High' (capitalized), but the data has lowercase 'low', 'avg', 'high'. Nothing matches, so everything becomes NaN.",
           "Python raises an error because the labels don't match the categories": "pd.Categorical does NOT raise an error for values outside the list: it silently turns them into NaN.",
           "Only 'avg' becomes NaN because it isn't in the categories list": "'low' != 'Low' either (matching is case-sensitive), so EVERY value becomes NaN."},
    "K10": {"leave becomes 1 for LEAVE customers and 0 for STAY customers": "The dictionary keys are 'yes'/'no', but the data holds 'LEAVE'/'STAY', so nothing matches. The working map is {'LEAVE': 1, 'STAY': 0}.",
            "Python raises a KeyError because 'LEAVE' is not a key": "Series.map() never errors on unmatched values; it just returns NaN.",
            "Nothing changes because map() leaves unmatched values as they are": "Everything IS replaced: with NaN."},
    "K11": {"Deletes the rows in which handset_price is missing": "fillna() fills; dropna() deletes.",
            "Replaces every handset_price value with the median": "fillna() only touches the MISSING cells.",
            "Calculates the median handset_price and prints it": "The result is assigned back into the column, so nothing is printed."},
    "K12": {"Drops every row that has any missing value in any column": "That would be df.dropna() with no subset. subset=['income'] limits the check to income only.",
            "Fills the missing income values with zero instead of dropping": "dropna removes rows; it never fills."},
    "K13": {"Number of duplicate rows: 0": "Customer 13678 appears twice, so there is a duplicate.",
            "Number of duplicate rows: 2": "duplicated() marks only the SECOND copy of a repeated row (the first copy is not flagged), so the count is 1.",
            "Number of duplicate rows: 40": "40 is the number of rows, not the number of duplicates."},
    "K14": {"39": "That only counts the -200 price. The two MISSING prices also fail the test, because NaN >= 0 is False.",
            "38": "NaN >= 0 is False, so BOTH missing prices are dropped as well as the -200: 40 - 3 = 37.",
            "40": "The filter does remove rows: negative and missing prices fail the test."},
    "K15": {"Deletes the rows in the top and bottom 1% of income": "clip() doesn't remove any rows. It pulls extreme values back to the cutoffs.",
            "Rescales income to a 0-1 range using min and max": "Normalizing would use (x - min) / (max - min). This only caps the extremes.",
            "Fills the missing income values with the 99th percentile": "Nothing here handles missing values; that is fillna()/dropna()."},
    "K16": {"Only the rows whose text_message_count is above the upper fence": "The filter keeps values INSIDE the fences, so the outliers are what gets dropped.",
            "Only the rows above the median text_message_count": "The median is never used here: the cutoffs come from Q1, Q3 and the IQR.",
            "All of the rows, because the filter only adds columns": "Rows outside the fences are removed (the 5000-text customer is one)."},
    "K17": {"The 10 cheapest listings in the entire rental dataset": "groupby makes ONE row per neighborhood (an average), and it sorts highest first.",
            "The number of listings in each of the top 10 neighborhoods": "That would be .size() or value_counts(). This takes the MEAN price.",
            "The 10 most expensive individual listings in the dataset": "groupby combines listings into neighborhood averages; it doesn't list individual listings."},
    "K18": {"A single correlation number for the whole table": "With several columns, corr() returns a matrix with a coefficient for every pair.",
            "The covariance matrix of the four selected columns": "corr() is correlation (scaled -1 to 1), not covariance.",
            "A scatterplot matrix of the four selected columns": "corr() returns numbers. Charts come from plt/sns."},
    "K19": {"A bar chart of price, where bins=30 sets the number of bars": "plt.hist makes a histogram: bins group values into ranges.",
            "A boxplot of price, where bins=30 sets the number of whiskers": "A boxplot would use plt.boxplot / sns.boxplot.",
            "A scatterplot of price, where bins=30 sets the number of points": "A scatterplot needs two variables."},
    "K20": {"A True/False column that flags the customers who sent over 500 texts": ".astype(int) converts True/False into 1/0, so the new column holds 0 and 1.",
            "A column that holds the number of texts above 500": "It is a flag (1 or 0), not a count.",
            "A column that replaces text_message_count with 1 and 0": "A NEW column called high_texter is created; the original stays."},
    "K22": {"Splits income into 3 ranges of equal width (same dollar span), labeled Low/Medium/High": "That is pd.cut. qcut uses QUANTILES so the groups have about the same number of rows.",
            "Sorts the incomes and labels the top third High, dropping the rest": "qcut labels rows; it never removes any.",
            "Creates 3 new columns, one for each of Low, Medium and High": "It creates ONE new column with 3 labels."},
    "K23": {"It isn't; both functions split the data into equal-sized groups": "They differ: cut slices the VALUE range into equal widths; qcut makes equal-sized groups.",
            "pd.cut only sorts the rows; it does not create groups": "cut never sorts; it assigns each value to a bin.",
            "pd.cut only works on text columns, not numeric ones": "cut works on numbers (it is how you bin a numeric column)."},
    "K24": {"Nothing changes, because get_dummies only reports the categories": "get_dummies replaces the column: the shape goes from (40, 16) to (40, 17).",
            "operating_system is recoded as the numbers 1 (Android) and 2 (IOS)": "That would be ordinal encoding. One-hot makes one 0/1 column per category.",
            "A new True/False column is added for each customer in the data": "One column per CATEGORY (Android, IOS), not per customer."},
    "K25": {"-1 to 1": "That is the range of a correlation, not MinMaxScaler.", "mean 0, std 1": "That is StandardScaler (z-score).",
            "the same as income": "Scaling changes the values to fit 0-1."},
    "K26": {"No difference; both lines return the same type of object, namely a DataFrame": "Single brackets with one name give a Series; a list of names inside double brackets gives a DataFrame.",
            "The first returns a DataFrame and the second returns a list": "It is the reverse of that: Series first, DataFrame second.",
            "The second line causes an error because of the double brackets": "df[['price', 'beds']] is the standard way to pick several columns."},
    "K27": {"Sorts by price only, and ignores the beds column": "A list sorts by the first column, then by the next to break ties.",
            "Sorts by price first, then by beds within each price": "The first name in the list (beds) is the primary sort.",
            "Sorts by beds and price, both in descending order": "Ascending is the default. You need ascending=False for descending."},
    "K29": {"Deletes every customer whose age is under 18 or over 120 from the whole dataset": "No rows are deleted: the bad ages are set to NaN and then filled.",
            "Clips ages under 18 up to 18 and ages over 120 down to 120": "They become NaN first, then take the MEDIAN.",
            "Calculates the average age of the customers who are 18 to 120": "describe() reports the mean, but the block's purpose is to fix impossible ages."},
    "K30": {"Raises an error when a date is invalid": "errors='raise' would do that. 'coerce' converts failures to NaT instead.",
            "Deletes the rows that contain bad dates": "Rows stay: only the date value becomes NaT.",
            "Guesses the closest valid date for each bad value": "It cannot guess; the bad value just becomes missing (NaT)."},
    "K31": {"Because the mode is impossible to compute for text categories": "The mode can be computed, but with an even split it would be arbitrary.",
            "Because rows with a missing gender should be deleted instead": "The code keeps every row by adding an 'Unknown' category.",
            "Because fillna cannot be used on category columns at all": "Category columns CAN have NaN. 'Unknown' is a choice that avoids guessing."},
    "K32": {"Loans that are Defaulted OR have ApplicantIncome over 5000": "& means AND (both conditions). | would be OR.",
            "Every loan, with only the three listed columns shown": "Both conditions must be True for a row to be kept.",
            "An error, because two filters cannot be combined this way": "Combining conditions with & is the standard approach (each in parentheses)."},
    "K33": {"The average loan amount of Defaulted loans in each EmploymentStatus group": "The mean here is of a True/False column (LoanStatus == 'Defaulted'), which gives the default RATE.",
            "The count of Defaulted loans in each EmploymentStatus group": "mean() isn't a count; it is the share of Trues.",
            "A bar chart of default counts for each EmploymentStatus group": "No plotting function is called, so this returns numbers."},
    "K34": {"Removes the skew by dropping the largest values": "No values are dropped: every row stays, and a NEW column log_downloads is added.", "Rescales the column so that its values run from 0 to 1": "log1p does not rescale to 0-1. That is what MinMaxScaler does.",
            "Sorts the column from smallest to largest": "np.log1p transforms values; it doesn't reorder them."},
    "K35": {"Inner join: only the customers found in both tables": "how='inner' would drop C4. how='left' keeps all customers.",
            "Outer join: every row from both tables is kept, with NaN gaps": "An outer join would also keep C5 (a plan with no customer).",
            "Right join: every row of plans is kept": "how='left' keeps every row of the LEFT table (customers)."},
    "K36": {"It makes the assignment run faster on large data": "The point is correctness: .loc updates the original frame and avoids SettingWithCopyWarning.",
            "To select only the first column and ignore the rest": ".loc[:, 'col'] selects ALL rows of one column.",
            "It converts the column to the category type": ".loc is selection/assignment; it doesn't convert types."},
    "K37": {"A pie chart of the 10 largest neighborhoods": "sns.barplot draws bars.", "A histogram of price for the top 10 listings": "The bars show listing counts per neighborhood, not price ranges.",
            "A scatterplot of nhood against price for 10 listings": "It is a bar chart of listing counts per neighborhood."},
    "PM7": {"df.groupby()": "groupby splits rows into groups so you can aggregate them. It doesn't check for missing values.",
            "df.corr()": "corr() computes correlations between numeric columns. It says nothing directly about missing cells.",
            "df.describe()": "describe() summarizes numeric columns (mean, std, quartiles...). Its count row hints at gaps, but isnull().sum() is the direct check."},
    "RP2": {"house (home price)": "A price is a measurement with many different values, not a small FIXED set of options.",
            "handset_price": "A price is a measurement with many different values, not a small FIXED set of options.",
            "customer_id": "An ID is unique for every customer, so it isn't a limited set of values.",
            "data_overage_mb": "Megabytes used is a measurement, not a limited set of categories."},
    "RP5": {"Identify the data type of product": "Identifying a type is .dtype or .info(). This line CHANGES the type (it assigns back with =).",
            "Determine if there is data in the product variable": "That would be .isnull() / .info(). This line converts the column.",
            "Convert the product variable to a category datatype": "Category would be astype('category'). astype('str') converts to string (text).",
            "Determine if all the data are of the same datatype": "Nothing here tests the types: it converts them."},
    "K1": {"Installs the pandas library from the web address": "Libraries come from pip install and import. read_csv loads DATA.",
           "Uploads the DataFrame df to the GitHub repository": "read_csv READS data in. Saving out would be df.to_csv().",
           "Opens the file in Excel and shows the first five rows": "read_csv loads the file into Python memory as a DataFrame. No other program opens."},
    "K5": {"Removes all spaces from the values inside each column": "df.columns holds only the column NAMES. The data values aren't touched.",
           "Converts every column in the DataFrame to string type": "The .str methods here clean the NAMES. No column's data type changes.",
           "Sorts the columns alphabetically by their new names": "Nothing is reordered: the names are cleaned in place."},
    "K6": {"The count of non-missing values in the column": "That is .count() (or .notnull().sum()). value_counts() tallies EACH distinct value.",
           "The sum of all the values in the column": "That is .sum().", "The number of columns in the DataFrame": "That is len(df.columns) or df.shape[1]."},
    "K21": {"To round the ratio to the nearest whole number": "Rounding would use .round(). The + 1 only guards the denominator.",
            "To convert the ratio to a percentage value": "A percent would multiply by 100.",
            "It is a typo and does not change the result": "It is deliberate: a ratio whose denominator can be 0 would give inf (or an error)."},
    "K28": {"To make the dataset twice as large for training": "copy() makes a second, independent object: a backup, not a doubled dataset.",
            "To convert every column to its correct data type": "copy() never changes types.", "To remove duplicate rows from the DataFrame": "copy() just duplicates the object. drop_duplicates() removes repeated rows."},
    "B5": {"A pie chart showing the share of income by LoanStatus": "Pie charts show parts of a whole for categories. They can't compare a numeric variable's spread across groups.",
           "A histogram of Loan_ID split by LoanStatus": "Loan_ID is just an identifier, and a histogram shows one variable's distribution.",
           "A line chart of ApplicantIncome across Loan_ID": "A line chart shows a trend over time, not a comparison between loan statuses."},
    "B8": {"(df['LoanAmount'] > 0).all()": "That is a RANGE check (the amount must be positive).",
           "df['CreditScore'].between(300, 850).all()": "That is a RANGE check (within 300-850).",
           "df.isnull().sum().sum() == 0": "That counts MISSING values, a completeness check, not uniqueness."},
    "B13": {"Fill baths and sqft with 0 so every row can be used": "Filling most of a column with 0 invents data (and 0 square feet is nonsense).",
            "Treat baths and sqft as the target variables to predict": "Nothing in the case says they are targets; they're just mostly-empty columns.",
            "Ignore the blanks, since missing values rarely change a model's results": "They matter a lot: a mostly-empty column may not be usable."},
    "B3": {"Ignore them, because most models handle outliers on their own": "A -200 price is impossible and 125,000 is an extreme outlier. Both would distort scaling and statistics.",
           "Delete the handset_price column since it has bad values": "The column is valuable. Fix or remove the bad VALUES.",
           "Replace both extreme values with the mean right away": "The mean is dragged by the outliers, and you haven't yet checked whether they are errors."},
    "B7": {"Referential integrity": "That compares keys across tables, not a bad value in one column.",
           "Uniqueness constraint": "Uniqueness is about duplicate IDs. A negative amount is a value that is out of bounds."},
    "B10": {"monthly_fee (the plan price the customer pays)": "The fee is known while the customer is still active, so it's a valid predictor.",
            "num_devices (devices linked to the account)": "Known before churn happens, so no leakage.", "region (where the customer lives)": "Known before churn happens, so no leakage."},
    "B12": {"Delete it right away because it is an outlier": "Deleting without checking might throw away a real luxury listing. Investigate first.",
            "Keep it and use it to set the new average price": "One outlier would wildly distort the average.",
            "Log-transform the entire dataset before looking at the outlier": "A transform is a later modeling decision. First work out whether this value is an error."},
    "B14": {"Harmonic surprise clearly causes higher downloads, so add more of it": "Correlation never proves causation, and a small sample proves even less.",
            "There is no real relationship, since the sample is too small to tell": "A 0.98 correlation is very strong.",
            "Higher downloads cause more harmonic surprises, since 0.98 is near 1": "The causal direction isn't established by correlation."},
    "B17": {"Yes, delete them, because negatives are impossible": "dB relative to full scale is naturally negative, so these are valid. Compare that to a negative handset price.",
            "Yes, convert all of them to positive numbers using the absolute value": "Taking absolute values would flip the meaning of the scale.",
            "Only the values below -20 dB are errors; the rest are valid": "They are all valid values; the scale is -30 to 0."},
}


def diagnose(q, picks, choices_shown=None):
    """picks = list of chosen choice texts. -> list of (choice, reason) for each WRONG pick (reason may be '')."""
    notes = TRAPS.get(q["id"], {})
    out = []
    for ch in picks:
        if ch in q["answer"]:
            continue
        out.append((ch, notes.get(ch, "")))
    return out


def multi_feedback(q, picks):
    """For select-all questions: what was missed and what was extra."""
    missed = [a for a in q["answer"] if a not in picks]
    extra = [p for p in picks if p not in q["answer"]]
    return missed, extra


# ---------------------------------------------------------------------------
# Stats helpers used by the cheat sheet calculators (pure Python = works without numpy)
# ---------------------------------------------------------------------------
def quantile(sorted_vals, q):
    """pandas default ('linear' interpolation) quantile."""
    n = len(sorted_vals)
    if n == 1:
        return sorted_vals[0]
    pos = (n - 1) * q
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def summarize_numbers(vals):
    vals = sorted(vals)
    n = len(vals)
    mean = sum(vals) / n
    std = (sum((v - mean) ** 2 for v in vals) / (n - 1)) ** 0.5 if n > 1 else 0.0  # pandas std = sample std
    q1, med, q3 = quantile(vals, 0.25), quantile(vals, 0.5), quantile(vals, 0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return {"n": n, "mean": mean, "std": std, "min": vals[0], "q1": q1, "median": med, "q3": q3, "max": vals[-1],
            "iqr": iqr, "lower": lo, "upper": hi, "outliers": [v for v in vals if v < lo or v > hi]}


def eval_expr_on(expr, dataset="megatelco"):
    """Evaluate ONE pandas expression with `df` loaded. -> (result_obj_or_None, text, error)"""
    expr = (expr or "").strip()
    if not expr:
        return None, "", ""
    if not HAVE_PANDAS:
        return None, "", "pandas isn't installed. " + INSTALL_HINT
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        return None, "", f"SyntaxError: {e.msg}"
    if _BIG_NUMBER.search(expr):
        return None, "", "numbers that big aren't allowed here"
    ns = make_namespace()
    ns["df"] = load_df(dataset)
    SANDBOX["on"] = True
    deadline = [time.monotonic() + TIME_LIMIT]
    old = sys.gettrace()
    try:
        sys.settrace(_trace_factory(deadline))
        try:
            val = eval(compile(tree, "<lab>", "eval"), ns)
        finally:
            sys.settrace(old)
    except StopRun as e:
        return None, "", str(e)
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"
    finally:
        SANDBOX["on"] = False
    return val, fmt_value(val, 25), ""


# ===========================================================================
# CHEAT SHEETS. "live" rows are evaluated by pandas on the Megatelco sample
# when the sheet opens, so the results can't be wrong.
# ===========================================================================
CHEAT_TABS = [
    {"key": "pandas", "title": "pandas toolkit", "blocks": [
        {"kind": "live", "dataset": "megatelco", "heading": "Look at the data   (df = the Megatelco sample, 40 rows)", "rows": [
            ("df.shape", "(rows, columns). It's an attribute, so no parentheses"),
            ("len(df)", "the number of ROWS"),
            ("list(df.columns)[:5]", "df.columns holds the column NAMES"),
            ("df['income'].dtype", "the data type of one column"),
            ("df.dtypes.astype(str).value_counts().to_dict()", "how many columns have each dtype (text shows as str or object)"),
            ("df['leave'].value_counts().to_dict()", "value_counts() = how many times each value appears"),
            ("df['operating_system'].unique().tolist()", "the distinct values in a column"),
            ("df['income'].describe().round(1).to_dict()", "describe() = count, mean, std, min, quartiles, max")]},
        {"kind": "live", "dataset": "megatelco", "heading": "Missing values & duplicates", "rows": [
            ("int(df.isnull().sum().sum())", "total missing cells: isnull() then sum() twice"),
            ("df.isnull().sum()[df.isnull().sum() > 0].to_dict()", "missing per column (only columns that have any)"),
            ("int(df['income'].isnull().sum())", "missing values in ONE column"),
            ("len(df.dropna())", "rows left after .dropna() (drops a row missing ANYTHING)"),
            ("len(df.dropna(subset=['income']))", "rows left when only income matters"),
            ("int(df.duplicated().sum())", "duplicated() flags the 2nd copy of a repeated row"),
            ("len(df.drop_duplicates())", "rows after drop_duplicates() (keeps the first)"),
            ("df['handset_price'].median()", "median ignores NaN and shrugs off outliers"),
            ("round(df['handset_price'].mean(), 1)", "the mean is dragged up by the 125,000 outlier"),
            ("int(df['handset_price'].fillna(df['handset_price'].median()).isnull().sum())", "fillna(median): nothing missing afterwards")]},
        {"kind": "live", "dataset": "megatelco", "heading": "Filtering, selecting & grouping", "rows": [
            ("len(df[df['handset_price'] >= 0])", "NaN >= 0 is False, so missing prices are dropped too"),
            ("len(df[(df['leave'] == 'LEAVE') & (df['income'] > 300000)])", "&  means AND (parentheses around each test)"),
            ("len(df[(df['leave'] == 'LEAVE') | (df['income'] > 300000)])", "|  means OR"),
            ("type(df['income']).__name__", "ONE name in single brackets -> a Series"),
            ("type(df[['income']]).__name__", "a LIST in double brackets -> a DataFrame"),
            ("df.groupby('leave')['income'].mean().round(0).to_dict()", "groupby: split, then average each group"),
            ("df.sort_values('income', ascending=False)['income'].head(3).tolist()", "sort descending, look at the top")]},
        {"kind": "live", "dataset": "megatelco", "heading": "Types, encoding & binning", "rows": [
            ("str(df['operating_system'].astype('category').dtype)", "astype('category'): a fixed set of values"),
            ("int(pd.Categorical(df['reported_satisfaction'], categories=['Low', 'Medium', 'High']).isnull().sum())", "TRAP: values not in categories (case matters!) become NaN"),
            ("int(df['leave'].map({'yes': 1, 'no': 0}).isnull().sum())", "TRAP: map() with the wrong keys -> every value NaN"),
            ("df['leave'].map({'LEAVE': 1, 'STAY': 0}).value_counts().to_dict()", "the working map: keys must match the data exactly"),
            ("pd.get_dummies(df, columns=['operating_system']).shape", "one-hot: 16 columns -> 17 (-1 original, +2 new)"),
            ("pd.qcut(df['income'], q=3, labels=['Low', 'Medium', 'High']).value_counts().to_dict()", "qcut: about the SAME NUMBER of rows per group"),
            ("pd.cut(df['data_mb_used'], bins=3, labels=['Light', 'Moderate', 'Heavy']).value_counts().to_dict()", "cut: equal-WIDTH ranges, uneven counts"),
            ("round(float(np.log1p(df['income'].dropna()).skew()), 2)", "skew() after log1p (log1p = log(1 + x), safe for zeros)")]},
        {"kind": "static", "heading": "Fill-it-with... cheat table (Lab 6)", "cols": ["Column looks like", "Fill / fix with"], "widths": [44],
         "rows": [("numeric WITH outliers (handset_price)", "the MEDIAN"),
                  ("blank really means 'none' (data_leftover_mb)", "0"),
                  ("categorical (considering_change_of_plan)", "the mode, or a placeholder like 'unknown'"),
                  ("only a few rows missing, column essential (income)", "DROP those rows: dropna(subset=[...])"),
                  ("time-ordered data with gaps", "forward fill / interpolate()"),
                  ("impossible values (negative price, age 150)", "set to NaN with .loc, then impute (or drop)")]}]},
    {"key": "stats", "title": "stats & formulas", "blocks": [
        {"kind": "static", "heading": "The formulas you need", "cols": ["Name", "Formula", "Example"], "widths": [22, 40],
         "rows": [("IQR", "Q3 - Q1", "Q1=20, Q3=40  ->  IQR = 20"),
                  ("Upper outlier fence", "Q3 + 1.5 x IQR", "40 + 1.5 x 20 = 70"),
                  ("Lower outlier fence", "Q1 - 1.5 x IQR", "20 - 1.5 x 20 = -10"),
                  ("Z-score", "(x - mean) / std", "(130 - 100) / 20 = 1.5"),
                  ("Min-Max scaling", "(x - min) / (max - min)", "(50 - 0) / (200 - 0) = 0.25"),
                  ("Mean", "sum / count", "sensitive to outliers"),
                  ("Median", "the middle value", "robust to outliers"),
                  ("Range", "max - min", "determined entirely by the extremes")]},
        {"kind": "static", "heading": "Shape of a distribution", "cols": ["Term", "Looks like", "Typical fix"], "widths": [22, 44],
         "rows": [("Positive (right) skew", "long tail to the RIGHT, mean > median (income)", "log transform"),
                  ("Negative (left) skew", "long tail to the LEFT", "(rarely needed)"),
                  ("Outlier", "beyond Q1 - 1.5 x IQR or Q3 + 1.5 x IQR", "error -> fix/remove; real -> keep or cap (winsorize)"),
                  ("Zero-variance column", "same value in every row", "drop it (adds nothing)")]},
        {"kind": "static", "heading": "Which chart?", "cols": ["I want to see...", "Use"], "widths": [52],
         "rows": [("the DISTRIBUTION of one numeric variable", "histogram"),
                  ("median, spread and outliers of one numeric variable", "boxplot"),
                  ("the relationship between TWO numeric variables", "scatterplot"),
                  ("counts / values for categories", "bar chart"),
                  ("correlations among MANY numeric variables", "heatmap of df.corr()  (or a pairplot)"),
                  ("a numeric variable compared across categories", "grouped boxplot"),
                  ("a trend over time", "line chart")]},
        {"kind": "static", "heading": "Correlation", "cols": ["Fact", "Detail"], "widths": [26],
         "rows": [("range", "-1 to 1 (the diagonal of corr() is always 1)"),
                  ("sign", "+ both rise together; - one rises as the other falls"),
                  ("near 0", "no LINEAR relationship"),
                  ("never forget", "correlation does NOT prove causation (Earworms case)"),
                  ("multicollinearity", "two predictors highly correlated with each other")]}]},
    {"key": "crisp", "title": "CRISP-DM & analytics", "blocks": [
        {"kind": "static", "heading": "The 6 CRISP-DM phases  (Big Dogs Don't Make Easy Decisions)", "cols": ["#", "Phase", "What happens"], "widths": [4, 24],
         "rows": [("1", "Business Understanding", "objectives, assess situation, data mining goals, project plan / charter"),
                  ("2", "Data Understanding", "collect, describe, EXPLORE (EDA), check quality"),
                  ("3", "Data Preparation", "clean, validate, transform, engineer features (60-80% of the time)"),
                  ("4", "Modeling", "choose and train models"),
                  ("5", "Evaluation", "does it meet the BUSINESS goals?"),
                  ("6", "Deployment", "put it to work, monitor it")]},
        {"kind": "static", "heading": "Four types of analytics", "cols": ["Type", "Question", "Example"], "widths": [16, 22],
         "rows": [("Descriptive", "What happened?", "seasonal admissions report, KPI dashboard"),
                  ("Diagnostic", "Why did it happen?", "root causes of a sales drop"),
                  ("Predictive", "What will happen?", "churn, demand or fraud forecast"),
                  ("Prescriptive", "What should we do?", "dynamic airline ticket pricing")]},
        {"kind": "static", "heading": "Supervised vs unsupervised", "cols": ["Kind", "Has a target?", "Examples"], "widths": [34, 16],
         "rows": [("Supervised - classification", "yes: a CATEGORY", "churn yes/no, fraud, loan approved/denied"),
                  ("Supervised - regression", "yes: a NUMBER", "downloads, price, sales, followers"),
                  ("Unsupervised - clustering", "no", "customer segments"),
                  ("Unsupervised - PCA", "no", "dimensionality reduction"),
                  ("Affinity grouping", "no", "market basket: items bought together")]},
        {"kind": "static", "heading": "Evaluating models", "cols": ["Model type", "Metrics"], "widths": [22],
         "rows": [("Classification", "accuracy, precision, recall, F1  (it also outputs a probability)"),
                  ("Regression", "MSE, RMSE, MAE, R-squared"),
                  ("Generalization", "performance on NEW, held-out TEST data")]}]},
    {"key": "data", "title": "data types & prep", "blocks": [
        {"kind": "static", "heading": "Types of variables", "cols": ["Type", "Meaning", "Example"], "widths": [14, 46],
         "rows": [("Nominal", "categories, NO order (binary is a subset)", "operating_system, country, yes/no"),
                  ("Ordinal", "categories WITH order, unequal gaps", "satisfaction low/avg/high, star ratings"),
                  ("Discrete", "countable whole numbers", "visitors per day"),
                  ("Continuous", "any value in a range, with decimals", "revenue, weight, income"),
                  ("Target", "the variable you predict (dependent)", "leave, downloads"),
                  ("Identifier", "just a label: NOT a predictor", "customer_id, song_id")]},
        {"kind": "static", "heading": "Data structure & collection", "cols": ["Term", "Meaning"], "widths": [26],
         "rows": [("Cross-sectional", "a snapshot at one point in time"),
                  ("Time series", "one thing tracked over time"),
                  ("Panel / longitudinal", "many subjects tracked over time (countries x years)"),
                  ("Structured", "rows and columns"),
                  ("Unstructured", "text, audio, images, video"),
                  ("3 Vs of big data", "Volume (how much), Velocity (how fast), Variety (how many formats)"),
                  ("Sampling", "random, stratified (within subgroups), systematic (every nth), convenience (easy = biased)")]},
        {"kind": "static", "heading": "Validation checks (Week 6)", "cols": ["Check", "Tests", "Example"], "widths": [24, 34],
         "rows": [("Range", "one value within bounds", "age 0-120, LoanAmount > 0"),
                  ("Logic", "consistency between fields", "signup_date before last_login_date"),
                  ("Uniqueness", "no duplicate keys", "Loan_ID.duplicated().sum() == 0"),
                  ("Referential integrity", "foreign keys match another table", "sales.customer_id exists in customers"),
                  ("Data leakage", "uses info unavailable at prediction time", "cancellation_reason when predicting churn")]},
        {"kind": "static", "heading": "Encoding, scaling & joins (Week 7)", "cols": ["Need", "Use"], "widths": [48],
         "rows": [("nominal category -> numbers", "one-hot  (pd.get_dummies)"),
                  ("ordered category -> numbers", "ordinal encoding (keeps the rank)"),
                  ("right-skewed positive numbers", "log transform (np.log1p if there are zeros)"),
                  ("rescale to 0-1 (outlier-sensitive)", "Min-Max normalization"),
                  ("mean 0, std 1 (less outlier-sensitive)", "z-score standardization"),
                  ("equal-WIDTH bins / equal-COUNT bins", "pd.cut  /  pd.qcut"),
                  ("INNER join", "only keys in BOTH tables"),
                  ("LEFT / RIGHT join", "all of the left / right table (NaN where no match)"),
                  ("OUTER join", "every key from both"),
                  ("too many features", "PCA (unsupervised) or feature selection: filter / wrapper / embedded")]}]},
    {"key": "biz", "title": "business understanding", "blocks": [
        {"kind": "static", "heading": "The 4 Business Understanding steps (in order)", "cols": ["#", "Step"], "widths": [4],
         "rows": [("1", "Determine business objectives (the business OUTCOME)"),
                  ("2", "Assess the situation (resources, constraints, data, stakeholders)"),
                  ("3", "Determine data mining goals (the technical task)"),
                  ("4", "Produce the project plan / charter (a LIVING document)")]},
        {"kind": "static", "heading": "Frameworks", "cols": ["Name", "Stands for"], "widths": [12],
         "rows": [("SMART", "Specific, Measurable, Achievable, Relevant, Time-bound"),
                  ("SWOT", "Strengths, Weaknesses, Opportunities, Threats"),
                  ("RACI", "Responsible (does it), Accountable (owns it), Consulted (input), Informed (updates)"),
                  ("KPIs", "business metrics (retention, revenue) AND technical metrics (precision, recall)")]},
        {"kind": "static", "heading": "Mendelow's stakeholder matrix", "cols": ["", "LOW interest", "HIGH interest"], "widths": [18, 24],
         "rows": [("HIGH power", "KEEP SATISFIED (regulators)", "MANAGE CLOSELY (record labels)"),
                  ("LOW power", "MONITOR", "KEEP INFORMED")]},
        {"kind": "static", "heading": "Problems & pitfalls", "cols": ["Idea", "Meaning"], "widths": [24],
         "rows": [("Tame problem", "well-defined, data available, known solutions, measurable: a good quick win"),
                  ("Wicked problem", "many stakeholders, no single answer, solutions cause new problems"),
                  ("4 pitfalls", "vague goals, misaligned stakeholders, skipping to the data too fast, ignoring constraints"),
                  ("Risk & Assumption Log", "tracks uncertainties: bad data, access, privacy, skills gaps"),
                  ("Business objective vs data mining goal", "'reduce churn 10%'  vs  'predict who will churn'"),
                  ("Data / information / knowledge", "raw facts / facts with context / insight that leads to action")]}]},
]



# ===========================================================================
# GUI (tkinter ships with Python)
# ===========================================================================
try:
    import tkinter as tk
    from tkinter import font as tkfont
    from tkinter import messagebox, ttk
    HAVE_TK = True
except Exception:  # ImportError, or a broken Tcl install
    HAVE_TK = False

if HAVE_TK:
    # palette
    # Every value inside one palette must be unique: switching themes remaps old colors to new ones.
    LIGHT = dict(
        BG="#f4f5f7", CARD="#ffffff", LINE="#d0d5dd", TEXT="#101828", MUTED="#667085", HEAD="#1e3a8a",
        ACCENT="#2563eb", ACCENT_DK="#1d4ed8", GOOD="#15803d", GOOD_BG="#dcfce7", BAD="#b91c1c",
        BAD_BG="#fee2e2", SEL_BG="#dbeafe", CUR_BG="#fff3b0", CHG_BG="#e6f4ea",
        SYN_KW="#008000", SYN_KWOP="#aa22ff", SYN_BUILTIN="#2e8b2e", SYN_STR="#ba2121",
        SYN_NUM="#2255dd", SYN_COMMENT="#408080", SYN_DEF="#0000ff",
        B1="#2f6fed", B2="#0d9488", B3="#ea7a12", B4="#7c3aed", B5="#16a34a", B6="#db2777",
    )
    DARK = dict(
        BG="#0d1117", CARD="#161b22", LINE="#30363d", TEXT="#e6edf3", MUTED="#8b949e", HEAD="#79b8ff",
        ACCENT="#388bfd", ACCENT_DK="#1f6feb", GOOD="#3fb950", GOOD_BG="#14301f", BAD="#f85149",
        BAD_BG="#3d1418", SEL_BG="#1c3358", CUR_BG="#4a4210", CHG_BG="#173824",
        SYN_KW="#7ee787", SYN_KWOP="#d2a8ff", SYN_BUILTIN="#56d364", SYN_STR="#ffa198",
        SYN_NUM="#79c0ff", SYN_COMMENT="#7d8590", SYN_DEF="#a5d6ff",
        B1="#2d6cdf", B2="#14a39a", B3="#d9730d", B4="#8957e5", B5="#2ea043", B6="#d12f7d",
    )
    PALETTES = {"light": LIGHT, "dark": DARK}
    CURRENT = {"name": "light"}


    def apply_palette(name):
        CURRENT["name"] = name
        globals().update(PALETTES[name])  # BG, CARD, TEXT, ... become module-level names


    def system_theme():
        """'dark' if Windows is set to dark app mode, else 'light'."""
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as k:
                return "light" if winreg.QueryValueEx(k, "AppsUseLightTheme")[0] else "dark"
        except Exception:
            return "light"


    apply_palette("light")
    F = {}  # shared fonts (resizing them resizes the whole app)
    APP = {"root": None, "listeners": []}


    def make_fonts(root):
        fam, mono = "Segoe UI", "Consolas"
        F["ui"] = tkfont.Font(root=root, family=fam, size=11)
        F["bold"] = tkfont.Font(root=root, family=fam, size=11, weight="bold")
        F["h1"] = tkfont.Font(root=root, family=fam, size=20, weight="bold")
        F["h2"] = tkfont.Font(root=root, family=fam, size=13, weight="bold")
        F["code"] = tkfont.Font(root=root, family=mono, size=12)
        F["codeb"] = tkfont.Font(root=root, family=mono, size=12, weight="bold")
        F["codei"] = tkfont.Font(root=root, family=mono, size=12, slant="italic")


    def shade(color, factor):
        h = color.lstrip("#")
        rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * factor))) for c in rgb)


    def row_height():
        return F["ui"].metrics("linespace") + 10


    def scale_trees(widget, ratio):
        """Keep table columns proportional when the text size changes."""
        if isinstance(widget, ttk.Treeview):
            for col in widget["columns"]:
                c = widget.column(col)
                widget.column(col, width=int(c["width"] * ratio), minwidth=int(c["minwidth"] * ratio))
        for child in widget.winfo_children():
            scale_trees(child, ratio)


    def resize_fonts(delta):
        old = abs(F["ui"].cget("size"))
        for f in F.values():
            f.configure(size=max(8, min(26, abs(f.cget("size")) + delta)))
        new = abs(F["ui"].cget("size"))
        root = APP["root"]
        if root is not None and new != old:
            ttk.Style(root).configure("Treeview", rowheight=row_height())  # taller rows for bigger text
            scale_trees(root, new / old)
        for fn in list(APP["listeners"]):
            fn()


    def make_tile(parent, title, subtitle, color_key, command):
        """A big colored button whose text WRAPS instead of being cut off at large text sizes."""
        col = globals()[color_key]
        tile = tk.Frame(parent, bg=col, cursor="hand2", padx=16, pady=12)
        top = tk.Label(tile, text=title, font=F["h2"], bg=col, fg="#fefefe", anchor="w", justify="left")
        sub = tk.Label(tile, text=subtitle, font=F["bold"], bg=col, fg="#fefefe", anchor="w", justify="left")
        top.pack(fill="x")
        sub.pack(fill="x")
        parts = (tile, top, sub)

        def paint(factor):
            c = globals()[color_key]
            c = c if factor == 1 else shade(c, factor)
            for w in parts:
                w.configure(bg=c)
        hover = lambda: 0.88 if CURRENT["name"] == "light" else 1.2  # noqa: E731
        for w in parts:
            w.bind("<Button-1>", lambda e: command())
            w.bind("<Enter>", lambda e: paint(hover()))
            w.bind("<Leave>", lambda e: paint(1))
        tile.bind("<Configure>", lambda e: (top.configure(wraplength=max(120, e.width - 40)),
                                            sub.configure(wraplength=max(120, e.width - 40))))
        return tile


    def make_chip(parent, item):
        """Small colored tag: purple = your professor's question, grey = practice question written by Claude."""
        prof = origin_of(item) == "prof"
        return tk.Label(parent, text=origin_chip(item), font=F["bold"], bg=B4 if prof else LINE,
                        fg="#fefefe" if prof else TEXT, padx=8, pady=2)


    def style_app(root):
        st = ttk.Style(root)
        st.theme_use("clam")
        root.configure(bg=BG)
        root.option_add("*TCombobox*Listbox.background", CARD)
        root.option_add("*TCombobox*Listbox.foreground", TEXT)
        st.configure(".", background=BG, foreground=TEXT, font=F["ui"], bordercolor=LINE,
                     lightcolor=BG, darkcolor=BG, troughcolor=LINE, focuscolor=BG)
        st.configure("TFrame", background=BG)
        st.configure("Card.TFrame", background=CARD)
        st.configure("TLabel", background=BG, foreground=TEXT, font=F["ui"])
        st.configure("TButton", background=CARD, foreground=TEXT, font=F["ui"], padding=(12, 6),
                     bordercolor=LINE, lightcolor=CARD, darkcolor=CARD)
        st.map("TButton", background=[("active", SEL_BG), ("disabled", BG)], foreground=[("disabled", MUTED)])
        st.configure("Accent.TButton", background=ACCENT, foreground="#ffffff", font=F["bold"],
                     padding=(14, 8), bordercolor=ACCENT_DK, lightcolor=ACCENT, darkcolor=ACCENT)
        st.map("Accent.TButton", background=[("active", ACCENT_DK), ("disabled", MUTED)],
               foreground=[("disabled", "#ffffff")])
        st.configure("Treeview", font=F["ui"], rowheight=row_height(), background=CARD, fieldbackground=CARD,
                     foreground=TEXT, bordercolor=LINE)
        st.map("Treeview", background=[("selected", ACCENT)], foreground=[("selected", "#ffffff")])
        st.configure("Treeview.Heading", font=F["bold"], background=LINE, foreground=TEXT, relief="flat")
        st.map("Treeview.Heading", background=[("active", SEL_BG)])
        st.configure("TLabelframe", background=BG, bordercolor=LINE)
        st.configure("TLabelframe.Label", background=BG, font=F["bold"], foreground=MUTED)
        for name in ("TEntry", "TSpinbox", "TCombobox"):
            st.configure(name, fieldbackground=CARD, foreground=TEXT, insertcolor=TEXT, bordercolor=LINE,
                         arrowcolor=TEXT, background=CARD)
        st.map("TCombobox", fieldbackground=[("readonly", CARD)], foreground=[("readonly", TEXT)])
        st.configure("TCheckbutton", background=BG, foreground=TEXT, indicatorbackground=CARD, indicatorforeground=TEXT,
                     bordercolor=MUTED, indicatormargin=(0, 0, 8, 0), indicatorsize=18)
        st.map("TCheckbutton", background=[("active", BG)],
               indicatorbackground=[("selected", ACCENT), ("!selected", CARD)])
        st.configure("TScrollbar", background=LINE, troughcolor=BG, bordercolor=BG, arrowcolor=TEXT)
        st.map("TScrollbar", background=[("active", MUTED)])
        st.configure("TScale", background=ACCENT, troughcolor=LINE)
        st.configure("TSeparator", background=LINE)
        st.configure("TPanedwindow", background=BG)
        st.configure("Sash", background=LINE)
        st.configure("TNotebook", background=BG, bordercolor=LINE)
        st.configure("TNotebook.Tab", background=BG, foreground=MUTED, padding=(14, 6), font=F["bold"])
        st.map("TNotebook.Tab", background=[("selected", CARD)], foreground=[("selected", TEXT)])


    # --- coloring code (tokenize-based) -------------------------------------------------------------
    BUILTIN_NAMES = {n for n in dir(builtins) if n[0].islower() and not keyword.iskeyword(n)}
    WORD_OPS = {"and", "or", "not", "in", "is"}
    STRING_TOKENS = {"STRING", "FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"}
    SYNTAX_TAGS = ("kw", "kwop", "builtin", "string", "number", "comment", "defname", "gutter")
    PANDAS_NAMES = {"pd", "np", "plt", "sns", "df"}


    def code_tags(txt):
        txt.tag_configure("kw", foreground=SYN_KW, font=F["codeb"])
        txt.tag_configure("kwop", foreground=SYN_KWOP, font=F["codeb"])
        txt.tag_configure("builtin", foreground=SYN_BUILTIN)
        txt.tag_configure("string", foreground=SYN_STR)
        txt.tag_configure("number", foreground=SYN_NUM)
        txt.tag_configure("comment", foreground=SYN_COMMENT, font=F["codei"])
        txt.tag_configure("defname", foreground=SYN_DEF, font=F["codeb"])
        txt.tag_configure("gutter", foreground=MUTED)
        txt.tag_configure("cur", background=CUR_BG)


    def highlight(txt, src, offset=0):
        """Color the code in `txt`. Line n of src is row n; `offset` = characters before the code on each row."""
        for tag in SYNTAX_TAGS:
            txt.tag_remove(tag, "1.0", "end")
        if offset:
            for row in range(1, src.count("\n") + 2):
                txt.tag_add("gutter", f"{row}.0", f"{row}.{offset}")
        tokens = []
        try:
            for tok in tokenize.generate_tokens(io.StringIO(src).readline):
                tokens.append(tok)
        except (tokenize.TokenError, SyntaxError):
            pass
        prev = ""
        for tok in tokens:
            text, (srow, scol), (erow, ecol) = tok.string, tok.start, tok.end
            kind = tokenize.tok_name.get(tok.type, "")
            tag = None
            if kind == "NAME":
                if prev in ("def", "class"):
                    tag = "defname"
                elif text in WORD_OPS:
                    tag = "kwop"
                elif keyword.iskeyword(text):
                    tag = "kw"
                elif text in BUILTIN_NAMES:
                    tag = "builtin"
                elif text in PANDAS_NAMES:
                    tag = "defname"
                prev = text
            else:
                if kind not in ("NL", "NEWLINE", "INDENT", "DEDENT", "COMMENT"):
                    prev = ""
                if kind == "NUMBER":
                    tag = "number"
                elif kind in STRING_TOKENS:
                    tag = "string"
                elif kind == "COMMENT":
                    tag = "comment"
            if not tag:
                continue
            for row in range(srow, erow + 1):
                a = (scol if row == srow else 0) + offset
                if row == erow:
                    txt.tag_add(tag, f"{row}.{a}", f"{row}.{ecol + offset}")
                else:
                    txt.tag_add(tag, f"{row}.{a}", f"{row}.end")


    # --- switching theme ---------------------------------------------------------------------------
    COLOR_OPTIONS = ("bg", "fg", "background", "foreground", "highlightbackground", "highlightcolor",
                     "insertbackground", "selectbackground", "selectforeground", "activebackground",
                     "activeforeground", "troughcolor", "disabledforeground")


    def recolor(widget, mapping):
        try:
            keys = widget.keys()
        except Exception:
            keys = []
        for opt in COLOR_OPTIONS:
            if opt in keys:
                try:
                    cur = str(widget.cget(opt)).lower()
                    if cur in mapping:
                        widget.configure(**{opt: mapping[cur]})
                except tk.TclError:
                    pass
        if isinstance(widget, tk.Text):
            for tag in widget.tag_names():
                for opt in ("background", "foreground"):
                    try:
                        cur = str(widget.tag_cget(tag, opt)).lower()
                        if cur in mapping:
                            widget.tag_configure(tag, **{opt: mapping[cur]})
                    except tk.TclError:
                        pass
        if isinstance(widget, ttk.Treeview):
            for tag in ("chg", "bar"):
                try:
                    cur = str(widget.tag_configure(tag, "background")).lower()
                    if cur in mapping:
                        widget.tag_configure(tag, background=mapping[cur])
                except tk.TclError:
                    pass
        if getattr(widget, "_theme_btn", False):
            widget.configure(text=theme_button_text())
        for child in widget.winfo_children():
            recolor(child, mapping)


    def theme_button_text():
        return "Light mode" if CURRENT["name"] == "dark" else "Dark mode"


    def set_theme(root, name):
        old, new = PALETTES[CURRENT["name"]], PALETTES[name]
        mapping = {old[k].lower(): new[k] for k in old}
        apply_palette(name)
        style_app(root)
        recolor(root, mapping)


    # --- small widget helpers ----------------------------------------------------------------------
    def ro_text(parent, height, font=None, bg=None, **kw):
        """Read-only Text widget with a scrollbar."""
        box = ttk.Frame(parent)
        kw.setdefault("wrap", "word")
        txt = tk.Text(box, height=height, font=font or F["ui"], bg=bg or CARD, fg=TEXT, insertbackground=TEXT,
                      relief="solid", bd=1, highlightthickness=0, padx=8, pady=6, **kw)
        sb = ttk.Scrollbar(box, command=txt.yview)
        txt.configure(yscrollcommand=sb.set, state="disabled")
        sb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)
        return box, txt


    def set_text(txt, content, tag=None):
        txt.configure(state="normal")
        txt.delete("1.0", "end")
        txt.insert("end", content, tag or ())
        txt.configure(state="disabled")


    def make_grid(parent, height=8, hscroll=True):
        """A table: Treeview with scrollbars. -> (frame, tree)."""
        box = ttk.Frame(parent)
        tree = ttk.Treeview(box, show="headings", height=height)
        vs = ttk.Scrollbar(box, command=tree.yview)
        tree.configure(yscrollcommand=vs.set)
        if hscroll:
            hs = ttk.Scrollbar(box, orient="horizontal", command=tree.xview)
            tree.configure(xscrollcommand=hs.set)
            hs.pack(side="bottom", fill="x")
        vs.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        tree.tag_configure("chg", background=CHG_BG)
        return box, tree


    def fill_plain_grid(tree, cols, rows):
        tree.delete(*tree.get_children())
        ids = [f"c{i}" for i in range(len(cols))]
        tree.configure(columns=ids)
        cw = F["bold"].measure("0")
        for i, name in enumerate(cols):
            width = max([len(str(name)) + 2] + [len(str(r[i])) for r in rows[:40]])
            tree.heading(ids[i], text=name, anchor="w")
            tree.column(ids[i], width=max(cw * 7, min(cw * 26, cw * width + 16)), minwidth=cw * 4, anchor="w", stretch=False)
        for r in rows:
            tree.insert("", "end", values=list(r))


    def dataset_table(name):
        rows = list(csv.reader(io.StringIO(DATA[name])))
        return rows[0], rows[1:]


    def fill_df_grid(tree, df, before=None, max_rows=25):
        """Show a DataFrame. Rows with changed cells are tinted; new columns get a star."""
        tree.delete(*tree.get_children())
        cols = list(df.columns)
        ids = ["idx"] + [f"c{i}" for i in range(len(cols))]
        tree.configure(columns=ids)
        new_cols = set(cols) - set(before.columns) if before is not None else set()
        cw = F["bold"].measure("0")
        tree.heading("idx", text="", anchor="w")
        tree.column("idx", width=cw * 5, minwidth=cw * 3, anchor="w", stretch=False)
        head = df.head(max_rows)
        for i, name in enumerate(cols):
            label = ("* " if name in new_cols else "") + str(name)
            width = max([len(label) + 2] + [len(_v(x)) for x in head[name].tolist()])
            tree.heading(ids[i + 1], text=label, anchor="w")
            tree.column(ids[i + 1], width=max(cw * 7, min(cw * 24, cw * width + 14)), minwidth=cw * 4, anchor="w", stretch=False)
        changed = set()
        if before is not None:
            try:
                shared = [c for c in cols if c in before.columns]
                common = [i for i in head.index if i in before.index]
                for c in shared:
                    ch = _changed_cells(before.loc[common, c], head.loc[common, c])
                    changed |= set(ch[ch].index)
                changed |= {i for i in head.index if i not in before.index}
            except Exception:
                changed = set()
        for idx, row in head.iterrows():
            tree.insert("", "end", values=[idx] + [_v(x) for x in row.tolist()],
                        tags=("chg",) if idx in changed else ())
        return len(df), len(cols)


    def fill_info_grid(tree, df, before=None):
        tree.delete(*tree.get_children())
        cols = ("name", "dtype", "nonnull", "missing", "unique")
        tree.configure(columns=cols)
        cw = F["bold"].measure("0")
        for c, txt, w in (("name", "Column", 22), ("dtype", "Type", 12), ("nonnull", "Non-null", 10),
                          ("missing", "Missing", 9), ("unique", "Unique", 9)):
            tree.heading(c, text=txt, anchor="w")
            tree.column(c, width=cw * w, minwidth=cw * 5, anchor="w", stretch=(c == "name"))
        prev = {r[0]: r for r in frame_info(before)} if before is not None else {}
        for row in frame_info(df):
            changed = before is not None and prev.get(row[0], None) != row
            tree.insert("", "end", values=row, tags=("chg",) if changed else ())


    class ScrollFrame(ttk.Frame):
        """A vertically scrollable area. Put content in .body"""

        def __init__(self, parent):
            super().__init__(parent)
            self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
            self.sb = ttk.Scrollbar(self, command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.sb.set)
            self.sb.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)
            self.body = ttk.Frame(self.canvas, padding=(24, 12))
            self.win = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
            self.body.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width))

        def scroll(self, units):
            if self.body.winfo_reqheight() > self.canvas.winfo_height():
                self.canvas.yview_scroll(units, "units")


    def parse_floats(raw):
        out = []
        for piece in re.split(r"[,\s;]+", raw.strip()):
            if piece:
                out.append(float(piece))
        return out


    def fmt_num(x):
        if isinstance(x, float):
            return f"{x:,.4f}".rstrip("0").rstrip(".")
        return str(x)


    def png_to_photo(png, max_w=640):
        img = tk.PhotoImage(data=base64.b64encode(png).decode("ascii"))
        if img.width() > max_w:
            img = img.subsample(-(-img.width() // max_w))
        return img



    # ===========================================================================
    # CODE LAB (the dev mode of this tool)
    # ===========================================================================
    class CodeLab(tk.Toplevel):
        def __init__(self, app, code_text, data=None, setup=None, heading="Code Lab", q=None, tag="lab"):
            super().__init__(app.root)
            self.app, self.code_text, self.data, self.setup, self.q, self.tag = app, code_text, data, setup, q, tag
            self.k = 0
            self.steps, self.error = [], None
            self.cum = []
            self.revealed = set()
            self._scale_lock = False
            self.playing = False
            self._photo = None
            self.predict = tk.BooleanVar(value=False)
            self.title("Code Lab  -  " + heading)
            self.geometry("1400x900")
            self.minsize(1040, 700)
            self.configure(bg=BG)
            self._build(heading)
            for key, fn in (("<Right>", self.next), ("<space>", self.next), ("<Return>", self.next),
                            ("<Left>", self.prev), ("<BackSpace>", self.prev)):
                self.bind(key, lambda e, fn=fn: self._key(fn))
            self.bind("<Home>", lambda e: self._key(lambda: self.go(0)))
            self.bind("<End>", lambda e: self._key(lambda: self.go(len(self.steps) - 1)))
            self.bind("<Escape>", lambda e: self.destroy())
            self.bind("<F3>", lambda e: self.app.open_cheat(self.app.cheat_tab_for(self.q)))
            self.bind("<Control-equal>", lambda e: resize_fonts(1))
            self.bind("<Control-minus>", lambda e: resize_fonts(-1))
            self.predict.trace_add("write", self._on_predict)
            self.update_idletasks()
            self.rerun()
            self.lift()
            self.focus_force()

        # --- layout ------------------------------------------------------------
        def _build(self, heading):
            top = ttk.Frame(self, padding=(14, 10, 14, 4))
            top.pack(fill="x")
            ttk.Label(top, text=heading, font=F["h2"], foreground=HEAD, wraplength=720, justify="left").pack(side="left")
            self.app.theme_button(top).pack(side="right", padx=8)
            ttk.Button(top, text="A+", width=3, command=lambda: resize_fonts(1)).pack(side="right", padx=2)
            ttk.Button(top, text="A-", width=3, command=lambda: resize_fonts(-1)).pack(side="right", padx=2)
            ttk.Button(top, text="Cheat sheets  (F3)", style="Accent.TButton",
                       command=lambda: self.app.open_cheat(self.app.cheat_tab_for(self.q))).pack(side="right", padx=8)
            if self.q:
                ttk.Button(top, text="Show answer", command=self.show_answer).pack(side="right", padx=2)
            if self.data:
                tk.Label(self, text=f"df = {DATASET_INFO.get(self.data, self.data)}", bg=BG, fg=MUTED, font=F["ui"],
                         anchor="w", justify="left", wraplength=1200).pack(fill="x", padx=14)
            hint = ttk.Frame(self, padding=(14, 0, 14, 2))
            hint.pack(fill="x")
            ttk.Label(hint, text="Keys:  Right / Space = next    Left = back    F3 = cheat sheets    Esc = close",
                      foreground=MUTED).pack(side="left")
            ttk.Checkbutton(hint, text="Predict first  (hide what each line does until I click Reveal)",
                            variable=self.predict, takefocus=False).pack(side="right")

            bar = ttk.Frame(self, padding=(14, 8))
            bar.pack(side="bottom", fill="x")
            self.btn_first = ttk.Button(bar, text="|<", width=4, command=lambda: self.go(0))
            self.btn_prev = ttk.Button(bar, text="<  Back", command=self.prev)
            self.btn_next = ttk.Button(bar, text="Next step  >", style="Accent.TButton", command=self.next)
            self.btn_last = ttk.Button(bar, text=">|", width=4, command=lambda: self.go(len(self.steps) - 1))
            self.btn_play = ttk.Button(bar, text="Auto-play", command=self.toggle_play)
            for b in (self.btn_first, self.btn_prev, self.btn_next, self.btn_last, self.btn_play):
                b.pack(side="left", padx=3)
            self.scale = ttk.Scale(bar, from_=0, to=1, orient="horizontal", command=self._on_scale)
            self.scale.pack(side="left", fill="x", expand=True, padx=14)
            self.counter = ttk.Label(bar, text="", font=F["bold"])
            self.counter.pack(side="left")

            main = ttk.PanedWindow(self, orient="horizontal")
            main.pack(fill="both", expand=True, padx=14, pady=4)
            left = ttk.Frame(main)
            main.add(left, weight=2)
            ttk.Label(left, text="CODE", foreground=MUTED, font=F["bold"]).pack(anchor="w")
            box, self.code = ro_text(left, 8, font=F["code"], wrap="none")
            code_tags(self.code)
            box.pack(fill="both", expand=True)
            if self.setup:
                ttk.Label(left, text="ALREADY RAN BEFORE THIS CODE (setup)", foreground=MUTED, font=F["bold"]).pack(anchor="w", pady=(8, 0))
                sbox, self.setup_txt = ro_text(left, min(5, self.setup.count("\n") + 2), font=F["code"], wrap="none")
                code_tags(self.setup_txt)
                self.setup_txt.configure(state="normal")
                self.setup_txt.insert("1.0", self.setup)
                highlight(self.setup_txt, self.setup)
                self.setup_txt.configure(state="disabled")
                sbox.pack(fill="x")
            ttk.Label(left, text="OUTPUT SO FAR", foreground=MUTED, font=F["bold"]).pack(anchor="w", pady=(8, 0))
            obox, self.out = ro_text(left, 6, font=F["code"])
            self.out.tag_configure("err", foreground=BAD)
            obox.pack(fill="x")

            right = ttk.Frame(main)
            main.add(right, weight=3)
            self.title_lbl = tk.Label(right, text="", font=F["h2"], bg=BG, fg=TEXT, anchor="w", justify="left", wraplength=640)
            self.title_lbl.pack(fill="x", pady=(0, 4))
            right.bind("<Configure>", lambda e: self.title_lbl.configure(wraplength=max(300, e.width - 20)))
            ebox, self.explain = ro_text(right, 9)
            for name, kw in (("h", dict(font=F["bold"], spacing1=6)), ("code", dict(font=F["code"])),
                             ("ok", dict(foreground=GOOD, font=F["bold"])), ("bad", dict(foreground=BAD, font=F["bold"])),
                             ("dim", dict(foreground=MUTED))):
                self.explain.tag_configure(name, **kw)
            ebox.pack(fill="both", expand=True)

            self.nb = ttk.Notebook(right)
            self.nb.pack(fill="both", expand=True, pady=(8, 0))
            dpage = ttk.Frame(self.nb, padding=4)
            self.nb.add(dpage, text="Data")
            row = ttk.Frame(dpage)
            row.pack(fill="x", pady=(0, 4))
            ttk.Label(row, text="Showing:").pack(side="left")
            self.frame_pick = ttk.Combobox(row, state="readonly", width=18, values=[])
            self.frame_pick.pack(side="left", padx=6)
            self.frame_pick.bind("<<ComboboxSelected>>", lambda e: self.render())
            self.data_note = ttk.Label(row, text="", foreground=MUTED)
            self.data_note.pack(side="left", padx=8)
            gbox, self.data_grid = make_grid(dpage, height=7)
            gbox.pack(fill="both", expand=True)
            ipage = ttk.Frame(self.nb, padding=4)
            self.nb.add(ipage, text="Columns (types & missing)")
            ibox, self.info_grid = make_grid(ipage, height=7)
            ibox.pack(fill="both", expand=True)
            vpage = ttk.Frame(self.nb, padding=4)
            self.nb.add(vpage, text="Variables")
            vbox, self.var_grid = make_grid(vpage, height=7)
            vbox.pack(fill="both", expand=True)
            cpage = ttk.Frame(self.nb, padding=4)
            self.nb.add(cpage, text="Chart")
            self.chart_cap = ttk.Label(cpage, text="", foreground=MUTED, wraplength=640)
            self.chart_cap.pack(anchor="w")
            self.chart_lbl = tk.Label(cpage, bg=BG, text="(no chart on this step)", fg=MUTED, font=F["ui"])
            self.chart_lbl.pack(fill="both", expand=True)

        # --- running -----------------------------------------------------------
        def rerun(self):
            self.playing = False
            self.revealed = set()
            self.btn_play.configure(text="Auto-play")
            self.steps, _, err = run_steps(self.code_text, self.data, self.setup, self.tag)
            self.error = err
            self.cum, acc = [], ""
            for s in self.steps:
                if s["printed"].strip():
                    acc += s["printed"]
                if s["result"] is not None:
                    acc += s["result"] + "\n"
                self.cum.append(acc)
            self.code.configure(state="normal")
            self.code.delete("1.0", "end")
            for n, line in enumerate(self.code_text.split("\n"), 1):
                self.code.insert("end", f"{n:>3} | {line}\n")
            highlight(self.code, self.code_text, 6)
            self.code.configure(state="disabled")
            n = len(self.steps)
            self.scale.configure(to=max(1, n - 1))
            self.k = 0
            if n == 0:
                self.title_lbl.configure(text="Nothing to run", fg=BAD if err else MUTED)
                set_text(self.explain, err or "There is no code to run.", "bad" if err else "dim")
                self.counter.configure(text="0 / 0")
            else:
                self.render()

        # --- navigation --------------------------------------------------------
        def _key(self, fn):
            if isinstance(self.focus_get(), (tk.Entry, ttk.Entry, ttk.Combobox)):
                return
            fn()

        def _on_predict(self, *_):
            self.focus_set()
            if self.steps:
                self.render()

        def go(self, k):
            if not self.steps:
                return
            self.k = max(0, min(len(self.steps) - 1, k))
            self.render()

        def next(self):
            if not self.steps:
                return
            if self.predict.get() and self.k not in self.revealed:
                self.revealed.add(self.k)
                self.render()
            elif self.k < len(self.steps) - 1:
                self.go(self.k + 1)
            else:
                self.playing = False
                self.btn_play.configure(text="Auto-play")

        def prev(self):
            self.go(self.k - 1)

        def _on_scale(self, v):
            if not self._scale_lock and self.steps:
                self.go(int(round(float(v))))

        def toggle_play(self):
            self.playing = not self.playing
            self.btn_play.configure(text="Pause" if self.playing else "Auto-play")
            if self.playing:
                if self.k >= len(self.steps) - 1:
                    self.go(0)
                self._tick()

        def _tick(self):
            if self.playing and self.winfo_exists():
                self.next()
                if self.playing:
                    self.after(1600 if self.predict.get() else 1100, self._tick)

        # --- drawing -----------------------------------------------------------
        def render(self):
            s, k, n = self.steps[self.k], self.k, len(self.steps)
            predicting = self.predict.get() and k not in self.revealed
            self._scale_lock = True
            self.scale.set(k)
            self._scale_lock = False
            self.counter.configure(text=f"Step {k + 1} / {n}")
            self.btn_next.configure(text="Reveal  >" if predicting else "Next step  >")
            self.btn_prev.state(["!disabled"] if k > 0 else ["disabled"])
            self.btn_first.state(["!disabled"] if k > 0 else ["disabled"])
            self.btn_next.state(["!disabled"] if (k < n - 1 or predicting) else ["disabled"])
            self.btn_last.state(["!disabled"] if k < n - 1 else ["disabled"])

            a, b = s["lines"]
            self.code.configure(state="normal")
            self.code.tag_remove("cur", "1.0", "end")
            self.code.tag_add("cur", f"{a}.0", f"{b}.0 lineend+1c")
            self.code.configure(state="disabled")
            self.code.see(f"{a}.0")

            where = f"line {a}" if a == b else f"lines {a}-{b}"
            if predicting:
                self.title_lbl.configure(text=f"Step {k + 1}:  PREDICT - what will {where} do?", fg=ACCENT)
            elif s["error"]:
                self.title_lbl.configure(text=f"Step {k + 1} ({where}) hit an error", fg=BAD)
            else:
                self.title_lbl.configure(text=f"Step {k + 1} of {n}  -  ran {where}", fg=TEXT)

            ex = self.explain
            ex.configure(state="normal")
            ex.delete("1.0", "end")
            if predicting:
                ex.insert("end", "Your turn! Before you click Reveal, think:\n", "h")
                ex.insert("end", "  1. Which columns or rows does this line touch?\n"
                                 "  2. After it runs, how many rows and columns will the data have?\n"
                                 "  3. Does any column change type, or gain / lose missing values?\n"
                                 "  4. Does it print something, or does it only LOOK at the data?\n\n")
                ex.insert("end", "The tables below show the data from BEFORE this line runs.", "dim")
            else:
                self._explain_step(ex, s)
            ex.configure(state="disabled")

            # data tabs: BEFORE this step while predicting, AFTER otherwise
            snap = s["before"] if predicting else s["snap"]
            prev_snap = (self.steps[k - 1]["snap"] if k > 0 else {}) if predicting else s["before"]
            frames = [name for name, (kind, _) in snap.items() if kind == "df"]
            self.frame_pick.configure(values=frames)
            want = self.frame_pick.get()
            if want not in frames:
                want = focus_frame(s) if not predicting else ("df" if "df" in frames else (frames[0] if frames else None))
                if want not in frames and frames:
                    want = frames[0]
            if want:
                self.frame_pick.set(want)
                df = snap[want][1]
                before = prev_snap.get(want, (None, None))[1] if prev_snap.get(want, (None, None))[0] == "df" else None
                nrows, ncols = fill_df_grid(self.data_grid, df, None if predicting else before)
                note = f"{nrows} rows x {ncols} columns"
                if nrows > 25:
                    note += "  (first 25 shown)"
                if not predicting and before is not None:
                    note += "   | tinted rows changed, * = new column"
                self.data_note.configure(text=note)
                fill_info_grid(self.info_grid, df, None if predicting else before)
            else:
                self.frame_pick.set("")
                for g in (self.data_grid, self.info_grid):
                    g.delete(*g.get_children())
                self.data_note.configure(text="(no DataFrame yet)")
            self._fill_vars(snap)

            if s["charts"] and not predicting:
                ch = s["charts"][0]
                self.chart_cap.configure(text=ch["caption"] + ("" if len(s["charts"]) == 1 else f"   (+{len(s['charts']) - 1} more)"))
                if ch["png"]:
                    try:
                        self._photo = png_to_photo(ch["png"], max(300, self.nb.winfo_width() - 40))
                        self.chart_lbl.configure(image=self._photo, text="")
                    except Exception:
                        self.chart_lbl.configure(image="", text=ch["caption"])
                else:
                    self.chart_lbl.configure(image="", text=ch["caption"])
                self.nb.select(3)
            else:
                self.chart_cap.configure(text="")
                self._photo = None
                self.chart_lbl.configure(image="", text="(no chart on this step)" if plt is not None
                                         else "Charts need matplotlib:  pip install matplotlib seaborn")
                if self.nb.index(self.nb.select()) == 3:
                    self.nb.select(0)

            out = (self.cum[k - 1] if k > 0 else "") if predicting else self.cum[k]
            self.out.configure(state="normal")
            self.out.delete("1.0", "end")
            self.out.insert("end", out if out.strip() else "(nothing printed yet)")
            if k == n - 1 and s["error"] and not predicting:
                self.out.insert("end", f"\n[stopped: {s['error']}]", "err")
            self.out.configure(state="disabled")
            self.out.see("end")

        def _explain_step(self, ex, s):
            if s["notes"]:
                ex.insert("end", "What this line uses\n", "h")
                for n in s["notes"]:
                    ex.insert("end", f"  - {n}\n")
            if s["error"]:
                ex.insert("end", "ERROR\n", "h")
                ex.insert("end", f"  {s['error']}\n", "bad")
            ex.insert("end", "What changed\n", "h")
            if s["changes"]:
                for ch in s["changes"]:
                    ex.insert("end", f"  {ch.strip()}\n" if not ch.startswith("   ") else f"      {ch.strip()}\n", "code")
            else:
                ex.insert("end", "  nothing: this line only LOOKS at the data\n", "dim")
            if s["printed"].strip():
                ex.insert("end", "Printed\n", "h")
                for ln in s["printed"].rstrip("\n").split("\n")[:12]:
                    ex.insert("end", f"  | {ln}\n", "code")
            if s["result_df"] is not None:
                ex.insert("end", "Result\n", "h")
                ex.insert("end", "  a table or Series: it is printed in the output box on the left\n", "dim")
            elif s["result"] is not None:
                ex.insert("end", "Result (what a notebook would display)\n", "h")
                for ln in s["result"].split("\n")[:14]:
                    ex.insert("end", f"  | {ln}\n", "code")
            for ch in s["charts"]:
                ex.insert("end", f"{ch['caption']}\n", "ok")
            if s["drawing"]:
                ex.insert("end", "(drawing on the chart... it appears when plt.show() runs)\n", "dim")

        def _fill_vars(self, snap):
            tree = self.var_grid
            tree.delete(*tree.get_children())
            cols = ("name", "kind", "summary")
            tree.configure(columns=cols)
            cw = F["bold"].measure("0")
            for c, txt, w in (("name", "Variable", 18), ("kind", "Kind", 12), ("summary", "Value / size", 50)):
                tree.heading(c, text=txt, anchor="w")
                tree.column(c, width=cw * w, minwidth=cw * 6, anchor="w", stretch=(c == "summary"))
            for name, (kind, v) in snap.items():
                if kind == "df":
                    tree.insert("", "end", values=(name, "DataFrame", f"{v.shape[0]} rows x {v.shape[1]} columns"))
                elif kind == "series":
                    tree.insert("", "end", values=(name, "Series", f"{len(v)} values, dtype {v.dtype}"))
                else:
                    tree.insert("", "end", values=(name, "value", v))

        def show_answer(self):
            q = self.q
            ans = "  /  ".join(q["answer"])
            messagebox.showinfo("Answer", f"Correct answer:\n{ans}\n\nWhy:\n{q['why']}", parent=self)


    # ===========================================================================
    # CHEAT SHEETS (live results computed by pandas) + calculators
    # ===========================================================================
    class CheatSheet(tk.Toplevel):
        def __init__(self, app, tab=None):
            super().__init__(app.root)
            self.app = app
            self.cache = {}
            self.title("Cheat sheets  -  pandas, stats formulas, CRISP-DM, data prep, business understanding")
            self.geometry("1180x860")
            self.minsize(880, 580)
            self.configure(bg=BG)
            top = ttk.Frame(self, padding=(14, 10, 14, 4))
            top.pack(fill="x")
            ttk.Label(top, text="Cheat sheets", font=F["h2"], foreground=HEAD).pack(side="left")
            app.theme_button(top).pack(side="right", padx=8)
            ttk.Button(top, text="A+", width=3, command=lambda: resize_fonts(1)).pack(side="right", padx=2)
            ttk.Button(top, text="A-", width=3, command=lambda: resize_fonts(-1)).pack(side="right", padx=2)
            tk.Label(self, bg=BG, fg=MUTED, font=F["ui"], anchor="w", justify="left", wraplength=1050,
                     text="Every result under the pandas toolkit was computed by pandas just now on the Megatelco sample, "
                          "so it can't be wrong. Use the Try-it box at the bottom to test your own expression."
                     ).pack(fill="x", padx=14)
            bar = ttk.Frame(self, padding=(14, 6))
            bar.pack(side="bottom", fill="x")
            row = ttk.Frame(bar)
            row.pack(fill="x")
            ttk.Label(row, text="Try it on", font=F["bold"]).pack(side="left")
            self.ds = ttk.Combobox(row, state="readonly", width=11, values=list(DATA))
            self.ds.set("megatelco")
            self.ds.pack(side="left", padx=6)
            self.entry = ttk.Entry(row, font=F["code"], width=44)
            self.entry.insert(0, "df['income'].median()")
            self.entry.pack(side="left", padx=6, fill="x", expand=True)
            self.entry.bind("<Return>", lambda e: self.run_try())
            ttk.Button(row, text="Evaluate", style="Accent.TButton", command=self.run_try).pack(side="left")
            rbox, self.result = ro_text(bar, 5, font=F["code"])
            self.result.tag_configure("bad", foreground=BAD)
            rbox.pack(fill="x", pady=(6, 0))
            self.nb = ttk.Notebook(self)
            self.nb.pack(fill="both", expand=True, padx=14, pady=8)
            self.pages, self.order = {}, []
            for tab_def in CHEAT_TABS:
                box, txt = ro_text(self.nb, 20, font=F["ui"], wrap="word")
                self.nb.add(box, text=tab_def["title"])
                self.pages[tab_def["key"]] = txt
                self.order.append(tab_def["key"])
                txt.tag_configure("h", font=F["h2"], foreground=HEAD, spacing1=16, spacing3=4)
                txt.tag_configure("colhead", font=F["bold"], foreground=MUTED, underline=True)
                txt.tag_configure("code", font=F["codeb"], foreground=SYN_DEF, spacing1=4)
                txt.tag_configure("res", font=F["code"], foreground=SYN_NUM)
                txt.tag_configure("err", font=F["code"], foreground=BAD)
                txt.tag_configure("note", font=F["ui"])
            self._build_calculators()
            self.render_all()
            self.run_try()
            if tab:
                self.select_tab(tab)
            APP["listeners"].append(self.render_all)
            self.bind("<Destroy>", self._on_destroy)
            self.bind("<Escape>", lambda e: self.destroy())
            self.bind("<Control-equal>", lambda e: resize_fonts(1))
            self.bind("<Control-minus>", lambda e: resize_fonts(-1))
            self.lift()

        def _on_destroy(self, e):
            if e.widget is self and self.render_all in APP["listeners"]:
                APP["listeners"].remove(self.render_all)

        def select_tab(self, key):
            if key in self.order:
                self.nb.select(self.order.index(key))
            elif key == "calc":
                self.nb.select(len(self.order))

        def render_all(self):
            for tab_def in CHEAT_TABS:
                self._fill(self.pages[tab_def["key"]], tab_def)

        def _eval(self, expr, dataset):
            key = (expr, dataset)
            if key not in self.cache:
                _, text, err = eval_expr_on(expr, dataset)
                self.cache[key] = (text.replace("\n", " | ")[:90], err)
            return self.cache[key]

        def _fill(self, txt, tab_def):
            cw = F["code"].measure("0")
            txt.configure(state="normal")
            txt.delete("1.0", "end")
            for bi, block in enumerate(tab_def["blocks"]):
                txt.insert("end", block["heading"] + "\n", "h")
                tabtag = f"tabs{bi}"
                if block["kind"] == "live":
                    txt.tag_configure(tabtag, lmargin1=8, lmargin2=40)
                    for expr, note in block["rows"]:
                        res, err = self._eval(expr, block["dataset"])
                        txt.insert("end", expr + "\n", ("code", tabtag))
                        if HAVE_PANDAS:
                            txt.insert("end", "    = ", ("note", tabtag))
                            txt.insert("end", (err.split(":")[0] if err else res) + "     ", ("err" if err else "res", tabtag))
                        else:
                            txt.insert("end", "    (install pandas to see the live result)     ", ("note", tabtag))
                        txt.insert("end", note + "\n", ("note", tabtag))
                else:
                    widths = block["widths"]
                    stops, acc = [], 0
                    for w in widths:
                        acc += w
                        stops.append(cw * acc)
                    txt.tag_configure(tabtag, tabs=tuple(stops), lmargin1=8, lmargin2=(stops[-1] if stops else 0) + 8)
                    txt.insert("end", "\t".join(block["cols"]) + "\n", ("colhead", tabtag))
                    for row in block["rows"]:
                        txt.insert("end", row[0], ("code", tabtag))
                        for cell in row[1:]:
                            txt.insert("end", "\t", tabtag)
                            txt.insert("end", cell, ("note", tabtag))
                        txt.insert("end", "\n", tabtag)
            txt.configure(state="disabled")

        # --- the Try-it box ------------------------------------------------------
        def run_try(self):
            _, text, err = eval_expr_on(self.entry.get(), self.ds.get())
            self.result.configure(state="normal")
            self.result.delete("1.0", "end")
            if err:
                self.result.insert("end", err, "bad")
            elif not text:
                self.result.insert("end", "type a pandas expression using df, e.g.  df['leave'].value_counts()   or   df.isnull().sum()")
            else:
                self.result.insert("end", text)
            self.result.configure(state="disabled")

        # --- calculators ---------------------------------------------------------
        def _build_calculators(self):
            page = ScrollFrame(self.nb)
            self.nb.add(page, text="calculators")
            f = page.body
            tk.Label(f, bg=BG, fg=MUTED, font=F["ui"], anchor="w", justify="left", wraplength=900,
                     text="Type numbers, press Enter. These use the same formulas as the course (pandas-style quartiles).").pack(fill="x")

            def box(title):
                lf = ttk.LabelFrame(f, text=title, padding=10)
                lf.pack(fill="x", pady=8)
                return lf

            # 1. describe my numbers
            lf = box("Describe my numbers  (mean, median, quartiles, IQR, outlier fences)")
            row = ttk.Frame(lf)
            row.pack(fill="x")
            self.nums = ttk.Entry(row, font=F["code"], width=50)
            self.nums.insert(0, "3, 7, 8, 9, 10, 10, 11, 12, 40")
            self.nums.pack(side="left", fill="x", expand=True)
            self.nums.bind("<Return>", lambda e: self.calc_describe())
            ttk.Button(row, text="Describe", style="Accent.TButton", command=self.calc_describe).pack(side="left", padx=8)
            self.desc_out = tk.Label(lf, text="", bg=BG, fg=TEXT, font=F["code"], anchor="w", justify="left", wraplength=1000)
            self.desc_out.pack(fill="x", pady=(6, 0))

            def three(title, labels, func, defaults):
                lf2 = box(title)
                row2 = ttk.Frame(lf2)
                row2.pack(fill="x")
                entries = []
                for lab, dv in zip(labels, defaults):
                    ttk.Label(row2, text=lab).pack(side="left", padx=(0, 4))
                    e = ttk.Entry(row2, width=10, font=F["code"])
                    e.insert(0, dv)
                    e.pack(side="left", padx=(0, 12))
                    entries.append(e)
                out = tk.Label(lf2, text="", bg=BG, fg=TEXT, font=F["code"], anchor="w", justify="left", wraplength=1000)

                def go(_=None):
                    try:
                        out.configure(text=func(*[float(e.get()) for e in entries]), fg=TEXT)
                    except ValueError:
                        out.configure(text="Enter plain numbers in every box.", fg=BAD)
                    except ZeroDivisionError:
                        out.configure(text="Can't divide by zero (check the std / range).", fg=BAD)
                for e in entries:
                    e.bind("<Return>", go)
                ttk.Button(row2, text="Calculate", style="Accent.TButton", command=go).pack(side="left")
                out.pack(fill="x", pady=(6, 0))
                go()

            three("IQR outlier fences", ["Q1", "Q3"],
                  lambda q1, q3: (f"IQR = Q3 - Q1 = {fmt_num(q3 - q1)}\n"
                                  f"lower fence = Q1 - 1.5 x IQR = {fmt_num(q1 - 1.5 * (q3 - q1))}\n"
                                  f"upper fence = Q3 + 1.5 x IQR = {fmt_num(q3 + 1.5 * (q3 - q1))}\n"
                                  f"anything below the lower or above the upper fence is an outlier"),
                  ["20", "40"])
            three("Z-score", ["value x", "mean", "std"],
                  lambda x, m, s: (f"z = (x - mean) / std = ({fmt_num(x)} - {fmt_num(m)}) / {fmt_num(s)} = {fmt_num((x - m) / s)}\n"
                                   f"so x is {fmt_num(abs((x - m) / s))} standard deviation(s) "
                                   f"{'above' if x >= m else 'below'} the mean"),
                  ["130", "100", "20"])
            three("Min-Max scaling", ["value x", "min", "max"],
                  lambda x, lo, hi: (f"scaled = (x - min) / (max - min) = ({fmt_num(x)} - {fmt_num(lo)}) / "
                                     f"({fmt_num(hi)} - {fmt_num(lo)}) = {fmt_num((x - lo) / (hi - lo))}"),
                  ["50", "0", "200"])
            self.calc_describe()

        def calc_describe(self):
            try:
                s = summarize_numbers(parse_floats(self.nums.get()))
            except (ValueError, ZeroDivisionError):
                self.desc_out.configure(text="Enter numbers separated by commas.", fg=BAD)
                return
            lines = [f"count {s['n']}    mean {fmt_num(s['mean'])}    median {fmt_num(s['median'])}    std {fmt_num(s['std'])}",
                     f"min {fmt_num(s['min'])}    Q1 {fmt_num(s['q1'])}    Q3 {fmt_num(s['q3'])}    max {fmt_num(s['max'])}    IQR {fmt_num(s['iqr'])}",
                     f"outlier fences: lower {fmt_num(s['lower'])}   upper {fmt_num(s['upper'])}",
                     "outliers: " + (", ".join(fmt_num(v) for v in s["outliers"]) if s["outliers"] else "none")]
            if s["mean"] > s["median"] * 1.15 and s["n"] > 2:
                lines.append("mean is well above the median -> right-skewed (a few big values pull the mean up)")
            self.desc_out.configure(text="\n".join(lines), fg=TEXT)



    # ===========================================================================
    # MAIN APP
    # ===========================================================================
    SHORT_TOPIC = {"W1": "Week 1", "W2": "Week 2", "W3": "Week 3", "W4": "Week 4", "W5": "Week 5", "W6": "Week 6",
                   "W7": "Week 7", "PY": "pandas code"}
    SKILL_TAB = {"pandas": "pandas", "missing": "pandas", "eda": "stats", "outliers": "stats", "models": "crisp",
                 "business": "biz", "types": "data", "transform": "data", "ethics": "crisp"}
    LAB_EXAMPLES = [
        ("Look at the data (Lab 2)", "megatelco", "df.head()\ndf.info()\ndf.describe()\ndf.isnull().sum()"),
        ("Find & fix missing values (Lab 6)", "megatelco",
         "print(df.isnull().sum().sum())\ndf['handset_price'] = df['handset_price'].fillna(df['handset_price'].median())\n"
         "df = df.dropna(subset=['income']).copy()\nprint(df.isnull().sum().sum())"),
        ("Outliers with the IQR (Lab 6)", "megatelco",
         "q1 = df['income'].quantile(0.25)\nq3 = df['income'].quantile(0.75)\niqr = q3 - q1\nlower = q1 - 1.5 * iqr\n"
         "upper = q3 + 1.5 * iqr\nprint(lower, upper)\ndf = df[(df['income'] >= lower) & (df['income'] <= upper)]\nprint(len(df))"),
        ("Group & compare (Lab 4)", "rent", "df.groupby('nhood')['price'].mean().sort_values(ascending=False).head(5)"),
        ("Types & categories (Labs 6/7)", "megatelco",
         "df['operating_system'] = df['operating_system'].astype('category')\n"
         "df['leave'] = df['leave'].map({'LEAVE': 1, 'STAY': 0})\ndf.dtypes"),
        ("Encode & bin (Lab 7)", "megatelco",
         "df['income_group'] = pd.qcut(df['income'], q=3, labels=['Low', 'Medium', 'High'])\n"
         "df_encoded = pd.get_dummies(df, columns=['operating_system'], prefix='os')\nprint(df_encoded.shape)\n"
         "df['income_group'].value_counts()"),
        ("A chart (Lab 5)", "spotifool", "plt.hist(df['downloads'], bins=10)\nplt.title('Downloads')\nplt.show()"),
        ("Validation checks (Week 6)", "fintrust",
         "print(df['Loan_ID'].duplicated().sum())\nprint((df['LoanAmount'] < 0).sum())\ndf[df['LoanAmount'] < 0]"),
    ]
    LETTER_KEYS = LETTERS


    def as_frame(obj):
        if isinstance(obj, pd.Series):
            name = obj.name if obj.name is not None else "value"
            return obj.to_frame(name=str(name))
        return obj


    class App:
        def __init__(self):
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass
            self.root = tk.Tk()
            self.root.title("IS 4487 - Business Analytics Midterm Trainer")
            self.root.geometry("1160x880")
            self.root.minsize(880, 680)
            self.root.report_callback_exception = self._report
            APP["root"] = self.root
            apply_palette(system_theme())
            make_fonts(self.root)
            style_app(self.root)
            self.mode, self.frame, self.scroller = "home", None, None
            self.wrap_labels, self.card_labels = [], []
            self.cheat = None
            self.shuffle_q = tk.BooleanVar(value=True)
            self.shuffle_c = tk.BooleanVar(value=True)
            self.pm_review = tk.BooleanVar(value=True)
            self.pm_ordered = tk.BooleanVar(value=True)
            self.exam_n = tk.IntVar(value=40)
            self.exam_end, self.clock_lbl, self._clock_job, self._time_up_shown = None, None, None, False
            self.items, self.i, self.answered = [], 0, False
            self.root.bind("<Key>", self._on_key)
            self.root.bind("<F2>", lambda e: self.open_lab())
            self.root.bind("<F3>", lambda e: self.open_cheat(self.cheat_tab_for(self.current_q())
                                                             if self.mode == "quiz" else None))
            self.root.bind("<Control-equal>", lambda e: resize_fonts(1))
            self.root.bind("<Control-minus>", lambda e: resize_fonts(-1))
            self.root.bind("<Configure>", self._on_resize)
            self.root.bind_all("<MouseWheel>", self._wheel)
            self.root.bind_all("<Button-4>", lambda e: self._wheel(e, 1))
            self.root.bind_all("<Button-5>", lambda e: self._wheel(e, -1))
            self.show_home()

        # --- helpers -----------------------------------------------------------
        def _report(self, exc, val, tb):
            """Show an unexpected error in a dialog instead of dying silently."""
            import traceback
            detail = "".join(traceback.format_exception(exc, val, tb))
            try:
                messagebox.showerror("Something went wrong", "The app hit an unexpected error but is still running.\n\n"
                                     + detail[-1500:])
            except Exception:
                pass

        def _wheel(self, e, direction=None):
            sc = self.scroller
            if sc is None or not sc.winfo_exists():
                return
            w = self.root.winfo_containing(e.x_root, e.y_root)
            if w is None or isinstance(w, (tk.Text, ttk.Treeview, tk.Listbox, ttk.Combobox)) or not str(w).startswith(str(sc)):
                return
            sc.scroll(direction * -1 if direction else int(-e.delta / 120))

        def theme_button(self, parent):
            btn = ttk.Button(parent, text=theme_button_text(), command=self.toggle_theme)
            btn._theme_btn = True
            return btn

        def toggle_theme(self):
            set_theme(self.root, "light" if CURRENT["name"] == "dark" else "dark")

        def clear(self, scroll=False):
            if self.frame is not None:
                self.frame.destroy()
            self.frame = ttk.Frame(self.root, padding=(24, 16))
            self.frame.pack(fill="both", expand=True)
            self.wrap_labels, self.card_labels, self.scroller = [], [], None
            self.clock_lbl = None
            if scroll:
                self.frame.configure(padding=0)
                sf = ScrollFrame(self.frame)
                sf.pack(fill="both", expand=True)
                self.scroller = sf
                return sf.body
            return self.frame

        def wlabel(self, parent, text, font=None, fg=None, bg=None, **kw):
            lbl = tk.Label(parent, text=text, font=font or F["ui"], fg=fg or TEXT, bg=bg or BG, justify="left",
                           anchor="w", **kw)
            self.wrap_labels.append(lbl)
            lbl.configure(wraplength=max(300, self.root.winfo_width() - 110))
            return lbl

        def _on_resize(self, e):
            if e.widget is self.root:
                for lbl in self.wrap_labels:
                    try:
                        lbl.configure(wraplength=max(300, e.width - 110))
                    except tk.TclError:
                        pass
                for lbl in self.card_labels:
                    try:
                        lbl.configure(wraplength=max(300, e.width - 190))
                    except tk.TclError:
                        pass

        def _typing(self):
            return isinstance(self.root.focus_get(), (tk.Text, tk.Entry, ttk.Entry, tk.Spinbox, ttk.Spinbox, ttk.Combobox))

        def _on_key(self, e):
            if self.mode == "flash" and not self._typing():
                if e.keysym == "space":
                    self.fc_flip()
                elif e.char.lower() == "y":
                    self.fc_grade(True)
                elif e.char.lower() == "n":
                    self.fc_grade(False)
                return
            if self.mode != "quiz" or self._typing():
                return
            ch = e.char.upper()
            if not self.answered and ch and ch in LETTERS[:len(self.cur_choices)]:
                self.select(LETTERS.index(ch))
            elif e.keysym in ("Return", "KP_Enter"):
                (self.next_q if self.answered else self.submit)()

        def current_q(self):
            if self.items and 0 <= self.i < len(self.items):
                it = self.items[self.i]
                return it if it.get("kind") != "essay" else None
            return None

        def cheat_tab_for(self, q):
            for sk in (q or {}).get("skills", []):
                if sk in SKILL_TAB:
                    return SKILL_TAB[sk]
            return None

        def open_cheat(self, tab=None):
            if self.cheat is not None and self.cheat.winfo_exists():
                self.cheat.lift()
                self.cheat.focus_force()
                if tab:
                    self.cheat.select_tab(tab)
                return
            self.cheat = CheatSheet(self, tab)

        def open_lab(self, code_text=None, data=None, setup=None, heading="free practice", q=None, tag="lab"):
            if not HAVE_PANDAS:
                messagebox.showinfo("The Code Lab needs pandas",
                                    "The Code Lab runs real pandas code, and pandas isn't installed.\n\nOpen a terminal and run:\n\n"
                                    f"    {INSTALL_HINT}\n\nThen start this trainer again. Everything else works without it.")
                return
            if code_text is None:
                cq = self.current_q() if self.mode == "quiz" else None
                if cq and cq["code"]:
                    code_text, data, setup, q, tag = cq["code"], cq["data"], cq["setup"], cq, cq["id"]
                    heading = f"{cq['id']}: {cq['prompt'].splitlines()[0]}"
                else:
                    name, data, code_text = LAB_EXAMPLES[0]
                    heading = "free practice - " + name
            CodeLab(self, code_text, data, setup, heading, q, tag)

        # --- home --------------------------------------------------------------
        def show_home(self):
            self.mode = "home"
            self._stop_clock()
            f = self.clear(scroll=True)
            head = ttk.Frame(f)
            head.pack(fill="x")
            ttk.Label(head, text="IS 4487  -  Business Analytics Midterm Trainer", font=F["h1"], foreground=HEAD).pack(side="left")
            self.theme_button(head).pack(side="right")
            self.wlabel(f, "Practice the midterm, drill any week, and step through pandas code in the Code Lab (F2). "
                           "Cheat sheets with live results and calculators are on F3.", fg=MUTED).pack(fill="x", pady=(2, 8))
            libs = library_status()
            if not HAVE_PANDAS:
                self.wlabel(f, "pandas isn't installed, so the quizzes work but the Code Lab is off. To turn it on, run:  "
                               + INSTALL_HINT, fg=BAD).pack(fill="x", pady=(0, 6))
            else:
                missing = [n for n, ok in libs if not ok]
                if missing:
                    self.wlabel(f, "Optional libraries not installed: " + ", ".join(missing) +
                                ".  Charts / MinMaxScaler demos need them:  " + INSTALL_HINT, fg=MUTED).pack(fill="x", pady=(0, 6))

            opts = ttk.LabelFrame(f, text="Options", padding=10)
            opts.pack(fill="x")
            ttk.Checkbutton(opts, text="Shuffle question order", variable=self.shuffle_q).grid(row=0, column=0, sticky="w", padx=6)
            ttk.Checkbutton(opts, text="Shuffle answer letters", variable=self.shuffle_c).grid(row=0, column=1, sticky="w", padx=6)
            ttk.Label(opts, text="Exam simulation questions:").grid(row=0, column=2, padx=(24, 4))
            ttk.Spinbox(opts, from_=10, to=len(BANK), width=5, textvariable=self.exam_n).grid(row=0, column=3)
            ttk.Checkbutton(opts, text="Practice Midterm: add the 5 review-page samples", variable=self.pm_review).grid(
                row=1, column=0, columnspan=2, sticky="w", padx=6, pady=(6, 0))
            ttk.Checkbutton(opts, text="Practice Midterm: keep the Canvas order", variable=self.pm_ordered).grid(
                row=1, column=2, columnspan=2, sticky="w", padx=(24, 0), pady=(6, 0))

            n = lambda g: sum(1 for q in BANK if q["group"] == g)  # noqa: E731
            grid = ttk.Frame(f)
            grid.pack(fill="x", pady=(14, 4))
            for c in range(3):
                grid.columnconfigure(c, weight=1, uniform="a")
            items = [
                (f"Practice Midterm\n{n('Practice Midterm') + 1} Canvas questions + {n('Review Page')} samples", self.start_practice_midterm),
                (f"Professor's Questions Only\n{len(PROF_QUESTIONS)} + 1 essay: Canvas exam and review page, shuffled", self.start_professor_only),
                (f"Concept Drills\n{n('Concepts')} questions, pick Weeks 1-7", self.show_concepts),
                (f"Code Reading\n{n('Code Reading')} pandas questions", lambda: self.start_pool(self.group("Code Reading"), "Code Reading")),
                (f"Business Cases\n{n('Business Cases')} case questions", lambda: self.start_pool(self.group("Business Cases"), "Business Cases")),
                ("EXAM SIMULATION\n40 questions + 2 essays, 60-minute clock", self.start_exam),
                ("Code Lab\nstep through any code question", self.show_lab_browser),
                ("Playground\nyour own pandas code, step by step", self.show_playground),
                (f"Short Essays\n{len(ESSAYS)} prompts with model answers", self.show_essay_menu),
                (f"Flashcards\n{len(FLASHCARDS)} key terms", self.show_flashcards),
                ("Weak Spots\nyour saved accuracy by topic", self.show_weak_spots),
                ("Cheat Sheets\npandas, formulas, calculators", self.open_cheat),
            ]
            for i, (txt, cmd) in enumerate(items):
                title, _, sub = txt.partition("\n")
                make_tile(grid, title, sub, f"B{i % 6 + 1}", cmd).grid(row=i // 3, column=i % 3, sticky="nsew", padx=6, pady=6)

            ttk.Label(f, text="PRACTICE BY SKILL  (drill what you mix up)", foreground=MUTED, font=F["bold"]).pack(anchor="w", pady=(10, 0))
            sgrid = ttk.Frame(f)
            sgrid.pack(fill="x", pady=(2, 8))
            for c in range(3):
                sgrid.columnconfigure(c, weight=1, uniform="s")
            for i, key in enumerate(SKILLS):
                cnt = sum(1 for q in BANK if key in q["skills"])
                make_tile(sgrid, SKILL_SHORT[key], f"{cnt} questions", f"B{(i + 3) % 6 + 1}",
                          lambda k=key: self.start_skill(k)).grid(row=i // 3, column=i % 3, sticky="nsew", padx=6, pady=6)
            ttk.Label(f, text="Tips:  F2 = Code Lab   |   F3 = cheat sheets   |   A-F = pick an answer   |   Enter = submit / next   |   Ctrl +/- = text size",
                      foreground=MUTED).pack(anchor="w")
            self.wlabel(f, f"Who wrote what: only {len(PROF_QUESTIONS)} questions plus the Q21 essay are your professor's (the Canvas practice "
                           "exam PM1-PM22 and the review-page samples RP1-RP5). They carry a purple PROFESSOR'S QUESTION tag. Everything "
                           "else carries a grey PRACTICE QUESTION tag: Claude wrote it, trying to match his style, but it is not an "
                           "actual exam question. Canvas never showed the answer key, so the keys for the professor's questions were "
                           "worked out from the readings and labs (the notes say so).",
                        fg=MUTED).pack(fill="x", pady=(6, 0))
            self.wlabel(f, "Code questions are checked by actually running them. Your accuracy is saved in one small file in your "
                           "home folder so Weak Spots can track it.", fg=MUTED).pack(fill="x", pady=(4, 0))

        # --- building quizzes ----------------------------------------------------------------
        @staticmethod
        def group(name):
            return [q for q in BANK if q["group"] == name]

        def maybe_shuffle(self, pool):
            return random.sample(pool, len(pool)) if self.shuffle_q.get() else list(pool)

        def start_pool(self, pool, title):
            self.start_quiz(self.maybe_shuffle(pool), title)

        def start_skill(self, key):
            self.start_pool([q for q in BANK if key in q["skills"]], SKILLS[key])

        def start_practice_midterm(self):
            pm = self.group("Practice Midterm")
            review = self.group("Review Page") if self.pm_review.get() else []
            essay = {"kind": "essay", "essay": ESSAYS[0], "id": "E1"}
            if self.pm_ordered.get():
                items = []
                for q in pm:
                    if q["id"] == "PM22":
                        items.append(essay)  # Canvas Q21 is the essay
                    items.append(q)
                items += review
            else:
                items = self.maybe_shuffle(pm + review) + [essay]
            self.start_quiz(items, "Practice Midterm")

        def start_professor_only(self):
            """Only the questions your professor wrote (Canvas practice exam + review page + the Q21 essay)."""
            essay = {"kind": "essay", "essay": ESSAYS[0], "id": "E1"}
            self.start_quiz(self.maybe_shuffle(PROF_QUESTIONS) + [essay], "Professor's Questions")

        def show_concepts(self):
            self.mode = "concepts"
            f = self.clear()
            top = ttk.Frame(f)
            top.pack(fill="x")
            ttk.Label(top, text="Concept Drills", font=F["h1"], foreground=HEAD).pack(side="left")
            ttk.Button(top, text="Home", command=self.show_home).pack(side="right")
            self.wlabel(f, "Tick the weeks you want to drill.", fg=MUTED).pack(fill="x", pady=(2, 8))
            self.week_vars = {}
            for k in TOPICS:
                if k == "PY":
                    continue
                cnt = sum(1 for q in BANK if q["topic"] == k and q["group"] != "Code Reading")
                v = tk.BooleanVar(value=True)
                self.week_vars[k] = v
                ttk.Checkbutton(f, text=f"{TOPICS[k]}   ({cnt} questions)", variable=v).pack(anchor="w", pady=3)
            ttk.Button(f, text="Start the drill", style="Accent.TButton", command=self.start_concepts).pack(anchor="w", pady=14)

        def start_concepts(self):
            chosen = [k for k, v in self.week_vars.items() if v.get()] or list(self.week_vars)
            self.start_pool([q for q in BANK if q["topic"] in chosen and q["group"] != "Code Reading"], "Concept Drill")

        def start_exam(self):
            try:
                n = max(10, min(len(BANK), int(self.exam_n.get())))
            except (tk.TclError, ValueError):
                n = 40
            cases = [q for q in BANK if q["group"] in ("Business Cases", "Practice Midterm", "Review Page")]
            rest = [q for q in BANK if q not in cases]
            k = min(len(cases), n // 2)
            pick = random.sample(cases, k) + random.sample(rest, min(len(rest), n - k))
            random.shuffle(pick)
            essays = [{"kind": "essay", "essay": e, "id": e["id"]} for e in random.sample(ESSAYS, 2)]
            self.start_quiz(pick + essays, "EXAM SIMULATION", exam=True)

        # --- exam clock ------------------------------------------------------------------------
        def _stop_clock(self):
            if self._clock_job is not None:
                try:
                    self.root.after_cancel(self._clock_job)
                except Exception:
                    pass
            self._clock_job = None

        def _tick_clock(self):
            self._clock_job = None
            if self.exam_end is None or self.mode not in ("quiz", "essay"):
                return
            left = self.exam_end - time.time()
            if self.clock_lbl is not None and self.clock_lbl.winfo_exists():
                if left > 0:
                    m, s = divmod(int(left), 60)
                    self.clock_lbl.configure(text=f"Time left {m:02d}:{s:02d}", fg=BAD if left < 600 else TEXT)
                else:
                    self.clock_lbl.configure(text="TIME'S UP", fg=BAD)
            if left <= 0 and not self._time_up_shown:
                self._time_up_shown = True
                messagebox.showinfo("Time's up", "The 60 minutes are over. On the real exam you would stop here; "
                                                 "you can keep going to finish the practice.")
            self._clock_job = self.root.after(1000, self._tick_clock)

        def _add_clock(self, parent):
            if self.exam_end is not None:
                self.clock_lbl = tk.Label(parent, text="", font=F["h2"], bg=BG, fg=TEXT)
                self.clock_lbl.pack(side="right", padx=14)
                self._stop_clock()
                self._tick_clock()

        # --- quiz ------------------------------------------------------------------------------
        def start_quiz(self, items, title, exam=False):
            if not items:
                messagebox.showinfo("Nothing to practice", "There are no questions for that selection.")
                return
            self.title_text = title
            self.items = list(items)
            self.i, self.score, self.answered_count = 0, 0, 0
            self.missed = []
            self.topic_stats, self.skill_stats, self.essay_log = {}, {}, []
            self.source_stats = {}
            self.started = time.time()
            self.exam_end = time.time() + 3600 if exam else None
            self._time_up_shown = False
            self.show_item()

        def show_item(self):
            it = self.items[self.i]
            if it.get("kind") == "essay":
                self.show_essay(it["essay"], in_quiz=True)
            else:
                self.show_question()

        def show_question(self):
            self.mode = "quiz"
            q = self.current_q()
            f = self.clear(scroll=True)
            self.answered, self.picks = False, set()
            choices = q["choices"][:]
            if self.shuffle_c.get() and q["kind"] != "tf":
                random.shuffle(choices)
            self.cur_choices = choices
            self.correct_idx = {i for i, c in enumerate(choices) if c in q["answer"]}

            info = ttk.Frame(f)
            info.pack(fill="x")
            ttk.Label(info, text=f"Question {self.i + 1} of {len(self.items)}   |   {q['id']}   |   {SHORT_TOPIC.get(q['topic'], q['topic'])}",
                      font=F["bold"], foreground=HEAD).pack(side="left")
            self.score_lbl = ttk.Label(info, text=self._score_text(), foreground=MUTED, font=F["bold"])
            self.score_lbl.pack(side="right")
            self._add_clock(info)
            bar = ttk.Frame(f)
            bar.pack(fill="x", pady=(6, 0))
            ttk.Button(bar, text="Code Lab  (F2)", style="Accent.TButton", command=self.open_lab).pack(side="right")
            ttk.Button(bar, text="Cheat sheets  (F3)",
                       command=lambda: self.open_cheat(self.cheat_tab_for(self.current_q()))).pack(side="right", padx=8)
            ttk.Button(bar, text="Home", command=self.confirm_home).pack(side="right")
            self.theme_button(bar).pack(side="right", padx=8)
            make_chip(bar, q).pack(side="left")
            self.wlabel(f, origin_note(q), fg=MUTED).pack(fill="x", pady=(6, 0))
            if q.get("skills"):
                self.wlabel(f, "Skills practiced:  " + "   |   ".join(SKILL_SHORT[x] for x in q["skills"]),
                            fg=MUTED).pack(fill="x", pady=(2, 0))
            ttk.Separator(f).pack(fill="x", pady=8)

            if q.get("context"):
                self.wlabel(f, q["context"], font=F["code"], fg=MUTED).pack(fill="x", pady=(0, 6))
            if q["data"]:
                self._data_toggle(f, q["data"])
            self.wlabel(f, q["prompt"], font=F["h2"]).pack(fill="x", pady=(0, 8))
            self.code_holder = ttk.Frame(f)
            self.code_holder.pack(fill="x")
            if q["code"]:
                self._show_code(self.code_holder, q["code"], "Code")
            if q["kind"] == "multi":
                self.wlabel(f, "Select ALL that apply, then press Submit.", fg=ACCENT, font=F["bold"]).pack(fill="x", pady=(6, 0))

            self.cards = []
            cf = ttk.Frame(f)
            cf.pack(fill="x", pady=10)
            for i, ch in enumerate(choices):
                card = tk.Frame(cf, bg=CARD, bd=1, relief="solid", cursor="hand2")
                card.pack(fill="x", pady=3)
                letter = tk.Label(card, text=LETTERS[i], font=F["h2"], bg=CARD, width=3, fg=ACCENT)
                letter.pack(side="left")
                body = tk.Label(card, text=ch, font=F["ui"], bg=CARD, fg=TEXT, justify="left", anchor="w",
                                wraplength=max(300, self.root.winfo_width() - 190))
                body.pack(side="left", fill="x", expand=True, pady=6)
                self.card_labels.append(body)
                for w in (card, letter, body):
                    w.bind("<Button-1>", lambda e, i=i: self.select(i))
                self.cards.append((card, letter, body))
            self.btn_row = ttk.Frame(f)
            self.btn_row.pack(fill="x", pady=4)
            self.submit_btn = ttk.Button(self.btn_row, text="Submit answer", style="Accent.TButton",
                                         command=self.submit, state="disabled")
            self.submit_btn.pack(side="left")
            ttk.Button(self.btn_row, text="Skip", command=self.skip).pack(side="left", padx=8)
            self.result_holder = ttk.Frame(f)
            self.result_holder.pack(fill="both", expand=True)

        def _data_toggle(self, parent, name):
            box = ttk.Frame(parent)
            box.pack(fill="x", pady=(0, 6))
            holder = ttk.Frame(box)
            state = {"open": False}
            btn = ttk.Button(box, text=f"Show the {name} data table")

            def toggle():
                if state["open"]:
                    holder.pack_forget()
                    btn.configure(text=f"Show the {name} data table")
                else:
                    if not holder.winfo_children():
                        g, tree = make_grid(holder, height=8)
                        g.pack(fill="x")
                        cols, rows = dataset_table(name)
                        fill_plain_grid(tree, cols, rows)
                    holder.pack(fill="x", pady=4)
                    btn.configure(text="Hide the data table")
                state["open"] = not state["open"]
            btn.configure(command=toggle)
            btn.pack(anchor="w")

        def _show_code(self, parent, text, heading):
            ttk.Label(parent, text=heading.upper(), foreground=MUTED, font=F["bold"]).pack(anchor="w")
            lines = text.split("\n")
            txt = tk.Text(parent, height=min(len(lines), 14), font=F["code"], bg=CARD, fg=TEXT, insertbackground=TEXT,
                          relief="solid", bd=1, highlightthickness=0, padx=8, pady=6, wrap="none")
            code_tags(txt)
            for n, line in enumerate(lines, 1):
                txt.insert("end", f"{n:>3} | {line}\n")
            highlight(txt, text, 6)
            txt.configure(state="disabled")
            txt.pack(fill="x", pady=(0, 6))

        def _score_text(self):
            return f"Score {self.score} / {self.answered_count}"

        def select(self, i):
            if self.answered:
                return
            q = self.current_q()
            if q["kind"] == "multi":
                self.picks ^= {i}
            else:
                self.picks = {i}
            for j, (card, letter, body) in enumerate(self.cards):
                col = SEL_BG if j in self.picks else CARD
                for w in (card, letter, body):
                    w.configure(bg=col)
            self.submit_btn.configure(state="normal" if self.picks else "disabled")

        def _color_cards(self):
            for j, (card, letter, body) in enumerate(self.cards):
                if j in self.correct_idx:
                    col = GOOD_BG
                elif j in self.picks:
                    col = BAD_BG
                else:
                    col = CARD
                for w in (card, letter, body):
                    w.configure(bg=col, cursor="arrow")

        def submit(self):
            if not self.answered and self.picks:
                self._finish_question(skipped=False)

        def skip(self):
            if not self.answered:
                self.picks = set()
                self._finish_question(skipped=True)

        def _section(self, parent, title):
            ttk.Label(parent, text=title, foreground=MUTED, font=F["bold"]).pack(anchor="w", pady=(12, 0))

        def _finish_question(self, skipped):
            q = self.current_q()
            self.answered = True
            for w in self.btn_row.winfo_children():
                w.destroy()
            correct = (not skipped) and self.picks == self.correct_idx
            letters = ", ".join(LETTERS[i] for i in sorted(self.correct_idx))
            if skipped:
                self.missed.append(q)
                msg, col = f"Skipped. The answer is {letters}.", MUTED
            else:
                self.answered_count += 1
                if correct:
                    self.score += 1
                    msg, col = "Correct!", GOOD
                else:
                    self.missed.append(q)
                    right_picked = len(self.picks & self.correct_idx)
                    msg = (f"Not quite. The answer is {letters}." if q["kind"] != "multi" else
                           f"Not quite: you found {right_picked} of {len(self.correct_idx)}. The answers are {letters}.")
                    col = BAD
                record(q["id"], correct)
            for key, table in (((q["topic"], self.topic_stats), (origin_of(q), self.source_stats))
                               + tuple((s, self.skill_stats) for s in q["skills"])):
                st = table.setdefault(key, [0, 0])
                st[1] += 1
                st[0] += 1 if correct else 0
            self.score_lbl.configure(text=self._score_text())
            self._color_cards()
            last = self.i == len(self.items) - 1
            tk.Label(self.btn_row, text=msg, font=F["h2"], fg=col, bg=BG, wraplength=700, justify="left").pack(side="left", padx=(0, 16))
            ttk.Button(self.btn_row, text="See results" if last else "Next  >", style="Accent.TButton",
                       command=self.next_q).pack(side="left")
            if q["code"]:
                ttk.Button(self.btn_row, text="Step through it in the Code Lab", command=self.open_lab).pack(side="left", padx=8)
            tab = self.cheat_tab_for(q)
            if tab:
                ttk.Button(self.btn_row, text="Open the cheat sheet", command=lambda: self.open_cheat(tab)).pack(side="left")
            self._learning_panel(q, skipped, correct)

        def _learning_panel(self, q, skipped, correct):
            rf = self.result_holder
            self._section(rf, "WHY THE RIGHT ANSWER IS RIGHT")
            self.wlabel(rf, q["why"]).pack(fill="x")
            if q["source"]:
                self.wlabel(rf, "Source: " + q["source"], fg=MUTED).pack(fill="x")

            if not correct:
                picked = [self.cur_choices[i] for i in sorted(self.picks)]
                if q["kind"] == "multi" and not skipped:
                    missed, extra = multi_feedback(q, picked)
                    self._section(rf, "WHAT YOU GOT WRONG")
                    if missed:
                        self.wlabel(rf, "You missed:  " + "  |  ".join(missed), fg=BAD).pack(fill="x")
                    for ch, why in diagnose(q, picked):
                        self.wlabel(rf, "You also chose:  " + ch, fg=BAD, font=F["bold"]).pack(fill="x", pady=(4, 0))
                        self.wlabel(rf, why or "That option isn't one of the correct answers (see the explanation above).", fg=MUTED).pack(fill="x")
                elif picked:
                    self._section(rf, f"WHY YOUR ANSWER ({LETTERS[min(self.picks)]}) ISN'T RIGHT")
                    self.wlabel(rf, "You picked:  " + picked[0], font=F["bold"]).pack(fill="x")
                    note = diagnose(q, picked)[0][1] if diagnose(q, picked) else ""
                    self.wlabel(rf, note or "Compare it with the explanation above" +
                                (", then step through the code in the Code Lab to see exactly what happens." if q["code"] else "."),
                                ).pack(fill="x", pady=(2, 0))

            if q["code"]:
                self._code_results(rf, q)

            others = [(i, ch) for i, ch in enumerate(self.cur_choices) if i not in self.correct_idx and i not in self.picks]
            notes = TRAPS.get(q["id"], {})
            reasons = [(i, ch, notes[ch]) for i, ch in others if ch in notes]
            if reasons:
                holder = ttk.Frame(rf)
                state = {"open": False}
                btn = ttk.Button(rf, text="Show why the other wrong options are wrong")

                def toggle():
                    if state["open"]:
                        holder.pack_forget()
                        btn.configure(text="Show why the other wrong options are wrong")
                    else:
                        if not holder.winfo_children():
                            for i, ch, why in reasons:
                                self.wlabel(holder, f"{LETTERS[i]})  " + ch.replace("\n", "  |  "), font=F["bold"]).pack(fill="x", pady=(6, 0))
                                self.wlabel(holder, why, fg=MUTED).pack(fill="x")
                        holder.pack(fill="x", pady=4)
                        btn.configure(text="Hide the other options")
                    state["open"] = not state["open"]
                btn.configure(command=toggle)
                btn.pack(anchor="w", pady=(12, 0))

            cards = related_flashcards(q)
            if cards:
                self._section(rf, "KEY TERMS TO REVIEW")
                for term, defn in cards:
                    self.wlabel(rf, term, font=F["bold"], fg=HEAD).pack(fill="x", pady=(4, 0))
                    self.wlabel(rf, defn, fg=MUTED).pack(fill="x")

        def _code_results(self, rf, q):
            if not HAVE_PANDAS:
                self._section(rf, "RUNNING THAT CODE")
                self.wlabel(rf, "Install pandas to see this code run on the real lab data:  " + INSTALL_HINT, fg=MUTED).pack(fill="x")
                return
            wait = tk.Label(rf, text="Running that code on the lab data...", bg=BG, fg=MUTED, font=F["ui"])
            wait.pack(anchor="w", pady=(10, 0))
            self.root.update_idletasks()
            res = quick_run(q)
            wait.destroy()
            self._section(rf, "RUNNING THAT CODE ON THE REAL LAB DATA GIVES")
            if res["text"].strip():
                lines = res["text"].split("\n")
                box, txt = ro_text(rf, min(10, len(lines) + 1), font=F["code"], wrap="none")
                txt.tag_configure("bad", foreground=BAD)
                txt.configure(state="normal")
                txt.insert("end", "\n".join(lines[:40]), "bad" if "ERROR" in res["text"] else ())
                txt.configure(state="disabled")
                box.pack(fill="x")
            for obj in res["frames"]:
                try:
                    g, tree = make_grid(rf, height=min(8, len(obj) + 1))
                    g.pack(fill="x", pady=(6, 0))
                    fill_df_grid(tree, as_frame(obj))
                except Exception:
                    pass
            self._imgs = []
            for ch in res["charts"][:2]:
                if ch["png"]:
                    try:
                        img = png_to_photo(ch["png"], max(300, self.root.winfo_width() - 160))
                        lbl = tk.Label(rf, image=img, bg=BG)
                        lbl.image = img
                        lbl.pack(anchor="w", pady=6)
                        self._imgs.append(img)
                    except Exception:
                        pass
                self.wlabel(rf, ch["caption"], fg=MUTED).pack(fill="x")
            lines = narrate_steps(res["steps"])
            if lines:
                self._section(rf, "WHAT THE CODE DOES, STEP BY STEP (IN WORDS)")
                box, txt = ro_text(rf, min(len(lines) + 1, 12), font=F["ui"])
                txt.configure(state="normal")
                txt.insert("end", "\n".join(lines))
                txt.configure(state="disabled")
                box.pack(fill="x")

        def next_q(self):
            if not self.answered:
                return
            if self.i >= len(self.items) - 1:
                self.show_results()
            else:
                self.i += 1
                self.show_item()

        def confirm_home(self):
            if messagebox.askyesno("Leave?", "Go back to the home screen? Your progress in this session will be lost."):
                self.show_home()


        # --- essays ------------------------------------------------------------------------------
        def show_essay(self, e, in_quiz=False):
            self.mode = "essay"
            f = self.clear(scroll=True)
            info = ttk.Frame(f)
            info.pack(fill="x")
            label = f"Item {self.i + 1} of {len(self.items)}   |   " if in_quiz else ""
            ttk.Label(info, text=f"{label}Short essay {e['id']}   ({e['source']})", font=F["bold"], foreground=HEAD).pack(side="left")
            if in_quiz:
                self._add_clock(info)
            bar = ttk.Frame(f)
            bar.pack(fill="x", pady=(6, 0))
            ttk.Button(bar, text="Home", command=self.confirm_home if in_quiz else self.show_home).pack(side="right")
            ttk.Button(bar, text="Cheat sheets  (F3)", command=lambda: self.open_cheat()).pack(side="right", padx=8)
            self.theme_button(bar).pack(side="right")
            item = {"kind": "essay", "id": e["id"]}
            make_chip(bar, item).pack(side="left")
            self.wlabel(f, origin_note(item), fg=MUTED).pack(fill="x", pady=(6, 0))
            ttk.Separator(f).pack(fill="x", pady=8)
            self.wlabel(f, e["prompt"], font=F["h2"]).pack(fill="x", pady=(0, 8))
            self.wlabel(f, "Write 100 words or less. The checker looks for key points (by keyword), so use the course vocabulary.",
                        fg=MUTED).pack(fill="x")
            ebox = ttk.Frame(f)
            ebox.pack(fill="x", pady=8)
            ed = tk.Text(ebox, height=9, font=F["ui"], bg=CARD, fg=TEXT, insertbackground=TEXT, relief="solid", bd=1,
                         highlightthickness=0, padx=8, pady=6, wrap="word", undo=True)
            ed.pack(fill="x")
            counter = tk.Label(f, text="0 words", bg=BG, fg=MUTED, font=F["bold"], anchor="w")
            counter.pack(fill="x")

            def update(_=None):
                words = len(re.findall(r"\b\w+\b", ed.get("1.0", "end-1c")))
                counter.configure(text=f"{words} words" + ("   (over the 100-word limit!)" if words > 100 else ""),
                                  fg=BAD if words > 100 else (GOOD if words else MUTED))
            ed.bind("<KeyRelease>", update)
            result = ttk.Frame(f)
            row = ttk.Frame(f)
            row.pack(fill="x", pady=8)
            state = {"checked": False}

            def check():
                for w in result.winfo_children():
                    w.destroy()
                ans = ed.get("1.0", "end-1c").strip()
                low = " " + ans.lower()
                self._section(result, "KEY POINTS THE GRADER WILL LOOK FOR")
                hit = 0
                for lab, keys in e["points"]:
                    ok = bool(ans) and any(k in low for k in keys)
                    hit += ok
                    tk.Label(result, text=("[x]  " if ok else "[  ]  ") + lab, bg=BG, fg=GOOD if ok else BAD,
                             font=F["ui"], anchor="w", justify="left").pack(fill="x")
                self.wlabel(result, f"You covered {hit} of {len(e['points'])} (a keyword check only, so judge for yourself too).",
                            fg=MUTED).pack(fill="x", pady=(4, 0))
                self._section(result, "MODEL ANSWER")
                self.wlabel(result, e["model"]).pack(fill="x")
                self.wlabel(result, f"({len(e['model'].split())} words)", fg=MUTED).pack(fill="x")
                result.pack(fill="x")
                if ans and not state["checked"]:
                    record(e["id"], hit >= len(e["points"]) - 1)
                    self.essay_log.append((e["id"], hit, len(e["points"]))) if in_quiz else None
                state["checked"] = True
            ttk.Button(row, text="Check my answer", style="Accent.TButton", command=check).pack(side="left")
            ttk.Button(row, text="Show the model answer", command=check).pack(side="left", padx=8)
            if in_quiz:
                last = self.i == len(self.items) - 1
                ttk.Button(row, text="See results" if last else "Continue  >", command=self._essay_next).pack(side="left")
            else:
                ttk.Button(row, text="Another essay", command=self.show_essay_menu).pack(side="left")

        def _essay_next(self):
            if self.i >= len(self.items) - 1:
                self.show_results()
            else:
                self.i += 1
                self.show_item()

        def show_essay_menu(self):
            self.mode = "essaymenu"
            f = self.clear()
            top = ttk.Frame(f)
            top.pack(fill="x")
            ttk.Label(top, text="Short Essays", font=F["h1"], foreground=HEAD).pack(side="left")
            ttk.Button(top, text="Home", command=self.show_home).pack(side="right")
            self.wlabel(f, "Double-click an essay prompt to practice it (100 words or less).", fg=MUTED).pack(fill="x", pady=(2, 8))
            tree = ttk.Treeview(f, columns=("id", "prompt"), show="headings", height=10)
            tree.heading("id", text="Essay")
            tree.heading("prompt", text="Prompt")
            tree.column("id", width=70, stretch=False)
            tree.column("prompt", width=860)
            for i, e in enumerate(ESSAYS):
                tree.insert("", "end", iid=str(i), values=(e["id"], e["prompt"][:110] + ("..." if len(e["prompt"]) > 110 else "")))
            tree.pack(fill="both", expand=True)

            def go(_=None):
                sel = tree.selection()
                if sel:
                    self.items, self.i = [], 0
                    self.essay_log = []
                    self.show_essay(ESSAYS[int(sel[0])])
            tree.bind("<Double-1>", go)
            ttk.Button(f, text="Practice the selected essay", style="Accent.TButton", command=go).pack(anchor="w", pady=10)

        # --- results ---------------------------------------------------------------------------
        def show_results(self):
            self._stop_clock()
            self.mode = "results"
            f = self.clear(scroll=True)
            top = ttk.Frame(f)
            top.pack(fill="x")
            ttk.Label(top, text="Results", font=F["h1"], foreground=HEAD).pack(side="left")
            self.theme_button(top).pack(side="right")
            if self.answered_count:
                pct = round(100 * self.score / self.answered_count)
                ttk.Label(f, text=f"{self.score} / {self.answered_count} answered correctly  ({pct}%)", font=F["h2"]).pack(anchor="w", pady=6)
            mins = (time.time() - self.started) / 60
            ttk.Label(f, text=f"Time: {mins:.1f} minutes" + ("   (the real exam is 60)" if self.exam_end else ""), foreground=MUTED).pack(anchor="w")
            if self.essay_log:
                ttk.Label(f, text="Essays: " + ",  ".join(f"{i}: {h}/{t} key points" for i, h, t in self.essay_log),
                          foreground=MUTED).pack(anchor="w")
            weak = []
            sources = {"prof": "Professor's questions", "claude": "Practice questions (written by Claude)"}
            for title, stats, names, bad_keys in (("BY SOURCE", getattr(self, "source_stats", {}), sources, None),
                                                  ("BY TOPIC", self.topic_stats, TOPICS, None),
                                                  ("BY SKILL  (red = your weak spots)", self.skill_stats, SKILLS, weak)):
                if not stats:
                    continue
                ttk.Label(f, text=title, foreground=MUTED, font=F["bold"]).pack(anchor="w", pady=(10, 2))
                for key in names:
                    if key not in stats:
                        continue
                    good, total = stats[key]
                    low = good / total < 0.75
                    if low and bad_keys is not None:
                        bad_keys.append(key)
                    tk.Label(f, text=f"{good}/{total}   {names[key][:70]}", font=F["ui"], bg=BG, anchor="w",
                             fg=GOOD if good == total else (BAD if low else TEXT)).pack(fill="x")
            ttk.Label(f, text="MISSED OR SKIPPED  (double-click to open the code in the Code Lab)", foreground=MUTED,
                      font=F["bold"]).pack(anchor="w", pady=(12, 2))
            tree = ttk.Treeview(f, columns=("t", "p"), show="headings", height=8)
            tree.heading("t", text="Question")
            tree.heading("p", text="Prompt")
            tree.column("t", width=110, stretch=False)
            tree.column("p", width=700)
            for idx, q in enumerate(self.missed):
                tree.insert("", "end", iid=str(idx), values=(q["id"], q["prompt"].split("\n")[0][:120]))
            tree.pack(fill="x")

            def open_sel(_=None):
                sel = tree.selection()
                if sel:
                    q = self.missed[int(sel[0])]
                    if q["code"]:
                        self.open_lab(q["code"], q["data"], q["setup"], f"{q['id']}: {q['prompt'].splitlines()[0]}", q, q["id"])
            tree.bind("<Double-1>", open_sel)
            row = ttk.Frame(f)
            row.pack(fill="x", pady=12)
            ttk.Button(row, text="Code Lab on selected", style="Accent.TButton", command=open_sel).pack(side="left")
            if self.missed:
                ttk.Button(row, text="Retry missed questions",
                           command=lambda: self.start_quiz(self.maybe_shuffle(self.missed[:]), "Retry")).pack(side="left", padx=8)
            if weak:
                ttk.Button(row, text="Practice my weak skills",
                           command=lambda: self.start_pool([q for q in BANK if any(k in q["skills"] for k in weak)], "Weak skills")
                           ).pack(side="left")
            ttk.Button(row, text="Home", command=self.show_home).pack(side="right")

        # --- weak spots (saved progress) -------------------------------------------------------
        def show_weak_spots(self):
            self.mode = "weak"
            f = self.clear(scroll=True)
            top = ttk.Frame(f)
            top.pack(fill="x")
            ttk.Label(top, text="Weak Spots", font=F["h1"], foreground=HEAD).pack(side="left")
            ttk.Button(top, text="Home", command=self.show_home).pack(side="right")
            self.theme_button(top).pack(side="right", padx=8)
            tried = {q["id"]: PROGRESS[q["id"]] for q in BANK if isinstance(PROGRESS.get(q["id"]), dict) and PROGRESS[q["id"]].get("tries")}
            if not tried:
                self.wlabel(f, "No history yet. Take a quiz first, then come back here to see your accuracy by topic.", fg=MUTED).pack(fill="x", pady=10)
                return
            self.wlabel(f, f"Your accuracy across all sessions ({sum(r['tries'] for r in tried.values())} answers saved in {PROGRESS_FILE}).",
                        fg=MUTED).pack(fill="x", pady=(2, 6))
            for title, key_of, names in (("BY TOPIC", lambda q: [q["topic"]], TOPICS), ("BY SKILL", lambda q: q["skills"], SKILLS)):
                stats = {}
                for q in BANK:
                    r = tried.get(q["id"])
                    if r:
                        for k in key_of(q):
                            s = stats.setdefault(k, [0, 0])
                            s[0] += r["right"]
                            s[1] += r["tries"]
                ttk.Label(f, text=title + "   (lowest first)", foreground=MUTED, font=F["bold"]).pack(anchor="w", pady=(10, 2))
                for k, (right, n) in sorted(stats.items(), key=lambda kv: kv[1][0] / kv[1][1]):
                    pct = 100 * right / n
                    bar = "#" * int(pct / 5) + "." * (20 - int(pct / 5))
                    tk.Label(f, text=f"{pct:5.1f}%   {bar}   {names[k].split(':')[0][:38]}   ({n} tries)", font=F["code"], bg=BG, anchor="w",
                             fg=GOOD if pct >= 80 else (TEXT if pct >= 60 else BAD)).pack(fill="x")
            wrong = [q for q in BANK if q["id"] in tried and tried[q["id"]].get("last") is False]
            row = ttk.Frame(f)
            row.pack(fill="x", pady=14)
            self.wlabel(f, f"{len(wrong)} question(s) you got wrong the last time you saw them.", fg=MUTED).pack(fill="x")
            if wrong:
                ttk.Button(row, text="Drill those now", style="Accent.TButton",
                           command=lambda: self.start_pool(wrong, "Weak Spots")).pack(side="left")
            ttk.Button(row, text="Reset my saved progress", command=self.reset_progress).pack(side="left", padx=8)

        def reset_progress(self):
            if messagebox.askyesno("Reset progress", "Erase all saved accuracy and flashcard progress?"):
                PROGRESS.clear()
                save_progress(PROGRESS)
                self.show_weak_spots()

        # --- flashcards ------------------------------------------------------------------------
        def show_flashcards(self, only_new=None):
            self.mode = "flash"
            known = known_cards()
            if only_new is None:
                only_new = getattr(self, "fc_only_new", tk.BooleanVar(value=False)).get() if hasattr(self, "fc_only_new") else False
            deck = [(t, d) for t, d in FLASHCARDS if not (only_new and t in known)]
            random.shuffle(deck)
            self.fc_deck, self.fc_i, self.fc_shown, self.fc_missed = deck, 0, False, []
            self.fc_only_new_flag = only_new
            self._draw_flash()

        def _draw_flash(self):
            f = self.clear()
            top = ttk.Frame(f)
            top.pack(fill="x")
            ttk.Label(top, text="Flashcards", font=F["h1"], foreground=HEAD).pack(side="left")
            ttk.Button(top, text="Home", command=self.show_home).pack(side="right")
            self.theme_button(top).pack(side="right", padx=8)
            known = known_cards()
            ttk.Label(f, text=f"{len(known)} of {len(FLASHCARDS)} cards marked as known (saved).   Keys: Space = reveal,  Y = I knew it,  N = not yet",
                      foreground=MUTED).pack(anchor="w", pady=(2, 8))
            var = tk.BooleanVar(value=self.fc_only_new_flag)
            self.fc_only_new = var
            ttk.Checkbutton(f, text="Only cards I haven't mastered", variable=var,
                            command=lambda: self.show_flashcards(only_new=var.get())).pack(anchor="w")
            if self.fc_i >= len(self.fc_deck):
                self.wlabel(f, f"Deck finished!  {len(self.fc_deck) - len(self.fc_missed)} known, {len(self.fc_missed)} to review.",
                            font=F["h2"]).pack(fill="x", pady=20)
                if self.fc_missed:
                    ttk.Button(f, text="Go through the ones I missed", style="Accent.TButton",
                               command=self._flash_retry).pack(anchor="w")
                ttk.Button(f, text="Shuffle and start again", command=lambda: self.show_flashcards(only_new=var.get())).pack(anchor="w", pady=8)
                return
            term, defn = self.fc_deck[self.fc_i]
            self.wlabel(f, f"Card {self.fc_i + 1} of {len(self.fc_deck)}", fg=MUTED).pack(fill="x", pady=(14, 0))
            card = tk.Frame(f, bg=CARD, bd=1, relief="solid", padx=24, pady=26)
            card.pack(fill="x", pady=10)
            self.wrap_labels.append(tk.Label(card, text=term, font=F["h1"], bg=CARD, fg=HEAD, justify="left", anchor="w",
                                             wraplength=900))
            self.wrap_labels[-1].pack(fill="x")
            self.fc_def = tk.Label(card, text="(try to say the definition out loud first)", font=F["ui"], bg=CARD, fg=MUTED,
                                   justify="left", anchor="w", wraplength=900)
            self.fc_def.pack(fill="x", pady=(14, 0))
            self.fc_card_defn = defn
            row = ttk.Frame(f)
            row.pack(fill="x", pady=8)
            self.fc_flip_btn = ttk.Button(row, text="Show the definition  (Space)", style="Accent.TButton", command=self.fc_flip)
            self.fc_flip_btn.pack(side="left")
            self.fc_yes = ttk.Button(row, text="I knew it  (Y)", command=lambda: self.fc_grade(True), state="disabled")
            self.fc_no = ttk.Button(row, text="Not yet  (N)", command=lambda: self.fc_grade(False), state="disabled")
            self.fc_yes.pack(side="left", padx=8)
            self.fc_no.pack(side="left")
            self.fc_shown = False

        def fc_flip(self):
            if self.mode != "flash" or self.fc_i >= len(self.fc_deck) or self.fc_shown:
                return
            self.fc_shown = True
            self.fc_def.configure(text=self.fc_card_defn, fg=TEXT)
            self.fc_yes.configure(state="normal")
            self.fc_no.configure(state="normal")
            self.fc_flip_btn.configure(state="disabled")

        def fc_grade(self, knew):
            if self.mode != "flash" or self.fc_i >= len(self.fc_deck) or not self.fc_shown:
                return
            term = self.fc_deck[self.fc_i][0]
            set_card_known(term, knew)
            if not knew:
                self.fc_missed.append(self.fc_deck[self.fc_i])
            self.fc_i += 1
            self._draw_flash()

        def _flash_retry(self):
            self.fc_deck, self.fc_i, self.fc_missed = self.fc_missed[:], 0, []
            self._draw_flash()

        # --- code lab browser ------------------------------------------------------------------
        def show_lab_browser(self):
            self.mode = "labs"
            f = self.clear()
            top = ttk.Frame(f)
            top.pack(fill="x")
            ttk.Label(top, text="Code Lab", font=F["h1"], foreground=HEAD).pack(side="left")
            ttk.Button(top, text="Home", command=self.show_home).pack(side="right")
            self.wlabel(f, "Double-click a question to run its code one line at a time on the real lab data. "
                           "Each step shows exactly which rows, columns, types and missing values changed.", fg=MUTED).pack(fill="x", pady=(2, 8))
            srow = ttk.Frame(f)
            srow.pack(fill="x")
            ttk.Label(srow, text="Filter:").pack(side="left")
            flt = tk.StringVar()
            ttk.Entry(srow, textvariable=flt, width=34, font=F["ui"]).pack(side="left", padx=6)
            tree = ttk.Treeview(f, columns=("id", "prompt", "data", "code"), show="headings")
            for col, w, txt in (("id", 70, "Question"), ("prompt", 380, "Prompt"), ("data", 110, "Dataset"), ("code", 360, "First line of code")):
                tree.heading(col, text=txt)
                tree.column(col, width=w)
            sb = ttk.Scrollbar(f, command=tree.yview)
            tree.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y", pady=8)
            tree.pack(fill="both", expand=True, pady=8)
            qs = [q for q in BANK if q["code"]]

            def fill(*_):
                tree.delete(*tree.get_children())
                needle = flt.get().lower()
                for i, q in enumerate(qs):
                    row = (q["id"], q["prompt"].split("\n")[0][:60], q["data"] or "-", q["code"].split("\n")[0][:60])
                    if needle in " ".join(row).lower() or needle in q["code"].lower():
                        tree.insert("", "end", iid=str(i), values=row)
            flt.trace_add("write", fill)
            fill()

            def go(_=None):
                sel = tree.selection()
                if sel:
                    q = qs[int(sel[0])]
                    self.open_lab(q["code"], q["data"], q["setup"], f"{q['id']}: {q['prompt'].splitlines()[0]}", q, q["id"])
            tree.bind("<Double-1>", go)
            tree.bind("<Return>", go)
            ttk.Button(f, text="Step through the selected code", style="Accent.TButton", command=go).pack(anchor="w")

        # --- playground ------------------------------------------------------------------------
        def show_playground(self):
            self.mode = "playground"
            f = self.clear()
            top = ttk.Frame(f)
            top.pack(fill="x")
            ttk.Label(top, text="Playground", font=F["h1"], foreground=HEAD).pack(side="left")
            ttk.Button(top, text="Home", command=self.show_home).pack(side="right")
            self.theme_button(top).pack(side="right", padx=8)
            self.wlabel(f, "Type or paste pandas code, choose which dataset is loaded as df, then step through it. "
                           "pd, np, plt and sns are already imported.", fg=MUTED).pack(fill="x", pady=(2, 8))
            row = ttk.Frame(f)
            row.pack(fill="x", pady=(0, 6))
            ttk.Label(row, text="df =").pack(side="left")
            ds = ttk.Combobox(row, state="readonly", width=12, values=list(DATA))
            ds.set("megatelco")
            ds.pack(side="left", padx=6)
            ex = ttk.Combobox(row, state="readonly", width=36, values=[n for n, _, _ in LAB_EXAMPLES])
            ex.set("Load an example...")
            ex.pack(side="right")
            box = ttk.Frame(f)
            box.pack(fill="both", expand=True)
            ed = tk.Text(box, font=F["code"], bg=CARD, fg=TEXT, insertbackground=TEXT, relief="solid", bd=1, undo=True,
                         padx=8, pady=6, wrap="none", highlightthickness=0)
            sbar = ttk.Scrollbar(box, command=ed.yview)
            ed.configure(yscrollcommand=sbar.set)
            sbar.pack(side="right", fill="y")
            ed.pack(fill="both", expand=True)
            code_tags(ed)
            ed.insert("1.0", LAB_EXAMPLES[1][2])
            ds.set(LAB_EXAMPLES[1][1])
            pending = []

            def recolor_editor(_=None):
                pending.clear()
                highlight(ed, ed.get("1.0", "end-1c"), 0)

            def schedule(_=None):
                if not pending:
                    pending.append(ed.after(120, recolor_editor))

            def on_tab(_):
                ed.insert("insert", "    ")
                return "break"

            def on_return(_):
                line = ed.get("insert linestart", "insert")
                indent = line[:len(line) - len(line.lstrip())]
                if line.rstrip().endswith(":"):
                    indent += "    "
                ed.insert("insert", "\n" + indent)
                ed.see("insert")
                schedule()
                return "break"

            def load_example(_):
                for name, d, src in LAB_EXAMPLES:
                    if name == ex.get():
                        ed.delete("1.0", "end")
                        ed.insert("1.0", src)
                        ds.set(d)
                        recolor_editor()
            ed.bind("<KeyRelease>", schedule)
            ed.bind("<Tab>", on_tab)
            ed.bind("<Return>", on_return)
            ex.bind("<<ComboboxSelected>>", load_example)
            recolor_editor()

            def run():
                src = ed.get("1.0", "end-1c").strip("\n")
                if src.strip():
                    self.open_lab(src, ds.get(), None, "Playground", None, "playground")
            bar = ttk.Frame(f)
            bar.pack(fill="x", pady=10)
            ttk.Button(bar, text="Step through this code", style="Accent.TButton", command=run).pack(side="left")
            ttk.Label(bar, text="(use the |> button in the Code Lab to jump to the end)", foreground=MUTED).pack(side="left", padx=10)

        def run(self):
            self.root.mainloop()



# ===========================================================================
# Entry point
# ===========================================================================
def entry():
    if sys.version_info < (3, 8):
        print("This trainer needs Python 3.8 or newer. You have " + sys.version.split()[0] + ".")
        return
    if not HAVE_TK:
        print("tkinter isn't available in this Python, so the window can't open. "
              "Reinstall Python from python.org and keep 'tcl/tk and IDLE' ticked.")
        return
    try:
        App().run()
    except tk.TclError as e:
        print(f"The window could not open ({e}).")


if __name__ == "__main__":
    entry()
