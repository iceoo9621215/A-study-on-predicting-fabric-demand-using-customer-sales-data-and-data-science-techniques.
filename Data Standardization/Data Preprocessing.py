import itertools
import time
import warnings
import re
import numpy as np
import pandas as pd
from tqdm import trange
from multiprocessing import Pool


# Parameter setting
warnings.filterwarnings('ignore')
ecode = 'utf-8-sig'
c = 'Color'
m = 'Material'

# Permutations color or material
def combinations(color_material):
    color_material_combine = []
    for i_cm in itertools.combinations(color_material, 2):
        color_material_combine.append(i_cm)
    return color_material_combine


# CJK and Latin Letters Cleaner
def CJK_cleaner(string):
    # Remove special chars, keep English letters, numbers, and CJK Unified Ideographs.(CJK Unified Ideographs)
    # Characters and Codes List:
    #   0-9              Digits (ASCII printable characters)
    #   a-z              Basic Latin Letters   (ASCII printable characters)
    #   A-Z              Basic Latin Letters   (ASCII printable characters)
    #   ƒ (\u83)         Latin Letters Extened (ASCII extended characters)
    #   Š (\u8a)         Latin Letters Extened (ASCII extended characters)
    #   Œ (\u8c)         Latin Letters Extened (ASCII extended characters)
    #   Ž (\u8e)         Latin Letters Extened (ASCII extended characters)
    #   š (\u9a)         Latin Letters Extened (ASCII extended characters)
    #   œ (\u9c)         Latin Letters Extened (ASCII extended characters)
    #   ž (\u9e)         Latin Letters Extened (ASCII extended characters)
    #   Ÿ (\u9f)         Latin Letters Extened (ASCII extended characters)
    #   \uc0-\ud6        Latin Letters Extened (ASCII extended characters)
    #   \ud8-\uf6        Latin Letters Extened (ASCII extended characters)
    #   \uf8-\uff        Latin Letters Extened (ASCII extended characters)
    #   \u100-\u17f      European Latin (Latin Extended-A)
    #   \u4e00-\u9fff    CJK Unified Ideographs (中日韓統一表意文字)
    #   \u3040-\u309f    Hiragana (平假名)
    #   \u30a0-\u30ff    Katakana (片假名)
    #   \u3130-\u318f    Korean language and computers (Hangul Compatibility Jamo 韓文)
    #   \uff00-\uffef    Halfwidth and Fullwidth Forms (半形及全形字符)
    filters = re.compile(
        u"[^0-9a-zA-Z\u0083\u008a\u008c\u008e\u009a\u009c\u009e\u009f\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff\u0100-\u017f\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\u3130-\u318f\uff00-\uffef]+",
        re.UNICODE)
    return filters.sub('', string)  # remove special characters


# Function define
def evaluation(thestr):
    return eval(thestr)


# Score integers are converted to strings for subsequent program execution
def rate_replace(i_star):
    print(str(time.ctime()) + ' start process ' + 'Score integers are converted to strings')
    # Score integers are converted to strings for subsequent program execution
    comment_data[i_star]['商品規格'] = comment_data[i_star]['商品規格'].str.replace('$', '')
    rate = [5, 4, 3, 2, 1]
    rate_r: list[str] = ['5', '4', '3', '2', '1']
    for rat in range(len(rate_r)):
        comment_data[i_star]['給星'] = comment_data[i_star]['給星'].replace(rate[rat], rate_r[rat])  # replace rating
    print(str(time.ctime()) + ' Finish: converted to strings')


