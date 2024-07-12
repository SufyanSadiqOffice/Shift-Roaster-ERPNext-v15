




import frappe
import json
from frappe.model.mapper import get_mapped_doc
from frappe.utils import add_days, getdate
from datetime import datetime




@frappe.whitelist()
def get_emloyees(branch , department , employee) :
    
    values = {
        'branch' : branch ,
        'department' : department ,
        'employee' : employee ,
    }
    
    if employee :
        emp_list = frappe.db.sql("""
            SELECT
                emp.name

            FROM
                `tabEmployee` emp
            WHERE
                emp.name = %(employee)s
                AND emp.status = 'Active'                 
        """, values=values , as_dict=1)

    else :
        if branch and department :
            emp_list = frappe.db.sql("""
            SELECT
                emp.name
            FROM
                `tabEmployee` emp
            WHERE
                emp.branch = %(branch)s
                AND emp.department = %(department)s
                AND emp.status = 'Active'                                       
            """, values=values , as_dict=1)
            
        elif branch :
            emp_list = frappe.db.sql("""
            SELECT
                emp.name
            FROM
                `tabEmployee` emp
            WHERE
                emp.branch = %(branch)s
                AND emp.status = 'Active'                                          
            """, values=values , as_dict=1)
        
        elif department :            
            emp_list = frappe.db.sql("""
            SELECT
                emp.name
            FROM
                `tabEmployee` emp
            WHERE
                emp.department = %(department)s
                AND emp.status = 'Active'                     
            """, values=values , as_dict=1)

        else :
            emp_list = frappe.db.sql("""
            SELECT
                emp.name
            FROM
                `tabEmployee` emp
            WHERE
                emp.status = 'Active'                                             
            """, values=values , as_dict=1)                     

    return emp_list





@frappe.whitelist()
def get_dates(from_date , frequency) :
    
    dates = []
    days = []
    date = from_date

    if frequency == 'Weekly' :
        for i in range(7) :
            dates.append(date)
            datetime_obj = frappe.utils.get_datetime(date)
            day = frappe.utils.get_weekday(datetime_obj)
            days.append(day)
            date = frappe.utils.add_days(date, 1)

    elif frequency == 'Bi Weekly' :
        for i in range(14) :
            dates.append(date)
            datetime_obj = frappe.utils.get_datetime(date)
            day = frappe.utils.get_weekday(datetime_obj)
            days.append(day)
            date = frappe.utils.add_days(date, 1)


    if frequency == 'Monthly' :        
        for i in range(28) :
            dates.append(date)
            datetime_obj = frappe.utils.get_datetime(date)
            day = frappe.utils.get_weekday(datetime_obj)
            days.append(day)
            date = frappe.utils.add_days(date, 1)


    return {"dates": dates, "days": days}       



