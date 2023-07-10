$(document).ready(function() {
    var table = $('#table1').DataTable({
        responsive: true,
        paging:false,
        "bScrollInfinite": true,
        "bScrollCollapse": true,
        "scrollY": "320px",
        columnDefs: [
            { targets: 0, responsivePriority: 1 ,sortable:true},  // Kolom pertama dengan prioritas tampilan tinggi
            { targets: -1, responsivePriority: 2 },
            { targets:'_all',sortable:false}  // Kolom terakhir dengan prioritas tampilan rendah
        ]
    });
    var table2 = $('#table2').DataTable({
        responsive: true,
        paging: false,
        "bScrollInfinite": true,
        "bScrollCollapse": true,
        "scrollY": "500px",
        searching: false,
        ordering:false,
        columnDefs: [
            { targets: 0, responsivePriority: 1 },
            { targets: 1, responsivePriority: 2 },

        ]
    });

    var table_pengajar = $('#table-pengajar').DataTable({
        responsive: true,
        paging:false,
        fixedHeader: true,
        fixedColumns: true,
        "bScrollInfinite": true,
        "bScrollCollapse": true,
        "scrollY": "350px",
        ordering:false,
        columnDefs: [
            { targets: 0, responsivePriority: 1},
            { targets: 1, responsivePriority: 2 }
        ]
    });

    var table_tugas = $('#table-tugas').DataTable({
        responsive: true,
   
        columnDefs: [
            { targets: 2, responsivePriority: 1 ,sortable:true},  // Kolom pertama dengan prioritas tampilan tinggi
            { targets: -2, responsivePriority: 2,sortable:true },
            { target:-1,sortable:false} // Kolom terakhir dengan prioritas tampilan rendah
        ]
    });
    
    var table_histori_transaksi = $('#table-histori-transaksi').DataTable({
        responsive: true,
        "bScrollInfinite": true,
        "bScrollCollapse": true,
        "scrollY": "250px",
        columnDefs: [
            { targets: 0, responsivePriority: 1 },
            { targets: 2, responsivePriority: 2 },

        ]
    });
});