# Material Definition and Replacement
def Material_Definition_and_Replacement(i_mat):
    print(str(time.ctime()) + ' start process ' + 'Material Definition and Replacement')
    for i1 in trange(len(comment_data[i_mat]['商品文案']), desc='CJK and Latin Letters Cleaner'):
        try:
            str_or = CJK_cleaner(comment_data[i_mat]['商品文案'][i1])
            comment_data[i_mat]['商品文案'][i1] = comment_data[i_mat]['商品文案'][i1].replace(
                comment_data[i_mat]['商品文案'][i1], str_or)
        except:
            continue
    # define the name of the replacement
    materials: list[str] = ['\'纖維\'', 'polyester', '聚酯纤维', 'wool', '吸濕排汗,', '\'None\'', '\'其他\'',
                            '說明', 'POLYESTER', 'SPANDEX', '吸濕排汗', '雪紡', '針織', '卡其', '涤纶', '滌綸',
                            '針織', '冰絲', 'Polyester排汗布', '細緻排汗布', '刷毛']
    replace2: list[str] = ['\'聚脂纖維\'', '聚脂纖維', '聚脂纖維', '羊毛', '', '', '', '', '聚脂纖維', '彈性纖維',
                           '聚脂纖維', '聚脂纖維', '聚脂纖維', '92%聚酯纖維 8%彈力纖維', '聚脂纖維', '聚脂纖維',
                           '聚脂纖維', '粘膠纖維', '聚脂纖維', '聚脂纖維', 'Polartec']
    for mat in range(len(materials)):
        comment_data[i_mat]['規格'] = comment_data[i_mat]['規格'].str.replace(materials[mat], replace2[mat])
        comment_data[i_mat]['商品文案'] = comment_data[i_mat]['商品文案'].str.replace(materials[mat], replace2[mat])
    print(str(time.ctime()) + ' Finish: Material Replacement')


# Color Definition and Replacement
def Replace_special_color(i_col):
    print(str(time.ctime()) + ' start process ' + 'Color Definition and Replacement')
    # Replace special color
    Special_color: list[str] = ['深灰', '熒光綠', '軍綠色', '酒紅', '深藍', '墨綠', '粉橘', '紫粉', '棗紅', '寶藍',
                                '卡其', '迷彩', '奶茶', '太妃糖', '紫羅蘭', '莫蘭迪']
    release_item: list[str] = ['1#', '2#', '3#', '4#', '5#', '6#', '7#', '8#', '9#', '10#', '11#', '12#', '13#',
                               '14#', '15#', '16#']
    for spe_color in range(len(Special_color)):
        comment_data[i_col]['商品規格'] = comment_data[i_col]['商品規格'].str.replace(Special_color[spe_color],
                                                                                      release_item[spe_color])
    # Replace Chinese characters that can express colors
    express_colors = ['赤', '桃紅', '粉色', '薰衣草', '丈青色', 'Black', 'White', 'Gray', '粉紅']
    release_color = ['紅', '桃', '粉', '紫色', '藏青', '黑', '白', '灰', '粉']
    for release_ch in range(len(express_colors)):
        comment_data[i_col]['商品規格'] = comment_data[i_col]['商品規格'].str.replace(express_colors[release_ch],
                                                                                      release_color[release_ch])
    print(str(time.ctime()) + ' Finish: Color Definition and Replacement')


