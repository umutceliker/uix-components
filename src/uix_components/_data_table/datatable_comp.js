

event_handlers["init-data-table"] = function (id, value, event_name) {
    document.onkeydown = function(e) {
        var targetElement;
        switch (e.keyCode) {
            case 37:
                targetElement = document.querySelector('.previous');
                break;
            case 38:
                targetElement = document.querySelector('.first');
                break;
            case 39:
                targetElement = document.querySelector('.next');
                break;
            case 40:
                targetElement = document.querySelector('.last');
                break;
        }

        if (targetElement) {
            var clickEvent = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            targetElement.dispatchEvent(clickEvent);
        }
    };
    dataTable_config = {
        data: value.data,
        columns: value.columns,
        columnDefs: [],
        pageLength: 20,
        
    };
    
    dataTable_config = Object.assign(dataTable_config, value.dataTable_config);

    const table=new DataTable("#"+id, dataTable_config);

    document.getElementById(id).table = table;
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




}

event_handlers["reload"] = function (id, value, event_name) {
    const table = document.getElementById(id).table;
    const currentPage = table.page();

    tableData = value.data;
        
    table.clear().rows.add(tableData).draw();
    table.page(currentPage).draw(false);
    editableRow(id);
}

function editableRow(id,table){
        const rows=document.querySelectorAll("#"+id+" > tbody > tr");    
        rows.forEach(row => {
            row.style.cursor = 'pointer';
        });
        
}