function doPost(e) {
    var data = JSON.parse(e.postData.contents);
    var jsonData = data.json_data;
    var tag = data.tag;
    var fileName = data.file_name;
    
    var sheet = SpreadsheetApp.openById('スプレッドシートのID').getSheetByName('シート名');
    
    var storeData = jsonData.store;
    var transactionData = jsonData.transaction;
    var itemsData = jsonData.items;
    var totalData = jsonData.total;
    var paymentData = jsonData.payment;
    
    for (var i = 0; i < itemsData.length; i++) {
      var itemData = itemsData[i];
      var rowData = [
        tag,
        fileName,
        storeData.name,
        transactionData.date,
        transactionData.time,
        itemData.item_name,
        itemData.unit_price,
        itemData.quantity,
        itemData.unit,
        itemData.category,
        itemData.total_price,
        totalData.amount,
        totalData.points_earned,
        totalData.points_used,
        paymentData.payment_method
      ];
      sheet.appendRow(rowData);
    }
    
    return ContentService.createTextOutput('Data received successfully');
  }