# Material column judgment and processing
def Material_column_judgment_and_processing(i_judgment):
    print(str(time.ctime()) + ' start process ' + 'Material column judgment and processing')
    # Specifications No information
    No_Material = comment_data[i_judgment][comment_data[i_judgment]['規格'] == '[]']
    # Rearrange index and divide string
    No_Material.reset_index(drop=True, inplace=True)
    No_Material['規格'] = No_Material['規格'].str.replace('[', '')
    No_Material['規格'] = No_Material['規格'].str.replace(']', '')
    # Define the material to look for
    index_s: list[str] = ['聚酯纖維', '羊毛', '彈力纖維', '合成材質', '尼龍', '氨綸', '冰絲', '陽離子',
                          'UPF30UP', 'Polartec® Power Stretch Pro®', 'FlashDry', '聚脂纖維', 'Polyester', 'Polartec']
    index: list[str] = ['聚酯纖維', '羊毛', '彈力纖維', '合成材質', '尼龍', '氨綸', '冰絲', '陽離子',
                        'UPF30UP', 'Polartec® Power Stretch Pro®', 'FlashDry', '聚酯纖維', '聚酯纖維', 'Polartec']
    # judgment and processing
    for mat_judgment in trange(len(index), position=0, desc='judgment'):
        # Determine whether there is a material
        # judgment_mat: object = No_Material['商品文案'].str.contains(index[mat_judgment])
        for mat_process in range(len(No_Material)):
            try:
                judgment_mat = re.search(index_s[mat_judgment], No_Material['商品文案'][mat_process])
            except:
                change = str(No_Material['商品文案'][mat_process])
                judgment_mat = re.search(index[mat_judgment], change)
            if judgment_mat:
                No_Material['規格'][mat_process] = No_Material['規格'][mat_process].replace(
                    No_Material['規格'][mat_process], No_Material['規格'][mat_process] + index[mat_judgment] + '/')
    No_Material['規格'] = No_Material['規格'].replace('', '未提供材質')
    # Material and non-material Combine
    # Specifications have information
    includesMaterial = comment_data[i_judgment][comment_data[i_judgment]['規格'] != '[]']
    includesMaterial['規格'] = includesMaterial['規格'].str.replace('\' 纖維\'', '\'聚酯纖維\'')
    includesMaterial['規格'] = includesMaterial['規格'].str.replace('\'纖維\'', '\'聚酯纖維\'')
    includesMaterial['規格'] = includesMaterial['規格'].str.replace('[', ',')
    includesMaterial['規格'] = includesMaterial['規格'].str.replace(']', '')
    includesMaterial['規格'] = includesMaterial['規格'].str.replace('\'', '')
    comment_data[i_judgment] = pd.concat([No_Material, includesMaterial], axis=0)
    comment_data[i_judgment].reset_index(drop=True, inplace=True)  # Rearrange index
    print(str(time.ctime()) + ' Finish: Material_column_judgment_and_processing')


# Add materials & Rate to product specifications
def Data_divide_ADD_PREPARE(p_add):
    global div_col, col_1, col_2
    print(str(time.ctime()) + ' start process ' + 'Add materials & Rate to product specifications(need long times)')
    # Prepare Process
    div_col = comment_data[p_add]['商品規格'].str.split('\'', expand=True)  # cut string
    div_col = div_col.iloc[:, [col % 2 == 1 for col in range(len(div_col.columns))]]  # delete invalid columns
    col_1 = list(div_col.columns)
    col_2 = col_1[1:]


def Add_materials_to_product_specifications(i_add):
    # Replace Columns
    for i1 in range(len(col_1)):
        print('Steps1 Progress: ' + str(i1 + 1) + '/' + str(len(col_1)))
        for i2 in trange(len(div_col[col_1[i1]]), position=0, desc='Step1'):
            if div_col[col_1[i1]][i2] is not None:
                div_col[col_1[i1]][i2] = div_col[col_1[i1]][i2].replace(div_col[col_1[i1]][i2], div_col[col_1[i1]][i2]
                                                                        + comment_data[i_add]['規格'][i2]
                                                                        + '$' + comment_data[i_add]['給星'][i2]
                                                                        + '$' + str(
                    comment_data[i_add]['留言時間'][i2]))
                div_col[col_1[i1]][i2] = div_col[col_1[i1]][i2].replace(div_col[col_1[i1]][i2], '\''
                                                                        + div_col[col_1[i1]][i2] + '\'')
    for i3 in range(len(col_2)):
        print('Steps2 Progress: ' + str(i3 + 1) + '/' + str(len(col_1)))
        for i4 in trange(len(div_col[col_1[i3]]), position=0, desc='Step2'):
            if div_col[col_2[i3]][i4] is not None:
                div_col[col_1[0]][i4] = div_col[col_1[0]][i4].replace(div_col[col_1[0]][i4], div_col[col_1[0]][i4] + ','
                                                                      + div_col[col_2[i3]][i4])
    comment_data[i_add]['商品規格'] = div_col[1]
    comment_data[i_add]['商品規格'] = '[' + comment_data[i_add]['商品規格'].map(str) + ']'
    print(str(time.ctime()) + ' Finish: Add materials & Rate to product specifications')


# Merge all the products purchased by consumers into one list
def Merge_all_the_products_purchased_by_consumers_into_one_list(apply_good):
    print(str(time.ctime()) + ' start process ' + 'Merge all the products purchased by consumers into one list')
    global All_Good
    # Insert the data content of the dataframe into the method
    comment_data[apply_good]['商品規格'] = comment_data[apply_good]['商品規格'].apply(evaluation)
    # Merge all the products purchased by consumers into one list
    All_Good = np.sum(comment_data[apply_good]['商品規格'])
    print(str(time.ctime()) + ' Finish: Merge all the products purchased by consumers into one list')


