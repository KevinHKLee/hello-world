import xlsxwriter

workbook = xlsxwriter.Workbook('upward_feedback_report.xlsx')
worksheet = workbook.add_worksheet('Jacky')

worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 24)

border_format=workbook.add_format({
                            'border':1
                           })
worksheet.conditional_format( 'A8:D14' , { 'type' : 'no_blanks' , 'format' : border_format} )
worksheet.conditional_format( 'A16:C16' , { 'type' : 'no_blanks' , 'format' : border_format} )
worksheet.conditional_format( 'A19:C23' , { 'type' : 'no_blanks' , 'format' : border_format} )
worksheet.conditional_format( 'A25:C25' , { 'type' : 'no_blanks' , 'format' : border_format} )
worksheet.conditional_format( 'A29:B30' , { 'type' : 'no_blanks' , 'format' : border_format} )

title_format = workbook.add_format()
title_format.set_bold()
title_format.set_font_size(24)
worksheet.write(0, 0, 'Upward Feedback Report', title_format)
worksheet.write(2, 0, 'Name:')
worksheet.write(2, 1, 'Jacky')

worksheet.write(6, 0, 'Core Values')
worksheet.write(7, 0, 'Q1')
worksheet.write(7, 1, 'Complementary Team')
worksheet.write(8, 0, 'Q2')
worksheet.write(8, 1, 'Ownership')
worksheet.write(9, 0, 'Q3')
worksheet.write(9, 1, 'People')
worksheet.write(10, 0, 'Q4')
worksheet.write(10, 1, 'Integrity')
worksheet.write(11, 0, 'Q5')
worksheet.write(11, 1, 'Customer')
worksheet.write(12, 0, 'Q6')
worksheet.write(12, 1, 'Continuous Improvement')
worksheet.write(13, 1, 'Average')
worksheet.write(15, 0, 'Q7')
worksheet.write(15, 1, 'Core Values All')
worksheet.write(17, 0, 'Leadership')
worksheet.write(18, 0, 'Q8')
worksheet.write(18, 1, 'Manage Team')
worksheet.write(19, 0, 'Q9')
worksheet.write(19, 1, 'Embed Target Behaviour')
worksheet.write(20, 0, 'Q10')
worksheet.write(20, 1, 'Inspiring Team')
worksheet.write(21, 0, 'Q11')
worksheet.write(21, 1, 'Effective Feedback')
worksheet.write(22, 1, 'Average')
worksheet.write(24, 0, 'Q12')
worksheet.write(24, 1, 'Leadership All')
worksheet.write(27, 0, 'Manager Rating')
worksheet.write(28, 0, 'Core Values')
worksheet.write(29, 0, 'Leadership')




#worksheet.insert_image('F2', 'download.png',{'x_scale':0.5,'y_scale':0.5})

workbook.close()