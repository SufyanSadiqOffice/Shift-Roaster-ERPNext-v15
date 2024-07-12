# Copyright (c) 2024, Sufyan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShiftRoaster(Document):

    def before_save(self):

        freq_days = 0
        if self.frequency == 'Weekly':
            freq_days = 7
        elif self.frequency == 'Bi Weekly':
            freq_days = 14
        elif self.frequency == 'Monthly':
            freq_days = 28



        # To Date must be greater than frequency respective date
        if self.is_replicated:
            if self.frequency == 'Weekly':
                t_date = frappe.utils.add_days(self.from_date, 7)
            elif self.frequency == 'Bi Weekly':
                t_date = frappe.utils.add_days(self.from_date, 14)
            elif self.frequency == 'Monthly':
                t_date = frappe.utils.add_days(self.from_date, 28)

            if self.to_date < t_date:
                frappe.throw("To Date must be after Frequency respective date.")



        shifts = []
        from_dates = []
        to_dates = []
        shifttable1 = []
        shifttable2 = []
        shifttable = []
        shifttable2.extend(self.shifts)
        shifttable1.extend(shifttable2)
        
		

        if self.is_replicated :
            days_diff = frappe.utils.date_diff(self.to_date , self.from_date) + 1
            div = int( days_diff / freq_days )
            mod = days_diff % freq_days   
            # frappe.msgprint(str(div))
            # frappe.msgprint(str(mod))

            for i in range(1,div) :
                shifttable1.extend(shifttable2)
            
            for i in range(0, mod) :
                shifttable1.append(shifttable2[i])

            shifttable.extend(shifttable1)

            for i in range(0, len(shifttable)) :
                shifttable[i].date = frappe.utils.add_days(self.from_date , i)
                # frappe.msgprint(str(i))
                # frappe.msgprint(str(self.from_date))
                

            # for row in shifttable1 :
                # frappe.msgprint(str(row.date) + " " + str(row.day) + " " + str(row.shift_type))



		



        if self.shifts:
            current_shift = None
            current_from_date = None
            current_to_date = None

            for row in self.shifts:
                if row.shift_type:
                    if current_shift is None:
                        current_shift = row.shift_type
                        current_from_date = row.date
                        current_to_date = row.date
                    elif row.shift_type == current_shift:
                        current_to_date = row.date
                    else:
                        if current_shift:
                            shifts.append(current_shift)
                            from_dates.append(current_from_date)
                            to_dates.append(current_to_date)
                        current_shift = row.shift_type
                        current_from_date = row.date
                        current_to_date = row.date
                else:
                    if current_shift:
                        next_shift = None
                        next_index = self.shifts.index(row) + 1
                        if next_index < len(self.shifts):
                            next_shift = self.shifts[next_index].shift_type
                        if next_shift != current_shift:
                            shifts.append(current_shift)
                            from_dates.append(current_from_date)
                            to_dates.append(current_to_date)
                            current_shift = None
                            current_from_date = None
                            current_to_date = None

            if current_shift:
                shifts.append(current_shift)
                from_dates.append(current_from_date)
                to_dates.append(current_to_date)
                
            # frappe.msgprint(str(shifts))
            # frappe.msgprint(str(from_dates))
            # frappe.msgprint(str(to_dates))




