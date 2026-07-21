import os

path = r'c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\js\utils.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

export_fn = """
utils.exportTableToCSV = function(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    let csv = [];
    for (let i = 0; i < table.rows.length; i++) {
        let row = [], cols = table.rows[i].querySelectorAll('td, th');
        
        let limit = cols.length;
        if (i === 0 && cols[limit - 1] && cols[limit - 1].innerText.trim().toLowerCase() === 'actions') {
            limit = cols.length - 1;
        } else if (i > 0 && table.rows[0].querySelectorAll('th').length > 0) {
            const headerCols = table.rows[0].querySelectorAll('th');
            if (headerCols[headerCols.length - 1].innerText.trim().toLowerCase() === 'actions') {
                limit = cols.length - 1;
            }
        }
        
        for (let j = 0; j < limit; j++) {
            let data = cols[j].innerText.replace(/(\\r\\n|\\n|\\r)/gm, '').replace(/\"/g, '\"\"').trim();
            row.push('\"' + data + '\"');
        }
        csv.push(row.join(','));
    }
    const csvFile = new Blob([csv.join('\\n')], {type: 'text/csv'});
    const downloadLink = document.createElement('a');
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
};
"""

if 'exportTableToCSV' not in content:
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + export_fn)
    print('Added exportTableToCSV to utils.js')
else:
    print('Already exists in utils.js')
