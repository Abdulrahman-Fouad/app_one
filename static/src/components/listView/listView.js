/* @odoo-module */

import {Component, useState, onWillUnmount} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";


export class ListViewAction extends Component {
    static template = "app_one.ListView";

    setup(){
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.state = useState({'records': []});
        this.loadRecords();

        this.intervalId = setInterval(()=> {this.loadRecords();}, 3000);
        onWillUnmount(() => {clearInterval(this.intervalId);});
    };

//    async loadRecords(){
//        const result = await this.orm.searchRead("property",[],[]);
//        console.log(result);
//        this.state.records = result;
//    }

    async loadRecords(){
        const result = await this.rpc("/web/dataset/call_kw",{
                model: 'property',
                method: 'search_read',
                args: [[]],
                kwargs: {fields: ['id', 'name', 'postcode', 'date_availability']},
            }
        );
        console.log(result);
        this.state.records = result;
    }

    async createRecord() {
        const result = await this.rpc("/web/dataset/call_kw",{
                model: 'property',
                method: 'create',
                args: [{
                    name: "Property B3",
                    postcode: "75314",
                    description: "Property B1 description",
                    owner_id: 2,
                    bedrooms: 4,
                    living_area: 320
                }],
                kwargs: {},
            }
        );
        this.loadRecords();
    };

    async deleteRecord(recordId) {
         const result = await this.rpc("/web/dataset/call_kw",{
            model: 'property',
            method: 'unlink',
            args: [recordId],
            kwargs: {},
            }
        );
        this.loadRecords();
    };

}

registry.category("actions").add("app_one.action_list_view", ListViewAction);