# Handle purchase date, rating field data
def Handle_purchase_date_rating_field_data():
    print(str(time.ctime()) + ' start process ' + 'Handle purchase date, rating field data')
    global Buyer_date, Rating
    date = pd.DataFrame(All_Good)
    date = date[0].str.split('$', expand=True)
    Buyer_date = date[2]
    Rating = date[1]
    print(str(time.ctime()) + ' Finish: Handle purchase date, rating field data')


# statistics Color or Material
def Statistics(color_or_material, output_columns, type_s, Permutations_cm):
    print(str(time.ctime()) + ' start process ' + 'statistics Color or Material')
    Amount = []
    Type = []
    co = []
    for s in trange(len(All_Good)):
        container = []
        Type.append(name[type_s])
        co.append(1)
        for c_m in color_or_material:
            col_mat = str.__contains__(All_Good[s], c_m)
            try:
                if col_mat:
                    container.append(1)
                else:
                    container.append(0)
            except:
                container.append(0)
        listSum = sum(container)
        if listSum > 1:
            for c1_m1 in range(len(color_or_material)):
                container[c1_m1] = 0
            for c2_m2 in Permutations_cm:
                cm1 = str.__contains__(All_Good[s], c2_m2[0])
                cm2 = str.__contains__(All_Good[s], c2_m2[1])
                if cm1 is True and cm2 is True:
                    col_mat = True
                else:
                    col_mat = False
                try:
                    if col_mat:
                        container.append(1)
                    else:
                        container.append(0)
                except:
                    container.append(0)
        else:
            for c2_m2 in range(len(Permutations_cm)):
                container.append(0)
        listSum = sum(container)
        if listSum == 0:
            container.append(1)
        else:
            container.append(0)
        if listSum > 1:
            container.append(1)
            for c_m_1 in range(len(color_or_material + Permutations_cm)):
                container[c_m_1] = 0
        else:
            container.append(0)
        Amount.append(container)
    cm_st = pd.DataFrame(Amount)
    cm_st.columns = output_columns
    Type = pd.DataFrame(Type)
    co = pd.DataFrame(co)
    co = co.rename(columns={0: 'Sum'})
    Type = Type.rename(columns={0: 'Type'})
    print(str(time.ctime()) + ' Finish: statistics Color or Material')
    return cm_st, Type, co


# Count the number of colors/material
def Count_the_number_of_colors_or_material(buyer_color_or_material: object, buyer_list: object, input_c_or_m: object,
                                           count_i: object) -> object:
    print(str(time.ctime()) + ' start process ' + 'Count the number of colors/material')
    buyer_sum = buyer_color_or_material
    t_buyer = buyer_sum.T
    c_m_t = []
    for t1 in range(len(t_buyer.columns)):
        for t2 in range(len(t_buyer.index)):
            if t_buyer[t1][t2] == 1:
                c_m_t.append(buyer_list[t2])
    buyer_sum = pd.DataFrame(c_m_t)  # Finished color or material table
    buyer_sum = buyer_sum.rename(columns={0: input_c_or_m})
    # Calculate the total
    Amount_cm = []  # Quantity of each color
    cm_list = []  # color/material list
    type_list = []  # category list
    for cm in range(len(buyer_list)):
        sum_c_m = np.sum(buyer_sum == buyer_list[cm])  # Count the total number of comments
        Amount_cm.append(sum_c_m)
        cm_list.append(buyer_list[cm])
        type_list.append(name[count_i])
    Amount_cm = pd.DataFrame(Amount_cm)
    Amount_cm = Amount_cm.rename(columns={input_c_or_m: 'Sum_' + input_c_or_m})
    cm_list = pd.DataFrame(cm_list)
    cm_list = cm_list.rename(columns={0: input_c_or_m})
    type_list = pd.DataFrame(type_list)
    type_list = type_list.rename(columns={0: 'Type_' + input_c_or_m})
    print(str(time.ctime()) + ' Finish: Count the number of colors/material')
    return buyer_sum, Amount_cm, cm_list, type_list


