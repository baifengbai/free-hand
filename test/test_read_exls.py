import xlrd

path = r'E:\Note\中证500.xls'
data = xlrd.open_workbook(path).sheet_by_index(0)
rows = data.nrows
columns = data.ncols

for i in range(1, rows-1):
    lis = data.row_values(i, 0)
    sql = "INSERT INTO `data_usable_database`.`tb_stocks_500` (`name`, `code`) VALUES ('{}', '{}');".format(lis[0], lis[1])
    cdb = Contraler_Database('data_usable_database')
    cdb.insertData2DB(sql)
