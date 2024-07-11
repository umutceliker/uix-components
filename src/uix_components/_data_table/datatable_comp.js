

event_handlers["init-data-table"] = function (id, value, event_name) {
    dataTable_config = {
        data: value.data,
        columns: value.columns,
        columnDefs: [],
        pageLength: 20,
    };
    
    dataTable_config = Object.assign(dataTable_config, value.dataTable_config);

    const table=new DataTable("#"+id, dataTable_config);

    if (value.isEditable) {
        editableRow(id);
        table.on('click', 'td', function(evt) {
            const dtRow = evt.target.closest('tr');
            const data = table.row(dtRow).data();
            const index = table.row(dtRow).index();
            clientEmit(value.dialog_id, {
                "data": data,
                "index": index,
            }, "info_dialog_open");
           
    })
    }

    document.getElementById(id).table = table;

}

event_handlers["reload"] = function (id, value, event_name) {
    const table = document.getElementById(id).table;
    const currentPage = table.page();

    tableData = value.data;
        
    table.clear().rows.add(tableData).draw();
    table.page(currentPage).draw(false);
    editableRow(id);
}

function editableRow(id){
        const rows=document.querySelectorAll("#"+id+" > tbody > tr");    
        rows.forEach(row => {
            row.style.cursor = 'pointer';
        });
        
}