# Make machine_learning_table
def machine_learning_table(list_color, list_material, rate, date, Type, due_month, AC, i_expend, year, month):
    print(str(time.ctime()) + ' start process ' + 'machine_learning_table')
    # Data Input
    original_data = pd.concat([Type, date, list_color, list_material, rate, AC], axis=1)
    original_data = original_data.rename(columns={2: 'Date', 1: 'Rate'})
    original_data['Date'] = pd.to_datetime(original_data['Date'])
    original_data = original_data.set_index('Date')
    # Produce Date List
    year = year
    month = month
    list_Date = []
    for i1 in range(due_month):
        while month > 12:
            year += 1
            month = 1
        date_list = str(year) + '-' + str(month)
        month += 1
        list_Date.append(date_list)
    Type_e = []
    Color = []
    Material = []
    Date = []
    rate_a = []
    Sum = []
    rate_item = ['5', '4', '3', '2', '1']
    for data_p in trange(len(list_Date), position=0):
        process = original_data[list_Date[data_p]]
        for cc in color_output_columns_Permutations:
            for mm in material_output_columns_Permutations:
                for ra in rate_item:
                    process_cm = process[(process['Color'] == cc) & (process['Material'] == mm)
                                         & (process['Rate'] == ra)]
                    Type_e.append(name[i_expend])
                    Date.append(list_Date[data_p])
                    Color.append(cc)
                    Material.append(mm)
                    rate_a.append(ra)
                    Sum.append(np.sum(process_cm['Sum']))
    Type_e = pd.DataFrame(Type_e)
    Type_e = Type_e.rename(columns={0: 'Type'})
    Color = pd.DataFrame(Color)
    Color = Color.rename(columns={0: 'Color'})
    Material = pd.DataFrame(Material)
    Material = Material.rename(columns={0: 'Material'})
    Date = pd.DataFrame(Date)
    Date = Date.rename(columns={0: 'Date'})
    rate_a = pd.DataFrame(rate_a)
    rate_a = rate_a.rename(columns={0: 'Rate'})
    Sum = pd.DataFrame(Sum)
    Sum = Sum.rename(columns={0: 'Y'})
    All = pd.concat([Type_e, Color, Material, Date, rate_a, Sum], axis=1)
    print('Finish(machine_learning_table)-' + name[i_expend])
    return All


# Import Comment Data(Test and Train)
data_type = '1'  # data type(0 = test, 1 = train)
if data_type == '0':
    container_comment1 = pd.read_csv(
        'Input Data/Test/2023-02-04排汗衣_留言資料.csv')
    container_comment2 = pd.read_csv(
        'Input Data/Test/2023-02-04涼感衣_留言資料.csv')
    container_comment3 = pd.read_csv(
        'Input Data/Test/2023-02-05發熱衣_留言資料.csv')
    container_comment4 = pd.read_csv(
        'Input Data/Test/2023-02-05防風防水外套_留言資料.csv')
else:
    container_comment1 = pd.read_csv(
        'Input Data/Train/2023-01-05排汗衣_留言資料.csv')
    container_comment2 = pd.read_csv(
        'Input Data/Train/2023-01-05涼感衣_留言資料.csv')
    container_comment3 = pd.read_csv(
        'Input Data/Train/2023-01-06發熱衣_留言資料.csv')
    container_comment4 = pd.read_csv(
        'Input Data/Train/2023-01-07防風防水外套_留言資料.csv')
comment_data = [container_comment1, container_comment2, container_comment3, container_comment4]
name = ['Perspiration Clothing', 'Cool Clothes', 'Heating Suit', 'Windproof and Waterproof Jacket']
print(str(time.ctime()) + ' The data import is complete and data processing begins')


