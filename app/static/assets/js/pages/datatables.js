$(document).ready(function() {
    var table = $('#table1').DataTable({
        responsive: true,
        paging:false,
        "bScrollInfinite": true,
        "bScrollCollapse": true,
        "scrollY": "500px",
        searching: false,
        rowReorder: {
            selector: 'td:nth-child(2)'
        },
        columnDefs: [
            { targets: 0, responsivePriority: 1 ,sortable:true},  // Kolom pertama dengan prioritas tampilan tinggi
            { targets: -1, responsivePriority: 2 },
            { targets:'_all',sortable:false}  // Kolom terakhir dengan prioritas tampilan rendah
        ]
    });
});
