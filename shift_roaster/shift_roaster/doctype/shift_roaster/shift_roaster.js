// Copyright (c) 2024, Sufyan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shift Roaster", {
	refresh(frm) {
        frm.fields_dict['shifts'].grid.wrapper.find('.grid-add-row').hide();
        frm.fields_dict['shifts'].grid.wrapper.find('.grid-remove-rows').hide();
	},

    onload: function(frm) {
        frm.fields_dict['shifts'].grid.wrapper.find('.grid-add-row').hide();
        frm.fields_dict['shifts'].grid.wrapper.find('.grid-remove-rows').hide();
        frm.refresh_field("shifts");
    },


    get_employees: async function(frm) {

        await frappe.call({
            method : "shift_roaster.shift_roaster.api.api.get_emloyees" ,
            args : {
                branch : frm.doc.branch || null ,
                department : frm.doc.department || null ,
                employee : frm.doc.employee || null ,
            } ,
            async : false ,
            callback : function (r) {
                if (r.message)
                {
                    frm.clear_table("employees");
                    r.message.forEach(employee => {
                        let row = frm.add_child("employees");
                        frappe.model.set_value(row.doctype, row.name, "employee", employee.name) ;
                    });    
                    frm.refresh_field("employees");
                    // frm.save()
                }
            },
        })

    },



    from_date: async function(frm) {

        if (frm.doc.from_date && frm.doc.frequency)
        {
            // console.log("yes");
            await frappe.call({
                method : "shift_roaster.shift_roaster.api.api.get_dates" ,
                args : {
                    from_date : frm.doc.from_date ,
                    frequency : frm.doc.frequency ,
                },
                async : false ,
                callback : function(r)
                {
                    if (r.message)
                    {
                        let dates = r.message.dates ;
                        let days = r.message.days ;
                        frm.clear_table("shifts");

                        for (let i=0; i<dates.length ; i++)
                        {
                            let row = frm.add_child("shifts") ;
                            row.date = dates[i] ;
                            row.day = days[i] ;
                        }

                        frm.refresh_field("shifts");
                    }
                }

            })
        }
        else {
            frm.clear_table("shifts");
            frm.refresh_field("shifts");
        }

        frm.fields_dict['shifts'].grid.wrapper.find('.grid-add-row').hide();
        frm.fields_dict['shifts'].grid.wrapper.find('.grid-remove-rows').hide();

    },



    frequency: async function(frm) {

        if (frm.doc.from_date && frm.doc.frequency)
        {
            await frappe.call({
                method : "shift_roaster.shift_roaster.api.api.get_dates" ,
                args : {
                    from_date : frm.doc.from_date ,
                    frequency : frm.doc.frequency ,
                },
                async : false ,
                callback : function(r)
                {
                    if (r.message)
                    {
                        let dates = r.message.dates ;
                        let days = r.message.days ;
                        frm.clear_table("shifts");

                        for (let i=0; i<dates.length ; i++)
                        {
                            let row = frm.add_child("shifts") ;
                            row.date = dates[i] ;
                            row.day = days[i] ;
                        }

                        frm.refresh_field("shifts");
                        
                    }
                }

            })
        }
        else {
            frm.clear_table("shifts");
            frm.refresh_field("shifts");
        }

        frm.fields_dict['shifts'].grid.wrapper.find('.grid-add-row').hide();
        frm.fields_dict['shifts'].grid.wrapper.find('.grid-remove-rows').hide();

    },



});