# Data Stander(Process Include: Sales time select, Missing data, Remove Unavailable Columns)
def Data_Standardization(import_data, Type):
    # Drop duplicates data
    a = len(comment_data[import_data])
    repeat = comment_data[import_data].drop_duplicates()  # 刪除重複值（所有行都一樣，即刪除）
    b = len(repeat)
    comment_data[import_data] = repeat
    print('Delete Comment Data Count：' + str(a - b))
    # 一般時間 datetime 與 Unix時間互轉
    if Type == 'test':
        t = 1672502400
    else:
        t = 1609430400
    a = len(comment_data[import_data])  # Calculate the number of data before deletion
    comment_data[import_data] = comment_data[import_data][
        comment_data[import_data]['留言時間'] >= t]  # Filter >=20210101 ,1609430400 # 1672502400(2023/1/1)
    comment_data[import_data]['留言時間'] = pd.to_datetime(comment_data[import_data]['留言時間'],
                                                           unit='s')  # 將UNIX 時間轉換為時間軸
    b = len(comment_data[import_data])  # Calculate the number of deleted data
    print(Type + '刪除留言的資料筆數：' + str(a - b))  # 顯示刪除資料總數

    # Remove unnecessary fields
    comment_data[import_data].pop("使用者ID")
    comment_data[import_data].pop("是否匿名")
    comment_data[import_data].pop("是否隱藏")
    comment_data[import_data].pop("訂單編號")
    comment_data[import_data].pop("留言內容")
    comment_data[import_data].dropna(axis=0, how='all')
    B = len(comment_data[import_data])
    print(b - B)


# Define colors/ Material and calculate sums (Add Combination Expand List-2023-01)
# Process Color
color = ['黑', '白', '灰', '綠', '粉', '膚', '橘', '藍', '紫色', '咖啡色', '焦糖', '桃', '紅', '黃', '藏青', '杏',
         '1#', '2#', '3#', '4#', '5#', '6#', '7#', '8#', '9#', '10#', '11#', '12#', '13#', '14#', '15#', '16#']
# Combination Expand List_Color
color_Permutations = combinations(color)
# Process Output Columns
color_output_columns = ['Black', 'White', 'Gray', 'Green', 'Pink', 'skin', 'Orange', 'Blue', 'Purple', 'Brown',
                        'Caramel Colour', 'Peach', 'Red', 'Yellow', 'Navy Blue', 'Apricot', 'Dark Gray',
                        'Fluorescent Green', 'ArmyGreen', 'Wine Red', 'Dark Blue', 'Dark Green', 'Pink Orange',
                        'Purple Pink', 'Claret', 'Sapphire', 'Khaki', 'Camouflage', 'Milk Tea', 'Taffy', 'Violets',
                        'Morandi']

# Process Output Columns Combination_Color
color_output_columns_Permutations = combinations(color_output_columns)
color_output_columns_Permutations_list = []
for columns_l in color_output_columns_Permutations:
    columns_2 = columns_l[0] + ' and ' + columns_l[1]
    color_output_columns_Permutations_list.append(columns_2)
color_output_columns_Permutations = color_output_columns + color_output_columns_Permutations_list
color_output_columns_Permutations.append('Not find Color')
color_output_columns_Permutations.append('Multi-color(over two color)')
# Process Material
material = ['聚酯纖維', '羊毛', '彈力纖維', '合成材質', '尼龍', '氨綸', '粘膠纖維', '陽離子', 'UPF30UP', '棉',
            'FlashDry', 'Polartec']
# Combination Expand List_Material
material_Permutations = combinations(material)
material_output_columns = ['Polyester', 'Wool', 'Elastic Fibers', 'Synthetic Material', 'Nylon', 'Spandex',
                           'Viscose fiber', 'CATION', 'UPF30UP', 'cotton', 'FlashDry', 'Polartec']
material_output_columns_Permutations = combinations(material_output_columns)
material_output_columns_Permutations_list = []
for columns_l in material_output_columns_Permutations:
    columns_2 = columns_l[0] + ' and ' + columns_l[1]
    material_output_columns_Permutations_list.append(columns_2)
material_output_columns_Permutations = material_output_columns + material_output_columns_Permutations_list
material_output_columns_Permutations.append('Not find Material')
material_output_columns_Permutations.append('Multi-Material(over two material)')


# Start timing and start processing data
def standardization(i):
    print(str(time.ctime()) + ' start process ' + name[i])
    table_type = 'train'
    # Data Standardization
    # If you are entering test data, enter 'test' as the second parameter, other data can be any string.
    Data_Standardization(i, table_type)
    # Score integers are converted to strings for subsequent program execution
    rate_replace(i)
    # Material Definition and Replacement
    Material_Definition_and_Replacement(i)
    # Replace special color
    Replace_special_color(i)
    # Material column judgment and processing
    Material_column_judgment_and_processing(i)
    # Add materials & Rate to product specifications
    Data_divide_ADD_PREPARE(i)
    Add_materials_to_product_specifications(i)
    # Merge all the products purchased by consumers into one list
    Merge_all_the_products_purchased_by_consumers_into_one_list(i)
    # Handle purchase date, rating field data
    Handle_purchase_date_rating_field_data()
    # color statistics
    buyer, Type_C, count = Statistics(color, color_output_columns_Permutations, i, color_Permutations)
    buyer, sc, lc, tc = Count_the_number_of_colors_or_material(buyer, color_output_columns_Permutations, c, i)
    # Material Statistics
    buyer2, Type_M, count2 = Statistics(material, material_output_columns_Permutations, i, material_Permutations)
    buyer2, sm, lm, tm = Count_the_number_of_colors_or_material(buyer2, material_output_columns_Permutations, m, i)

    # tableau Output
    # c_buy = pd.concat([tc, lc, sc], axis=1)  # Color_Summary (tableau use)2023.02_Remove
    # M_buy = pd.concat([tm, lm, sm], axis=1)  # Material_Summary (tableau use)2023.02_Remove
    if table_type != 'test':
        tableau = pd.concat([Type_C, buyer, buyer2, Buyer_date, Rating], axis=1)  # Material + Color Table (tableau use)
        tableau = tableau.rename(columns={2: 'Date', 1: 'Rate'})
        tableau_Remove_None = tableau[
            (tableau['Color'] != 'Not find Color') & (tableau['Material'] != 'Not find Material')]
        tableau_Remove_None.to_csv(
            "/Users/xuyuteng/PycharmProjects/Shopee Crawler/Color and Material Form/Output/tableau/{0}_Table.csv".format(
                name[i]), index=False, encoding=ecode)
    # Make Machine Learning Table
    if table_type != 'test':
        ML_TABLE = machine_learning_table(buyer, buyer2, Rating, Buyer_date, Type_C, 24, count, i, 2021,
                                          1)  # Train table
    else:
        ML_TABLE = machine_learning_table(buyer, buyer2, Rating, Buyer_date, Type_C, 1, count, i, 2023, 1)  # Test table
    ML_Remove0 = ML_TABLE[(ML_TABLE['Y'] > 0)]
    ML_TABLE_N0_NC_NM = ML_Remove0[(ML_Remove0['Color'] != 'Not find Color') &
                                   (ML_Remove0['Material'] != 'Not find Material')]
    if table_type != 'test':
        ML_TABLE.to_csv(
            "/Users/xuyuteng/PycharmProjects/Shopee Crawler/Color and Material Form/Output/ML/Train/{0}_Table_all.csv".format(
                name[i]), index=False, encoding=ecode)
        ML_TABLE_N0_NC_NM.to_csv(
            "/Users/xuyuteng/PycharmProjects/Shopee Crawler/Color and Material Form/Output/ML/Train/{0}_Table.csv".format(
                name[i]), index=False, encoding=ecode)
    else:
        ML_TABLE.to_csv(
            "/Users/xuyuteng/PycharmProjects/Shopee Crawler/Color and Material Form/Output/ML/Test/{0}_Table_all.csv".format(
                name[i]), index=False, encoding=ecode)
        ML_TABLE_N0_NC_NM.to_csv(
            "/Users/xuyuteng/PycharmProjects/Shopee Crawler/Color and Material Form/Output/ML/Test/{0}_Table.csv".format(
                name[i]), index=False, encoding=ecode)
    print('-----------' + name[i] + 'Finish-----------')


if __name__ == '__main__':
    inputs = [0, 1, 2, 3]
    # Set the number of handlers
    pool = Pool(4)
    # Run multiprocessing
    pool_output = pool.map(standardization, inputs)
